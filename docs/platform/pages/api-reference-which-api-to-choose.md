# Which API to Choose

> Source: Untis GmbH developer documentation, `developer.untis.com/api-reference/which-api-to-choose/`.
> Reproduced here as an offline mirror so this repository is self-contained.
> © Untis GmbH; see [`NOTICE.md`](../../../NOTICE.md).

---

We offer two families of APIs. The key differences are the **user-focused data scope** of OneRoster (only entities with assigned users) and the **read/write capabilities** of the Untis Platform APIs. Below you’ll find recommendations for selecting the right API for your use case.

OneRoster APIs

An open standard for **read-only** roster data, implemented on the Untis Platform.

- Returns only entities with **assigned users** — students or teachers without user accounts do not appear
- No create, update, or delete operations
- Covers organizations, users, classes, enrollments, and academic sessions

**Best for:** LMS integrations, student portals, read-only data sync.

Untis Platform APIs

Proprietary APIs with **read and write** access to master-data and platform-specific features.

- Returns **complete master-data** regardless of user assignment — all students included, even without user accounts
- Create and update operations (deletion is manual — not available via API)
- Additional domains: timetables, absences, exams, lessons, messaging

**Best for:** School management systems, admin tools, bidirectional sync.

**Note:** A student who exists in master-data but has no assigned user account will
appear in Untis Platform API responses but **will not** appear in OneRoster.

---

## Quick decision table

Map your functional need to the right API:

| I need to… | API |
| --- | --- |
| Read roster data (orgs, users, classes, enrollments, academic sessions) | **OneRoster** |
| Read all users | **OneRoster** |
| Read lessons and their students & teachers | **OneRoster** |
| Read schoolyears | **OneRoster** |
| Create or update students | **Student Management** |
| Assign user accounts to students | **Student Management** |
| Create or update teachers | **Teacher Management** |
| Create or update classes | **Class Management** |
| Manage legal guardians | **Legal Guardian Management** |
| Manage admin/staff users (no master-data) | **User Management** |
| Read room information | **Room Management** (read-only) |
| Read timetable with substitutions | **Timetable** (read-only) |
| Read absences from class register | **Absences & Class Register** (read-only) |
| Read exams and exam types | **Exams** (read-only) |
| Read lessons with full student lists | **Lessons** (read-only) |
| Send messages to users | **Messaging** |
| Display calendar events in the timetable | **Timetable Push of Events** |

For current versions and deprecation status, see the [API version table](api-reference-api-overview.md).

---

## Recommendation

Start with OneRoster

Your app is **read-only and roster-focused**. Most integrations that only display or sync user, class, and enrollment data can use OneRoster exclusively.

- IMS Global standard
- Fewer endpoints to integrate
- Ideal for LMS, portals, reporting

Add Untis Platform APIs

You need to **write data back**, access **complete master-data**, or use **platform-specific features** like timetables, absences, exams, or messaging.

Use both

**Hybrid approach** — many integrations combine OneRoster for common roster reads with Untis Platform APIs for write operations or specialized domains.

---

## Related guides

[API Overview](api-reference-api-overview.md)  Environments, base URLs, version table, and API family summary.

[Common API Concepts](api-reference-common-api-concepts.md)  Pagination, sorting, and filtering — shared across both API families.

[OneRoster APIs](api-reference-oneroster-apis.md)  Supported scope, limitations, and terminology mapping.

[Untis Platform APIs](api-reference-webuntis-apis.md)  Capabilities, constraints, and available domains.
