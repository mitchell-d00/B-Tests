"""Repeat the existing 12 public-paper queries from public, hash-pinned extracted text."""
import argparse,hashlib,json,subprocess,sys,tempfile
from pathlib import Path
REV='ccbb5804eb47f78c2338d57c142ad087b47be710'
BASE=Path(__file__).resolve().parents[3]/'evaluation/public-papers'
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--mplpb-root',type=Path,default=Path('/workspace/mplpb'));p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=False)
 assert subprocess.check_output(['git','-C',str(a.mplpb_root),'rev-parse','HEAD'],text=True).strip()==REV
 sys.path.insert(0,str(a.mplpb_root.resolve()))
 from mplpb_combined.ledger import write,seal
 from mplpb_combined.reader import answer,Profile
 manifest=json.loads((BASE/'manifest.json').read_text());original=json.loads((BASE/'queries.json').read_text());when=json.loads((BASE/'freeze.json').read_text())['when']
 freeze={'revision':REV,'source_manifest_sha256':hashlib.sha256((BASE/'manifest.json').read_bytes()).hexdigest(),'runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'inputs':'Existing public first-15-page extractions and supplied excerpt; not the newly supplied full Ben text.'}
 (a.out/'freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
 rows=[]
 with tempfile.TemporaryDirectory(prefix='current-public-paper-ledger-') as ledger:
  for row in manifest:
   raw=(BASE/row['text_file']).read_bytes();assert hashlib.sha256(raw).hexdigest()==row['text_sha256']
   record=write(ledger,doc_id=row['ledger_id'],title=row['short_name'],scope=row['short_name'],body=raw.decode(),when=when,source_authorship='unknown');seal(ledger,when=when)
   assert record.hash==row['ledger_hash']
  for old in original:
   result=answer(ledger,old['query'],Profile('open',None,True));view=result.to_dict();expected=dict(old['answer']);observed=dict(view);expected.pop('root',None);observed.pop('root',None)
   rows.append({'query':old['query'],'kind':result.kind,'answer':view,'identical_to_prior_except_root':observed==expected,'answer_supported_field_present':hasattr(result,'answer_supported') or 'answer_supported' in view})
 (a.out/'results.json').write_text(json.dumps({'revision':REV,'results':rows,'all_identical_except_root':all(r['identical_to_prior_except_root'] for r in rows)},indent=2,ensure_ascii=False)+'\n')
 print('Public-paper answers identical except root:',all(r['identical_to_prior_except_root'] for r in rows))
if __name__=='__main__':main()
