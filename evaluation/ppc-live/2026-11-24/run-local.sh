#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -lt 3 ] || [ "$#" -gt 4 ]; then
    echo "Usage: $0 ASSET_DIRECTORY PPC_V02_DIRECTORY NEW_OUTPUT_DIRECTORY [PORT]" >&2
    exit 2
fi
here=$(cd "$(dirname "$0")" && pwd)
assets=$(realpath "$1")
package=$(realpath "$2")
out=$(realpath -m "$3")
port=${4:-53294}
server="$assets/llama-b12622/llama-server"
weights="$assets/qwen.gguf"
printf '%s  %s\n' \
    18e8fe023e66cc9f7d6ab6b32af0cf6b662f58a70d975029eefc9bca166d16c1 "$server" \
    6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e "$weights" |
    sha256sum -c
(cd "$package" && sha256sum -c SHA256SUMS)
mkdir "$out"
"$server" --version >"$out/runtime-version.txt" 2>&1
"$server" --model "$weights" --alias qwen2.5-1.5b --host 127.0.0.1 --port "$port" \
    --ctx-size 4096 --threads 4 --parallel 4 --gpu-layers 0 --no-webui >"$out/server.log" 2>&1 &
server_pid=$!
cleanup() {
    kill "$server_pid" 2>/dev/null || true
    local server_exit=0
    wait "$server_pid" || server_exit=$?
    printf '%s\n' "$server_exit" >"$out/server-exit.txt"
}
trap cleanup EXIT
for ((i = 0; i < 60; i++)); do
    kill -0 "$server_pid"
    if curl --noproxy '*' -fsS "http://127.0.0.1:$port/health" >"$out/health.json" 2>/dev/null; then
        break
    fi
    sleep 1
done
curl --noproxy '*' -fsS "http://127.0.0.1:$port/health" >"$out/health.json"
NO_PROXY=127.0.0.1 no_proxy=127.0.0.1 python -B "$here/live.py" --package "$package" \
    --out "$out/live" --endpoint "http://127.0.0.1:$port/v1/chat/completions" \
    --model qwen2.5-1.5b >"$out/live.stdout" 2>"$out/live.stderr"
python -B "$here/score.py" --package "$package" --frozen "$out/live/frozen.json" \
    --traces "$out/live/trials.jsonl" --out "$out/scored"
