"""Run Combined MPLPB's unmodified historical-component/adoption checker."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
import time
from .common import save,sha
from .mplpb_native_suite import CURRENT


def run(root,out):
    root=root.resolve();out=out.resolve()
    if out.exists():raise ValueError('Preserve earlier executions; use a new directory')
    def git(*args):return subprocess.check_output(['git','-C',str(root),*args],text=True).strip()
    if git('rev-parse','HEAD')!=CURRENT or git('status','--porcelain','--untracked-files=no'):
        raise ValueError('Use the clean pinned full checkout')
    argv=[sys.executable,'tools/check_parts.py']
    save(out/'freeze.json',{'revision':CURRENT,'tree':git('rev-parse','HEAD^{tree}'),
         'command':argv,'runner_sha256':sha(Path(__file__).read_bytes()),
         'note':'The official checker reruns the Combined suite as well as historical parts; do not add that repeat to independent sample size.'})
    start=time.perf_counter()
    with (out/'stdout.txt').open('w') as stdout,(out/'stderr.txt').open('w') as stderr:
        p=subprocess.run(argv,cwd=root,stdout=stdout,stderr=stderr)
    text=(out/'stdout.txt').read_text()
    result={'schema':'mplpb-parts-native-1','revision':CURRENT,'status':'PASS' if p.returncode==0 else 'FAIL',
         'exit_code':p.returncode,'elapsed_seconds':time.perf_counter()-start,
         'stdout_sha256':sha((out/'stdout.txt').read_bytes()),'stderr_sha256':sha((out/'stderr.txt').read_bytes()),
         'suite_lines':[l.strip() for l in text.splitlines() if ' tests ' in l],
         'adoption_lines':[l.strip() for l in text.splitlines() if 'sealed,' in l],
         'tracked_target_changed':bool(git('status','--porcelain','--untracked-files=no')),
         'scope':'Native checks of the vendored versions in this Combined commit, not a claim every upstream repository tree passes. The Swarm copy uses its retained complete archive.',
         'model_calls':0}
    save(out/'summary.json',result);print(json.dumps(result,indent=2));return result


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--mplpb-root',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();r=run(a.mplpb_root,a.out);return int(r['status']!='PASS' or r['tracked_target_changed'])


if __name__=='__main__':raise SystemExit(main())
