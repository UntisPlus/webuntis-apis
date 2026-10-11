"""Shared helpers for the WebUntis / Untis API examples.

Pure Python 3 standard library — no dependencies.

Quick start:

    cp examples/.env.example examples/.env
    $EDITOR examples/.env
    set -a; . examples/.env; set +a
    python3 examples/python/01_school_search.py "Gymnasium"
"""

import base64
import hashlib
import hmac
import http.cookiejar
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

USER_AGENT = "webuntis-apis-examples/1.0"


def need(name):
    """Return a required environment variable or exit with a helpful message."""
    value = os.environ.get(name)
    if not value:
        sys.exit(
            f"error: environment variable {name} is not set.\n"
            f"       See examples/.env.example and `source examples/.env`."
        )
    return value


def opt(name, default=""):
    return os.environ.get(name, default)


def server_base(server=None):
    """Turn a tenant server name (e.g. 'mese') into its base URL."""
    server = server or need("UNTIS_SERVER")
    if server.startswith("http"):
        return server.rstrip("/")
    return f"https://{server}.webuntis.com"


def pretty(obj):
    if isinstance(obj, (bytes, bytearray)):
        obj = obj.decode(errors="replace")
    if isinstance(obj, str):
        return obj
    return json.dumps(obj, indent=2, ensure_ascii=False)


class Session:
    """A tiny cookie-aware HTTP client (persists JSESSIONID automatically)."""

    def __init__(self):
        self.jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.jar)
        )

    def request(self, url, data=None, headers=None, method=None):
        hdrs = {"User-Agent": USER_AGENT}
        if headers:
            hdrs.update(headers)
        body = None
        if data is not None:
            body = json.dumps(data).encode()
            hdrs.setdefault("Content-Type", "application/json")
        req = urllib.request.Request(url, data=body, headers=hdrs, method=method)
        try:
            with self.opener.open(req, timeout=30) as resp:
                return resp.status, decode_body(resp.read()), dict(resp.headers)
        except urllib.error.HTTPError as err:
            return err.code, decode_body(err.read()), dict(err.headers)


def decode_body(raw):
    try:
        return json.loads(raw)
    except Exception:
        return raw.decode(errors="replace")


def jsonrpc(session, url, method, params=None, call_id=1):
    """POST a JSON-RPC 2.0 request and return (status, payload, headers)."""
    payload = {"id": call_id, "method": method, "params": params or {}, "jsonrpc": "2.0"}
    return session.request(url, data=payload)


def totp(secret_b32, when=None):
    """RFC 6238 TOTP (SHA-1, 6 digits, 30 s) from a base32 secret."""
    secret_b32 = secret_b32.strip().replace(" ", "").upper()
    pad = "=" * ((8 - len(secret_b32) % 8) % 8)
    key = base64.b32decode(secret_b32 + pad)
    counter = int((when if when is not None else time.time()) // 30)
    digest = hmac.new(key, counter.to_bytes(8, "big"), hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    code = (int.from_bytes(digest[offset : offset + 4], "big") & 0x7FFFFFFF) % 1_000_000
    return f"{code:06d}"


def jwt_exp(token):
    """Return the `exp` claim (epoch seconds) of a JWT, or None."""
    try:
        part = token.split(".")[1]
        part += "=" * ((4 - len(part) % 4) % 4)
        return json.loads(base64.urlsafe_b64decode(part)).get("exp")
    except Exception:
        return None
