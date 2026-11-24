"""Seeded synthetic gate stress test; not a model experiment."""
import itertools,json,random,platform
from pathlib import Path
from run import gate

def main():
    rng=random.Random(20261124)
    decisions=['ACCEPT','REFUSE','accept','',None,True,0,[],{}]
    acks=[True,False,0,1,None,'true',[],{}]
    evidence=[True,False,1,0,None,'true',[],{}]
    proposals=[None,[],{},'ACCEPT']+[{'decision':d,'acknowledged':a} for d,a in itertools.product(decisions,acks)]
    proposals += [dict(p,override=True) for p in proposals if isinstance(p,dict)]
    pairs=list(itertools.product(proposals,evidence))
    def value(depth=0):
        vals=[None,True,False,0,1,'ACCEPT','REFUSE','true','']
        if depth<2: vals += [[value(depth+1)],{'x':value(depth+1)}]
        return rng.choice(vals)
    for _ in range(10000):
        p={k:value() for k in rng.sample(['decision','acknowledged','override'],rng.randrange(4))} if rng.randrange(2) else value()
        pairs.append((p,value()))
    failures=[]; accepted=0
    for p,e in pairs:
        expected='ACCEPT' if e is True and p in ({'decision':'ACCEPT','acknowledged':True},{'decision':'ACCEPT','acknowledged':False}) and isinstance(p,dict) and type(p.get('acknowledged')) is bool else 'REFUSE'
        try: actual=gate(p,e)
        except Exception as exc: actual=repr(exc)
        accepted+=actual=='ACCEPT'
        if actual!=expected: failures.append({'proposal':p,'evidence':e,'expected':expected,'actual':actual})
    result={'seed':20261124,'python':platform.python_version(),'structured_pairs':len(pairs)-10000,'random_pairs':10000,'total':len(pairs),'accepted':accepted,'refused_or_error':len(pairs)-accepted,'failures':failures,'scope':'synthetic JSON-compatible proposals and evaluator labels; not model outputs'}
    Path('results/stress-v02.json').write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result,indent=2)); return bool(failures)
if __name__=='__main__': raise SystemExit(main())
