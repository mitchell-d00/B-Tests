"""Replay native execution records without executing either target again."""
import argparse
import json
from pathlib import Path
import re
from .common import sha


def replay(root):
    digests=json.loads((root/'sha256.json').read_text())
    for name,digest in digests.items():assert sha((root/name).read_bytes())==digest,name
    suites=[]
    for name in ('restricted-environment','network-enabled'):
        directory=root/name;report=json.loads((directory/'summary.json').read_text())
        assert report['tracked_target_changed'] is False
        for row in report['results']:
            if row['status']=='NOT_RUN':continue
            d=directory/row['id']
            assert sha((d/'stdout.txt').read_bytes())==row['stdout_sha256']
            assert sha((d/'stderr.txt').read_bytes())==row['stderr_sha256']
            assert row['status']==('PASS' if row['exit_code']==0 else 'FAIL')
        suites.append({'condition':name,'counts':report['counts'],'python_tests':report['results'][0]['unittest_count']})
    component=json.loads((root/'component-check/summary.json').read_text())
    assert component['status']=='PASS' and component['tracked_target_changed'] is False
    for stream in ('stdout','stderr'):
        assert sha((root/'component-check'/f'{stream}.txt').read_bytes())==component[f'{stream}_sha256']
    pairs=json.loads((root/'final-seven-case-pairs/summary.json').read_text())
    for r in pairs['results']:
        expected=r['expected_effect']
        if r['case']=='export_without_evidence':ok=r['support_promotion_rejected'] and r['event_count_before']==r['event_count_after']
        elif expected:ok=r['observed_effect'] and r['exception'] is None
        else:ok=not r['observed_effect'] and r['exception'] is not None and r['event_count_before']==r['event_count_after']
        assert r['status']==('PASS' if ok else 'FAIL')
        version='old' if r['revision'].startswith('257e') else 'current'
        d=root/'final-seven-case-pairs'/version/r['case']
        assert (d/'effect.txt').exists()==r['observed_effect']
    return {'new_target_executions':0,'component_checks':component,'native_suite_records':suites,'paired_results':[
        {k:r.get(k) for k in ('case','revision','status','observed_effect','claim_effective_status','action_permission')} for r in pairs['results']],
        'scope':'Replay verifies retained bytes and criteria, not independent attestation of original execution or a new native run.'}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path('evaluation/mplpb-native'));a=p.parse_args()
    print(json.dumps(replay(a.root),indent=2))


if __name__=='__main__':main()
