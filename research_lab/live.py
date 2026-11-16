"""Real recorded OpenAI-compatible requests, with no scripted AI responses.

No credentials => NOT_RUN. A server error is not an architecture failure.
Each call has a new messages array; no previous provider conversation is reused.
The same task, evidence, output contract and budgets apply to both treatments.
"""
from __future__ import annotations
import argparse
import json
import os
import time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from .common import ROOT, save, sha

BASELINE = '''Maintain a useful project handoff using ordinary source governance.
Track current work, original documents and revisions, decisions, uncertainty,
unresolved disagreements, failed attempts, dependencies, permissions and next steps.
Check originals when needed. Keep authorization distinct from factual support.
Correct mistaken interpretations when stronger evidence appears. Distinguish source
statements from inference, and similar ideas from demonstrated causal influence.
Keep corrections and rejected alternatives recoverable. Ask or abstain when the
available evidence is insufficient. Account for review effort and access limits.'''

def rules(arm):
    if arm=='CONVENTIONAL': return BASELINE
    if arm=='FUNCTIONAL_VERBATIM':
        data=json.loads((ROOT/'research/oocc_v1/functional_verbatim.json').read_text())
        return '\n\n'.join(f'SOURCE {p["source"]}, PDF PAGE {p["pdf_page"]}\n'+p['text'] for p in data['passages'])
    if arm!='CAD_VERBATIM': raise ValueError('Unknown instruction arm')
    data=json.loads((ROOT/'research/frozen/cad_verbatim.json').read_text())
    return '\n\n'.join(f'SOURCE {p["source"]}, PDF PAGE {p["pdf_page"]}\n'+p['text'] for p in data['passages'])

def request(system,user,model,seed,max_tokens=1800):
    return {'model':model,'messages':[{'role':'system','content':system},
                                     {'role':'user','content':user}],
            'temperature':0,'seed':seed,'max_tokens':max_tokens}

