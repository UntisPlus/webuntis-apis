# 04 — Public JSON-RPC API

> 🟡 **Official spec, retransmitted.** This API is specified by an Untis-authored
> PDF titled *WebUntis JSON-RPC API* dated **2018-09-20** that circulates
> third-party. It is the most stable integration surface on the tenant servers.

## Transport

- **URL:** `http(s)://<server>.webuntis.com/WebUntis/jsonrpc.do?school=<school>`
- **Method:** `POST` (mandatory).
- **Body:** JSON-RPC 2.0.
- **Content-Type:** `application/json` (some servers accept `text/plain`).
- **Encoding:** UTF-8.

`<school>` is a mandatory query parameter, equal to the school's login name
(usually the same as the `server` subdomain, but not always — see
[03](03-school-discovery.md)).

## Envelope

Request:

```json
{ "id": "id", "method": "methodName", "params": {}, "jsonrpc": "2.0" }
```

Response:

```json
{ "jsonrpc": "2.0", "id": "id", "result": … }
```

Error:

```json
{ "jsonrpc": "2.0", "id": "id", "error": { "code": -8509, "message": "…" } }
```

`id` is an opaque client-chosen identifier echoed back.

## Authentication

See [02 — Authentication](02-authentication.md). Send `authenticate` first; every
later call carries the `JSESSIONID` cookie. Call `logout` when done.

## Methods

All methods below are 🟡 **official** (2018 spec). `params: {}` means no
parameters.

### Session

| Method | Params | Returns |
|---|---|---|
| `authenticate` | `user`, `password`, `client` | `{ sessionId, personType, personId }` |
| `logout` | `{}` | `{}` |

### Master data

| Method | Params | Returns |
|---|---|---|
| `getTeachers` | `{}` | `[{ id, name, foreName, longName, foreColor, backColor }]` |
| `getStudents` | `{}` | `[{ id, key, name, foreName, longName, gender }]` |
| `getKlassen` | `schoolyearId?` (default: current) | `[{ id, name, longName, foreColor, backColor, did, teacher1, teacher2 }]` |
| `getSubjects` | `{}` | `[{ id, name, longName, foreColor, backColor }]` |
| `getRooms` | `{}` | `[{ id, name, longName, foreColor, backColor }]` |
| `getDepartments` | `{}` | `[{ id, name, longName }]` |
| `getHolidays` | `{}` | `[{ id, name, longName, startDate, endDate }]` |
| `getStatusData` | `{}` | `{ lstypes: […], codes: […] }` (lesson-type & period-code colors) |

### Time & school years

| Method | Params | Returns |
|---|---|---|
| `getTimegridUnits` | `{}` | `[{ day, timeUnits: [{ startTime, endTime, name? }] }]`; `day` 1=Sun … 7=Sat |
| `getCurrentSchoolyear` | `{}` | `[{ id, name, startDate, endDate }]` |
| `getSchoolyears` | `{}` | `[{ id, name, startDate, endDate }]` |
| `getLatestImportTime` | `{}` | Unix timestamp (number). Use to test session validity |

### Timetable

| Method | Params | Returns |
|---|---|---|
| `getTimetable` (simple) | `id`*, `type`*, `startDate?`, `endDate?` | array of period objects |
| `getTimetable` (customizable) | `options` object | array of period objects |
| `getTimetableWithAbsences` | `options.startDate`, `options.endDate` | `{ periodsWithAbsences: […] }` |

\* mandatory.

**Simple period object:** `id, date, startTime, endTime, kl[], te[], su[], ro[],
lstype, code, lstext, statflags, activityType`.

- `code` ∈ `"" | "cancelled" | "irregular"` (omitted when empty).
- `lstype` is omitted for a normal lesson.

**Customizable `options`:**

| Key | Meaning |
|---|---|
| `element` | `{ id, type, keyType }`; `keyType` ∈ `id` \| `name` \| `externalkey` |
| `startDate`, `endDate` | Untis dates (`YYYYMMDD`) |
| `onlyBaseTimetable` | Ignore substitutions/changes |
| `showBooking`, `showInfo`, `showSubstText`, `showLsText`, `showLsNumber`, `showStudentgroup` | Include the named fields (booleans, default `false`) |
| `klasseFields`, `roomFields`, `subjectFields`, `teacherFields` | Which fields to expand per element: `id` \| `name` \| `longname` \| `externalkey` |

The customizable period adds `info`, `substText`, `lstext`, `lsnumber`,
`statflags`, `activityType`, `sg`, `bkRemark`, `bkText`, and expands
`kl/te/su/ro` to the requested fields.

### Substitutions & class register

| Method | Params | Returns |
|---|---|---|
| `getSubstitutions` | `startDate`, `endDate`, `departmentId` (0 = all) | array of substitution objects |
| `getClassregEvents` | `startDate`, `endDate` | array of class-register events |
| `getClassregEvents` (element form) | `options.startDate`, `options.endDate`, `options.element{id,type,keyType}` | array of class-register events |
| `getClassregCategories` | `{}` | `[{ id, name, longName, groupId? }]` |
| `getClassregCategoryGroups` | `{}` | `[{ id, name }]` |

**Substitution object:** `type, lsid, date, startTime, endTime, kl[], te[], su[],
ro[], txt`, plus `reschedule { date, startTime, endTime }` for `cancel`/`shift`.

`type` ∈ `cancel, subst, add, shift, rmchg, rmlk, bs, oh, sb, other, free, exam,
ac, holi, stxt`.

Element "id objects" carry `id, name, externalkey, orgid, orgname,
orgexternalkey` (`org*` = the replaced original element).

**`getTimetableWithAbsences` item:** `date, startTime, endTime, studentId
(external key), subjectId, teacherIds[], studentGroup, status ("irregular"),
absenceReason?, absentTime?, excuseStatus?, user, checked, invalid?`.

### Exams

| Method | Params | Returns |
|---|---|---|
| `getExams` | `examTypeId`, `startDate`, `endDate` | `[{ id, classes[], teachers[], students[], subject, date, startTime, endTime }]` |
| `getExamTypes` | `{}` | `[{ id, name, longName }]` |

### Person lookup

| Method | Params | Returns |
|---|---|---|
| `getPersonId` | `type` (2 or 5), `sn`, `fn`, `dob` (0 if unknown) | person id, or `0` if not found |

## Notes & quirks

- Optional/empty fields (colors, texts) are **omitted**, not `null`.
- Dates are `YYYYMMDD`; times are `HHMM`/`Hmm` — pad to four digits before
  splitting into `HH:mm`. See [11](11-conventions.md).
- Servers emit dates as a number *or* a string depending on version — accept
  both.
- `getLatestImportTime` scale (seconds vs. milliseconds) varies by server
  version; check the magnitude before dividing.
- Element types: `1` class, `2` teacher, `3` subject, `4` room, `5` student.
  Some community libraries swap room/student — verify per server.
- Error codes are community-observed, not officially enumerated; see
  [11](11-conventions.md).

## Minimal example

```http
POST /WebUntis/jsonrpc.do?school=demo-school HTTP/1.1
Host: mese.webuntis.com
Content-Type: application/json

{"id":"1","method":"authenticate","params":{"user":"demo","password":"demo","client":"docs"},"jsonrpc":"2.0"}
```

```http
POST /WebUntis/jsonrpc.do?school=demo-school HTTP/1.1
Host: mese.webuntis.com
Content-Type: application/json
Cookie: JSESSIONID=…

{"id":"2","method":"getTimetable","params":{"element":{"id":123,"type":1,"keyType":"id"},"startDate":20261005,"endDate":20261011},"jsonrpc":"2.0"}
```
