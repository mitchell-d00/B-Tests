"""Tests for the separation-effect analysis.

Each test plants a known pattern of judge behaviour and checks the analysis
reports it correctly, including each way the paper's claim could fail.
"""

import random
import shutil
import tempfile
import unittest
from pathlib import Path

from wie import ACCEPT, REJECT
from wie.freeze import freeze
from wie.generate import generate
from wie.separation import parse_label, separation_effect
from wie.util import read_jsonl, write_jsonl


class SepBase(unittest.TestCase):
    PER_CLASS = 12

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.run = self.tmp / "run"
        generate(self.run, seed=11, per_class=self.PER_CLASS)
        freeze(self.run)
        self.key = {r["case_id"]: r for r in read_jsonl(self.run / "sealed" / "key.jsonl")}
        self.rng = random.Random(3)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def judge(self, label, catch, false_alarm, abstain=0.0):
        """Write a synthetic judge: catches each incorrect case with prob `catch`,
        rejects each correct case with prob `false_alarm`."""
        rows = []
        for cid, k in sorted(self.key.items()):
            r = self.rng.random()
            if r < abstain:
                v = "ABSTAIN"
            elif k["expected"] == REJECT:
                v = REJECT if self.rng.random() < catch else ACCEPT
            else:
                v = REJECT if self.rng.random() < false_alarm else ACCEPT
            rows.append({"case_id": cid, "verdict": v, "reason": "synthetic"})
        write_jsonl(self.run / "verdicts" / f"{label}.jsonl", rows)

    def copy(self, src, dst):
        """A judge at another level giving exactly the same verdicts: a true null."""
        rows = read_jsonl(self.run / "verdicts" / f"{src}.jsonl")
        write_jsonl(self.run / "verdicts" / f"{dst}.jsonl", rows)

    def analyse(self, **kw):
        return separation_effect(self.run, perms=kw.pop("perms", 800), **kw)


class TestParse(unittest.TestCase):
    def test_labels(self):
        self.assertEqual(parse_label("I3_cross__report_plus_state__grok"), ("I3", "report_plus_state", "grok"))
        self.assertEqual(parse_label("I2_fresh__report_only__codex"), ("I2", "report_only", "codex"))
        self.assertEqual(parse_label("I4_retained_state"), ("I4", "native", None))


