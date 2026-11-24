"""Export fixed-size blinded correction-review packets and a separate join key."""
import argparse
from collections import defaultdict
import gzip
from hashlib import sha256
import json
from pathlib import Path

SALT = 'ppc-v02-correction-review-2026-11-24'
LABELS = ['explicit_rule_acknowledgment', 'generic_acknowledgment', 'absent_or_other',
          'contradicts_rule', 'unreviewable']


def digest(value):
    return sha256(f'{SALT}|{value}'.encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('traces', type=Path)
    parser.add_argument('out', type=Path)
    args = parser.parse_args()
    open_traces = gzip.open if args.traces.suffix == '.gz' else open
    arms_by_case = defaultdict(list)
    with open_traces(args.traces, 'rt', encoding='utf-8') as traces:
        for line in traces:
            row = json.loads(line)
            for arm in 'AB':
                run = row['arms'][arm]
                if correction := run['correction_call']:
                    key = digest(f"{row['id']}|{arm}|{row['repeat']}")
                    arms_by_case[(arm, row['id'])].append((key, row, arm, run, correction))
    args.out.mkdir(parents=True)
    items = sorted(item for group in arms_by_case.values() for item in sorted(group)[:3])
    packet, join_key = [], []
    for key, row, arm, run, correction in items:
        response = correction.get('response')
        packet.append({
            'review_id': key[:12],
            'correction': correction['request']['messages'][-1]['content'],
            'response': response['choices'][0]['message']['content'] if response else None,
            'rubric_options': LABELS,
        })
        join_key.append({
            'review_id': key[:12], 'case': row['id'], 'repeat': row['repeat'], 'arm': arm,
            'evidence': row['evidence'], 'decision': run['decision'], 'outcome': run['outcome'],
        })
    for filename, values in [('packet.json', packet), ('join-key.json', join_key)]:
        (args.out / filename).write_text(json.dumps(values, indent=2) + '\n')


if __name__ == '__main__':
    main()
