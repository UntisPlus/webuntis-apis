# 03 — School discovery

Before you can call a school's API you need its **server host** (e.g. `mese`)
and its **school login name**. This page covers how clients find them.

> Legend: 🟢 official · 🟡 official spec · 🔴 reverse-engineered.

## 1. `searchSchool` (JSON-RPC) 🔴

All variants are a JSON-RPC `searchSchool` call against a central host:

| Host | Path | Notes |
|---|---|---|
| `schoolsearch.webuntis.com` | `/schoolquery2` | Used by BetterUntis and the Ruby `webuntis-api` gem |
| `mobile.webuntis.com` | `/ms/schoolquery2/?v=a4.2.10` | Observed in the Untis Mobile APK |
| `school.webuntis.com` | `/WebUntis/jsonrpc.do` | Historical |

Request:

```http
POST https://schoolsearch.webuntis.com/schoolquery2
Content-Type: application/json

{
  "id": "untis-mobile-android",
  "jsonrpc": "2.0",
  "method": "searchSchool",
  "params": [ { "schoolid": 0, "search": "my school" } ]
}
```

Each `result.schools[]` entry carries fields such as:

| Field | Meaning |
|---|---|
| `id` / `schoolId` | Internal school id |
| `name` / `displayName` | Human-readable school name |
| `address` | Address string |
| `schoolType` | Type label |
| `server` | Tenant server subdomain (e.g. `mese`) |
| `serverUrl` | Full base URL |
| `loginName` | School login name used as `?school=` |
| `tenantId` | Platform tenant id |
| `useMobileServiceUrlAndroid` / `useMobileServiceUrlIos` | When true, use a mobile service URL instead |

> ⚠️ If a school's `mobileServiceUrl` / `useMobileServiceUrl*` is set, the mobile
> API must be called through that URL. `mobile.webuntis.com` itself is no longer
> accepted as an API target by Untis.

## 2. App shared secret 🔴

The legacy mobile host can hand out a per-school app secret before login:

```http
POST https://mobile.webuntis.com/ms/app/<appId>?school=<school>&v=a4.2.10&m=getAppSharedSecret&anonymous=false&server=<host>
```

Also reachable as the intern JSON-RPC method `getAppSharedSecret` (see
[05](05-jsonrpc-intern.md)).

## 4. Direct probing 🔴

Some clients skip search entirely and probe common TLDs
(`.webuntis.com`, `.webuntis.de`, `.webuntis.at`, `*.untis.at`) for a reachable
`/WebUntis/jsonrpc.do`. This is discouraged: it is slow, noisy, and can trip
rate limits.

## 5. Resolving the tenant server from a known part

- If the school name equals the server subdomain (`mese` → `mese.webuntis.com`),
  you can try it directly.
- Some deployments expose the canonical host in the web login page; parse it if
  you have the login URL.
- The Platform API resolves everything through `api.webuntis.com` and its
  `tenantId`, so no `searchSchool` is needed — see [10](10-platform-api.md).

## 6. The `schoolname` cookie 🔴

The web client and REST calls additionally set:

```http
Cookie: schoolname=_<base64(school)>
```

The leading underscore is literal; the value is standard Base64 of the school
login name (e.g. `_bWVzZQ==` for `mese`). Some servers accept requests without
it, some require it alongside `JSESSIONID`.
