"""Check failure modes in matched-evidence Witness comparisons."""

from fractions import Fraction
import importlib.util
from pathlib import Path
import unittest


PATH = Path(__file__).resolve().parents[1] / "evaluation/witness-section19/live/separation.py"
SPEC = importlib.util.spec_from_file_location("witness_separation", PATH)
SEPARATION = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SEPARATION)

TRUTH = {"bad1": "REJECT", "bad2": "REJECT", "good1": "ACCEPT", "good2": "ACCEPT"}
ACCEPT_ALL = dict.fromkeys(TRUTH, "ACCEPT")
REJECT_ALL = dict.fromkeys(TRUTH, "REJECT")
STEP = "I0_model->I2_fresh"


def crossed(arms_by_level):
    return {(level, mode): verdict
            for level, verdicts in zip(SEPARATION.LEVELS, arms_by_level)
            for mode, verdict in zip(SEPARATION.MODES, verdicts)}


class WitnessSeparationTests(unittest.TestCase):
    def test_greater_rejection_does_not_imply_discrimination(self):
        arms = crossed([(ACCEPT_ALL, ACCEPT_ALL), (REJECT_ALL, REJECT_ALL), (TRUTH, TRUTH)])
        result = SEPARATION.analyze(TRUTH, arms)
        step = result["by_matched_evidence"]["report_only"][STEP]
        self.assertEqual(step["delta"]["E"], 1)
        self.assertEqual(step["delta"]["F"], 1)
        self.assertIn("detection_gain_offset_by_false_alarms", step["reasons"])
        self.assertFalse(result["monotonic_quality_gain"])

    def test_gain_exceeding_false_alarm_budget_still_fails(self):
        candidate = {**TRUTH, "good1": "REJECT"}
        arms = crossed([(ACCEPT_ALL, ACCEPT_ALL), (candidate, candidate), (TRUTH, TRUTH)])
        step = SEPARATION.analyze(TRUTH, arms)["by_matched_evidence"]["report_only"][STEP]
        self.assertGreater(step["delta"]["J"], 0)
        self.assertEqual(step["reasons"], ["false_alarm_increase_exceeds_limit"])

    def test_evidence_improvement_cannot_be_credited_to_separation(self):
        arms = crossed([(ACCEPT_ALL, TRUTH)] * 3)
        result = SEPARATION.analyze(TRUTH, arms)
        self.assertTrue(result["evidence_gain_without_matched_separation_gain"])
        self.assertFalse(result["monotonic_quality_gain"])
        self.assertTrue(all(row["status"] == "QUALITY_GAIN"
                            for row in result["evidence_added_within_judge"].values()))

    def test_abstention_can_raise_j_while_reducing_correct_decisions(self):
        baseline = {**TRUTH, "good1": "REJECT"}
        candidate = {**TRUTH, "good1": "ABSTAIN", "good2": "ABSTAIN"}
        arms = crossed([(baseline, baseline), (candidate, candidate), (TRUTH, TRUTH)])
        step = SEPARATION.analyze(TRUTH, arms)["by_matched_evidence"]["report_only"][STEP]
        self.assertEqual(step["delta"]["J"], Fraction(1, 2))
        self.assertEqual(step["delta"]["balanced_correct_verdict_rate"], Fraction(-1, 4))
        self.assertIn("coverage_loss_exceeds_limit", step["reasons"])

    def test_a_gain_with_state_does_not_make_the_gradient_monotonic(self):
        halfway = {**ACCEPT_ALL, "bad1": "REJECT"}
        arms = crossed([(ACCEPT_ALL, ACCEPT_ALL), (halfway, halfway), (ACCEPT_ALL, TRUTH)])
        result = SEPARATION.analyze(TRUTH, arms)
        last = "I2_fresh->I3_cross"
        self.assertEqual(result["by_matched_evidence"]["report_plus_state"][last]["status"], "QUALITY_GAIN")
        self.assertEqual(result["interaction_added_state_minus_report_only"][last]["J"], 1)
        self.assertFalse(result["monotonic_quality_gain"])

    def test_genuine_monotonic_detection_gain_is_recognized(self):
        halfway = {**ACCEPT_ALL, "bad1": "REJECT"}
        arms = crossed([(ACCEPT_ALL, ACCEPT_ALL), (halfway, halfway), (TRUTH, TRUTH)])
        result = SEPARATION.analyze(TRUTH, arms)
        self.assertTrue(result["monotonic_quality_gain"])
        self.assertTrue(result["monotonic_detection_gain"])
        step = result["by_matched_evidence"]["report_only"][STEP]
        self.assertEqual(step["correct_verdict_switches"], {"wins": 1, "losses": 0})

    def test_missing_cases_are_not_silently_dropped_or_counted_as_abstentions(self):
        arms = crossed([(ACCEPT_ALL, ACCEPT_ALL), (TRUTH, TRUTH), (TRUTH, TRUTH)])
        arms["I2_fresh", "report_only"] = {k: v for k, v in TRUTH.items() if k != "good2"}
        result = SEPARATION.analyze(TRUTH, arms)
        step = result["by_matched_evidence"]["report_only"][STEP]
        self.assertEqual(step["status"], "INCONCLUSIVE")
        self.assertEqual(step["missing_after"], ["good2"])
        self.assertIsNone(result["monotonic_quality_gain"])

    def test_missing_ground_truth_class_is_inconclusive(self):
        result = SEPARATION.analyze({"bad": "REJECT"}, crossed([({"bad": "REJECT"}, {"bad": "REJECT"})] * 3))
        self.assertIsNone(result["monotonic_quality_gain"])
        self.assertTrue(result["by_matched_evidence"]["report_only"][STEP]["missing_class"])
