# Examples

Small, runnable examples for each WebUntis API surface. Download the repo,
fill in a couple of environment variables, and run them.

## Setup

```sh
git clone https://github.com/UntisPlus/webuntis-apis.git
cd webuntis-apis

cp examples/.env.example examples/.env
$EDITOR examples/.env            # set UNTIS_SERVER, UNTIS_SCHOOL, credentials…
set -a; . examples/.env; set +a  # load it into the shell
```

The Python examples use **only the standard library** (Python 3.8+). The shell
examples need `curl` (and use `jq` for pretty output if it is installed).

> ⚠️ Never commit a filled-in `examples/.env`; it is gitignored. These
> endpoints talk to real school servers — only query data you are allowed to.

## Python examples

| Script | API | Docs |
|---|---|---|
| [`python/01_school_search.py`](python/01_school_search.py) | School discovery (`searchSchool`) | [03](../docs/03-school-discovery.md) |
| [`python/02_public_jsonrpc.py`](python/02_public_jsonrpc.py) | Public JSON-RPC (official) | [04](../docs/04-jsonrpc-public.md) |
| [`python/03_intern_login_totp.py`](python/03_intern_login_totp.py) | Intern JSON-RPC (TOTP / anonymous) | [05](../docs/05-jsonrpc-intern.md) |
| [`python/04_mobile_jwt.py`](python/04_mobile_jwt.py) | Mobile v2 auth → JWT | [06](../docs/06-mobile-rest-auth.md) |
| [`python/05_view_rest.py`](python/05_view_rest.py) | View REST (`api/rest/view/v1`) | [07](../docs/07-rest-view.md) |
| [`python/06_legacy_rest.py`](python/06_legacy_rest.py) | Legacy cookie REST | [08](../docs/08-legacy-rest.md) |
| [`python/07_extern_timetable.py`](python/07_extern_timetable.py) | External Timetable v3 | [09](../docs/09-extern-timetable-v3.md) |
| [`python/08_platform_oauth.py`](python/08_platform_oauth.py) | Platform OAuth2 token | [10](../docs/10-platform-api.md) |

`python/lib.py` holds the shared helpers (a cookie-aware HTTP client, TOTP, a
JSON-RPC call, JWT parsing).

### Quick runs

```sh
python3 examples/python/01_school_search.py "Gymnasium"
python3 examples/python/02_public_jsonrpc.py

# anonymous intern login (schools with a public timetable)
UNTIS_ELEMENT_ID=123 python3 examples/python/03_intern_login_totp.py

# password -> JWT, then use it
export UNTIS_JWT="$(python3 examples/python/04_mobile_jwt.py | sed -n 's/^# jwt: //p' | tr -d '.')"
python3 examples/python/05_view_rest.py
```

## Shell / curl examples

| Script | Shows |
|---|---|
| [`curl/public-jsonrpc.sh`](curl/public-jsonrpc.sh) | `authenticate` → `getKlassen` → `logout`, cookie jar |
| [`curl/token-new.sh`](curl/token-new.sh) | Mint a JWT from a cookie session |
| [`curl/intern-login.sh`](curl/intern-login.sh) | Anonymous intern login + `getTimetable2017` |
| [`curl/extern-v3.sh`](curl/extern-v3.sh) | External Timetable v3 with a bearer token |

```sh
./examples/curl/public-jsonrpc.sh
./examples/curl/intern-login.sh
```

## Notes

- Replace dates/ids with real values from your school.
- Public JSON-RPC expects `YYYYMMDD` dates; intern and view REST use
  `YYYY-MM-DD` — see [formats](../docs/11-conventions.md).
- The intern/mobile examples hit **reverse-engineered** endpoints; they may
  change without notice.
