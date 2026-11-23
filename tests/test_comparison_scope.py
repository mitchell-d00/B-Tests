"""Keep the crawler comparison ledger aligned with recorded execution scope."""

import json
from pathlib import Path
import hashlib
import unittest


ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_bytes())


class TestComparisonScope(unittest.TestCase):
    def test_instruction_and_native_counts_remain_separate(self):
        scope = read("research/comparison-scope.json")
        comparisons = {row["id"]: row for row in scope["comparisons"]}
        instruction = comparisons["instruction_trials_30"]
        findings = read("evaluation/findings-index.json")
        self.assertEqual(instruction["sessions"], findings["target_sessions"])
        self.assertEqual(sum(c["sessions"] for c in instruction["conditions"]), instruction["sessions"])
        self.assertEqual([a["id"] for a in instruction["arms"]], ["cad_instruction", "conventional_instruction"])
        self.assertFalse(instruction["native_mplpb_arm"])

        native = comparisons["native_mplpb_before_after"]
        self.assertFalse(native["included_in_30_sessions"])
        observed = read(native["record"])["results"]
        for arm in native["arms"]:
            statuses = [event["status"] for event in observed if event["revision"] == arm["revision"]]
            self.assertEqual((statuses.count("PASS"), statuses.count("FAIL")), (arm["passed"], arm["failed"]))

    def test_attribution_and_unrun_claims_are_preserved(self):
        comparisons = read("research/comparison-scope.json")["comparisons"]
        for row in comparisons:
            with self.subTest(comparison=row["id"]):
                self.assertTrue((ROOT / row["record"]).is_file())
                if row["id"] in {"native_gelhaus_oocc", "m6"}:
                    self.assertEqual(row["status"], "NOT_RUN")
                    self.assertIsNone(row["performance_result"])
                elif row["id"] == "gelhaus_public_mplpb_package":
                    audit = read(row["record"])
                    self.assertEqual(row["wrapper_authorship"], "UNESTABLISHED_BY_PACKAGE")
                    self.assertFalse(audit["package_contains_m6_runtime"])
                    imported = {f"{entry['module']}.{name}"
                                for entry in audit["imports_from"] for name in entry["names"]}
                    self.assertEqual(set(row["upstream_modules"]), imported)


    def test_public_driver_replay_distinguishes_question_labels_from_engine_results(self):
        scope = read("research/comparison-scope.json")
        entry = next(row for row in scope["comparisons"] if row["id"] == "gelhaus_public_mplpb_package")
        verification = read(entry["fresh_verification"])
        earlier_audit = read(entry["record"])
        identity = verification["published_package"]
        self.assertEqual(identity["zip_sha256"], earlier_audit["package_sha256"])
        self.assertEqual(identity["script_sha256"], earlier_audit["reproduction_script_sha256"])
        self.assertFalse(verification["benchmark_inputs"]["driver_loads_csv_key"])
        replay = verification["unchanged_replay"]
        result_bytes = (ROOT / replay["retained_result"]).read_bytes()
        self.assertEqual(hashlib.sha256(result_bytes).hexdigest(), replay["source_result_sha256"])
        result = json.loads(result_bytes)
        self.assertEqual(replay["canonical_supported"], result["exact_supported"])
        self.assertEqual(replay["paraphrases_supported"], result["paraphrase_supported"])
        negative_cases = sum(row["cases"] for row in replay["negative_controls"].values())
        self.assertEqual(replay["total_engine_queries"],
                         verification["benchmark_inputs"]["positive_questions"] + negative_cases)
