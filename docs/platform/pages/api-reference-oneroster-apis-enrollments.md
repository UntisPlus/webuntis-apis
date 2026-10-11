# Enrollments

> Source: Untis GmbH developer documentation, `developer.untis.com/api-reference/oneroster-apis/enrollments/`.
> Reproduced here as an offline mirror so this repository is self-contained.
> © Untis GmbH; see [`NOTICE.md`](../../../NOTICE.md).

---

Enrollments represent the relationships between **users** and **classes**. They link students to the classes they attend, teachers to the classes they teach, and both to the school context where the enrollment occurs.

OneRoster 1.1  Read-only   **Endpoints:** 4

Current school year only

`getAllEnrollments` and `getEnrollmentsForSchool` return only enrollments for
the **current school year** (the active academic year configured in Untis
Platform). This is a performance-related constraint. For historical enrollment
data, use the [Untis Platform APIs](api-reference-webuntis-apis.md).

---

## Endpoints

All paths are relative to your API base URL.

| Service call | Path | School-year scope |
| --- | --- | --- |
| `getAllEnrollments` | `/ims/oneroster/v1p1/enrollments` | Current year only |
| `getEnrollment` | `/ims/oneroster/v1p1/enrollments/{id}` | No |
| `getEnrollmentsForClassInSchool` | `/ims/oneroster/v1p1/schools/{id}/classes/{id}/enrollments` | No |
| `getEnrollmentsForSchool` | `/ims/oneroster/v1p1/schools/{id}/enrollments` | Current year only |

---

## School-year scope

The “current school year” is determined by the **academic session marked as active** in Untis Platform — typically the school year currently in progress.

| Endpoint | Returns |
| --- | --- |
| `getAllEnrollments` | Current school year enrollments only |
| `getEnrollmentsForSchool` | Current school year enrollments only |
| `getEnrollmentsForClassInSchool` | Enrollments independent of school year |
| `getEnrollment` (by ID) | The specific enrollment regardless of year |

---

## Java examples

Uses the shared `OneRosterClient` — see the [Users page](api-reference-oneroster-apis-users.md) for the full client setup.

**Fetch enrollments for the current school year:**

```
OneRosterClient client = new OneRosterClient(tenantId, clientId, password, new ObjectMapper());
OneRosterResponse<EnrollmentDto> result = client.list(
    "/ims/oneroster/v1p1/enrollments", "enrollments", EnrollmentDto.class, null, null, 100, 0);
```

**Fetch all records at once:**

```
// Use a high limit to retrieve all records in a single request
OneRosterResponse<EnrollmentDto> result = client.list(
    "/ims/oneroster/v1p1/enrollments", "enrollments", EnrollmentDto.class, null, null, 100000, 0);
```

---

## Related pages

[Academic Sessions](api-reference-oneroster-apis-academic-sessions.md)  School years and terms that scope enrollment data.

[Classes](api-reference-oneroster-apis-classes.md)  The teaching groups that enrollments link users to.
