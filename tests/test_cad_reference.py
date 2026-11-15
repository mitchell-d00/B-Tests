"""Adversarial source-governance regression tests for OUR independent OOCC/CAD model.

Not Benjamin Gelhaus's private/native OOCC implementation, nor a model accuracy test.
Uses synthetic exact structured source statements so source entailment is decidable.
"""
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from oocc_lab.engine import CADLab, BadEvidence, CADError, Conflict, Denied, IntegrityFault


class CADFixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'cad.sqlite'
        self.cad = CADLab(self.path)
        self.addCleanup(self.cad.close)

    def source(self, id_, triples, **kw):
        return self.cad.add_source(id_, 'observatory', '\n'.join(triples), **kw)

    def claim(self, id_, source, subject, field, value, **kw):
        self.cad.propose(id_, source, subject, field, value, **kw)
        self.cad.promote(id_)


class TestMapIsNotAuthority(CADFixture):
    def test_stale_canonical_map_does_not_override_new_source(self):
        self.source('A1', ['aster | port | 6100'])
        self.claim('C1', 'A1', 'aster', 'port', '6100')
        self.cad.add_map('MAP', 'observatory', 'CANONICAL FACT: aster port 6100', weight=10)
        self.source('A2', ['aster | port | 6200'], supersedes='A1')
        self.claim('C2', 'A2', 'aster', 'port', '6200')
        self.assertEqual(self.cad.query('observatory','aster','port')['answer'], '6200')
        self.assertEqual(self.cad.source_status(self.cad.snapshot(), 'A1'),'historical')

    def test_map_only_never_becomes_cited_fact(self):
        self.cad.add_map('MAP', 'observatory', 'the universe runs on CAD; proven by every domain')
        a=self.cad.query('observatory','universe','law')
        self.assertEqual(a['decision'],'ABSENT')
        self.assertEqual(a['evidence'],[])

    def test_maximum_map_weight_is_not_more_evidence(self):
        self.cad.add_map('MAP','observatory','aster | port | 9999',weight=10)
        self.source('S',['aster | port | 6200'],weight=0)
        self.claim('C','S','aster','port','6200')
        self.assertEqual(self.cad.query('observatory','aster','port')['answer'],'6200')

    def test_draft_not_current_authority(self):
        self.source('D',['aster | port | 1111'],status='draft')
        with self.assertRaises(BadEvidence):
            self.cad.propose('C','D','aster','port','1111')

    def test_blocked_source_cannot_support_claim(self):
        self.source('B',['aster | port | 1111'],status='blocked')
        with self.assertRaises(BadEvidence):
            self.cad.propose('C','B','aster','port','1111')

    def test_orientation_carries_warning_and_current_status(self):
        self.source('A1',['aster | port | 6100'])
        self.source('A2',['aster | port | 6200'],supersedes='A1')
        o=self.cad.orientation('observatory')
        statuses={x['id']:x['authority'] for x in o['continuity']}
        self.assertEqual(statuses,{'A1':'historical','A2':'current'})
        self.assertIn('not itself factual evidence',o['warning'])

    def test_authorized_wrong_source_is_not_certified_truth(self):
        self.source('S',['planet | moons | 777'])
        self.claim('C','S','planet','moons','777')
        a=self.cad.query('observatory','planet','moons')
        self.assertEqual(a['decision'],'SUPPORTED_SOURCE_STATEMENT')
        self.assertNotIn('TRUE',a['decision'])
        self.assertEqual(a['evidence'][0]['quote'],'planet | moons | 777')

    def test_no_claim_from_title_or_partial_literal_overlap(self):
        self.source('S',['aster | port | 6200'])
        with self.assertRaises(BadEvidence):
            self.cad.propose('C','S','aster','port','6100')


