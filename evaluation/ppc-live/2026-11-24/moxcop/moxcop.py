"""Mox Cult of Personality (MoxCOP): frozen, separately traced inference trials."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
import math
import os
from pathlib import Path
import random
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

SCHEMA = 'moxcop-trial-plan-v1'


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def read_json(path):
    return json.loads(path.read_bytes())


def write_json(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)
        stream.write('\n')


def make_plan(spec):
    if set(spec) != {'model', 'repeats', 'seed', 'temperature', 'max_tokens', 'trials'}:
        raise ValueError('Expected only model, repeats, seed, temperature, max_tokens and trials')
    if not isinstance(spec['model'], str) or not spec['model'].strip():
        raise ValueError('A model name is required')
    for field in ('repeats', 'max_tokens', 'seed'):
        if type(spec[field]) is not int or (field != 'seed' and spec[field] < 1):
            raise ValueError(f'Invalid {field}')
    temperature = spec['temperature']
    if type(temperature) not in (int, float) or not math.isfinite(temperature) or temperature < 0:
        raise ValueError('Temperature must be finite and nonnegative')
    cases = spec['trials']
    if not isinstance(cases, list) or not cases:
        raise ValueError('At least one trial definition is required')
    seen = set()
    for case in cases:
        if type(case) is not dict or set(case) != {'id', 'system', 'turns'}:
            raise ValueError('Each trial must contain only id, system and turns')
        if not all(isinstance(case[key], str) and case[key].strip() for key in ('id', 'system')):
            raise ValueError('Each trial needs a text id and system prompt')
        if case['id'] in seen:
            raise ValueError(f"Duplicate trial ID: {case['id']}")
        seen.add(case['id'])
        if (not isinstance(case['turns'], list) or not case['turns']
                or not all(isinstance(turn, str) and turn.strip() for turn in case['turns'])):
            raise ValueError('Each trial needs a nonempty list of user turns')
    rng = random.Random(spec['seed'])
    schedule = []
    for repeat in range(spec['repeats']):
        ordered = [case['id'] for case in cases]
        rng.shuffle(ordered)
        schedule.extend({'repeat': repeat, 'id': case_id} for case_id in ordered)
    return {'schema': SCHEMA, 'spec': spec, 'schedule': schedule}


def load_plan(path):
    plan = read_json(path)
    if plan != make_plan(plan['spec']):
        raise ValueError('Frozen schedule does not match its specification')
    return plan


def request_body(spec, messages):
    return {key: spec[key] for key in ('model', 'temperature', 'max_tokens')} | {
        'messages': messages.copy()
    }


def unpack(trace):
    if trace.get('http_status') != 200:
        raise ValueError('Expected HTTP 200')
    raw = json.loads(trace['body'])
    receipt = raw['id']
    model = raw['model']
    content = raw['choices'][0]['message']['content']
    if not isinstance(receipt, str) or not receipt.strip():
        raise ValueError('Provider response ID missing')
    if not isinstance(model, str) or not model.strip() or not isinstance(content, str):
        raise ValueError('Missing returned model or message text')
    return receipt, model, content


def call(endpoint, key, body):
    trace = {'request': body, 'started_unix_ns': time.time_ns()}
    headers = {'Content-Type': 'application/json'}
    if key:
        headers['Authorization'] = 'Bearer ' + key
    request = Request(endpoint, json.dumps(body).encode(), headers)
    try:
        with urlopen(request, timeout=120) as response:
            trace['http_status'] = response.status
            trace['body'] = response.read().decode()
        _, _, content = unpack(trace)
    except HTTPError as exc:
        trace.update(http_status=exc.code, body=exc.read().decode(errors='replace'),
                     error=f'{type(exc).__name__}: {exc}')
        content = None
    except (URLError, OSError, ValueError, KeyError, IndexError, TypeError) as exc:
        trace['error'] = f'{type(exc).__name__}: {exc}'
        content = None
    trace['finished_unix_ns'] = time.time_ns()
    return trace, content


def run_one(endpoint, key, spec, case, position):
    messages = [{'role': 'system', 'content': case['system']}]
    traced = []
    for turn in case['turns']:
        messages.append({'role': 'user', 'content': turn})
        trace, reply = call(endpoint, key, request_body(spec, messages))
        traced.append(trace)
        if reply is None:
            break
        messages.append({'role': 'assistant', 'content': reply})
    return {**position, 'calls': traced}


def run(plan_path, output, endpoint, workers):
    plan = load_plan(plan_path)
    parsed = urlsplit(endpoint)
    if (parsed.scheme not in ('http', 'https') or not parsed.hostname
            or parsed.username is not None or parsed.password is not None or parsed.query or parsed.fragment):
        raise ValueError('Specify an HTTP(S) endpoint without credentials, query or fragment')
    if workers < 1:
        raise ValueError('Workers must be positive')
    spec = plan['spec']
    cases = {case['id']: case for case in spec['trials']}
    output.mkdir(parents=True)
    frozen = output / 'plan.json'
    frozen.write_bytes(plan_path.read_bytes())
    write_json(output / 'run.json', {
        'endpoint': endpoint,
        'workers': workers,
        'plan_sha256': digest(frozen),
        'tool_sha256': digest(Path(__file__)),
        'started_unix_ns': time.time_ns(),
    })
    key = os.environ.get('MODEL_API_KEY')

    def actor(position):
        return run_one(endpoint, key, spec, cases[position['id']], position)

    with (output / 'traces.jsonl').open('x', encoding='utf-8', buffering=1) as stream:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            for result in pool.map(actor, plan['schedule']):
                stream.write(json.dumps(result, ensure_ascii=False) + '\n')
    return verify(output)


def verify(output):
    plan_path = output / 'plan.json'
    plan = load_plan(plan_path)
    manifest = read_json(output / 'run.json')
    if digest(plan_path) != manifest['plan_sha256']:
        raise ValueError('Plan digest does not match run record')
    spec = plan['spec']
    cases = {case['id']: case for case in spec['trials']}
    trace_path = output / 'traces.jsonl'
    ids = set()
    model_counts = Counter()
    complete = incomplete = 0
    with trace_path.open(encoding='utf-8') as stream:
        for index, position in enumerate(plan['schedule']):
            line = stream.readline()
            if not line:
                incomplete += len(plan['schedule']) - index
                break
            result = json.loads(line)
            if {key: result[key] for key in position} != position:
                raise ValueError('Trace ID or ordering differs from frozen plan')
            case = cases[position['id']]
            messages = [{'role': 'system', 'content': case['system']}]
            calls = result['calls']
            if not 1 <= len(calls) <= len(case['turns']):
                raise ValueError('Trace has an invalid number of calls')
            replies = 0
            for call_index, trace in enumerate(calls):
                messages.append({'role': 'user', 'content': case['turns'][call_index]})
                if trace['request'] != request_body(spec, messages):
                    raise ValueError('Request differs from the expected isolated history')
                if trace['finished_unix_ns'] < trace['started_unix_ns']:
                    raise ValueError('Call times are reversed')
                if 'error' in trace:
                    if call_index != len(calls) - 1:
                        raise ValueError('A call followed a failed turn')
                    break
                receipt, model, reply = unpack(trace)
                if receipt in ids:
                    raise ValueError(f'Duplicate provider response ID: {receipt}')
                ids.add(receipt)
                model_counts[model] += 1
                messages.append({'role': 'assistant', 'content': reply})
                replies += 1
            if replies == len(case['turns']):
                complete += 1
            else:
                incomplete += 1
        if stream.readline():
            raise ValueError('Trace has more trials than the frozen plan')
    return {
        'planned_trials': len(plan['schedule']),
        'complete_trials': complete,
        'incomplete_trials': incomplete,
        'unique_provider_responses': len(ids),
        'returned_models': dict(model_counts),
        'plan_sha256': digest(plan_path),
        'traces_sha256': digest(trace_path),
        'scope': 'Separate request histories and unique provider receipts in the retained trace.',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    freeze = commands.add_parser('freeze')
    freeze.add_argument('spec', type=Path)
    freeze.add_argument('plan', type=Path)
    execute = commands.add_parser('run')
    execute.add_argument('plan', type=Path)
    execute.add_argument('output', type=Path)
    execute.add_argument('--endpoint', required=True)
    execute.add_argument('--workers', type=int, default=1)
    audit = commands.add_parser('verify')
    audit.add_argument('output', type=Path)
    args = parser.parse_args()
    if args.command == 'freeze':
        write_json(args.plan, make_plan(read_json(args.spec)))
        return 0
    if args.command == 'run':
        result = run(args.plan, args.output, args.endpoint, args.workers)
        write_json(args.output / 'verification.json', result)
    else:
        result = verify(args.output)
    print(json.dumps(result, indent=2))
    return 1 if result['incomplete_trials'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
