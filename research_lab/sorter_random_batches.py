"""Prepare and run 5 sets of 5 scripted MPLPB users on 100 randomized topics."""

from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path
import random
import re
import secrets
import sys

from .common import ROOT, read_json, save, sha, tree_snapshot
from .sorter_mixed_users import (
    CREATE_LEDGER, REVISION, call, check_budget, check_candidate, git,
    map_results, materialize, require,
)

CATALOG = ROOT / "fixtures/sorter_web_topics.json"
ACTORS = ("Mara", "Ivo", "Nora", "Tess")
ROLES = ("records clerk", "correspondence reviewer", "field researcher", "release editor", "maintainer")
SCENARIOS = ("supported", "competing", "processed-only", "insufficient")
# Keep topics within the reader's finite attribution grammar. The fixtures
# measure routing and candidate behavior rather than punctuation coverage.
UNSUPPORTED_WORDS = frozenset(
    "and or if unless when because not never may might could would should alleged reported claimed "
    "allegedly apparently perhaps probably possibly reportedly supposedly intended planned requested "
    "permitted that this it him her them those these dated pending except only provided wrote appointed "
    "sent received".split()
)
TABLES = {
    "experience": [(25, "beginner"), (50, "occasional"), (75, "regular"), (100, "advanced")],
    "layout": [(25, "mail export"), (50, "working notes"),
               (75, "hand-off transcript"), (100, "mixed archive")],
    "profile": [(40, "internal"), (70, "lab"), (100, "external")],
    "exploration_passages": [(25, 12), (50, 16), (75, 20), (100, 24)],
    "copy_format": [(25, "txt"), (50, "md"), (75, "text"), (100, "markdown")],
}


