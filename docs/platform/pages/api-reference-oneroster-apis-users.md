# Users

> Source: Untis GmbH developer documentation, `developer.untis.com/api-reference/oneroster-apis/users/`.
> Reproduced here as an offline mirror so this repository is self-contained.
> © Untis GmbH; see [`NOTICE.md`](../../../NOTICE.md).

---

The Users entity provides access to student, teacher, and other user profiles. You can query all users at once or filter by role using the dedicated student and teacher endpoints.

OneRoster 1.1  Read-only   **Endpoints:** 10

Note

OneRoster only returns users who have **assigned user accounts**. Students and
teachers without user accounts are not included. For complete master-data, use
the [Untis Platform APIs](api-reference-webuntis-apis.md).

---

## Supported roles

| Role | Endpoint | Description |
| --- | --- | --- |
| **Students** | `/students` | Learners enrolled in classes (`role="student"`) |
| **Teachers** | `/teachers` | Instructors teaching classes (`role="teacher"`) |
| **All users** | `/users` | All roles including administrators and aides |

## WebUntis role mapping

The following table shows how WebUntis user roles map to OneRoster roles:

| WebUntis role | OneRoster role |
| --- | --- |
| `teacher` | `teacher` |
| `student` | `student` |
| `admin` | `administrator` |
| `parent` | `parent` |
| `LG` | `parent` |
| `AR` | `aide` |
| `staff` | `aide` |
| `directorate` | `aide` |
| `other` | `aide` |

---

## Endpoints

| Service call | Endpoint |
| --- | --- |
| `getAllUsers` | `{{API_URL}}/ims/oneroster/v1p1/users` |
| `getUser` | `{{API_URL}}/ims/oneroster/v1p1/users/{id}` |
| `getAllStudents` | `{{API_URL}}/ims/oneroster/v1p1/students` |
| `getStudent` | `{{API_URL}}/ims/oneroster/v1p1/students/{id}` |
| `getAllTeachers` | `{{API_URL}}/ims/oneroster/v1p1/teachers` |
| `getTeacher` | `{{API_URL}}/ims/oneroster/v1p1/teachers/{id}` |
| `getStudentsForSchool` | `{{API_URL}}/ims/oneroster/v1p1/schools/{id}/students` |
| `getTeachersForSchool` | `{{API_URL}}/ims/oneroster/v1p1/schools/{id}/teachers` |
| `getStudentsForClassInSchool` | `{{API_URL}}/ims/oneroster/v1p1/classes/{id}/students` |
| `getTeachersForClassInSchool` | `{{API_URL}}/ims/oneroster/v1p1/classes/{id}/teachers` |

---

## User identifiers

Each user carries multiple identifiers in the `userIds` attribute. Understanding these is critical for linking OneRoster data to Untis Platform master-data.

| Identifier | Scope | Description |
| --- | --- | --- |
| **uuid** | Globally unique | Hashed ID of a user |
| **id** | Unique across users | Internal ID of the user |
| **external-user-id** | Unique across users | External ID of the user |
| **person-id** | Unique within role | Internal ID of the person (master-data) |
| **external-person-id** | Unique within role | External ID of the person (master-data) |
| **short-name** | Unique within role | Short name of the person (master-data) |
| **national-id** | Globally unique | National unique ID of the person (master-data) |

person-id is role-scoped

The `person-id` is **not** unique across roles. Person ID `42` as a student
and Person ID `42` as a teacher are **different people**. Always pair
`person-id` with the role: `(student, 42)` or `(teacher, 42)`. To call
`/students/{id}`, use the OneRoster `sourcedId` — not the `person-id`.

---

## Metadata extensions

Untis Platform enriches user objects with additional metadata:

| Metadata field | Description | Example |
| --- | --- | --- |
| **Sex** | Gender (optional) | `"female"` |
| **Birthdate** | Date of birth (optional) | `"2010-03-15"` |
| **Usergroup** | The user group from Untis Platform | `"Students"` |
| **Userrole** | The user’s role from Untis Platform | `"student"` |

---

## Java example

The `OneRosterClient` below uses **Spring `RestClient`**. It handles token acquisition via [Client Credentials](core-concepts-authentication-model.md) internally — construct it with the tenant ID, client ID, platform-generated password, and an `ObjectMapper` instance. It supports `filter`, `sort`, `limit`, and `offset` on every call.

```
import java.util.List;

public record OneRosterResponse<T>(List<T> items) {}
```

