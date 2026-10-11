# User Management

> Source: Untis GmbH developer documentation, `developer.untis.com/api-reference/webuntis-apis/user-management/`.
> Reproduced here as an offline mirror so this repository is self-contained.
> © Untis GmbH; see [`NOTICE.md`](../../../NOTICE.md).

---

Manage all types of user accounts — including admin users, IT staff, non-teaching staff, students, teachers, legal guardians, and any other user type.

v1  Read & Write   **Endpoints:** 4

---

## Use cases

Admin accounts

Provision accounts for school administrators and IT staff.

Staff management

Create and update user accounts for non-teaching staff who need Untis
Platform access.

---

## Endpoints

| Method | Operation ID | Description |
| --- | --- | --- |
| `GET` | `getUserByExternUuid` | Get a single user by external UUID |
| `GET` | `getUsers` | List all users |
| `POST` | `createUsers` | Create users (batch) |
| `PUT` | `updateUsers` | Update users (batch) |

---

## Related pages

[Student Management](api-reference-webuntis-apis-student-management.md)  For users linked to student master-data.

[Teacher Management](api-reference-webuntis-apis-teacher-management.md)  For users linked to teacher master-data.

---

## API reference
