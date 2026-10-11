#!/usr/bin/env python3
"""Example 08 - Untis Platform API: OAuth2 client credentials.

Exchanges a client id + platform-generated password for a short-lived bearer
token, then (optionally) calls a resource.

Usage:
    export UNTIS_API_URL=https://api.webuntis.com
    export UNTIS_TENANT=1004400
    export UNTIS_CLIENT_ID=<client id>
    export UNTIS_CLIENT_SECRET=<platform-generated password>
    python3 examples/python/08_platform_oauth.py

The printed token can be reused as UNTIS_API_TOKEN for 07_extern_timetable.py.

See docs/10-platform-api.md.
"""

import base64
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

from lib import opt


def get_token(api, tenant, client_id, client_secret):
    url = f"{api}/WebUntis/api/sso/v3/{tenant}/token"
    basic = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    body = urllib.parse.urlencode({"grant_type": "client_credentials"}).encode()
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Basic {basic}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as err:
        return err.code, err.read().decode(errors="replace")


def main():
    api = opt("UNTIS_API_URL", "https://api.webuntis.com").rstrip("/")
    tenant = opt("UNTIS_TENANT")
    client_id = opt("UNTIS_CLIENT_ID")
    client_secret = opt("UNTIS_CLIENT_SECRET")
    if not all((tenant, client_id, client_secret)):
        sys.exit(
            "error: set UNTIS_TENANT, UNTIS_CLIENT_ID and UNTIS_CLIENT_SECRET\n"
            "       (see examples/.env.example)"
        )

    status, data = get_token(api, tenant, client_id, client_secret)
    print(f"# POST {api}/WebUntis/api/sso/v3/{tenant}/token -> HTTP {status}")
    if not isinstance(data, dict) or "access_token" not in data:
        print(data)
        return

    print(f"# token_type={data.get('token_type')} expires_in={data.get('expires_in')}s")
    print(f"# access_token={data['access_token'][:50]}...")
    print()
    print(f"export UNTIS_API_TOKEN={data['access_token']}")


if __name__ == "__main__":
    main()
