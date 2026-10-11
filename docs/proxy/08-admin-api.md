# 08 — Admin API

A dependency-free single-page dashboard plus the JSON API behind it. It exposes
everything `untisctl` can do, for the browser and for scripting.

| Route | Auth | Serves |
|---|---|---|
| `GET /admin` | admin session | embedded dashboard HTML |
| `GET /admin/login` | public | browser login form |
| `/admin/*` | admin session | the JSON API below |

Both `/admin` and `/admin/` are gated by a session (`JSESSIONID`) **and** the
`users.admin` flag. A request with no session gets `401`; a signed-in non-admin
gets `403 {"error":"forbidden"}`.

## Bootstrapping the first admin

There is no admin until one is granted:

```sh
untisctl -db data/untis.db users admin --user evan          # on (default)
untisctl -db data/untis.db users admin --user evan --off    # revoke
```

At server start the same can be done once with `-admin evan,bschneider`
(env `UNTIS_ADMIN`). The flag **only** seeds admins that do not exist yet (a
settings row `admin_bootstrap`); afterwards the `users.admin` column is
authoritative and can be changed from the API.

## Endpoint reference

All admin endpoints are JSON. A `school` in the path (or `?school=`) selects a
school; the default school is used when omitted.

### Status & search

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/admin/status` | counts: users, admins, boosted, editors, recon, pool, schools, tokens, webhooks, ntfy, **outbox** (`pending`/`sending`/`dead`), plus the global switches |
| `GET` | `/admin/search?school=&q=&type=&limit=` | element picker: classes, students, teachers, rooms, subjects; `type` filters one kind, `limit` defaults to 60, max 2000 |
| `GET` | `/admin/perms` | every permission row (`{"perms":[…]}`) |

### Users

| Method | Path | Body / notes |
|---|---|---|
| `GET` | `/admin/users` | username, method, personId/Type, classId/Name, school, admin, displayName, email, lastSeen, effective flags (`boosted`, `editor`, `reconAllowed`, `techniker`) and raw `permissions` |
| `POST` | `/admin/users` | `{username, password?, method?, admin?}` — create or update; `method` defaults to `password`. Granting `admin` also grants `boosted` |
| `POST` | `/admin/users/{u}` | `{feature, allowed}` to grant/revoke `recon`/`boosted`/`editor`/`techniker`; or `{admin:true|false}` |
| `DELETE` | `/admin/users/{u}` | delete user + secret + overrides + personal tokens |

A `key`-method account whose password is a valid base32 secret is stored in the
`secrets` table as the replay key; anything else goes through the account
password path.

### Pool & schools

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/admin/pool[/{school}]` | pooled classes and their owner |
| `GET` | `/admin/schools` | registered schools (with pool/recon counts) |
| `POST` | `/admin/schools/{name}` | register a school (idempotent) |

### Calendar tokens

| Method | Path | Body / notes |
|---|---|---|
| `GET` | `/admin/tokens[/{school}]` | list tokens with resolved `elementName`, `days`, `createdAt`, `lastAccess`, `createdBy` |
| `POST` | `/admin/tokens` | `{elementType, elementId, timezone?, days?}` — create/reuse a token for any CLASS/TEACHER/ROOM/SUBJECT/STUDENT |
| `POST` | `/admin/tokens/{token}` | `{days}` — change the horizon |
| `DELETE` | `/admin/tokens/{token}` | revoke |

### Webhooks & ntfy

| Method | Path | Body / notes |
|---|---|---|
| `GET` | `/admin/webhooks[/{school}]` | list |
| `POST` | `/admin/webhooks` | `{school, url, secret?}` + target `classId` (legacy) or `elementType`/`elementId` |
| `POST` | `/admin/webhooks/{id}/test` | one test delivery |
| `DELETE` | `/admin/webhooks/{id}` | remove |
| `GET` | `/admin/ntfy[/{school}]` | list with resolved element `name` |
| `POST` | `/admin/ntfy` | `{school, topic, baseUrl?}` + target `classId` or `elementType`/`elementId` |
| `POST` | `/admin/ntfy/{id}/test` | one test publish |
| `DELETE` | `/admin/ntfy/{id}` | remove |

See [04](04-notifications.md) for targeting and delivery.

### Outbox

| Method | Path | Notes |
|---|---|---|
| `GET` | `/admin/outbox` | `{"pending","sending","dead","failed":[…]}` |
| `GET` | `/admin/outbox?state=dead` | only exhausted deliveries |

The `failed` list omits payloads (a blob of timetable data is useless for
diagnosis) and gives school, class, version, destination, attempts, last error
and created time.

### Recon

| Method | Path | Notes |
|---|---|---|
| `GET` | `/admin/recon[/{school}]` | per-class scan progress: `target`, `refreshDays`, class count, scanned, stale, oldest horizon, `perClass` |
| `POST` | `/admin/recon/rescan[/{school}]` | forget scan horizons and re-enumerate every pooled class from the year start |

### Rooms

| Method | Path | Notes |
|---|---|---|
| `GET` | `/admin/rooms?school=` | `{"rooms":{name:id},"texts":[…]}` — the override map plus event room texts not yet mapped |
| `POST` | `/admin/rooms?school=` | `{rooms:{name:id}}` — replace the map (normalized: lowercased names, positive ids only) |

See [07 — Room overrides](07-student-events.md#room-overrides).

### Student events & the absence register

These live under `/api/admin/events…` rather than `/admin/…`, but use the same
admin session. Full reference: [07](07-student-events.md).

## Self-service vs. admin

Several surfaces exist in both forms:

| Concern | Self-service | Admin |
|---|---|---|
| Webhooks | `/api/webhooks` (own class / privileged) | `/admin/webhooks` (any) |
| ntfy | `/api/ntfy` (own class/student / privileged) | `/admin/ntfy` (any) |
| Calendar tokens | `POST /api/calendar/token` (own targets) | `/admin/tokens` (any element) |

Everything admin can do is a superset of the self-service form. Admin does **not**
imply `editor`: an admin who wants to write into Untis also needs the `editor`
flag (see [01](01-permissions.md)).
