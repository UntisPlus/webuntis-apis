# 00 — Getting started

New to WebUntis or to this repo? Read this page first. It gives you the mental
model, a first working request, and a path through the rest of the docs.

Everything you need is inside this repository: the prose (`docs/`), the
machine-readable specs (`specs/`), runnable examples (`examples/`) and saved
payloads (`samples/`).

---

## 1. What is WebUntis?

**WebUntis** is a school information system made by **Untis GmbH**. A school
runs it and students, teachers and parents use it for timetables, substitutions
(cancellations), homework, absences and messaging. Each school lives on a
*tenant server* such as `mese.webuntis.com`.

There is no single global API. A "WebUntis API" is really one of several
surfaces, and this repo documents all of them:

| # | Surface | Who uses it | Auth | Trust |
|---|---|---|---|---|
| 1 | Public JSON-RPC | official integrations, simple scripts | cookie | 🟡 specified by Untis |
| 2 | Internal JSON-RPC | the official mobile apps | OTP → cookie | 🔴 reverse-engineered |
| 3 | Mobile auth v2 | mobile apps | password → JWT | 🔴 reverse-engineered |
| 4 | "View" REST | the web/mobile internals | JWT | 🔴 reverse-engineered |
| 5 | Legacy cookie REST | the web client | cookie | 🔴 reverse-engineered |
| 6 | External Timetable API | official partners | OAuth2 | 🟢 official |
| 7 | Platform API | official partners | OAuth2/OIDC | 🟢 official |

The trust column matters. 🟢/🟡 surfaces are stable and documented by Untis;
🔴 surfaces were figured out by the community from the apps and can change any
week. See [01 — Overview](01-overview.md) for the full picture.

## 2. The mental model

Two things trip up newcomers:

1. **You always talk to a school's server, not to a global one.**
   `https://<server>.webuntis.com`. You discover the `<server>` name with
   [school discovery](03-school-discovery.md).
2. **Most surfaces are session-based.** You first *authenticate* and get either
   a **cookie** (`JSESSIONID`) or a **JWT** (a signed token string). Every later
   request carries that credential. This is the same flow a browser uses.

```
discover server  →  authenticate  →  get cookie/token  →  call methods  →  logout
   (03)                (02)                 (02)             (04–10)
```

## 3. Your first request

You can try the whole flow with only `curl`. Discovery first:

```sh
curl -sS -H 'Content-Type: application/json' \
  -d '{"id":"1","method":"searchSchool","params":{"search":"Gymnasium"},"jsonrpc":"2.0"}' \
  https://schoolsearch.webuntis.com/WebUntis/jsonrpc.do
```

Pick a result's `server` and `loginName`, then log in and ask for classes:

```sh
export UNTIS_SERVER=mese UNTIS_SCHOOL=demo-school
export UNTIS_USER=demo UNTIS_PASSWORD=demo

curl -sS -c jar.txt -H 'Content-Type: application/json' \
  -d "{\"id\":\"1\",\"method\":\"authenticate\",\"params\":{\"user\":\"$UNTIS_USER\",\"password\":\"$UNTIS_PASSWORD\",\"client\":\"learn\"},\"jsonrpc\":\"2.0\"}" \
  "https://$UNTIS_SERVER.webuntis.com/WebUntis/jsonrpc.do?school=$UNTIS_SCHOOL"

curl -sS -b jar.txt -H 'Content-Type: application/json' \
  -d '{"id":"2","method":"getKlassen","params":{},"jsonrpc":"2.0"}' \
  "https://$UNTIS_SERVER.webuntis.com/WebUntis/jsonrpc.do?school=$UNTIS_SCHOOL"
```

The same flow as a script is [`examples/curl/public-jsonrpc.sh`](../examples/curl/public-jsonrpc.sh)
and [`examples/python/02_public_jsonrpc.py`](../examples/python/02_public_jsonrpc.py).

## 4. Run the bundled examples

```sh
git clone https://github.com/UntisPlus/webuntis-apis.git
cd webuntis-apis

cp examples/.env.example examples/.env
$EDITOR examples/.env            # set UNTIS_SERVER, UNTIS_SCHOOL, credentials
set -a; . examples/.env; set +a

python3 examples/python/01_school_search.py "Gymnasium"
python3 examples/python/02_public_jsonrpc.py
```

The Python examples use only the standard library, so there is nothing to
install. [`examples/README.md`](../examples/README.md) lists every script and
which doc it matches.

## 5. What you need to experiment

- **To read everything:** nothing. Start reading.
- **To call a public timetable:** the school's server name; some schools publish
  anonymous access (see [05 — Internal JSON-RPC](05-jsonrpc-intern.md), OTP
  `100170`).
- **To use your own account:** your username/password, and for the intern
  surfaces a **shared secret** (the TOTP/QR code) from the app's
  *"share timetable"* / QR screen. See [02 — Authentication](02-authentication.md).
- **To use the official Platform/Timetable APIs:** API credentials issued by
  Untis GmbH (see [12 — Credits](12-reference-clients.md)).

## 6. Reading order for a new developer

1. [01 — Overview](01-overview.md) — how the families fit together.
2. [02 — Authentication](02-authentication.md) — cookies, TOTP, JWT, OAuth2.
3. [03 — School discovery](03-school-discovery.md).
4. [04 — Public JSON-RPC](04-jsonrpc-public.md) — the stable, documented methods.
5. Then the surface you actually need: [05](05-jsonrpc-intern.md),
   [06](06-mobile-rest-auth.md), [07](07-rest-view.md), [08](08-legacy-rest.md),
   [09](09-extern-timetable-v3.md) or [10](10-platform-api.md).
6. [11 — Formats & conventions](11-conventions.md) — dates, element types, errors.

## 7. Conventions you will hit immediately

| Thing | Rule |
|---|---|
| Dates | `YYYYMMDD` on public JSON-RPC, `YYYY-MM-DD` on REST, ISO-8601 on extern v3 |
| Times | `HHMM` on JSON-RPC |
| Colors | `RRGGBB` |
| Element types | `1`=class, `2`=teacher, `3`=subject, `4`=room, `5`=student |
| Content type | send `Content-Type: application/json` |
| Errors | `{"error":{"code":…,"message":…}}` (JSON-RPC) |

Full detail (all element types, error codes, enums) is in
[11 — Conventions](11-conventions.md).

## 8. When something goes wrong

| Symptom | Likely cause |
|---|---|
| `401` / login fails | wrong server, wrong school name, or the account requires TOTP |
| Login works, next call `401` | you did not send the session cookie / bearer token |
| `-8509` / `notAuthenticated` | cookie expired; authenticate again |
| Empty timetable | wrong element type/id, or school year boundary |
| `403` on a method | account lacks the required *right* for that method |

Methods and their required rights are listed in
[04 — Public JSON-RPC](04-jsonrpc-public.md).

## 9. Be a good citizen

Only query accounts and schools you are allowed to. Do not hammer servers, do
not scrape personal data, and remember the reverse-engineered surfaces are not
officially supported — the sanctioned path for production is the Untis Platform
API. See [`NOTICE.md`](../NOTICE.md).
