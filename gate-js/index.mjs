const TOKEN = /^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$/
const ACTION = /^[a-z][a-z0-9-]{0,63}$/
const CHECK_STATES = new Set(['passed', 'failed', 'pending', 'not_run', 'canceled'])

function isRecord(value) {
  return value !== null && typeof value === 'object' &&
    [Object.prototype, null].includes(Object.getPrototypeOf(value))
}

function isToken(value) {
  return typeof value === 'string' && TOKEN.test(value)
}

function isAction(value) {
  return typeof value === 'string' && ACTION.test(value)
}

function all(list, predicate) {
  return Array.isArray(list) && Array.from(list).every(predicate)
}

function readProposal(proposal) {
  if (!isRecord(proposal) || Object.keys(proposal).length !== 2 ||
      !Object.hasOwn(proposal, 'action') || !Object.hasOwn(proposal, 'revision')) {
    return null
  }
  const { action, revision } = proposal
  return isAction(action) && isToken(revision) ? Object.freeze({ action, revision }) : null
}

function validState(state) {
  return isRecord(state) && isToken(state.revision) &&
    isRecord(state.direction) && isToken(state.direction.id) &&
    all(state.direction.grants, grant =>
      isRecord(grant) && isAction(grant.action) && isToken(grant.revision)) &&
    isRecord(state.requirements) &&
    Object.entries(state.requirements).every(([action, checks]) =>
      isAction(action) && all(checks, isToken) && new Set(checks).size === checks.length) &&
    all(state.checks, receipt => isRecord(receipt) && isToken(receipt.id) &&
      isToken(receipt.revision) && isToken(receipt.check) && CHECK_STATES.has(receipt.status))
}

/** Evaluate a model's proposal against the caller's independently supplied state. */
export function evaluateAction(input, state) {
  const proposal = readProposal(input)
  const verdict = (code, detail = {}) => ({
    allowed: code === 'allowed',
    code,
    proposal,
    ...detail,
  })
  if (!proposal) return verdict('invalid_proposal')
  if (!validState(state)) return verdict('invalid_state')
  if (proposal.revision !== state.revision) {
    return verdict('revision_mismatch', { expectedRevision: state.revision })
  }
  if (!Object.hasOwn(state.requirements, proposal.action)) return verdict('unknown_action')

  const directionId = state.direction.id
  const grants = state.direction.grants.filter(grant =>
    grant.action === proposal.action && grant.revision === proposal.revision)
  if (grants.length !== 1) {
    const code = grants.length === 0 ? 'not_authorized' : 'ambiguous_authorization'
    return verdict(code, { directionId })
  }

  const receiptIds = []
  for (const check of state.requirements[proposal.action]) {
    const receipts = state.checks.filter(receipt =>
      receipt.check === check && receipt.revision === proposal.revision)
    if (receipts.length === 0) return verdict('missing_check', { directionId, check })
    if (receipts.length > 1) return verdict('ambiguous_check', { directionId, check })
    const [receipt] = receipts
    if (receipt.status !== 'passed') {
      return verdict('check_not_passed', { directionId, check, status: receipt.status, receiptId: receipt.id })
    }
    receiptIds.push(receipt.id)
  }

  return verdict('allowed', { directionId, receiptIds })
}

/** Bind state and effects to trusted application code. Model callers submit only proposals. */
export function createActionGate({ readState, dispatch }) {
  if (typeof readState !== 'function' || typeof dispatch !== 'function') {
    throw new TypeError('readState and dispatch must be functions')
  }

  async function evaluate(input) {
    const proposal = readProposal(input)
    if (!proposal) return evaluateAction(input)
    try {
      return evaluateAction(proposal, await readState())
    } catch {
      return { allowed: false, code: 'state_unavailable', proposal }
    }
  }

  async function run(input) {
    const verdict = await evaluate(input)
    if (!verdict.allowed) return { verdict, dispatched: false }
    const result = await dispatch(verdict.proposal, verdict)
    return { verdict, dispatched: true, result }
  }

  return Object.freeze({ evaluate, run })
}

/** JavaScript equivalent of the archived PPC v0.2 treatment C predicate. */
export function evaluatePpcGate(proposal, eligible) {
  const accepts = isRecord(proposal) && Object.keys(proposal).length === 2 &&
    Object.hasOwn(proposal, 'decision') && Object.hasOwn(proposal, 'acknowledged') &&
    proposal.decision === 'ACCEPT' && typeof proposal.acknowledged === 'boolean'
  return accepts && eligible === true ? 'ACCEPT' : 'REFUSE'
}
