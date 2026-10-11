# 08 — Legacy cookie REST

> 🔴 **Reverse-engineered.** These paths are served by the WebUntis web client
> and the mobile login bootstrap. They authenticate with cookies only
> (`JSESSIONID`, `schoolname`) — no bearer token. Several are broken or being
> retired since ~2024 in favour of the view API ([07](07-rest-view.md)).

## Login bootstrap

| Method | Path | Returns |
|---|---|---|
| GET | `/WebUntis/api/app/config` | `data.data.loginServiceConfig.user` → `{ personId, persons[] }` |
| GET | `/WebUntis/api/daytimetable/config` | `data.data.klasseId` |

After an intern OTP login, `api/app/config` is how a client learns its
`personType`: find the entry in `persons[]` whose `id == personId`. See
[05 — Login flow](05-jsonrpc-intern.md).

## Timetable, homework, exams, absences

| Method | Path | Notes |
|---|---|---|
| GET | `/WebUntis/api/public/timetable/weekly/data?elementType=&elementId=&date=yyyy-MM-dd&formatId=` | Rich weekly timetable. ⚠️ Only endpoint using ISO dates (`yyyy-MM-dd`); else `yyyyMMdd` |
| GET | `/WebUntis/api/homeworks/lessons?startDate=&endDate=` | `data.data.homeworks` |
| GET | `/WebUntis/api/exams?startDate=&endDate=&klasseId=&withGrades=` | `data.data.exams` |
| GET | `/WebUntis/api/classreg/absences/students?startDate=&endDate=&studentId=&excuseStatusId=` | Student absences |
| GET | `/WebUntis/api/public/news/newsWidgetData?date=YYYYMMDD` | News / messages of the day |

`weekly/data` error envelope:

```json
{ "data": { "error": { "data": { "messageKey": "ERR_TTVIEW_NOTALLOWED_ONDATE" } } } }
```

### Known breakage

- Since ~2024 `api/public/timetable/weekly/data` has been returning 500s /
  `ERR_TTVIEW_NOTALLOWED_ONDATE` and masking class names. Projects moved to
  `view/v1/timetable/{filter,entries}`.
- Homework is scoped to the **session's school year**. Cross-year requests
  return HTTP 200 with empty collections unless the session year is switched.

## Reports (PDF)

```http
GET /WebUntis/reports.do?name=Excuse&format=pdf&rpt_sd=<start>&rpt_ed=<end>
```

Returns `{ messageId, reportParams }` and a URL from which the PDF is fetched.

## Form login & CSRF (web UI)

The web UI does not use JSON-RPC to log in:

1. `GET /WebUntis/?school=<school>` — the HTML embeds a CSRF token.
2. `POST /WebUntis/j_spring_security_check` with fields `school`, `j_username`,
   `j_password`, `token`.

Success returns `{"switchUI":true,"state":"SUCCESS"}`.

To switch the server-side school year (needed by homework and some reports):

```http
POST /WebUntis/jsonrpc_web/jsonCalendarService
```

with a CSRF token.

## `api/restricted/*`

Endpoints such as `api/restricted/data` and `api/restricted/statusdata` are
web-client internals. Their shapes are **not** reliably documented here; treat
them as unstable.

## Recommendation

Use the view API ([07](07-rest-view.md)) or the official
[extern timetable API](09-extern-timetable-v3.md) for new work. Treat the paths
on this page as legacy compatibility.
