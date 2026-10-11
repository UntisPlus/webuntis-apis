#!/usr/bin/env python3
"""Example 05 - "View" REST API with a JWT.

Calls a couple of endpoints from `api/rest/view/v1`.

Usage:
    export UNTIS_SERVER=mese
    export UNTIS_SCHOOL=demo-school
    export UNTIS_JWT=<jwt>              # from 04_mobile_jwt.py
    export UNTIS_TENANT=1004400         # optional, if the server requires it
    python3 examples/python/05_view_rest.py
    python3 examples/python/05_view_rest.py timetable 123   # class id 123

See docs/07-rest-view.md.
"""

import sys

from lib import Session, need, opt, pretty, server_base


def headers():
    h = {"Accept": "application/json, text/plain, */*"}
    jwt = need("UNTIS_JWT")
    h["Authorization"] = f"Bearer {jwt}"
    if opt("UNTIS_TENANT"):
        h["Tenant-Id"] = opt("UNTIS_TENANT")
    if opt("UNTIS_SCHOOL_YEAR"):
        h["X-Webuntis-Api-School-Year-Id"] = opt("UNTIS_SCHOOL_YEAR")
    return h


def main():
    base = server_base()
    school = need("UNTIS_SCHOOL")
    session = Session()

    what = sys.argv[1] if len(sys.argv) > 1 else "mobile"
    if what == "timetable" and len(sys.argv) > 2:
        path = (
            f"/WebUntis/api/rest/view/v1/timetable/entries"
            f"?start={opt('UNTIS_START', '2026-10-05')}"
            f"&end={opt('UNTIS_END', '2026-10-11')}"
            f"&format=1&resourceType=CLASS&resources={sys.argv[2]}"
            f"&periodTypes=&timetableType=STANDARD&layout=START_TIME"
        )
    else:
        path = "/WebUntis/api/rest/view/v1/mobile/data"

    url = base + path
    status, data, _ = session.request(url, headers=headers())
    print(f"# GET {url} -> HTTP {status}")
    print(pretty(data)[:3000])


if __name__ == "__main__":
    main()
