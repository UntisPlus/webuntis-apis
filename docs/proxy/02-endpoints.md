# 02 — HTTP endpoint reference

Every route the proxy serves. Routes under `/WebUntis/…` are **forwarded** to
the school server (with proxy additions); everything else is implemented by the
proxy.

Auth legend: **public** = no auth; **session** = `JSESSIONID` cookie from a
proxy login; **admin** = session whose user has `users.admin`; **token** = an
opaque calendar token in the URL.

## Forwarded WebUntis routes

| Route | Methods | Auth | Notes |
|---|---|---|---|
| `/WebUntis/jsonrpc.do?school=<school>` | POST | session | Public JSON-RPC; editor class-scoped methods run as the boosted teacher |
| `/WebUntis/jsonrpc_intern.do?school=<school>&m=<method>` | POST | self-authenticating (`auth` block) | Intern JSON-RPC; capabilities rewritten; personal fields enriched |
| `/WebUntis/api/…` | * | session | Legacy cookie REST passthrough (config, homeworks, etc.) |

Selecting the school: `?school=` on the login/request, or the `schoolname`
cookie.

### Login (`jsonrpc_intern.do`)

```
POST /WebUntis/jsonrpc_intern.do?school=<school>&m=getUserData2017
Content-Type: application/json

{"id":"1","jsonrpc":"2.0","method":"getUserData2017",
 "params":[{"auth":{"clientTime":<ms>,"user":"<user>","otp":"<otp>"}}]}
```

