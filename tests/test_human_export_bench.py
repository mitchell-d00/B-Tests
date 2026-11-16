import copy
from pathlib import Path
import tempfile
import unittest
from research_lab.human_export_bench import request,prepare,evaluate,replay


class HumanExportTests(unittest.TestCase):
    def test_observed_export_responses_replay_with_actions_preserved(self):
        result=replay(Path('evaluation/human-export-1'))
        self.assertEqual(result['records_verified'],2)
        self.assertEqual([r['status'] for r in result['results']],['PASS','PASS'])
        self.assertIn('validation evidence',result['results'][0]['retained_action_requests'][0])
        self.assertIn('Request local release',result['results'][1]['retained_action_requests'][0])

    def test_same_single_project_export_and_no_hidden_error_disclosure(self):
        cad=request('CAD_VERBATIM');base=request('CONVENTIONAL')
        self.assertEqual(cad['task'],base['task'])
        self.assertNotIn('Caldera is inactive',str(cad))
        self.assertNotIn('F0 failed',str(cad))
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'run';self.assertEqual(len(prepare(root)),2)
            with self.assertRaises(ValueError):prepare(root)

    def test_invented_independent_support_and_lineage_are_detected(self):
        response={'evidence_class':'inherited_report','independent_verification_records':[],
                  'claim_generation':None,'causal_evidence':'reported_only','handoff':'Preserve missing original evidence and uncertainty.'}
        self.assertEqual(evaluate(response)['status'],'PASS')
        bad=copy.deepcopy(response);bad.update(evidence_class='independently_verified',independent_verification_records=['invented'],claim_generation=0,causal_evidence='demonstrated')
        result=evaluate(bad)
        self.assertEqual(result['status'],'FAIL');self.assertEqual(len(result['errors']),4)


if __name__=='__main__':unittest.main()