class TestSeparationEffect(SepBase):
    def test_graded_improvement_supports(self):
        for lvl, cat in (("I0_model", 0.05), ("I2_fresh", 0.5), ("I3_cross", 0.9)):
            self.judge(f"{lvl}__report_plus_state__m", cat, 0.05)
        r = self.analyse()
        s = r["strata"]["model_report_plus_state"]
        self.assertGreater(s["slope_BA_per_level"], 0.1)
        self.assertLess(s["p_one_sided"], 0.01)
        self.assertEqual(r["verdict"]["status"], "SUPPORTS")

    def test_flat_performance_weakens(self):
        self.judge("I0_model__report_plus_state__m", 0.6, 0.1)
        for lvl in ("I2_fresh", "I3_cross"):
            self.copy("I0_model__report_plus_state__m", f"{lvl}__report_plus_state__m")
        r = self.analyse()
        self.assertAlmostEqual(r["strata"]["model_report_plus_state"]["slope_BA_per_level"], 0.0)
        self.assertGreater(r["strata"]["model_report_plus_state"]["p_one_sided"], 0.05)
        self.assertEqual(r["verdict"]["status"], "WEAKENS")

    def test_reversed_order_weakens(self):
        for lvl, cat in (("I0_model", 0.9), ("I2_fresh", 0.5), ("I3_cross", 0.1)):
            self.judge(f"{lvl}__report_plus_state__m", cat, 0.05)
        r = self.analyse()
        self.assertLess(r["strata"]["model_report_plus_state"]["slope_BA_per_level"], 0)
        self.assertEqual(r["verdict"]["status"], "WEAKENS")

    def test_stricter_is_not_better(self):
        # Higher level catches everything only by rejecting everything: kill condition 2.
        self.judge("I0_model__report_plus_state__m", 0.1, 0.0)
        self.judge("I3_cross__report_plus_state__m", 1.0, 1.0)
        r = self.analyse()
        s = r["strata"]["model_report_plus_state"]
        self.assertTrue(s["lowest_to_highest"]["skeptical_not_discriminating"])
        self.assertLessEqual(s["slope_BA_per_level"], 0.0)
        self.assertEqual(r["verdict"]["status"], "WEAKENS")
        self.assertTrue(any("stricter, not better" in n for n in r["verdict"]["notes"]))

    def test_reject_all_scores_like_accept_all(self):
        self.judge("I0_model__report_only__m", 0.0, 0.0)
        self.judge("I2_fresh__report_only__m", 1.0, 1.0)
        js = {j["label"]: j for j in self.analyse()["strata"]["model_report_only"]["judges"]}
        self.assertAlmostEqual(js["I0_model__report_only__m"]["BA"], 0.5)
        self.assertAlmostEqual(js["I2_fresh__report_only__m"]["BA"], 0.5)

    def test_evidence_not_separation(self):
        # Kill condition 3's confound: state access helps, separation doesn't.
        self.judge("I0_model__report_only__m", 0.2, 0.05)
        self.judge("I0_model__report_plus_state__m", 0.9, 0.05)
        for lvl in ("I2_fresh", "I3_cross"):
            self.copy("I0_model__report_only__m", f"{lvl}__report_only__m")
            self.copy("I0_model__report_plus_state__m", f"{lvl}__report_plus_state__m")
        r = self.analyse()
        self.assertEqual(r["verdict"]["status"], "WEAKENS")
        self.assertTrue(all(e["delta_BA_from_state"] > 0.2 for e in r["evidence_effect"]))
        self.assertTrue(any("adding state changed BA" in n for n in r["verdict"]["notes"]))

    def test_mixed_when_only_one_mode_shows_effect(self):
        for lvl, cat in (("I0_model", 0.1), ("I2_fresh", 0.5), ("I3_cross", 0.9)):
            self.judge(f"{lvl}__report_plus_state__m", cat, 0.05)
        self.judge("I0_model__report_only__m", 0.3, 0.05)
        for lvl in ("I2_fresh", "I3_cross"):
            self.copy("I0_model__report_only__m", f"{lvl}__report_only__m")
        self.assertEqual(self.analyse()["verdict"]["status"], "MIXED")

    def test_abstain_counts_against_overall_judgment(self):
        self.judge("I0_model__report_only__m", 1.0, 0.0, abstain=0.0)
        self.judge("I2_fresh__report_only__m", 1.0, 0.0, abstain=0.5)
        js = {j["label"]: j for j in self.analyse()["strata"]["model_report_only"]["judges"]}
        self.assertAlmostEqual(js["I0_model__report_only__m"]["BA"], 1.0)
        self.assertLess(js["I2_fresh__report_only__m"]["BA"], 0.8)

    def test_permutation_is_deterministic(self):
        for lvl, cat in (("I0_model", 0.3), ("I3_cross", 0.6)):
            self.judge(f"{lvl}__report_only__m", cat, 0.1)
        a = self.analyse(seed=5)["strata"]["model_report_only"]["p_one_sided"]
        b = self.analyse(seed=5)["strata"]["model_report_only"]["p_one_sided"]
        self.assertEqual(a, b)

    def test_single_level_is_not_run(self):
        self.judge("I2_fresh__report_only__a", 0.5, 0.1)
        self.judge("I2_fresh__report_only__b", 0.6, 0.1)
        self.assertEqual(self.analyse()["verdict"]["status"], "NOT_RUN")

    def test_refuses_tampered_run(self):
        self.judge("I0_model__report_only__m", 0.5, 0.1)
        self.judge("I2_fresh__report_only__m", 0.5, 0.1)
        p = next((self.run / "cases").rglob("report.json"))
        p.write_text(p.read_text() + " ")
        with self.assertRaises(Exception):
            self.analyse()

    def test_writes_report(self):
        self.judge("I0_model__report_only__m", 0.2, 0.1)
        self.judge("I3_cross__report_only__m", 0.8, 0.1)
        self.analyse()
        md = (self.run / "results" / "SEPARATION.md").read_text()
        self.assertIn("Effect of evaluator separation on overall judgment", md)
        self.assertIn("model_report_only", md)


class TestFalseSupportRate(SepBase):
    def test_no_effect_rarely_reported_as_support(self):
        # Independent noisy judges with identical true ability, many runs.
        # A sound test should call SUPPORTS/MIXED in roughly alpha of them or fewer.
        wrong, runs = 0, 30
        for s in range(runs):
            self.rng = random.Random(500 + s)
            for f in (self.run / "verdicts").glob("*.jsonl"):
                f.unlink()
            for lvl in ("I0_model", "I2_fresh", "I3_cross"):
                for ev in ("report_only", "report_plus_state"):
                    self.judge(f"{lvl}__{ev}__m", 0.6, 0.1)
            wrong += self.analyse(perms=200, seed=s)["verdict"]["status"] != "WEAKENS"
        self.assertLessEqual(wrong, 4, f"{wrong}/{runs} null runs reported as support")


class TestDeterministicJudgesOnDemo(SepBase):
    def test_deterministic_stratum_is_flagged_as_confounded(self):
        from wie.judges import run_deterministic
        run_deterministic(self.run)
        r = self.analyse()
        self.assertIn("all_judges", r["strata"])
        self.assertIn("confounded", r["verdict"]["basis"])
        # Deterministic judges see different evidence, so no verdict may be issued.
        self.assertEqual(r["verdict"]["status"], "CONFOUNDED_NO_VERDICT")



class TestAbstentionMetrics(SepBase):
    def test_abstention_reduces_accuracy_and_coverage_without_a_false_alarm(self):
        self.judge("I0_model__report_only__a", catch=0, false_alarm=0, abstain=1)
        self.judge("I2_fresh__report_only__a", catch=0, false_alarm=0)
        result = self.analyse(perms=20)["strata"]["model_report_only"]
        baseline = result["judges"][0]
        self.assertEqual((baseline["BA"], baseline["F"], baseline["coverage"]), (0, 0, 0))
        self.assertEqual(baseline["abstentions_on_correct"], 2 * self.PER_CLASS)
        self.assertEqual(result["lowest_to_highest"]["delta_F"], 0)
        self.assertEqual(result["lowest_to_highest"]["delta_BA"], 0.5)


if __name__ == "__main__":
    unittest.main()