def invoke(payload,directory,endpoint,key):
    """Retain full provider response, including failed/invalid output. No retries hidden."""
    save(directory/'request.json',payload)
    start=time.perf_counter();raw=b''
    try:
        req=Request(endpoint,data=json.dumps(payload).encode(),method='POST',
                    headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
        with urlopen(req,timeout=60) as r:
            raw=r.read(4_000_001);http_status=r.status
        if len(raw)>4_000_000: raise ValueError('Response exceeds retained-output limit')
        (directory/'response.raw').write_bytes(raw)
        body=json.loads(raw);choice=body['choices'][0];content=choice['message']['content']
        if not isinstance(content,str): raise ValueError('No text model output')
        meta={'status':'OBSERVED','http_status':http_status,'elapsed_seconds':time.perf_counter()-start,
              'returned_model':body.get('model'),'system_fingerprint':body.get('system_fingerprint'),
              'usage':body.get('usage'),'finish_reason':choice.get('finish_reason'),
              'request_sha256':sha(json.dumps(payload).encode()),'raw_response_sha256':sha(raw)}
        save(directory/'receipt.json',meta)
        return content,meta
    except (HTTPError,URLError,OSError,ValueError,KeyError,IndexError) as exc:
        # Error bodies may echo authentication details. Retain only sanitized
        # classification, HTTP code and any received successful response bytes.
        meta={'status':'NOT_RUN','blocker':type(exc).__name__,'http_status':getattr(exc,'code',locals().get('http_status')),
              'received_bytes':len(raw),
              'elapsed_seconds':time.perf_counter()-start,'model_output_observed':False}
        save(directory/'receipt.json',meta);return None,meta

def score_handoff(text,fixture,sources):
    try: value=json.loads(text)
    except (ValueError,TypeError): return {'status':'FAIL','level':'response_contract_only','errors':['invalid_json']}
    if not isinstance(value,dict): return {'status':'FAIL','level':'response_contract_only','errors':['invalid_object']}
    errors=[]
    facts=value.get('facts',{})
    if not isinstance(facts,dict): facts={};errors.append('facts_not_object')
    wrong_assertions=[];unknown_fields=[]
    for k,v in fixture['oracle'].items():
        if k=='invented_source_forbidden': continue
        field_value=facts.get(k)
        if field_value!=v:
            errors.append('lost_or_changed:'+k)
            if field_value is None or field_value=='unknown':unknown_fields.append(k)
            else:wrong_assertions.append(k)
    known={s['id']:s['body'] for s in sources}
    citations=value.get('citations',[])
    if not isinstance(citations,list):citations=[];errors.append('invalid_citations')
    grounded=set()
    for c in citations:
        if not isinstance(c,dict):errors.append('invalid_citation');continue
        sid=c.get('source_id');quote=c.get('quote')
        if sid not in known or not isinstance(quote,str) or not quote.strip() or quote not in known[sid]: errors.append('unrecoverable_citation')
        else:grounded.add(sid)
    for sid in ('PRIMARY','FAILURE','ALTERNATIVES'):
        if sid not in grounded: errors.append('missing_evidence:'+sid)
    # Exact structured outcomes are machine-scored; citations still need semantic
    # adjudication to establish that they justify each field, not mere overlap.
    return {'status':'FAIL' if errors else 'INCONCLUSIVE','errors':errors,
            'level':'response_contract_only','contract_met':not errors,
            'unknown_fields':unknown_fields,'wrong_assertions':wrong_assertions,
            'safe_abstention_observed':bool(unknown_fields) and not wrong_assertions,
            'semantic_review':'pending_independent_review','response':value}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=ROOT/'research/results/live')
    ap.add_argument('--model',action='append',dest='models')
    ap.add_argument('--endpoint',default=os.getenv('OPENAI_BASE_URL','https://api.openai.com/v1').rstrip('/')+'/chat/completions')
    ap.add_argument('--key-env',default='OPENAI_API_KEY');ap.add_argument('--trials',type=int,default=3)
    ap.add_argument('--require-live',action='store_true');ap.add_argument('--family',choices=['all','handoff','graph'],default='all')
    args=ap.parse_args();out=args.out
    if out.exists(): raise SystemExit('Use a new results directory; never overwrite observed runs.')
    out.mkdir(parents=True);models=args.models or ['gpt-4.1'];key=os.getenv(args.key_env)
    # Freeze exact generated source bytes inside this new run before dispatch.
    # Large graph files need not be manually copied into a checkout.
    from .freeze import compression, graphs
    inputs=out/'inputs';fixture=compression();save(inputs/'handoff.json',fixture)
    if args.family in ('all','graph'):
        for n in (10,100,1000,10000):save(inputs/f'graph_{n}.json',graphs(n))
    input_seal={p.name:sha(p.read_bytes()) for p in sorted(inputs.glob('*.json'))}
    save(inputs/'seal.json',input_seal)
    rows=[];attempts=0;completions=0;transport_blocked=False
    save(out/'run_config.json',{'models':models,'endpoint':args.endpoint,'trials':args.trials,
        'key_environment_name':args.key_env,'credential_configured':bool(key),'family':args.family,
        'temperature':0,'max_output_tokens':1800,'independent_holdout':False,
        'runner_sha256':sha(Path(__file__).read_bytes()),'input_seal':input_seal,
        'treatments':{a:sha(rules(a).encode()) for a in ('CAD_VERBATIM','CONVENTIONAL')}})
    for mi,model in enumerate(models):
      for trial in range(args.trials):
       # Alternate presentation order across trials; no model is claimed blinded.
       arms=('CAD_VERBATIM','CONVENTIONAL') if trial%2==0 else ('CONVENTIONAL','CAD_VERBATIM')
       for arm in arms:
        system=rules(arm);base=out/f'm{mi}-t{trial}-{arm}'
        if args.family in ('all','handoff'):
         summary=json.dumps(fixture['sources'],ensure_ascii=False)
         for cycle,budget in enumerate(fixture['character_budgets'],1):
          sources=fixture['sources']+([fixture['new_source']] if cycle>=fixture['correction_after_cycle'] else [])
          user=json.dumps({'task':'Prepare a project handoff from the supplied material.',
               'inherited_handoff':summary,'new_originals':[fixture['new_source']] if cycle==fixture['correction_after_cycle'] else [],
               'maximum_output_characters':budget,'output':'Return only the handoff text.'},ensure_ascii=False)
          directory=base/f'handoff-{cycle}';payload=request(system,user,model,trial)
          if not key or transport_blocked:
            save(directory/'request.json',payload)
            rows.append({'model':model,'trial':trial,'arm':arm,'family':'handoff','cycle':cycle,'status':'NOT_RUN',
                         'blocker':'Model transport unavailable; no usable completion or dependent handoff exists.'})
            continue
          attempts+=1
          text,meta=invoke(payload,directory,args.endpoint,key)
          if text is None:
            transport_blocked=True
            rows.append(dict(meta,model=model,arm=arm,trial=trial,family='handoff',cycle=cycle));continue
          completions+=1
          summary=text
          for audit_mode in ('summary_only','originals_available'):
            audit=json.dumps({'task':fixture['audit_query'],'handoff':summary,
              'accessible_originals':sources if audit_mode=='originals_available' else [],
              'output_contract':{'facts':{'test_passed':'boolean or unknown','release_authorized':'boolean or unknown','failed_approach':'string or unknown',
                'rejected_edge':'string or unknown','alternatives':['string']},'citations':[{'source_id':'string','quote':'exact source substring'}]}},ensure_ascii=False)
            attempts+=1
            answer,ameta=invoke(request(system,audit,model,trial),directory/audit_mode,args.endpoint,key)
            if answer is not None:completions+=1
            else:transport_blocked=True
            scored=score_handoff(answer,fixture,sources) if answer is not None else ameta
            rows.append(dict(scored,model=model,trial=trial,arm=arm,family='handoff',cycle=cycle,audit_mode=audit_mode,
                        output_characters=len(summary),character_budget=budget,budget_met=len(summary)<=budget,
                        summarization_receipt=meta,audit_receipt=ameta,
                        note='Loss of required information is distinct from confident falsehood. Unknown/abstention is not counted as a hallucination. An exceeded character budget does not establish robustness at that compression level.'))
            if transport_blocked:break
        if args.family in ('all','graph'):
         for n in (10,100,1000,10000):
          g=json.loads((inputs/f'graph_{n}.json').read_text())
          qs=g['questions'][:5]+g['questions'][-5:]
          # Strip all expected outcomes and hidden relation-type labels.
          user=json.dumps({'task':'Answer each query from these sources; return JSON with answers keyed by query id, decision ANSWER/REFUSE/CONFLICT, cited source IDs and exact quotations.',
                 'sources':g['projects'],'questions':[{'id':q['id'],'query':q['query']} for q in qs]},ensure_ascii=False)
          payload=request(system,user,model,trial);directory=base/f'graph-{n}'
          if not key or transport_blocked:
            save(directory/'request.json',payload)
            rows.append({'model':model,'trial':trial,'arm':arm,'family':'graph','relationships':n,'status':'NOT_RUN',
                         'blocker':'Model transport unavailable; no usable completion.'});continue
          attempts+=1
          text,meta=invoke(payload,directory,args.endpoint,key)
          if text is not None:completions+=1
          else:transport_blocked=True
          # General-purpose source reasoning is not reliably judged by substring.
          rows.append(dict(meta,model=model,trial=trial,arm=arm,family='graph',relationships=n,
             status='INCONCLUSIVE' if text is not None else 'NOT_RUN',semantic_review='pending_independent_review'))
    save(out/'results.json',{'schema':'recorded-instruction-evaluation-1','results':rows,
          'counts':{s:sum(r['status']==s for r in rows) for s in sorted({r['status'] for r in rows})},
          'http_requests_attempted':attempts,'valid_model_completions':completions,
          'human_review_minutes':None,'total_usd':None,
          'warning':'Instruction responses cannot certify blocked operations, autonomous state correction, native OOCC, or comparative superiority.'})
    print(json.dumps({'records':len(rows),'credential_configured':bool(key)}))
    return 2 if args.require_live and any(r['status']=='NOT_RUN' for r in rows) else 0

if __name__=='__main__': raise SystemExit(main())
