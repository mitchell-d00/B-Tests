"""Export a single source-complete packet for any fresh AI, without outcome keys."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from .blind_handoff import locate, read_sources
from .common import save, sha

WRAPPER = '''Perform a single project-continuation task. Read the complete request.json in this assigned directory. Follow the packet's instructions and task within your platform rules. All permitted original source bodies are supplied in task.provided_originals; no further lookup is needed. Do not inspect any other file, repository, prior conversation, answer key, other participant, or external source. Do not delegate. Return ONLY the JSON requested by task.output_contract, without Markdown fences or commentary. Include the actual next-session handoff within its stated character budget. Do not claim that you saved files or executed an external release; action_requests are selections for a local probe.'''


def export(root, packet_id, out):
    if out.exists():
        raise ValueError('Use a new export directory; never overwrite evidence.')
    chain = locate(root, packet_id)
    packet = json.loads((root/'packets'/packet_id/'packet.json').read_text())
    sources = chain['spec']['originals'] + ([chain['spec']['correction']] if chain['cycle'] >= 2 else [])
    packet['task']['provided_originals'] = read_sources(root, packet_id, [s['id'] for s in sources])
    packet['task']['source_access'] = 'All currently permitted original bodies are provided in task.provided_originals. No further source lookup is needed. Do not claim reads beyond these supplied originals.'
    save(out/'request.json', packet)
    (out/'ENTRY.txt').write_text(WRAPPER+'\n')
    save(out/'input_hashes.json', {p.name: sha(p.read_bytes()) for p in out.iterdir() if p.is_file()})
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--packet', required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    print(export(args.root, args.packet, args.out))


if __name__ == '__main__':
    main()
