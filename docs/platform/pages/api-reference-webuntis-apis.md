# Untis Platform APIs

> Source: Untis GmbH developer documentation, `developer.untis.com/api-reference/webuntis-apis/`.
> Reproduced here as an offline mirror so this repository is self-contained.
> © Untis GmbH; see [`NOTICE.md`](../../../NOTICE.md).

---

Untis Platform APIs provide comprehensive access to master-data and platform-specific functionality that extends beyond the OneRoster standard. Use these APIs when you need **write access**, **complete master-data** (including entities without user accounts), or **platform-specific features** like timetables, absences, exams, and messaging.

---

## Management APIs (read & write)

Create, read, and update master-data.

[Student Management](api-reference-webuntis-apis-student-management.md)  Student master-data, class assignments, and user accounts.

[Teacher Management](api-reference-webuntis-apis-teacher-management.md)  Teacher master-data and user accounts.

[Class Management](api-reference-webuntis-apis-class-management.md)  Organizational student groups (Klassen).

[Legal Guardian Management](api-reference-webuntis-apis-legal-guardian-management.md)  Parent/guardian master-data and portal access.

[User Management](api-reference-webuntis-apis-user-management.md)  Admin and staff users without master-data.

[Teacher Absence Management](api-reference-webuntis-apis-teacher-absence-management.md)  Teacher absence management

[Teacher Absence Reason Management](api-reference-webuntis-apis-teacher-absence-reason-management.md)  Teacher absence reason management

---

## Data APIs (read-only)

Read-only access to timetable, attendance, exam, lesson, room and subject data.

[Timetable Data](api-reference-webuntis-apis-timetable-data.md)  Real-time timetable with substitutions and changes.

[Absences & Class Register](api-reference-webuntis-apis-absences-class-register.md)  Student absence data from the class register module.

[Exams](api-reference-webuntis-apis-exams.md)  Exam schedules and exam type definitions.

[Lessons](api-reference-webuntis-apis-lessons.md)  Lesson info with complete student lists (including students without users).

[Room Management](api-reference-webuntis-apis-room-management.md)  Room master-data and location information.

[Subject Management](api-reference-webuntis-apis-subject-management.md)  Subject master-data.

---

## Data APIs (write)

Write / push data to WebUntis.

[Timetable Push Events](api-reference-webuntis-apis-timetable-event-push.md)  Platform apps can push events for displaying in the timetable.

---

## Communication

[Messaging](api-reference-webuntis-apis-messaging.md)  Send messages to Untis Platform users as the platform or on behalf of a user.

---

## Shared constraints

Payload size limit

All Untis Platform APIs enforce a **10 MB maximum payload** for both requests
and responses. Exceeding this limit returns HTTP 413. Use pagination, filters,
and smaller batch sizes to stay within the limit.

No delete operations

Student, teacher, guardian, class, and user deletion must be done
**manually** in Untis Platform — it is not available via the API.

Module dependencies

Some APIs require optional Untis Platform modules. For example, the Absences
& Class Register API is only available when the class register module is
activated.

Version-specific endpoints

Each API maintains **independent versioning**. Always use the latest version
for new integrations. See the [API version
table](api-reference-api-overview.md)
for details.

---

## Related guides

[Which API to Choose](api-reference-which-api-to-choose.md)  Side-by-side comparison between OneRoster and Untis Platform APIs.

[Common API Concepts](api-reference-common-api-concepts.md)  Pagination, sorting, and filtering — shared across both API families.

[OneRoster APIs](api-reference-oneroster-apis.md)  Standards-based read-only roster data.
