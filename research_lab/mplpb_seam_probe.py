"""Paired native work-boundary probes on genuine unmodified MPLPB revisions.

The same authored source/task inputs hit each target's public coordinator API.
FAIL means the explicit current probe criterion was violated, not that an older
version claimed a source-semantic checker or that Ben's private test was replicated.
"""
from __future__ import annotations
import argparse
import importlib
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
from .common import save,sha

OLD='257e54a51edac272eb6b2441457f38a40485ee4d'
NEW='cc21ce300b5ec228c07fc77a149804fba6c89792'
CASES={'contradictory_claim':False,'claim_only_chain':False,'supported_control':True,
       'revoked_seat':False,'changed_source':False,'unavailable_original':False,
       'export_without_evidence':False}


def worker(root,out,case,revision):
    root=root.resolve();out=out.resolve()
    if subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()!=revision:raise ValueError('Wrong target revision')
    sys.path.insert(0,str(root))
    from mplpb_combined.ledger import write,revise,Ledger
    from mplpb_work import WorkStore,WorkError
    from mplpb_work.model import OPERATIONS
    import mplpb_work
    assert Path(mplpb_work.__file__).resolve().is_relative_to(root)
    corpus=out/'corpus';write(corpus,doc_id='SRC-0001',title='Supplier',scope='supplier availability',
        body='Configuration AX-14 is discontinued. Component X remains available.')
    source=Ledger(corpus).by_id['SRC-0001'][0]
    store,host=WorkStore.create(out/'work',{'research':corpus},clock=lambda:1000.0)
    token=store.assign(host,seat='operator',instance='native-fixture',
        model={'name':'none','provider':'no model','version':'none','context_policy_hash':'sha256:'+sha(b'native-probe-context-policy')},
        contract={'operations':sorted(OPERATIONS),'tools':['probe.effect.v1'],'scopes':['T1'],
                  'share_with':[],'profile':'internal','expires_at':10000.0},expected_head=store.head(host)['hash'])['credential']
    def put(id,kind,payload,deps=None):
        return store.put(token,id=id,kind=kind,payload=payload,dependencies=deps or {},visibility=['operator'],expected_revision=0,expected_head=store.snapshot(token)['head'])
    put('T1','task',{'goal':'Check source-bound work eligibility','criteria':['local probe passes'],'review_budget':2,'state':'open','acceptance':{}})
    if case=='export_without_evidence':
        # A promoted export alone cannot create effective supported premises.
        with sqlite3.connect('file:'+str(store.path)+'?mode=ro',uri=True) as db:before=db.execute('SELECT count(*) FROM events').fetchone()[0]
        error=None
        try:put('C1','claim',{'task':'T1','proposition':'Component X remains available','basis':'inference',
                'assessment':'supported_under_scope','assumptions':[],'alternatives':[],
                'revisit_when':'Original evidence becomes available'})
        except WorkError as exc:error={'type':type(exc).__name__,'message':str(exc)}
        with sqlite3.connect('file:'+str(store.path)+'?mode=ro',uri=True) as db:after=db.execute('SELECT count(*) FROM events').fetchone()[0]
        result={'case':case,'revision':revision,'status':'PASS' if error and before==after else 'FAIL',
            'criterion':'A claimed supported human export with no pinned evidence cannot be promoted as supported work.',
            'expected_effect':False,'observed_effect':False,'support_promotion_rejected':error is not None,
            'exception':error,'event_count_before':before,'event_count_after':after,
            'verification':'Independent read-only SQLite event counts before and after attempted support promotion.',
            'scope':'Native record-creation contract, not detection of a false outside-world original.','model_calls':0}
        save(out/'result.json',result);return result
    positive=case!='contradictory_claim'
    quote='Component X remains available.' if positive else 'Configuration AX-14 is discontinued.'
    put('E1','evidence',{'task':'T1','corpus':'research','source_id':source.id,'source_hash':source.hash,'quote':quote,'query':'supplier availability'})
    claim={'task':'T1','proposition':'Component X remains available' if positive else 'Component X is discontinued',
           'basis':'inference','assessment':'supported_under_scope','assumptions':[],
           'alternatives':[],'revisit_when':'Source changes'}
    put('C1','claim',claim,{'E1':1});claim_id='C1'
    if case=='claim_only_chain':put('C2','claim',claim,{'C1':1});claim_id='C2'
    put('A1','action',{'task':'T1','task_revision':1,'operation':'probe.effect.v1','arguments':{},
         'side_effect':'local','executor_seat':'operator','state':'proposed','retry_of':{},'retry_reason':''},{claim_id:1})
    marker=out/'effect.txt'
    def effect(request):
        marker.write_text('Actual local adapter invoked.\n')
        return {'result':'passed','validation':{'local probe passes':True},'artifact':'local probe completed'}
    store.executors['probe.effect.v1']=effect
    initial=store.snapshot(token);before_rows={r['id']:r for r in initial['records']}
    if case=='revoked_seat':store.revoke(host,'operator',store.head(host)['hash'])
    if case=='changed_source':revise(corpus,source.id,body='Configuration AX-14 is discontinued. Component X is not available.')
    if case=='unavailable_original':
        source_path=Path(source.path)
        if not source_path.is_absolute():source_path=corpus/source_path
        assert source_path.resolve().is_relative_to(corpus.resolve())
        source_path.unlink()
        store=WorkStore(out/'work',{'probe.effect.v1':effect},clock=lambda:1000.0)
    try:
        current=store.snapshot(token);rows={r['id']:r for r in current['records']};head=current['head']
    except WorkError:
        rows={};head=initial['head']
    def count_events():
        with sqlite3.connect('file:'+str(store.path)+'?mode=ro',uri=True) as db:return db.execute('SELECT count(*) FROM events').fetchone()[0]
    before=count_events();error=None;receipt=None
    try:receipt=store.execute(token,id='A1',expected_revision=1,expected_head=head)
    except WorkError as exc:error={'type':type(exc).__name__,'message':str(exc)}
    after=count_events();exists=marker.exists();expected=CASES[case]
    ok=(exists and error is None) if expected else (not exists and error is not None and before==after)
    result={'case':case,'revision':revision,'status':'PASS' if ok else 'FAIL',
         'criterion':'Allow supported control; reject contradictory/claim-only/revoked/stale premises before any local adapter effect.',
         'expected_effect':expected,'observed_effect':exists,'adapter_marker':marker.read_text() if exists else None,
         'claim_effective_status':rows.get(claim_id,{}).get('effective_status'),
         'action_permission':rows.get('A1',{}).get('permission'),
         'submitted_claim_assessment':claim['assessment'],'proposition':claim['proposition'],
         'source_body':'Configuration AX-14 is discontinued. Component X remains available.',
         'source_quote':quote,'event_count_before':before,'event_count_after':after,'exception':error,
         'receipt_returned':receipt is not None,'source_identity':{'id':source.id,'hash':source.hash},
         'verification':'Separate read-only SQLite event count and actual adapter marker file; no simulated blocked effect.',
         'scope':'Authored native contract probe; old-version failures are against this current criterion, not a retroactive specification judgment.',
         'model_calls':0}
    save(out/'result.json',result);return result


