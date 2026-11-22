"""Generate the human and machine-readable inventories of B-Tests."""

import argparse
import ast
from collections import Counter, defaultdict
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import tarfile
from urllib.parse import quote
import zipfile


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN = "docs/TEST_INDEX.md"
DATA = "research/test-index.json"
INVENTORY = "research/test-inventory.jsonl"
CASE_COLLECTIONS = {"assignments", "cases", "checks", "comparisons", "questions", "records", "results",
                    "rows", "tests", "trials"}
STATUS_FIELDS = ("status", "execution_status", "native_oocc_status", "run_status", "review_status", "passed")
FIND_ENTRYPOINTS = {"readme.md", "results.md", "report.md", "reproduction.md",
                    "summary.json", "results.json", "findings-index.json", "start.md"}
EXCLUDED = {MARKDOWN, DATA, INVENTORY}
PREPARED_CATALOGUES = {"research/oocc_claim_tests_v1.json"}


def repository_paths(root):
    raw = subprocess.check_output(
        ["git", "ls-files", "-z", "--cached"], cwd=root,
    )
    return sorted({p.decode("utf-8") for p in raw.split(b"\0") if p})


def collection(path):
    parts = PurePosixPath(path).parts
    if len(parts) == 1:
        return "."
    if parts[0] in ("evaluation", "comparative-tests") and len(parts) > 2:
        return "/".join(parts[:2])
    if parts[0] == "docs" and len(parts) > 2:
        return "/".join(parts[:2])
    if parts[0] == ".github":
        return ".github/workflows"
    return parts[0]


def python_definitions(path):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    definitions = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            methods = ((f"{node.name}.{method.name}", method.lineno) for method in node.body
                       if isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef)) and method.name.startswith("test"))
            definitions.extend(methods)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_"):
            definitions.append((node.name, node.lineno))
    main_guard = any(isinstance(node, ast.If) and '__name__' in ast.unparse(node.test)
                     and '__main__' in ast.unparse(node.test) for node in tree.body)
    return definitions, main_guard


def archive_members(path):
    if path.name.endswith(".zip"):
        with zipfile.ZipFile(path) as archive:
            return sorted(item.filename for item in archive.infolist() if not item.is_dir())
    with tarfile.open(path, mode="r:gz") as archive:
        return sorted(item.name for item in archive if item.isfile())


def pointer_part(value):
    return str(value).replace("~", "~0").replace("/", "~1")


def json_records(data):
    """Find source records using IDs, collection keys, and recorded status fields."""
    records = []

    def visit(node, pointer="", context=None, key_id=None):
        if isinstance(node, list):
            for index, row in enumerate(node):
                visit(row, f"{pointer}/{index}", context)
            return
        if not isinstance(node, dict):
            return
        statuses = {field: node[field] for field in STATUS_FIELDS
                    if isinstance(node.get(field), (bool, str))}
        id_fields = ("case_id", "test_id", "case", "id", "scenario")
        identifier = next((node[field] for field in id_fields
                           if isinstance(node.get(field), str)), key_id)
        if identifier is None and context in CASE_COLLECTIONS:
            identifier = next((node[field] for field in ("title", "name", "condition")
                               if isinstance(node.get(field), str)), None)
        identified_case = identifier is not None and (context or any(field in node for field in id_fields[:3]))
        if identified_case or (statuses and (not pointer or context in CASE_COLLECTIONS)):
            row = {"pointer": pointer}
            if identifier is not None:
                row["id"] = identifier
            for field in ("title", "name", "boundary", "revision"):
                if isinstance(node.get(field), str):
                    row[field] = node[field]
            if statuses:
                row["reported_status"] = statuses
            records.append(row)
        for field, value in node.items():
            next_pointer = f"{pointer}/{pointer_part(field)}"
            if field in CASE_COLLECTIONS and isinstance(value, dict):
                for name, member in value.items():
                    if isinstance(member, dict):
                        visit(member, f"{next_pointer}/{pointer_part(name)}", field, name)
                    elif isinstance(member, list):
                        visit(member, f"{next_pointer}/{pointer_part(name)}", field)
            elif isinstance(value, (list, dict)):
                visit(value, next_pointer, field if field in CASE_COLLECTIONS else None)

    visit(data)
    return records


