# 05 — Internal JSON-RPC API

> 🔴 **Reverse-engineered.** This is the JSON-RPC surface the official Untis
> Mobile apps and the WebUntis web client use. It is undocumented and can change
> without notice. Methods come from the BetterUntis client, pyWebUntis, the Ruby
> `webuntis-api` gem, and the Elixir `untis` library.

## Transport

```http
POST /WebUntis/jsonrpc_intern.do?m=<method>&school=<school>&v=i2.2
Content-Type: application/json
```

| Query param | Meaning |
|---|---|
| `m` | Method name (duplicated in the JSON body) |
| `school` | School login name |
| `v` | API version; `i2.2` is the common value. Some clients use `i5.12.3` and add `a=true&s=<host>` |

Body (the login call):

```json
{
  "id": "untis-mobile-android",
  "jsonrpc": "2.0",
  "method": "getUserData2017",
  "params": [
    { "auth": { "clientTime": 1720000000000, "user": "<username>", "otp": 123456 } }
  ]
}
```

- `id` is a client identifier. Observed values: `untis-mobile-android`,
  `untis-mobile-blackberry-2.7.4`. The server does not validate it; some clients
  send a random hex string.
- The `auth` block is attached to **every** authenticated method.
- Success sets the `JSESSIONID` cookie (same cookie the public API uses).

### The `auth` block

```json
{ "auth": { "clientTime": 1720000000000, "user": "<username>", "otp": 123456 } }
```

- `clientTime` — current time, **epoch milliseconds**.
- `user` — login name, or `#anonymous#` for anonymous access.
- `otp` — a 6-digit RFC 6238 TOTP from the QR-code secret; or the constant
  `100170` for `#anonymous#`.

See [02 — Authentication](02-authentication.md) for the TOTP/QR details.

## The `*2017` method family

The apps bootstrap with a `getUserData2017` call, then issue element queries.
Method names and params below are reverse-engineered.

| Method | Params (besides `auth`) | Notes |
|---|---|---|
| `getUserData2017` | `deviceOs`, `deviceOsVersion`, `elementId` | Login/bootstrap; returns app config + master data |
| `getTimetable2017` | `id`, `type`, `startDate`, `endDate` (`yyyy-MM-dd`), `masterDataTimestamp`, `timetableTimestamp`, `timetableTimestamps[7]` | 7-day window typical; timestamps are incremental-change hints |
| `getPeriodData2017` | `ttIds` (array) | Extra data for timetable entries |
| `getHomeWork2017` | `id`, `type` (`STUDENT`), `startDate`, `endDate` | → `result.homeWorks` |
| `getMessagesOfDay2017` | `date` (`yyyy-MM-dd`) | → `result.messages` |
| `getStudentAbsences2017` | `startDate`, `endDate`, `includeExcused`, `includeUnExcused` | → `result.absences` |
| `getExams2017` | `id`, `type`, `startDate`, `endDate` | exams |
| `getOfficeHours2017` | `klasseId`, `startDate` | office hours |
| `getLessonTopic2017` | lesson identifiers | lesson topics |
| `getAppInfo`, `getVersion` | `{}` | no auth block |
| `getAppSharedSecret` | `username`, `password`, `token` | no auth block |
| `getAuthToken` | `auth: { user, key }` (no `otp`) | returns a JWT for the REST API |

### Write methods

| Method | Params |
|---|---|
| `createImmediateAbsence2017` | `periodId`, `studentId`, `startTime`, `endTime` |
| `deleteAbsence2017` | `absenceId` |
| `submitAbsencesChecked2017` | `ttIds` |
| `submitLessonTopic` | `lessonTopic`, `ttId` |

### Example: timetable

```json
POST /WebUntis/jsonrpc_intern.do?m=getTimetable2017&school=demo-school&v=i2.2

{
  "id": "untis-mobile-android",
  "jsonrpc": "2.0",
  "method": "getTimetable2017",
  "params": [{
    "auth": { "clientTime": 1720000000000, "user": "#anonymous#", "otp": "100170" },
    "id": 889,
    "type": "STUDENT",
    "startDate": "2026-10-05",
    "endDate": "2026-10-11",
    "masterDataTimestamp": 0,
    "timetableTimestamp": 0,
    "timetableTimestamps": [0, 0, 0, 0, 0, 0, 0]
  }]
}
```

`type` is an uppercase element type: `STUDENT`, `CLASS`, `TEACHER`, `SUBJECT`,
`ROOM`.

## Login flow

1. `getUserData2017` with the auth block → server sets `JSESSIONID`.
2. `GET /WebUntis/api/app/config` (cookie only) →
   `data.data.loginServiceConfig.user` gives `personId` and a `persons[]` array;
   select the person with `id == personId` to learn `personType`.
3. Optional: `GET /WebUntis/api/daytimetable/config` → `data.data.klasseId`.
4. Anonymous logins skip the person lookup.

The config calls are covered in [08 — Legacy cookie REST](08-legacy-rest.md).

## Relationship to the other APIs

- Same host, same cookie jar as the public API, but a different endpoint and
  richer methods.
- The `*2017` methods return more detail (cancelled/irregular periods, per-day
  timestamps) than public `getTimetable`.
- For new work, prefer the view REST API ([07](07-rest-view.md)) or the official
  Timetable API v3 ([09](09-extern-timetable-v3.md)).

## Caveats

- Undocumented and unsupported. The modern apps are migrating to
  `/WebUntis/api/rest/view/...`.
- Field names return inconsistently across server versions; parse defensively.
- Anonymous sessions are read-only.
