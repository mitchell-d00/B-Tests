# Author clarification: the Section 19 ZIP is a test-design scaffold

Mitchell D. McPhetridge clarified on20November2026 that the old ZIP was the
structure he built to think through ways to test OOCC and MPLPB. The scripted
conditions illustrate possible evaluator roles, planted cases, detection and
false-alarm calculations. They are not a claimed invocation of Gelhaus's native
controller or the native MPLPB executor.

The original ZIP is preserved unchanged at
[supplied/witness-section19-experiments.zip](supplied/witness-section19-experiments.zip),
SHA-256 `0322c429a214752d25b3ede08567a8f76d2a8ed894a10fdd23f742f96ca1d395`.
The revised Witness PDF supplied again on20November is byte-identical to the
[existing revised paper](../../docs/paper/THE_WITNESS_INSIDE_THE_MACHINE_REVISED.pdf),
SHA-256 `b21e7d8a37c215ceaa4189c754810c331ea1823408225e248b1aa1064e56391b`.
Its Section19 is an experimental design with proposed evaluator conditions and
separate detection and false-alarm measures.

The [prior replication audit](RESULTS.md) retains what the old scripts actually
do, their historical README wording, and the separately executed filesystem and
native tests. This clarification does not rewrite those scripts, reported values
or retained outputs. It prevents the design artifact from being mistaken for an
empirical comparison, or its limited scope from being used to erase the later
real tests. Repeated ZIP copies, a revised paper, design controls and target
executions are different evidence units.

The new [Testing OOCC paper](../../docs/paper/TESTING_OOCC.md) incorporates this
clarification and credits the design contribution explicitly. No global winner
or native OOCC result is inferred from the scaffold.
