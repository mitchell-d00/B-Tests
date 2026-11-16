import copy
import json
import tempfile
import unittest
from pathlib import Path
from research_lab.oocc_adversarial import load_fixture,model_input,inspect,controls

class CorrectionControls(unittest.TestCase):
    def test_oracle_controls_are_explicitly_not_model_results(self):
        for row in controls():self.assertEqual(row['evidence_level'],'harness_self_test_only')

    def test_oracle_not_transmitted(self):
        for case in load_fixture()['cases']:
            a=model_input(case,'CAD_VERBATIM');b=model_input(case,'CONVENTIONAL')
            self.assertEqual(a['user'],b['user'])
            self.assertNotIn('expected_state',a['user'])
            self.assertNotIn('required_citations',a['user'])

    def test_poisoned_state_is_not_repaired_by_harness(self):
        case=load_fixture()['cases'][0]
        with tempfile.TemporaryDirectory() as folder:
            value={'working_state':case['initial_state'],'effect_requests':['release'],
                   'facts':case['expected_facts'],'citations':[],'source_reads_claimed':[]}
            r=inspect(case,json.dumps(value),Path(folder))
            self.assertEqual(r['status'],'FAIL')
            self.assertEqual(json.loads((Path(folder)/'committed_state.json').read_text()),case['initial_state'])
            self.assertEqual(json.loads((Path(folder)/'effects.jsonl').read_text())['operation'],'release')

    def test_bad_response_is_preserved_as_failure_not_clean_refusal(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertEqual(inspect(load_fixture()['cases'][0],'OK',Path(folder))['status'],'FAIL')

if __name__=='__main__':unittest.main()
