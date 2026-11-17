"""Capture official public native evaluations or the component checker on the new pin."""
import argparse,hashlib,json,subprocess,sys,time
from pathlib import Path
REV='ccbb5804eb47f78c2338d57c142ad087b47be710'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--mplpb-root',type=Path,default=Path('/workspace/mplpb'));p.add_argument('--out',type=Path,required=True);p.add_argument('--parts',action='store_true');a=p.parse_args();a.out=a.out.resolve()
 def git(*args):return subprocess.check_output(['git','-C',str(a.mplpb_root),*args],text=True).strip()
 assert git('rev-parse','HEAD')==REV
 assert not git('status','--porcelain','--untracked-files=no')
 a.out.mkdir(parents=True,exist_ok=False)
 commands=[('components',[sys.executable,'tools/check_parts.py'])] if a.parts else [('public-evidence',[sys.executable,'-m','tools.evaluate_public_evidence','--require-capabilities','--output',str(a.out/'public-evidence.json')]),('original-papers',[sys.executable,'-m','tools.evaluate_historical_experts','--output',str(a.out/'original-papers.json')])]
 (a.out/'freeze.json').write_text(json.dumps({'revision':REV,'commands':commands,'runner_sha256':sha(Path(__file__)),'models_enabled':False,'scope':'Official published developer evaluations on current native code; not private Ben fixtures or independent blinded judgment.'},indent=2)+'\n')
 rows=[]
 for name,argv in commands:
  start=time.perf_counter();r=subprocess.run(argv,cwd=a.mplpb_root,capture_output=True,text=True)
  stdout=a.out/(name+'.stdout.txt');stderr=a.out/(name+'.stderr.txt');stdout.write_text(r.stdout);stderr.write_text(r.stderr)
  rows.append({'id':name,'status':'PASS' if r.returncode==0 else 'FAIL','exit_code':r.returncode,'elapsed_seconds':time.perf_counter()-start,'stdout_sha256':sha(stdout),'stderr_sha256':sha(stderr)})
  print(name,rows[-1]['status'],flush=True)
 result={'revision':REV,'results':rows,'tracked_target_changed':bool(git('status','--porcelain','--untracked-files=no')),'note':'The component checker repeats the root native suite; that repeat is not additional unique coverage.'}
 (a.out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
 if result['tracked_target_changed'] or any(x['status']!='PASS' for x in rows):raise SystemExit(1)
if __name__=='__main__':main()
