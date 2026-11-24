from __future__ import annotations
import hashlib
import gzip
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIN = '257e54a51edac272eb6b2441457f38a40485ee4d'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def read_bytes(path):
    """Read retained bytes, accepting a losslessly compressed evidence artifact."""
    path=Path(path)
    if path.exists():
        data=path.read_bytes()
        return gzip.decompress(data) if path.suffix=='.gz' else data
    return gzip.decompress(Path(str(path)+'.gz').read_bytes())

def read_json(path):
    return json.loads(read_bytes(path))

def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+'\n')

def blob(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def verify_target(root):
    """Verify acquired GitHub blobs, not a fabricated local Git HEAD.

    This is a partial source snapshot, sufficient for the three native packages.
    The acquisition manifest is a retained trust root; it must itself be pinned
    before evaluation. Extra executable files in these packages are rejected.
    """
    root = Path(root).resolve()
    spec = json.loads((ROOT/'research/acquisition.json').read_text())['mplpb']
    if spec['revision'] != PIN:
        raise ValueError('Wrong source revision')
    required = {f['path']: f for f in spec['files']}
    for name, item in required.items():
        path = root/name
        if path.is_symlink() or not path.is_file() or blob(path.read_bytes()) != item['sha']:
            raise ValueError('Target bytes differ from pinned upstream Git blob: '+name)
    for package in ('mplpb_answers','mplpb_combined','mplpb_work'):
        actual = {str(p.relative_to(root)) for p in (root/package).rglob('*.py')}
        expected = {n for n in required if n.startswith(package+'/') and n.endswith('.py')}
        if actual != expected:
            raise ValueError('Unpinned executable files in '+package)
    return {'revision': PIN, 'verification': 'exact_upstream_git_blob_hashes',
            'files_verified': len(required), 'full_repository_checkout': False,
            'acquisition_sha256': sha((ROOT/'research/acquisition.json').read_bytes())}

def tree_snapshot(root):
    return {str(p.relative_to(root)): sha(p.read_bytes()) for p in sorted(Path(root).rglob('*'))
            if p.is_file() and '__pycache__' not in p.parts}
