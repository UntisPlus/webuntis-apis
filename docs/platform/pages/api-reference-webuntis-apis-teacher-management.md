# Teacher Management

> Source: Untis GmbH developer documentation, `developer.untis.com/api-reference/webuntis-apis/teacher-management/`.
> Reproduced here as an offline mirror so this repository is self-contained.
> © Untis GmbH; see [`NOTICE.md`](../../../NOTICE.md).

---

Manage teacher master-data and user accounts. Returns all teachers regardless of whether they have assigned user accounts.

v2  Read & Write   **Endpoints:** 4

Tip

v1 is **deprecated**. Use v2 for all new integrations.

---

## Use cases

HR integration

Synchronize teacher records from HR systems and onboarding workflows.

Account management

Create teacher records and manage their user accounts.

---

## Endpoints

| Method | Operation ID | Description |
| --- | --- | --- |
| `GET` | `getTeacherById` | Get a single teacher by ID |
| `GET` | `getTeachers` | List all teachers |
| `POST` | `createTeachers` | Create teachers (batch) |
| `PUT` | `updateTeachers` | Update teachers (batch) |

---

## Related pages

[Users (OneRoster)](api-reference-oneroster-apis-users.md)  Read-only teacher data via the standards-based OneRoster API.

[Student Management](api-reference-webuntis-apis-student-management.md)  Manage student master-data with a similar API structure.

---

## API reference
