"""Reproduce the requested public-paper strict-reader comparison; no private adapters.

Requires PyMuPDF==1.26.6 and the two public clones. Run from any directory:
python /workspace/b-tests/evaluation/public-papers/run.py
For a repeat, pass --ledger /tmp/public-paper-ledger-repeat --output /tmp/public-paper-repeat.
The ledger directory must not already exist; prior runs are never overwritten there.
"""
import argparse
from collections import Counter
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import os
import fitz

QUERIES = [
    'What is Continuity in CAD?', 'What does Authority distinguish?',
    'Is CAD only prompt-level guidance?', 'What is Directive?',
    'What is Artificial Tangibility?', 'Does retrieval alone determine authority?',
    'What is the DHS Translation Protocol?',
    "Does Headmaster preserve the learner's original answers?",
    'source authority', 'Continuity Authority Directive',
    'What is the capital of France?', 'unprepared original source records',
]
WHEN='2026-11-01T00:00Z'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf-8')


def git(root,*args):
    return subprocess.check_output(['git','-C',str(root),*args],text=True).strip()


def cell(value):
    return str(value).replace('|','\\|').replace('\r','').replace('\n','<br>')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--mplpb-root',type=Path,default=Path('/workspace/mplpb'))
    p.add_argument('--b-tests-root',type=Path,default=Path('/workspace/b-tests'))
    p.add_argument('--attachments',type=Path,default=Path('/workspace/attachments'))
    p.add_argument('--ledger',type=Path,default=Path('/tmp/public-paper-ledger'))
    p.add_argument('--output',type=Path,default=Path(__file__).resolve().parent)
    a=p.parse_args(); a.output.mkdir(parents=True,exist_ok=True)
    if a.ledger.exists():raise SystemExit('Use a new --ledger directory; existing evidence is preserved.')
    if git(a.mplpb_root,'status','--porcelain','--untracked-files=no'):
        raise SystemExit('MPLPB has tracked changes; use an unmodified clone.')
    commit=git(a.mplpb_root,'rev-parse','HEAD'); bcommit=git(a.b_tests_root,'rev-parse','HEAD')
    freeze={'mplpb_commit':commit,'mplpb_tree':git(a.mplpb_root,'rev-parse','HEAD^{tree}'),
            'b_tests_commit':bcommit,'when':WHEN,'queries':QUERIES,
            'profile':{'name':'open','max_depth':None,'prose':True,'not_for':True},
            'extraction':'PyMuPDF page.get_text("text"), original order; concatenate first min(15,page_count) pages without editorial additions',
            'pymupdf_version':fitz.VersionBind,'python':sys.version,
            'runner_sha256':digest(Path(__file__).read_bytes()),
            'scope':'Public attached papers and supplied public TXT only; no private systems or adapters.'}
    save(a.output/'freeze.json',freeze)
    rows=[]
    for source in sorted(a.attachments.glob('*.pdf')):
        safe=re.sub(r'[^A-Za-z0-9._-]+','-',source.stem)
        with fitz.open(source) as doc:
            n=min(15,len(doc));text=''.join(doc[i].get_text('text') for i in range(n))
            total=len(doc)
        data=text.encode('utf-8');target=a.output/(safe+'.txt')
        target.write_bytes(data)
        (a.output/(safe+'.txt.sha256')).write_text(digest(data)+'  '+target.name+'\n')
        rows.append({'source_filename':source.name,'source_sha256':digest(source.read_bytes()),
                     'text_file':target.name,'text_sha256':digest(data),'total_pages':total,
                     'pages_extracted':n,'short_name':safe.replace('_',' ').replace('-',' '),
                     'format':'PDF first 15 pages or full if shorter'})
    if not rows:raise SystemExit('No supplied PDFs found')
    # This separately supplied text is included verbatim, not presented as PDF extraction.
    for source in sorted(a.attachments.glob('*.txt')):
        safe=re.sub(r'[^A-Za-z0-9._-]+','-',source.stem)
        target=a.output/(safe+'.txt');data=source.read_bytes();data.decode('utf-8')
        target.write_bytes(data)
        (a.output/(safe+'.txt.sha256')).write_text(digest(data)+'  '+target.name+'\n')
        rows.append({'source_filename':source.name,'source_sha256':digest(data),'text_file':target.name,
                     'text_sha256':digest(data),'total_pages':None,'pages_extracted':None,
                     'short_name':safe.replace('_',' ').replace('-',' '),'format':'Supplied TXT copied byte-for-byte'})
    if len({r['text_file'] for r in rows})!=len(rows):raise SystemExit('Output filename collision')
    sys.path.insert(0,str(a.mplpb_root.resolve()))
    from mplpb_combined.ledger import write,seal,Ledger
    from mplpb_combined.reader import answer,Profile
    import mplpb_combined.reader as reader
    assert Path(reader.__file__).resolve().is_relative_to(a.mplpb_root.resolve())
    for i,row in enumerate(rows,1):
        r=write(a.ledger,doc_id=f'PAPER-{i:04d}',title=row['short_name'],scope=row['short_name'],
                body=(a.output/row['text_file']).read_text(encoding='utf-8'),when=WHEN,
                source_authorship='unknown')
        sealed=seal(a.ledger,when=WHEN)
        reread=next(x for x in Ledger(a.ledger).records if x.id==r.id)
        assert reread.hash and reread.intact
        row.update({'ledger_id':reread.id,'ledger_hash':reread.hash,'ledger_path':reread.path,
                    'intact':reread.intact,'seal_return':sealed})
    ledger=Ledger(a.ledger)
    assert len(ledger.servable())==len(rows)
    save(a.output/'manifest.json',rows)
    outputs=[]
    for question in QUERIES:
        result=answer(a.ledger,question,Profile('open',None,True))
        view=result.to_dict()
        supported={'present':hasattr(result,'answer_supported') or 'answer_supported' in view,
                   'value':getattr(result,'answer_supported',view.get('answer_supported'))}
        outputs.append({'query':question,'kind':result.kind,'text_preview':result.text[:250],
                        'answer_supported':supported,'answer':view,'answer_dataclass':asdict(result)})
    save(a.output/'queries.json',outputs)
    # These public commands have been inspected: native_evidence only replays public files.
    commands=[('unittest',[sys.executable,'-m','unittest','discover','-s','tests','-v']),
              ('native_evidence',[sys.executable,'-m','research_lab.native_evidence'])]
    tests=[]
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    for label,cmd in commands:
        proc=subprocess.run(cmd,cwd=a.b_tests_root,capture_output=True,text=True,env=env)
        (a.output/(label+'.stdout.txt')).write_text(proc.stdout)
        (a.output/(label+'.stderr.txt')).write_text(proc.stderr)
        tests.append({'name':label,'command':cmd,'exit_code':proc.returncode,
                      'status':'PASS' if proc.returncode==0 else 'FAIL',
                      'stdout_sha256':digest(proc.stdout.encode()),'stderr_sha256':digest(proc.stderr.encode())})
    save(a.output/'test-results.json',tests)
    assert not git(a.mplpb_root,'status','--porcelain','--untracked-files=no')
    assert not git(a.b_tests_root,'status','--porcelain','--untracked-files=no')
    counts=dict(sorted(Counter(x['kind'] for x in outputs).items()))
    summary=('On these public-text excerpts, the strict reader produced '+', '.join(f'{n} {k}' for k,n in counts.items())+
             ', returning only selected sealed page text and abstaining on unresolved ownership; these outputs do not independently verify the papers\' factual claims.')
    report=f'''# Public-paper comparison\n\nMPLPB commit: `{commit}` (post-PR #43 main observed at acquisition).\n\nB-Tests commit: `{bcommit}`.\n\nProfile: `Profile("open", None, True)`; page timestamp: `{WHEN}`.\n\n## Materials and extraction\n\nTen supplied PDF documents were extracted with PyMuPDF {fitz.VersionBind}, first 15 physical pages or full if shorter. Text is unedited `get_text("text")` output concatenated in physical page order; PDF extraction can affect layout and reading order. The separately supplied Beyond Guarded Retrieval TXT is included verbatim as an additional source, not described as an extracted PDF. Pages after 15 are absent from this run. No inferred definitions, scope synonyms or answers were added.\n\nThe requested clone/attachment paths initially did not exist. Fresh public clones were acquired at the requested paths. Nine PDFs and the TXT came from the current attachment batch; the earlier attached No More First Dates PDF supplies the tenth PDF. Source-byte hashes, page ranges, extracted-text hashes and sealed ledger identities are in `manifest.json`. These hashes permit matching supplied files independently of their local filenames.\n\n| Paper | Pages extracted / total | Extracted-text SHA-256 |\n|---|---|---|\n'''
    for row in rows:
        pages=f"{row['pages_extracted']} / {row['total_pages']}" if row['total_pages'] is not None else 'Supplied TXT (full)'
        report+=f"| {cell(row['text_file'])} | {pages} | `{row['text_sha256']}` |\n"
    report+='''\n## Ledger and source status\n\nAll extracted texts and the supplied TXT were loaded through native `write`, with title and scope equal to each short name, and native `seal` was explicitly called after each write. Native `write` already produces hash-sealed records, so the subsequent `seal` calls return empty lists; every page was independently reloaded and its hash/intact state checked, and all pages were servable. No ratification, extra relationship, promotion, hand-edited source metadata or model-generated answer was added. The imported page's origin metadata follows `write`'s default; source authorship is explicitly unknown. Sealing proves the local content identity, not factual correctness or independently authenticated authorship.\n\n## Complete query results\n\n`queries.json` retains the complete native `Answer.to_dict()` (including full returned text and diagnostics), dataclass fields, and preview. The table shows the requested 250-character preview. “Absent” means this reader's Answer has no `answer_supported` field; it must not be interpreted as true. `return` selects a whole source page, not an independently inferred answer to a proposition.\n\n| Query | kind | text[:250] | answer_supported | Diagnostic |\n|---|---|---|---|---|\n'''
    for out in outputs:
        view=out['answer']
        diagnostic={k:view[k] for k in ('reason','known','unknown','matched_on','quarantined','route','clarification') if k in view}
        diagnostic['candidates']=view.get('candidates',[])
        diagnostic['withheld']=view.get('withheld',[]);diagnostic['set_aside']=view.get('set_aside',[])
        supported=str(out['answer_supported']['value']) if out['answer_supported']['present'] else 'Absent'
        report+=f"| {cell(out['query'])} | {out['kind']} | {cell(out['text_preview'])} | {supported} | {cell(json.dumps(diagnostic,ensure_ascii=False))} |\n"
    report+='\n## Public B-Tests commands\n\n'
    for test in tests:
        report+=f"- `{test['name']}`: **{test['status']}**, exit {test['exit_code']}; complete stdout/stderr retained next to this report.\n"
    log=(a.output/'unittest.stderr.txt').read_text()
    match=re.search(r'Ran (\d+) tests? in',log)
    if match:report+=f"\nUnit-test count: **{match.group(1)}**. These are laboratory tests, not additional OOCC/CAD target trials.\n"
    report+='''\n`research_lab.native_evidence` reads public retained files only and makes zero new target executions or model requests. Its historical pins are not the current MPLPB pin above; replaying those records does not newly validate the PR #43 implementation. No private adapter was needed or used.\n\n## Not tested because not public\n\n- Live OOCC controller.\n- Memory/Drive/SQL scheduler.\n- Recipient acceptance.\n- Unprepared original source records (matching the private benchmark packages).\n- Live adapter and independent readbacks.\n- E4 native integration acceptance.\n- E5 comparative validation.\n- Controlled operator-burden and re-entry measurements.\n- Reciprocal blinded scoring.\n\nThese labels follow the requested unavailable-evidence list; labels alone do not establish that a private package was examined. Matching a phrase in a public paper does not test the underlying private records. No private Drive, SQL, or controller paths were accessed. The temporary local ledger is a public-text fixture, not Ben's live system.\n\n## Observed source-authority behavior\n\n'''+summary+'''\n\nThis is the complete inspectable public comparison **within the requested first-15-pages, strict-reader and public-command scope**; it is not an exhaustive evaluation of every published page or all MPLPB capabilities. Private items remain **NOT_RUN** until furnished under the same version pins and blinded scoring. There is no global architectural victory claim.\n\n## Reproduction\n\nThe public clones and supplied attached PDFs/TXT are the only evidence inputs. Extraction requires `PyMuPDF==1.26.6`; repository source files are unmodified. `freeze.json` records the implementation pins, query list, profile, extractor version and runner hash before execution. Original PDFs are not copied into the evaluation directory.\n\n```sh\npython evaluation/public-papers/run.py --mplpb-root /workspace/mplpb --b-tests-root /workspace/b-tests --attachments /workspace/attachments --ledger /tmp/public-paper-ledger-repeat --output /tmp/public-paper-repeat\n```\n\nUse a fresh ledger path for each run. Exact text hashes, record content hashes and query decisions are deterministic with identical input bytes, PyMuPDF version and code pins. Temporary-root paths, unit-test durations and incidental diagnostic log paths can differ. Preserve original filenames from the attachment staging described above so short-name scopes remain identical.\n'''
    (a.output/'RESULTS.md').write_text(report,encoding='utf-8')
    save(a.output/'sha256.json',{p.name:digest(p.read_bytes()) for p in sorted(a.output.iterdir()) if p.is_file() and p.name!='sha256.json'})
    print(json.dumps({'report':str(a.output/'RESULTS.md'),'summary':summary,'query_counts':counts,'test_results':tests},indent=2))

if __name__=='__main__':main()
