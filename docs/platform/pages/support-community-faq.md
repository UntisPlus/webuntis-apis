# FAQ

> Source: Untis GmbH developer documentation, `developer.untis.com/support-community/faq/`.
> Reproduced here as an offline mirror so this repository is self-contained.
> © Untis GmbH; see [`NOTICE.md`](../../../NOTICE.md).

---

Answers to common questions from integration partners, organized by topic.

## Platform & Authentication

#### The authorize endpoint returns `invalid_resource`. What does this mean?

The `redirect_uri` submitted in the request does not match any of the configured values for your platform application in PAM. At least one UI Integration URL configured in PAM must exactly match the submitted `redirect_uri`. Alternatively, you can define an **SSO Redirect Path** in PAM as the target. See the [SSO Integration guide](integration-guides-sso.md) for configuration requirements.

#### Can pictures such as student profile photos be read from or written to the platform via API?

No. Reading or updating profile pictures is not currently supported by any API.

#### Can the logout redirect URL point to an external domain?

No. The logout endpoint redirect must always be within the same domain as the Untis Platform instance.

#### We are calling the extern Student API but not receiving all students. What could be wrong?

The extern Student API applies a default result limit of **1,000 records** per request. If a school has more students than this, you will not receive the full set in a single call. To retrieve all records, either raise the `limit` parameter or use `offset` to page through successive result sets.

```
GET /WebUntis/api/rest/extern/v3/students?limit=2000
GET /WebUntis/api/rest/extern/v3/students?limit=1000&offset=1000
```

See [Common API Concepts](api-reference-common-api-concepts.md) for pagination details.

#### How can I determine the school name at activation time, before any user has logged in?

Retrieve it via the OneRoster [Organizations & Schools](api-reference-oneroster-apis-organizations-schools.md) endpoint. The school name is returned in the `name` field of the organization record.

#### Is the `sub` claim in the JWT globally unique? And can a user have multiple roles?

The `sub` claim is a UUID and can be treated as globally unique in practice, though Untis does not formally guarantee uniqueness across tenants.

A user account is always associated with exactly one role. If a person requires access under multiple roles, they are assigned multiple separate user accounts.

---

## OneRoster API

#### How can I read all student groups?

Since each student group is always linked to a lesson, it is sufficient to retrieve the lessons (‘class’).

#### Can I query historical data, for example which students were active one month ago?

No. There is no history available through the OneRoster API. However, data from previous school years may be accessible via academic sessions — see [Academic Sessions](api-reference-oneroster-apis-academic-sessions.md) for details.

#### When does a student stop appearing in the OneRoster API?

A student is removed from the API when their account is physically deleted in WebUntis. Inactive or archived accounts may still appear until that deletion occurs.

#### What is the difference between `status` and `enabledUser`?

`enabledUser` reflects whether the user account itself is deactivated in WebUntis — it returns `false` if the account has been disabled. `status` reflects the underlying master data record: if the person (teacher or student) has an exit date in the past, `status` is returned as `tobedeleted`.

#### Which students are returned when querying a specific class?

Only the students enrolled in that specific class (lesson), not all students of the broader WU-class. For example, querying the class representing “Deutsch” for 4b returns only the students in that lesson, not every student in 4b.

#### The `displayName` for teachers differs between schools. Can this be configured?

Yes. The `displayName` value is determined by the school’s own configuration under **Administration → Layout Settings → General** in WebUntis. This is a per-school setting that each school controls.

---

## Untis Platform APIs

#### The extern class API only returns the main class teacher, not subject teachers. Is this a bug?

No, this is by design. A class teacher (*Klassenvorstand* or *Klassenlehrer*) is the teacher formally assigned to a class as its main teacher. A class can have zero or more class teachers.

Subject teachers (*Fachlehrer*) are not returned per class because they are assigned to lessons, not classes. To find all teachers who teach a class, query the lessons for that class and inspect the teacher assignments there.

#### Is a `startDate` always required when assigning a student to a class?

Yes. The `startDate` defines when the student’s assignment to that class begins and is required for the assignment to be valid.

#### How can I retrieve all students belonging to a specific class?

This is not possible through the OneRoster API. Use the extern Student Management API with a `filter` query parameter targeting the class name:

```
GET /WebUntis/api/rest/extern/v3/students?filter=classAssignments.className='1A'
```

See the [Student Management API](api-reference-webuntis-apis-student-management.md) for full details.

---

## Timetable API

#### What is the difference between lessons and periods?

