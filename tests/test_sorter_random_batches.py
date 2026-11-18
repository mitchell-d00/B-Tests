import tempfile
import unittest
from pathlib import Path

from research_lab.common import read_json
from research_lab.sorter_random_batches import prepare


class SorterRandomBatchTests(unittest.TestCase):
    def test_seed_recreates_the_batch_and_key(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            first = prepare(root / "first", 27)
            second = prepare(root / "repeat", 27)
            other = prepare(root / "other", 28)
            self.assertEqual(first, second)
            self.assertNotEqual(first["packet_hashes"], other["packet_hashes"])

    def test_five_sets_and_four_distinct_cases_per_user(self):
        with tempfile.TemporaryDirectory() as temp:
            batch = Path(temp) / "batch"
            prepare(batch, 37)
            packets = batch / "packets"
            topics = []
            for group in sorted(packets.iterdir()):
                users = [read_json(path) for path in sorted(group.glob("*/tasks.json"))]
                self.assertEqual(len(users), 5)
                self.assertEqual(len({user["role"] for user in users}), 5)
                for user in users:
                    self.assertEqual(len(user["cases"]), 4)
                    self.assertTrue(all("scenario" not in case for case in user["cases"]))
                    topics.extend(case["web_topic"]["url"] for case in user["cases"])
            self.assertEqual(len(topics), 100)
            self.assertEqual(len(set(topics)), 100)
            self.assertFalse(list(packets.rglob("operator-key.json")))
            replay = read_json(batch / "d100-rolls.json")
            self.assertTrue(all(1 <= row["roll"] <= 100 for row in replay["rolls"]))


if __name__ == "__main__":
    unittest.main()