def file_record(root, name):
    disk = root / name
    filename = disk.name
    group = collection(name)
    record = {"path": name, "collection": group, "role": "supporting_file"}
    if name in PREPARED_CATALOGUES:
        record["role"] = "proposed_test_catalogue"
    elif name.startswith(".github/workflows/"):
        record["role"] = "workflow"
    elif name.startswith("fixtures/"):
        record["role"] = "fixture"
    elif filename.endswith((".tar.gz", ".zip")):
        record["role"] = "archive"
        try:
            record["members"] = archive_members(disk)
        except (OSError, tarfile.TarError, zipfile.BadZipFile):
            record["metadata_status"] = "archive_unreadable"
    elif disk.suffix == ".md":
        record["role"] = "documentation"
        heading = re.search(r"^# (.+)$", disk.read_text(encoding="utf-8"), flags=re.MULTILINE)
        if heading:
            record["title"] = heading.group(1)
    elif name.startswith(("evaluation/", "comparative-tests/")):
        record["role"] = "retained_record"

    if disk.suffix == ".py":
        definitions, main_guard = python_definitions(disk)
        if filename.startswith("test_") or filename.endswith("_test.py"):
            record["role"] = "test_source"
            record["test_definitions"] = [{"name": test, "line": line} for test, line in definitions]
        elif main_guard:
            record["role"] = "runnable_script"
    if disk.suffix == ".sh" or name == "make_cases.py":
        record["role"] = "runnable_script"
    if disk.suffix == ".json":
        try:
            extracted = json_records(json.loads(disk.read_bytes()))
        except (UnicodeError, json.JSONDecodeError):
            record["metadata_status"] = "json_unparsed"
        else:
            if extracted:
                record["case_and_status_records"] = extracted
    return record


def catalog(root):
    files = []
    for name in repository_paths(root):
        if name in EXCLUDED:
            continue
        path = root / name
        if not path.is_file():
            continue
        files.append(file_record(root, name))
    by_collection = defaultdict(list)
    for record in files:
        by_collection[record["collection"]].append(record)
    collections = []
    for group, entries in sorted(by_collection.items()):
        links = sorted((r["path"] for r in entries if PurePosixPath(r["path"]).name.lower() in FIND_ENTRYPOINTS),
                       key=lambda path: (path.count("/"), path))
        collections.append({
            "path": group, "files": len(entries), "entry_points": links,
            "records_with_case_or_status": sum(bool(r.get("case_and_status_records")) for r in entries),
        })
    return {
        "schema_version": 1,
        "scope": {
            "important_distinction": "Inventory presence is not an execution or a passed result. Read the source records.",
            "coverage": "Git-indexed repository files. Archive member names are indexed one layer deep.",
            "record_semantics": "Raw status fields are transcribed. File and record counts may include repeat runs and references.",
        },
        "counts": {
            "files": len(files), "collections": len(collections),
            "test_source_files": sum("test_definitions" in r for r in files),
            "python_test_definitions": sum(len(r.get("test_definitions", [])) for r in files),
            "archives": sum(r["role"] == "archive" for r in files),
            "archive_member_files": sum(len(r.get("members", [])) for r in files),
        },
        "details": {"path": INVENTORY, "format": "jsonl", "record_scope": "one repository file per line"},
        "collections": collections,
        "test_sources": [r for r in files if r["role"] == "test_source"],
        "runners_and_workflows": [r["path"] for r in files if r["role"] in {"runnable_script", "workflow"}],
        "files": files,
    }


def link(path, name=None, line=None):
    label = (name or path).replace("|", r"\|").replace("[", r"\[").replace("]", r"\]")
    location = f"#L{line}" if line is not None else ""
    return f"[{label}](../{quote(path, safe='/')}{location})"


