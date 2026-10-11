# Teacher Absence Management

> Source: Untis GmbH developer documentation, `developer.untis.com/api-reference/webuntis-apis/teacher-absence-management/`.
> Reproduced here as an offline mirror so this repository is self-contained.
> © Untis GmbH; see [`NOTICE.md`](../../../NOTICE.md).

---

Manage teacher absences, you can create, update & delete teacher absences.

v1  Read & Write   **Endpoints:** 5

---

## Use cases

Substitution planning

Identify substitution needs based on teacher absences.

Parent/Teacher talks

Synchronize teacher absences when planning parent-teacher talks.

---

## Endpoints

| Method | Operation ID | Description |
| --- | --- | --- |
| `GET` | `getTeacherAbsenceById` | Get a single teacher absence by ID |
| `GET` | `getTeacherAbsences` | List teacher absences |
| `POST` | `createTeacherAbsence` | Create a teacher absence |
| `PUT` | `updateTeacherAbsence` | Update a teacher absence |
| `DELETE` | `deleteTeacherAbsence` | Delete a teacher absence |

---

## Related pages

[Timetable Data](api-reference-webuntis-apis-timetable-data.md)  Real-time timetable data including teacher absences.

[Untis Platform APIs Overview](api-reference-webuntis-apis.md)  All available Untis Platform APIs and shared constraints.

---

## API reference
