# 10 — Untis Platform API

> 🟢 **Official.** Published by Untis GmbH on its developer portal
> (developer.untis.com); summarised locally in this page.
> This is the sanctioned, versioned, contract-backed integration surface.

## Base URLs

| Environment | URL |
|---|---|
| Production | `https://api.webuntis.com/` |
| Sandbox / integration | `https://api.integration.webuntis.dev/` |

Everything is fronted by a single API gateway. Two resource families:

| Family | Path pattern |
|---|---|
| Untis Platform | `{{API_URL}}/WebUntis/api/rest/extern/v{version}/{resource}` |
| OneRoster | `{{API_URL}}/ims/oneroster/v1p1/{resource}` |

## Authentication

Three concerns:

| Concern | Mechanism |
|---|---|
| **User** (UI/SSO) | OpenID Connect Authorization Code; PKCE supported. Tenants may federate to O365/LDAP/SAML/OIDC. v3 only |
| **Application** (server-to-server) | OAuth2 Client Credentials; `Basic base64(clientId:platform-password)`; **short-lived tokens (~3 min)** — cache and honour `expires_in` |
| **Request** (webhooks) | RSA request signing (Untis → your endpoint); verify the signature |

```http
POST {{API_URL}}/WebUntis/api/sso/v3/<tenantId>/token
Authorization: Basic base64(<clientId>:<platform-generated-password>)
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials
```

⚠️ Use the **platform-generated password**, not the OIDC client secret.

## Rate limits & quotas

- Token lifetime **~3 minutes** (client credentials).
- Respect `expires_in`; do not request a token per call.

## Resource APIs

| API | Version | Status |
|---|---|---|
| Students | v1 | current |
| Timetable | **v3** | v1/v2 deprecated — see [09](09-extern-timetable-v3.md) |
| Teachers | v2 | |
| Classes | v1 | |
| Rooms | v1 | |
| Subjects | v1 | |
| Absences | v1 | |
| Exams | v1 | |
| Lessons | v1 | |
| Messaging | v1 | |
| OneRoster | v1p1 | |

Typical endpoints (pattern):

```
GET {{API_URL}}/WebUntis/api/rest/extern/v1/students
GET {{API_URL}}/WebUntis/api/rest/extern/v3/timetable?start=…&end=…&class=…
GET {{API_URL}}/WebUntis/api/rest/extern/v1/exams?start=…&end=…
```

## Errors

Standard HTTP status codes with a JSON body:

```json
{ "errorCode": "…", "errorMessage": "…", "requestId": "…", "traceId": "…" }
```

Validation errors carry a `validationErrors[]` array. Consult
`developer.untis.com` for the per-API schema.

## When to use it

- You are building an official integration and can register an application.
- You need a stable contract, versioning, and support.
- You can map your tenant (`tenantId`) and resources.

For quick, unauthenticated reads of a public timetable, the public JSON-RPC API
([04](04-jsonrpc-public.md)) or the extern timetable API
([09](09-extern-timetable-v3.md)) are lighter-weight.

## Sources

This page summarises the official developer portal (developer.untis.com). The
External Timetable v3 spec it references is vendored locally in
[`specs/untis-extern/`](../specs/untis-extern).
