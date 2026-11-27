#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -B - <<'PY' | node --input-type=module -e '
import assert from "node:assert/strict"
import { readFileSync } from "node:fs"
import { evaluatePpcGate } from "./gate-js/index.mjs"

const rows = JSON.parse(readFileSync(0, "utf8"))
assert.equal(rows.length, 72)
for (const [id, proposal, eligibility, expected] of rows) {
  assert.equal(evaluatePpcGate(proposal, eligibility), expected, id)
}
console.log("72 JavaScript decisions matched the archived Python gate.")
'
import json
from itertools import product
import sys

sys.path.insert(0, "evaluation/ppc-live/2026-11-24/original/v02/ppc_package")
from run import CASES, gate

rows = []
for case, decision, acknowledged in product(CASES, ("ACCEPT", "REFUSE"), (True, False)):
    proposal = {"decision": decision, "acknowledged": acknowledged}
    eligibility = case["evidence"]
    rows.append([case["id"], proposal, eligibility, gate(proposal, eligibility)])

malformed = [
    None, [], {}, {"decision": "ACCEPT"}, {"decision": "ACCEPT", "acknowledged": 1},
    {"decision": "ACCEPT", "acknowledged": True, "override": True},
    {"decision": "ALLOW", "acknowledged": True},
    {"decision": "REFUSE", "acknowledged": "false"},
]
for i, proposal in enumerate(malformed):
    rows.append([f"malformed-{i}", proposal, True, gate(proposal, True)])

proposal = {"decision": "ACCEPT", "acknowledged": False}
for i, eligibility in enumerate((True, False, 1, 0, "true", None, {}, [])):
    rows.append([f"eligibility-{i}", proposal, eligibility, gate(proposal, eligibility)])
print(json.dumps(rows))
PY