```
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JavaType;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatusCode;
import org.springframework.http.MediaType;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.util.StreamUtils;
import org.springframework.web.client.RestClient;
import org.springframework.web.util.UriComponentsBuilder;
import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.util.Base64;
import java.util.List;
import java.util.Map;

public class OneRosterClient {

    private static final String API_URL = "https://api.integration.webuntis.dev";

    private final String tenantId;
    private final String clientId;
    private final String password;
    private final RestClient http;
    private final ObjectMapper objectMapper;

    private String cachedToken;
    private Instant tokenExpiry = Instant.EPOCH;

    public OneRosterClient(String tenantId, String clientId, String password, ObjectMapper objectMapper) {
        this.tenantId = tenantId;
        this.clientId = clientId;
        this.password = password;
        this.objectMapper = objectMapper;
        this.http = RestClient.builder()
                .baseUrl(API_URL)
                .defaultHeader(HttpHeaders.ACCEPT, MediaType.APPLICATION_JSON_VALUE)
                .build();
    }

    private synchronized String getAuthToken() {
        if (cachedToken == null || Instant.now().isAfter(tokenExpiry)) {
            Map<String, Object> tokenResponse = fetchAccessToken(tenantId, clientId, password);
            cachedToken = (String) tokenResponse.get("access_token");
            int expiresIn = ((Number) tokenResponse.get("expires_in")).intValue();
            tokenExpiry = Instant.now().plusSeconds(expiresIn - 30);
        }
        return cachedToken;
    }

    private Map<String, Object> fetchAccessToken(String tenantId, String clientId, String password) {
        String credentials = Base64.getEncoder()
                .encodeToString((clientId + ":" + password).getBytes(StandardCharsets.UTF_8));

        MultiValueMap<String, String> form = new LinkedMultiValueMap<>();
        form.add("grant_type", "client_credentials");

        return RestClient.create().post()
                .uri(API_URL + "/WebUntis/api/sso/v3/" + tenantId + "/token")
                .header(HttpHeaders.AUTHORIZATION, "Basic " + credentials)
                .header(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_FORM_URLENCODED_VALUE)
                .body(form)
                .retrieve()
                .body(Map.class);
    }

    public <T> OneRosterResponse<T> list(String resource, String envelope,
                                         Class<T> itemType, String filter,
                                         String sort, int limit, int offset) {
        UriComponentsBuilder uri = UriComponentsBuilder
                .fromPath(resource)
                .queryParam("limit",  limit)
                .queryParam("offset", offset);

        if (filter != null && !filter.isBlank()) uri.queryParam("filter", filter);
        if (sort   != null && !sort.isBlank())   uri.queryParam("sort",   sort);

        String json = http.get()
                .uri(uri.build().toUriString())
                .header(HttpHeaders.AUTHORIZATION, "Bearer " + getAuthToken())
                .retrieve()
                .onStatus(HttpStatusCode::is4xxClientError, (req, res) -> {
                    String body = StreamUtils.copyToString(res.getBody(), StandardCharsets.UTF_8);
                    throw new IllegalArgumentException(
                        "[" + res.getStatusCode().value() + "] " + req.getURI() + ": " + body);
                })
                .onStatus(HttpStatusCode::is5xxServerError, (req, res) -> {
                    String body = StreamUtils.copyToString(res.getBody(), StandardCharsets.UTF_8);
                    throw new RuntimeException(
                        "[" + res.getStatusCode().value() + "] " + req.getURI() + ": " + body);
                })
                .body(String.class);

        try {
            JavaType listType = objectMapper.getTypeFactory().constructCollectionType(List.class, itemType);
            List<T> items = objectMapper.readValue(
                    objectMapper.readTree(json).get(envelope).toString(), listType);
            return new OneRosterResponse<>(items);
        } catch (JsonProcessingException e) {
            throw new RuntimeException("Failed to parse OneRoster response", e);
        }
    }
}
```

**Fetch all students, sorted by family name:**

```
OneRosterClient client = new OneRosterClient(tenantId, clientId, password, new ObjectMapper());
OneRosterResponse<UserDto> result = client.list(
    "/ims/oneroster/v1p1/students", "students", UserDto.class, null, "familyName", 100, 0);
List<UserDto> students = result.items();
```

**Filter to a specific role:**

```
OneRosterResponse<UserDto> teachers = client.list(
    "/ims/oneroster/v1p1/users", "users", UserDto.class,
    "role='teacher'", "familyName", 100, 0);
```

Note

The `envelope` parameter must match the response wrapper key — e.g. `users`, `students`, `teachers`.

---

## Related pages

[Enrollments](api-reference-oneroster-apis-enrollments.md)  How users are linked to classes.

[Student Management (Untis Platform)](api-reference-webuntis-apis-student-management.md)  Full master-data access including students without user accounts.