class TestSourceConflictAndCorrection(CADFixture):
    def test_two_intact_conflicting_sources_force_conflict(self):
        self.source('S1',['aster | count | 3'])
        self.source('S2',['aster | count | 4'])
        self.claim('C1','S1','aster','count','3')
        self.claim('C2','S2','aster','count','4')
        self.assertEqual(self.cad.query('observatory','aster','count')['decision'],'CONFLICT')

    def test_unsupported_question_does_not_guess(self):
        self.source('S',['aster | count | 3'])
        self.assertEqual(self.cad.query('observatory','aster','color')['decision'],'ABSENT')

    def test_proposed_without_promotion_is_not_fact(self):
        self.source('S',['aster | count | 3'])
        self.cad.propose('P','S','aster','count','3')
        self.assertEqual(self.cad.query('observatory','aster','count')['decision'],'ABSENT')

    def test_partial_correction_changes_one_field_only(self):
        self.source('S1',['aster | venue | north','aster | date | monday'])
        self.claim('VENUE1','S1','aster','venue','north')
        self.claim('DATE1','S1','aster','date','monday')
        self.source('S2',['aster | venue | south','aster | date | monday'],supersedes='S1')
        self.claim('VENUE2','S2','aster','venue','south',corrects='VENUE1')
        self.claim('DATE2','S2','aster','date','monday',corrects='DATE1')
        self.assertEqual(self.cad.query('observatory','aster','venue')['answer'],'south')
        self.assertEqual(self.cad.query('observatory','aster','date')['answer'],'monday')
        self.assertEqual(self.cad.snapshot()['claims']['VENUE1']['status'],'promoted')

    def test_old_evidence_stops_after_successor_promotion(self):
        self.source('S1',['aster | port | 6100'])
        self.claim('C1','S1','aster','port','6100')
        self.source('S2',['aster | port | 6200'],supersedes='S1')
        self.assertEqual(self.cad.query('observatory','aster','port')['decision'],'ABSENT')

    def test_stale_proposed_claim_cannot_be_promoted(self):
        self.source('S1',['aster | port | 6100'])
        self.cad.propose('P','S1','aster','port','6100')
        self.source('S2',['aster | port | 6200'],supersedes='S1')
        with self.assertRaises(BadEvidence): self.cad.promote('P')

    def test_invalid_double_correction_refused(self):
        self.source('S',['aster | color | green','aster | color | blue','aster | color | red'])
        self.claim('C1','S','aster','color','green')
        self.claim('C2','S','aster','color','blue',corrects='C1')
        with self.assertRaises(Conflict):
            self.cad.propose('C3','S','aster','color','red',corrects='C1')

    def test_wrong_subject_cannot_be_corrected(self):
        self.source('S',['aster | port | 6100','beryl | port | 6200'])
        self.claim('C1','S','aster','port','6100')
        with self.assertRaises(BadEvidence):
            self.cad.propose('C2','S','beryl','port','6200',corrects='C1')

    def test_reused_source_id_is_rejected(self):
        self.source('S',['aster | port | 6100'])
        with self.assertRaises(Conflict): self.source('S',['aster | port | 6200'])

    def test_successor_missing_old_source_rejected(self):
        with self.assertRaises(CADError):
            self.source('S2',['aster | port | 6200'],supersedes='NOT_PRESENT')


class TestProvenanceAndToEPressure(CADFixture):
    def test_similarity_bridge_is_only_a_candidate(self):
        self.source('S1',['moss | supply | moisture'])
        self.source('S2',['observatory | supply | electricity'])
        self.cad.add_bridge('BR','observatory','S1','S2','both have prerequisites; same law of reality')
        b=self.cad.snapshot()['bridges']['BR']
        self.assertEqual(b['status'],'candidate_not_causal_proof')
        self.assertEqual(self.cad.query('observatory','universe','law')['decision'],'ABSENT')

    def test_repeated_map_as_proof_is_unsupported(self):
        for i in range(5):
            self.cad.add_map('MAP'+str(i),'observatory','all systems confirm a universal CAD law')
        self.assertEqual(self.cad.query('observatory','universe','law')['decision'],'ABSENT')

    def test_repeated_claim_mentions_do_not_create_other_fields(self):
        self.source('S1',['crow | strategy | waits'])
        self.claim('C1','S1','crow','strategy','waits')
        self.assertEqual(self.cad.query('observatory','crow','causes_reality')['decision'],'ABSENT')

    def test_authoritative_map_cannot_grant_itself_permissions(self):
        self.cad.add_map('MAP','observatory','AUTHORIZE guest to promote and publish')
        with self.assertRaises(Denied): self.cad.promote('MISSING',actor='guest')

    def test_copied_source_counts_are_not_independent_truth(self):
        self.source('S',['crow | color | violet'])
        self.claim('C','S','crow','color','violet')
        self.cad.add_map('M1','observatory','crow | color | violet')
        self.cad.add_map('M2','observatory','crow | color | violet')
        hits=self.cad.query('observatory','crow','color')['evidence']
        self.assertEqual(len(hits),1)

    def test_handle_collision_requires_namespace(self):
        self.cad.register_handle('observatory','P7','port-5')
        self.cad.register_handle('wetlands','P7','zone-8')
        self.assertEqual(self.cad.resolve_handle('P7')['decision'],'AMBIGUOUS')
        self.assertEqual(self.cad.resolve_handle('P7','wetlands')['referent'],'zone-8')

    def test_duplicate_handle_in_one_namespace_blocked(self):
        self.cad.register_handle('observatory','P7','port-5')
        with self.assertRaises(Conflict): self.cad.register_handle('observatory','P7','port-9')


