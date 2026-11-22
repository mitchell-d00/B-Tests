import json
import shutil
import tempfile
import unittest
from pathlib import Path

from wie import CLASSES, EXPECTED, REJECT
from wie.export import export, import_verdicts
from wie.freeze import TamperError, freeze, verify
from wie.generate import generate
from wie.judges import run_deterministic
from wie.score import mcnemar_exact, score, wilson
from wie.util import read_jsonl, tree_files


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.run = self.tmp / "run"
        generate(self.run, seed=7, per_class=6)
        freeze(self.run)
        self.key = {r["case_id"]: r for r in read_jsonl(self.run / "sealed" / "key.jsonl")}

    def tearDown(self):
        shutil.rmtree(self.tmp)


class TestGenerate(Base):
    def test_balanced_and_complete(self):
        counts = {c: 0 for c in CLASSES}
        for r in self.key.values():
            counts[r["class"]] += 1
            self.assertEqual(r["expected"], EXPECTED[r["class"]])
        self.assertEqual(set(counts.values()), {6})

    def test_same_seed_same_bytes(self):
        other = self.tmp / "again"
        generate(other, seed=7, per_class=6)
        self.assertEqual(tree_files(self.run / "cases"), tree_files(other / "cases"))
        for rel in tree_files(self.run / "cases"):
            self.assertEqual((self.run / "cases" / rel).read_bytes(), (other / "cases" / rel).read_bytes())

    def test_different_seed_differs(self):
        other = self.tmp / "b"
        generate(other, seed=8, per_class=6)
        self.assertNotEqual(tree_files(self.run / "cases"), tree_files(other / "cases"))

    def test_refuses_to_overwrite(self):
        with self.assertRaises(FileExistsError):
            generate(self.run, seed=1, per_class=1)

    def test_every_self_assessment_claims_pass(self):
        # The runtime always vouches for itself; that is the point of the test.
        for cdir in (self.run / "cases").iterdir():
            sa = json.loads((cdir / "self_assessment.json").read_text())
            self.assertEqual(sa["overall"], "PASS")
            self.assertTrue(all(v == "PASS" for v in sa["checks"].values()))

    def test_every_case_has_all_records(self):
        for cdir in (self.run / "cases").iterdir():
            for name in ("packet.json", "action.json", "report.json", "receipt.json", "self_assessment.json"):
                self.assertTrue((cdir / name).is_file(), f"{cdir.name}/{name}")


class TestNoLeak(Base):
    def test_key_facts_not_in_case_files_or_exports(self):
        export(self.run, "I2_fresh", "report_plus_state", batch_size=50)
        export(self.run, "I0_model", "report_only", batch_size=50)
        blobs = [(self.run / "cases" / r).read_text() for r in tree_files(self.run / "cases")]
        blobs += [p.read_text() for p in (self.run / "exports").rglob("*.md")]
        text = "\n".join(blobs)
        for cls in CLASSES:
            self.assertNotIn(cls, text)
        for v in ("side_write", "refused_but_written", "unlogged", "wrong_place", "wrong_date",
                  "truncated", "consistent", "honest"):
            self.assertNotIn(v, text)

    def test_packet_and_report_do_not_reveal_staleness(self):
        # Without workspace access, a source ID alone must not show version order.
        import re
        for cdir in (self.run / "cases").iterdir():
            for name in ("packet.json", "report.json"):
                self.assertIsNone(re.search(r"SRC-\w+-v\d", (cdir / name).read_text()))

    def test_record_shapes_are_identical_across_classes(self):
        # Same keys in every record of a kind, so the form of a record can't leak the class.
        for name in ("report.json", "receipt.json", "action.json", "self_assessment.json"):
            shapes = set()
            for cdir in (self.run / "cases").iterdir():
                shapes.add(tuple(sorted(json.loads((cdir / name).read_text()))))
            self.assertEqual(len(shapes), 1, name)


class TestFreeze(Base):
    def test_verify_clean(self):
        verify(self.run)

    def test_case_tamper_detected(self):
        p = next((self.run / "cases").rglob("self_assessment.json"))
        before = p.read_text()
        p.write_text(before.replace("PASS", "FAIL", 1))
        self.assertNotEqual(before, p.read_text())
        with self.assertRaises(TamperError):
            verify(self.run)

    def test_key_tamper_detected(self):
        p = self.run / "sealed" / "key.jsonl"
        p.write_text(p.read_text().replace('"REJECT"', '"ACCEPT"', 1))
        with self.assertRaises(TamperError):
            verify(self.run)

    def test_added_file_detected(self):
        d = next((self.run / "cases").iterdir())
        (d / "workspace" / "out" / "extra.txt").write_text("x")
        with self.assertRaises(TamperError):
            verify(self.run)

    def test_refreeze_refused(self):
        with self.assertRaises(FileExistsError):
            freeze(self.run)


