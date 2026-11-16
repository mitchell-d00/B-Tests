"""Score a PRE-REGISTERED OOCC versus baseline relationship-saturation study.

Only scores supplied observations. Never produces a native software pass or
independent-science certificate. Retains negative and null results.
"""
from __future__ import annotations
import argparse
import json
import math
import sys
from pathlib import Path

REQUIRED_SIZES=(10,100,1000)
REQUIRED_ARMS=('OOCC','baseline')
COUNT_FIELDS=('tasks','verified_tasks','judged_relations','false_proven_links',
              'refuted_links','refuted_links_active_after','operator_corrections','tool_calls','tokens')
COST_FIELDS=('human_minutes','cpu_seconds','elapsed_seconds','total_usd')

def num(x,field):
    if isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) or x<0:
        raise ValueError(f'{field} must be a finite nonnegative number')
    return x

def score(data):
    if not isinstance(data,dict):raise ValueError('Expected object')
    if data.get('preregistered_before_outcomes') is not True:
        raise ValueError('Pre-outcome preregistration required')
    if data.get('equal_original_source_access') is not True:
        raise ValueError('Equal original source access required')
    if data.get('independent_blind_labels') is not True:
        raise ValueError('Independent blind labels required for study scoring')
    if not isinstance(data.get('protocol_sha256'),str) or len(data['protocol_sha256'])!=64:
        raise ValueError('Pinned protocol SHA-256 required')
    rows=data.get('rows')
    if not isinstance(rows,list) or not rows:raise ValueError('No study rows')
    bykey={}
    for row in rows:
        if not isinstance(row,dict):raise ValueError('Invalid row')
        key=(row.get('edge_count'),row.get('arm'))
        if key in bykey:raise ValueError('Duplicate arm/edge count')
        if key[0] not in REQUIRED_SIZES or key[1] not in REQUIRED_ARMS:
            raise ValueError('Unexpected edge count or study arm')
        if row.get('source_snapshot_sha256') is None:
            raise ValueError('Every arm requires a source snapshot pin')
        for field in COUNT_FIELDS:
            v=num(row.get(field),field)
            if not isinstance(v,int):raise ValueError('Count must be an integer: '+field)
        for field in COST_FIELDS:num(row.get(field),field)
        if row['tasks']==0 or row['judged_relations']==0:
            raise ValueError('Nonempty outcome and relation denominators required')
        if row['verified_tasks']>row['tasks'] or row['false_proven_links']>row['judged_relations']:
            raise ValueError('Impossible outcomes')
        if row['refuted_links_active_after']>row['refuted_links']:
            raise ValueError('Refuted-link counts inconsistent')
        bykey[key]=row
    required={(n,a) for n in REQUIRED_SIZES for a in REQUIRED_ARMS}
    if set(bykey)!=required:raise ValueError('Missing paired arm or edge scale')
    output=[]
    for n in REQUIRED_SIZES:
        a,b=bykey[(n,'OOCC')],bykey[(n,'baseline')]
        if a['source_snapshot_sha256']!=b['source_snapshot_sha256']:
            raise ValueError('Mismatched source snapshot at scale '+str(n))
        def metrics(row):
            return {
              'verified_task_rate':row['verified_tasks']/row['tasks'],
              'false_proven_relation_rate':row['false_proven_links']/row['judged_relations'],
              'refuted_relation_reactivation_rate':(row['refuted_links_active_after']/row['refuted_links'] if row['refuted_links'] else None),
              'human_minutes_per_verified_task':(row['human_minutes']/row['verified_tasks'] if row['verified_tasks'] else None),
              'operator_corrections':row['operator_corrections'],
              'total_usd':row['total_usd'],
              'tokens':row['tokens'],
              'tool_calls':row['tool_calls']
            }
        ma,mb=metrics(a),metrics(b)
        output.append({'edge_count':n,'OOCC':ma,'baseline':mb,
                       'delta_verified_task_rate':ma['verified_task_rate']-mb['verified_task_rate'],
                       'delta_false_proven_relation_rate':ma['false_proven_relation_rate']-mb['false_proven_relation_rate'],
                       'delta_human_minutes':a['human_minutes']-b['human_minutes'],
                       'delta_total_usd':a['total_usd']-b['total_usd']})
    return {'status':'DESCRIPTIVE_PAIRWISE_ANALYSIS_ONLY',
            'independence_certified_by_this_script':False,
            'no_automatic_superiority_conclusion':True,
            'comparison':output}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('data',type=Path)
    p.add_argument('--out',type=Path)
    args=p.parse_args(argv)
    result=score(json.loads(args.data.read_text(encoding='utf8')))
    text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.out:args.out.write_text(text,encoding='utf8')
    else:print(text)
    return 0

if __name__=='__main__':sys.exit(main())