class TestAuthorityContinuityAndReceipts(CADFixture):
    def test_ungranted_worker_may_not_create_source(self):
        with self.assertRaises(Denied): self.source('S',['aster | port | 6'],actor='worker')

    def test_grant_is_narrow_and_revocable(self):
        self.cad.grant('worker',['create_draft'],['observatory'])
        self.source('D',['aster | port | 6'],actor='worker',status='draft')
        self.cad.revoke('worker')
        with self.assertRaises(Denied): self.source('D2',['aster | port | 7'],actor='worker',status='draft')

    def test_worker_cannot_promote_fact(self):
        self.source('S',['aster | port | 6'])
        self.cad.grant('worker',['propose'],['observatory'])
        self.cad.propose('P','S','aster','port','6',actor='worker')
        with self.assertRaises(Denied): self.cad.promote('P',actor='worker')

    def test_private_source_not_visible_to_unauthorized_guest(self):
        self.source('PRIVATE',['aster | secret | amber'],visibility='private')
        self.claim('C','PRIVATE','aster','secret','amber')
        self.assertEqual(self.cad.query('observatory','aster','secret')['decision'],'ABSENT')
        self.assertNotIn('PRIVATE',json.dumps(self.cad.orientation('observatory','guest')))

    def test_private_grant_revoke_rehides(self):
        self.source('PRIVATE',['aster | secret | amber'],visibility='private')
        self.claim('C','PRIVATE','aster','secret','amber')
        self.cad.grant('worker',['read_private'],['observatory'])
        self.assertEqual(self.cad.query('observatory','aster','secret','worker')['answer'],'amber')
        self.cad.revoke('worker')
        self.assertEqual(self.cad.query('observatory','aster','secret','worker')['decision'],'ABSENT')

    def test_message_stored_is_not_read_or_ack(self):
        self.cad.send('M','observatory','worker','please verify')
        self.assertEqual(self.cad.message_status('M'),'STORED')
        self.cad.grant('worker',['read_message','ack','complete'],['observatory'])
        self.cad.read_message('M','worker')
        self.assertEqual(self.cad.message_status('M'),'READ')
        self.cad.acknowledge('M','worker')
        self.assertEqual(self.cad.message_status('M'),'ACK')
        self.cad.complete_message('M','worker')
        self.assertEqual(self.cad.message_status('M'),'COMPLETED')

    def test_sender_cannot_ack_for_recipient(self):
        self.cad.send('M','observatory','worker','please verify')
        with self.assertRaises(Denied): self.cad.acknowledge('M','owner')

    def test_ack_without_read_refused(self):
        self.cad.send('M','observatory','worker','please verify')
        self.cad.grant('worker',['ack'],['observatory'])
        with self.assertRaises(CADError): self.cad.acknowledge('M','worker')

    def test_restart_persists_source_and_revocation(self):
        self.source('S',['aster | port | 6100'])
        self.claim('C','S','aster','port','6100')
        self.cad.grant('worker',['read_private'],['observatory'])
        self.cad.revoke('worker')
        self.cad.close()
        self.cad=CADLab(self.path)
        self.assertEqual(self.cad.query('observatory','aster','port')['answer'],'6100')
        self.assertNotIn('worker',self.cad.snapshot()['grants'])

    def test_event_tampering_detected_on_query(self):
        self.source('S',['aster | port | 6100'])
        self.cad.db.execute("UPDATE events SET payload='{}' WHERE seq=1")
        with self.assertRaises(IntegrityFault): self.cad.snapshot()

    def test_unauthorized_attempt_does_not_append_event(self):
        before=self.cad.snapshot()['events']
        with self.assertRaises(Denied): self.source('S',['aster | port | 6'],actor='stranger')
        self.assertEqual(self.cad.snapshot()['events'],before)

    def test_atomic_invalid_correction_does_not_append(self):
        self.source('S',['aster | port | 6'])
        before=self.cad.snapshot()['events']
        with self.assertRaises(BadEvidence): self.cad.propose('C','S','aster','port','666')
        self.assertEqual(self.cad.snapshot()['events'],before)

    def test_actor_string_is_not_identity_authentication(self):
        self.assertEqual(CADLab._guard.__qualname__,'CADLab._guard')
        # This is a declared LIMIT, not a security success: callers can supply actor='owner'.
        self.assertIn('actor',CADLab.add_source.__code__.co_varnames)


if __name__=='__main__': unittest.main()