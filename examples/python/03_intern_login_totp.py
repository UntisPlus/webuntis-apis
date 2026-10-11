#!/usr/bin/env python3
"""Example 03 - Internal JSON-RPC login with TOTP or anonymous access.

Demonstrates the `jsonrpc_intern.do` endpoint the official Untis Mobile app
uses. Logs in with either a QR-code TOTP secret or anonymous access, then
fetches a timetable via `getTimetable2017`.

Usage (TOTP):
    export UNTIS_SERVER=mese
    export UNTIS_SCHOOL=demo-school
    export UNTIS_USER=<username>
    export UNTIS_SECRET=<qr-code-secret>     # from the web UI "show QR-code"
    python3 examples/python/03_intern_login_totp.py CLASS 123

Anonymous (public timetable schools):
    export UNTIS_ANONYMOUS=1
    python3 examples/python/03_intern_login_totp.py

See docs/05-jsonrpc-intern.md.
"""

import sys
import time

from lib import Session, need, jsonrpc, opt, pretty, server_base, totp

INTERN = "/WebUntis/jsonrpc_intern.do"


def main():
    base = server_base()
    school = need("UNTIS_SCHOOL")
    session = Session()

    if opt("UNTIS_ANONYMOUS"):
        user, otp = "#anonymous#", "100170"
    else:
        user = need("UNTIS_USER")
        otp = totp(need("UNTIS_SECRET"))

    auth = {"clientTime": int(time.time() * 1000), "user": user, "otp": otp}
    url = f"{base}/WebUntis/jsonrpc_intern.do?m=getUserData2017&school={school}&v=i2.2"
    status, data, _ = jsonrpc(
        session,
        url,
        "getUserData2017",
        [{"auth": auth}],
    )
    print(f"# login -> HTTP {status}")
    if isinstance(data, dict) and data.get("error"):
        sys.exit(f"login failed: {pretty(data['error'])}")
    print(pretty((data or {}).get("result", data))[:1200])

    # Optionally fetch a timetable. UNTIS_ELEMENT_TYPE is one of
    # STUDENT|CLASS|TEACHER|SUBJECT|ROOM.
    element_id = opt("UNTIS_ELEMENT_ID")
    if not element_id:
        print("# set UNTIS_ELEMENT_ID (+ UNTIS_ELEMENT_TYPE) to fetch a timetable")
        return

    element_type = opt("UNTIS_ELEMENT_TYPE", "CLASS")
    tt_url = f"{base}/WebUntis/jsonrpc_intern.do?m=getTimetable2017&school={school}&v=i2.2"
    status, tt, _ = jsonrpc(
        session,
        tt_url,
        "getTimetable2017",
        [
            {
                "auth": auth,
                "id": int(element_id),
                "type": element_type,
                "startDate": opt("UNTIS_START", "2026-10-05"),
                "endDate": opt("UNTIS_END", "2026-10-11"),
                "masterDataTimestamp": 0,
                "timetableTimestamp": 0,
                "timetableTimestamps": [0] * 7,
            }
        ],
    )
    print(f"# getTimetable2017 -> HTTP {status}")
    print(pretty(tt)[:2000])


if __name__ == "__main__":
    main()
