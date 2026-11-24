"""Execute the pinned B-Tests probe against a pinned native MPLPB checkout."""
import argparse
import hashlib
import json
from pathlib import Path
import sqlite3
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
MPLPB = 'e3990bf98ac6fb2e3b991a2eb251347ca571e873'
B_TESTS = 'e646f82e4758e35e7a883eb492bcf756a8d29c83'
sys.path.insert(0, str(ROOT / 'native_runner'))
from research_lab.mplpb_seam_probe import CASES


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mplpb', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    source = args.mplpb.resolve()
    git = ['git', '-C', str(source)]
    if subprocess.check_output(git + ['rev-parse', 'HEAD'], text=True).strip() != MPLPB:
        parser.error('MPLPB checkout must match the frozen revision')
    if subprocess.check_output(git + ['status', '--porcelain'], text=True).strip():
        parser.error('MPLPB checkout must be clean')
    args.out.mkdir(parents=True)
    runner = ROOT / 'native_runner'
    manifest = {'b_tests_revision': B_TESTS, 'mplpb_revision': MPLPB, 'cases': CASES,
                'runner_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in (runner / 'research_lab').glob('*.py')}}
    (args.out / 'frozen.json').write_text(json.dumps(manifest, indent=2) + '\n')
    results = []
    for case, expected in CASES.items():
        out = (args.out / case).resolve()
        out.mkdir()
        command = [sys.executable, '-B', '-m', 'research_lab.mplpb_seam_probe',
                   'worker', '--root', str(source), '--out', str(out),
                   '--case', case, '--revision', MPLPB]
        process = subprocess.run(command, cwd=runner, capture_output=True)
        (out / 'stdout.txt').write_bytes(process.stdout)
        (out / 'stderr.txt').write_bytes(process.stderr)
        (out / 'process.json').write_text(json.dumps(
            {'argv': command, 'cwd': str(runner), 'exit': process.returncode}, indent=2) + '\n')
        if process.returncode:
            results.append({'case': case, 'status': 'NOT_RUN', 'exit': process.returncode})
            continue
        result = json.loads((out / 'result.json').read_text())
        databases = sorted(out.glob('work/**/*.sqlite*'))
        databases = [p for p in databases if p.is_file() and not p.name.endswith(('-shm', '-wal'))]
        if len(databases) != 1:
            results.append({'case': case, 'status': 'NOT_RUN', 'issue': 'SQLite evidence unavailable'})
            continue
        with sqlite3.connect(databases[0].as_uri() + '?mode=ro', uri=True) as db:
            count = db.execute('SELECT COUNT(*) FROM events').fetchone()[0]
        marker = out / 'effect.txt'
        verified = marker.is_file() == expected and count == result['event_count_after']
        results.append(dict(result, status='PASS' if verified and result['status'] == 'PASS' else 'FAIL',
                            marker_observed_on_disk=marker.is_file(), sqlite_event_count=count))
    (args.out / 'summary.json').write_text(json.dumps({'results': results}, indent=2) + '\n')
    return int(any(row['status'] != 'PASS' for row in results))


if __name__ == '__main__':
    raise SystemExit(main())
