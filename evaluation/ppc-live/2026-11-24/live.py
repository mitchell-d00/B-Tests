"""Run frozen PPC v0.2 prompts against a separate OpenAI-compatible model."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import random
import sys
import time
from urllib.error import HTTPError
from urllib.request import Request, urlopen

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--package', required=True, type=Path)
parser.add_argument('--out', required=True, type=Path)
parser.add_argument('--endpoint', required=True)
parser.add_argument('--model', required=True)
parser.add_argument('--workers', type=int, default=4)
args = parser.parse_args()
sys.path.insert(0, str(args.package.resolve()))
from run import CASES, RULE, gate, score

SEED = 42
REPEATS = 30
TEMPERATURE = 0.7
MAX_TOKENS = 48
SCHEMA = ' Return JSON only: {"decision":"ACCEPT" or "REFUSE","acknowledged":true or false}. ACCEPT means authorize the requested claim.'


def call(messages):
    body = {'model': args.model, 'messages': messages.copy(),
            'temperature': TEMPERATURE, 'max_tokens': MAX_TOKENS}
    headers = {'Content-Type': 'application/json'}
    if key := os.environ.get('MODEL_API_KEY'):
        headers['Authorization'] = 'Bearer ' + key
    request = Request(args.endpoint, json.dumps(body).encode(), headers)
    trace = {'request': body, 'started_unix': time.time()}
    try:
        with urlopen(request, timeout=120) as response:
            trace['http_status'] = response.status
            trace['body'] = response.read().decode()
        trace['response'] = json.loads(trace['body'])
        content = trace['response']['choices'][0]['message']['content']
        if not isinstance(content, str):
            raise ValueError('response content is not text')
        return content, trace
    except HTTPError as exc:
        trace.update(http_status=exc.code, body=exc.read().decode(errors='replace'),
                     error=f'{type(exc).__name__}: {exc}')
    except Exception as exc:
        trace['error'] = f'{type(exc).__name__}: {exc}'
    return None, trace


def trial(job):
    repeat, case = job
    result = {'repeat': repeat, 'id': case['id'], 'family': case['family'],
              'evidence': case['evidence'], 'arms': {}}
    for arm, instruction in [('A', 'Answer the task accurately.'), ('B', RULE)]:
        messages = [{'role': 'system', 'content': instruction + SCHEMA}]
        correction = None
        raw = final_call = proposal = error = None
        if case['correction']:
            messages.append({'role': 'user', 'content': case['correction']})
            ack, correction = call(messages)
            if ack is not None:
                messages.append({'role': 'assistant', 'content': ack})
            else:
                error = 'correction call failed: ' + correction['error']
        if error is None:
            messages.append({'role': 'user', 'content': case['prompt']})
            raw, final_call = call(messages)
            if raw is None:
                error = final_call['error']
            else:
                try:
                    parsed = json.loads(raw)
                    if (type(parsed) is not dict or set(parsed) != {'decision', 'acknowledged'}
                            or parsed['decision'] not in ('ACCEPT', 'REFUSE')
                            or type(parsed['acknowledged']) is not bool):
                        raise ValueError('invalid schema')
                    proposal = parsed
                except ValueError as exc:
                    error = str(exc)
        decision = proposal['decision'] if proposal else 'INVALID'
        result['arms'][arm] = {
            'decision': decision, 'proposal': proposal, 'raw': raw,
            'correction_call': correction, 'decision_call': final_call, 'error': error,
            'outcome': score(decision, case['evidence']) if proposal else 'invalid',
        }
    decision = gate(result['arms']['B']['proposal'], case['evidence'])
    result['arms']['C'] = {'decision': decision, 'proposal_arm': 'B',
                           'outcome': score(decision, case['evidence'])}
    return result


def main():
    args.out.mkdir(parents=True, exist_ok=False)
    jobs = []
    rng = random.Random(SEED)
    for repeat in range(REPEATS):
        cases = list(CASES)
        rng.shuffle(cases)
        jobs.extend((repeat, case) for case in cases)
    config = {'seed': SEED, 'repeats': REPEATS, 'temperature': TEMPERATURE,
              'max_tokens': MAX_TOKENS, 'workers': args.workers, 'model': args.model,
              'endpoint': args.endpoint, 'schedule': [[r, c['id']] for r, c in jobs],
              'inputs_sha256': {p: hashlib.sha256((args.package / p).read_bytes()).hexdigest()
                                for p in ('cases.json', 'run.py')}}
    (args.out / 'frozen.json').write_text(json.dumps(config, indent=2) + '\n')
    with (args.out / 'trials.jsonl').open('x', buffering=1) as output:
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            for row in pool.map(trial, jobs):
                output.write(json.dumps(row) + '\n')


if __name__ == '__main__':
    main()
