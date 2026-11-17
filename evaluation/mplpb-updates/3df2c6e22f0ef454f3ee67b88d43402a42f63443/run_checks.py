"""Explicit new-version executions of existing B-Tests, preserving historical pins.
Run from B-Tests: python evaluation/mplpb-updates/3df2c6e22f0ef454f3ee67b88d43402a42f63443/run_checks.py --out NEW_DIRECTORY
Full native command is separately documented in RESULTS.md. No target edits.
"""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REV='3df2c6e22f0ef454f3ee67b88d43402a42f63443'
BROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(BROOT))
from research_lab.mplpb_seam_probe import CASES
from side_by_side.run import load_manifest,run_mplpb


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--mplpb-root',type=Path,default=Path('/workspace/mplpb'));p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 a.out=a.out.resolve();target=a.mplpb_root.resolve()
 head=subprocess.check_output(['git','-C',str(target),'rev-parse','HEAD'],text=True).strip()
 assert head==REV,head
 assert not subprocess.check_output(['git','-C',str(target),'status','--porcelain','--untracked-files=no'],text=True).strip()
 a.out.mkdir(parents=True,exist_ok=False)
 save(a.out/'freeze.json',{'evaluated_revision':REV,'b_tests_commit':subprocess.check_output(['git','-C',str(BROOT),'rev-parse','HEAD'],text=True).strip(),'runner_sha256':sha(Path(__file__)),'seam_worker_sha256':sha(BROOT/'research_lab/mplpb_seam_probe.py'),'legacy_cases_sha256':sha(BROOT/'side_by_side/cases.json'),'legacy_function_sha256':sha(BROOT/'side_by_side/run.py'),'cases':CASES,'scope':'Explicit new revision, unchanged frozen fixture/scoring logic. Not a new AI comparison or private benchmark.'})
 rows=[]
 with tempfile.TemporaryDirectory(prefix='btests-new-revision-') as temporary:
  for case in CASES:
   private=Path(temporary)/case;private.mkdir()
   cmd=[sys.executable,'-m','research_lab.mplpb_seam_probe','worker','--root',str(target),'--out',str(private),'--case',case,'--revision',REV]
   r=subprocess.run(cmd,cwd=BROOT,capture_output=True,text=True)
   public=a.out/'seams'/case;public.mkdir(parents=True)
   (public/'stdout.txt').write_text(r.stdout);(public/'stderr.txt').write_text(r.stderr)
   if r.returncode:result={'case':case,'revision':REV,'status':'NOT_RUN','exit_code':r.returncode,'blocker':'Worker did not complete; retained stderr'}
   else:
    result=json.loads((private/'result.json').read_text());shutil.copyfile(private/'result.json',public/'result.json')
    if (private/'effect.txt').exists():shutil.copyfile(private/'effect.txt',public/'effect.txt')
   rows.append(result);print(case,result['status'],flush=True)
 save(a.out/'seams/summary.json',{'results':rows,'evaluated_revision':REV,'model_calls':0})
 manifest=load_manifest();legacy=[]
 for case in manifest['cases']:
  result=run_mplpb(case,target)
  # The reused historical function stamps its constant PIN in metadata; retain it
  # verbatim under a named raw field, and identify the actual checkout independently.
  legacy.append({'evaluated_revision':REV,'fixture_original_revision':manifest['mplpb_pin'],
    'case':case['id'],'status':result['status'],'frozen_function_output':result,
    'metadata_note':'Raw repo_pin is the historical function constant, not the checkout evaluated here. HEAD is independently verified at freeze.'})
  print(case['id'],result['status'],flush=True)
 save(a.out/'legacy-development.json',{'results':legacy,'evaluated_revision':REV,'fixture_sha256':manifest['_sha256'],'new_condition':True,'model_calls':0,'CAD':'NOT_RUN: no new real AI adapter configured','BASELINE':'NOT_RUN: no new real AI adapter configured'})
 for name,cmd in [('btests-unit',[sys.executable,'-m','unittest','discover','-s','tests','-v']),('historical-native-replay',[sys.executable,'-m','research_lab.native_evidence'])]:
  r=subprocess.run(cmd,cwd=BROOT,capture_output=True,text=True)
  (a.out/(name+'.stdout.txt')).write_text(r.stdout);(a.out/(name+'.stderr.txt')).write_text(r.stderr)
  save(a.out/(name+'.json'),{'command':cmd,'exit_code':r.returncode,'status':'PASS' if r.returncode==0 else 'FAIL','new_target_execution':False,'scope':'Laboratory tests or public historical-record replay; not new native passes on the updated target.'})
 assert not subprocess.check_output(['git','-C',str(target),'status','--porcelain','--untracked-files=no'],text=True).strip()

if __name__=='__main__':main()
