#!/usr/bin/env bash
# Example - Public JSON-RPC with curl: authenticate, getKlassen, logout.
#
#   export UNTIS_SERVER=mese UNTIS_SCHOOL=demo-school
#   export UNTIS_USER=demo UNTIS_PASSWORD=demo
#   ./examples/curl/public-jsonrpc.sh
#
# See docs/04-jsonrpc-public.md.
set -euo pipefail

: "${UNTIS_SERVER:?set UNTIS_SERVER}"
: "${UNTIS_SCHOOL:?set UNTIS_SCHOOL}"
: "${UNTIS_USER:?set UNTIS_USER}"
: "${UNTIS_PASSWORD:?set UNTIS_PASSWORD}"

base="https://${UNTIS_SERVER}.webuntis.com"
url="${base}/WebUntis/jsonrpc.do?school=${UNTIS_SCHOOL}"
jar="$(mktemp)"
trap 'rm -f "$jar"' EXIT

pretty() { if command -v jq >/dev/null 2>&1; then jq .; else cat; fi; }

echo "# authenticate"
curl -sS -c "$jar" -b "$jar" -H 'Content-Type: application/json' \
  -d "{\"id\":\"1\",\"method\":\"authenticate\",\"params\":{\"user\":\"${UNTIS_USER}\",\"password\":\"${UNTIS_PASSWORD}\",\"client\":\"curl-example\"},\"jsonrpc\":\"2.0\"}" \
  "$url" | pretty

echo "# getKlassen"
curl -sS -c "$jar" -b "$jar" -H 'Content-Type: application/json' \
  -d '{"id":"2","method":"getKlassen","params":{},"jsonrpc":"2.0"}' \
  "$url" | pretty

echo "# logout"
curl -sS -c "$jar" -b "$jar" -H 'Content-Type: application/json' \
  -d '{"id":"3","method":"logout","params":{},"jsonrpc":"2.0"}' \
  "$url" | pretty
