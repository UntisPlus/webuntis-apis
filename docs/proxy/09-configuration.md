# 09 — Configuration

Every command-line flag is also settable as an environment variable named
`UNTIS_<FLAG>` (uppercased, dashes → underscores). Precedence is:

```
explicit flag  >  environment variable  >  flag default
```

A malformed env value is logged and the default kept, rather than taking the
process down.

## Flags / environment

| Flag | Env | Default | Meaning |
|---|---|---|---|
| `-addr` | `UNTIS_ADDR` | `:8509` | public listen address |
| `-school` | `UNTIS_SCHOOL` | *(required)* | the school name — the key **all** data is stored under |
| `-server` | `UNTIS_SERVER` | *(auto)* | fallback upstream host; normally auto-resolved per school via `searchSchool` |
| `-db` | `UNTIS_DB` | `untis.db` | SQLite database path |
| `-ttl` | `UNTIS_TTL` | `5m` | timetable cache TTL |
| `-year-start` / `-year-end` | `UNTIS_YEAR_START` / `UNTIS_YEAR_END` | *(auto)* | school-year bounds override |
| `-env` | `UNTIS_ENV` | `dev` | deployment mode (`dev`/`beta`/`prod`) |
| `-version` | `UNTIS_VERSION` | build version | reported build version |
| `-poll-interval` | `UNTIS_POLL_INTERVAL` | `60s` | change-detection poll interval |
| `-ntfy-base` | `UNTIS_NTFY_BASE` | `https://ntfy.sh` | default ntfy publish server |
| `-allow-private-targets` | `UNTIS_ALLOW_PRIVATE_TARGETS` | `false` | allow webhook/ntfy targets on private/loopback/link-local addresses (SSRF guard) |
| `-calendar-token-max-days` | `UNTIS_CALENDAR_TOKEN_MAX_DAYS` | `0` | max age (days) of a calendar token; `0` = never expires |
| `-public-base` | `UNTIS_PUBLIC_BASE` | `""` | externally reachable base URL for click-through links |
| `-admin` | `UNTIS_ADMIN` | `""` | comma-separated usernames to bootstrap as admins (once) |
| `-metrics-addr` | `UNTIS_METRICS_ADDR` | `""` | bind address for `/metrics`; empty disables it |
| `-recon-refresh` | `UNTIS_RECON_REFRESH` | `21` | days a class's recon horizon may lag before re-enumeration |
| `-recon-rescan` | `UNTIS_RECON_RESCAN` | `false` | re-enumerate every pooled class from the year start on boot |

`-school` is **required**: it is the storage key for pool, recon, permissions,
sessions and tokens. Defaulting it would let a fresh deployment silently inherit
another school's identity.

## School year

Derived automatically and used by the boot-time recon scan: German school years
start in **August**. Aug–Dec → 1 Aug of this year … 31 Jul next; Jan–Jul → 1 Aug
of the previous year … 31 Jul this year. Override only for unusual calendars.

## Health, status & metrics

| Endpoint | Listener | Auth | Contents |
|---|---|---|---|
| `GET /status` | public | none | `{"status":"ok","mode","version","uptime_sec"}` |
| `GET /healthz` | public | none | `{"status":"ok|degraded","uptime_sec","schools","degraded"}` |
| `GET /healthz` (detailed) | metrics listener | network | per-school array (names, counts, scan state, poll counters, reasons) |
| `GET /metrics` | metrics listener | network | Prometheus text format |

A school is **degraded** when it has a non-empty pool and:

- no class poll has ever succeeded, **or**
- the most recent poll failed (a poller that succeeded until recently is already
  serving stale data), **or**
- the last *successful* poll was more than `10m` ago, **or**
- too many pooled classes are behind the recon target horizon.

The process is `ok` only when every school is healthy. `/healthz` returns `503`
when degraded, `200` otherwise, and works unchanged as a container healthcheck.

> **Why metrics are gated.** The metrics and detailed-health responses carry the
> **school name** as a label on every series, plus pool size and poll counters —
> a free inventory of the deployment. They were previously reachable without
> authentication. They now live only on the separate `-metrics-addr` listener, so
> the boundary is the network: bind it to loopback or a private network and a
> scraper needs no credentials while the public address exposes nothing. Set no
> `-metrics-addr` and `/metrics` is not served at all.

The public `/healthz` and `/status` stay **aggregate-only** and never name a
school or a failing destination.

## Public surface & security headers

Every response carries:

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: no-referrer
Content-Security-Policy: default-src 'self'; img-src 'self' data:;
    style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline';
    connect-src 'self'; font-src 'self' data:; base-uri 'none';
    form-action 'self'; frame-ancestors 'none'; object-src 'none'
Strict-Transport-Security: max-age=31536000      (only over TLS)
```

- Bodies are capped at **1 MiB** (`MaxBytesReader`).
- Session cookies are `HttpOnly`, `SameSite=Lax`, and `Secure` whenever the
  request arrived over TLS or `X-Forwarded-Proto: https` — a spoofed header can
  only *add* Secure, never remove it.

HTTP server timeouts: read-header `10s`, read `15s`, write `30s`, idle `120s`.

## SSRF guard

Webhook URLs and ntfy `baseUrl` overrides are validated (`validateTargetURL`)
against private, loopback and link-local addresses unless
`-allow-private-targets` is set. Keep it off unless you deliberately deliver to a
LAN receiver.

## School year / recon options

- `-recon-refresh N` — a class is re-scanned once its stored horizon is more than
  `N` days behind the target (default `21`).
- `-recon-rescan` — re-enumerate every pooled class from the year start on boot
  instead of resuming; also available at runtime via
  `POST /admin/recon/rescan` ([08](08-admin-api.md)).

## Related

- Operator CLI: [`untisctl`](10-untisctl.md), which reads the same `UNTIS_DB` /
  `UNTIS_SCHOOL` environment.
