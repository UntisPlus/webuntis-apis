# 05 — Calendar subscriptions

The proxy turns any timetable into a subscribable **iCalendar** (`.ics`) feed
plus a server-rendered **week page**, both addressed by one opaque token.
Possession of the token *is* the credential — treat it like a password.

## Minting a token

```
POST /api/calendar/token
```

Session required. The body names **exactly one** target:

| Body | Target | Access needed |
|---|---|---|
| `{"classId":5000}` | a class | class in the pool, or `boosted`/staff |
| `{"classId":2000000000}` | the synthetic **Technik** aggregate class | `techniker` |
| `{"personal":true}` | your own person | — |
| `{"personId":5006}` | your own person | must equal your person id |
| `{"teacherId":123}` | a teacher | `recon`, `boosted`, or staff |
| `{"roomId":456}` | a room | `recon`, `boosted`, or staff |
| `{"subjectId":789}` | a subject | `recon`, `boosted`, or staff |

Optional: `{"timezone":"Europe/Berlin"}` (default), `{"days":30}`
(default `30`, clamped to `365`).

The access column mirrors the app's `masterData` visibility exactly: a plain
student gets the pooled classes and their personal timetable; `recon` adds the
reconstructed teachers/rooms/subjects; `boosted` and *staff* (non-student)
accounts keep stock WebUntis visibility (every element); `techniker` adds the
synthetic **Technik** class (`id 2000000000`, the union of every student's
events).

Minting is **idempotent per target per user**: asking again as the same user
returns that user's token, but a token an operator minted for the element (via
`untisctl` or `/admin/tokens`) is **never** handed to (or silently reused by) an
app user. Each caller gets a token they own, so it shows up in their
`GET /api/calendar/tokens` list and only they can revoke it. Response:

```json
{"type":"class","id":5000,"name":"10b","classId":5000,
 "token":"7aff8e9dd4707fde8c992c3902be0c96",
 "url":"https://<host>/api/calendar/7aff8e9dd4707fde8c992c3902be0c96.ics",
 "timezone":"Europe/Berlin","days":30,"horizon":"2026-11-10",
 "created":1750000000,"lastUsed":1750000000,"createdBy":"jdoe"}
```

The feed URL is always **https**, even when read over plain HTTP, because a
subscription is meant to be pasted into a calendar client.

## Discovery and self-service

A client does not have to guess ids from `masterData`: the proxy exposes exactly
the targets a user may subscribe to, and lets them manage their own tokens.

```
GET    /api/calendar/options   # what you can subscribe to
GET    /api/calendar/tokens     # the tokens you created
PATCH  /api/calendar/{token}    # change the lookahead window
DELETE /api/calendar/{token}    # revoke a token
```

`GET /api/calendar/options` mirrors the `masterData` display flags the login
rewrite sets, so it never advertises something the app would not also show:

```json
{"school":"myschool",
 "personal":{"personId":5006,"name":"Jane Doe"},
 "class":[{"id":5000,"name":"10b"}],
 "teacher":[{"id":123,"name":"Herr Müller"}],
 "room":[],
 "subject":[],
 "technik":{"id":2000000000,"name":"Technik"}}
```

`class`/`teacher`/`room`/`subject` are always present (possibly `[]`);
`personal` is present when the account has a person id; `technik` only for a
`techniker`. Fields:

- **everyone** — the pooled classes (`class`) + own personal timetable;
- **`recon`** — the teachers/rooms/subjects the recon scan actually enumerated;
- **`boosted` / staff** — every class/teacher/room/subject;
- **`techniker`** — the synthetic Technik class.

`GET /api/calendar/tokens` returns only the caller's own tokens (matched on
`created_by`), each in the same shape as the mint response. `PATCH` takes
`{"days":90}` (clamped `[1,365]`, default `30`) and `DELETE` removes the token —
both **owner-checked**: a missing token and another user's token both return
`404`. Neither endpoint touches the public `.ics` feed, so revoking takes effect
on the next subscription fetch.

## The `.ics` feed

```
GET /api/calendar/{token}.ics
```

Public by design (token-based). Each request:

1. Looks up the token (404 if unknown or, when `ClassTokenMaxAge` is set,
   expired) and touches `lastUsed`.
2. Resolves the target to a display name + its periods for `[today, today+days]`.
3. Emits one `VEVENT` per period.

Each `VEVENT`:

| Field | Value |
|---|---|
| `UID` | `<periodId>@untis-api` |
| `SEQUENCE` | the relevant version counter (class / school / student) |
| `DTSTART` / `DTEND` | `TZID=<token timezone>` |
| `SUMMARY` | `subject · teacher(s)` |
| `LOCATION` | room(s), comma-joined |
| `DESCRIPTION` | German-labelled multi-line detail (Klasse, Lehrer, Raum, Raumänderung, Fach, Klausur, Thema, Vertretung, Info, Hausaufgabe, Status) |
| `TRANSP:OPAQUE`, `CLASS:PUBLIC` | |

The calendar carries `X-WR-CALNAME: Untis <name>` and
`X-WR-CALDESC: Untis timetable for <name>`, and downloads as
`untis-<id>.ics` / `untis-teacher-<id>.ics` / `untis-room-<id>.ics` /
`untis-subject-<id>.ics`.

A **personal/student** feed additionally carries that student's own
[proxy events](07-student-events.md) as extra events (rendered by
`buildCustomICSVEVENT`). Class/teacher/room/subject feeds cannot: they have no
single username, so there is nowhere those private events could be read from.

A **Technik** feed is the one class-like feed that *does* carry events: it is the
same merged, student-labelled aggregate the app's synthetic Technik class shows,
so a coordinator can subscribe to the whole events calendar. It downloads as
`untis-technik.ics`.

Feed horizons and element names come from the shared `masterData` cache; a
subject's **longName** (`Mathematik 3`) is preferred over its short code (`M3`).

## The week page

```
GET /week/{token}
```

Same token as the feed. Renders a **JavaScript-free** HTML page — one bookmark
for a parent's phone:

- a **rolling 7 days starting today** (not the calendar week: on a Friday
  evening "this week" is nearly over, and what a parent wants is what's coming).
- one column per day, lessons sorted by start time.
- each lesson shows time range, subject, teacher · room · class, and notes
  (Vertretung, Thema, info), with flags for `CANCELLED` / substitution / exam
  (the exam label from `examtype` + `name`).
- custom student events render inline (marked as custom, with their own title
  and description).
- the feed's `Version` is shown, plus a link to the `.ics` URL.

The page is rendered fresh on every request with `Cache-Control: no-store`.
An unreadable timezone falls back to UTC rather than failing.

## Token lifecycle

| Concern | Behaviour |
|---|---|
| Uniqueness | one token per (school, class) / (school, person) / (school, element) |
| Expiry | disabled by default; `SetCalendarTokenMaxAge(d)` bounds it, after which the feed 404s |
| Revocation | delete the token row (`DELETE /api/calendar/{token}` by its creator, the dashboard *Tokens* section, or `untisctl`) |
| Usage | `lastUsed` is bumped on every `.ics` / week-page hit |
| Transfer | the URL is a bearer credential; anyone with it reads the timetable |

## Related

- [07 — Student events](07-student-events.md): the only target type that can
  carry per-student custom events on a feed.
- [08 — Admin API](08-admin-api.md): list/revoke tokens.
- [10 — `untisctl`](10-untisctl.md): `untisctl calendar` generates feed links,
  honouring `SetPublicBase`.
