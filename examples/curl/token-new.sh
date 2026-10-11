#!/usr/bin/env bash
# Mint a JWT from a cookie session (plain-text response body).
#
#   export UNTIS_SERVER=mese UNTIS_SCHOOL=demo-school
#   export UNTIS_USER=demo UNTIS_PASSWORD=demo
#   ./examples/curl/token-new.sh
#
# See docs/02-authentication.md (section 2.2) and docs/06-mobile-rest-auth.md.
set -euo pipefail

: "${UNTIS_SERVER:?set UNTIS_SERVER}"
: "${UNTIS_SCHOOL:?set UNTIS_SCHOOL}"
: "${UNTIS_USER:?set UNTIS_USER}"
: "${UNTIS_PASSWORD:?set UNTIS_PASSWORD}"

base="https://${UNTIS_SERVER}.webuntis.com"
jar="$(mktemp)"
trap 'rm -f "$jar"' EXIT

echo "# authenticate (stores the JSESSIONID cookie)"
curl -sS -c "$jar" -b "$jar" -H 'Content-Type: application/json' \
  -d "{\"id\":\"1\",\"method\":\"authenticate\",\"params\":{\"user\":\"${UNTIS_USER}\",\"password\":\"${UNTIS_PASSWORD}\",\"client\":\"curl-example\"},\"jsonrpc\":\"2.0\"}" \
  "${base}/WebUntis/jsonrpc.do?school=${UNTIS_SCHOOL}" >/dev/null

echo "# GET /WebUntis/api/token/new"
curl -sS -b "$jar" -H 'Accept: text/plain' "${base}/WebUntis/api/token/new"
echo
