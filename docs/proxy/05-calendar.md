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
| `{"classId":5000}` | a class | class must be in the pool |
| `{"personal":true}` | your own person | — |
| `{"personId":5006}` | your own person | must equal your person id |
| `{"teacherId":123}` | a teacher | `recon` or `boosted` |
| `{"roomId":456}` | a room | `recon` or `boosted` |
| `{"subjectId":789}` | a subject | `recon` or `boosted` |

Optional: `{"timezone":"Europe/Berlin"}` (default), `{"days":30}`
(default `30`, clamped to `365`).

Minting is **idempotent per target**: asking again returns the same token
(`ClassTokenForClass` / `ClassTokenForPerson` / `ClassTokenForElement`). Response:

```json
{"type":"class","id":5000,"name":"10b","classId":5000,
 "token":"7aff8e9dd4707fde8c992c3902be0c96",
 "url":"https://<host>/api/calendar/7aff8e9dd4707fde8c992c3902be0c96.ics",
 "timezone":"Europe/Berlin","days":30,"horizon":"2026-11-10",
 "created":1750000000,"lastUsed":1750000000,"createdBy":"jdoe"}
```

The feed URL is always **https**, even when read over plain HTTP, because a
subscription is meant to be pasted into a calendar client.

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
| Revocation | delete the token row (dashboard *Tokens* section or `untisctl`) |
| Usage | `lastUsed` is bumped on every `.ics` / week-page hit |
| Transfer | the URL is a bearer credential; anyone with it reads the timetable |

## Related

- [07 — Student events](07-student-events.md): the only target type that can
  carry per-student custom events on a feed.
- [08 — Admin API](08-admin-api.md): list/revoke tokens.
- [10 — `untisctl`](10-untisctl.md): `untisctl calendar` generates feed links,
  honouring `SetPublicBase`.
