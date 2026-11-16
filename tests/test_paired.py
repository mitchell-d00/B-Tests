"""Self-tests for scoring and audit boundaries. Do not count as OOCC passes."""
import json
from pathlib import Path
import tempfile
import unittest
from side_by_side.run import load_manifest, prompt, validate_model_response, execute, run_mplpb, PIN


class PairedHarnessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = load_manifest()
        cls.cases = {x['id']: x for x in cls.m['cases']}

    def test_no_duplicate_cases(self):
        self.assertEqual(len(self.cases), 16)

    def test_references_pin_mplpb(self):
        self.assertEqual(self.m['mplpb_pin'], PIN)

    def test_cad_and_baseline_see_identical_evidence(self):
        for c in self.m['cases']:
            self.assertEqual(prompt(c,'CAD')['user'],prompt(c,'BASELINE')['user'])
            self.assertNotEqual(prompt(c,'CAD')['system'],prompt(c,'BASELINE')['system'])

    def test_correct_exact_answer_passes(self):
        c=self.cases['SH01']
        self.assertEqual(validate_model_response(c, {'decision':'ANSWER','answer':'for sculpture','evidence_ids':['S1']})[0],'INCONCLUSIVE')

    def test_absent_citation_fails(self):
        c=self.cases['SH01']
        self.assertEqual(validate_model_response(c, {'decision':'ANSWER','answer':'for sculpture','evidence_ids':[]})[0],'FAIL')

    def test_fabricated_citation_fails(self):
        c=self.cases['SH01']
        self.assertEqual(validate_model_response(c, {'decision':'ANSWER','answer':'for sculpture','evidence_ids':['INVENTED']})[0],'FAIL')

    def test_false_continuation_fails(self):
        c=self.cases['CAD13']
        self.assertEqual(validate_model_response(c, {'decision':'ANSWER','answer':'proven','evidence_ids':['MAP-C']})[0],'FAIL')

    def test_unwarranted_causation_fails(self):
        c=self.cases['CAD16']
        self.assertEqual(validate_model_response(c, {'decision':'ANSWER','answer':'B copied A','evidence_ids':['A-2020']})[0],'FAIL')

    def test_refusal_passes_only_matching_oracle(self):
        c=self.cases['CAD16']
        self.assertEqual(validate_model_response(c, {'decision':'REFUSE','answer':'Exposure not documented','evidence_ids':['A-2020','B-2023']})[0],'INCONCLUSIVE')

    def test_unsupported_arms_not_run(self):
        r=execute(self.m, None, None, 3, max_cases=2)
        self.assertEqual(r['arms']['CAD'],{'NOT_RUN':2})
        self.assertEqual(r['arms']['BASELINE'],{'NOT_RUN':2})
        self.assertEqual(r['arms']['MPLPB'],{'NOT_RUN':2})

    def test_no_native_as_theory_of_everything_proxy(self):
        c=self.cases['CAD12']
        r=run_mplpb(c,Path('/unavailable'))
        self.assertEqual(r['status'],'OUT_OF_SCOPE')

    def test_missing_native_source_marks_not_run(self):
        c=self.cases['SH01']
        r=run_mplpb(c,Path('/unavailable'))
        self.assertEqual(r['status'],'NOT_RUN')

    def test_unknown_manifest_schema_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'cases.json'
            p.write_text(json.dumps({'schema':'made-up','mplpb_pin':PIN}))
            with self.assertRaises(ValueError): load_manifest(p)

if __name__=='__main__': unittest.main()
