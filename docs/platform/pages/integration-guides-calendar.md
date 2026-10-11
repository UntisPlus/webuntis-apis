# Calendar API

> Source: Untis GmbH developer documentation, `developer.untis.com/integration-guides/calendar/`.
> Reproduced here as an offline mirror so this repository is self-contained.
> © Untis GmbH; see [`NOTICE.md`](../../../NOTICE.md).

---

**Deprecated. Will be removed before end of 2026. Use the timetable push API instead.**

The Calendar API is a **platform-initiated pull** — Untis Platform calls your endpoint to request calendar events for a specific user and date range, and your application returns the data as an iCal response. Untis Platform then displays these events in the user’s timetable.

Unlike the credentials and deactivation webhooks, the Calendar API is data-driven: Untis Platform calls it on demand whenever it needs to render a user’s schedule.

Like all other platform-initiated requests, the Calendar API request is **signed** and must be verified before you trust the content — see Step 1 in [Handling requirements](#handling-requirements) below.

## Request

Untis Platform sends a signed `POST` request to your Calendar API endpoint.

### Headers

| Header | Value |
| --- | --- |
| `Content-Type` | `application/json` |
| `Authorization` | Base64-encoded RSA signature over the raw request body |
| `Algorithm` | Signing algorithm, e.g. `SHA256withRSA` |

### Request body

```
{
  "tenantId": "456800",
  "user": "b953ec5f-598a-4305-87c1-d4b5f95a28c7",
  "startDate": "2023-03-10",
  "endDate": "2023-03-13"
}
```

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `tenantId` | string | Yes | Identifier of the school/tenant |
| `user` | string | Yes | External UUID of the Untis Platform user whose calendar is being requested |
| `startDate` | string | Yes | Start of the requested date range (inclusive), formatted as `YYYY-MM-DD` |
| `endDate` | string | Yes | End of the requested date range (inclusive), formatted as `YYYY-MM-DD` |

All four parameters are always present. Parameters may be sent in any order.

## Response

Your endpoint must respond with a valid **iCal** document (`text/calendar`) containing `VEVENT` entries for the requested user and date range.

### Event fields

Only `VEVENT` components are processed. Other iCal component types are ignored.

**Required fields:**

| Field | Description |
| --- | --- |
| `DTSTART` | Event start date/time |
| `DTEND` | Event end date/time |

**Optional standard fields:**

| Field | Description |
| --- | --- |
| `UID` | Unique event ID — digits, optionally followed by `-` and text |
| `STATUS` | `CONFIRMED` (default), `CANCELLED`, or `TENTATIVE` |
| `SUMMARY` | Short description of the event |
| `LOCATION` | Short location text |
| `DESCRIPTION` | Multi-line description; may contain HTML links |

**Optional custom fields:**

| Field | Description |
| --- | --- |
| `X-COLOR` | Hex colour with leading `#`, e.g. `#E09FF0` — displayed as the event colour in the timetable |
| `X-GROUPNAME` | School-internal group name for the event |
| `X-LINK` | URL that opens the event in your application — displayed as a button in the timetable UI |

The calendar name shown in Untis Platform is defined in your platform application configuration in PAM, not in the iCal response.

### Example response

```
BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
UID:123456-weekly-meeting
DTSTART:20230310T090000
DTEND:20230310T100000
SUMMARY:Weekly Team Meeting
LOCATION:Room 3B
STATUS:CONFIRMED
X-COLOR:#4A90D9
X-LINK:https://yourapp.example.com/events/123456
END:VEVENT
END:VCALENDAR
```

## Dates and times

The `startDate` and `endDate` fields in the request use the `YYYY-MM-DD` format, for example `2023-03-10`.

In the iCal response, `DTSTART` and `DTEND` use the iCal date-time format `YYYYMMDDTHHmmss`, for example `20230310T090000`.

All times in Untis are in the **school’s local time zone**. There is no public API endpoint to query the school’s time zone.

## Constraints

Zero-minute appointments will break the timetable

Untis Platform does not support events where `DTSTART` equals `DTEND`. Sending 0-minute appointments will break the timetable display for affected users. If you need to represent reminders or deadlines, send them as **full-day events** or **1-minute events** instead.

## Handling requirements

1. **Verify the signature first** — before reading `tenantId`, `user`, or any other field. See [Verifying the Untis Platform Identity](integration-guides-webhooks-verifying-identity.md).
2. **Scope the response** — return only events for the specified `user` within the `startDate`–`endDate` range. The `endDate` is inclusive.
3. **Respect per-tenant data isolation** — use `tenantId` to look up the correct school’s data. Never return events from one tenant in response to a request for another.
4. **Respond promptly** — return the iCal data synchronously. Untis Platform is waiting for the response to render the timetable.
5. **Return an empty calendar if no events exist** — a valid iCal document with no VEVENT entries is acceptable. Do not return `404` or an error for empty date ranges.

## Relevant articles

[Verifying the Untis Platform Identity](integration-guides-webhooks-verifying-identity.md)  How to verify the request signature.

[Integration Webhooks](integration-guides-webhooks.md)  Overview of platform-initiated callbacks.

[Credentials Webhook](integration-guides-webhooks-credentials.md)  How credentials for the tenant are delivered.

[Get Your Platform Application](getting-started-get-platform-application.md)  Configure your Calendar API endpoint.
