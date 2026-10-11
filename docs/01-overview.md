# 01 — Overview

WebUntis is a school information system by Untis GmbH (Austria). Over its long
life it has accumulated **several distinct API surfaces** that are frequently
confused with each other. This page maps them out; the linked pages document
each in detail.

> **Provenance legend:** 🟢 official · 🟡 official spec (retransmitted) ·
> 🔴 reverse-engineered. See the [root README](../README.md).

## The families

```
                             Untis GmbH
                                 │
        ┌────────────────────────┼──────────────────────────────┐
        │                        │                              │
  Legacy web/JSON-RPC      Mobile / web client internals    Untis Platform
  (per school server)      (undocumented)                   (central gateway)
        │                        │                              │
  jsonrpc.do  🟡           jsonrpc_intern.do  🔴             api.webuntis.com  🟢
                           api/mobile/v2      🔴             OAuth2 / OIDC
                           api/rest/view      🔴             /WebUntis/api/rest/extern
                           api/*              🔴
```

### 1. Legacy public JSON-RPC API 🟡

- **Base:** `https://<server>.webuntis.com/WebUntis/jsonrpc.do?school=<school>`
- **Used by:** third-party integrations, `python-webuntis`, school plugins.
- **Auth:** `authenticate` (username + password + client) → `JSESSIONID` cookie.
- **Status:** stable for years; documented by an official Untis-authored PDF
  dated 2018-09-20 that circulates third-party.
- **Docs:** [04 — Public JSON-RPC](04-jsonrpc-public.md)

### 2. Internal "intern" JSON-RPC API 🔴

- **Base:** `https://<server>.webuntis.com/WebUntis/jsonrpc_intern.do?m=<method>&school=<school>&v=i2.2`
- **Used by:** the official Untis Mobile apps and (historically) the WebUntis
  web client.
- **Auth:** an `auth` block carrying a TOTP `otp` (from the QR-code secret) →
  `JSESSIONID` cookie.
- **Status:** undocumented and unstable; replaced in places by the "view" REST
  API.
- **Docs:** [05 — Internal JSON-RPC](05-jsonrpc-intern.md)

### 3. "View" REST API 🔴

- **Base:** `https://<server>.webuntis.com/WebUntis/api/rest/view/v1..v4/...`
- **Used by:** the current Untis Mobile app and web app.
- **Auth:** `Authorization: Bearer <JWT>` + `Tenant-Id` header (+ cookies).
- **Docs:** [07 — "View" REST API](07-rest-view.md)

### 4. Legacy cookie REST 🔴

- **Base:** `https://<server>.webuntis.com/WebUntis/api/...` (e.g. `api/app/config`,
  `api/homeworks/lessons`, `api/public/timetable/weekly/data`).
- **Auth:** cookies only (`JSESSIONID`, `schoolname`).
- **Status:** partly broken since ~2024; superseded by the view API.
- **Docs:** [08 — Legacy cookie REST](08-legacy-rest.md)

### 5. External Timetable API 🟢/🟡

- **Base:** `https://<server>.webuntis.com/WebUntis/api/rest/extern/v{1,2,3}/timetable`
  (and on the central gateway `https://api.webuntis.com/WebUntis/api/rest/extern/...`).
- **Auth:** the platform's OAuth2 client-credentials token (legacy: API key).
- **Status:** officially documented, actively maintained; **v3** is current.
- **Docs:** [09 — Timetable API v3](09-extern-timetable-v3.md)

### 6. Untis Platform APIs 🟢

- **Base:** `https://api.webuntis.com/` (sandbox `https://api.integration.webuntis.dev/`).
- **Auth:** OAuth2 client credentials (server-to-server) or OIDC (user).
- **Resources:** students, teachers, classes, rooms, subjects, timetable,
  exams, lessons, messaging, absences, OneRoster.
- **Docs:** [10 — Untis Platform API](10-platform-api.md)

## Choosing an API

| You want to… | Use |
|---|---|
| Integrate officially, with a contract | Platform API 🟢 / extern Timetable v3 |
| Read a public/anonymous timetable | Public JSON-RPC 🟡 or extern v3 |
| Do what the official mobile app does | Intern JSON-RPC 🔴 + view REST 🔴 |
| Support passwordless login (QR/TOTP) | Intern `getUserData2017` 🔴 |
| Read messaging, homework, exams, absences | View REST 🔴 (or Platform API where available) |

> ⚠️ Only the 🟢 surfaces are sanctioned by Untis. The 🔴 surfaces are
> reverse-engineered, may change at any time, and their use may conflict with a
> school's or Untis' terms of service.

## Hosts

| Host | Purpose |
|---|---|
| `<server>.webuntis.com` | A school's tenant server (`server` ∈ `mese`, `tritone`, `hepta`, …) |
| `schoolsearch.webuntis.com` | Central school search (`searchSchool`) |
| `mobile.webuntis.com` | Legacy mobile school query/app-secret host |
| `api.webuntis.com` | Central Untis Platform gateway |
| `api.integration.webuntis.dev` | Platform sandbox |

See [03 — School discovery](03-school-discovery.md) for how a school name maps
to a `<server>` host.
