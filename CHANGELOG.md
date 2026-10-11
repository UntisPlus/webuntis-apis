# Changelog

All notable changes to this reference are recorded here. The format follows
Keep a Changelog (keepachangelog.com).

## [Unreleased]

### Added

- Initial documentation set:
  - `00` getting-started guided tour
  - `01` overview and API-family matrix
  - `02` authentication (cookie, TOTP/QR, JWT, OAuth2/OIDC)
  - `03` school discovery (`searchSchool`, `schoolquery2`)
  - `04` public JSON-RPC method reference (official 2018 spec)
  - `05` internal `jsonrpc_intern.do` and `*2017` methods
  - `06` mobile REST auth (`api/mobile/v2/.../authentication`)
  - `07` "view" REST API endpoint catalogue
  - `08` legacy cookie REST endpoints
  - `09` external Timetable API v1/v2/v3
  - `10` Untis Platform API (OAuth2)
  - `11` formats, element types, error codes
  - `12` credits, prior art and how to get credentials
- Vendored the machine-readable specs under `specs/` (intern `untis-mobile.yaml`
  and `untis-rest.yaml`, extern Timetable v3 with error schemas) so the repo is
  self-contained, with attribution in `NOTICE.md`.
- Runnable examples under `examples/`: Python 3 (stdlib only) plus `curl`
  scripts for each API surface, and `examples/.env.example`.
- Illustrated sample payloads under `samples/` for every API surface.
- Offline mirror of the official Untis developer documentation under
  `docs/platform/` (42 pages: authentication, every Platform resource API,
  OneRoster, webhooks and integration guides), plus a Platform API summary with
  current versions, rate limits and the deleted-periods endpoint.
- Complete OpenAPI specs for all 15 Untis Platform APIs under
  `specs/untis-platform/` (full request/response schemas, enums and errors).
- Documentation of the **UntisPlus-Proxy** gateway surface under `docs/proxy/`:
  overview, permissions, endpoints, change detection, notifications, calendar,
  homework & absences, student events, the admin API, configuration and the
  `untisctl` operator CLI.
