# 04 — Notifications (webhooks & ntfy)

Every detected [change](03-change-detection.md) is fanned out to subscribed
**webhooks** and **ntfy topics**. Both share one targeting model, one JSON
payload, and one durable delivery queue (the *outbox*).

## Targeting

A subscription watches **one element** or the **whole school**:

| Target | Webhook / ntfy config | Fires when… |
|---|---|---|
| School-wide | no element, `classId 0`, empty `elementType` | any class in the school changes |
| Class | `classId: 5000` (legacy) or `elementType:"CLASS", elementId:5000` | that class changes |
| Student | `elementType:"STUDENT", elementId:<personId>` | a change touches the student's class |
| Teacher | `elementType:"TEACHER", elementId:<id>` | a changed row's resolved teacher name equals that teacher |
| Room | `elementType:"ROOM", elementId:<id>` | a changed row's resolved room name |
| Subject | `elementType:"SUBJECT", elementId:<id>` | a changed row's resolved subject name |

Matching is evaluated in memory (`elementMatches`) against targets resolved
*before* the snapshot transaction opens — the store's single connection is
already held by that transaction, so nothing may query inside it. A change with
an unresolvable target simply does not match; a destination created in the tiny
gap between the resolve pass and the commit does not get that one change.

## The change payload

Delivered to webhooks and embedded in the ntfy envelope:

```json
{
  "event": "change",
  "school": "testschool",
  "classId": 5000,
  "version": 4,
  "summary": "10b · 2 changes: 1 added · 1 changed",
  "digest": { "title": "10b · 2 changes", "summary": "…", "lines": ["…"],
              "changed": 1, "added": 1, "removed": 0 },
  "changes": [
    { "PeriodID": 123456, "Kind": "ADDED",
      "Start": "2026-09-07 08:00", "End": "2026-09-07 08:45",
      "Subject": "M", "Room": "101", "Teacher": "Willner",
      "Description": "", "ModVer": 4 }
  ]
}
```

`Kind` is `ADDED`, `CHANGED` or `REMOVED`. The `changes` rows are Go-marshaled
`PeriodRow` values, so the field names are exported (`PeriodID`, `Kind`, …).

### Webhook headers

| Header | Value |
|---|---|
| `Content-Type` | `application/json` |
| `User-Agent` | `untis-proxy/1.0` |
| `X-Untis-Event` | `timetable-change` (or `test`) |
| `X-Untis-Summary` | single-line, ASCII-transliterated digest summary |
| `X-Untis-Signature` | `sha256=<hex HMAC-SHA256(body, secret)>`, only if a secret is set |

Verify the signature by recomputing the HMAC over the **raw body bytes** with
the shared secret and comparing in constant time.

```
X-Untis-Signature: sha256=9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08
```

`X-Untis-Summary` is forced to single-line printable ASCII with umlauts
transliterated (`ä→ae`, `→→->`), because headers may be read as latin-1.

### ntfy envelope

A matched topic is published as a **JSON envelope to the ntfy server ROOT**
(`https://ntfy.sh/` or the topic's `baseUrl`), *not* to `/<topic>`:

```json
{
  "topic": "schl123-klasse5000",
  "title": "10b · 2 changes",
  "message": "added: Thu 02.10. 08:00–08:45 · Mathe · R112 · Müller\n… and 6 more",
  "tags": ["calendar"],
  "click": "https://proxy.example.org/api/timetable/changes"
}
```

> Posting the JSON envelope to `/<topic>` makes the server treat the body as
> literal message text — every notification then arrives as a wall of raw JSON.
> The root URL is required (see ntfy's "publish as JSON" docs).

The `title` is the digest title; for an element-scoped topic the element name is
prepended (`Timetable change — room 01-Aula`). The `message` is the multi-line
digest, truncated at 8 lessons with `… and N more`.

## The outbox — durable, retrying delivery

The version bump that records a change and the notification announcing it must
not be able to disagree. So:

- **Enqueue inside the transaction.** Every matching destination gets **one
  outbox row** written in the same transaction that stamps the new version. A
  committed change always has a delivery waiting; a crash cannot lose it.
- **One row per destination, not per change.** A permanently unreachable
  receiver cannot cause healthy receivers to be replayed forever.
- **Worker with backoff.** `StartOutboxWorker` drains due rows every `5s`.
  A failed attempt is retried after `30s`, doubling each attempt, capped at
  `15m`, up to **8 attempts** (`outboxMaxAttempts`); the last attempt lands
  roughly 25 minutes after the first.
- **Dead rows.** After 8 attempts the row is parked as `dead` and never retried.
  It is kept for **7 days** for inspection, then pruned hourly. A dead row names
  school, class, version, destination and error.
- **Crash recovery.** On startup, rows abandoned in `sending` are released and
  retried.
- **Deleted subscriptions** drop their queued backlog rather than retrying a
  destination removed on purpose.

### Inspecting the backlog

Admin only (`GET /admin/outbox`, see [08](08-admin-api.md)):

- `?state=dead` — only exhausted deliveries.
- `GET /admin/status` includes `outbox.{pending,sending,dead}`.

`pending` growing steadily means the worker cannot keep up or a destination is
failing; `dead > 0` means a destination gave up. The public `/healthz` and
`/status` stay aggregate-only and never name a failing school or destination —
outbox detail needs an admin session or the gated metrics listener.

## Self-service subscriptions

Session required; a plain user may only touch their **own class** and, for ntfy,
their **own student** target. `editor`/`boosted`/admin may also touch any pooled
class and school-wide (`classId 0`) subscriptions. Created rows remember
`createdBy`, and only the creator (or a privileged user) may test/delete them.

`GET /api/webhooks`, `POST /api/webhooks`, `DELETE /api/webhooks/{id}`,
`POST /api/webhooks/{id}/test`, and the parallel `/api/ntfy…` routes are
documented in [02](02-endpoints.md#notifications--self-service-subscriptions).
Every subscription can also be managed from the dashboard's *Webhooks* / *ntfy
topics* sections ([08](08-admin-api.md)).

Creation validates the destination URL (`validateTargetURL`); publishing to a
private address is refused unless `-allow-private-targets` is set
([09](09-configuration.md)). ntfy `baseUrl` overrides are trimmed of trailing
slashes so duplicate rows do not accumulate.

## Testing a destination

`POST /api/webhooks/{id}/test` performs **one** delivery with the real headers
(same HMAC signature) but an `event:"test"` body; it is deliberately **not**
retried and returns `{"ok":true,"status":<httpStatus>}` or an error.
`POST /api/ntfy/{id}/test` publishes a test envelope (title, tags, priority,
click) so the dashboard button proves the whole render path, not just the
socket. Both accept a `status` from the receiver; a non-2xx is reported.

## Why student events are *not* webhooks/ntfy

A student's private events deliberately bypass this whole pipeline — they are
neither class changes nor safe to broadcast. See
[07](07-student-events.md#why-events-bypass-the-outbox).
