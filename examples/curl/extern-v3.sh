#!/usr/bin/env bash
# External Timetable API v3 (official).
#
#   export UNTIS_API_URL=https://api.webuntis.com
#   export UNTIS_API_TOKEN=<bearer token>
#   export UNTIS_CLASS=123
#   ./examples/curl/extern-v3.sh
#
# See docs/09-extern-timetable-v3.md.
set -euo pipefail

: "${UNTIS_API_TOKEN:?set UNTIS_API_TOKEN (see examples/python/08_platform_oauth.py)}"
api="${UNTIS_API_URL:-https://api.webuntis.com}"
api="${api%/}"

start="${UNTIS_START:-2026-10-05T00:00:00}"
end="${UNTIS_END:-2026-10-11T00:00:00}"
filter=""
if [[ -n "${UNTIS_CLASS:-}" ]]; then
  filter="&class=${UNTIS_CLASS}"
elif [[ -n "${UNTIS_DATE_LAST_MODIFIED_AFTER:-}" ]]; then
  filter="&dateLastModifiedAfter=${UNTIS_DATE_LAST_MODIFIED_AFTER}"
else
  echo "set UNTIS_CLASS or UNTIS_DATE_LAST_MODIFIED_AFTER" >&2
  exit 1
fi

auth_hdr=(-H "Authorization: Bearer ${UNTIS_API_TOKEN}" -H 'Accept: application/json')
[[ -n "${UNTIS_TENANT:-}" ]] && auth_hdr+=(-H "Tenant-Id: ${UNTIS_TENANT}")

url="${api}/WebUntis/api/rest/extern/v3/timetable?start=${start}&end=${end}&limit=0&offset=0&includeStudents=false${filter}"
echo "# GET ${url}"
curl -sS "${auth_hdr[@]}" "$url" | { if command -v jq >/dev/null 2>&1; then jq '{version, periods: (.timetableData.periods|length), first: .timetableData.periods[0]}'; else cat; fi; }
