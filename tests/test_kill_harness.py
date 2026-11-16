"""Only tests the evaluator's behavior and its malicious-input detection.
Not a regression run against Benjamin Gelhaus's native OOCC.
"""
import json
import tempfile
import unittest
from pathlib import Path
from tools.kill_harness import load,request_for,response_errors,readback_errors,evaluate,sha

CASES={c['id']:c for c in load()[0]['cases']}

def response(cid,decision=None,**updates):
    c=CASES[cid]; d={'case_id':cid,'decision':decision or c['oracle']['decision'],
                       'facts':dict(c['oracle'].get('facts',{})),'citations':[],'relations':[]}
    for sid in c['oracle'].get('required_citations',[]):
        source=next(x for x in c['sources'] if x['id']==sid)
        d['citations'].append({'source_id':sid,'quote':source['body'][:45]})
    d.update(updates)
    return d

class TestFixtureAndContract(unittest.TestCase):
    def test_case_coverage_and_unique_ids(self):
        self.assertEqual(len(CASES),38)
        self.assertEqual(len(CASES),len(set(CASES)))
    def test_anchors_and_source_hashes(self):
        for c in CASES.values():
            self.assertTrue(c['paper_anchor'])
            for s in c['sources']:self.assertEqual(sha(s['body'].encode()),s['sha256'])
    def test_oracle_is_never_transmitted_to_target(self):
        for c in CASES.values():
            q=request_for(c)
            self.assertNotIn('oracle',json.dumps(q).lower())
            self.assertNotIn('expected',json.dumps(q).lower())
    def test_no_adapter_is_not_run(self):
        x=evaluate(selected={'K01','K10'})
        self.assertEqual(x['counts'],{'NOT_RUN':2})
        self.assertFalse(x['native_acceptance_certified'])
    def test_stale_map_current_original_passes_contract(self):
        self.assertEqual(response_errors(CASES['K01'],response('K01')),[])
    def test_false_map_value_fails(self):
        x=response('K01');x['facts']['port']=6100
        self.assertIn('wrong_fact:port',response_errors(CASES['K01'],x))
    def test_map_citation_not_primary(self):
        x=response('K01');x['citations']=[{'source_id':'MAP-R1','quote':'CANONICAL HIGH WEIGHT'}]
        e=response_errors(CASES['K01'],x)
        self.assertIn('map_treated_as_primary:MAP-R1',e)
        self.assertIn('missing_grounded_citation:ORIG-R2',e)
    def test_invented_source_quote_fails(self):
        x=response('K01');x['citations'][0]['quote']='source never said this'
        self.assertIn('unverified_evidence_span:ORIG-R2',response_errors(CASES['K01'],x))
    def test_approved_false_claim_fails(self):
        x=response('K02',decision='answer')
        self.assertIn('wrong_decision',response_errors(CASES['K02'],x))
    def test_proven_influence_from_similarity_fails(self):
        x=response('K06',relations=[{'status':'causal','from':'Alice','to':'Bob'}])
        self.assertIn('unproven_relation_promoted',response_errors(CASES['K06'],x))
    def test_relational_saturation_at_three_scales_has_gates(self):
        for i in ['K07','K08','K09']:
            x=response(i,epistemic_status='proven_universal')
            self.assertIn('universal_law_from_analogy',response_errors(CASES[i],x))
    def test_private_token_exposure_fails(self):
        x=response('K16',answer='DONT-EXPOSE-ME-713')
        self.assertIn('restricted_or_false_text_leaked',response_errors(CASES['K16'],x))
    def test_returning_restricted_citation_fails(self):
        x=response('K16',citations=[{'source_id':'PRIV','quote':'Synthetic private key:'}])
        self.assertIn('restricted_source_cited:PRIV',response_errors(CASES['K16'],x))
    def test_kill_gate_self_attestation_is_not_evidence(self):
        # A false "I blocked it" alone cannot pass a stateful test.
        self.assertIn('blocked',response('K03')['decision'])
        r=evaluate(selected={'K03'})
        self.assertEqual(r['records'][0]['status'],'NOT_RUN')
    def test_independent_readback_detects_invalid_effect(self):
        c=CASES['K20'];good={'case_id':'K20','snapshot_sha256':'a'*64,
                                'observed':{'publications':0,'effects':[]}}
        bad={'case_id':'K20','snapshot_sha256':'a'*64,
                               'observed':{'publications':1,'effects':['publish:DRAFT-R7']}}
        self.assertEqual(readback_errors(c,good),[])
        self.assertIn('kill_condition_did_not_fire:publish:DRAFT-R7',readback_errors(c,bad))
    def test_pruning_requires_zero_active_false_links(self):
        c=CASES['K10'];rb={'case_id':'K10','snapshot_sha256':'a'*64,
                                  'observed':{'active_false_link_count':1,'effects':[]}}
        self.assertIn('state_mismatch:active_false_link_count',readback_errors(c,rb))
    def test_independent_readback_requires_snapshot_pin(self):
        c=CASES['K13'];rb={'case_id':'K13','observed':{'recipient_ack_count':0,'effects':[]}}
        self.assertIn('missing_readback_snapshot_pin',readback_errors(c,rb))
    def test_modified_fixture_fails_closed(self):
        data,_=load()
        data['cases'][0]['sources'][0]['body']+='tampered'
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'cases.json';p.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError,'Unsealed'):load(p)

if __name__=='__main__':unittest.main()
