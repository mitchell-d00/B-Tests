import unittest
from run import gate, score, CASES
class Contract(unittest.TestCase):
    def test_all_cases(self):
        for c in CASES:
            for decision in ('ACCEPT','REFUSE'):
                for ack in (True,False):
                    with self.subTest(case=c['id'],decision=decision,ack=ack):
                        self.assertEqual(gate({'decision':decision,'acknowledged':ack},c['evidence']), 'ACCEPT' if c['evidence'] and decision=='ACCEPT' else 'REFUSE')
    def test_malformed(self):
        for p in (None,[],{}, {'decision':'ACCEPT','acknowledged':1},{'decision':'ACCEPT','acknowledged':True,'override':True}):
            self.assertEqual(gate(p,True),'REFUSE')
    def test_no_false_refusal_claim(self):
        self.assertEqual(score(gate({'decision':'REFUSE','acknowledged':True},True),True),'false_refusal')
    def test_untrusted_truth(self):
        self.assertEqual(gate({'decision':'ACCEPT','acknowledged':True},'true'),'REFUSE')
    def test_fixture_recurrence(self):
        c=next(c for c in CASES if c['id']=='recurrence-negative')
        self.assertEqual(score(c['fixture']['B'],False),'false_accept')
        self.assertEqual(gate({'decision':c['fixture']['B'],'acknowledged':True},False),'REFUSE')
if __name__=='__main__': unittest.main()
