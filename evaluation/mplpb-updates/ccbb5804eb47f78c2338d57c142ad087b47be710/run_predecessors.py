"""Run earlier public repositories from pinned source; preserve original clones."""
import argparse,hashlib,io,json,os,shutil,subprocess,sys,tempfile,time,zipfile
from pathlib import Path
PINS={'portable-evidence-runtime':'4fdc20193c01f82baea0598b4c7d8ef3040772d5','mplpb-residual-experiment':'1ec160051ba306ce61d74ba3186f0aa5873694c5'}
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True);p.add_argument('--workspace',type=Path,default=Path('/workspace'));p.add_argument('--residual-source',type=Path,default=Path('/tmp/mplpb-residual-baseline257e'));a=p.parse_args();a.out=a.out.resolve();a.out.mkdir(parents=True,exist_ok=False)
 freeze={'runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'pins':PINS,'residual_source':'257e54a51edac272eb6b2441457f38a40485ee4d','scope':'Earlier public software controls; no new model trials or independent historical accuracy.'};save(a.out/'freeze.json',freeze)
 rows=[]
 def run(name,argv,cwd):
  start=time.perf_counter();r=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
  (a.out/(name+'.stdout.txt')).write_text(r.stdout);(a.out/(name+'.stderr.txt')).write_text(r.stderr)
  row={'id':name,'argv':list(map(str,argv)),'cwd':str(cwd),'status':'PASS' if r.returncode==0 else 'FAIL','exit_code':r.returncode,'elapsed_seconds':time.perf_counter()-start};rows.append(row);print(name,row['status'],flush=True);return r
 with tempfile.TemporaryDirectory(prefix='public-predecessor-check-') as tmp:
  clone=a.workspace/'portable-evidence-runtime';assert subprocess.check_output(['git','-C',str(clone),'rev-parse','HEAD'],text=True).strip()==PINS[clone.name]
  raw=subprocess.check_output(['git','-C',str(clone),'archive','--format=zip','HEAD']);copy=Path(tmp)/'portable';copy.mkdir();zipfile.ZipFile(io.BytesIO(raw)).extractall(copy)
  run('portable-python',[sys.executable,'-m','unittest','discover','-s','tests','-v'],copy)
  run('portable-browser-core',['node','tests/test_browser_core.cjs'],copy)
  run('portable-authoring-core',['node','tests/test_authoring_core.cjs'],copy)
  run('portable-synthetic',[sys.executable,'scripts/run_experiment.py'],copy)
  run('portable-offline-browser',[sys.executable,'scripts/browser_offline_probe.py'],copy)
  for name in ('synthetic_run.json','browser_offline_probe.json'):
   file=copy/'experiment/results'/name
   if file.exists():shutil.copyfile(file,a.out/name)
 clone=a.workspace/'mplpb-residual-experiment';assert subprocess.check_output(['git','-C',str(clone),'rev-parse','HEAD'],text=True).strip()==PINS[clone.name]
 run('residual-run',[sys.executable,'run.py','--source',str(a.residual_source),'--out',str(a.out/'residual')],clone)
 run('residual-check',[sys.executable,'check.py',str(a.out/'residual')],clone)
 for name in PINS:assert not subprocess.check_output(['git','-C',str(a.workspace/name),'status','--porcelain','--untracked-files=no'],text=True).strip()
 save(a.out/'summary.json',{'results':rows,'pins':PINS,'source_clones_modified':False,'new_model_calls':0})
 if any(x['status']!='PASS' for x in rows):raise SystemExit(1)
if __name__=='__main__':main()
