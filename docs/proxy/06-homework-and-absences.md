# 06 — Homework & absences

Two proxy-local overlays in this area:

1. **Homework flags** — a student's own "done" mark, kept *beside* the teacher's
   completion state.
2. **Absence enrichment** — derived metadata plus the student's own private note
   on a real Untis absence.

Both are keyed by the **session user**, never by a value in the request body.

## Homework

Untis' `homeWorks[].completed` is the **teacher's** decision about the whole
class: the proxy passes it through untouched and **never writes it**. The
student's own answer lives in the proxy, keyed by `(school, viewer, homeworkId)`,
and is attached to the homework wherever upstream already returns it.

### Enrichment

For the viewer's own responses, every `homeWorks[]` entry gains two fields:

```json
{ "id": 1001, "completed": false, "...": "...",
  "done": true, "doneAt": "2026-10-01T12:34:56Z" }
```

- `done: true` + `doneAt` when the student marked it done.
- `done: false` + `doneAt: null` otherwise — an explicit false is easier to
  branch on than a missing field, and it documents that the proxy considered the
  assignment.

This decoration happens for the student's own `getHomeWork2017` and
`getPeriodData2017` responses. It is **not** applied to a class-scoped editor
request that was replayed as a boosted teacher (that response is not the
viewer's own data).

### The endpoints

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

`GET` lists only the flags that are set (`done: true`), sorted by homework id.
`POST` is idempotent: `done:false` clears the flag. A `username` field in the
body is **accepted and ignored** — a client that sends one out of habit still
behaves correctly and can never redirect the write at somebody else.

`doneAt` is RFC3339 UTC.

## Absences

`getStudentAbsences2017` returns rich but unreadable records: a class *id*, a
reason *code*, and a date range — nothing saying which weekday it was or which
lesson it displaced. The proxy adds everything **alongside** the upstream fields,
never in place of them.

### Derived metadata

Each of the viewer's own absences gains a `derived` block (omitted when nothing
could be derived honestly):

```json
{ "id": 300001, "studentId": 5006, "klasseId": 5000,
  "startDateTime": "2026-10-01T08:00", "endDateTime": "2026-10-01T08:45",
  "absenceReasonId": 3,
  "note": "bring workbook", "noteUpdatedAt": "2026-10-01T12:34:56Z",
  "derived": {
    "classId": 5000, "className": "10b",
    "weekday": "Thursday", "date": "2026-10-01",
    "subject": "Mathematik 3",
    "reason": "krank"
  } }
```

| Field | Source | Rule |
|---|---|---|
| `classId` / `className` | `klasseId` + masterData | |
| `weekday` / `date` | `startDateTime` | |
| `subject` | the **single** lesson the absence overlaps | if it overlaps **zero or more than one** lesson, `subject` is omitted — a whole-day absence has no honest single subject |
| `reason` | `absenceReasonId` → masterData reason text | first non-empty of `longName`/`displayText`/`text`/`name` |

Two hard rules:

- **A note is never attached to somebody else's absence.** The proxy reads the
  `studentId` off each entry and leaves the entry completely undecorated if it
  disagrees with the viewer. `getStudentAbsences2017` is deliberately *not* a
  class-scoped method, so it is never replayed as a teacher — there is no code
  path from a teacher's response to a note lookup.
- **Derived metadata degrades to absent, never to a guess.**

### Notes API

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

`absenceKey` is the upstream absence `id`. An empty/whitespace-only `note`
**clears** it (returns `null`); the maximum length is **2000** characters.
`GET` returns only the notes that are set, sorted by key. As with homework, a
`username` in the body is ignored.

## Do not confuse this with the event-absence register

`/api/absence/notes` is a student's **private note on a real Untis absence**
(this page). The Technik **event-absence register** ([07](07-student-events.md))
is something else: a technician ticking off attendance on a **proxy event**,
answered through the ordinary intern absence methods and stored entirely
proxy-local.
