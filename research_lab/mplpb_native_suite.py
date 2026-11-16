"""Execute the unmodified full MPLPB checkout and retain every command result.

This runner reports native authored-suite evidence, not general semantic accuracy
or an OOCC/CAD model score. No target repair, installation or hidden retry occurs.
"""
from __future__ import annotations
import argparse
import json
import os
import platform
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
from .common import save,sha

CURRENT='cc21ce300b5ec228c07fc77a149804fba6c89792'


def run(root,out,revision=CURRENT):
    root=root.resolve();out=out.resolve()
    if out.exists():raise ValueError('Use a new output directory; preserve all earlier results')
    def git(*args):return subprocess.check_output(['git','-C',str(root),*args],text=True).strip()
    actual=git('rev-parse','HEAD')
    if actual!=revision:raise ValueError('Checkout does not match the requested revision')
    before=git('status','--porcelain','--untracked-files=no')
    if before:raise ValueError('Tracked target changes exist; evaluate an unmodified checkout')
    commands=[
        ('python-full-suite',[sys.executable,'-m','unittest','discover','-s','tests','-t','.','-v']),
        ('ui-script',[sys.executable,'tools/check_ui_script.py']),
        ('browser-transport',['node','tools/check_browser_transport.cjs']),
        ('javascript-api',['node','tests/javascript-api.cjs']),
        ('crawler-worker',['node','crawler/test_worker.mjs']),
        ('source-infrastructure',[sys.executable,'tools/check_repository_infrastructure.py']),
        ('committed-handoff',[sys.executable,'tools/build_handoff.py','--check']),
        ('five-instance-recovery',[sys.executable,'-m','tools.demo_specialist_continuity','--output',str(out/'five-instance-demo.json')]),
    ]
    # Save exact target/command identity before any test executes.
    save(out/'freeze.json',{'revision':revision,'actual_head':actual,'git_tree':git('rev-parse','HEAD^{tree}'),
         'source_origin':git('remote','get-url','origin'),'tracked_clean_before':True,
         'runner_sha256':sha(Path(__file__).read_bytes()),'commands':commands,
         'python':sys.version,'platform':platform.platform(),'model_calls':0,
         'scope':'Native repository development tests and local demonstrations; no new independent human or neural-model validation.'})
    rows=[]
    for name,argv in commands:
        print('START '+name,flush=True);directory=out/name;directory.mkdir()
        start=time.perf_counter()
        if shutil.which(argv[0]) is None:
            row={'id':name,'command':argv,'status':'NOT_RUN','blocker':'Executable unavailable: '+argv[0]}
        else:
            with (directory/'stdout.txt').open('w') as stdout,(directory/'stderr.txt').open('w') as stderr:
                proc=subprocess.run(argv,cwd=root,stdout=stdout,stderr=stderr,check=False)
            text=(directory/'stdout.txt').read_text()+'\n'+(directory/'stderr.txt').read_text()
            counts=re.findall(r'Ran (\d+) tests? in ',text)
            row={'id':name,'command':argv,'status':'PASS' if proc.returncode==0 else 'FAIL',
                 'exit_code':proc.returncode,'elapsed_seconds':time.perf_counter()-start,
                 'unittest_count':int(counts[-1]) if counts else None,
                 'stdout_sha256':sha((directory/'stdout.txt').read_bytes()),
                 'stderr_sha256':sha((directory/'stderr.txt').read_bytes()),
                 'evidence_level':'native_unmodified_repository_execution',
                 'scope':'A failed command requires log review; this status alone does not classify an architectural defect.'}
        save(directory/'result.json',row);rows.append(row)
        save(out/'progress.json',{'revision':revision,'results':rows})
        print(name+' '+row['status'],flush=True)
    after=git('status','--porcelain','--untracked-files=no')
    summary={'schema':'mplpb-native-suite-1','revision':revision,'git_tree':git('rev-parse','HEAD^{tree}'),
             'results':rows,'counts':{s:sum(r['status']==s for r in rows) for s in ('PASS','FAIL','NOT_RUN')},
             'tracked_target_changed':bool(after),'tracked_status_after':after,
             'model_calls':0,'native_oocc_access':False,'independent_quality_validation':False,
             'limits':['Authored development suites are not independent accuracy or usability studies.',
                       'JavaScript checks are not automatically real-browser or physical-device inference.',
                       'Ben original private benchmarks are not supplied or reproduced by this runner.']}
    save(out/'summary.json',summary)
    return summary


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--mplpb-root',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);p.add_argument('--revision',default=CURRENT)
    a=p.parse_args();r=run(a.mplpb_root,a.out,a.revision)
    print(json.dumps({'counts':r['counts'],'tracked_target_changed':r['tracked_target_changed']}))
    return int(r['counts']['FAIL']>0 or r['counts']['NOT_RUN']>0 or r['tracked_target_changed'])


if __name__=='__main__':raise SystemExit(main())
