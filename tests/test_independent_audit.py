import json
import tempfile
import unittest
from pathlib import Path
from research_lab.common import sha
from research_lab.live import score_handoff,request,rules
from research_lab.freeze import compression,graphs
from side_by_side.run import load_manifest,validate_model_response

class IndependentAuditControls(unittest.TestCase):
    def test_refusal_label_does_not_certify_false_answer(self):
        c=next(c for c in load_manifest()['cases'] if c['id']=='CAD16')
        status,detail=validate_model_response(c,{'decision':'REFUSE','answer':'B definitely copied A','evidence_ids':['A-2020']})
        self.assertEqual(status,'INCONCLUSIVE')
        self.assertEqual(detail['semantic_review'],'pending_independent_review')

    def test_handoff_missing_failure_is_detected(self):
        f=compression();value={'facts':{k:v for k,v in f['oracle'].items() if k!='invented_source_forbidden'},
              'citations':[{'source_id':s['id'],'quote':s['body']} for s in f['sources'] if s['id']!='APPROVED-MAP']}
        self.assertTrue(score_handoff(json.dumps(value),f,f['sources'])['contract_met'])
        del value['facts']['failed_approach']
        self.assertIn('lost_or_changed:failed_approach',score_handoff(json.dumps(value),f,f['sources'])['errors'])

    def test_no_semantic_pass_from_matching_fields(self):
        f=compression();value={'facts':{k:v for k,v in f['oracle'].items() if k!='invented_source_forbidden'},
           'citations':[{'source_id':s['id'],'quote':s['body']} for s in f['sources'] if s['id']!='APPROVED-MAP']}
        self.assertEqual(score_handoff(json.dumps(value),f,f['sources'])['status'],'INCONCLUSIVE')

    def test_invented_citation_fails(self):
        f=compression()
        self.assertEqual(score_handoff(json.dumps({'facts':{},'citations':[{'source_id':'PROOF-9','quote':'proven'}]}),f,f['sources'])['status'],'FAIL')

    def test_uncertainty_after_information_loss_is_not_hallucination(self):
        f=compression()
        r=score_handoff(json.dumps({'facts':{'test_passed':'unknown'},'citations':[]}),f,f['sources'])
        self.assertTrue(r['safe_abstention_observed'])
        self.assertEqual(r['wrong_assertions'],[])

    def test_confident_wrong_conclusion_surviving_compression_is_identified(self):
        f=compression()
        r=score_handoff(json.dumps({'facts':{'test_passed':True},'citations':[]}),f,f['sources'])
        self.assertIn('test_passed',r['wrong_assertions'])

    def test_graph_scale_is_actual_input_not_a_thousand_word_claim(self):
        for n in (10,100,1000,10000):
            g=graphs(n);self.assertEqual(len(g['questions']),n);self.assertEqual(len(g['projects']),10)
            self.assertEqual({q['type'] for q in g['questions']},{'legitimate','duplicate_root','contradiction','similarity','rejected'})

    def test_requests_have_no_hidden_oracle_or_prior_provider_session(self):
        a=request('rules','evidence','model',0);b=request('rules','evidence','model',0)
        self.assertEqual(a,b);self.assertEqual(set(a),{'model','messages','temperature','seed','max_tokens'})
        self.assertNotIn('oracle',json.dumps(a))

    def test_verbatim_treatment_has_identifiable_published_boundaries(self):
        self.assertIn('does not guarantee factual correctness',rules('CAD_VERBATIM'))
        self.assertIn('BASELINE_DISPUTED',rules('CAD_VERBATIM'))

if __name__=='__main__':unittest.main()
