# Error Handling

> Source: Untis GmbH developer documentation, `developer.untis.com/api-reference/error-handling/`.
> Reproduced here as an offline mirror so this repository is self-contained.
> © Untis GmbH; see [`NOTICE.md`](../../../NOTICE.md).

---

Due to historical reasons there is no common error handling shared between the OneRoster and Untis Platform API families.

---

## Untis Platform API

Most of the Untis Platform APIs follow a common error handling pattern defining structured JSON responses:

- User Management
- Student Management
- Teacher Management
- Legal Guardian Management
- Class Management
- Room Management
- Lessons

Other APIs (e.g. Timetable or Messaging) use individual error handling with different response types.

### Standard Error Response Format

These APIs all define the same HTTP error status set and the same two reusable error response schemas: `ValidationErrorResponse` and `ErrorResponse`.

| HTTP status | Response schema | Meaning |
| --- | --- | --- |
| `400` | `ValidationErrorResponse` | Request parameters are invalid |
| `401` | `ErrorResponse` | Authentication missing or invalid |
| `403` | `ErrorResponse` | Authenticated caller not allowed |
| `404` | `ErrorResponse` | Requested entity not found |
| `500` | `ErrorResponse` | Unexpected internal error |

---

#### `ErrorResponse`

Tip

Use the `errorCode` field for programmatic error handling and the `requestId`
/ `traceId` when contacting support.

| Field | Description |
| --- | --- |
| `errorCode` | Machine-readable code identifying the error type. |
| `errorMessage` | Human-readable message describing the error. |
| `requestId` | Unique identifier for the API request. Use when contacting support or tracing logs. |
| `traceId` | Identifier used for distributed tracing across services. |

```
{
  "errorCode": "FORBIDDEN",
  "errorMessage": "Access denied.",
  "requestId": "5f0c7f12-3a17-4a0b-9b1a-2d8f5c8d1234",
  "traceId": "9e8f7a6b5c4d3210"
}
```

---

#### `ValidationErrorResponse`

| Field | Description |
| --- | --- |
| `errorCode` | Machine-readable code identifying the error type. |
| `requestId` | Unique identifier for the API request. Use when contacting support or tracing logs. |
| `traceId` | Identifier used for distributed tracing across services. |
| `validationErrors` | Array describing individual validation problems detected in the request. |

**`validationErrors` entry fields:**

| Field | Required | Description |
| --- | --- | --- |
| `path` | yes | Location of the invalid field in the request payload or parameters. Start index is 0. |
| `errorMessage` | yes | Human-readable description of the validation problem. |
| `errorKey` | no | Machine-readable key identifying the specific validation rule that failed. |
| `constraintValue` | no | The constraint value associated with the validation rule (e.g. maximum length). |
| `index` | no | For bulk operations — indicates which array element caused the error. Start index is 0. |
| `errorData` | no | Additional structured information such as identifiers of related entities. |

```
{
  "errorCode": "VALIDATION_ERROR",
  "requestId": "5f0c7f12-3a17-4a0b-9b1a-2d8f5c8d1234",
  "traceId": "9e8f7a6b5c4d3210",
  "validationErrors": [
    {
      "path": "students[0].externKey",
      "errorMessage": "must not be blank",
      "errorKey": "field.mustNotBeBlank",
      "index": 0,
      "constraintValue": "1"
    }
  ]
}
```

---

### Non-Standard Error Response Formats

#### Absences & Class Register

The **Classreg-Absences API** defines error handling only through HTTP status codes. It does **not** define a common error response schema.

| HTTP status | Response schema | Meaning |
| --- | --- | --- |
| `400` | none defined | Invalid request |
| `401` | none defined | Authentication missing or invalid |
| `403` | none defined | Access forbidden |
| `500` | none defined | Unexpected internal error |

---

#### Exams

The **Exam API** defines error handling through HTTP status codes and a shared **`Error`** response object.

| HTTP status | Response schema | Meaning |
| --- | --- | --- |
| `400` | `Error` | Client error / invalid request |
| `500` | `Error` | Server error |

| Field | Required | Description |
| --- | --- | --- |
| `title` | yes | Short, human-readable summary of the problem type. |
| `status` | yes | The HTTP status code. |
| `detail` | no | Human-readable explanation specific to this occurrence of the problem. |

```
{
  "title": "Bad Request",
  "status": 400,
  "detail": "At least one filter criterion is required."
}
```

---

#### Timetable

The **Timetable API** defines error handling through HTTP status codes and a shared **`Error`** response object.

| HTTP status | Response schema | Meaning |
| --- | --- | --- |
| `400` | `Error` | Invalid request |
| `401` | `Error` | Authentication missing or invalid |
| `403` | `Error` | Authenticated caller not allowed |
| `404` | `Error` | Requested resource not found |
| `500` | `Error` | Unexpected server error |

| Field | Required | Description |
| --- | --- | --- |
| `title` | yes | Short, human-readable summary of the problem type. |
| `status` | yes | The HTTP status code. |
| `detail` | no | Human-readable explanation specific to this occurrence of the problem. |

```
{
  "title": "Forbidden",
  "status": 403,
  "detail": "Access to the requested timetable resource is not allowed."
}
```

---

#### Messaging

The **Messages API** defines error handling through HTTP status codes. Only **one error response body** is explicitly modeled in the specification.

| HTTP status | Response schema | Meaning |
| --- | --- | --- |
| `400` | none defined | Invalid request |
| `401` | none defined | Authentication missing or invalid |
| `403` | none defined | Access forbidden |
| `422` | `ExternalMessageSendResponseDto` with `error: ErrorResponseDto` | Request understood but semantically invalid |
| `500` | none defined | Unexpected internal error |

For the `422` error case, the response uses an **`ErrorResponseDto`** nested inside `ExternalMessageSendResponseDto`:

| Field | Description |
| --- | --- |
| `message` | High-level error message summarizing the issue. |
| `details` | Array of detailed messages explaining specific issues. |

```
{
  "error": {
    "message": "Validation Failed",
    "details": [
      "Subject must not be blank",
      "At least one recipientUserUuid is required"
    ]
  }
}
```

---

## OneRoster API

The **OneRoster API** defines error handling through HTTP status codes and a shared structured `ErrorPayloads` response body.

| HTTP status | Response schema | Meaning |
| --- | --- | --- |
| `400` | `ErrorPayloads` | Request was invalid and cannot be served |
| `401` | `ErrorPayloads` | Request requires authorization |
| `403` | `ErrorPayloads` | Server understood the request but refuses further action |
| `404` | `ErrorPayloads` | No resource exists behind the URI |
| `429` | `ErrorPayloads` | Too many requests; retry later |
| `500` | `ErrorPayloads` | Internal server error |

`ErrorPayloads` is an **array** of `ErrorPayload` objects.

| Field | Description |
| --- | --- |
| `errorCode` | Numeric error code. |
| `codeMajor` | High-level classification. Values: `success`, `failure`. |
| `severity` | Severity of the result. Values: `status`, `warning`, `error`. |
| `codeMinor` | Specific machine-readable classification. Values: `full success`, `invalid_sort_field`, `invalid_selection_field`, `invalid data`, `invalid_filter_field`, `invalid_blank_selection_field`, `unauthorized`, `forbidden`, `unknown object`, `server_busy`. |
| `description` | Human-readable description of the error. |

```
[
  {
    "errorCode": 4001,
    "codeMajor": "failure",
    "severity": "error",
    "codeMinor": "invalid data",
    "description": "The request contains invalid filter parameters."
  }
]
```
