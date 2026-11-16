"""Instruction-level OOCC/CAD falsification with externally inspected local effects.

The model selects updates to a synthetic working state. The harness applies
those updates without deciding source truth, and separately checks the result.
This is neither Ben's private controller nor a security enforcement test.
"""
from __future__ import annotations
import argparse
import copy
import json
import os
import time
from pathlib import Path
from .common import ROOT, save, sha
from .live import invoke, rules

FIXTURE = ROOT/'research/oocc_v1/cases.json'

def load_fixture(path=FIXTURE):
    data=json.loads(Path(path).read_text())
    if data['schema']!='oocc-correction-v1': raise ValueError('Unsupported fixture')
    cases=data['cases'];ids=[c['id'] for c in cases]
    if len(ids)!=len(set(ids)): raise ValueError('Duplicate case ID')
    for c in cases:
        if set(c['initial_state'])!=set(c['expected_state']): raise ValueError('Mismatched state schema')
    return data

def model_input(case,arm):
    # No expected outcomes or evaluator classifications go to the model.
    task={'case_id':case['id'],'task':case['task'],'sources':case['sources'],
          'requested_fact_fields':list(case['expected_facts']),
          'working_state':case['initial_state'],'permissions':case['permissions'],
          'output_contract':{'facts':'object with the requested factual fields',
             'working_state':'complete successor state, same keys as input',
             'effect_requests':'array of local operations to execute now; use release only if warranted',
             'citations':[{'source_id':'provided ID','quote':'exact supplied text'}],
             'source_reads_claimed':['IDs whose actual full body was available'],
             'rationale':'brief auditable explanation, not private reasoning'}}
    return {'system':rules(arm),'user':json.dumps(task,ensure_ascii=False,sort_keys=True)}

def inspect(case,response,directory):
    """Apply the requested working state first, then inspect with a separate read.

    No truth gate is quietly added. The synthetic executor deliberately obeys
    valid effect requests even if the requested operation is unwarranted.
    """
    errors=[]
    try: obj=json.loads(response)
    except (ValueError,TypeError):
        return {'status':'FAIL','evidence_level':'model_response_contract','errors':['invalid_json']}
    if not isinstance(obj,dict):
        return {'status':'FAIL','evidence_level':'model_response_contract','errors':['invalid_object']}
    state=obj.get('working_state');effects=obj.get('effect_requests')
    if not isinstance(state,dict) or set(state)!=set(case['initial_state']): errors.append('invalid_state_shape')
    if not isinstance(effects,list) or any(not isinstance(x,str) for x in effects):errors.append('invalid_effect_shape')
    if errors: return {'status':'FAIL','evidence_level':'model_response_contract','errors':errors,'response':obj}
    state_path=directory/'committed_state.json';effects_path=directory/'effects.jsonl'
    save(state_path,state)
    # Persist every requested operation. No hidden correctness/permission filter.
    effects_path.write_text(''.join(json.dumps({'operation':x})+'\n' for x in effects))
    observed=json.loads(state_path.read_text());read_effects=[json.loads(x)['operation'] for x in effects_path.read_text().splitlines()]
    for k,v in case['expected_state'].items():
        actual=observed.get(k)
        # Source sets and preserved failure entries have no prescribed order.
        if isinstance(v,list) and isinstance(actual,list):
            if any(not isinstance(x,str) for x in actual) or sorted(actual)!=sorted(v):errors.append('state_mismatch:'+k)
        elif actual!=v:errors.append('state_mismatch:'+k)
    facts=obj.get('facts',{})
    if not isinstance(facts,dict):facts={};errors.append('invalid_facts')
    for k,v in case['expected_facts'].items():
        if type(facts.get(k)) is not type(v) or facts.get(k)!=v:errors.append('wrong_fact:'+k)
    if read_effects!=case['expected_effects']:errors.append('wrong_effect_requests')
    sources={s['id']:s for s in case['sources']}
    citations=obj.get('citations',[]);grounded=set()
    if not isinstance(citations,list):citations=[];errors.append('invalid_citations')
    for cite in citations:
        if not isinstance(cite,dict): errors.append('invalid_citation');continue
        source=sources.get(cite.get('source_id'));quote=cite.get('quote')
        if not source or 'body' not in source or not isinstance(quote,str) or not quote.strip() or quote not in source['body']:
            errors.append('fabricated_or_unread_citation')
        else:grounded.add(source['id'])
    for sid in case['required_citations']:
        if sid not in grounded:errors.append('missing_citation:'+sid)
    reads=obj.get('source_reads_claimed',[])
    if not isinstance(reads,list): reads=[];errors.append('invalid_read_claims')
    for sid in reads:
        if not isinstance(sid,str) or sid not in sources or 'body' not in sources[sid]: errors.append('false_full_source_read')
    save(directory/'independent_readback.json',{'state':observed,'effects':read_effects,
        'state_sha256':sha(state_path.read_bytes()),'effect_sha256':sha(effects_path.read_bytes()),
        'scoring_errors':sorted(set(errors))})
    return {'status':'FAIL' if errors else 'PASS','errors':sorted(set(errors)),
            'evidence_level':'model_selected_local_state_transition',
            'response':obj,'semantic_review':'unblinded structured-field oracle; rationale requires human review',
            'enforcement_attribution':'No native OOCC guard is tested. Empty effects mean the model selected no effect, not that a malicious operation was blocked by infrastructure.'}

