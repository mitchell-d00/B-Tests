import unittest
from tools.score_scaling import score

PIN='a'*64

def trial():
    rows=[]
    for n in (10,100,1000):
        for arm in ('OOCC','baseline'):
            rows.append({'arm':arm,'edge_count':n,'source_snapshot_sha256':PIN,
                        'tasks':10,'verified_tasks':8 if arm=='OOCC' else 9,
                        'judged_relations':n,'false_proven_links':n//10 if arm=='OOCC' else 0,
                        'refuted_links':2,'refuted_links_active_after':1 if arm=='OOCC' else 0,
                        'operator_corrections':3,'tool_calls':12,'tokens':500,
                        'human_minutes':20.,'cpu_seconds':3.,'elapsed_seconds':40.,'total_usd':0.5})
    return {'preregistered_before_outcomes':True,'equal_original_source_access':True,
            'independent_blind_labels':True,'protocol_sha256':PIN,'rows':rows}

class TestScalingScorer(unittest.TestCase):
    def test_negative_results_are_retained(self):
        result=score(trial())
        self.assertEqual(len(result['comparison']),3)
        self.assertTrue(all(x['delta_verified_task_rate']<0 for x in result['comparison']))
        self.assertTrue(all(x['delta_false_proven_relation_rate']>0 for x in result['comparison']))
        self.assertFalse(result['independence_certified_by_this_script'])
    def test_requires_preoutcome_registration(self):
        d=trial();d['preregistered_before_outcomes']=False
        with self.assertRaises(ValueError):score(d)
    def test_requires_equal_access(self):
        d=trial();d['equal_original_source_access']=False
        with self.assertRaises(ValueError):score(d)
    def test_requires_blinded_reviews(self):
        d=trial();d['independent_blind_labels']=False
        with self.assertRaises(ValueError):score(d)
    def test_rejects_incomplete_scales(self):
        d=trial();d['rows'].pop()
        with self.assertRaises(ValueError):score(d)
    def test_rejects_mismatched_source_corpus(self):
        d=trial();d['rows'][-1]['source_snapshot_sha256']='b'*64
        with self.assertRaises(ValueError):score(d)
    def test_rejects_bool_counts(self):
        d=trial();d['rows'][0]['tasks']=True
        with self.assertRaises(ValueError):score(d)
    def test_rejects_duplicate_arm(self):
        d=trial();d['rows'].append(d['rows'][0].copy())
        with self.assertRaises(ValueError):score(d)
    def test_rejects_false_links_exceeding_judged(self):
        d=trial();d['rows'][0]['false_proven_links']=11
        with self.assertRaises(ValueError):score(d)
    def test_rejects_refuted_links_beyond_total(self):
        d=trial();d['rows'][0]['refuted_links_active_after']=3
        with self.assertRaises(ValueError):score(d)

if __name__=='__main__':unittest.main()
