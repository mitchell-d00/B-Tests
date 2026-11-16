"""Real GitHub Models chat adapter for paired B-Tests.

Input: a single request JSON object from side_by_side.run on stdin.
Output: a single normalized response JSON object on stdout.
All API errors go to stderr with nonzero status; never fabricate an AI reply.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ENDPOINT = "https://models.github.ai/inference/chat/completions"


def call(request: dict, *, model: str, timeout: int = 55) -> dict:
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN not configured (requires models:read)")
    if request.get("schema") != "btests-model-input-1":
        raise ValueError("Unexpected model request schema")
    system = request["system"]
    user = request["user"]
    content = user + "\n\nReturn only the requested JSON object. No Markdown fences or text outside JSON."
    payload = {"model": model, "messages": [{"role": "system", "content": system},
                                              {"role": "user", "content": content}],
               "temperature": 0, "max_tokens": 550}
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = Request(ENDPOINT, data=data, method="POST",
                  headers={"Authorization": "Bearer " + token,
                           "Content-Type": "application/json", "Accept": "application/json"})
    failure = None
    for attempt in range(3):
        try:
            with urlopen(req, timeout=timeout) as resp:
                response = json.loads(resp.read(400_000).decode("utf-8"))
            break
        except HTTPError as e:
            failure = "GitHub Models HTTP " + str(e.code)
            if e.code not in (429, 500, 502, 503) or attempt >= 2:
                raise RuntimeError(failure) from None
            time.sleep(5 * (attempt + 1))
        except URLError as e:
            raise RuntimeError("GitHub Models network unavailable") from e
    else:
        raise RuntimeError(failure or "GitHub Models transport unavailable")
    content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
    if not isinstance(content, str):
        raise ValueError("No text output in model response")
    compact = content.strip()
    # Accept exact JSON; reject a model that cannot return the requested response contract.
    if compact.startswith("```"):
        compact = re.sub(r"^```(?:json)?\s*|\s*```$", "", compact, flags=re.IGNORECASE).strip()
    try:
        result = json.loads(compact)
    except ValueError:
        raise ValueError("Model did not produce parseable JSON: " + compact[:300])
    if not isinstance(result, dict):
        raise ValueError("Model output is not a JSON object")
    result["_model_metadata"] = {"provider": "GitHub Models", "requested_model": model,
                                 "returned_model": response.get("model"),
                                 "usage": response.get("usage"),
                                 "finish_reason": response.get("choices", [{}])[0].get("finish_reason")}
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="openai/gpt-4.1-mini")
    args = parser.parse_args(argv)
    try:
        request = json.load(sys.stdin)
        result = call(request, model=args.model)
        json.dump(result, sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")
        return 0
    except (ValueError, RuntimeError, KeyError) as exc:
        print("ADAPTER_ERROR: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
