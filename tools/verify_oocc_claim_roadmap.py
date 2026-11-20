"""Check the paper's structural consistency; does not judge its semantic claims.

Run: python -m tools.verify_oocc_claim_roadmap
Uses the published source inventory, not private source PDFs or native OOCC.
"""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def read_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_digest(path, expected):
    actual = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
    require(actual == expected, f"Digest mismatch: {path}")


def main():
    manifest = read_json("docs/paper/TESTING_OOCC.manifest.json")
    catalogue = read_json(manifest["claim_test_catalogue"])
    sources = {x["id"]: x for x in read_json(manifest["source_inventory"])}
    tests = catalogue["tests"]
    expected = [f"T{i:02}" for i in range(1, manifest["claim_test_families"] + 1)]
    require([x["id"] for x in tests] == expected, "Duplicate, missing or unordered test IDs")
    for item in tests:
        require(item["execution_status"] == "NOT_RUN_IN_THIS_ITERATION", item["id"])
        require(item["native_oocc_status"] == "NOT_RUN", item["id"])
        require(item["measured_native_oocc_result"] is None, item["id"])
        for ref in item["source_references"]:
            require(ref["source"] in sources, f"Unknown source: {ref}")
            require(bool(ref["pdf_pages"]), f"Empty source pages: {ref}")
            require(all(1 <= n <= sources[ref["source"]]["pdf_pages"]
                        for n in ref["pdf_pages"]), f"Invalid source pages: {ref}")
    for path in ("docs/paper/TESTING_OOCC.md", "docs/OOCC_CLAIMS_AND_REQUIRED_TESTS.md"):
        text = (ROOT / path).read_text(encoding="utf-8")
        require(re.findall(r"^#{2,3} (T\d+) —", text, re.M) == expected, path)
    for path, value in manifest["files"].items():
        check_digest(path, value["sha256"])
        require((ROOT / path).stat().st_size == value["bytes"], path)
    check_digest(manifest["renderer"], manifest["renderer_sha256"])
    for paper in read_json("docs/papers/archive/manifest.json")["papers"]:
        for file in paper["files"]:
            check_digest(file["path"], file["sha256"])
    first = Path(manifest["first_edition"]["path"])
    old = read_json(first / "TESTING_OOCC.manifest.json")
    for extension in ("md", "txt", "pdf"):
        check_digest(first / f"TESTING_OOCC.{extension}",
                     old["files"][f"docs/paper/TESTING_OOCC.{extension}"]["sha256"])
    print(f"PASS: {len(tests)} test families; source-page bounds, status labels, "
          "paper/archive hashes and preserved first edition. Semantic claims not adjudicated.")


if __name__ == "__main__":
    main()
