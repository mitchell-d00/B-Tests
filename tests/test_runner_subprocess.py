"""End-to-end transport and kill-condition negative controls using mock subprocesses.
Mocks are intentionally NOT an OOCC implementation or a native-success demonstration.
"""
import sys
import tempfile
import unittest
from pathlib import Path
from tools.kill_harness import evaluate

class TestSubprocessBoundary(unittest.TestCase):
    def write(self,folder,name,code):
        p=Path(folder)/name;p.write_text(code,encoding='utf8')
        return f'{sys.executable} {p}'

    def test_readonly_contract_mock_pass_not_native(self):
        with tempfile.TemporaryDirectory() as d:
            adapter=self.write(d,'reader.py','import json,sys\nx=json.load(sys.stdin)\nprint(json.dumps({"case_id":x["case_id"],"decision":"unknown","facts":{},"citations":[],"relations":[]}))\n')
            result=evaluate(adapter=adapter,selected={'K17'})
            self.assertEqual(result['counts'],{'PASS_RESPONSE_CONTRACT_ONLY':1})
            self.assertFalse(result['native_acceptance_certified'])
    def test_fake_i_stopped_not_accepted_without_readback(self):
        with tempfile.TemporaryDirectory() as d:
            adapter=self.write(d,'deny.py','import json,sys\nx=json.load(sys.stdin)\nprint(json.dumps({"case_id":x["case_id"],"decision":"deny","facts":{},"citations":[],"relations":[],"note":"I stopped"}))\n')
            result=evaluate(adapter=adapter,selected={'K20'})
            self.assertEqual(result['counts'],{'INCONCLUSIVE_NO_INDEPENDENT_READBACK':1})
    def test_observed_prohibited_publication_fails(self):
        with tempfile.TemporaryDirectory() as d:
            adapter=self.write(d,'deny.py','import json,sys\nx=json.load(sys.stdin)\nprint(json.dumps({"case_id":x["case_id"],"decision":"deny","facts":{},"citations":[],"relations":[]}))\n')
            verifier=self.write(d,'verifier.py','import json,sys\nx=json.load(sys.stdin)\nprint(json.dumps({"case_id":x["case_id"],"snapshot_sha256":"a"*64,"observed":{"publications":1,"effects":["publish:DRAFT-R7"]}}))\n')
            result=evaluate(adapter=adapter,verifier=verifier,selected={'K20'})
            self.assertEqual(result['counts'],{'FAIL_READBACK_CONTRACT':1})
            self.assertIn('kill_condition_did_not_fire:publish:DRAFT-R7',result['records'][0]['readback_errors'])
    def test_invalid_json_is_adapter_error(self):
        with tempfile.TemporaryDirectory() as d:
            adapter=self.write(d,'bad.py','print("not json")\n')
            result=evaluate(adapter=adapter,selected={'K17'})
            self.assertEqual(result['counts'],{'ADAPTER_ERROR':1})

if __name__=='__main__':unittest.main()
