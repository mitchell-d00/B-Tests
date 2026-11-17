"""Repeat an environment-blocked component suite; permit local networking in the host."""
import argparse,hashlib,json,subprocess,sys,time
from pathlib import Path
REV='3df2c6e22f0ef454f3ee67b88d43402a42f63443'
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--component',choices=['networked','image'],required=True);p.add_argument('--mplpb-root',type=Path,default=Path('/workspace/mplpb'));p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out=a.out.resolve();a.out.mkdir(parents=True,exist_ok=False)
 rev=subprocess.check_output(['git','-C',str(a.mplpb_root),'rev-parse','HEAD'],text=True).strip();assert rev==REV
 cmd=[sys.executable,'-m','unittest','discover','-s', 'Tests' if a.component=='networked' else 'tests']
 if a.component=='networked':cmd+=['-t','.']
 (a.out/'freeze.json').write_text(json.dumps({'revision':rev,'command':cmd,'cwd':'parts/'+a.component,'runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'environment_change':'Local networking permitted; no target changes.','original_failure':'components/'+a.component+'.stderr.txt: socket creation PermissionError'},indent=2)+'\n')
 start=time.perf_counter();r=subprocess.run(cmd,cwd=a.mplpb_root/'parts'/a.component,capture_output=True,text=True)
 (a.out/'stdout.txt').write_text(r.stdout);(a.out/'stderr.txt').write_text(r.stderr)
 (a.out/'summary.json').write_text(json.dumps({'revision':rev,'status':'PASS' if r.returncode==0 else 'FAIL','exit_code':r.returncode,'elapsed_seconds':time.perf_counter()-start,'stdout_sha256':hashlib.sha256(r.stdout.encode()).hexdigest(),'stderr_sha256':hashlib.sha256(r.stderr.encode()).hexdigest()},indent=2)+'\n')
 print(a.component,r.returncode);raise SystemExit(r.returncode)
if __name__=='__main__':main()
