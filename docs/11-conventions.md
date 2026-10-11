# 11 — Formats & conventions

Cross-cutting rules shared by the WebUntis APIs.

## Dates and times

| Context | Format | Example |
|---|---|---|
| Public JSON-RPC / legacy REST dates | `YYYYMMDD` | `20261005` |
| Public JSON-RPC times | `HHMM` / `Hmm` | `800`, `1345` |
| Intern `*2017` methods | ISO `yyyy-MM-dd` | `2026-10-05` |
| `api/public/timetable/weekly/data` | ISO `yyyy-MM-dd` | `2026-10-05` |
| Extern Timetable v3 & Platform API | ISO 8601 date-time | `2026-10-05T08:50:00` |

⚠️ **The date/time ambiguity is the top compatibility bug:**

- Servers emit dates as a JSON number *or* a string depending on version —
  accept both.
- Times appear as `Hmm` and `HHmm`; pad to four digits, then split into `HH:mm`.
- 8-digit dates (`YYYYMMDD`) are safe to slice.

## Element / resource types

JSON-RPC element types:

| Type | Meaning |
|---|---|
| `1` | Class (Klasse) |
| `2` | Teacher |
| `3` | Subject |
| `4` | Room |
| `5` | Student |

⚠️ Some community libraries swap room/student; verify per server. The extern
Timetable API uses the clearer enum `CLASS, ROOM, STUDENT, TEACHER, LESSON,
PERIOD` instead of numbers.

Person types (from `authenticate`): `2` = teacher, `5` = student.

## Days of the week

`getTimegridUnits` uses `1 = Sunday … 7 = Saturday` (ISO would be
`1 = Monday`). Watch for the off-by-one when mapping to a calendar.

## Colors

`RRGGBB` without a leading `#`, e.g. `000000`. Empty colors are **omitted**, not
`null`.

## Dates vs. school years

Most student data (homework, absences, view-API content) is scoped to the
school year of the session. Cross-year reads return HTTP 200 with empty
collections until the session school year is switched — see
[08](08-legacy-rest.md).

## Error codes

> Reverse-engineered / community-observed; the code space is **not** officially
> enumerated.

### JSON-RPC

| Code | Meaning |
|---|---|
| `-8509` | Not authenticated / session invalid |
| `-8520` | Not authorized / invalid credentials (also used for permission errors) |
| `-8504` | Bad credentials (observed in some libraries) |

Authentication and permission errors can also arrive as a JSON-RPC `error`
object *or* as a successful `result` containing an error code, depending on
server version.

### REST

- View API: auth failures are frequently masked as **404**; error bodies nest as
  `data.error.data.messageKey`.
- Extern Timetable API: minimal RFC 7807 (`{ title, status, detail }`).
- Platform API: `{ errorCode, errorMessage, requestId, traceId }` (+
  `validationErrors[]`).

## Cookies

| Cookie | Value |
|---|---|
| `JSESSIONID` | Session id from `authenticate` / intern login |
| `schoolname` | `_<base64(school)>` (leading underscore literal) |

## `id` fields

JSON-RPC requests carry an opaque `id` echoed back in the response. There is no
requirement that it be numeric; `python-webuntis` and others use incrementing
integers.

## Content types

- JSON-RPC: `application/json` (some servers accept `text/plain`).
- Intern login historically sent `application/json-rpc` and an `okhttp/…`
  user agent.
