"""Harness integrity checks. These unit tests are outside the empirical pilot."""

import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest


LAB = Path(__file__).resolve().parents[1] / "evaluation/witness-section19/live"


class WitnessLiveHarness(unittest.TestCase):
    def effect(self, root, mode, *options):
        return subprocess.run(
            [sys.executable, "-I", str(LAB / "effects.py"), mode, str(root), *options],
            capture_output=True, text=True, timeout=10, check=False,
        )

    def test_writer_and_observer_use_real_slot_and_policy(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            policy = root / "policy.json"
            policy.write_text('{"write_allowed":false}', encoding="utf-8")
            refused = self.effect(root, "write", "--value", "available")
            self.assertEqual(refused.returncode, 77)
            before = self.effect(root, "observe")
            self.assertIsNone(json.loads(before.stdout)["status.txt"])
            policy.write_text('{"write_allowed":true}', encoding="utf-8")
            stalled = self.effect(root, "write", "--value", "available", "--fault", "ack_only")
            self.assertEqual(stalled.returncode, 0)
            self.assertIsNone(json.loads(self.effect(root, "observe").stdout)["status.txt"])
            committed = self.effect(root, "write", "--value", "discontinued")
            self.assertEqual(committed.returncode, 0)
            actual = json.loads(self.effect(root, "observe").stdout)
            self.assertEqual(actual["status.txt"]["text"], "discontinued\n")

    def test_missing_model_has_no_fabricated_scores(self):
        with TemporaryDirectory() as directory:
            out = Path(directory) / "run"
            subprocess.run([sys.executable, str(LAB / "run.py"), "--out", str(out)],
                           capture_output=True, timeout=10, check=True)
            scored = subprocess.run([sys.executable, str(LAB / "score.py"), str(out)],
                                    capture_output=True, timeout=10, check=True)
            summary = json.loads(scored.stdout)
            self.assertEqual(summary["scored_cases"], 0)
            self.assertEqual(summary["inventory"], {"NOT_RUN": 12})
            for condition in summary["evaluators"].values():
                self.assertIsNone(condition["E"])
                self.assertIsNone(condition["F"])

    def test_seeded_case_packet_is_repeatable(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            paths = [root / "first", root / "second"]
            for path in paths:
                subprocess.run([sys.executable, str(LAB / "handoff.py"), "generate",
                                "--seed", "19226", "--rounds", "2", "--out", str(path)],
                               capture_output=True, timeout=10, check=True)
            once, again = [(path / "protocol.json").read_bytes() for path in paths]
            self.assertEqual(once, again)
            cases = json.loads(once)["cases"]
            self.assertEqual(len(cases), 24)
            self.assertEqual(len({case["id"] for case in cases}), 24)
