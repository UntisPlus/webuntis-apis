# Changelog

All notable changes to this reference are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Initial documentation set:
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
  - `12` reference clients and sources
- Runnable examples under `examples/`: Python 3 (stdlib only) plus `curl`
  scripts for each API surface, and `examples/.env.example`.
- `specs/README.md` with links to the upstream machine-readable specs.
