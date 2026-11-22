"""Audit real subprocess effects separately from the AI experiment."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys


WRITER = Path(__file__).resolve().with_name("effects.py")
CONTROLS = (
    ("allowed_commit", True, "none", 0, b"discontinued\n"),
    ("blocked_write", False, "none", 77, None),
    ("staging_only", True, "ack_only", 0, None),
    ("io_error", True, "io_error", 74, None),
)


def save(path, data):
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def check(out):
    out.mkdir(parents=True, exist_ok=False)
    save(out / "frozen.json", {
        "scope": "Engineering controls. No AI model or evaluator treatment.",
        "driver_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "writer_sha256": hashlib.sha256(WRITER.read_bytes()).hexdigest(),
        "controls": [{"id": name, "allowed": allowed, "fault": fault, "expected_exit": exit_code,
                      "expected_marker": marker.decode() if marker else None}
                     for name, allowed, fault, exit_code, marker in CONTROLS],
    })
    rows = []
    for name, allowed, fault, exit_code, marker in CONTROLS:
        root = out / name
        root.mkdir()
        save(root / "policy.json", {"write_allowed": allowed})
        command = [sys.executable, "-I", str(WRITER), "write", str(root),
                   "--value", "discontinued", "--fault", fault]
        process = subprocess.run(command, capture_output=True, check=False, timeout=15)
        (root / "stdout.txt").write_bytes(process.stdout)
        (root / "stderr.txt").write_bytes(process.stderr)
        file = root / "status.txt"
        actual = file.read_bytes() if file.is_file() else None
        row = {"id": name, "command": command, "exit_code": process.returncode,
               "observed_marker": actual.decode() if actual else None,
               "marker_sha256": hashlib.sha256(actual).hexdigest() if actual else None,
               "pass": process.returncode == exit_code and actual == marker}
        save(root / "result.json", row)
        rows.append(row)
    save(out / "summary.json", rows)
    return all(row["pass"] for row in rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    sys.exit(0 if check(parser.parse_args().out.resolve()) else 1)
