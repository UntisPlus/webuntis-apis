# 12 — Reference clients & sources

Open-source projects that implement or document these APIs, and the primary
external sources used to write this reference.

## Implementations

| Project | Language | What it shows |
|---|---|---|
| [SapuSeven/BetterUntis](https://github.com/SapuSeven/BetterUntis) | Kotlin / Android | Intern JSON-RPC client, `Auth.kt` TOTP, `*2017` method constants, reverse-engineered OpenAPI specs (`untis-mobile.yaml`, `untis-rest.yaml`) |
| [SchoolUtils/WebUntis](https://github.com/SchoolUtils/WebUntis) | Node / JS | JSON-RPC + OTP login, `api/token/new` JWT minting, legacy `api/*` REST |
| [Meow/webuntis-api](https://github.com/Meow/webuntis-api) | Ruby | Four login modes, anonymous `100170`, TOTP, JWT refresh, `view` v1–v4 endpoint list, `schoolquery2` discovery |
| [python-webuntis/python-webuntis](https://github.com/python-webuntis/python-webuntis) | Python | Public `jsonrpc.do` methods + required-rights matrix |
| [michilyy/pyWebUntis](https://github.com/michilyy/pyWebUntis) | Python | Intern `*2017` methods, `anonymous-school` header |
| [4biddencode/UntAPI](https://github.com/4biddencode/UntAPI) | Node | Method index, error codes |
| [mklemmingen/webuntis-public](https://github.com/mklemmingen/webuntis-public) | ? | Anonymous timetable access, migration away from `weekly/data` |
| [untis](https://docs.rs/untis/) (Rust crate) | Rust | `getStatusData` and client structure |
| [xp4u1/untis](https://github.com/xp4u1/untis), [webuntis](https://webuntis.hexdocs.pm/json-rpc.html) | Elixir | JSON-RPC method constants, 2017 methods |
| [Keule0010/WebUntisAPI](https://github.com/Keule0010/WebUntisAPI) | Java | `searchSchool`, secret login |

## Specifications

| Spec | Origin | Location |
|---|---|---|
| WebUntis JSON-RPC API PDF (2018-09-20) | 🟡 Untis-authored | [untis-sr.ch mirror](https://untis-sr.ch/wp-content/uploads/2019/11/2018-09-20-WebUntis_JSON_RPC_API.pdf) |
| Timetable API v3 | 🟢 Untis GmbH | [`specs/README.md`](../specs/README.md) |
| Untis Mobile / REST (intern) | 🔴 BetterUntis | [`specs/README.md`](../specs/README.md) |

## Official documentation

- Developer portal: <https://developer.untis.com/>
- Timetable v3: <https://developer.untis.com/api-reference/webuntis-apis/timetable-data/>
- Untis website: <https://www.untis.at/>

## Community write-ups

- SchoolUtils docs: <https://webuntis.noim.me/>
- Ruby `webuntis-api` REST rdoc:
  <https://rdoc.info/github/Meow/webuntis-api/WebUntis/REST>
- BetterUntis issue #219 (URL derivation, mobile service URL):
  <https://github.com/SapuSeven/BetterUntis/issues/219>

## See also

- [`README.md`](../README.md) — project overview
- [`specs/README.md`](../specs/README.md) — spec attribution
