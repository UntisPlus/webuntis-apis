# 07 — "View" REST API

> 🔴 **Reverse-engineered.** The current REST surface used by the Untis Mobile
> app and the WebUntis web app. Base path:

```
https://<server>.webuntis.com/WebUntis/api/rest/view/v{1..4}/…
```

## Authentication & headers

Every call carries (see [02](02-authentication.md)):

```http
Authorization: Bearer <jwt>
Tenant-Id: <tenantId>
X-Webuntis-Api-School-Year-Id: <schoolYearId>   # when required
Cookie: JSESSIONID=<sid>; schoolname=_<base64(school)>
Accept: application/json, text/plain, */*
```

Anonymous access to the timetable endpoints uses an `anonymous-school` header
instead of a bearer token / cookie. Authentication failures are frequently
masked as **404** rather than 401. Error bodies nest as
`data.error.data.messageKey`, or expose a top-level `errorMessage`.

Date query values are `YYYY-MM-DD`; array params are comma-separated.

## Endpoint catalogue

Base path below: `/WebUntis/api/rest/view`.

### App & user

| Method | Path | Notes |
|---|---|---|
| GET | `v1/app/data` | App metadata; `tenant.id` (tenant discovery fallback) |
| GET | `v1/home`, `v2/home` | User home page |
| GET | `v1/mobile/data`, `v3/mobile/data` | Mobile user data (school year, tenant, user) |
| GET | `v1/profile/user-contact-data` | Contact data |
| PUT | `v1/profile/user-contact-data` | Update contact data (e.g. the required email) |
| GET | `v1/trigger/startup` | Startup trigger |

### Timetable

| Method | Path | Key query params |
|---|---|---|
| GET | `v1/timetable/grid` | `timetableType=STANDARD`; returns per-type format ids |
| GET | `v1/timetable/filter` | `resourceType`, `timetableType`, `start`, `end` |
| GET | `v1/timetable/entries` | `start`, `end`, `format`, `resourceType`, `resources`, `periodTypes`, `timetableType=STANDARD`, `layout=START_TIME` |
| GET | `v1/timetable/entriesWeekOverview` | week overview |
| GET | `v1/timetable/search` | `q`, `schoolyear` |
| GET | `v1/timetable/menu`, `calendar`, `today/meta`, `dashboard/cards`, `timegrid`, `schoolyears` | UI support |
| POST | `v1/session/status` | Body `{ clientTimeZone }` |
| GET | `v2/timetable/availableRooms` | ISO datetimes |

Example:

```http
GET /WebUntis/api/rest/view/v1/timetable/entries?start=2026-10-05&end=2026-10-11&format=1&resourceType=CLASS&resources=123&periodTypes=&timetableType=STANDARD&layout=START_TIME
```

### Master data

| Method | Path |
|---|---|
| GET | `v1/teachers`, `v1/teachers/{id}` |
| GET | `v1/students`, `v1/students/overview`, `v1/students/{id}`, `v1/students/{id}/lessons`, `v1/students/{id}/class-history` |
| GET | `v1/subjects`, `v1/rooms` |

### Exams

| Method | Path | Notes |
|---|---|---|
| GET | `v1/exams` | `start`, `end`, `withDeleted` |
| GET | `v1/exams/filter`, `v1/exams/statistics`, `v1/exam-types` | |
| GET | `v2/calendar-entry/detail` | numeric `elementType`, `homeworkOption=DUE` |

### Class register, homework, absences

| Method | Path |
|---|---|
| GET | `v1/classreg/homework/meta` |
| POST | `v1/classreg/homework/list` |
| GET | `v4/classreg/absences` |
| GET | `v1/classreg/open-periods` |

### Messaging

| Method | Path | Summary |
|---|---|---|
| GET | `v1/messages` | Incoming messages + read-confirmation messages |
| GET | `v1/messages/{messageId}` | Message detail |
| GET | `v1/messages/sent` | Sent messages |
| GET | `v1/messages/drafts` | Drafts |
| GET | `v1/messages/status` | Unread count |
| GET | `v1/messages/permissions` | What the user may send |
| GET | `v1/messages/recipients/static/persons` | Static recipient groups |
| GET | `v1/timetable/grid` | Also yields per-type `format` ids |

