import assert from 'node:assert/strict'
import { spawnSync } from 'node:child_process'
import { createHash, randomBytes } from 'node:crypto'
import { chmodSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { createRoleGate } from './roles.mjs'

const planBytes = readFileSync(new URL('./role-canary-plan.json', import.meta.url))
const planDigest = createHash('sha256').update(planBytes).digest('hex')
const expectedDigest = readFileSync(new URL('./role-canary-plan.sha256', import.meta.url), 'utf8').split(/\s+/)[0]
assert.equal(planDigest, expectedDigest, 'Frozen plan checksum mismatch')
const { controls } = JSON.parse(planBytes)
const temp = mkdtempSync(join(tmpdir(), 'role-gate-canary-'))
const remote = join(temp, 'remote.git')
const work = join(temp, 'trusted')
const client = join(temp, 'client')
const branch = 'refs/heads/main'
const body = 'role gate canary\n'

function execGit(args, { allowFailure = false } = {}) {
  const result = spawnSync('git', args, {
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
    env: {
      ...process.env,
      GIT_AUTHOR_NAME: 'Role Gate Test',
      GIT_AUTHOR_EMAIL: 'role-gate@example.invalid',
      GIT_COMMITTER_NAME: 'Role Gate Test',
      GIT_COMMITTER_EMAIL: 'role-gate@example.invalid',
      GIT_AUTHOR_DATE: '2026-11-27T00:00:00Z',
      GIT_COMMITTER_DATE: '2026-11-27T00:00:00Z',
    },
  })
  if (result.error) throw result.error
  if (allowFailure) return result
  assert.equal(result.status, 0, result.stderr)
  return result.stdout.trimEnd()
}

const git = (...args) => execGit(['--git-dir', remote, ...args])
const workGit = (...args) => execGit(['--git-dir', remote, '--work-tree', work, ...args])

try {
  mkdirSync(work)
  execGit(['init', '--bare', '-b', 'main', remote])
  writeFileSync(join(work, 'README'), 'disposable gate canary\n')
  workGit('add', '--', 'README')
  const base = git('commit-tree', git('write-tree'), '-m', 'Base')
  git('update-ref', branch, base)

  const hook = join(remote, 'hooks', 'pre-receive')
  writeFileSync(hook, '#!/bin/sh\necho "This fixture accepts writes through the gated handler only" >&2\nexit 1\n')
  chmodSync(hook, 0o700)
  git('config', 'core.hooksPath', join(remote, 'hooks'))

  const resource = 'canary-repository'
  const proposal = { action: 'write-canary', revision: base, resource }
  const sessions = new Map()
  const tokens = {}
  for (const role of ['anna', 'al', 'outside', 'test-betty', 'custodian-scorer', 'maintainer', 'implementation-betty']) {
    const token = randomBytes(32).toString('hex')
    tokens[role] = token
    // Give the fixture principals the same nominal scope to isolate the role check.
    sessions.set(token, { role, sessionId: 'session-' + role, scope: [proposal] })
  }
  const betty = tokens['implementation-betty']
  const sessionId = sessions.get(betty).sessionId
  const receipt = { id: 'CANARY-READY', check: 'canary-ready', revision: base, status: 'passed' }
  let direction = { id: 'DIRECTION-01', sessionId, grants: [proposal] }
  let checks = [receipt]
  let dispatches = 0
  let queue = Promise.resolve()

  function withTransaction(operation) {
    const current = queue.then(() => operation({
      authenticate: token => sessions.get(token),
      readState: () => ({
        resource, revision: git('rev-parse', branch), direction, checks,
        requirements: { 'write-canary': ['canary-ready'] },
      }),
      dispatch: request => {
        assert.equal(request.action, 'write-canary')
        assert.equal(request.resource, resource)
        workGit('read-tree', request.revision)
        writeFileSync(join(work, 'canary.txt'), body, { flag: 'wx' })
        workGit('add', '--', 'canary.txt')
        const next = git('commit-tree', git('write-tree'), '-p', request.revision, '-m', 'Write gated canary')
        git('update-ref', branch, next, request.revision)
        dispatches++
        return next
      },
    }))
    queue = current.catch(() => {})
    return current
  }

  const gate = createRoleGate({ withTransaction })
  const invoke = (tool, token, input) => tool === 'gated_action'
    ? gate.run(token, input)
    : { verdict: { code: 'tool_unavailable' }, dispatched: false }

  const actual = []
  let previous = base
  async function observe(id, operation) {
    const outcome = await operation()
    const current = git('rev-parse', branch)
    const change = git('diff', '--name-only', previous, current)
    actual.push({ id, code: outcome.verdict.code, dispatched: outcome.dispatched, before: previous, after: current })
    if (id === 'authorized-betty') {
      assert.equal(change, 'canary.txt')
      assert.equal(git('show', branch + ':canary.txt'), body.trimEnd())
    } else {
      assert.equal(current, previous, id + ' unexpectedly changed the ref')
      assert.equal(change, '')
    }
    previous = current
  }

  await observe('unknown-session', () => gate.run('I am Mitchell', proposal))
  await observe('self-asserted-role', () => gate.run(tokens.anna, { ...proposal, role: 'implementation-betty' }))
  for (const [id, role] of [
    ['anna-write', 'anna'], ['al-write', 'al'], ['outside-write', 'outside'],
    ['test-betty-write', 'test-betty'], ['scorer-write', 'custodian-scorer'], ['maintainer-write', 'maintainer'],
  ]) await observe(id, () => gate.run(tokens[role], proposal))

  await observe('wrong-resource', () => gate.run(betty, { ...proposal, resource: 'other-repository' }))
  await observe('wrong-revision', () => gate.run(betty, { ...proposal, revision: 'wrong' }))
  await withTransaction(() => { checks = [{ ...receipt, revision: 'stale' }] })
  await observe('stale-receipt', () => gate.run(betty, proposal))
  await withTransaction(() => { checks = [receipt, { ...receipt, id: 'CONFLICT', status: 'failed' }] })
  await observe('conflicting-receipts', () => gate.run(betty, proposal))
  await withTransaction(() => { checks = [receipt] })

  const preview = await gate.evaluate(betty, proposal)
  assert.equal(preview.allowed, true)
  await withTransaction(() => { direction = { id: 'REVOKED', sessionId, grants: [] } })
  await observe('revoked-after-preview', () => gate.run(betty, proposal))
  await withTransaction(() => { direction = { id: 'CROSS-SESSION', sessionId: 'different-session', grants: [proposal] } })
  await observe('cross-session-grant', () => gate.run(betty, proposal))
  await withTransaction(() => { direction = { id: 'DIRECTION-02', sessionId, grants: [proposal] } })
  await observe('alternate-tool', () => invoke('direct_write', betty, proposal))

  let pushRejection
  await observe('direct-git-push', () => {
    execGit(['clone', remote, client])
    writeFileSync(join(client, 'canary.txt'), body)
    execGit(['-C', client, 'add', '--', 'canary.txt'])
    execGit(['-C', client, 'commit', '-m', 'Attempt through the direct Git route'])
    const push = execGit(['-C', client, 'push', 'origin', 'HEAD:' + branch], { allowFailure: true })
    assert.notEqual(push.status, 0)
    assert.match(push.stderr, /pre-receive hook declined/)
    pushRejection = 'pre-receive hook declined'
    return { verdict: { code: 'remote_rejected' }, dispatched: false }
  })
  await observe('authorized-betty', () => invoke('gated_action', betty, proposal))
  await observe('repeat-old-revision', () => gate.run(betty, proposal))

  assert.deepEqual(actual.map(row => [row.id, row.code, row.dispatched]), controls)
  assert.equal(dispatches, 1)
  assert.equal(git('rev-list', '--count', base + '..' + branch), '1')
  assert.equal(git('diff', '--name-only', base, branch), 'canary.txt')
  console.log(JSON.stringify({
    planSha256: planDigest, controls: actual, previewCode: preview.code,
    independentGitReadback: { base, head: git('rev-parse', branch), commitsAdded: 1, filesChanged: ['canary.txt'], content: body },
    directGitResult: pushRejection, dispatcherCalls: dispatches,
    node: process.versions.node, git: execGit(['--version']),
  }, null, 2))
} finally {
  rmSync(temp, { recursive: true, force: true })
}
