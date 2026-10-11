# 03 — Change detection

The proxy re-fetches each pooled class on an interval, diffs the result against
the previous snapshot, and — when something moved — bumps that class's version
and fans the change out. This is what powers the [SSE stream](#get-apitimetablestream--sse),
[webhooks and ntfy](04-notifications.md), and the pull-based
[`/api/timetable/changes`](02-endpoints.md).

## Where a version comes from

Version data lives in the `classes` / snapshots / change tables (see the proxy
repo). Three counters exist per school:

- **class version** — incremented by `1` every time a polled class's timetable
  differs from the stored snapshot.
- **school version** — the closest monotonic counter spanning all pooled
  classes; used by teacher/room/subject calendar feeds, whose periods come from
  many classes at once.
- **student event version** — a *separate, per-student* counter, bumped only
  when an admin adds/edits/removes one of that student's
  [events](07-student-events.md). It deliberately does **not** touch the class
  version: one student's private event must never surface to classmates.

Clients re-fetch when **either** the class version or the student event version
moves.

## The poll loop

`StartPollLoop` runs once per default school (`-poll-interval`, default `60s`),
immediately then on every tick. Each pass:

1. Reads the school's pool (every donated class).
2. Calls `pollOnce` → `checkClassErr` for each class.
3. `checkClassErr` fetches the class timetable for a window of **yesterday …
   +4 days** (`-1`/`+4` days) and builds a normalized snapshot row per period
   (`PeriodID`, `Kind`, `Start`, `End`, `Subject`, `Room`, `Teacher`,
   `Description`, `ModVer` — the Go struct has no JSON tags, so the wire form is
   the exported field names, i.e. PascalCase).
4. Opens the snapshot transaction, which compares rows against the stored
   snapshot, drafts add/change/remove rows, bumps the class version, and
   **enqueues one outbox row per matching destination inside the same
   transaction** — so a committed change can never lose its notification.
5. Publishes the change to the in-process SSE hub.

Other schools that auto-register at runtime are picked up on the next tick: the
tick iterates `store.ListSchools()` after the default school.

A healthy poll is one that actually **read** the timetable; a fetch error is
tracked separately so `/healthz` and `/metrics` can report a stale upstream
instead of a silently dead poller (see [09](09-configuration.md)).

## `GET /api/timetable/changes` — polling

Session required; the viewer may only ask for **their own class** (omit
`classId`, or pass one equal to their class).

| Query | Meaning |
|---|---|
| `school` | school (default: server's) |
| `classId` | class id; defaults to the session's class, 403 if different |
| `since` | last-seen **class** version |
| `sinceEvents` | last-seen **student event** version (optional) |

```json
{
  "school": "testschool",
  "classId": 5000,
  "since": 42,
  "current": 43,
  "eventVersion": 7,
  "sinceEvents": 7,
  "summary": "10b · 2 changes: 1 added · 1 changed",
  "digest": {
    "title": "10b · 2 changes",
    "summary": "10b · 2 changes: 1 added · 1 changed",
    "lines": [
      "added: Thu 02.10. 08:00–08:45 · Mathe · R112 · Müller",
      "Thu 02.10. 09:35–10:20 · Sport · room R204 → R112 · Weber"
    ],
    "changed": 1,
    "added": 1,
    "removed": 0
  },
  "changes": [ { "PeriodID": 9001, "Kind": "ADDED", "Start": "...",
                 "End": "...", "Subject": "Mathe", "Room": "R112",
                 "Teacher": "Müller", "Description": "", "ModVer": 4 } ]
}
```

**`304 Not Modified`** is returned when `since == current`, there are no
pending rows, and the event version is unchanged.

> The event version takes part in the 304 decision **only when the client sent
> `sinceEvents`**. A client that never sends it has an unknown last-seen value,
> and treating "absent" as `0` would make `events != 0` forever — answering every
> poll with a full `200` to an app that used to get `304`s. So if you care about
> event changes, send and advance `sinceEvents` yourself.

The `digest` block is the human-readable diff (see below).

## `GET /api/timetable/stream` — SSE

Session required. Streams the requester's own class changes plus their own
student-event changes. Standard **Server-Sent Events**; heartbeat comment every
30s.

```
event: snapshot
data: {"event":"snapshot","school":"testschool","classId":5000,
       "current":43,"changes":[...],"eventVersion":7}

event: change
data: {"event":"change","school":"testschool","classId":5000,
       "version":44,"changes":[...]}

: heartbeat

event: student-events
data: {"event":"student-events","school":"testschool",
       "eventVersion":8,"reason":"create"}
```

- The first message is always a **`snapshot`** so a client can hydrate without a
  separate fetch.
- **`change`** carries the full changed rows for the class.
- **`student-events`** carries **only the counter and a reason** — no title,
> no time. The recipient is expected to re-fetch through a surface it is already
> authenticated for. This is deliberate: a shared class fan-out is exactly the
> wrong place for one student's private data.
- A `:` comment line every 30s is a heartbeat keep-alive.

A client that stops draining a channel is dropped rather than blocking the
admin's request; it recovers by polling, where the event version is still
authoritative.

## The digest (human-readable diff)

`changeDigest` feeds the ntfy body, the `X-Untis-Summary` webhook header and the
`changes` answer:

```json
{"title":"10b · 1 change",
 "summary":"10b · 1 change: 1 changed",
 "lines":["Tue 29.09. 08:00–08:45 · Mathe · room R204 → R112 · Müller · Sub: entfällt"],
 "changed":1,"added":0,"removed":0}
```

- It diffs each changed row against the **previous snapshot**, which is what
  lets it say `room R204 → R112` instead of `1 changed`.
- `Message()` renders at most `digestMaxLines` (`8`) lines, appending
  `… and N more`.
- `Summary` is forced to single-line printable ASCII with German umlauts
  transliterated (`ä→ae`, `→→->`), because `X-Untis-Summary` is an HTTP header.

## Version vs. snapshot: what is stored

The snapshot table is the *only* place the pre-change state exists — so it is
what powers diffs. Rows older than **today** are dropped on each successful poll
(`dropBefore` = today), keeping the snapshot a rolling window.

## Related

- Delivery mechanics (outbox, retries, signatures): [04](04-notifications.md).
- A full re-scan can be forced from the admin API:
  `POST /admin/recon/rescan` ([08](08-admin-api.md)).
