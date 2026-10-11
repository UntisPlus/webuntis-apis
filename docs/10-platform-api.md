# 10 — Untis Platform API

> 🟢 **Official.** Published by Untis GmbH on its developer portal
> (developer.untis.com); summarised locally in this page.
> This is the sanctioned, versioned, contract-backed integration surface.
>
> 📚 **Full offline copy:** the entire official documentation is mirrored under
> [`platform/`](platform/README.md) (42 pages: auth, all resource APIs,
> OneRoster, webhooks, guides). This page is the quick orientation.
>
> 📄 **Machine-readable schemas:** complete OpenAPI specs for all 15 Platform
> APIs are in [`specs/untis-platform/`](../specs/untis-platform/README.md).

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

- **Max 40 requests/second per app** (fair-use monitoring).
- Token lifetime **~3 minutes** (client credentials); respect `expires_in` and
  do not request a token per call.
- Schedule large sync jobs off-peak: **Mon–Fri 19:00–05:00, or weekends**.
  Avoid 06:00–09:00.

## Resource APIs

| API | Current version | Status |
|---|---|---|
| User management | v1 | current |
| Student management | **v3** | v1/v2 deprecated |
| Teacher management | **v2** | v1 deprecated |
| Legal guardian management | v1 | current |
| Class management | **v2** | v1 deprecated |
| Room management | v1 | current (read-only) |
| Subject management | v1 | current (read-only) |
| Teacher absence management | v1 | current |
| Teacher absence reasons | v1 | current |
| Timetable | **v3** | v1/v2 deprecated — see [09](09-extern-timetable-v3.md) |
| Timetable event push | v1 | current |
| Class register absences | v1 | current |
| Exams | v1 | current |
| Lessons | v1 | current |
| Messaging | v1 | current |
| OneRoster | v1p1 | current |

Pattern:

```
GET {{API_URL}}/WebUntis/api/rest/extern/v3/students?schoolYearId=2026
GET {{API_URL}}/WebUntis/api/rest/extern/v3/teachers
GET {{API_URL}}/WebUntis/api/rest/extern/v3/classes
GET {{API_URL}}/WebUntis/api/rest/extern/v2/teachers
GET {{API_URL}}/WebUntis/api/rest/extern/v1/rooms
GET {{API_URL}}/WebUntis/api/rest/extern/v3/timetable?start=…&end=…&class=…
GET {{API_URL}}/WebUntis/api/rest/extern/v3/timetable/deleted-periods?dateLastModifiedAfter=…
GET {{API_URL}}/WebUntis/api/rest/extern/v1/exams?start=…&end=…
GET {{API_URL}}/ims/oneroster/v1p1/students?limit=100&offset=0
```

Every list endpoint supports OneRoster-style `limit`/`offset` paging, `sort` +
`orderBy=asc|desc`, and a single-operator `filter` (see
[Common API concepts](platform/pages/api-reference-common-api-concepts.md)).
Per-resource details are in the [`platform/`](platform/README.md) mirror.

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

This page summarises the official developer portal (developer.untis.com), which
is mirrored in full under [`platform/`](platform/README.md). The External
Timetable OpenAPI is vendored in [`../specs/untis-extern/`](../specs/untis-extern).
