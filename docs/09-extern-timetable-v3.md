# 09 — External Timetable API (v1/v2/v3)

> 🟢 **Official** — *WebUntis Timetable API*, published by Untis GmbH. See
> [`specs/README.md`](../specs/README.md) for the machine-readable spec link.

Gets all data needed to display a timetable; filters by resource
(student, teacher, room, class, lesson, or period); includes either all periods
or only changed ones; and merges the scheduled and current (substitution) state.

## Versions

| Version | Path | Notes |
|---|---|---|
| v1 | `/api/rest/extern/v1/timetable` | Deprecated |
| v2 | `/api/rest/extern/v2/timetable` | Deprecated |
| **v3** | `/api/rest/extern/v3/timetable` | **Current** |

The same path exists on the central gateway (`https://api.webuntis.com/...`) and
on a tenant server (`https://<server>.webuntis.com/...`).

## Authentication

Uses the Untis Platform OAuth2 client-credentials token (or, historically, a
per-tenant API key). See [10 — Untis Platform API](10-platform-api.md).

## Request

```http
GET /WebUntis/api/rest/extern/v3/timetable
    ?start=2026-10-05T00:00:00
    &end=2026-10-11T00:00:00
    &class=123
    &includeStudents=false
```

### Filters

At least one of *changes-only*, *Untis ids*, or *external ids* is required.

| Parameter | Type | Notes |
|---|---|---|
| `start` | date-time | **required**; must be in the same school year as `end` |
| `end` | date-time | **required** |
| `limit` | int32 | pagination size; 0 = no limit |
| `offset` | int32 | 1-based skip; 0 = no pagination |
| `includeStudents` | bool | include period students |
| `dateLastModifiedAfter` | date-time | return only periods changed since this timestamp |
| `period`, `lesson`, `class`, `room`, `student`, `teacher` | int64 arrays (≤50) | filter by WebUntis entity id |
| `lesson_ext`, `class_ext`, `room_ext`, `student_ext`, `teacher_ext` | string arrays | filter by external id (no `period_ext`) |

## Response — `TimetableDto`

```jsonc
{
  "version": "1.12.0",
  "headerData": {
    "created": "2026-02-18T07:45:00",
    "user": "Meier",
    "school": { "tenantId": "1004400", "name": "BG/BRG Stockerau" },
    "schoolYearStart": "2026-09-01",
    "schoolYearEnd": "2027-06-30",
    "filter": { "start": "…", "end": "…", "limit": 0, "offset": 0,
                "filterByChanges": { "dateLastModifiedAfter": "…" },
                "filterByResource": [ { "resourceType": "CLASS", "id": 123 } ] }
  },
  "masterData": {
    "classes": [ ClassDto ], "departments": [ … ], "rooms": [ RoomDto ],
    "studentgroups": [ … ], "students": [ StudentDto ],
    "subjects": [ SubjectDto ], "teachers": [ TeacherDto ]
  },
  "timetableData": {
    "timeGrid": { … },
    "periods": [ PeriodDto, … ]
  }
}
```

### `PeriodDto` (subset)

| Field | Type | Notes |
|---|---|---|
| `id` | int64 | required |
| `type` | enum | `NORMAL_TEACHING_PERIOD, ADDITIONAL_PERIOD, STAND_BY_PERIOD, OFFICE_HOUR, EXAM, BREAK_SUPERVISION, EVENT, MEETING` |
| `status` | enum | `REGULAR, CANCELLED, ADDITIONAL, CHANGED` |
| `start`, `end`, `modified` | date-time | ISO 8601 |
| `lesson` / `lesson_ext` | int64 / string | |
| `timegridId` | int64 | |
| `relatedPeriod` | int64 | other side of a moved period |
| `icons` | enum[] | |
| `exam` | `ExamDto` | `{ id, type, name }` |
| `departments`, `classes`, `studentgroups`, `subjects`, `rooms`, `teachers`, `students` | `PeriodResourceDto[]` | each `{ id, status }` |
| `periodText`, `substText`, `lessonText`, `lsnumber`, `info` | string | |

`ResourceStatusEnum` ∈ `REGULAR, ADDED, REMOVED`.

### Enum quick reference

- `FilterResourceTypeEnum`: `CLASS, ROOM, STUDENT, TEACHER, LESSON, PERIOD`.
- `PeriodStatusEnum`: `REGULAR, CANCELLED, ADDITIONAL, CHANGED` (note: the
  filter enum spells the third value `ADDED`; the status enum is `ADDITIONAL`).
- `ResourceStatusEnum`: `REGULAR, ADDED, REMOVED`.

### Consuming the response (per the official description)

1. Take all periods whose `status` is **not** `CANCELLED`.
2. For each, keep resources whose status is `REGULAR` or `ADDED`.
3. Resolve each referenced id in `masterData`.
3. Render by joining `start`/`end` and the referenced resources.

## Incremental sync

Poll both the timetable and the changes endpoint with the **same**
`dateLastModifiedAfter`, and advance the watermark only when both succeed:

```
GET /api/rest/extern/v3/timetable?dateLastModifiedAfter=<ts>&start=…&end=…
GET /api/rest/extern/v3/timetable/deleted-periods?dateLastModifiedAfter=<ts>
```

`deleted-periods` reports periods removed since the timestamp.

## Errors

RFC 7807-style, minimal:

```json
{ "title": "…", "status": 400, "detail": "…" }
```

Standard HTTP status codes apply (`400`, `401`, `403`, `404`, `500`).

## Notes

- A period may be returned twice for a moved lesson: the cancellation and the
  new placement are linked via `relatedPeriod`. If a period is moved twice, only
  the last two are related.
- Prefer external ids (`*_ext`) when the surrounding system owns the keys.
