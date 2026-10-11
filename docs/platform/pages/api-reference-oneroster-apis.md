# OneRoster APIs

> Source: Untis GmbH developer documentation, `developer.untis.com/api-reference/oneroster-apis/`.
> Reproduced here as an offline mirror so this repository is self-contained.
> © Untis GmbH; see [`NOTICE.md`](../../../NOTICE.md).

---

Untis Platform implements the **IMS Global OneRoster v1.1** specification, giving integration partners standards-based, read-only access to organizational and enrollment data. If your platform already speaks OneRoster, you can consume Untis Platform roster information without learning proprietary data structures.

Tip

OneRoster APIs are **read-only** and return only entities with **assigned user
accounts**. If you need write access or complete master-data, see the [Untis
Platform APIs](api-reference-webuntis-apis.md).

---

## Available entities

[Organizations & Schools](api-reference-oneroster-apis-organizations-schools.md)  School and district organizational structures.

[Users](api-reference-oneroster-apis-users.md)  Students, teachers, and all users — filterable by role.

[Classes](api-reference-oneroster-apis-classes.md)  Teaching groups (mapped to Untis Platform lessons).

[Academic Sessions](api-reference-oneroster-apis-academic-sessions.md)  School years, terms, and grading periods.

[Enrollments](api-reference-oneroster-apis-enrollments.md)  User-to-class membership relationships.

---

## Supported features

| Feature | Details |
| --- | --- |
| **Operations** | `GET` only — all endpoints are read-only |
| **Filtering** | Filter by `dateLastModified` for incremental sync |
| **Pagination** | `limit` and `offset` parameters on every list endpoint. **Attention: The default limit is set to 100!** |
| **Role filtering** | Retrieve users by specific role (student, teacher) |

---

## Limitations

Read-only

No create, update, or delete operations — POST, PUT, DELETE are not
available.

User-assigned data only

Students and teachers without user accounts are **not returned**. For
complete master-data, use the Untis Platform APIs.

Current school year

Enrollment data is limited to the **active school year**. Historical and
future enrollments are not exposed.

No gradebook or demographics

Gradebook (lineItems, results), resources, and demographics endpoints are
**not implemented**.

---

## Terminology mapping

OneRoster and Untis Platform use different names for the same concepts:

| OneRoster term | Untis Platform term | Notes |
| --- | --- | --- |
| **Class** | **Lesson** | A class in OneRoster = a lesson (Unterricht) in Untis Platform |
| **Course** | **Subject** | Not directly exposed in OneRoster APIs |
| **Organization** | **School** | Treated as equivalent — `/orgs` and `/schools` return the same data |
| **Academic Session** | **School Year / Term** | Hierarchical time periods for organizing instruction |

---

## Related guides

[Which API to Choose](api-reference-which-api-to-choose.md)  Side-by-side comparison to help pick the right API family.

[Common API Concepts](api-reference-common-api-concepts.md)  Pagination, sorting, and filtering — shared across both families.

[OneRoster v1.1 Specification](https://www.imsglobal.org/oneroster-v11-final-specification)  Full IMS Global specification for data models and endpoints.
