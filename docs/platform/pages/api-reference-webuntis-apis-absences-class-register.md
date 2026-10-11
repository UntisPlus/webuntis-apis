# Absences & Class Register

> Source: Untis GmbH developer documentation, `developer.untis.com/api-reference/webuntis-apis/absences-class-register/`.
> Reproduced here as an offline mirror so this repository is self-contained.
> © Untis GmbH; see [`NOTICE.md`](../../../NOTICE.md).

---

Read-only access to student absence data from the Untis Platform class register module. Retrieve aggregated absence totals or individual lesson-level absence records.

v1  Read-only   **Endpoints:** 3

Module prerequisite

The class register is an **optional** Untis Platform module. This API is only
available if the class register module is activated for the school.

---

## Use cases

Attendance tracking

Integrate absence data into attendance dashboards and reporting tools.

Parent portals

Show parents detailed absence records for their children.

---

## Endpoints

| Method | Operation ID | Description |
| --- | --- | --- |
| `GET` | `getStudentAbsenceTimes` | Aggregated absence totals per student |
| `POST` | `getStudentAbsences` | Unprocessed Absences per students |
| `GET` | `getStudentLessonAbsences` | Individual lesson-level absence records |

---

## Java example

Retrieve aggregated absence totals per student for a given school year. Construct the client with an access token obtained via [Client Credentials](core-concepts-authentication-model.md).

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

    public AbsencesResponse getStudentAbsenceTimes(int schoolYearId) {
        String uri = UriComponentsBuilder
                .fromPath("/WebUntis/api/rest/extern/v1/classreg/students/absencetimes")
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
                .body(AbsencesResponse.class);
    }

    public record AbsencesResponse(List<StudentAbsence> students) {
        public record StudentAbsence(int studentId, String studentExternKey,
                                     AbsenceTotals totals, AbsenceTotals excusedTotals,
                                     AbsenceTotals unexcusedTotals,
                                     List<AbsenceTime> absenceTimes) {}
        public record AbsenceTotals(DayCount days, int hours, int delays) {}
        public record DayCount(int count, int remainingHours) {}
        public record AbsenceTime(String start, String end, int minutes,
                                  String subjectName, String status, String type) {}
    }
}
```

**Usage:**

```
UntisApiClient client = new UntisApiClient("https://api.integration.webuntis.dev", accessToken);
UntisApiClient.AbsencesResponse response = client.getStudentAbsenceTimes(2025);
response.students().forEach(s -> {
    System.out.println("Student " + s.studentId()
        + " — total hours absent: " + s.totals().hours());
});
```

Module prerequisite

This endpoint returns a `404` if the class register module is not activated for the school. Handle this case explicitly in your error handler.

---

## Related pages

[Student Management](api-reference-webuntis-apis-student-management.md)  The student master-data referenced in absence records.

[Lessons](api-reference-webuntis-apis-lessons.md)  Lesson data that absence records refer to.

---

## API reference
