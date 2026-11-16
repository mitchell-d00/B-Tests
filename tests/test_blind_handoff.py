import copy
import json
from pathlib import Path
import tempfile
import unittest
from research_lab.blind_handoff import prepare,locate,read_sources,evaluate,accept,fault_controls,export_packet

class BlindHandoffTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)/'experiment';self.entries=prepare(self.root,1)

    def test_target_packet_excludes_oracle_other_arm_and_hypothesis(self):
        for row in self.entries:
            p=self.root/'packets'/row['packet_id']/'packet.json';text=p.read_text();c=locate(self.root,row['packet_id'])
            for secret in ('expected_before','expected_after','case_family','armored worldview'):self.assertNotIn(secret,text)
            self.assertNotIn(c['spec']['correction']['body'],text)

    def test_matched_arms_share_source_bytes(self):
        by={}
        for item in self.entries:
            c=locate(self.root,item['packet_id']);by.setdefault(c['spec']['case_family'],[]).append(c['spec'])
        for pair in by.values():self.assertEqual(pair[0],pair[1])

    def test_future_source_is_unavailable_before_its_stage(self):
        item=self.entries[0];c=locate(self.root,item['packet_id'])
        r=read_sources(self.root,item['packet_id'],[c['spec']['correction']['id']])
        self.assertEqual(r[0]['status'],'UNAVAILABLE')

    def test_fault_injections_detect_smoothing_and_transfer_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            rows=fault_controls(Path(tmp)/'controls')
            self.assertEqual(len(rows),126)
            self.assertTrue(all(r['detected'] and r['evidence_level']=='harness_fault_injection_only' for r in rows))

    def test_fabricated_read_cannot_pass(self):
        c=locate(self.root,self.entries[0]['packet_id']);expected=c['spec']['expected_before']
        r=evaluate(c,{'state':expected,'source_reads_claimed':['made-up'],'citations':[],
          'handoff':'state','action_requests':[]})
        self.assertIn('false_read_claim',r['errors'])

    def test_export_contains_current_evidence_but_no_private_key(self):
        packet=self.entries[0]['packet_id'];out=Path(self.tmp.name)/'export'
        export_packet(self.root,packet,out)
        self.assertEqual({p.name for p in out.iterdir()},{'ENTRY.md','packet.json','originals.json','input_hashes.json'})
        combined=''.join(p.read_text() for p in out.iterdir())
        self.assertNotIn('expected_before',combined)
        self.assertNotIn(locate(self.root,packet)['spec']['correction']['body'],combined)

if __name__=='__main__':unittest.main()
