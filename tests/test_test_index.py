"""Check discovery of new test material and retention of source status."""

import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from zipfile import ZipFile

from tools.build_test_index import catalog, markdown


class TestArchiveIndex(unittest.TestCase):
    def test_indexes_new_tests_and_evidence_without_treating_them_as_executions(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            (root / "tests").mkdir()
            (root / "evaluation/fresh").mkdir(parents=True)
            test = root / "tests/test_example.py"
            test.write_text("class Sample:\n    def test_added(self):\n        pass\n", encoding="utf-8")
            verdict = root / "evaluation/fresh/results.json"
            verdict.write_text(json.dumps({"cases": [{"id": "C1", "status": "NOT_RUN"}]}), encoding="utf-8")
            package = root / "evaluation/fresh/sample.zip"
            with ZipFile(package, "w") as archive:
                archive.writestr("pack/cases/C1/input.json", "{}")
            (root / "untracked.json").write_text("{}", encoding="utf-8")
            subprocess.run(["git", "add", "tests", "evaluation"], cwd=root, check=True)

            index = catalog(root)
            records = {row["path"]: row for row in index["files"]}
            self.assertEqual(index["counts"]["python_test_definitions"], 1)
            self.assertEqual(records["tests/test_example.py"]["test_definitions"], [
                {"name": "Sample.test_added", "line": 2},
            ])
            self.assertEqual(records["evaluation/fresh/results.json"]["case_and_status_records"], [
                {"pointer": "/cases/0", "id": "C1", "reported_status": {"status": "NOT_RUN"}},
            ])
            self.assertEqual(records["evaluation/fresh/sample.zip"]["members"], ["pack/cases/C1/input.json"])
            self.assertNotIn("untracked.json", records)
            self.assertIn("tests/test_example.py#L2", markdown(index))
            self.assertIn("evaluation/fresh/results.json", markdown(index))
