#!/usr/bin/env python3
"""Example 07 - External Timetable API v3 (official).

Fetches a class timetable from `/WebUntis/api/rest/extern/v3/timetable`.

Authentication uses the Untis Platform OAuth2 bearer token (or a legacy API
key). This example takes a ready-made token from the environment.

Usage:
    export UNTIS_API_URL=https://api.webuntis.com      # or https://<server>.webuntis.com
    export UNTIS_API_TOKEN=<bearer token>
    export UNTIS_TENANT=1004400
    export UNTIS_CLASS=123
    export UNTIS_START=2026-10-05T00:00:00
    export UNTIS_END=2026-10-11T00:00:00
    python3 examples/python/07_extern_timetable.py

See docs/09-extern-timetable-v3.md and 08_platform_oauth.py (which can mint
UNTIS_API_TOKEN).
"""

from urllib.parse import urlencode

from lib import Session, opt, pretty


def main():
    api = opt("UNTIS_API_URL", "https://api.webuntis.com").rstrip("/")
    token = opt("UNTIS_API_TOKEN")
    if not token:
        print("# UNTIS_API_TOKEN is not set - run 08_platform_oauth.py first, or paste a token")
        return

    query = {
        "start": opt("UNTIS_START", "2026-10-05T00:00:00"),
        "end": opt("UNTIS_END", "2026-10-11T00:00:00"),
        "limit": opt("UNTIS_LIMIT", "0"),
        "offset": opt("UNTIS_OFFSET", "0"),
        "includeStudents": "false",
    }
    if opt("UNTIS_CLASS"):
        query["class"] = opt("UNTIS_CLASS")
    elif opt("UNTIS_DATE_LAST_MODIFIED_AFTER"):
        query["dateLastModifiedAfter"] = opt("UNTIS_DATE_LAST_MODIFIED_AFTER")
    else:
        print("# set UNTIS_CLASS (or UNTIS_DATE_LAST_MODIFIED_AFTER) to filter")
        return

    url = f"{api}/WebUntis/api/rest/extern/v3/timetable?{urlencode(query)}"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    if opt("UNTIS_TENANT"):
        headers["Tenant-Id"] = opt("UNTIS_TENANT")

    status, data, _ = Session().request(url, headers=headers)
    print(f"# GET {url} -> HTTP {status}")
    if not isinstance(data, dict) or "timetableData" not in data:
        print(pretty(data)[:2000])
        return

    master = data.get("masterData", {})
    periods = data.get("timetableData", {}).get("periods", [])
    print(f"# version={data.get('version')} periods={len(periods)}")
    for kind in ("classes", "teachers", "rooms", "subjects"):
        print(f"#   {kind}: {len(master.get(kind, []) or [])}")
    for period in periods[:5]:
        print(pretty(period))


if __name__ == "__main__":
    main()
