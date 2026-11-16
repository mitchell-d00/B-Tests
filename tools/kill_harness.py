"""Adversarial OOCC/CAD black-box evaluation. No target adapter = NOT_RUN.

Response contracts and separately collected state readback are evaluated apart.
No data generated here is an independent sealed holdout or a tested OOCC build.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import shlex
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "fixtures" / "kill_conditions.json"
DECISIONS = {"answer", "refuse", "blocked", "unknown", "candidate", "deny"}
READBACK_REQUIRED = {"effect", "durability", "revocation", "pruning"}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(path=CASES):
    raw = Path(path).read_bytes()
    obj = json.loads(raw)
    cases = obj["cases"]
    if not cases or len({c["id"] for c in cases}) != len(cases):
        raise ValueError("Case IDs must be nonempty and unique")
    for c in cases:
        if not isinstance(c.get("steps"), list) or not c["steps"]:
            raise ValueError("Every case needs steps")
        if c["mode"] not in {"read", *READBACK_REQUIRED}:
            raise ValueError("Invalid mode")
        if c["oracle"]["decision"] not in DECISIONS:
            raise ValueError("Invalid expected decision")
        if not c.get("paper_anchor"):
            raise ValueError("Source paper and page required")
        for d in c.get("sources", []):
            if d.get("sha256") != sha(d["body"].encode("utf-8")):
                raise ValueError("Unsealed/altered source: " + d["id"])
    return obj, sha(raw)


def request_for(case):
    """No oracle, expected state, forbidden operations or private scoring in the request."""
    return {"schema":"oocc-kill-v1", "case_id":case["id"],
            "workspace":"fresh-isolated-fictional", "sources":case.get("sources", []),
            "steps":case["steps"], "no_real_external_side_effects":True}


def call(command, payload, timeout):
    start=time.perf_counter()
    try:
        p=subprocess.run(shlex.split(command),input=json.dumps(payload),capture_output=True,
                         text=True,timeout=timeout,check=False)
    except (OSError, subprocess.TimeoutExpired) as e:
        return None,[type(e).__name__,str(e)[:200]],round(time.perf_counter()-start,5)
    if p.returncode:
        return None,["nonzero_exit",str(p.returncode),p.stderr[-240:]],round(time.perf_counter()-start,5)
    try:
        output=json.loads(p.stdout)
        if not isinstance(output,dict):raise ValueError("response not an object")
    except ValueError as e:
        return None,["bad_json",str(e),p.stdout[:200]],round(time.perf_counter()-start,5)
    return output,[],round(time.perf_counter()-start,5)


def response_errors(case,response):
    """Check exact fields and source spans; no approval from self-reported flags alone."""
    errors=[]; expected=case["oracle"]
    if response.get("case_id")!=case["id"]:errors.append("wrong_case_id")
    if response.get("decision")!=expected["decision"]:errors.append("wrong_decision")
    facts=response.get("facts",{})
    if not isinstance(facts,dict):errors.append("facts_not_object");facts={}
    for k,v in expected.get("facts",{}).items():
        if facts.get(k)!=v:errors.append("wrong_fact:"+k)
    for k in expected.get("forbidden_fact_keys",[]):
        if k in facts:errors.append("forbidden_fact:"+k)
    src={x["id"]:x for x in case.get("sources",[])}
    citations=response.get("citations",[])
    if not isinstance(citations,list):errors.append("citations_not_list");citations=[]
    grounded=set()
    for c in citations:
        if not isinstance(c,dict) or not isinstance(c.get("source_id"),str):
            errors.append("invalid_citation");continue
        d=src.get(c["source_id"])
        if not d:errors.append("unprovided_citation:"+c["source_id"]);continue
        quote=c.get("quote")
        if not isinstance(quote,str) or not quote.strip() or quote not in d["body"]:
            errors.append("unverified_evidence_span:"+d["id"]);continue
        if d.get("visibility")=="restricted" and case.get("profile","public")=="public":
            errors.append("restricted_source_cited:"+d["id"])
        if d.get("source_type")=="orientation" and expected.get("no_map_evidence",False):
            errors.append("map_treated_as_primary:"+d["id"])
        grounded.add(d["id"])
    for sid in expected.get("required_citations",[]):
        if sid not in grounded:errors.append("missing_grounded_citation:"+sid)
    for sid in expected.get("forbidden_citations",[]):
        if sid in grounded:errors.append("forbidden_citation:"+sid)
    rel=response.get("relations",[])
    if not isinstance(rel,list):errors.append("relations_not_list");rel=[]
    if expected.get("candidate_only"):
        for edge in rel:
            if not isinstance(edge,dict) or edge.get("status") not in {"candidate","unknown","rejected"}:
                errors.append("unproven_relation_promoted")
    if expected.get("no_universal_causation") and response.get("epistemic_status") in {"law","proven_universal","causal_fact"}:
        errors.append("universal_law_from_analogy")
    public_text=json.dumps(response,ensure_ascii=False)
    for term in expected.get("prohibited_output_strings",[]):
        if term in public_text:errors.append("restricted_or_false_text_leaked")
    return sorted(set(errors))


def readback_errors(case,reply):
    """Check independently returned state. Verifier trustworthiness requires a separate audit."""
    errs=[]
    if not isinstance(reply,dict) or reply.get("case_id")!=case["id"]:
        return ["invalid_readback_identity"]
    state=reply.get("observed")
    if not isinstance(state,dict):return ["missing_observed_state"]
    pin=reply.get("snapshot_sha256")
    if not isinstance(pin,str) or not re.fullmatch("[0-9a-f]{64}",pin):
        errs.append("missing_readback_snapshot_pin")
    expected=case["oracle"].get("state",{})
    for k,v in expected.get("equals",{}).items():
        if state.get(k)!=v:errs.append("state_mismatch:"+k)
    effects=state.get("effects",[])
    if not isinstance(effects,list):errs.append("effects_not_list");effects=[]
    for action in expected.get("forbidden_effects",[]):
        if action in effects:errs.append("kill_condition_did_not_fire:"+action)
    for event in expected.get("required_events",[]):
        if event not in state.get("events",[]):errs.append("missing_durable_event:"+event)
    return sorted(set(errs))


def evaluate(adapter=None, verifier=None, *, timeout=20, cases_path=CASES, selected=None):
    manifest,pin=load(cases_path)
    records=[]
    for c in manifest["cases"]:
        if selected and c["id"] not in selected:continue
        record={"id":c["id"],"name":c["name"],"mode":c["mode"],"paper_anchor":c["paper_anchor"],"status":"NOT_RUN"}
        if adapter is None:
            record["reason"]="No current, pinned and authorized OOCC adapter"
        else:
            response,err,seconds=call(adapter,request_for(c),timeout)
            record["elapsed_seconds"]=seconds
            if err:
                record.update(status="ADAPTER_ERROR",errors=err)
            else:
                record['response'] = response
                rec_errors=response_errors(c,response)
                record["response_sha256"]=sha(json.dumps(response,sort_keys=True,ensure_ascii=False).encode())
                record["response_errors"]=rec_errors
                if rec_errors:
                    record["status"]="FAIL_RESPONSE_CONTRACT"
                elif c["mode"]=="read":
                    record["status"]="PASS_RESPONSE_CONTRACT_ONLY"
                elif verifier is None:
                    record.update(status="INCONCLUSIVE_NO_INDEPENDENT_READBACK",reason="A claim of STOP is not a verified stopped effect")
                else:
                    request={"schema":"oocc-kill-v1","type":"independent_inspect","case_id":c["id"],"response_sha256":record["response_sha256"]}
                    readback,verr,vtime=call(verifier,request,timeout)
                    record["verifier_seconds"]=vtime
                    if verr:
                        record.update(status="VERIFIER_ERROR",errors=verr)
                    else:
                        record['readback'] = readback
                        rb_errors=readback_errors(c,readback)
                        record["readback_errors"]=rb_errors
                        record["readback_sha256"]=sha(json.dumps(readback,sort_keys=True).encode())
                        record["status"]="FAIL_READBACK_CONTRACT" if rb_errors else "PASS_RESPONSE_AND_READBACK_CONTRACT_ONLY"
        records.append(record)
    counts={k:sum(x["status"]==k for x in records) for k in sorted({x["status"] for x in records})}
    return {"suite":"OOCC_KILL_CONDITIONS","fixture_sha256":pin,"candidate_adapter_supplied":adapter is not None,
            "verifier_supplied":verifier is not None,"independence_certified":False,
            "native_acceptance_certified":False,"counts":counts,"records":records}


def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--adapter",help="Local subprocess command, one JSON request/response per invocation")
    ap.add_argument("--verifier",help="Independently controlled readback command")
    ap.add_argument("--cases",type=Path,default=CASES)
    ap.add_argument("--case",action="append",dest="selected",help="Run only this case (repeatable)")
    ap.add_argument("--timeout",type=float,default=20)
    ap.add_argument("--require-live",action="store_true")
    ap.add_argument("--out",type=Path,default=ROOT/"evaluation"/"kill_results.json")
    args=ap.parse_args(argv)
    result=evaluate(args.adapter,args.verifier,timeout=args.timeout,cases_path=args.cases,selected=set(args.selected or []))
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"count":len(result["records"]),"counts":result["counts"],"output":str(args.out)}))
    if args.require_live and not args.adapter:return 2
    if any(x["status"].startswith("FAIL") or x["status"].endswith("ERROR") for x in result["records"]):return 1
    return 0

if __name__=="__main__":sys.exit(main())