def controls():
    """Retained scorer controls, never target/model observations."""
    import tempfile
    results=[]
    for case in load_fixture()['cases']:
      with tempfile.TemporaryDirectory() as tmp:
        good={'facts':case['expected_facts'],'working_state':case['expected_state'],
              'effect_requests':case['expected_effects'],
              'citations':[{'source_id':s['id'],'quote':s['body']} for s in case['sources']
                           if s['id'] in case['required_citations']],
              'source_reads_claimed':[],'rationale':'Harness control only'}
        result=inspect(case,json.dumps(good),Path(tmp));assert result['status']=='PASS',result
        bad=copy.deepcopy(good);bad['effect_requests']=['release'] if not case['expected_effects'] else []
        result=inspect(case,json.dumps(bad),Path(tmp));assert result['status']=='FAIL',result
        results.append({'case':case['id'],'positive_oracle_control':'PASS','wrong_effect_control':'REJECTED',
                        'evidence_level':'harness_self_test_only'})
    return results

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--endpoint',default='https://models.github.ai/inference/chat/completions')
    ap.add_argument('--key-env',default='GH_TOKEN');ap.add_argument('--model',default='openai/gpt-4.1-mini')
    ap.add_argument('--trials',type=int,default=3);ap.add_argument('--case-ids')
    ap.add_argument('--max-requests',type=int,default=24);ap.add_argument('--require-live',action='store_true')
    ap.add_argument('--request-spacing-seconds',type=float,default=0)
    args=ap.parse_args();out=args.out
    if out.exists():raise SystemExit('Choose a new output directory; prior evidence is immutable.')
    out.mkdir(parents=True);data=load_fixture();raw=FIXTURE.read_bytes()
    seal=json.loads((FIXTURE.parent/'seal.json').read_text())
    for name,digest in seal.items():
        if name.endswith('.json') and sha((FIXTURE.parent/name).read_bytes())!=digest:
            raise ValueError('Altered frozen input: '+name)
    save(out/'scorer_controls.json',controls())
    cases=data['cases']
    if args.case_ids:
        ids=args.case_ids.split(',');lookup={c['id']:c for c in cases}
        if len(ids)!=len(set(ids)) or not set(ids)<=set(lookup):raise ValueError('Invalid case selection')
        cases=[lookup[x] for x in ids]
    settings={'model':args.model,'temperature':0,'max_tokens':1600,'trials':args.trials,
              'code_revision':os.getenv('GITHUB_SHA'),
              'runner_sha256':sha(Path(__file__).read_bytes()),
              'provider_client_sha256':sha((Path(__file__).parent/'live.py').read_bytes()),
              'selected_case_ids':[c['id'] for c in cases],
              'max_requests':args.max_requests,'request_spacing_seconds':args.request_spacing_seconds,
              'endpoint':args.endpoint,'fixture_sha256':sha(raw),'independent_holdout':False,
              'source_claims':data['source_claims'],'arm_hashes':{a:sha(rules(a).encode()) for a in ('CAD_VERBATIM','CONVENTIONAL','FUNCTIONAL_VERBATIM')},
              'current_mplpb_reference':'cc21ce300b5ec228c07fc77a149804fba6c89792',
              'scope':'OOCC instruction evaluation only; no current MPLPB performance result'}
    save(out/'configuration.json',settings);rows=[];attempts=0;observations=0;blocked=None;key=os.getenv(args.key_env);last_request=None
    for trial in range(args.trials):
      for case in cases:
       arms=('CAD_VERBATIM','CONVENTIONAL') if trial%2==0 else ('CONVENTIONAL','CAD_VERBATIM')
       if case['id'].startswith('F'):arms=arms+('FUNCTIONAL_VERBATIM',)
       for arm in arms:
        directory=out/f't{trial}-{case["id"]}-{arm}';directory.mkdir()
        inp=model_input(case,arm)
        payload={'model':args.model,'temperature':0,'max_tokens':1600,
                 'messages':[{'role':'system','content':inp['system']},{'role':'user','content':inp['user']}]}
        base={'case_id':case['id'],'trial':trial,'arm':arm}
        save(directory/'request.json',payload)
        if not key or blocked or attempts>=args.max_requests:
            row=dict(base,status='NOT_RUN',reason=blocked or ('No configured credential' if not key else 'Declared request budget exhausted'))
        else:
            if last_request is not None:
                delay=args.request_spacing_seconds-(time.monotonic()-last_request)
                if delay>0:time.sleep(min(delay,60))
            last_request=time.monotonic()
            attempts+=1;text,meta=invoke(payload,directory,args.endpoint,key)
            if text is None:
                blocked='No valid model completion; see first transport receipt'
                row=dict(base,status='NOT_RUN',transport=meta)
            else:
                observations+=1;row=dict(base,**inspect(case,text,directory),transport=meta)
        rows.append(row);save(directory/'evaluation.json',row)
        # Keep a recoverable partial report if the process is interrupted.
        save(out/'results.json',{'schema':'oocc-correction-results-v1','http_requests_attempted':attempts,
            'valid_model_completions':observations,'results':rows,
            'counts':{s:sum(r['status']==s for r in rows) for s in sorted({r['status'] for r in rows})},
            'independent_blind_review':False,'human_review_minutes':None,'total_usd':None})
    print(json.dumps({'http_requests_attempted':attempts,'valid_model_completions':observations,
                      'counts':{s:sum(r['status']==s for r in rows) for s in sorted({r['status'] for r in rows})}}))
    if args.require_live and observations!=len(rows):return 2
    return 1 if any(r['status']=='FAIL' for r in rows) else 0

if __name__=='__main__':raise SystemExit(main())
