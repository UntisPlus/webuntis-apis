# 02 — Authentication

WebUntis uses several unrelated authentication schemes depending on the API
family. This page covers each, in increasing order of modernity.

> Legend: 🟢 official · 🟡 official spec · 🔴 reverse-engineered.
> See [04](04-jsonrpc-public.md), [05](05-jsonrpc-intern.md), [06](06-mobile-rest-auth.md),
> [10](10-platform-api.md) for the endpoints referenced here.

## Summary

| Scheme | Applies to | Credential | Result |
|---|---|---|---|
| Password login 🟡 | `jsonrpc.do` | `user` + `password` + `client` | `sessionId` / `JSESSIONID` cookie |
| TOTP / QR login 🔴 | `jsonrpc_intern.do` | `user` + `otp` (TOTP) | `JSESSIONID` cookie |
| Anonymous 🔴 | `jsonrpc_intern.do` | user `#anonymous#`, otp `100170` | `JSESSIONID` cookie (read-only) |
| Mobile REST auth 🔴 | `api/mobile/v2/.../authentication` | `username` + `password` | JWT |
| Token minting 🔴 | `api/token/new` | existing cookie session | JWT (plain text) |
| OAuth2 client credentials 🟢 | Platform API | `clientId` + `clientSecret` | bearer token (~3 min) |
| OIDC authorization code 🟢 | Platform API (user) | SSO / IdP | bearer token |

## 1. Cookie sessions (JSON-RPC) 🟡🔴

### 1.1 Password login (public API) 🟡

```http
POST /WebUntis/jsonrpc.do?school=<school>
Content-Type: application/json

{
  "id": "request",
  "method": "authenticate",
  "params": { "user": "<username>", "password": "<password>", "client": "<app-id>" },
  "jsonrpc": "2.0"
}
```

Response:

```json
{
  "jsonrpc": "2.0",
  "id": "request",
  "result": { "sessionId": "644AFBF2C1B592B68C6B04938BD26965", "personType": 2, "personId": 17 }
}
```

- `personType`: `2` = teacher, `5` = student (see [11](11-conventions.md)).
- The session is *also* delivered as the `JSESSIONID` cookie. Send it on every
  subsequent call:

  ```http
  Cookie: JSESSIONID=644AFBF2C1B592B68C6B04938BD26965
  ```

- The older path-parameter form (`;jsessionid=…`) is **deprecated and rejected**
  from WebUntis 2019 onward.
- `client` is a client-app identifier; the 2018 spec says it "will be mandatory
  in the future", so always send one.
- Log out explicitly with `{"method":"logout","params":{}}` to free server
  resources.

### 1.2 TOTP / QR login (intern API) 🔴

The mobile apps log in with a per-user secret instead of a password. The secret
is shown as a QR code in the web UI (profile → *show QR-code*) and is the key all
owning data is scoped under.

```http
POST /WebUntis/jsonrpc_intern.do?m=getUserData2017&school=<school>&v=i2.2
Content-Type: application/json

{
  "id": "untis-mobile-android",
  "jsonrpc": "2.0",
  "method": "getUserData2017",
  "params": [ { "auth": { "clientTime": 1720000000000, "user": "<username>", "otp": 123456 } } ]
}
```

- `otp` is a **RFC 6238 TOTP**: HMAC-SHA1 over the base32-decoded, uppercased
  secret; `counter = unixSeconds / 30`; 6 digits (`& 0x7FFFFFFF`, `% 1000000`).
- `clientTime` is the current time in **epoch milliseconds**.
- Success returns `JSESSIONID` via `Set-Cookie`.
- The QR URI format is 🔴:
  `untis://setschool?url=<server>&school=<school>&user=<username>&key=<secret>&schoolNumber=<n>`

### 1.3 Anonymous login 🔴

Schools that publish a public timetable accept:

```json
{ "auth": { "clientTime": 1720000000000, "user": "#anonymous#", "otp": "100170" } }
```

The pair `#anonymous#` / `100170` is a community-observed constant. Anonymous
sessions are read-only and cannot use messaging or own-homework features.

## 2. JSON Web Tokens (REST) 🔴

The REST APIs (view API, mobile v2) use short-lived JWTs.

### 2.1 Obtain a JWT with a password

```http
POST /WebUntis/api/mobile/v2/<schoolName>/authentication
Content-Type: application/json

{ "username": "<username>", "password": "<password>" }
```

```json
{ "jwt": "eyJhbGciOi…", "isPasswordChangeRequired": false, "isEmailUpdateRequired": false }
```

See [06 — Mobile REST auth](06-mobile-rest-auth.md).

### 2.2 Mint a JWT from a cookie session

```http
GET /WebUntis/api/token/new
Cookie: JSESSIONID=<sid>; schoolname=<base64(school)>
Accept: text/plain
```

The response body **is** the JWT (plain text, not JSON). This lets a client that
logged in via JSON-RPC/OTP reach the REST API without seeing the password. The
token's `exp` claim bounds its lifetime (observed ~15 min); refresh ~30 s early.

### 2.3 Using the JWT

```http
Authorization: Bearer <jwt>
Tenant-Id: <tenantId>
X-Webuntis-Api-School-Year-Id: <schoolYearId>
Cookie: JSESSIONID=<sid>; schoolname=<base64(school)>
```

Some endpoints require `Tenant-Id` and/or the school-year header. Without a
valid bearer token the view API often answers **404** rather than 401. See
[07 — "View" REST API](07-rest-view.md).

## 3. OAuth2 / OIDC (Platform API) 🟢

### 3.1 Server-to-server (client credentials)

```http
POST https://api.webuntis.com/WebUntis/api/sso/v3/<tenantId>/token
Authorization: Basic base64(<clientId>:<platform-generated-password>)
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials
```

- Use the **platform-generated password** as the secret (not the OIDC client
  secret).
- Tokens are short-lived (**~3 minutes**); cache and respect `expires_in`.

### 3.2 User (OIDC authorization code)

Standard OpenID Connect authorization-code flow, optionally with PKCE for public
clients (v3 only). Tenants may federate to O365 / LDAP / SAML / OIDC.

### 3.2 Webhooks

Untis signs outbound webhook requests with RSA; verify the signature before
trusting the payload.

See [10 — Untis Platform API](10-platform-api.md).

## 4. Session validation

- Public JSON-RPC: call `getLatestImportTime`; the session is valid iff the
  result is a number.
- Sessions expire after a short period of inactivity (observed ~10 min for the
  legacy web client) and after a long absolute lifetime.

## 4. Sessions and the school year

Homework and some class-register data are **pinned to the school year active at
login**. To read a different year you must switch the server-side session year
(web client: `POST /WebUntis/jsonrpc_web/jsonCalendarService` with a CSRF token;
see [08](08-legacy-rest.md)). Cross-year requests otherwise return HTTP 200 with
empty collections.