class D100:
    def __init__(self, seed):
        self.random = random.Random(seed)
        self.rolls = []

    def roll(self, label):
        face = self.random.randint(1, 100)
        self.rolls.append({"chart": label, "roll": face})
        return face

    def table(self, label):
        face = self.roll(label)
        return next(value for maximum, value in TABLES[label] if face <= maximum)

    def index(self, size, label):
        # Compose as many base-100 digits as needed. Reject the remainder so
        # every entry has the same chance even when a pool does not divide 100.
        if size == 1:
            return 0
        width = 1
        while 100**width < size:
            width += 1
        limit = (100**width // size) * size
        while True:
            value = 0
            for _ in range(width):
                value = 100 * value + self.roll(label) - 1
            if value < limit:
                return value % size

    def sample(self, values, count, label):
        pool = list(values)
        return [pool.pop(self.index(len(pool), label)) for _ in range(count)]

    def shuffle(self, values, label):
        return self.sample(values, len(values), label)


def select_topics(catalog, rng):
    sections = defaultdict(list)
    for entry in catalog["entries"]:
        title = entry["topic"]
        if re.fullmatch(r"[A-Za-z][A-Za-z -]{2,65}", title) and not (
                set(re.findall(r"[a-z]+", title.lower())) & UNSUPPORTED_WORDS):
            sections[entry["section"]].append(entry)
    names = sorted(sections)
    require(len(names) == 11, "The catalog must contain 11 topic sections")
    extra = rng.sample(names, 1, "extra_topic_section")[0]
    topics = []
    for name in names:
        entries = sorted(sections[name], key=lambda entry: entry["url"])
        topics.extend(rng.sample(entries, 9 + (name == extra), f"topic:{name}"))
    require(len({entry["url"] for entry in topics}) == 100, "Expected 100 distinct topics")
    return rng.shuffle(topics, "topic_assignment")


def user_dump(topics, role, rng):
    queue = rng.shuffle(SCENARIOS, "scenario_order")
    characteristics = {label: rng.table(label)
                       for label in ("experience", "layout", "profile", "exploration_passages")}
    originals, processed, cases, expected = [], {}, [], {}

    def approve(title, body):
        doc_id = f"DOC-{len(originals) + 1}"
        originals.append({"doc_id": doc_id, "title": title, "body": body})
        return doc_id

    for position, (scenario, topic) in enumerate(zip(queue, topics, strict=True), 1):
        label = f"topic-{position:02d}"
        first, second = rng.sample(ACTORS, 2, "record_actor")
        title = f"{topic['topic']} memorandum"
        statement = f"{first} wrote the {title}."
        question = f"Who wrote the {title}?"
        candidates = []
        if scenario == "supported":
            owners = [approve(title, statement)]
            candidates = ["exact_match", "conflicting_wording"]
            processed[f"{label}-mail.txt"] = f"{first} did not write the {title}."
        elif scenario == "competing":
            owners = [approve(title, statement), approve(title, f"{second} wrote the {title}.")]
            candidates = ["exact_match"]
        elif scenario == "insufficient":
            owners = [approve(title, f"The {title} remains unassigned.")]
        else:
            owners = []
            question = f"What about {topic['topic']}?"
            statement = f"{first} studied {topic['topic']}."
        processed[f"{label}-copy.{rng.table('copy_format')}"] = statement
        processed[f"{label}-web-pointer.md"] = (
            f"# Public topic pointer\n\n{topic['topic']}\n\n{topic['url']}\n\n"
            "This link supplies a topic for a fictional record exercise.\n"
        )
        cases.append({"id": label, "question": question, "web_topic": topic})
        expected[label] = {"scenario": scenario, "owner_ids": owners, "supported": scenario == "supported",
                           "candidate_kinds": candidates, "copy_text": statement}
    layout = characteristics["layout"]
    processed["collection-notes.md"] = {
        "mail export": "# Mail export\n\nMessage-ID: ARCHIVE-77\n\nDelivery traces are incomplete.",
        "working notes": "# Working notes\n\nDraft inventory. Items require review before release.",
        "hand-off transcript": "# Handoff\n\n> Review begins after the next maintenance window.",
        "mixed archive": "# Archive notes\n\nStatus: pending\n\nThese entries came from several exports.",
    }[layout]
    # Include a format the current sorter does not directly ingest.
    processed["index.csv"] = "type,state\nworking-index,draft\n"
    return {"role": role, "characteristics": characteristics,
            "originals": originals, "processed": processed, "cases": cases}, expected


def prepare(out, seed, revision=REVISION):
    catalog = read_json(CATALOG)
    rng = D100(seed)
    topics = select_topics(catalog, rng)
    out.mkdir(parents=True, exist_ok=False)
    packets = out / "packets"
    key = {}
    for set_number in range(1, 6):
        roles = rng.shuffle(ROLES, f"role_assignment:set-{set_number:02d}")
        for user_number, role in enumerate(roles, 1):
            user_id = f"set-{set_number:02d}/user-{user_number:02d}"
            start = ((set_number - 1) * 5 + user_number - 1) * 4
            spec, expected = user_dump(topics[start:start + 4], role, rng)
            packet = packets / user_id
            materialize(ROOT, spec, packet)
            save(packet / "tasks.json", {"role": role, "characteristics": spec["characteristics"],
                                        "cases": spec["cases"], "originals": [{k: doc[k] for k in ("doc_id", "title")}
                                                      for doc in spec["originals"]]})
            key[user_id] = expected
    save(out / "operator-key.json", key)
    save(out / "d100-rolls.json", {"tables": TABLES, "rolls": rng.rolls})
    freeze = {
        "seed": seed, "revision": revision, "python": sys.version,
        "catalog_revision": catalog["catalog_revision_url"],
        "catalog_sha256": sha(CATALOG.read_bytes()), "catalog_entries": len(catalog["entries"]),
        "generator_sha256": sha(Path(__file__).read_bytes()),
        "native_harness_sha256": sha((ROOT / "research_lab/sorter_mixed_users.py").read_bytes()),
        "topic_count": 100, "set_count": 5,
        "users_per_set": 5, "topics_per_user": 4, "packet_hashes": tree_snapshot(packets),
        "key_sha256": sha((out / "operator-key.json").read_bytes()),
        "d100_sha256": sha((out / "d100-rolls.json").read_bytes()),
        "scope": "Public topic metadata with fictional records and scripted users. No historical accuracy claim.",
    }
    save(out / "freeze.json", freeze)
    return freeze


def run_user(target, packet, expected, output):
    receipts = output / "commands"
    receipts.mkdir(parents=True)
    tasks = read_json(packet / "tasks.json")
    processed, approved = packet / "dump/processed", packet / "dump/approved"
    ledger = output / "ledger"
    originals = json.dumps(tasks["originals"]).encode()
    original_paths = json.loads(call(target, receipts, "ledger", "-c", CREATE_LEDGER,
                                     ledger, approved, stdin=originals))
    call(target, receipts, "validate", "-m", "mplpb_combined", "validate", ledger)
    before = tree_snapshot(ledger)
    graphs = []
    for mode in ("not-compared", "compare"):
        path = output / f"{mode}.json"
        call(target, receipts, f"sort-{mode}", "-m", "mplpb_work.sorter", "sort", processed,
             "--mode", mode, "--output", path)
        call(target, receipts, f"verify-{mode}", "-m", "mplpb_work.sorter", "verify", path,
             "--sources", processed)
        graphs.append(read_json(path))
    raw, graph = graphs
    require(raw["sources"] == graph["sources"] and raw["nodes"] == graph["nodes"]
            and graph["edges"][:len(raw["edges"])] == raw["edges"], "Sorter changed raw observations")
    input_types = {p.name: "synthetic_or_web_topic_pointer" for p in processed.iterdir()}
    require(set(input_types) - {r["path"] for r in graph["sources"]} == {"index.csv"},
            "Unexpected input inventory")
    spec = {"originals": tasks["originals"]}
    rows = []
    for case in tasks["cases"]:
        case_id = case["id"]
        key = expected[case_id]
        workspace = output / f"{case_id}-workspace.json"
        base = ("-m", "mplpb_work.candidate_workspace")
        inputs = (output / "compare.json", "--processed", processed, "--originals", ledger)
        config = tasks["characteristics"]
        call(target, receipts, f"build-{case_id}", *base, "build", *inputs, "--profile", config["profile"],
             "--exploration-passages", config["exploration_passages"],
             "--question", case["question"], "--output", workspace)
        review = read_json(workspace)
        replay = json.loads(call(target, receipts, f"replay-{case_id}", *base, "peruse", *inputs,
                                 "--workspace", workspace))
        require(replay == review, "Candidate workspace did not replay")
        check_budget(review)
        decision = review["mplpb_decision"]
        supported = (decision["strict_answer"] or {}).get("answer_supported", False)
        owner_ids = {item["id"] for item in decision["competing_sources"]}
        if decision["page"]:
            owner_ids.add(decision["page"]["id"])
        require(decision["eligible_owner_count"] == len(key["owner_ids"])
                and owner_ids == set(key["owner_ids"]) and supported is key["supported"],
                f"{case_id} did not preserve the declared owners and strict support")
        candidates = {c["kind"] for c in review["candidates"]
                      if c["original"]["source_id"] in owner_ids}
        require(set(key["candidate_kinds"]) <= candidates, f"{case_id} is missing expected candidate kinds")
        require(any(p["span"]["text"] == key["copy_text"] for p in review["processed_passages"]),
                f"{case_id} did not retain the copy for review")
        for item in review["processed_passages"]:
            check_candidate(item)
        mapping = map_results(spec, processed, approved, ledger, original_paths, input_types, graph, review)
        save(output / f"{case_id}-source-map.json", mapping)
        rows.append({"id": case_id, "web_topic": case["web_topic"], "scenario": key["scenario"],
                     "owners": sorted(owner_ids), "strict_answer_supported": supported,
                     "candidate_count": len(review["candidates"]), "status": "PASS"})
    require(tree_snapshot(ledger) == before, "Review changed the native originals")
    return rows


def run(out, target):
    freeze = read_json(out / "freeze.json")
    revision = freeze["revision"]
    require(freeze["generator_sha256"] == sha(Path(__file__).read_bytes())
            and freeze["native_harness_sha256"] == sha((ROOT / "research_lab/sorter_mixed_users.py").read_bytes()),
            "Test runner changed after preparation")
    packets = out / "packets"
    key_path = out / "operator-key.json"
    require(tree_snapshot(packets) == freeze["packet_hashes"]
            and sha(key_path.read_bytes()) == freeze["key_sha256"]
            and sha((out / "d100-rolls.json").read_bytes()) == freeze["d100_sha256"],
            "Prepared batch changed")
    require(git(target, "rev-parse", "HEAD").decode().strip() == revision
            and not git(target, "status", "--porcelain"), "Expected a clean pinned checkout")
    output = out / "run"
    output.mkdir()
    key = read_json(key_path)
    results = []
    for user, expected in key.items():
        try:
            cases = run_user(target, packets / user, expected, output / user)
            result = {"user": user, "status": "PASS", "cases": cases}
        except (AssertionError, RuntimeError) as error:
            result = {"user": user, "status": "FAIL", "reason": str(error)}
        results.append(result)
        print(user, result["status"], result.get("reason", ""), flush=True)
    require(tree_snapshot(packets) == freeze["packet_hashes"]
            and not git(target, "status", "--porcelain"), "Run changed the packets or target")
    passed = sum(result["status"] == "PASS" for result in results)
    save(output / "summary.json", {"revision": revision, "seed": freeze["seed"],
                                   "passed_users": passed, "users": results})
    return int(passed != len(key))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    make = commands.add_parser("prepare")
    make.add_argument("--out", type=Path, required=True)
    make.add_argument("--seed", type=int)
    make.add_argument("--revision", default=REVISION)
    execute = commands.add_parser("run")
    execute.add_argument("--out", type=Path, required=True)
    execute.add_argument("--mplpb-root", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "prepare":
        if not re.fullmatch(r"[a-f0-9]{40}", args.revision):
            parser.error("Use a full Git commit SHA to freeze the MPLPB revision")
        seed = args.seed if args.seed is not None else secrets.randbits(64)
        result = prepare(args.out.resolve(), seed, args.revision)
        print(f"Prepared 100 topics for 25 scripted users. Seed: {result['seed']}")
        return 0
    target, output = args.mplpb_root.resolve(), args.out.resolve()
    if output.is_relative_to(target):
        parser.error("Batch output must be outside the MPLPB checkout")
    return run(output, target)


if __name__ == "__main__":
    raise SystemExit(main())
