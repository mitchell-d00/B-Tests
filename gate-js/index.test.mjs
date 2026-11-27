import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { test } from 'node:test'
import { createActionGate, evaluateAction } from './index.mjs'

const r7 = JSON.parse(readFileSync(new URL('./round-7.json', import.meta.url), 'utf8'))
const deploy = { action: 'deploy', revision: 'R7' }
const smoke = { action: 'run-smoke', revision: 'R7' }
const passed = { id: 'SMOKE-R7', revision: 'R7', check: 'post-merge-smoke', status: 'passed' }

function withChecks(...receipts) {
  return { ...r7, checks: [...r7.checks, ...receipts] }
}

test('allows the R4 accessibility review authorized for R4', () => {
  const action = { action: 'review-accessibility', revision: 'R4' }
  const state = {
    revision: 'R4',
    direction: { id: 'DIR-R4', grants: [action] },
    requirements: { 'review-accessibility': [] },
    checks: [],
  }
  assert.equal(evaluateAction(action, state).allowed, true)
})

test('blocks R7 deployment when the passing receipt is for P7', () => {
  assert.deepEqual(evaluateAction(deploy, r7), {
    allowed: false, code: 'missing_check', proposal: deploy,
    directionId: 'DIR-R7', check: 'post-merge-smoke',
  })
})

for (const status of ['failed', 'pending', 'not_run', 'canceled']) {
  test(`blocks R7 deployment for an R7 receipt marked ${status}`, () => {
    const verdict = evaluateAction(deploy, withChecks({ ...passed, status }))
    assert.equal(verdict.code, 'check_not_passed')
    assert.equal(verdict.status, status)
  })
}

test('allows R7 deployment after the required R7 receipt passes', () => {
  assert.deepEqual(evaluateAction(deploy, withChecks(passed)), {
    allowed: true, code: 'allowed', proposal: deploy, directionId: 'DIR-R7', receiptIds: ['SMOKE-R7'],
  })
})

test('blocks conflicting same-revision receipts and duplicate grants', () => {
  const conflicting = withChecks(passed, { ...passed, id: 'SMOKE-R7-2', status: 'failed' })
  assert.equal(evaluateAction(deploy, conflicting).code, 'ambiguous_check')
  const duplicateGrant = { ...r7, direction: { id: 'DIR-R7', grants: [deploy, deploy] } }
  assert.equal(evaluateAction(deploy, duplicateGrant).code, 'ambiguous_authorization')
})

test('blocks R8 retry while allowing the scoped inspection', () => {
  const inspect = { action: 'inspect-canceled-job', revision: 'R8' }
  const state = {
    revision: 'R8',
    direction: { id: 'DIR-R8', grants: [inspect] },
    requirements: { 'inspect-canceled-job': [], 'retry-deployment': [] },
    checks: [],
  }
  assert.equal(evaluateAction(inspect, state).allowed, true)
  assert.equal(evaluateAction({ action: 'retry-deployment', revision: 'R8' }, state).code, 'not_authorized')
})

test('rejects wrong revisions and action keys outside the policy', () => {
  assert.equal(evaluateAction({ ...deploy, revision: 'P7' }, r7).code, 'revision_mismatch')
  assert.equal(evaluateAction({ ...deploy, action: 'publish' }, r7).code, 'unknown_action')
  assert.equal(evaluateAction({ ...deploy, action: 'constructor' }, r7).code, 'unknown_action')
})

test('rejects inline policy overrides and malformed state', () => {
  assert.equal(evaluateAction({ ...deploy, checks: [passed] }, r7).code, 'invalid_proposal')
  assert.equal(evaluateAction(deploy, { ...r7, checks: [{ ...passed, status: true }] }).code, 'invalid_state')
  assert.equal(evaluateAction(deploy, { ...r7, requirements: null }).code, 'invalid_state')
})

test('only dispatches allowed proposals and rereads trusted state each time', async () => {
  const observed = []
  let state = r7
  const gate = createActionGate({
    readState: () => state,
    dispatch: proposal => {
      observed.push(proposal)
      return 'simulated effect'
    },
  })

  assert.equal((await gate.evaluate(smoke)).allowed, true)
  assert.equal((await gate.run(deploy)).dispatched, false)
  assert.deepEqual(observed, [])
  assert.equal((await gate.run(smoke)).dispatched, true)

  state = withChecks(passed)
  assert.equal((await gate.run(deploy)).result, 'simulated effect')
  assert.deepEqual(observed, [smoke, deploy])

  state = { ...state, direction: { id: 'DIR-NEXT', grants: [] } }
  assert.equal((await gate.run(deploy)).dispatched, false)
  assert.deepEqual(observed, [smoke, deploy])
})

test('does not dispatch when trusted state is unavailable', async () => {
  const gate = createActionGate({
    readState: async () => { throw new Error('offline') },
    dispatch: () => assert.fail('blocked proposal reached dispatcher'),
  })
  const result = await gate.run(deploy)
  assert.equal(result.verdict.code, 'state_unavailable')
  assert.equal(result.dispatched, false)
})

test('binds the validated action and revision before waiting for state', async () => {
  const input = { ...smoke }
  const gate = createActionGate({
    readState: async () => {
      input.action = 'deploy'
      return r7
    },
    dispatch: proposal => proposal,
  })
  const result = await gate.run(input)
  assert.deepEqual(result.result, smoke)
})
