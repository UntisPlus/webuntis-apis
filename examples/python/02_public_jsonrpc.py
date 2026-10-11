#!/usr/bin/env python3
"""Example 02 - Public JSON-RPC API (official 2018 spec).

Logs in with username/password, then fetches classes, rooms, and a timetable.

Usage:
    export UNTIS_SERVER=mese
    export UNTIS_SCHOOL=demo-school
    export UNTIS_USER=demo
    export UNTIS_PASSWORD=demo
    python3 examples/python/02_public_jsonrpc.py

See docs/04-jsonrpc-public.md.
"""

import sys

from lib import Session, need, jsonrpc, opt, pretty, server_base


def main():
    base = server_base()
    school = need("UNTIS_SCHOOL")
    user = need("UNTIS_USER")
    password = need("UNTIS_PASSWORD")
    url = f"{base}/WebUntis/jsonrpc.do?school={school}"
    session = Session()

    # 1. authenticate -> sets the JSESSIONID cookie
    status, data, _ = jsonrpc(
        session,
        url,
        "authenticate",
        {"user": user, "password": password, "client": "webuntis-apis-example"},
    )
    print(f"# authenticate -> HTTP {status}")
    if not isinstance(data, dict) or "result" not in data:
        print(pretty(data))
        sys.exit("login failed")
    result = data["result"]
    print(f"# sessionId={result.get('sessionId')} personType={data['result'].get('personType')}")

    # 2. master data
    _, klassen, _ = jsonrpc(session, url, "getKlassen", {})
    classes = klassen.get("result", []) if isinstance(klassen, dict) else []
    print(f"\n# {len(classes)} classes; first three:")
    for klasse in classes[:3]:
        print(pretty(klasse))

    # 2b. rooms and teachers
    _, rooms, _ = jsonrpc(session, url, "getRooms", {})
    _, teachers, _ = jsonrpc(session, url, "getTeachers", {})
    print(f"# rooms={len(_count(rooms))} teachers={len(_count(teachers))}")

    # 3. timetable for the first class over a week
    if classes:
        class_id = classes[0]["id"]
        _, tt, _ = jsonrpc(
            session,
            url,
            "getTimetable",
            {
                "element": {"id": class_id, "type": 1, "keyType": "id"},
                "startDate": int(opt("UNTIS_START", "20261005")),
                "endDate": int(opt("UNTIS_END", "20261011")),
            },
        )
        periods = tt.get("result", []) if isinstance(tt, dict) else []
        print(f"# {len(periods)} period(s) for class {class_id}")
        for period in periods[:5]:
            print(pretty(period))

    # 4. always log out
    jsonrpc(session, url, "logout", {})
    print("# logged out")


def _count(payload):
    if isinstance(payload, dict):
        return payload.get("result", []) or []
    return []


if __name__ == "__main__":
    main()
