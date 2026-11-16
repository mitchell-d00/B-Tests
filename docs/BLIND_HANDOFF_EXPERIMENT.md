# Compression, smoothing and work-transfer experiment

The [neutral entry](../blind/START.md) is intended for an AI encountering an assigned
run for the first time. Targets receive only their current packet. Private outcome
keys, condition mapping, scores and future corrections stay outside exported
packets. This is target-answer concealment, not a claim of double-blind research.
Instruction wording can reveal a treatment; operators know the protocol; public
readers may browse elsewhere. Independent reviewers and secure remote allocation
have not been supplied.

Seven synthetic case families test provenance loss, dropped qualifications,
failed work becoming success, resurrection of a rejected edge, stale completion
after transfer, scientific authority surviving a downgrade to metaphor, and a
legitimate authorized positive control. Each family has matched CAD and ordinary
governance arms with identical source identities and bytes. Order is randomized
before requests. Four fresh-session stages use handoff budgets of 2,200, 1,400,
900 and 500 characters. A genuine source correction and permission revocation
arrive at stage 2; they are inaccessible before that stage.

Only the model's actual handoff text transfers. Its structured answer is scored
separately and is not secretly carried into the next session. A source catalogue
remains available so the successor can request originals and recover lost reasons.
The experiment records these read requests and content hashes. This separates
preserved evidence from evidence that can be recovered after loss. Source identity
retention alone does not prove that the correct justification survived.

The evaluator checks current facts, original failure outcomes, qualifications,
rejected relations, task status, citations and local action selection. It persists
the submitted state and action requests before reopening and checking them.
Wrong action requests are not blocked by a hidden truth guard. This is a local
decision/effect test, not Ben's native permission infrastructure.

## Run evaluator controls

```sh
python -m unittest discover -s tests -v
python -m research_lab.blind_handoff controls --root /tmp/new-handoff-controls
```

The 126 scripted fault injections are explicitly **harness controls**. They test
whether planted compression, smoothing and transfer errors are detected; they are
never labeled live AI outputs or OOCC failures. Real file transfers are exercised
by persisting a submission and reopening the next packet.

## Prepare answer-hidden packets

```sh
python -m research_lab.blind_handoff prepare \
  --root evaluation/blind-private-runs/new-study --trials 1
```

The root must not exist. Give each fresh AI only ONE exported directory under
`packets/`. Do not expose `private/` or the complete entry index to a target.
Keep the root local: those paths are ignored by Git. Preparation freezes a private
oracle hash and treatment hashes before any target answer. These are newly
generated development tasks, not independently authored holdouts.

For an API endpoint:

```sh
python -m research_lab.blind_handoff run \
  --root evaluation/blind-private-runs/new-study \
  --key-env OPENAI_API_KEY --endpoint https://api.openai.com/v1/chat/completions \
  --model YOUR_MODEL --max-requests 12
```

Every new stage starts a new messages array. Source-read rounds stay within that
stage; they are logged. Requests, raw responses, provider receipts and source
readbacks remain available. Unusable transport stops further network attempts;
unstarted and dependent stages become `NOT_RUN`. A response-format failure affects
that chain rather than silently suppressing the other condition.

## Run manually in fresh chats

If the endpoint is unavailable, give an assigned packet to a fresh chat without
this repository's evaluation discussion. When it requests source IDs, run:

```sh
python -m research_lab.blind_handoff read --root YOUR_STUDY \
  --packet PACKET_ID --source REQUESTED_ID
```

Supply the returned bodies. Save the model's final JSON and the actual session
transcript, then submit them:

```sh
python -m research_lab.blind_handoff submit --root YOUR_STUDY \
  --packet PACKET_ID --response response.json --transcript transcript.txt
```

The evaluator returns the next entry path. Transfer only that new packet to a new
session. Do not show the next model the previous score. A transcript hash identifies
the supplied record; it does not authenticate the provider, prove a fresh session,
or establish independent human review. Missing transcripts cannot be represented
as independently verified model executions.

## Interpretation

Report first loss of a required fact, source identity, qualification, rejected edge
or failure outcome separately from wrong confident assertions and unauthorized
action selection. An honest unknown is information loss, not hallucination. A
budget violation means fidelity at that compression level was not established.
Report coverage on the positive control so universal refusal cannot appear robust.

Ben's Artificial Tangibility paper proposes re-entry, failure-recovery and weight
tests in physical PDF pages 14–16. CAD page 7 disclaims factual guarantees.
No More First Dates pages 439–445 describe a reader-owned setup and a genuinely
new-session handoff. The glossary page 2 permits category downgrades; the test
checks that a downgrade removes scientific/operational authority rather than
merely changing its label. These are source-linked instruction tests, not a
reproduction of Ben's inaccessible live cloud system.

Both useful corrections and failures count. Human review time, token usage,
latency and operator interventions must be retained when observed. Blinded
semantic review and live system access remain separate requirements.
