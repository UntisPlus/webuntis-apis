# Untis Platform API — OpenAPI specs

The machine-readable OpenAPI documents for the Untis Platform APIs, downloaded
from the official developer portal so this repository is self-contained. These
are the **complete** request/response schemas (every field, enum and status
code) for the official integration surface.

| File | API | Version |
|---|---|---|
| [`openapi-extern-user-management-api_v1.yaml`](openapi-extern-user-management-api_v1.yaml) | User management | v1 |
| [`openapi-extern-student-management-api_v3.yaml`](openapi-extern-student-management-api_v3.yaml) | Student management | v3 |
| [`openapi-extern-teacher-management-api_v2.yaml`](openapi-extern-teacher-management-api_v2.yaml) | Teacher management | v2 |
| [`openapi-extern-legal-guardian-management-api_v1.yaml`](openapi-extern-legal-guardian-management-api_v1.yaml) | Legal guardian management | v1 |
| [`openapi-extern-class-management-api_v2.yaml`](openapi-extern-class-management-api_v2.yaml) | Class management | v2 |
| [`openapi-extern-room-management-api_v1.yaml`](openapi-extern-room-management-api_v1.yaml) | Room management | v1 |
| [`openapi-extern-subject-management-api_v1.yaml`](openapi-extern-subject-management-api_v1.yaml) | Subject management | v1 |
| [`openapi-extern-teacher-absences-api_v1.yaml`](openapi-extern-teacher-absences-api_v1.yaml) | Teacher absence management | v1 |
| [`openapi-extern-teacher-absence-reason-v1.yaml`](openapi-extern-teacher-absence-reason-v1.yaml) | Teacher absence reasons | v1 |
| [`openapi-extern-classreg-absences-v1-api.yaml`](openapi-extern-classreg-absences-v1-api.yaml) | Class register absences | v1 |
| [`openapi-extern-exam-api.yaml`](openapi-extern-exam-api.yaml) | Exams | v1 |
| [`openapi-extern-lesson-api.yaml`](openapi-extern-lesson-api.yaml) | Lessons | v1 |
| [`openapi-extern-messages-api.yaml`](openapi-extern-messages-api.yaml) | Messaging | v1 |
| [`openapi-extern-timetable-api_v3.yaml`](openapi-extern-timetable-api_v3.yaml) | Timetable | v3 |
| [`openapi-extern-platform-calendar-events-api.yaml`](openapi-extern-platform-calendar-events-api.yaml) | Timetable event push | v1 |

## Notes

- Source: `developer.untis.com/openapi/<file>` (official, © Untis GmbH). See
  [`../../NOTICE.md`](../../NOTICE.md).
- OneRoster (`/ims/oneroster/v1p1/...`) follows the public **IMS Global
  OneRoster 1.1** specification and is not shipped as a Untis-hosted document.
- Prose walkthroughs of each API are mirrored under
  [`../../docs/platform/`](../../docs/platform/README.md).