def markdown(index):
    counts = index["counts"]
    lines = [
        "# B-Tests archive and test index",
        "",
        "This index covers the repository's test code, experiment runners, fixtures, retained",
        "results, and proposed comparisons. Use the linked records to determine which cases ran,",
        "on which revision, and under which conditions.",
        "",
        "[AI entry point (JSON)](../research/test-index.json) · "
        "[Full file inventory (JSONL)](../research/test-inventory.jsonl) · "
        "[Generator](../tools/build_test_index.py) · "
        "[Update workflow](https://github.com/mitchell-d00/B-Tests/actions/workflows/test-index.yml)",
        "",
        f"Found **{counts['python_test_definitions']} Python test definitions** in "
        f"**{counts['test_source_files']} files**, **{counts['files']} repository files** and "
        f"**{counts['archives']} archives** with **{counts['archive_member_files']} listed member files**.",
        "Case records may include repeated trials, references, and unrun cases.",
        "",
        "## Automated test definitions",
        "",
        "The count comes from source definitions. Runtime discovery can differ for generated or parameterized tests.",
        "Run the main suite with `python -m unittest discover -s tests -q`. Run the Witness package",
        "suite from `evaluation/witness-section19/research-archive` with the same command.",
        "",
        "| Test source | Definitions |",
        "| --- | ---: |",
    ]
    for record in index["files"]:
        if "test_definitions" in record:
            lines.append(f"| {link(record['path'])} | {len(record['test_definitions'])} |")
    lines.extend(["", "<details>", "<summary>Browse individual Python tests</summary>", ""])
    for record in index["test_sources"]:
        lines.extend([f"**{link(record['path'])}**", ""])
        lines.extend(f"- {link(record['path'], test['name'], test['line'])}"
                     for test in record["test_definitions"])
        lines.append("")
    lines += ["</details>", "", "## Experiment and evidence collections", "",
              "The JSON entry point lists suites and collections. The JSONL inventory includes every scoped",
              "file, extracted case IDs and statuses, source line numbers, and archive member names.",
              "Read the linked evidence for results and limitations. For example, search only Witness files with",
              "`jq -c 'select(.collection == \"evaluation/witness-section19\")' research/test-inventory.jsonl`.",
              "",
              "| Collection | Files | Case or status files | Entry points |",
              "| --- | ---: | ---: | --- |"]
    for group in index["collections"]:
        paths = group["entry_points"]
        entries = " · ".join(link(p, p.removeprefix(group["path"] + "/")) for p in paths[:4])
        if len(paths) > 4:
            entries += f" · {len(paths) - 4} more in JSON"
        lines.append(f"| {link(group['path'])} | {group['files']} | {group['records_with_case_or_status']} | {entries} |")
    lines += ["", "## Runnable scripts and workflow entry points", ""]
    for record in index["files"]:
        if record["role"] in {"runnable_script", "workflow"}:
            lines.append(f"- {link(record['path'])}")
    lines += ["", "## Regenerate or verify", "", "```sh", "python -m tools.build_test_index",
              "python -m tools.build_test_index --check", "```", "",
              "Stage new files before regenerating locally. GitHub Actions refreshes the index after",
              "changes reach `main`. Generation is deterministic and does not execute the indexed tests.", ""]
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Exit nonzero if an index is missing or stale")
    args = parser.parse_args(argv)
    index = catalog(ROOT)
    document = markdown(index)
    files = index.pop("files")
    rendered = {
        MARKDOWN: document,
        DATA: json.dumps(index, indent=2, ensure_ascii=False) + "\n",
        INVENTORY: "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in files),
    }
    stale = []
    for name, content in rendered.items():
        path = ROOT / name
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(name)
        else:
            path.write_text(content, encoding="utf-8")
    if stale:
        parser.exit(1, f"Stale test index: {', '.join(stale)}. Run python -m tools.build_test_index.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
