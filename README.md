# WebUntis & Untis API Reference

A community-maintained, source-cited reference for the **WebUntis / Untis**
APIs: the official web and platform APIs, the JSON-RPC APIs used by the web
client, and the reverse-engineered "intern" APIs used by the official Untis
Mobile apps.

The goal is to give client developers one place that answers *which* API exists,
*where* it lives, *how* it authenticates, and *what* it returns — with each fact
labelled **official** or **reverse-engineered** so you know how much to trust it.

> **Provenance legend**
> - 🟢 **Official** — published/operated by Untis GmbH (e.g. `developer.untis.com`).
> - 🟡 **Official spec, retransmitted** — authored by Untis but hosted third-party
>   (e.g. the 2018 WebUntis JSON-RPC API PDF).
> - 🔴 **Reverse-engineered** — undocumented, observed from the official apps or
>   community libraries. Subject to change without notice.

## The API families at a glance

| Family | Host / base path | Protocol | Auth | Docs here |
|---|---|---|---|---|
| Legacy JSON-RPC (public) | `<server>.webuntis.com/WebUntis/jsonrpc.do?school=<school>` | JSON-RPC 2.0 | `JSESSIONID` cookie | [04](docs/04-jsonrpc-public.md) |
| Internal JSON-RPC (mobile/web client) | `<server>.webuntis.com/WebUntis/jsonrpc_intern.do?m=…&school=…&v=i2.2` | JSON-RPC 2.0 | OTP block → `JSESSIONID` cookie | [05](docs/05-jsonrpc-intern.md) |
| Mobile auth (v2) | `<server>.webuntis.com/WebUntis/api/mobile/v2/<school>/authentication` | REST/JSON | username+password → JWT | [06](docs/06-mobile-rest-auth.md) |
| "View" REST API (web/mobile internals) | `<server>.webuntis.com/WebUntis/api/rest/view/v1…v4/…` | REST/JSON | JWT bearer (+ cookies) | [07](docs/07-rest-view.md) |
| Legacy cookie REST (web client) | `<server>.webuntis.com/WebUntis/api/…` | REST/JSON | `JSESSIONID` cookie | [08](docs/08-legacy-rest.md) |
| Extern Timetable API v3 | `<server>.webuntis.com/WebUntis/api/rest/extern/v3/timetable` | REST/JSON | OAuth2 / platform token | [09](docs/09-extern-timetable-v3.md) |
| Untis Platform API | `api.webuntis.com/WebUntis/api/rest/extern/…` | REST/JSON + OIDC/OAuth2 | OAuth2 / OIDC | [10](docs/10-platform-api.md) |

## Documentation index

| Doc | Contents |
|---|---|
| [01 — Overview](docs/01-overview.md) | How the families relate, server architecture, when to use which |
| [02 – Authentication](docs/02-authentication.md) | Cookie sessions, TOTP/QR, JWT, OAuth2/OIDC, anonymous access |
| [03 – School discovery](docs/03-school-discovery.md) | `searchSchool`, `schoolquery2`, server URL derivation |
| [04 – Public JSON-RPC](docs/04-jsonrpc-public.md) | The 🟡 officially specified `jsonrpc.do` methods |
| [05 – Internal JSON-RPC](docs/05-jsonrpc-intern.md) | 🔴 `jsonrpc_intern.do` and the `*2017` methods |
| [06 – Mobile REST auth](docs/06-mobile-rest-auth.md) | 🔴 `api/mobile/v2/.../authentication` and JWT minting |
| [07 – "View" REST API](docs/07-rest-view.md) | 🔴 `api/rest/view/v1..v4` endpoint catalogue |
| [08 – Legacy cookie REST](docs/08-legacy-rest.md) | 🔴 `api/app/config`, `api/homeworks`, `weekly/data`, … |
| [09 – Timetable API v3 (extern)](docs/09-extern-timetable-v3.md) | 🟢/🟡 official `/api/rest/extern/v{1,2,3}/timetable` |
| [10 – Untis Platform API](docs/10-platform-api.md) | 🟢 `api.webuntis.com`, OAuth2, resource APIs |
| [11 – Formats & conventions](docs/11-conventions.md) | Dates, times, element types, error codes |
| [12 – Reference clients](docs/12-reference-clients.md) | Open-source implementations and specs |

## OpenAPI specs

The machine-readable companions to the prose docs live upstream (the
reverse-engineered specs come from the [BetterUntis](https://github.com/SapuSeven/BetterUntis)
project; the external timetable spec is published by Untis GmbH). See
[`specs/README.md`](specs/README.md) for links and attribution rather than
vendored copies.

## Legal

This repository documents API surfaces by observation and by citing public
sources. It contains **no** Untis server code and no credentials. "Untis" and
"WebUntis" are trademarks of Untis GmbH. Reverse-engineered sections are not
endorsed by Untis and may violate a provider's terms of service; the only
sanctioned integration surface is the one described at
[`developer.untis.com`](https://developer.untis.com/).

## License

Documentation is licensed under [CC BY 4.0](LICENSE). See the file for details.
