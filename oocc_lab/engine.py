"""Small source-governed OOCC/CAD workbench backed by verified SQLite events.

Claims are literal structured statements of the form `SUBJECT | FIELD | VALUE`
inside immutable source bytes. That deliberately avoids pretending that this
proof-of-principle implements natural-language semantic entailment.

The request's actor is assumed to have been authenticated *by the caller*.
No network/identity provider is implemented; a caller could spoof an actor if
this module were naively exposed as an HTTP service. Do not deploy it that way.
"""
from __future__ import annotations
import hashlib
import json
import sqlite3
from pathlib import Path


class CADError(ValueError): pass
class IntegrityFault(CADError): pass
class Denied(CADError): pass
class Conflict(CADError): pass
class BadEvidence(CADError): pass


def canon(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False)


def digest(value):
    return hashlib.sha256(canon(value).encode('utf-8')).hexdigest()


def sha(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


class CADLab:
    """Durable, explicit, human-governed object map, not a model or crawler."""
    def __init__(self, location):
        self.path = str(location)
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(self.path, isolation_level=None, timeout=8)
        self.db.execute('PRAGMA busy_timeout=8000')
        self.db.execute('PRAGMA journal_mode=WAL')
        self.db.execute('''CREATE TABLE IF NOT EXISTS events (
            seq INTEGER PRIMARY KEY, kind TEXT NOT NULL, payload TEXT NOT NULL,
            previous TEXT NOT NULL, digest TEXT NOT NULL)''')

    def close(self):
        self.db.close()

    def __enter__(self): return self
    def __exit__(self,*unused): self.close()

    def _replay(self, db=None):
        q = db or self.db
        state = {'sources':{},'claims':{},'grants':{},'messages':{},
                 'notes':{},'bridges':{},'handles':{},'events':0,'head':'0'*64}
        prev = '0'*64
        for seq,kind,raw,old,actual in q.execute('SELECT seq,kind,payload,previous,digest FROM events ORDER BY seq'):
            if seq != state['events']+1 or old != prev:
                raise IntegrityFault('EVENT_SEQUENCE_OR_PREVIOUS_HASH')
            try: payload=json.loads(raw)
            except (ValueError,TypeError) as e: raise IntegrityFault('EVENT_PAYLOAD_INVALID') from e
            if canon(payload)!=raw:
                raise IntegrityFault('EVENT_NONCANONICAL_PAYLOAD')
            if digest({'seq':seq,'kind':kind,'payload':payload,'previous':old}) != actual:
                raise IntegrityFault('EVENT_DIGEST_MISMATCH')
            self._project(state,kind,payload)
            state['events']+=1
            prev=actual
        state['head']=prev
        return state

    @staticmethod
    def _project(s,kind,p):
        if kind=='source.create': s['sources'][p['id']] = p
        elif kind=='claim.propose': s['claims'][p['id']] = dict(p,status='proposed')
        elif kind=='claim.promote': s['claims'][p['id']]['status']='promoted'
        elif kind=='grant.set': s['grants'][p['grantee']]=p
        elif kind=='grant.revoke': s['grants'].pop(p['grantee'],None)
        elif kind=='message.send': s['messages'][p['id']]=dict(p,receipt='stored')
        elif kind=='message.read': s['messages'][p['id']]['receipt']='read'
        elif kind=='message.ack': s['messages'][p['id']]['receipt']='ack'
        elif kind=='message.complete': s['messages'][p['id']]['receipt']='completed'
        elif kind=='note.create': s['notes'][p['id']]=p
        elif kind=='bridge.candidate': s['bridges'][p['id']]=p
        elif kind=='handle.register': s['handles'][p['namespace']+'::'+p['name']]=p
        else: raise IntegrityFault('UNKNOWN_EVENT_KIND:'+kind)

    def snapshot(self):
        """Validate hash chain on every read; no separately trusted projection."""
        return self._replay()

    def _write(self, actor, kind, build, action, namespace=None):
        self.db.execute('BEGIN IMMEDIATE')
        try:
            st=self._replay(self.db)
            self._guard(st,actor,action,namespace)
            p=build(st)
            if not isinstance(p,dict): raise CADError('INVALID_EVENT')
            # Verify a replay can project the proposed state before committing.
            shadow={k: (v.copy() if isinstance(v,dict) else v) for k,v in st.items()}
            shadow['claims']={k:v.copy() for k,v in st['claims'].items()}
            shadow['messages']={k:v.copy() for k,v in st['messages'].items()}
            self._project(shadow,kind,p)
            seq=st['events']+1
            h=digest({'seq':seq,'kind':kind,'payload':p,'previous':st['head']})
            self.db.execute('INSERT INTO events(seq,kind,payload,previous,digest) VALUES(?,?,?,?,?)',
                            (seq,kind,canon(p),st['head'],h))
            self.db.execute('COMMIT')
            return {'seq':seq,'head':h,'event':kind,'payload':p}
        except BaseException:
            self.db.execute('ROLLBACK')
            raise

    @staticmethod
    def _guard(st,actor,action,namespace):
        if actor=='owner': return
        g=st['grants'].get(actor)
        if not g or action not in g['actions'] or (namespace is not None and namespace not in g['namespaces']):
            raise Denied('UNAUTHORIZED_ACTION')

    @staticmethod
    def _unique(st,id_):
        if any(id_ in st[k] for k in ('sources','claims','messages','notes','bridges')):
            raise Conflict('ID_REUSED')

    @staticmethod
    def source_status(st,source_id):
        src=st['sources'][source_id]
        if any(s.get('supersedes')==source_id for s in st['sources'].values()):
            return 'historical'
        return src['status']

    @staticmethod
    def _public(st,src,requester):
        return src['visibility']=='public' or requester=='owner' or (
            requester in st['grants'] and
            src['namespace'] in st['grants'][requester]['namespaces'] and
            'read_private' in st['grants'][requester]['actions'])

    def grant(self,grantee,actions,namespaces,actor='owner'):
        if not grantee or grantee=='owner' or not actions or not namespaces:
            raise CADError('BAD_GRANT')
        approved={'read_private','propose','send','read_message','ack','complete','create_draft','make_bridge'}
        if set(actions)-approved: raise Denied('PRIVILEGE_CANNOT_BE_DELEGATED')
        return self._write(actor,'grant.set',lambda s:{'grantee':grantee,'actions':sorted(set(actions)),
            'namespaces':sorted(set(namespaces))},'admin')

    def revoke(self,grantee,actor='owner'):
        def build(s):
            if grantee not in s['grants']: raise CADError('NO_SUCH_GRANT')
            return {'grantee':grantee}
        return self._write(actor,'grant.revoke',build,'admin')

    def add_source(self,id_,namespace,body,actor='owner',status='current',visibility='public',
                   role='source',weight=1,next_safe_action='verify',supersedes=None):
        if status not in ('current','draft','blocked','historical') or visibility not in ('public','private'):
            raise CADError('INVALID_SOURCE_METADATA')
        if not isinstance(body,str) or not body.strip() or len(body)>300000: raise CADError('INVALID_SOURCE_BODY')
        if not isinstance(weight,int) or not 0<=weight<=10: raise CADError('INVALID_WEIGHT')
        if role not in ('source','draft','note'): raise CADError('INVALID_SOURCE_ROLE')
        action='create_draft' if status=='draft' else 'source_write'
        def build(s):
            self._unique(s,id_)
            if supersedes:
                old=s['sources'].get(supersedes)
                if not old or old['namespace']!=namespace or self.source_status(s,supersedes)!='current':
                    raise CADError('INVALID_SUPERSESSION')
                if status!='current' or actor!='owner': raise Denied('INVALID_SUCCESSOR_AUTHORITY')
            return {'id':id_,'namespace':namespace,'body':body,'sha256':sha(body),
                    'actor':actor,'status':status,'visibility':visibility,'role':role,
                    'weight':weight,'next_safe_action':next_safe_action,'supersedes':supersedes}
        return self._write(actor,'source.create',build,action,namespace)

    def propose(self,id_,source_id,subject,field,value,actor='owner',corrects=None):
        """Literal structured evidence only; no free-prose semantic entailment."""
        def build(s):
            self._unique(s,id_)
            src=s['sources'].get(source_id)
            if not src or self.source_status(s,source_id)!='current': raise BadEvidence('SOURCE_NOT_CURRENT')
            if not self._public(s,src,actor): raise Denied('SOURCE_NOT_VISIBLE')
            if not all(isinstance(x,str) and x.strip() and '|' not in x and '\n' not in x
                       for x in (subject,field,value)):
                raise BadEvidence('INVALID_TRIPLE')
            evidence=f'{subject} | {field} | {value}'
            if evidence not in src['body'].splitlines(): raise BadEvidence('NO_EXACT_SOURCE_STATEMENT')
            if corrects:
                old=s['claims'].get(corrects)
                if (not old or old['status']!='promoted' or old['namespace']!=src['namespace'] or
                        old['subject']!=subject or old['field']!=field):
                    raise BadEvidence('INVALID_CORRECTION_TARGET')
                if any(c.get('corrects')==corrects and c['status']=='promoted' for c in s['claims'].values()):
                    raise Conflict('ALREADY_CORRECTED')
            return {'id':id_,'source_id':source_id,'namespace':src['namespace'],
                    'subject':subject,'field':field,'value':value,'exact_quote':evidence,
                    'source_sha256':src['sha256'],'actor':actor,'corrects':corrects}
        # Resolve namespace inside transaction so namespace grants cannot be spoofed.
        ns=self.snapshot()['sources'].get(source_id,{}).get('namespace')
        return self._write(actor,'claim.propose',build,'propose',ns)

    def promote(self,id_,actor='owner'):
        def build(s):
            c=s['claims'].get(id_)
            if not c or c['status']!='proposed': raise CADError('NOT_PROPOSED')
            src=s['sources'][c['source_id']]
            if self.source_status(s,c['source_id'])!='current' or src['sha256']!=c['source_sha256']:
                raise BadEvidence('STALE_EVIDENCE')
            if c['corrects'] and (s['claims'][c['corrects']]['status']!='promoted' or
                    any(x['status']=='promoted' and x.get('corrects')==c['corrects'] for x in s['claims'].values())):
                raise Conflict('INVALID_CORRECTION_NOW')
            return {'id':id_,'actor':actor}
        return self._write(actor,'claim.promote',build,'promote')

    @staticmethod
    def _claim_live(st,c):
        src=st['sources'][c['source_id']]
        return (c['status']=='promoted' and CADLab.source_status(st,c['source_id'])=='current'
                and not any(x['status']=='promoted' and x.get('corrects')==c['id'] for x in st['claims'].values()))

    def query(self,namespace,subject,field,requester='guest'):
        st=self.snapshot()
        hits=[]
        for c in st['claims'].values():
            if c['namespace']!=namespace or c['subject']!=subject or c['field']!=field or not self._claim_live(st,c):
                continue
            source=st['sources'][c['source_id']]
            if not self._public(st,source,requester): continue
            hits.append({'claim_id':c['id'],'value':c['value'],'source_id':c['source_id'],
                         'source_sha256':source['sha256'],'quote':c['exact_quote']})
        # One eligible source line per claim, no duplicate-root inflation.
        # Different eligible source lines with matching value remain distinct cited evidence.
        values={h['value'] for h in hits}
        if not hits: return {'decision':'ABSENT','answer':None,'evidence':[]}
        if len(values)>1: return {'decision':'CONFLICT','answer':None,'evidence':hits}
        return {'decision':'SUPPORTED_SOURCE_STATEMENT','answer':next(iter(values)),'evidence':hits}

    def add_map(self,id_,namespace,body,actor='owner',next_safe_action='check_originals',weight=3):
        def build(s):
            self._unique(s,id_)
            return {'id':id_,'namespace':namespace,'body':body,'actor':actor,
                    'role':'orientation_map','weight':weight,'authority':'non_evidentiary',
                    'next_safe_action':next_safe_action}
        return self._write(actor,'note.create',build,'map_write',namespace)

    def add_bridge(self,id_,namespace,left_source,right_source,description,actor='owner'):
        def build(s):
            self._unique(s,id_)
            for sid in (left_source,right_source):
                src=s['sources'].get(sid)
                if not src or src['namespace']!=namespace or not self._public(s,src,actor):
                    raise BadEvidence('BRIDGE_SOURCE_INELIGIBLE')
            return {'id':id_,'namespace':namespace,'left':left_source,'right':right_source,
                    'description':description,'status':'candidate_not_causal_proof','actor':actor}
        return self._write(actor,'bridge.candidate',build,'make_bridge',namespace)

    def register_handle(self,namespace,name,referent,actor='owner'):
        def build(s):
            key=namespace+'::'+name
            if key in s['handles']: raise Conflict('CANONICAL_HANDLE_ALREADY_ESTABLISHED')
            if not name or not referent: raise CADError('BAD_HANDLE')
            return {'namespace':namespace,'name':name,'referent':referent,'actor':actor}
        return self._write(actor,'handle.register',build,'handle_write',namespace)

    def resolve_handle(self,name,namespace=None):
        st=self.snapshot()
        hits=[p for p in st['handles'].values() if p['name']==name and
              (namespace is None or p['namespace']==namespace)]
        if not hits: return {'decision':'ABSENT'}
        if len(hits)>1: return {'decision':'AMBIGUOUS','namespaces':sorted(x['namespace'] for x in hits)}
        return {'decision':'RESOLVED','referent':hits[0]['referent'],'namespace':hits[0]['namespace']}

    def send(self,id_,namespace,recipient,body,actor='owner'):
        def build(s):
            self._unique(s,id_)
            if not recipient or not body: raise CADError('INVALID_MESSAGE')
            return {'id':id_,'namespace':namespace,'sender':actor,'recipient':recipient,
                    'body':body,'sha256':sha(body)}
        return self._write(actor,'message.send',build,'send',namespace)

    def _message_step(self,id_,actor,kind,prior,action):
        snap=self.snapshot()
        ns=snap['messages'].get(id_,{}).get('namespace')
        def build(s):
            m=s['messages'].get(id_)
            if not m: raise CADError('NO_MESSAGE')
            if m['recipient']!=actor: raise Denied('ONLY_RECIPIENT_MAY_ATTEST')
            if m['receipt']!=prior: raise CADError('RECEIPT_PREREQUISITE_MISSING')
            return {'id':id_,'actor':actor,'previous':prior}
        return self._write(actor,kind,build,action,ns)

    def read_message(self,id_,actor):
        return self._message_step(id_,actor,'message.read','stored','read_message')
    def acknowledge(self,id_,actor):
        return self._message_step(id_,actor,'message.ack','read','ack')
    def complete_message(self,id_,actor):
        return self._message_step(id_,actor,'message.complete','ack','complete')

    def message_status(self,id_,requester='owner'):
        s=self.snapshot();m=s['messages'].get(id_)
        if not m: return 'ABSENT'
        if requester not in ('owner',m['sender'],m['recipient']): return 'ABSENT'
        return m['receipt'].upper()

    def orientation(self,namespace,requester='guest'):
        """Human-readable CAD re-entry interface, never a source-of-truth replacement."""
        st=self.snapshot()
        objects=[]
        for src in st['sources'].values():
            if src['namespace']!=namespace or not self._public(st,src,requester): continue
            objects.append({'id':src['id'],'role':src['role'],
                'authority':self.source_status(st,src['id']),'boundary':src['visibility'],
                'continuity':'persisted','directive':src['next_safe_action'],
                'weight':src['weight'],'sha256':src['sha256']})
        objects.sort(key=lambda x:(-x['weight'],x['id']))
        notes=[{'id':n['id'],'authority':'non_evidentiary','directive':n['next_safe_action']}
               for n in st['notes'].values() if n['namespace']==namespace]
        blockers=[x['id'] for x in objects if x['authority']=='blocked']
        return {'namespace':namespace,'continuity':objects,'authority':'source-specific, not truth',
                'directive':'inspect_current_originals_before_action',
                'blocked':blockers,'maps':notes,'head':st['head'],
                'event_count':st['events'],'warning':'Orientation is not itself factual evidence'}

    def event_log(self):
        st=self.snapshot()
        return [{'seq':seq,'kind':kind,'digest':h,'previous':previous} for seq,kind,previous,h in
                self.db.execute('SELECT seq,kind,previous,digest FROM events ORDER BY seq')]