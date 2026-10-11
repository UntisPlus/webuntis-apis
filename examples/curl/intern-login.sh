#!/usr/bin/env bash
# Internal JSON-RPC login (anonymous) + a timetable call.
#
# Anonymous login only works for schools that publish a public timetable.
#
#   export UNTIS_SERVER=mese
#   export UNTIS_SCHOOL=demo-school
#   export UNTIS_ELEMENT_ID=123      # optional; enables the timetable call
#   export UNTIS_ELEMENT_TYPE=CLASS
#   ./examples/curl/intern-login.sh
#
# See docs/05-jsonrpc-intern.md.
set -euo pipefail

: "${UNTIS_SERVER:?set UNTIS_SERVER}"
: "${UNTIS_SCHOOL:?set UNTIS_SCHOOL}"

base="https://${UNTIS_SERVER}.webuntis.com"
jar="$(mktemp)"
trap 'rm -f "$jar"' EXIT
pretty() { if command -v jq >/dev/null 2>&1; then jq .; else cat; fi; }

now_ms="$(date +%s%3N)"
auth="{\"clientTime\":${now_ms},\"user\":\"#anonymous#\",\"otp\":\"100170\"}"

echo "# login (getUserData2017)"
curl -sS -c "$jar" -b "$jar" -H 'Content-Type: application/json' \
  -d "{\"id\":\"untis-mobile-android\",\"jsonrpc\":\"2.0\",\"method\":\"getUserData2017\",\"params\":[{\"auth\":${auth}}]}" \
  "${base}/WebUntis/jsonrpc_intern.do?m=getUserData2017&school=${UNTIS_SCHOOL}&v=i2.2" | pretty

if [[ -n "${UNTIS_ELEMENT_ID:-}" ]]; then
  echo "# getTimetable2017"
  curl -sS -c "$jar" -b "$jar" -H 'Content-Type: application/json' \
    -d "{\"id\":\"untis-mobile-android\",\"jsonrpc\":\"2.0\",\"method\":\"getTimetable2017\",\"params\":[{\"auth\":${auth},\"id\":${UNTIS_ELEMENT_ID},\"type\":\"${UNTIS_ELEMENT_TYPE:-CLASS}\",\"startDate\":\"${UNTIS_START:-2026-10-05}\",\"endDate\":\"${UNTIS_END:-2026-10-11}\",\"masterDataTimestamp\":0,\"timetableTimestamp\":0,\"timetableTimestamps\":[0,0,0,0,0,0,0]}]}" \
    "${base}/WebUntis/jsonrpc_intern.do?m=getTimetable2017&school=${UNTIS_SCHOOL}&v=i2.2" | pretty
fi
