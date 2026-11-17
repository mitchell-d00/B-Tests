"""Run published component commands and adoption checks without repeating root tests.
The already separate native run covers the root suite. No target source is changed.
"""
import argparse,hashlib,json,runpy,shutil,subprocess,sys,tempfile,time
from pathlib import Path
REV='3df2c6e22f0ef454f3ee67b88d43402a42f63443'
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--mplpb-root',type=Path,default=Path('/workspace/mplpb'));p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out=a.out.resolve();target=a.mplpb_root.resolve()
 def git(*args):return subprocess.check_output(['git','-C',str(target),*args],text=True).strip()
 assert git('rev-parse','HEAD')==REV and not git('status','--porcelain','--untracked-files=no')
 a.out.mkdir(parents=True,exist_ok=False)
 sys.path.insert(0,str(target))
 config=runpy.run_path(str(target/'tools/check_parts.py'))
 commands=[(name,cwd,[sys.executable,*args]) for name,cwd,args in config['SUITES'][1:]]
 commands.append(('local-mirror',target/'parts/local-mirror',[sys.executable,'tools/validate.py','site']))
 save(a.out/'freeze.json',{'revision':REV,'runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'published_checker_sha256':hashlib.sha256((target/'tools/check_parts.py').read_bytes()).hexdigest(),'commands':[(name,str(cwd),cmd) for name,cwd,cmd in commands],'scope':'Individual published component commands and native adoption, omitting root repeat; no target edits.'})
 rows=[]
 for name,cwd,cmd in commands:
  start=time.perf_counter();r=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True)
  (a.out/(name+'.stdout.txt')).write_text(r.stdout);(a.out/(name+'.stderr.txt')).write_text(r.stderr)
  rows.append({'component':name,'status':'PASS' if r.returncode==0 else 'FAIL','exit_code':r.returncode,'elapsed_seconds':time.perf_counter()-start})
  print(name,rows[-1]['status'],flush=True)
 from mplpb_combined.ledger import seal,Ledger
 adoption=[]
 for name,site in config['SITES']:
  with tempfile.TemporaryDirectory(prefix='btests-adopt-current-') as temp:
   root=Path(temp)/'site';shutil.copytree(site,root);sealed=seal(root,when='2026-11-01T00:00Z');ledger=Ledger(root)
   errors=[str(f) for f in ledger.findings() if f.level=='error']
   adoption.append({'site':name,'sealed':len(sealed),'errors':errors,'status':'PASS' if not errors else 'FAIL'})
 save(a.out/'summary.json',{'revision':REV,'results':rows,'adoption':adoption,'tracked_target_changed':bool(git('status','--porcelain','--untracked-files=no')),'models_called':0})
 if any(x['status']!='PASS' for x in rows+adoption):raise SystemExit(1)
if __name__=='__main__':main()
