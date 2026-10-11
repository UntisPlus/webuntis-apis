# Timetable Data

> Source: Untis GmbH developer documentation, `developer.untis.com/api-reference/webuntis-apis/timetable-data/`.
> Reproduced here as an offline mirror so this repository is self-contained.
> © Untis GmbH; see [`NOTICE.md`](../../../NOTICE.md).

---

Access real-time timetable data including scheduled lessons, substitutions, cancellations, and room changes. Filter by resource type, date range, and change status.

v3  Read-only   **Endpoints:** 3 (across versions)

**Tip:** v2 and v1 are still available but **v3 is recommended** for all new
integrations.

---

## Use cases

Timetable apps

Display student and teacher timetables in mobile apps or digital signage.

Substitution plans

Show real-time substitutions, cancellations, and room changes.

---

## Endpoints

| Method | Operation ID | Description |
| --- | --- | --- |
| `GET` | `getTimetable` | Timetable (v1, deprecated) |
| `GET` | `getTimetableV2` | Timetable (v2, deprecated) |
| `GET` | `getTimetableV3` | Timetable (v3, recommended) |

---

## Filtering options

| Filter | Description |
| --- | --- |
| **start / end** | Date range for the requested timetable window (ISO 8601) |
| **Resource filter** (class, student, teacher, room, lesson) | Filter by a specific resource — by Untis ID or external ID |
| **dateLastModifiedAfter** | Returns only periods modified after the given timestamp. **Recommended** — avoids fetching the full timetable on every call |
| **Change status** | All periods or only changed periods |
| **Timetable source** | Scheduled timetable from planning or real-time data |

**Tip:** Prefer **`dateLastModifiedAfter`** over a fixed date range for incremental
sync. It returns only what has changed since your last call, keeping responses
small and avoiding a full timetable reload on every poll. Use a fixed date
range (start/end) when you need to load a specific window for the first time
or after a full reset.

---

## Detecting deleted periods

v3 includes a dedicated endpoint for deleted period IDs. Use it alongside the main timetable endpoint to detect and remove periods that no longer exist.

```
GET {{API_URL}}/WebUntis/api/rest/extern/v3/timetable/deleted-periods
```

| Behaviour | Detail |
| --- | --- |
| Returns | An array of deleted period IDs only — no metadata |
| Filtering | Does **not** support timetable filters (departments, classes, etc.) — filter on your side by joining against your stored data |
| Required parameter | `dateLastModifiedAfter` — use the same value as your main timetable call |

Process both calls atomically

Always call `/v3/timetable` and `/v3/timetable/deleted-periods` with the **same `dateLastModifiedAfter`** value and process the results together. Advance `dateLastModifiedAfter` only when both calls succeed — otherwise retry both to avoid data desync. If the deleted-periods endpoint is unavailable, fall back to a full reload (start/end range) and diff on your side.

---

## Double periods

Periods that span two consecutive time slots (double periods) share the same `lessonId` but appear as **two separate period records** in the response — because they can be cancelled individually (e.g. different substitution teachers per slot).

Two periods are considered equivalent if all of the following attributes match:

`lessonId`, `type`, `status`, `exam`, `classes`, `departments`, `resources`, `studentGroups`, `students`, `subjects`, `rooms`, `teachers`

Group them on your side using this comparison when you need to display double periods as a single event. If any of those attributes differs between the two slots, display them separately.

---

## Java example

The `UntisApiClient` below uses [**Spring `RestClient`**](https://docs.spring.io/spring-framework/reference/integration/rest-clients.html). Construct it with an access token obtained via [Client Credentials](core-concepts-authentication-model.md).

```
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatusCode;
import org.springframework.http.MediaType;
import org.springframework.util.StreamUtils;
import org.springframework.web.client.RestClient;
import org.springframework.web.util.UriComponentsBuilder;
import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;
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

    private <T> T get(String uri, Class<T> responseType) {
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
                .body(responseType);
    }

    public TimetableResponse getTimetable(LocalDate start, LocalDate end,
                                          Instant dateLastModifiedAfter) {
        UriComponentsBuilder uri = UriComponentsBuilder
                .fromPath("/WebUntis/api/rest/extern/v3/timetable")
                .queryParam("start", start.toString())
                .queryParam("end",   end.toString());

        if (dateLastModifiedAfter != null) {
            String formatted = dateLastModifiedAfter.atZone(ZoneOffset.UTC)
                    .toLocalDateTime()
                    .format(DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss"));
            uri.queryParam("dateLastModifiedAfter", formatted);
        }

        return get(uri.build().toUriString(), TimetableResponse.class);
    }

    public record TimetableResponse(
            HeaderData headerData, MasterData masterData, TimetableData timetableData) {
        public record HeaderData(SchoolRef school) {}
        public record SchoolRef(String tenantId, String name) {}
        public record MasterData(List<Resource> classes, List<Resource> teachers,
                                 List<Resource> rooms, List<Resource> subjects,
                                 List<Resource> students) {}
        public record Resource(int id, String externKey, String displayName) {}
        public record TimetableData(List<Period> periods) {}
        public record Period(int id, String modified, String start, String end,
                             String type, String status,
                             List<ResourceRef> classes, List<ResourceRef> teachers,
                             List<ResourceRef> rooms, List<ResourceRef> subjects,
                             List<ResourceRef> students) {}
        public record ResourceRef(int id, String status) {}
    }
}
```

**Usage:**

```
UntisApiClient client = new UntisApiClient("https://api.integration.webuntis.dev", accessToken);

// Full load for a date range
UntisApiClient.TimetableResponse full =
    client.getTimetable(LocalDate.of(2025, 9, 1), LocalDate.of(2025, 9, 30), null);

// Incremental update — only periods changed since last sync
UntisApiClient.TimetableResponse delta =
    client.getTimetable(LocalDate.of(2025, 9, 1), LocalDate.of(2025, 9, 30), Instant.parse("2025-09-15T08:00:00Z"));
```

**Tip:** For regular polling, always pass `dateLastModifiedAfter` to receive only what has changed. Advance this value only after both the timetable call and the [deleted-periods call](#detecting-deleted-periods) succeed.

---

## Related pages

[Room Management](api-reference-webuntis-apis-room-management.md)  Room master-data referenced in timetable entries.

[Calendar Integration Guide](integration-guides-calendar.md)  How to build calendar integrations with timetable data.

---

## API reference
