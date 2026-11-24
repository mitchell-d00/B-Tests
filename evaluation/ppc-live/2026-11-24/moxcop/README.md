# Mox Cult of Personality (MoxCOP)

MoxCOP generates a frozen schedule of separate language-model inference trials and verifies the recorded request histories and provider responses. Each trial can contain one or more user turns. Python 3.10+ and a Chat Completions endpoint are required for live calls. Verification runs offline with the standard library.

```sh
python moxcop.py freeze example.json example-plan.json
python moxcop.py run example-plan.json example-run \
  --endpoint http://127.0.0.1:53294/v1/chat/completions --workers 2
python moxcop.py verify example-run
```

Start the local runtime separately or choose an authorized compatible endpoint. `MODEL_API_KEY` is optional. The program sends it as a header and keeps headers out of its trace. The trace retains the prompt and model response body, so use inputs you can retain and share. The schedule seed controls order. Sampling is controlled by the endpoint.

## How trial separation is established

- The frozen plan defines trial IDs, repeats, prompts, turn order, model name and sampling settings. Its digest is recorded before the first model call.
- Each trial starts a new in-memory message list. Its initial request contains only that trial’s system prompt and first user turn. Later calls carry forward only responses from that trial. The client sends no conversation or state identifiers.
- Each turn sends its own HTTP request and records the actual response body, HTTP status and timing. Offline verification reconstructs the expected message history and rejects altered histories, out-of-order trials and reused provider response IDs. Failed calls and missing trials count as incomplete.
- This establishes separation at the application and request levels. Separate requests can use the same server, model weights, random number source and prefix cache. Provider IDs alone cannot prove internal process isolation, provider statelessness, cryptographic authenticity or statistical independence. Different trials can legitimately return identical text.

## How this relates to the 30-repeat PPC experiment

The original v0.2 fixture repeats replayed authored responses. The fresh PPC instance used the frozen v0.2 prompts with independent request histories for each A and B case, logged the provider response envelopes and independently checked them using the PPC scorer. Each correction reply stayed within its own trial. C reused the exact B proposal and made zero model calls. See [the run report](../README.md), [frozen schedule](../live/frozen.json) and [reproduction instructions](../REPRODUCTION.md). MoxCOP turns the same trial-separation checks into a reusable tool. Its example is a separate smoke run.

## Earlier 30-session B-Tests comparison

The earlier governance-prompt comparison counted 30 fresh target sessions across five conditions (16 + 2 + 4 + 6 + 2). Session separation was procedural. Separate targets received assigned inputs, and a later stage in a trajectory received the saved state and handoff as deliberate input. These stages are dependent observations. The archive has normalized responses and checks, including a file-access monitor for the discovery condition. It has no provider response IDs or complete API transcripts to retroactively verify those 30 sessions with MoxCOP. See the [comparison scope](https://github.com/mitchell-d00/B-Tests/blob/e646f82e4758e35e7a883eb492bcf756a8d29c83/docs/COMPARISON_SCOPE.md).
