# Next-instance handoff — v0.2

1. Unzip and enter `ppc_package`; run `sha256sum -c SHA256SUMS` before modifying anything.
2. Review README.md, cases.json, run.py, stress.py, and paper Appendix A. Preserve all prior result files and evidence.
3. Rerun unit tests and fixture/stress scripts, saving new versioned results. Fixture repeats are not fresh model observations.
4. Highest-priority outstanding experiment: obtain an explicitly authorized OpenAI-compatible endpoint and model; use README live command with 30 repeats and save raw outputs. Do not substitute authored outputs or same-context assistant judgments for independent API calls. Keep invalid results and errors. Independently assess correction acknowledgment and semantic fidelity.
5. Obtain native executable systems and complete original chat separately; do not treat supplied logs as reruns. Keep native and model status NOT_RUN until actual execution.
6. Update paper Markdown, PDF and text together, document limitations and version changes, refresh checksums, and return a full ZIP. Do not claim publication approval or empirical superiority from fixture data.

v0.2 decisions: 30 fixture repeats, original seed 42, new stress seed 20261124, append-only paper update, no remote transmission. Live endpoint and native source unavailable. Original paper remains attributed to its named author; additions are AI-assisted and pending review.
