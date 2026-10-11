# 07 — Student events (Technik)

Admins can place **dated entries on one student's timetable** — "Technik"
appointments, extra duties, room bookings — that exist nowhere in Untis. The
proxy stores them, overlays them onto that student's own timetable, and offers a
role (`techniker`) for the coordinator who needs to see them all at once.

Everything here is **proxy-local**: nothing is ever written to Untis.

## Data model

A student event is `(school, username, date, startTime, endTime, title, subject,
room, teacher, description)` plus `createdBy`, `createdAt`, `updatedAt` and a
`revision` that increments on every edit. The `revision` is what an `.ics` client
sees as `SEQUENCE`.

- **Stored per student, keyed by the folded username** — so a batch handed to
  five technicians is five rows, not one shared row. A shared row could not be
  read as one student's without leaking it to another.
- **A student who has never logged in** still gets their event, filed under the
  folded short code (`eventKey`). The day they log in, their appointments appear
  with no second import.
- `title` is required; `subject` defaults to **Technik** so the lesson cell is
  never blank; `date` must be `YYYY-MM-DD`; times `HH:MM`; and `endTime`
  strictly after `startTime`.

## Admin API

Admin session only (the gate runs before the method is dispatched, so a
non-admin's response is identical whatever they asked for).

| Route | Method | Purpose |
|---|---|---|
| `/api/admin/events?username=<name>` | GET | list one student's events (a username is **required**), sorted by date then start |
| `/api/admin/events` | POST | create |
| `/api/admin/events/{id}` | PATCH | edit one or more fields (validated against the **merged** row) |
| `/api/admin/events/{id}` | DELETE | remove (idempotent) |
| `/api/admin/events/import?school=<s>` | POST | bulk import (CSV/JSON) |
| `/api/admin/events/absences?school=<s>&from=&to=` | GET | the event-absence register |
| `/api/admin/events/absences` | PATCH | correct a register row |
| `/api/admin/events/absences/log?school=<s>&from=&to=` | GET | append-only register changelog |

### Create

```json
POST /api/admin/events
{"username":"dee","date":"2026-10-01","startTime":"14:00","endTime":"15:00",
 "title":"Technik","subject":"Mathe","room":"R12","teacher":"Mr Smith",
 "description":"Arbeitsblatt mitbringen"}
```

`username` may be replaced by `usernames: [..]` for a **batch**; every target is
validated before anything is written, so a batch lands for all or none. Duplicate
slots (same student, date and time window) are **skipped**, not created twice,
and the skip is reported so the admin sees the slot was already covered. A single
student keeps the single-object response shape; a batch returns
`{"created":[…],"skipped":[…]}`.

`username` must exist in that school as a **student** (PersonType 5) —
otherwise `404`. An event filed against a typo, or against a teacher account
(whose timetable has no viewer), would sit in the table forever.

### Reads

The read side is deliberately *not* a public "list events" endpoint: events reach
a student only through surfaces that already know who is asking — a student's own
`getTimetable2017`, their personal `.ics` feed, and their `/week` page.

### Why events bypass the outbox

Every webhook and ntfy destination is scoped to an element or a whole class, and
everyone who can read that class can read those messages. A student's private
appointment announced there would reach every classmate. So student events
deliberately **do not** go through the outbox, webhooks or ntfy. Instead:

| Mechanism | Scope |
|---|---|
| `GET /api/timetable/changes?sinceEvents=N` | `eventVersion`, private to the session user |
| `GET /api/timetable/stream` → `event: student-events` | same counter, for that user only |

Both move on create, edit **and delete** (the delete is the case a counter
derived from the rows could not catch), and carry only the counter and a reason
(`created`/`updated`/`deleted`) — never the event's content. The client refetches
through a surface it already authenticated for.

## Who sees a student's events

| Viewer | Sees |
|---|---|
| the owning student | their own events on their timetable, `/week`, and personal `.ics` |
| an **admin** | the CRUD API |
| a user with **`techniker`** | all of the above for every student, via the synthetic *Technik* class, room/teacher overlays, and the event-absence register |

### The synthetic "Technik" class

The proxy injects a class named **Technik** (id `syntheticElementBase`, below
2³¹ so a 32-bit client can hold and send it back) into masterData for
`techniker` users, and answers `getTimetable2017` for it with the **union of
every student's events** in the requested range:

- Each period is labeled with the assigned student so a class full of
  appointments reads at a glance (owner name on the substitution line,
  description on the lesson line).
- Events that share an appointment (same date/time/title/room) are **merged**
  into one row listing every assigned student.
- The synthetic class is added by bumping masterData's `timeStamp`, so a client
  that logged in before the permission was granted still picks it up.
- The aggregate is **permission-gated on every request** (`serveTechnikClass`),
  so revoking `techniker` takes effect without a re-login; everyone else's
  responses are byte-for-byte unchanged.

`techniker` is independent of admin/`editor`/`boosted`/`recon`.

### Room & teacher overlays

An event's free-text room/teacher is resolved to the same element ids real
lessons use, so it appears on the **room** and **teacher** timetables too:

- the school's masterData catalogue is the normal source of truth;
- **room overrides** (below) win over the catalogue;
- a name found in neither is still **synthesized**, so the event never
  disappears just because its room is unknown.

### The event-absence register

A proxy event is not a real lesson: it has no upstream `ttId`, no class register
and no absence record. The official app still offers its absence editor on any
period whose `can` list carries `READ/WRITE_STUD_ABSENCE`, and a technician needs
exactly that — a way to tick off who showed up.

The proxy answers the app's four methods for a synthetic period **entirely from
its own store**, intercepting them before the editor write-gate (a technician
writes a local note, so needs neither `editor` nor a teacher account):

| App method | Proxy behaviour |
|---|---|
| `getPeriodData2017` | returns the appointment's roster (`referencedStudents`), recorded absences and whether the register was submitted; **merged** with a real call if the request mixes ids |
| `createImmediateAbsence2017` | records a student absent from the appointment; returns a `StudentAbsence` with a **synthetic negative id** the app deletes with later |
| `deleteAbsence2017` | removes a local absence (a non-local id still forwards to Untis) |
| `submitAbsencesChecked2017` | records that the register was submitted |

Synthetic ids live in reserved ranges (`eventAbsenceIDSpace`,
`syntheticPersonIDBase`) so they can never collide with a real Untis id. Every
change is appended to an **append-only changelog** — there is no delete
counterpart, by design.

Admin read/correct surfaces:

```json
GET /api/admin/events/absences?school=…&from=…&to=…
{
  "appointments": [
    { "appointmentKey": "…", "date": "2026-10-01",
      "startTime": "14:00", "endTime": "15:00",
      "title": "Technik", "subject": "Technik", "room": "R12",
      "checked": true,
      "roster": [ {"username":"dee","displayName":"…","absent":true,"startTime":"14:00","endTime":"15:00"} ] }
  ],
  "absences": [ … ]
}
```

A student on the roster with `absent:false` is the "was there" side, which the
absence table alone could not otherwise show. `PATCH /api/admin/events/absences`
corrects a window and/or moves an absence to another **assigned** student
(`newUsername`), logging the correction. The appointment must still exist on that
date, so an edit can never resurrect an absence for a deleted event.

## Import (transport-calendar export)

```
POST /api/admin/events/import?school=<s>
```

The body is the export itself: **JSON** when it starts with `{`, otherwise the
semicolon **CSV**. Admin only.

- **JSON**: `{"techniker":[{"name","code"}],"veranstaltungen":[{datum,beginn,
  ende,titel,veranstalter,ort,material,notizen,einsatz:[…]}]}`. With a roster, a
  code that names no technician (a teacher, "SISS Technik") is a **note, not a
  technician on duty**, so no event is filed for it.
- **CSV** — the flat semicolon export. Columns:
  `date;start;end;…;room(7);title(8);description(9);teacher(10);…;codes(12)`.
  A line needs ≥13 fields. Windows-1252 export is decoded; placeholder room
  values (`-`, `/`, `TRUE`, `"keine technik"`, …) become empty.

Codes fold the same way event keys do: lowercased, umlauts folded, punctuation
and a trailing disambiguator dropped, so `AbcDef1 (nur A)` and the login `AbcDef`
match. A code naming **no** account is still filed under the folded code (the
student's future login picks it up). Duplicates (same student/date/window) are
skipped.

The response reports `created`, `skipped` (with `reason`), `unknown` codes and
ignored codes, so an import is auditable. Every created event announces a
`created` change to that student's private counter.

## Room overrides

Admins can pin event room text to an exact Untis room id, per school
(dashboard *Rooms* section → `GET`/`POST /admin/rooms`). The map is stored as
JSON under the setting key `room_overrides:<school>` and takes effect on the next
request without a restart.

- Names are **lowercased and trimmed**, so `"01-Aula"`, `"Aula"` and `" aula "`
  cannot become three different keys; non-positive ids are dropped.
- An override beats both the school catalogue and the synthetic fallback, which
  matters when a name is ambiguous (a retired "Aula") or absent from a cold
  masterData cache.

## `.ics` and `/week`

A **personal/student** calendar feed ([05](05-calendar.md)) appends that
student's events as extra `VEVENT`s. Class/teacher/room/subject feeds cannot,
because those have no single username to read a student's private events from.

The `/week/{token}` page renders custom events inline (own title and
description, marked as custom).
