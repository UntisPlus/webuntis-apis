# 06 — Mobile REST auth (v2)

> 🔴 **Reverse-engineered.** Observed from the official Untis Mobile app and
> documented in BetterUntis' `untis-mobile.yaml`. One observed use case:
> exchanging username/password for a JWT.

## Endpoint

```http
POST /WebUntis/api/mobile/v2/<schoolName>/authentication
Content-Type: application/json
```

This path is **not** under the usual `/WebUntis/api/rest/view` prefix; note the
`/api/mobile/v2` segment.

### Request

```json
{ "username": "<username>", "password": "<password>" }
```

| Field | Type | Required |
|---|---|---|
| `username` | string | yes |
| `password` | string | yes |

### Response `200`

```json
{
  "jwt": "eyJhbGciOi…",
  "isEmailUpdateRequired": false,
  "isPasswordChangeRequired": false
}
```

| Field | Meaning |
|---|---|
| `jwt` | Bearer token for the REST API (see [07](07-rest-view.md)) |
| `isEmailUpdateRequired` | Prompt the user to update their email; do so via `PUT /api/rest/view/v1/profile/user-contact-data` |
| `isPasswordChangeRequired` | Prompt for a password change (exact server behaviour unknown) |

### Errors

```json
{ "type": "BAD_CREDENTIALS" }
```

or the structured error shape:

```json
{
  "errorCode": "INTERNAL_ERROR",
  "requestId": "…",
  "traceId": "…",
  "errorMessage": "…"
}
```

| Status | Body |
|---|---|
| `401` | `{ "type": "BAD_CREDENTIALS" }` |

## Alternatives to the password flow

You do not need this endpoint to obtain a JWT:

- **From a cookie session** (public JSON-RPC or intern OTP login):
  `GET /WebUntis/api/token/new` returns a JWT as plain text. This is the
  passwordless path the intern API advertises via `getAuthToken`.
- **Platform API**: OAuth2 client credentials / OIDC — see [10](10-platform-api.md).

## Usage

Present the JWT on the view API:

```http
GET /WebUntis/api/rest/view/v1/home
Authorization: Bearer <jwt>
Tenant-Id: <tenantId>
Cookie: JSESSIONID=<sid>; schoolname=_<base64(school)>
```

Token lifetime is short (observed ~15 min); parse `exp` and refresh before it
lapses.
