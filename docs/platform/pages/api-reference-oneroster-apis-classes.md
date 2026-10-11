# Classes

> Source: Untis GmbH developer documentation, `developer.untis.com/api-reference/oneroster-apis/classes/`.
> Reproduced here as an offline mirror so this repository is self-contained.
> © Untis GmbH; see [`NOTICE.md`](../../../NOTICE.md).

---

In OneRoster, a **class** represents a teaching group where instruction occurs — the unit where students and teachers are enrolled, attendance is recorded, and timetable scheduling happens.

OneRoster 1.1  Read-only   **Endpoints:** 2

Terminology alert

A **class** in OneRoster is **not** the same as a **Class (Klasse)** in Untis
Platform. OneRoster classes map to Untis Platform **lessons** (Unterricht).
Untis Platform Classes (organizational student groups like “9A”) are **not**
exposed as OneRoster classes — they appear only in metadata.

---

## Endpoints

| Service call | Endpoint |
| --- | --- |
| `getAllClasses` | `{{API_URL}}/ims/oneroster/v1p1/classes` |
| `getClass` | `{{API_URL}}/ims/oneroster/v1p1/classes/{id}` |

---

## Mapping to Untis Platform

Lesson (Unterricht) = OneRoster Class

A teaching group for a specific subject, taught by one or more teachers, with enrolled students from one or more Untis Platform Classes.

**Example:** “Biology - 9th Grade - Mr. Smith” is exposed as a OneRoster **class**.

Class (Klasse) ≠ OneRoster Class

An administrative/organizational student group (e.g., “9A”, “10B”) — typically a homeroom or form group. This information appears in **metadata extensions**, not as a separate OneRoster entity.

| Untis Platform term | English | OneRoster equivalent |
| --- | --- | --- |
| **Unterricht** | Lesson | **Class** |
| **Klasse** | Class (organizational group) | *(metadata only)* |

---

## Metadata extensions

Untis Platform enriches OneRoster class objects with additional metadata:

| Metadata field | Description | Example |
| --- | --- | --- |
| **Untis Platform-Classes ID** | ID and name of the organizational classes | `"1A"`, `"9B"` |
| **From- and to-date** | Date range of the lesson | `"2025-09-01"` |
| **Lesson name** | Optional name of the lesson | `"Biology Lab"` |

---

## Java example

Fetch all classes (lessons), sorted by title. Uses the shared `OneRosterClient` — see the [Users page](api-reference-oneroster-apis-users.md) for the full client setup.

```
OneRosterClient client = new OneRosterClient(tenantId, clientId, password, new ObjectMapper());
OneRosterResponse<Map<String, Object>> result = client.list(
    "/ims/oneroster/v1p1/classes", "classes", Map.class, null, "title", 100, 0);

List<Map<String, Object>> classes = result.items();
classes.forEach(c -> System.out.println(c.get("title")));
```

Terminology reminder

OneRoster **classes** map to Untis Platform **lessons** (Unterricht) — not to organizational classes (Klassen). The `metadata` field on each class object contains additional Untis Platform-specific data such as the associated Klassen IDs.

---

## Related pages

[Enrollments](api-reference-oneroster-apis-enrollments.md)  User-to-class membership relationships.

[Class Management (Untis Platform)](api-reference-webuntis-apis-class-management.md)  Create and update organizational student groups (Klassen) via the Untis Platform API.