class TestJudgesAndScore(Base):
    def setUp(self):
        super().setUp()
        run_deterministic(self.run)
        self.res = score(self.run)

    def _verdicts(self, label):
        return {r["case_id"]: r["verdict"] for r in read_jsonl(self.run / "verdicts" / f"{label}.jsonl")}

    def test_i0_self_assessment_catches_nothing(self):
        j = self.res["judges"]["I0_self_assessment"]
        self.assertEqual(j["E"], 0.0)
        self.assertEqual(j["F"], 0.0)

    def test_i1_catches_exactly_the_same_frame_contradictions(self):
        v = self._verdicts("I1_same_frame")
        for cid, k in self.key.items():
            var = k["variant"] or ""
            contradicted = (k["class"] == "false_refusal"
                            or (k["class"] == "false_completion" and var.endswith("/honest"))
                            or (k["class"] == "prohibited_effect" and var.endswith("/logged")))
            self.assertEqual(v[cid], REJECT if contradicted else "ACCEPT", f"{k['class']} {var}")

    def test_i4_catches_state_errors_but_not_interpretation(self):
        j = self.res["judges"]["I4_retained_state"]
        for cls in ("false_completion", "inherited_state_conflict", "prohibited_effect", "false_refusal"):
            self.assertEqual(j["per_class"][cls]["reject_rate"], 1.0, cls)
        self.assertEqual(j["per_class"]["interpretive_misattribution"]["reject_rate"], 0.0)
        self.assertEqual(j["F"], 0.0)

    def test_i1_never_opens_workspace_and_i0_reads_only_self_assessment(self):
        from wie.judges import ALLOWED, CaseView, judge_i0, judge_i1
        cdir = next((self.run / "cases").iterdir())
        with self.assertRaises(PermissionError):
            CaseView(cdir, ALLOWED["I1_same_frame"]).path("workspace/out")
        with self.assertRaises(PermissionError):
            CaseView(cdir, ALLOWED["I0_self_assessment"]).json("report.json")
        # And they still work with the workspace physically gone.
        for cdir in (self.run / "cases").iterdir():
            shutil.rmtree(cdir / "workspace")
            judge_i1(CaseView(cdir, ALLOWED["I1_same_frame"]))
            judge_i0(CaseView(cdir, ALLOWED["I0_self_assessment"]))

    def test_judges_do_not_read_sealed(self):
        shutil.move(str(self.run / "sealed"), str(self.tmp / "sealed_elsewhere"))
        for f in (self.run / "verdicts").glob("*.jsonl"):
            f.unlink()
        run_deterministic(self.run)  # must work with no key present
        score(self.run, key_path=self.tmp / "sealed_elsewhere" / "key.jsonl")


class TestImport(Base):
    def test_import_roundtrip_and_validation(self):
        good = self.tmp / "pasted.txt"
        lines = ["```json"] + [json.dumps({"case_id": c, "verdict": k["expected"], "reason": "x"})
                               for c, k in self.key.items()] + ["```"]
        good.write_text("\n".join(lines))
        import_verdicts(self.run, "I3_cross__report_plus_state__oracle", [good])
        r = score(self.run)["judges"]["I3_cross__report_plus_state__oracle"]
        self.assertEqual((r["E"], r["F"], r["coverage"]), (1.0, 0.0, 1.0))
        with self.assertRaises(FileExistsError):
            import_verdicts(self.run, "I3_cross__report_plus_state__oracle", [good])

    def test_import_rejects_unknown_ids_and_bad_verdicts(self):
        bad = self.tmp / "bad.txt"
        bad.write_text(json.dumps({"case_id": "Cnope", "verdict": "ACCEPT"}))
        with self.assertRaises(ValueError):
            import_verdicts(self.run, "x", [bad])
        cid = next(iter(self.key))
        bad.write_text(json.dumps({"case_id": cid, "verdict": "MAYBE"}))
        with self.assertRaises(ValueError):
            import_verdicts(self.run, "y", [bad])

    def test_missing_requires_flag(self):
        part = self.tmp / "part.txt"
        cid = next(iter(self.key))
        part.write_text(json.dumps({"case_id": cid, "verdict": "REJECT"}))
        with self.assertRaises(ValueError):
            import_verdicts(self.run, "z", [part])
        import_verdicts(self.run, "z", [part], allow_missing=True)
        rows = read_jsonl(self.run / "verdicts" / "z.jsonl")
        self.assertEqual(sum(r["verdict"] == "ABSTAIN" for r in rows), len(self.key) - 1)


class TestStats(unittest.TestCase):
    def test_wilson(self):
        lo, hi = wilson(0, 20)
        self.assertEqual(lo, 0.0)
        self.assertAlmostEqual(hi, 0.161, places=3)
        self.assertEqual(wilson(0, 0), (None, None))

    def test_mcnemar(self):
        self.assertEqual(mcnemar_exact(0, 0), 1.0)
        self.assertAlmostEqual(mcnemar_exact(0, 10), 2 / 1024)
        self.assertEqual(mcnemar_exact(5, 5), 1.0)


if __name__ == "__main__":
    unittest.main()
