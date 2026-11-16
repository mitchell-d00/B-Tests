"""Audit retained agent outputs. Replay is scoring, never new AI inference."""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
from .blind_handoff import evaluate
from .common import sha,read_json


def replay(path):
    bundle = read_json(path)
    rows = []
    chains = {}
    for record in bundle['records']:
        chain = record['chain']
        packet = record['request']
        response = record['response']
        assert sha(json.dumps(chain['spec'], sort_keys=True).encode()) == record['frozen_spec_sha256']
        assert packet['instructions'] == bundle['instructions'][chain['arm']]
        assert sha(packet['instructions'].encode()) == bundle['instruction_hashes'][chain['arm']]
        assert packet['task']['provided_originals'] == chain['spec']['originals'] + ([chain['spec']['correction']] if chain['cycle'] >= 2 else [])
        assert record['committed_state'] == response['state']
        assert record['local_effects'] == response['action_requests']
        score = evaluate(chain, response)
        for key in ('status', 'errors', 'budget_met', 'handoff_characters', 'handoff_source_id_retention'):
            assert score[key] == record['strict_score'][key], (record['packet_id'], key)
        assert all(not e.startswith(('wrong_fact:', 'fabricated_citation', 'missing_citation:')) for e in score['errors'])
        chains.setdefault(chain['id'], []).append(record)
        rows.append({'packet_id': record['packet_id'], 'arm': chain['arm'],
                     'case_family': chain['spec']['case_family'], 'cycle': chain['cycle'],
                     'strict_status': score['status'], 'budget_met': score['budget_met'],
                     'handoff_characters': score['handoff_characters'], 'errors': score['errors']})
    transfers = 0
    for records in chains.values():
        records.sort(key=lambda r: r['chain']['cycle'])
        assert [r['chain']['cycle'] for r in records] == list(range(4))
        for previous, current in zip(records, records[1:]):
            assert current['request']['task']['inherited_handoff'] == previous['response']['handoff']
            transfers += 1
    return {'schema': 'agent-pilot-replay-1', 'new_model_requests': 0,
            'records_verified': len(rows), 'chains_verified': len(chains),
            'handoff_transfers_verified': transfers, 'rows': rows,
            'warning': 'Strict scoring replay; semantic annotations are unblinded human/assistant judgments, not independent replication.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', type=Path, default=Path('evaluation/agent-pilot-1/records.json'))
    args = parser.parse_args()
    print(json.dumps(replay(args.bundle), indent=2))


if __name__ == '__main__':
    main()
