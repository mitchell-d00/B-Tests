import { evaluateAction } from './index.mjs'

const ROLE_ACTIONS = new Map([
  ['outside', ['read-permitted', 'record-objection']],
  ['al', ['inspect-repo', 'inspect-evidence', 'propose-work']],
  ['anna', ['read-packet', 'submit-first-response']],
  ['test-betty', ['record-trial', 'prepare-review-note']],
  ['implementation-betty', [
    'inspect-repo', 'inspect-evidence', 'edit', 'run-tests', 'publish',
    'write-canary', 'run-smoke', 'review-accessibility', 'deploy', 'retry-deployment',
  ]],
  ['custodian-scorer', ['read-key', 'score-response']],
  ['maintainer', ['assign-role', 'authorize-scope', 'revoke-scope']],
])

const KEY = /^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$/
const ACTION = /^[a-z][a-z0-9-]{0,63}$/

function readProposal(value) {
  if (!value || ![Object.prototype, null].includes(Object.getPrototypeOf(value)) ||
      Object.keys(value).length !== 3 ||
      !['action', 'revision', 'resource'].every(key => Object.hasOwn(value, key) && typeof value[key] === 'string')) {
    return null
  }
  const { action, revision, resource } = value
  if (!ACTION.test(action) || !KEY.test(revision) || !KEY.test(resource)) return null
  return Object.freeze({ action, revision, resource })
}

function matchesScope(scope, proposal) {
  return scope?.resource === proposal.resource && scope?.action === proposal.action
}

function denial(code, proposal) {
  return { allowed: false, code, proposal }
}

/**
 * The host authenticates opaque request context and owns the transaction, state and credentials.
 * It serializes grants/revocations with execution or makes its dispatcher revalidate atomically.
 */
export function createRoleGate({ withTransaction }) {
  if (typeof withTransaction !== 'function') throw new TypeError('withTransaction must be a function')

  async function decide(tx, context, proposal) {
    let principal
    try {
      principal = await tx.authenticate(context)
    } catch {
      return denial('unverified_session', proposal)
    }
    if (typeof principal?.sessionId !== 'string' || !KEY.test(principal.sessionId) ||
        !ROLE_ACTIONS.has(principal.role)) {
      return denial('unverified_session', proposal)
    }
    const { sessionId, role, scope } = principal
    if (!ROLE_ACTIONS.get(role).includes(proposal.action)) return denial('role_denied', proposal)
    if (!Array.isArray(scope) || !scope.some(entry => matchesScope(entry, proposal))) {
      return denial('scope_denied', proposal)
    }

    let state
    try {
      state = await tx.readState({ sessionId, resource: proposal.resource })
    } catch {
      return denial('state_unavailable', proposal)
    }
    if (state == null) return denial('state_unavailable', proposal)
    if (state.resource !== proposal.resource || state.direction?.sessionId !== sessionId) {
      return denial('scope_binding_mismatch', proposal)
    }

    // The host must close this receipt within the same transaction as the first submission.
    if (proposal.action === 'submit-first-response' &&
        (!Array.isArray(state.requirements?.['submit-first-response']) ||
         !state.requirements['submit-first-response'].includes('submission-open'))) {
      return denial('invalid_state', proposal)
    }
    const { action, revision } = proposal
    const verdict = evaluateAction({ action, revision }, state)
    return { ...verdict, proposal, sessionId, role }
  }

  async function evaluate(context, input) {
    const proposal = readProposal(input)
    if (!proposal) return denial('invalid_proposal', null)
    return withTransaction(tx => decide(tx, context, proposal))
  }

  async function run(context, input) {
    const proposal = readProposal(input)
    if (!proposal) return { verdict: denial('invalid_proposal', null), dispatched: false }
    return withTransaction(async tx => {
      const verdict = await decide(tx, context, proposal)
      if (!verdict.allowed) return { verdict, dispatched: false }
      const result = await tx.dispatch(proposal, verdict)
      return { verdict, dispatched: true, result }
    })
  }

  return Object.freeze({ evaluate, run })
}
