"""Run independent scripted MPLPB sorter users on isolated mixed dumps."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys

from .common import ROOT, read_json, save, sha, tree_snapshot

REVISION = "bbf6690d69b32d16969cc10e5ce9d380427ead40"
FIXTURE = ROOT / "fixtures/sorter_mixed_users.json"
EXPLORATORY = "Exploratory · outside MPLPB-approved evidence."
STATUSES = {None: "not_requested", 0: "no_eligible_owner", 1: "one_eligible_owner"}

CREATE_LEDGER = """
import json
from pathlib import Path
import sys
from mplpb_combined.ledger import write, withdraw

root, source = map(Path, sys.argv[1:])
root.mkdir()
ids = {}
for original in json.load(sys.stdin):
    doc_id = original['doc_id']
    text = (source / (doc_id + '.txt')).read_bytes().decode('utf-8')
    result = write(root, doc_id=doc_id, title=original['title'], scope=original['title'],
                   origin='human', external=original.get('external', 'yes'), body=text)
    if original.get('withdrawn'):
        withdraw(root, result.id, note='Synthetic user withdrew approval')
    ids[doc_id] = result.path
print(json.dumps(ids))
"""


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def relative(path):
    value = PurePosixPath(path)
    if value.is_absolute() or ".." in value.parts or not value.parts or "\\" in path:
        raise ValueError(f"Unsafe fixture path: {path!r}")
    return value


def git(target, *args):
    return subprocess.check_output(["git", "-C", str(target), *args])


def call(target, receipts, name, *args, stdin=None):
    command = [sys.executable, "-E", "-s", *map(str, args)]
    result = subprocess.run(command, cwd=target, input=stdin, capture_output=True, timeout=120)
    (receipts / f"{name}.stdout").write_bytes(result.stdout)
    (receipts / f"{name}.stderr").write_bytes(result.stderr)
    save(receipts / f"{name}.json", {"argv": command, "exit_code": result.returncode})
    if result.returncode:
        raise RuntimeError(f"{name} exited {result.returncode}. See {receipts}.")
    return result.stdout


def materialize(target, user, directory):
    processed = directory / "dump" / "processed"
    approved = directory / "dump" / "approved"
    processed.mkdir(parents=True)
    approved.mkdir()
    files = {name: (text.encode("utf-8"), "synthetic")
             for name, text in user["processed"].items()}
    for name in user.get("repo_paths", []):
        files[f"repo/{relative(name)}"] = (git(target, "show", f"HEAD:{name}"), f"repository:{name}")
    input_types = {}
    for name, (data, input_type) in files.items():
        path = processed / relative(name)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        input_types[name] = input_type
    for original in user["originals"]:
        doc_id = original["doc_id"]
        require(relative(doc_id).name == doc_id, "Original identifiers must be simple file names")
        body = original["body"].encode("utf-8")
        if "repo_path" in original:
            name = str(relative(original["repo_path"]))
            require(body in git(target, "show", f"HEAD:{name}"), "Original excerpt drifted from the pinned repository")
        (approved / f"{doc_id}.txt").write_bytes(body)
    return processed, approved, input_types


def check_span(root, path, start, end, quote, digest):
    raw = (root / relative(path)).read_bytes()
    require(0 <= start < end <= len(raw), f"Invalid byte bounds in {path}")
    require("sha256:" + sha(raw) == digest, f"Wrong source hash for {path}")
    require(raw[start:end] == quote.encode("utf-8"), f"Wrong byte quote for {path}")


def check_candidate(item):
    require(item["status"] == "candidate for review" and item["evidence_status"] == EXPLORATORY,
            "Missing exploratory candidate label")
    require(all(item[field] is False for field in ("answer_supported", "approval_transferred", "content_truth_verified")),
            "A processed candidate claimed authority")


def check_budget(review):
    check_candidate(review)
    spans = {}
    for passage in review["processed_passages"]:
        check_candidate(passage)
        span = passage["span"]
        spans[("processed", span["path"], span["source_sha256"], span["byte_start"], span["byte_end"])] = span["text"]
    for candidate in review["candidates"]:
        original = candidate["original"]
        spans[("original", original["path"], original["hash"], original["body_start"], original["body_end"])] = original["quote"]
    budget = review["exploration_budget"]
    require(budget["strict_slots_consumed"] == 0
            and len(spans) == budget["unique_spans"] <= budget["max_passages"]
            and sum(map(len, spans.values())) == budget["characters"] <= budget["max_characters"],
            "Exploration miscounted exact spans or exceeded its budget")


def map_results(user, processed, approved, ledger, original_paths, input_types, graph, review):
    sources = {source["path"]: source for source in graph["sources"]}
    statements = defaultdict(list)
    details = {p["node_id"]: p for p in review["processed_passages"]}
    links = defaultdict(list)
    references = defaultdict(list)
    for reference in review["unresolved_references"]:
        check_candidate(reference)
        span = reference["reference_span"]
        check_span(processed, span["path"], span["byte_start"], span["byte_end"],
                   span["text"], span["source_sha256"])
        references[reference["processed"]["node_id"]].append({
            "target": reference["target_key"], "span": span,
            "eligible_document_identified": reference["eligible_document_identified"],
            "target_claim_status": reference["target_claim_status"],
        })
    for candidate in review["candidates"]:
        check_candidate(candidate)
        check_candidate(candidate["processed"])
        original = candidate["original"]
        require(original["approval_status"] == "eligible_original" and original["answer_supported"] is False,
                "A review link changed the status of the original")
        check_span(ledger, original["path"], original["byte_start"], original["byte_end"],
                   original["raw_excerpt"], original["native_original_sha256"])
        links[candidate["processed"]["node_id"]].append(
            {"id": candidate["id"], "kind": candidate["kind"], "original_id": original["source_id"],
             "original_path": original["path"], "byte_start": original["byte_start"],
             "byte_end": original["byte_end"], "reason": candidate["why"]})
    for node in graph["nodes"]:
        if node["kind"] != "statement":
            continue
        span = node["span"]
        check_span(processed, span["path"], span["byte_start"], span["byte_end"],
                   span["text"], span["source_sha256"])
        shown = details.get(node["id"])
        if shown:
            check_candidate(shown)
            require(shown["span"] == span, "Review changed the sorter span")
        statements[span["path"]].append({
            "node_id": node["id"], "occurrence_id": node["occurrence"], "span": span,
            "review_status": shown["original_match_status"] if shown else "not_displayed_for_this_query",
            "candidate_links": links.get(node["id"], []),
            "unresolved_references": references.get(node["id"], []),
        })
    return {
        "approved": [
            {"id": doc["doc_id"], "dump_path": f"dump/approved/{doc['doc_id']}.txt",
             "sha256": sha((approved / f"{doc['doc_id']}.txt").read_bytes()),
             "ledger_path": original_paths[doc["doc_id"]],
             "ledger_sha256": sha((ledger / original_paths[doc["doc_id"]]).read_bytes()),
             "withdrawn": doc.get("withdrawn", False), "external": doc.get("external", "yes"),
             "repository_source": doc.get("repo_path")}
            for doc in user["originals"]
        ],
        "processed": [
            {"path": path, "input_type": input_types[path],
             "sha256": sha((processed / path).read_bytes()),
             "sorter_status": "included" if path in sources else "excluded",
             "sorter_source": sources.get(path), "statements": statements.get(path, [])}
            for path in sorted(input_types)
        ],
    }


def evaluate_user(target, user, directory):
    receipts = directory / "commands"
    receipts.mkdir(parents=True)
    processed, approved, input_types = materialize(target, user, directory)
    ledger = directory / "ledger"
    input_bytes = tree_snapshot(directory / "dump")
    original_data = json.dumps(user["originals"], ensure_ascii=False).encode("utf-8")
    original_paths = json.loads(call(target, receipts, "create-ledger", "-c", CREATE_LEDGER,
                                     ledger, approved, stdin=original_data))
    call(target, receipts, "validate-ledger", "-m", "mplpb_combined", "validate", ledger)
    ledger_bytes = tree_snapshot(ledger)

    graphs = {}
    for mode in ("not-compared", "compare"):
        path = directory / f"{mode}.json"
        call(target, receipts, f"sort-{mode}", "-m", "mplpb_work.sorter", "sort", processed,
             "--mode", mode, "--output", path)
        call(target, receipts, f"verify-{mode}", "-m", "mplpb_work.sorter", "verify", path,
             "--sources", processed)
        graphs[mode] = read_json(path)
    observations, graph = graphs["not-compared"], graphs["compare"]
    require(observations["sources"] == graph["sources"] and observations["nodes"] == graph["nodes"],
            "Comparing changed source material or sorter nodes")
    observed_edges = observations["edges"]
    require(graph["edges"][:len(observed_edges)] == observed_edges, "Comparing rewrote observations")
    for item in graph["sources"] + graph["nodes"] + graph["edges"]:
        require(all(item["assessment"][field] is False for field in
                    ("answer_supported", "source_support_established", "historical_truth_independently_verified")),
                "Sorter graph claimed support or truth")
    expected = user["expected"]
    excluded = sorted(set(input_types) - {item["path"] for item in graph["sources"]})
    require(excluded == sorted(expected.get("excluded", [])), f"Unexpected source exclusions: {excluded}")

    workspace_args = ("-m", "mplpb_work.candidate_workspace")
    inputs = (directory / "compare.json", "--processed", processed, "--originals", ledger)
    selection = ["--profile", user.get("profile", "internal")]
    for key in ("question", "topic"):
        if key in user:
            selection.extend((f"--{key}", user[key]))
    decisions = {}
    for budget, extra in (("standard", ()), ("tiny", ("--exploration-passages", 1, "--exploration-chars", 20))):
        path = directory / f"{budget}-workspace.json"
        call(target, receipts, f"build-{budget}", *workspace_args, "build", *inputs,
             *selection, *extra, "--output", path)
        review = read_json(path)
        replay = json.loads(call(target, receipts, f"peruse-{budget}", *workspace_args, "peruse",
                                *inputs, "--workspace", path))
        require(replay == review, f"Review replay changed at {budget} budget")
        check_budget(review)
        decisions[budget] = review["mplpb_decision"]
    require(decisions["standard"] == decisions["tiny"], "Exploration budget changed the strict decision")

    review = read_json(directory / "standard-workspace.json")
    decision = decisions["standard"]
    owners = expected["owner_count"]
    require(decision["eligible_owner_count"] == owners and
            decision["status"] == STATUSES.get(owners, "multiple_eligible_owners"), "Unexpected ownership outcome")
    supported = (decision["strict_answer"] or {}).get("answer_supported", False)
    require(supported is expected["supported"], "Unexpected strict answer outcome")
    if supported:
        citations = [citation for claim in decision["strict_answer"]["claims"] for citation in claim["citations"]]
        require(bool(citations) and all(c["source_id"] == expected["owner_id"]
                    and c["path"] == original_paths[c["source_id"]] for c in citations),
                "Strict answer cited material outside the designated original")
    require(bool(review["processed_passages"]), "Processed material was not explorable")
    if "owner_id" in expected:
        require(decision["page"]["id"] == expected["owner_id"], "Unexpected eligible owner")
    if "competing_ids" in expected:
        require({s["id"] for s in decision["competing_sources"]} == set(expected["competing_ids"]),
                "A competing approved source disappeared")
    kinds = Counter(c["kind"] for c in review["candidates"])
    if "candidate_kinds" in expected:
        required = set(expected["candidate_kinds"])
        require(required <= kinds.keys() if required else not kinds, f"Unexpected candidate kinds: {dict(kinds)}")
    for kind, path in expected.get("candidate_paths", {}).items():
        require(any(c["kind"] == kind and c["processed"]["span"]["path"] == path
                    for c in review["candidates"]), f"Missing {kind} classification for {path}")
    if "blocked_originals" in expected:
        require(not (set(expected["blocked_originals"]) & {c["original"]["source_id"] for c in review["candidates"]}),
                "Ineligible original appeared in a candidate")
    if "unresolved_target" in expected:
        require(any(r["target_key"] == expected["unresolved_target"] and not r["eligible_document_identified"]
                    for r in review["unresolved_references"]), "Missing or ineligible reference did not stay unresolved")
    if "unmatched_paths" in expected:
        require(set(expected["unmatched_paths"]) <= {p["span"]["path"] for p in review["unmatched_passages"]},
                "Processed-only material disappeared")

    mapping = map_results(user, processed, approved, ledger, original_paths, input_types, graph, review)
    save(directory / "source-map.json", mapping)
    require(tree_snapshot(ledger) == ledger_bytes and tree_snapshot(directory / "dump") == input_bytes,
            "Review mutated originals or inputs")
    return {"id": user["id"], "task": user["task"], "status": "PASS", "owner_count": owners,
            "answer_supported": supported, "processed_files": len(input_types), "excluded_files": excluded,
            "statements": sum(len(item["statements"]) for item in mapping["processed"]),
            "processed_passages_shown": len(review["processed_passages"]), "candidate_kinds": dict(sorted(kinds.items())),
            "sorter_limits_or_exclusions": graph["limits_or_exclusions"], "ledger_unchanged": True,
            "strict_decision_stable_at_tiny_budget": True, "source_map": f"{user['id']}/source-map.json"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mplpb-root", type=Path, required=True)
    parser.add_argument("--revision", default=REVISION)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    target, output = args.mplpb_root.resolve(), args.out.resolve()
    if output.is_relative_to(target):
        parser.error("Output must be outside the MPLPB checkout")
    require(git(target, "rev-parse", "HEAD").decode().strip() == args.revision, "Wrong MPLPB revision")
    require(not git(target, "status", "--porcelain"), "MPLPB checkout must be clean")
    output.mkdir(parents=True, exist_ok=False)
    users = read_json(FIXTURE)["users"]
    require(len(users) == len({user["id"] for user in users}) == 5, "Expected five separate synthetic users")
    save(output / "freeze.json", {"revision": args.revision, "fixture_sha256": sha(FIXTURE.read_bytes()),
                                  "runner_sha256": sha(Path(__file__).read_bytes()), "model_calls": 0})
    results = []
    for user in users:
        directory = output / relative(user["id"])
        try:
            result = evaluate_user(target, user, directory)
        except (AssertionError, RuntimeError, subprocess.TimeoutExpired) as error:
            result = {"id": user["id"], "task": user["task"], "status": "FAIL", "reason": str(error)}
            save(directory / "failure.json", result)
        results.append(result)
        print(f"{user['id']}: {result['status']}", flush=True)
    require(not git(target, "status", "--porcelain"), "Native commands changed the target checkout")
    passed = sum(result["status"] == "PASS" for result in results)
    save(output / "summary.json", {"revision": args.revision, "status": "PASS" if passed == len(users) else "FAIL",
                                  "passed": passed, "users": results,
                                  "scope": "Five scripted synthetic users. Historical semantic accuracy unscored."})
    return int(passed != len(users))


if __name__ == "__main__":
    raise SystemExit(main())