## Response schemas

These are the schemas from the reverse-engineered
[`untis-rest.yaml`](../specs/untis-intern/untis-rest.yaml).

### Messages

```jsonc
// GET /view/v1/messages
{
  "incomingMessages": [ Message, … ],
  "readConfirmationMessages": [ Message, … ]
}

// GET /view/v1/messages/sent      → { "sentMessages": [ Message, … ] }
// GET /view/v1/messages/drafts    → { "draftMessages": [ Message, … ] }
// GET /view/v1/messages/status    → { "unreadMessagesCount": 12 }
```

`Message` (subset):

| Field | Type | Notes |
|---|---|---|
| `id` | int64 | required |
| `subject`, `contentPreview`, `content` | string | |
| `sender` | `Sender` | `{ userId, displayName, imageUrl, className }` |
| `numberOfRecipients`, `recipients`, `recipientGroups`, `recipientPersons` | | |
| `replyHistory` | `Message[]` | |
| `requestConfirmation`, `requestConfirmationStatus` | object | read-confirmation bookkeeping |
| `attachments` | `MessageAttachment[]` | `attachmentType` ∈ `ONE_DRIVE` \| `STORAGE_ATTACHMENT` \| `BLOB_ATTACHMENT` |
| `isRead`/`isReportMessage`/`isReply`, … | boolean | |

`GET /view/v1/messages/permissions`:

```jsonc
{
  "recipientOptions": "STUDENTS",        // STUDENTS|PARENTS|CUSTOM|REPLY|TEACHER|STAFF
  "allowRequestReadConfirmation": true,
  "recipientSearchMaxResult": 100,
  "showDraftsTab": true,
  "showSentTab": true,
  "canForbidReplies": false,
  "maxFileSize": 7000000,
  "maxFileCount": 5
}
```

### Mobile data

```jsonc
// GET /view/v1/mobile/data
{
  "schoolYear": { "dateRange": { "start": "…", "end": "…" }, "id": 1, "name": "2023/2024" },
  "tenant":     { "id": 1004400, "displayName": "…", "wuVersion": "…" },
  "user": {
    "id": 42, "username": "…",
    "person": { "id": 7, "displayName": "…", "imageUrl": "…" },
    "referencedStudents": [ … ],
    "locale": "de-DE", "departmentId": 3, "role": "STUDENT",
    "permissions": [ "…" ]
  }
}
```

### Home

```jsonc
// GET /view/v1/home
{
  "schoolname": "…",
  "sections": [ { "cells": [ { "badge": { "count": 2 }, "type": "STUDENT_ABSENCES" } ] } ],
  "integrationsSection": [ { "id": 1, "name": "…", "url": "…", "iconName": "…", "type": "WEB", "appId": "…" } ]
}
```

`HomeSectionCell.type` ∈ `MY_EVENTS, CLASS_TEACHER, PARENTS_DAYS, CONTACT_HOURS,
STUDENT_ABSENCES, TEACHER_ABSENCES, SUBSTITUTION_REQUESTS,
STUDENT_ABSENCES_ADMINISTRATION, n/a`.

### Contact data

```jsonc
// GET|PUT /view/v1/profile/user-contact-data
{
  "email": "user@example.org",
  "telephoneNumber": null, "mobileNumber": null,
  "street": null, "postCode": null, "city": null,
  "areContactDetailsWriteable": true,
  "userEmailMissingOrDifferentToMasterData": false
}
```

## Notes

- Since ~2024 the web client migrated from the legacy `api/public/timetable/weekly/*`
  endpoints to `view/v1/timetable/{filter,entries}`.
- The JWT and headers are shared with the mobile v2 auth endpoint
  ([06](06-mobile-rest-auth.md)).
