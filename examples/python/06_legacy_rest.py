#!/usr/bin/env python3
"""Example 06 - Legacy cookie REST (web-client bootstrap).

Logs in over JSON-RPC (to get the session cookie), then calls the cookie-only
config endpoints the web/mobile client uses during startup.

Usage:
    export UNTIS_SERVER=mese
    export UNTIS_SCHOOL=demo-school
    export UNTIS_USER=demo
    export UNTIS_PASSWORD=demo
    python3 examples/python/06_legacy_rest.py

See docs/08-legacy-rest.md.
"""

from lib import Session, jsonrpc, need, pretty, server_base


def main():
    base = server_base()
    school = need("UNTIS_SCHOOL")
    session = Session()

    # 1. authenticate (public JSON-RPC) to obtain a JSESSIONID cookie.
    status, data, _ = jsonrpc(
        session,
        f"{base}/WebUntis/jsonrpc.do?school={school}",
        "authenticate",
        {
            "user": need("UNTIS_USER"),
            "password": need("UNTIS_PASSWORD"),
            "client": "webuntis-apis-examples",
        },
    )
    print(f"# authenticate -> HTTP {status}")

    # 2. cookie-only config endpoints.
    for path in ("/WebUntis/api/app/config", "/WebUntis/api/daytimetable/config"):
        status, data, _ = session.request(base + path)
        print(f"\n# GET {path} -> HTTP {status}")
        print(pretty(data)[:1500])


if __name__ == "__main__":
    main()
