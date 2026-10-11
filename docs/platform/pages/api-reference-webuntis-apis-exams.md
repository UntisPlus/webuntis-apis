# Exams

> Source: Untis GmbH developer documentation, `developer.untis.com/api-reference/webuntis-apis/exams/`.
> Reproduced here as an offline mirror so this repository is self-contained.
> © Untis GmbH; see [`NOTICE.md`](../../../NOTICE.md).

---

Read-only access to exam data and exam type definitions. Retrieve upcoming exams with date, time, class/subject, and related student information.

v1  Read-only   **Endpoints:** 2

---

## Use cases

Student portals

Display upcoming exams for students and parents.

LMS integration

Sync exam schedules into learning management systems and study planning
tools.

---

## Endpoints

| Method | Operation ID | Description |
| --- | --- | --- |
| `GET` | `getExams` | List exams with date, time, and class/subject |
| `GET` | `getExamTypes` | List exam type definitions |

---

## Related pages

[Timetable Data](api-reference-webuntis-apis-timetable-data.md)  Timetable context for when exams are scheduled.

[Absences & Class Register](api-reference-webuntis-apis-absences-class-register.md)  Track absences for exam-related attendance.

---

## API reference
