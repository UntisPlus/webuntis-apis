# 12 — Credits & prior art

Everything you need to use the WebUntis/Untis APIs is contained in this
repository: the prose in [`docs/`](README.md), the OpenAPI documents under
[`specs/`](../specs), the runnable [`examples/`](../examples), and the recorded
payloads under [`samples/`](../samples). You should never have to leave this
repo to understand an endpoint.

This page credits the projects the reference was built from and shares credit
with. Links and license details for anything we re-publish live in
[`NOTICE.md`](../NOTICE.md).

## Prior art

Reverse-engineering the WebUntis APIs was community work. The following
open-source projects, in roughly the order they informed this reference, made
it possible:

| Project | Language | What it contributed |
|---|---|---|
| SapuSeven/BetterUntis | Kotlin / Android | Intern JSON-RPC client, `Auth.kt` TOTP, `*2017` method constants, and the reverse-engineered OpenAPI specs (vendored in [`specs/untis-intern/`](../specs/untis-intern)) |
| SchoolUtils/WebUntis | Node / JS | JSON-RPC + OTP login, `api/token/new` JWT minting, legacy `api/*` REST |
| Meow/webuntis-api | Ruby | Four login modes, the anonymous OTP `100170`, TOTP, JWT refresh, the `view` v1–v4 endpoint list, `schoolquery2` discovery |
| python-webuntis/python-webuntis | Python | Public `jsonrpc.do` methods and the required-rights matrix |
| michilyy/pyWebUntis | Python | Intern `*2017` methods and the `anonymous-school` header |
| 4biddencode/UntAPI | Node | Method index and error codes |
| mklemmingen/webuntis-public | ? | Anonymous timetable access and migration away from `weekly/data` |
| untis (Rust crate) | Rust | `getStatusData` and client structure |
| xp4u1/untis, webuntis (Elixir) | Elixir | JSON-RPC method constants, `2017` methods |
| Keule0010/WebUntisAPI | Java | `searchSchool` and secret login |

## Specifications used

| Spec | Origin | In this repo |
|---|---|---|
| WebUntis JSON-RPC API (2018-09-20) | 🟡 authored by Untis GmbH | rendered as [04 — Public JSON-RPC](04-jsonrpc-public.md) |
| External Timetable API v1/v2/v3 | 🟢 Untis GmbH | [`specs/untis-extern/`](../specs/untis-extern) |
| Untis Platform APIs (15 OpenAPI docs) | 🟢 Untis GmbH | [`specs/untis-platform/`](../specs/untis-platform) + [platform docs mirror](platform/README.md) |
| Untis Mobile / REST (intern) | 🔴 BetterUntis | [`specs/untis-intern/`](../specs/untis-intern) |

## Getting credentials

The official API keys, SSO clients and platform passwords are issued by Untis
GmbH through its developer portal (developer.untis.com). The portal's
*documentation* is mirrored locally here (see
[`platform/`](platform/README.md)), but account sign-up and credential issuance
are the one thing that cannot be — you need an account there to call the official
Platform and Timetable APIs in production. Everything about *how* those APIs
behave is documented locally in [10 — Platform API](10-platform-api.md) and
[09 — Timetable API v3](09-extern-timetable-v3.md).

## See also

- [`README.md`](../README.md) — project overview
- [`NOTICE.md`](../NOTICE.md) — attribution and licenses
- [`specs/README.md`](../specs/README.md) — spec index
