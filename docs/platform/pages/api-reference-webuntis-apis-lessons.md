# Lessons

> Source: Untis GmbH developer documentation, `developer.untis.com/api-reference/webuntis-apis/lessons/`.
> Reproduced here as an offline mirror so this repository is self-contained.
> © Untis GmbH; see [`NOTICE.md`](../../../NOTICE.md).

---

Read-only access to lesson data and associated student information. Unlike OneRoster, this API returns **students without assigned users**, giving you complete lesson rosters regardless of user account status.

v1  Read-only   **Endpoints:** 1

Tip

If you only need students **with** user accounts, the [Classes
(OneRoster)](api-reference-oneroster-apis-classes.md) endpoint may be simpler.
Use this API when you need the **complete** student list.

---

## Use cases

Complete rosters

Get full student lists for lessons, including students without user
accounts.

Attendance systems

Build attendance tracking that covers all enrolled students.

---

## Endpoints

| Method | Operation ID | Description |
| --- | --- | --- |
| `GET` | `getLessons` | List lessons with associated students |

---

## Related pages

[Classes (OneRoster)](api-reference-oneroster-apis-classes.md)  OneRoster classes = Untis Platform lessons (user-assigned students only).

[Absences & Class Register](api-reference-webuntis-apis-absences-class-register.md)  Absence data references these lesson records.

---

## API reference
