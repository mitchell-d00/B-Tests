import assert from 'node:assert/strict'
import { test } from 'node:test'
import { createRoleGate } from './roles.mjs'

const resource = 'packet-01'
const revision = 'rev-01'
const submit = { action: 'submit-first-response', resource, revision }
const note = { action: 'prepare-review-note', resource, revision }
const write = { action: 'write-canary', resource, revision }

function trial() {
  let calls = 0
  let slotStatus = 'passed'
  let queue = Promise.resolve()
  const principals = {
    anna: { sessionId: 'anna-01', role: 'anna', scope: [submit, note, write] },
    testBetty: { sessionId: 'tb-01', role: 'test-betty', scope: [submit, note, write] },
  }
  const gate = createRoleGate({
    withTransaction(operation) {
      const run = queue.then(() => operation({
        authenticate: name => Object.hasOwn(principals, name) && principals[name],
        readState: ({ sessionId }) => ({
          revision, resource,
          direction: { id: 'DIR-1', sessionId, grants: [submit, note, write] },
          requirements: { 'submit-first-response': ['submission-open'], 'prepare-review-note': [], 'write-canary': [] },
          checks: [{ id: 'SLOT-01', check: 'submission-open', revision, status: slotStatus }],
        }),
        dispatch: proposal => {
          if (proposal.action === submit.action) slotStatus = 'canceled'
          calls++
        },
      }))
      queue = run.catch(() => {})
      return run
    },
  })
  return { gate, calls: () => calls }
}

test('serialized first submissions consume the slot once', async () => {
  const { gate, calls } = trial()
  const [first, second] = await Promise.all([gate.run('anna', submit), gate.run('anna', submit)])
  assert.equal(first.dispatched, true)
  assert.equal(second.verdict.code, 'check_not_passed')
  assert.equal(calls(), 1)
})

test('completion does not promote Anna or give Test Betty implementation permission', async () => {
  const { gate, calls } = trial()
  assert.equal((await gate.run('anna', submit)).dispatched, true)
  assert.equal((await gate.run('anna', note)).verdict.code, 'role_denied')
  assert.equal((await gate.run('testBetty', note)).dispatched, true)
  assert.equal((await gate.run('testBetty', write)).verdict.code, 'role_denied')
  assert.equal(calls(), 2)
})

test('a first-response action cannot omit the host-owned open-slot requirement', async () => {
  const gate = createRoleGate({
    withTransaction: operation => operation({
      authenticate: () => ({ sessionId: 'anna-01', role: 'anna', scope: [submit] }),
      readState: () => ({
        revision, resource,
        direction: { id: 'DIR-1', sessionId: 'anna-01', grants: [submit] },
        requirements: { 'submit-first-response': [] }, checks: [],
      }),
      dispatch: () => assert.fail('submission reached the dispatcher'),
    }),
  })
  assert.equal((await gate.run('anna', submit)).verdict.code, 'invalid_state')
})
