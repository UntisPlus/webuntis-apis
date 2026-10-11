# Academic Sessions

> Source: Untis GmbH developer documentation, `developer.untis.com/api-reference/oneroster-apis/academic-sessions/`.
> Reproduced here as an offline mirror so this repository is self-contained.
> © Untis GmbH; see [`NOTICE.md`](../../../NOTICE.md).

---

Academic sessions represent the school years that structure the school calendar. They determine when classes are taught and when enrollments are active.

OneRoster 1.1  Read-only   **Endpoints:** 2

---

Note

Currently, only the `schoolYear` session type is supported.

---

## Endpoints

| Service call | Endpoint |
| --- | --- |
| `getAllAcademicSessions` | `{{API_URL}}ims/oneroster/v1p1/academicSessions` |
| `getAcademicSession` | `{{API_URL}}ims/oneroster/v1p1/academicSessions/{{id}}` |

---

## Mapping to Untis Platform periods

Untis Platform uses **planning periods (Planungsperioden)** to structure the school year. Here is how they map to OneRoster session types:

| Untis Platform period | OneRoster session type | Example |
| --- | --- | --- |
| School Year | `type="schoolYear"` | 2025-2026 |

---

## Related pages

[Enrollments](api-reference-oneroster-apis-enrollments.md)  Enrollment data is scoped to academic sessions.

[OneRoster APIs Overview](api-reference-oneroster-apis.md)  Supported scope, limitations, and terminology mapping.
