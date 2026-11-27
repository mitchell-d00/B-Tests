import { readFile } from 'node:fs/promises'
import { stdin } from 'node:process'
import { evaluateAction, evaluatePpcGate } from './index.mjs'

async function main() {
  const args = process.argv.slice(2)
  const ppc = args[0] === '--ppc'
  const [statePath, ...extra] = ppc ? args.slice(1) : args
  if (!statePath || extra.length) {
    throw new Error('Usage: node gate-js/cli.mjs [--ppc] STATE.json < proposal.json')
  }

  const state = JSON.parse(await readFile(statePath, 'utf8'))
  stdin.setEncoding('utf8')
  let body = ''
  for await (const chunk of stdin) body += chunk
  const proposal = JSON.parse(body)
  const result = ppc ? { decision: evaluatePpcGate(proposal, state) } : evaluateAction(proposal, state)
  process.stdout.write(JSON.stringify(result) + '\n')
  const allowed = ppc ? result.decision === 'ACCEPT' : result.allowed
  if (!allowed) process.exitCode = 1
}

main().catch(error => {
  process.stderr.write(error.message + '\n')
  process.exitCode = 2
})
