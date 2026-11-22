"""Freeze and verify a run.

freeze() hashes every case file plus ARTIFACT.md, CRITERIA.md and run.json,
and hashes the sealed key separately. The root hash is what you publish
(commit message, post, PhilArchive note) before any judging happens.
"""

from pathlib import Path

from .util import dump_json, load_json, sha256_file, sha256_text, tree_files

FROZEN_TOP = ("ARTIFACT.md", "CRITERIA.md", "run.json")


class TamperError(RuntimeError):
    pass


def _case_hashes(run_dir: Path) -> dict:
    out = {}
    for name in FROZEN_TOP:
        out[name] = sha256_file(run_dir / name)
    for rel in tree_files(run_dir / "cases"):
        out[f"cases/{rel}"] = sha256_file(run_dir / "cases" / rel)
    return out


def _root(files: dict, key_sha: str) -> str:
    lines = [f"{h}  {p}" for p, h in sorted(files.items())] + [f"{key_sha}  sealed/key.jsonl"]
    return sha256_text("\n".join(lines) + "\n")


def freeze(run_dir: Path, key_path: Path = None) -> dict:
    run_dir = Path(run_dir)
    if (run_dir / "manifest.json").exists():
        raise FileExistsError("run is already frozen; manifests are never rewritten")
    key_path = Path(key_path or run_dir / "sealed" / "key.jsonl")
    files = _case_hashes(run_dir)
    key_sha = sha256_file(key_path)
    manifest = {"files": files, "key_sha256": key_sha, "root_sha256": _root(files, key_sha)}
    dump_json(run_dir / "manifest.json", manifest)
    return manifest


def verify(run_dir: Path, key_path: Path = None, need_key: bool = True) -> dict:
    run_dir = Path(run_dir)
    mpath = run_dir / "manifest.json"
    if not mpath.exists():
        raise TamperError("run is not frozen (no manifest.json)")
    manifest = load_json(mpath)
    now = _case_hashes(run_dir)
    problems = []
    for p in sorted(set(manifest["files"]) | set(now)):
        if manifest["files"].get(p) != now.get(p):
            problems.append(p)
    if need_key:
        key_path = Path(key_path or run_dir / "sealed" / "key.jsonl")
        if not key_path.exists():
            problems.append("sealed/key.jsonl (missing)")
        elif sha256_file(key_path) != manifest["key_sha256"]:
            problems.append("sealed/key.jsonl")
    if _root(manifest["files"], manifest["key_sha256"]) != manifest["root_sha256"]:
        problems.append("manifest.json (root hash)")
    if problems:
        raise TamperError("frozen run changed: " + ", ".join(problems[:10]) +
                          (f" (+{len(problems) - 10} more)" if len(problems) > 10 else ""))
    return manifest
