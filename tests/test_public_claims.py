"""Controls for the review harness, not new OOCC/model performance trials."""
import json
from pathlib import Path
import tempfile
import unittest
from research_lab.public_claims import analytical, comparisons, prepare_model_packets, score_model, reference_controls


class PublicClaimTests(unittest.TestCase):
    def test_number_comparison_replays_and_retains_contrary_cases(self):
        self.assertEqual(analytical(7,64),analytical(7,64))
        rows=analytical(7,2048)['numbers']
        self.assertEqual({r['exponent'] for r in rows},set(range(1,2049)))
        self.assertTrue(any(r['shorter_expression'] for r in rows))
        self.assertTrue(any(not r['shorter_expression'] for r in rows))
        self.assertTrue(all(r['same_integer'] for r in rows))
        for count in (0,2049,True):
            with self.assertRaises(ValueError):analytical(samples=count)

    def test_dictionary_cost_includes_first_definition(self):
        rows=analytical(11,3)['dictionary_costs']
        self.assertTrue(all(r['indexed_total_bytes']>=r['dictionary_bytes'] for r in rows))
        self.assertTrue(any(r['indexed_shorter'] for r in rows))
        self.assertTrue(any(not r['indexed_shorter'] for r in rows))

    def test_reference_program_is_explicitly_ours(self):
        with tempfile.TemporaryDirectory() as tmp:
            result=reference_controls(Path(tmp))
        self.assertIn('NOT Gelhaus',result['ownership'])
        self.assertTrue(all(r['passed'] for r in result['rows']))
        self.assertEqual(result['rows'][0]['referent_state'],'historical')

    def test_native_and_prompt_comparisons_are_never_pooled(self):
        rows={r['id']:r for r in comparisons()}
        self.assertEqual(rows['C5']['status'],'NOT_RUN')
        self.assertEqual(rows['C6']['status'],'NOT_RUN')
        self.assertNotEqual(rows['C4']['unit'],rows['C5']['unit'])

    def packet_fixture(self,root):
        cad=root/'cad.json';cad.write_text(json.dumps({'source_pdf_sha256':'a'*64,'passages':[{'pdf_page':7,'text':'Public instructions test fixture.'}]}))
        out=root/'prepared';prepare_model_packets(out,cad)
        return out

    def test_packet_task_identity_and_missing_responses_stay_not_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);out=self.packet_fixture(root)
            packets=[json.loads(p.read_text()) for p in (out/'packets').glob('*/request.json')]
            self.assertEqual(packets[0]['task'],packets[1]['task'])
            for folder in (out/'packets').iterdir():self.assertEqual(sorted(p.name for p in folder.iterdir()),['request.json'])
            score=score_model(out,root/'absent',root/'score.json')
            self.assertTrue(all(r['status']=='NOT_RUN' and r['correct'] is None for r in score['rows']))
            self.assertFalse(score['native_oocc_tested'])

    def test_quotes_cannot_substitute_for_correct_values_or_source_binding(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);out=self.packet_fixture(root);responses=root/'responses';responses.mkdir()
            key=json.loads((out/'custody/expected.json').read_text())
            assignment=json.loads((out/'custody/assignments.json').read_text())[0]
            ident=assignment['packet_id']
            answers=[{'id':qid,'value':target['value'],'citations':[{'source_id':target['source_id'],'quote':target['required_span']}]} for qid,target in key.items()]
            answers[0]['value']=True  # bool cannot impersonate integer1/4.
            answers[1]['citations']=[{'source_id':'ROOT','quote':'This is one original observation.'}]
            (responses/(ident+'.json')).write_text(json.dumps({'answers':answers}))
            report=score_model(out,responses,root/'score.json')
            observed=next(r for r in report['rows'] if r['status']=='RESPONSE_SCORED')
            self.assertEqual(observed['correct'],3)
            self.assertTrue(all(c['quotation_fidelity'] for c in observed['cases']))
            self.assertFalse(observed['model_identity_verified'])
            # Frozen input mutation is rejected, never silently relabelled.
            (out/'custody/expected.json').write_text('{}')
            with self.assertRaisesRegex(ValueError,'key changed'):score_model(out,responses,root/'other.json')

    def test_unrequested_claims_do_not_receive_a_perfect_contract_score(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);out=self.packet_fixture(root);responses=root/'responses';responses.mkdir()
            key=json.loads((out/'custody/expected.json').read_text())
            assignment=json.loads((out/'custody/assignments.json').read_text())[0]
            answers=[{'id':qid,'value':target['value'],'citations':[{'source_id':target['source_id'],'quote':target['required_span']}]} for qid,target in key.items()]
            (responses/(assignment['packet_id']+'.json')).write_text(json.dumps({'answers':answers,'unrequested_claim':'The private native controller was independently certified.'}))
            report=score_model(out,responses,root/'score.json')
            row=next(r for r in report['rows'] if r['status']!='NOT_RUN')
            self.assertEqual(row['status'],'INVALID_RESPONSE')



if __name__=='__main__':unittest.main()
