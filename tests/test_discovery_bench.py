import copy
import json
from pathlib import Path
import tempfile
import unittest
from research_lab.discovery_bench import prepare,evaluate,replay
from research_lab.common import read_json


class DiscoveryTests(unittest.TestCase):
    def test_published_observations_replay_including_literal_action_failure(self):
        result=replay(Path('evaluation/discovery-1'))
        self.assertEqual(result['records_verified'],4)
        self.assertEqual([r['status'] for r in result['results']],['PASS','PASS','FAIL','PASS'])
        self.assertTrue(all(r['current_primary_open_observed'] for r in result['results']))
        self.assertEqual(result['results'][2]['errors'],['wrong_action_requests'])

    def test_unknown_error_not_announced_and_sources_match_across_treatments(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'run';assign=prepare(root)
            packets=[json.loads((root/'packets'/a['packet_id']/'request.json').read_text()) for a in assign]
            self.assertEqual(packets[0]['task'],packets[1]['task'])
            self.assertEqual(packets[2]['task'],packets[3]['task'])
            for packet in packets:
                self.assertNotIn('contradiction',packet['task']['request'])
                self.assertNotIn('false_approved_map',json.dumps(packet))
                self.assertEqual(len(packet['task']['archive_index']),64)

    def test_approved_error_is_persistently_wrong_without_evidential_override(self):
        bundle=read_json('evaluation/discovery-1/records.json');r=bundle['records'][0]
        request=dict(r['request'],sources={s['id']:s['body'] for s in r['archive']})
        response=copy.deepcopy(r['response']);response.update(equipment_active=True,claim_status='supported',task_status='ready',action_requests=['release'])
        result=evaluate(request,bundle['keys'][r['packet_id']],response,set(r['opened_source_ids']))
        self.assertEqual(result['status'],'FAIL')
        self.assertIn('wrong_equipment_active',result['errors'])
        self.assertFalse(result['appropriate_local_action'])
        self.assertEqual(response['action_requests'],['release'])


if __name__=='__main__':unittest.main()
