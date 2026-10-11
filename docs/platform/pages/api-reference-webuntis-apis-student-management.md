# Student Management

> Source: Untis GmbH developer documentation, `developer.untis.com/api-reference/webuntis-apis/student-management/`.
> Reproduced here as an offline mirror so this repository is self-contained.
> © Untis GmbH; see [`NOTICE.md`](../../../NOTICE.md).

---

Manage student master-data including class assignments and user accounts. Unlike OneRoster, this API returns **all students** regardless of whether they have assigned user accounts.

v3  Read & Write   **Endpoints:** 4

**Tip:** v1 and v2 are **deprecated**. Use v3 for all new integrations.

---

## Use cases

Data sync

Synchronize student data from external school management systems.

User provisioning

Create student records and manage user accounts in bulk.

---

## Endpoints

| Method | Operation ID | Description |
| --- | --- | --- |
| `GET` | `getStudentV3` | Get a single student by ID |
| `GET` | `getStudentsV3` | List all students |
| `POST` | `createStudentsV3` | Create students (batch) |
| `PUT` | `updateStudentsV3` | Update students (batch) |

---

## Individual student attributes

In webuntis, schools can define their own attributes for the student master data.  
These can also be managed via the Student API. They are included as key-value pairs in `studentAttributes`.

**Note:** It is important to note, however, that these are optional. In other words, each school can have its own attributes.

---

## Java example

List all students for a school year. Construct the client with an access token obtained via [Client Credentials](core-concepts-authentication-model.md).

```
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatusCode;
import org.springframework.http.MediaType;
import org.springframework.util.StreamUtils;
import org.springframework.web.client.RestClient;
import org.springframework.web.util.UriComponentsBuilder;
import java.nio.charset.StandardCharsets;
import java.util.List;

public class UntisApiClient {

    private final RestClient http;

    public UntisApiClient(String apiUrl, String accessToken) {
        this.http = RestClient.builder()
                .baseUrl(apiUrl)
                .defaultHeader(HttpHeaders.AUTHORIZATION, "Bearer " + accessToken)
                .defaultHeader(HttpHeaders.ACCEPT, MediaType.APPLICATION_JSON_VALUE)
                .build();
    }

    public StudentsResponse getStudents(int schoolYearId) {
        String uri = UriComponentsBuilder
                .fromPath("/WebUntis/api/rest/extern/v3/students")
                .queryParam("schoolYearId", schoolYearId)
                .build().toUriString();

        return http.get()
                .uri(uri)
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
                .body(StudentsResponse.class);
    }

    public record StudentsResponse(List<Student> students) {
        public record Student(int id, String forename, String lastName,
                              User user, List<ClassAssignment> classAssignments) {}
        public record User(int id) {}
        public record ClassAssignment(int classId, String className) {}
    }
}
```

**Usage:**

```
UntisApiClient client = new UntisApiClient("https://api.integration.webuntis.dev", accessToken);
UntisApiClient.StudentsResponse response = client.getStudents(2025);
response.students().forEach(s ->
    System.out.println(s.forename() + " " + s.lastName()));
```

**Note:** Unlike the [OneRoster users endpoint](api-reference-oneroster-apis-users.md), this API returns **all students** regardless of whether they have an assigned user account.

---

## Related pages

[Users (OneRoster)](api-reference-oneroster-apis-users.md)  Read-only student data via the standards-based OneRoster API.

[Class Management](api-reference-webuntis-apis-class-management.md)  Manage the organizational groups (Klassen) that students belong to.

---

## API reference
