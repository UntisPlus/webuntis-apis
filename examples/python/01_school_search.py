#!/usr/bin/env python3
"""Example 01 - School discovery via `searchSchool`.

Finds the tenant server and login name for a school by name.

Usage:
    python3 examples/python/01_school_search.py "Gymnasium"

Requires: nothing (public endpoint).
"""

import sys

from lib import Session, jsonrpc, pretty

HOSTS = [
    "https://schoolsearch.webuntis.com/schoolquery2",
    "https://mobile.webuntis.com/ms/schoolquery2/?v=a4.2.10",
]


def main():
    query = " ".join(sys.argv[1:]).strip()
    if not query:
        sys.exit('usage: 01_school_search.py "<school name>"')

    for host in HOSTS:
        session = Session()
        status, data, _ = jsonrpc(
            session, host, "searchSchool", [{"schoolid": 0, "search": query}]
        )
        print(f"# GET {host} -> HTTP {status}")
        if isinstance(data, dict) and data.get("result"):
            schools = data["result"].get("schools", [])
            print(f"# {len(schools)} school(s) found")
            for school in schools:
                print(pretty(school))
            return
        print(pretty(data))
    print("# no schools returned by any known search host")


if __name__ == "__main__":
    main()
