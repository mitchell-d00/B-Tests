from pathlib import Path
import unittest
from research_lab.native_evidence import replay


class NativeEvidenceTests(unittest.TestCase):
    def test_unmodified_full_native_suite_and_environment_failure_are_both_retained(self):
        result=replay(Path('evaluation/mplpb-native'))
        old,new=result['native_suite_records']
        self.assertEqual(old['python_tests'],875)
        self.assertEqual(old['counts']['FAIL'],1)
        self.assertEqual(new['python_tests'],887)
        self.assertEqual(new['counts'],{'PASS':8,'FAIL':0,'NOT_RUN':0})

    def test_component_checks_preserve_exact_counts(self):
        component=replay(Path('evaluation/mplpb-native'))['component_checks']
        self.assertEqual(component['status'],'PASS')
        self.assertEqual(component['suite_lines'],['combined (this repo)    887 tests  OK','smart-local              52 tests  OK','swarm                   145 tests  OK','networked                61 tests  OK','image                    93 tests  OK'])

    def test_paired_current_guards_and_historical_gaps_are_not_erased(self):
        result=replay(Path('evaluation/mplpb-native'))['paired_results']
        old=[r for r in result if r['revision'].startswith('257e')]
        current=[r for r in result if r['revision'].startswith('cc21')]
        self.assertEqual(len(old),7);self.assertEqual(len(current),7)
        self.assertEqual([r['case'] for r in old if r['status']=='FAIL'],['contradictory_claim','claim_only_chain'])
        self.assertTrue(all(r['status']=='PASS' for r in current))
        self.assertTrue(next(r for r in current if r['case']=='supported_control')['observed_effect'])
        self.assertFalse(next(r for r in current if r['case']=='unavailable_original')['observed_effect'])


if __name__=='__main__':unittest.main()
