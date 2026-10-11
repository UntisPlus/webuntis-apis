# Organizations & Schools

> Source: Untis GmbH developer documentation, `developer.untis.com/api-reference/oneroster-apis/organizations-schools/`.
> Reproduced here as an offline mirror so this repository is self-contained.
> © Untis GmbH; see [`NOTICE.md`](../../../NOTICE.md).

---

In Untis Platform, **organizations and schools are the same thing**. Both represent the school where teaching occurs and are exposed as OneRoster `org` objects with `type="school"`. The `/schools` endpoints are convenience aliases that return identical data to `/orgs`.

OneRoster 1.1  Read-only   **Endpoints:** 4 (2 unique + 2 aliases)

---

## Endpoints

| Service call | Endpoint | Notes |
| --- | --- | --- |
| `getAllOrgs` | `{{API_URL}}ims/oneroster/v1p1/orgs` |  |
| `getOrg` | `{{API_URL}}ims/oneroster/v1p1/orgs/{{id}}` |  |
| `getAllSchools` | `{{API_URL}}ims/oneroster/v1p1/schools` | Same as `getAllOrgs` |
| `getSchool` | `{{API_URL}}ims/oneroster/v1p1/schools/{{id}}` | Same as `getOrg` |

**Tip:** Use `/schools` if your integration expects school-level entities, or `/orgs`
for consistency with OneRoster terminology. Both return the same data.

---

## Identifiers

The primary identifier is **`sourcedId`** — a UUID assigned by Untis Platform. Always use this when referencing schools in API requests.

---

## Relationships to other entities

Organizations are referenced throughout the OneRoster data model:

| Entity | Relationship |
| --- | --- |
| **Users** | `user.orgs` array contains the `sourcedId` of the user’s school |
| **Classes** | `class.school` references the school where the class is taught |
| **Enrollments** | `enrollment.school` links the enrollment to a school context |

**Note:** Users are typically associated with a **single school**. Multi-school
scenarios are not currently supported in Untis Platform.

---

## Related pages

[Users](api-reference-oneroster-apis-users.md)  User profiles reference organizations via the orgs array.

[OneRoster APIs Overview](api-reference-oneroster-apis.md)  Supported scope, limitations, and terminology mapping.
