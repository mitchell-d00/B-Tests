import copy
from pathlib import Path
import unittest
from research_lab.propagation_bench import packet,evaluate,replay


class PropagationTests(unittest.TestCase):
    def test_preserved_actual_chains_replay_without_truth_detection_claim(self):
        result=replay(Path('evaluation/propagation-1'))
        self.assertEqual(result['records_verified'],6)
        self.assertEqual([r['status'] for r in result['results']],['PASS','PASS','PASS','PASS','PASS','FAIL'])
        self.assertTrue(all(r['outside_world_truth_detection']=='INCONCLUSIVE' for r in result['results']))
        self.assertEqual(result['results'][-1]['errors'],['compression_budget_not_met'])

    def test_only_original_access_changes_and_derivative_roots_never_multiply(self):
        for stage,count in enumerate((10,100,1000)):
            task=packet('CONVENTIONAL',stage)['task']
            self.assertEqual(len(task['promoted_descendants']),count)
            self.assertEqual({tuple(r['provenance_roots']) for r in task['promoted_descendants']},{('OBS-01',)})
            self.assertEqual('body' in task['archived_original'],stage==0)
            self.assertNotIn('actually inactive',str(task))

    def test_harness_detects_authority_inflation_without_repairing_submission(self):
        response={'working_state':{'source_supported_projects':['P0'],'independent_evidence_roots':['OBS-01'],'accepted_causal_edges':[]},'action_requests':['P0'],'source_reads_claimed':[],'handoff':'Keep original scope and root.'}
        self.assertEqual(evaluate(2,response)['status'],'PASS')
        bad=copy.deepcopy(response);bad['working_state']['source_supported_projects'].append('P1')
        bad['working_state']['independent_evidence_roots'].append('DER-2-0001');bad['action_requests'].append('P1')
        result=evaluate(2,bad)
        self.assertEqual(result['status'],'FAIL')
        self.assertIn('derivatives_promoted_to_independent_evidence',result['errors'])
        self.assertEqual(bad['action_requests'],['P0','P1'])


if __name__=='__main__':unittest.main()