def run(old,current,out):
    if out.exists():raise ValueError('Use a new output directory')
    save(out/'freeze.json',{'cases':CASES,'old_revision':OLD,'current_revision':NEW,
         'runner_sha256':sha(Path(__file__).read_bytes()),'fixture':'Same source/task/propositions for both native revisions; no live models.',
         'failure_interpretation':'Violation of this frozen probe criterion; does not establish Ben independently demonstrated that case or old claimed general semantic entailment.'})
    rows=[]
    for name,root,revision in [('old',old,OLD),('current',current,NEW)]:
        for case in CASES:
            directory=out/name/case
            argv=[sys.executable,'-m','research_lab.mplpb_seam_probe','worker','--root',str(root.resolve()),'--out',str(directory.resolve()),'--case',case,'--revision',revision]
            directory.mkdir(parents=True)
            proc=subprocess.run(argv,capture_output=True,text=True)
            (directory/'stdout.txt').write_text(proc.stdout);(directory/'stderr.txt').write_text(proc.stderr)
            if proc.returncode!=0:row={'case':case,'revision':revision,'status':'NOT_RUN','blocker':'Worker did not complete; inspect retained stderr','exit_code':proc.returncode}
            else:row=json.loads((directory/'result.json').read_text())
            rows.append(row);print(name,case,row['status'],row.get('observed_effect'),flush=True)
    summary={'schema':'mplpb-native-seams-1','results':rows,'scope':'Paired native development probes, not Ben private benchmark reproduction or independent performance estimate.','model_calls':0}
    save(out/'summary.json',summary);return summary


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['run','worker'])
    p.add_argument('--out',type=Path,required=True);p.add_argument('--old-root',type=Path);p.add_argument('--current-root',type=Path)
    p.add_argument('--root',type=Path);p.add_argument('--case',choices=list(CASES));p.add_argument('--revision')
    a=p.parse_args()
    if a.command=='worker':r=worker(a.root,a.out,a.case,a.revision)
    else:r=run(a.old_root,a.current_root,a.out)
    print(json.dumps(r,indent=2))


if __name__=='__main__':main()