`otp` is a live 6-digit TOTP **or** the base32 shared secret itself (see
[README](README.md#login-the-proxys-own-auth)). Anonymous access uses
`user:"#anonymous#"`, `otp:"100170"` for schools that publish a timetable.
`?school=` on this request registers an unknown school on first login.

## Status, health & identity

| Route | Auth | Response |
|---|---|---|
| `GET /status` | public | `{"status":"ok","mode":"dev","version":"<tag or dev>","uptime_sec":N}` |
| `GET /healthz` | public | `200`/`503` `{"status":"ok|degraded","uptime_sec":N,"schools":N,"degraded":N}` |
| `GET /me` | session | `{"username","level","permissions":{...}}` |

`/healthz` is `200` while every school with a non-empty pool is being polled,
`503` when a school has gone stale. It reports no per-school detail by design
(see [09](09-configuration.md#health-status--metrics)).

## Change detection

| Route | Auth | Notes |
|---|---|---|
| `GET /api/timetable/changes` | session | pollable diff; see [03](03-change-detection.md) |
| `GET /api/timetable/stream` | session | SSE live stream; see [03](03-change-detection.md) |

Query parameters:

- `changes`: `school`, `classId` (omit → own class), `since` (class version),
  `sinceEvents` (own event version).
- `stream`: `school`.

`changes` returns `304 Not Modified` when neither the class version nor the
event version moved.

## Notifications — self-service subscriptions

Session required. Users manage subscriptions for classes they are entitled to:
their own class always; any pooled class, or school-wide (`classId 0`), only
with `editor`/`boosted`/admin.

| Route | Methods | Body / notes |
|---|---|---|
| `/api/webhooks` | GET | `{"webhooks":[{"id","school","classId","url"}]}` |
| `/api/webhooks` | POST | `{"classId":5000,"url":"…","secret":"…"}` → `{"id":N}` |
| `/api/webhooks/{id}` | DELETE | `{"deleted":true}` |
| `/api/webhooks/{id}/test` | POST | fire a test delivery → `{"ok":true,"status":N}` |
| `/api/ntfy` | GET | `{"topics":[{"id","school","classId","topic","baseUrl"}]}` |
| `/api/ntfy` | POST | `{"classId":5000,"topic":"…","baseUrl":"…"}` → `{"id":N}` |
| `/api/ntfy/{id}` | DELETE | `{"deleted":true}` |
| `/api/ntfy/{id}/test` | POST | → `{"ok":true,"status":N,"topic":"…","server":"…"}` |

The `GET /api/ntfy` listing is **element-aware**: a plain user sees topics for
their own class and their own student element; school-wide and
teacher/room/subject topics are only listed for `editor`/`boosted`/admin. See
[04](04-notifications.md) for the full model.

## Homework

Session required; the viewer comes from the session cookie and never the body.

```
GET  /api/homework/flags[?school=<name>]
200  {"school":"testschool","flags":[{"homeworkId":1001,"done":true,
                                       "doneAt":"2026-10-01T12:34:56Z"}]}
401  {"error":"not logged in"}

POST /api/homework/done[?school=<name>]   {"homeworkId":1001,"done":true}
200  {"homeworkId":1001,"done":true,"doneAt":"2026-10-01T12:34:56Z"}
200  {"homeworkId":1001,"done":false,"doneAt":null}
400  {"error":"homeworkId and done are required"}
401  {"error":"not logged in"}
```

`done:false` clears the flag; both writes are idempotent. See
[06](06-homework-and-absences.md).

## Absence notes

Session required.

```
GET  /api/absence/notes[?school=<name>]
200  {"school":"testschool","notes":[{"absenceKey":300001,
                                      "note":"bring workbook",
                                      "updatedAt":"2026-10-01T12:34:56Z"}]}

POST /api/absence/notes[?school=<name>]  {"absenceKey":300001,"note":"bring workbook"}
200  {"absenceKey":300001,"note":"bring workbook","updatedAt":"2026-10-01T12:34:56Z"}
200  {"absenceKey":300001,"note":null}
400  {"error":"absenceKey is required"} | {"error":"note is too long"}
401  {"error":"not logged in"}
```

An empty or whitespace-only `note` clears it. Capped at 2000 characters. See
[06](06-homework-and-absences.md).

## Calendar

| Route | Auth | Notes |
|---|---|---|
| `POST /api/calendar/token` | session | mint/return a subscription token |
| `GET /api/calendar/{token}.ics` | token | the iCal feed |
| `GET /week/{token}` | token | server-rendered week page (no JS) |

`POST /api/calendar/token` body — exactly one target:

```json
{"classId":5000}
{"personal":true}
{"personId":5006}
{"teacherId":123}
{"roomId":456}
{"subjectId":789}
```

Optional: `{"timezone":"Europe/Berlin"}` (default), `{"days":30}` (default 30,
max 365). Access: classes need pool membership; personal needs your own person
id; teacher/room/subject need `recon` or `boosted`. Response:

```json
{"type":"class","id":5000,"name":"10b","classId":5000,
 "token":"7aff8e9dd4707fde8c992c3902be0c96",
 "url":"https://<host>/api/calendar/7aff8e9dd4707fde8c992c3902be0c96.ics",
 "timezone":"Europe/Berlin","days":30,"horizon":"2026-11-10",
 "created":1750000000,"lastUsed":1750000000,"createdBy":"jdoe"}
```

See [05](05-calendar.md) for the feed contents and `/week`.

## Student events (Technik) — admin API

Admin session required. See [07](07-student-events.md).

| Route | Methods | Purpose |
|---|---|---|
| `GET /api/admin/events?username=<name>[&school=<s>]` | GET | one student's events, sorted by date then start |
| `/api/admin/events` | POST | create |
| `/api/admin/events/import?school=<s>` | POST | bulk import (CSV/JSON) |
| `GET /api/admin/events/absences?school=<s>` | GET | event-absence register |
| `PATCH /api/admin/events/absences` | PATCH | correct a register row |
| `GET /api/admin/events/absences/log?school=<s>` | GET | register changelog |
| `/api/admin/events/{id}` | PATCH / DELETE | partial edit / idempotent remove |

```json
POST {"username":"dee","date":"2026-10-01","startTime":"14:00","endTime":"15:00",
      "title":"Technik","subject":"Mathe","room":"R12","teacher":"Mr Smith",
      "description":"Arbeitsblatt mitbringen"}
```

## Absence notes vs. event-absence register

Do not confuse them: `/api/absence/notes` is a **student's private note on a
real Untis absence**; the event-absence register under `/api/admin/events/…` is
the **technician's local attendance tracking on proxy events**. The former is a
REST/JSON surface; the latter is driven through the ordinary intern absence
methods (see [07](07-student-events.md#the-event-absence-register)).

## Admin dashboard

| Route | Auth | Notes |
|---|---|---|
| `GET /admin` | admin | embedded single-page dashboard |
| `GET /admin/login` | public | login form |
| `/admin/*` | admin | JSON API used by the dashboard |

See [08](08-admin-api.md) for the full `/admin/*` API.

## Metrics (gated listener)

`GET /metrics` is **not** on the public handler. It is served only when
`-metrics-addr` is set, on that separate listener, together with the detailed
`GET /healthz`. See [09](09-configuration.md).
