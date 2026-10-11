# Class Management

> Source: Untis GmbH developer documentation, `developer.untis.com/api-reference/webuntis-apis/class-management/`.
> Reproduced here as an offline mirror so this repository is self-contained.
> © Untis GmbH; see [`NOTICE.md`](../../../NOTICE.md).

---

Manage class (organizational group) master-data. In Untis Platform a **Class (Klasse)** is an organizational group of students like “Grade 10A” or “5B”.

v2  Read & Write   **Endpoints:** 4

Terminology

A **Class** in Untis Platform (an organizational student group) is **not** the
same as a **class** in OneRoster (which represents a lesson). See [Classes
(OneRoster)](api-reference-oneroster-apis-classes.md) for details.

**Tip:** v1 is **deprecated**. Use v2 for all new integrations.

---

## Use cases

SIS sync

Synchronize class structures from school information systems.

Year preparation

Automate class creation for new school years.

---

## Endpoints

| Method | Operation ID | Description |
| --- | --- | --- |
| `GET` | `getClassByIdV2` | Get a single class by ID |
| `GET` | `getClassesV2` | List all classes |
| `POST` | `createClassesV2` | Create classes (batch) |
| `PUT` | `updateClassesV2` | Update classes (batch) |

---

## Related pages

[Classes (OneRoster)](api-reference-oneroster-apis-classes.md)  Read-only access to teaching groups (lessons) via the OneRoster standard.

[Student Management](api-reference-webuntis-apis-student-management.md)  Students reference classes via class assignments.

---

## API reference
