import copy
import json
from pathlib import Path
import tempfile
import unittest

from research_lab.critical_bench import build, prepare, evaluate, submit, replay as replay_critical
from research_lab.agent_replay import replay


def control(task, oracle):
    """Scripted oracle response for HARNESS CONTROLS ONLY, never AI evidence."""
    return {'answers': [dict(id=q, value=e['value'], sources=e['sources']) for q,e in oracle['answers'].items()],
            'citations': [{'source_id': p['id'], 'quote': p['body']} for p in task['pages']],
            'action_requests': oracle['action_requests'], 'handoff': 'Retain failed attempts, current permissions, uncertainty and original records.'}


class CriticalBenchTests(unittest.TestCase):
    def test_reproducible_dimensions_and_unanimous_refusal_control(self):
        task, oracle = build()
        self.assertEqual((task, oracle), build())
        self.assertEqual(len(task['pages']), 64)
        self.assertEqual(len(task['questions']), 119)
        self.assertEqual(sum(len(p.get('planning_relation_appearances', [])) for p in task['pages']), 5120)
        self.assertEqual(oracle['action_requests'], ['P7'])
        good = control(task, oracle)
        self.assertEqual(evaluate(task, oracle, good)['status'], 'PASS')
        good['action_requests'] = []
        self.assertEqual(evaluate(task, oracle, good)['local_action_selection'], 'FAIL')

    def test_false_promotions_receipts_relations_and_duplicates_are_detected(self):
        task, oracle = build()
        # Eight distinct frozen question types, not eight scripted model runs.
        for offset in (0, 3, 4, 5, 6, 8, 9, 10):
            bad = control(task, oracle)
            row = bad['answers'][offset]
            row['value'] = not row['value'] if isinstance(row['value'], bool) else row['value']+1
            score = evaluate(task, oracle, bad)
            self.assertEqual(score['status'], 'FAIL')
            self.assertEqual(score['correct_values'], 118)

    def test_fabricated_quote_and_missing_answers_fail(self):
        task, oracle = build()
        bad = control(task, oracle)
        bad['citations'][0]['quote'] = 'invented source quotation'
        bad['answers'].pop()
        score = evaluate(task, oracle, bad)
        self.assertIn('fabricated_citation', score['errors'])
        self.assertEqual(score['correct_values'], 118)

    def test_packets_match_evidence_hide_key_and_commit_before_scoring(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)/'study'; entries = prepare(root)
            requests = [json.loads((Path(e['entry']).parent/'request.json').read_text()) for e in entries]
            self.assertEqual(requests[0]['task'], requests[1]['task'])
            for entry in entries:
                directory = Path(entry['entry']).parent
                chunks = [json.loads((directory/f'pages-{n}.json').read_text()) for n in range(1,5)]
                self.assertEqual(sum(map(len, chunks)), 64)
                self.assertNotIn('oracle', (directory/'instructions-and-questions.json').read_text())
            task, oracle = build(); bad = control(task, oracle); bad['action_requests'] = ['P0']
            response = Path(tmp)/'response.json'; response.write_text(json.dumps(bad))
            transcript = Path(tmp)/'transcript.txt'; transcript.write_text('HARNESS CONTROL, NOT A MODEL TRANSCRIPT')
            pid = entries[0]['packet_id']; score = submit(root,pid,response,transcript)
            self.assertEqual(json.loads((root/'packets'/pid/'local_effects.json').read_text()), ['P0'])
            self.assertEqual(score['local_action_selection'], 'FAIL')
            with self.assertRaises(ValueError): submit(root,pid,response,transcript)

    def test_retained_real_agent_records_replay(self):
        result = replay('evaluation/agent-pilot-1/records.json')
        self.assertEqual((result['records_verified'], result['handoff_transfers_verified']), (16,12))
        self.assertEqual(sum(not r['budget_met'] for r in result['rows']), 2)

    def test_retained_critical_benchmark_and_known_score_limitations_replay(self):
        result = replay_critical(Path('evaluation/critical-bench-1'))
        self.assertEqual(result['records_verified'], 2)
        self.assertEqual([r['correct_values'] for r in result['results']], [119,119])
        self.assertEqual([r['fully_supported_answers'] for r in result['results']], [108,109])
        self.assertIn('unknown_question', result['results'][0]['errors'])

    def test_malformed_citation_is_a_failure_not_an_evaluator_crash(self):
        task, oracle = build(); bad = control(task, oracle)
        bad['citations'][0]['source_id'] = ['invalid']
        self.assertIn('fabricated_citation', evaluate(task, oracle, bad)['errors'])


if __name__ == '__main__': unittest.main()