The lesson defines which teacher teaches which students a particular subject in a specific room.  
For example, Mr Aigner teaches all the students in Class 1A maths in Room 01/23.

However, this does not yet specify when and how often this lesson takes place.  
That is defined by the individual periods. It is, in effect, the instantiation of a lesson.  
For example, the lesson mentioned above then takes place during the first period on Monday and the fourth period on Wednesday.

#### Can a school configure a timetable without breaks, so that consecutive lessons share the same end and start time?

Yes. This is common, particularly in Austria, where it is normal for the first two periods to run back-to-back with no break, followed by a longer break afterwards. For example:

| Period | Start | End |
| --- | --- | --- |
| 1 | 08:00 | 08:50 |
| 2 | 08:50 | 09:40 |

The end time of one lesson and the start time of the next can be identical.

#### Are timetable periods stored as recurring events, or are all instances materialized?

All periods are materialized — there are no recurring events in the Timetable API.

#### How should double periods (two consecutive periods grouped together) be handled?

Double periods share the same `lessonId` but are returned as two separate periods because each can be cancelled independently. To group them, compare the following attributes — two periods belong to the same group when all of these match:

- Lesson ID, type, status, exam
- Classes, departments, resources, student groups, students
- Subjects, rooms, teachers

#### What happens when one period in a double lesson is cancelled?

The two periods are shown separately because their attributes (such as teacher) are no longer identical across both. There is no automatic regrouping.

#### How do I detect deleted periods?

Call both `/api/rest/extern/v3/timetable/deleted-periods` and `/api/rest/extern/v3/timetable` using the same `dateLastModifiedAfter` value, and process the results atomically:

- The `deleted-periods` endpoint returns an array of deleted period IDs only — no metadata is included.
- It does not support timetable filters (departments, classes, etc.) — apply filtering on your side after joining the IDs against your local data.
- Only advance `dateLastModifiedAfter` if both calls succeed. If either fails, retry to avoid desync.
- If you cannot call the deleted-periods endpoint, fall back to a full reload for the relevant date range and compute a diff on your side.

#### How does the Timetable API represent teacher changes?

| Scenario | API behaviour |
| --- | --- |
| Teacher changed in substitution planning (individual period) | Original teacher is returned as `REMOVED`; substituting teacher is returned as `REGULAR`. |
| Teacher changed in timetabling (lesson level, whole year or term) | No substitution is recorded. Changing a lesson creates a new clean slate — WebUntis does not track the previous teacher. The API simply reflects the current state. |

#### How do period and resource statuses behave together?

Period and resource statuses are related but do not automatically mirror each other:

- **If a period changes its time:** The original period is cancelled and a new period is created, linked via `relatedPeriod`. Only the last two periods in a chain of shifts are linked. Resource statuses on both periods remain `regular`.
- **If resources are added or removed:** All resource changes are reported individually, and the period status also changes to reflect the modification.
- Any resource change implies a period status change, but a period status change does not necessarily imply a resource change (for example, a time shift).

#### Why does the Timetable API only return abbreviations for subjects, classes, and rooms?

Full names are available through other APIs. For example, full class names can be retrieved via the [Class Management API](api-reference-webuntis-apis-class-management.md).

#### How are notes entered across multiple lessons stored?

Notes can be entered collectively (applying to multiple lessons at once) or per individual lesson. If entered collectively, the data in the first period takes precedence. In the database, notes are stored per individual period.

#### Why is break duration not available via the API?

Break duration is part of the school’s internal timetable configuration and is not exposed through any external API.

#### Is there an API to retrieve the school’s timezone?

No. The timezone is always the school’s local timezone. There is no public endpoint to retrieve it programmatically.

#### Is there a Room API to query rooms directly?

Yes. Rooms can be queried directly via the [Room Management API](api-reference-webuntis-apis-room-management.md), which lists all rooms or fetches a single room by ID.

#### How can I get the start and end dates of a school year?

School years are exposed as academic sessions via the OneRoster [Academic Sessions](api-reference-oneroster-apis-academic-sessions.md) API, which returns each session’s start and end dates.

#### Can I sync data for the whole tenant at once rather than per entity?

Yes. Omit the entity-specific filter (for example the `teacher-id` parameter) and set `dateLastModifiedAfter` to a sufficiently early date to retrieve all records across the tenant.

#### Why am I receiving `HTTP 403` errors from the Timetable API?

This indicates missing permissions for your platform application. If permissions were recently updated, reinstalling the app for the affected school should resolve the issue.
