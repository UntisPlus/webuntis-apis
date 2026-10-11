# API Overview & Base URLs

> Source: Untis GmbH developer documentation, `developer.untis.com/api-reference/api-overview/`.
> Reproduced here as an offline mirror so this repository is self-contained.
> © Untis GmbH; see [`NOTICE.md`](../../../NOTICE.md).

---

The Untis Platform APIs enable data exchange between Untis Platform and third-party applications — retrieving roster data, synchronizing masterdata, reading timetables, and more. All requests are routed through a **central API gateway** that handles authentication, authorization, rate limiting, and consistent error handling.

Central Gateway

Every API call goes through a single gateway — one entry point for all
integrations, regardless of API family or version.

Two API Families

**OneRoster** for standardized read-only roster data. **Untis Platform
APIs** for full masterdata access with read and write operations.

URL-based Versioning

Each API maintains its own version in the URL path. Updates to one API do
not affect another.

---

## Environments & base URLs

All API requests use the `{{API_URL}}` placeholder, which resolves to the appropriate base URL depending on your environment.

Integration

`https://api.integration.webuntis.dev/`

Development and testing with test schools and synthetic data. Mirrors production behavior. May include preview features.

The interactive **Try it out** in these docs runs against a dedicated **sandbox school** (isolated tenant) on this environment.

Production

`https://api.webuntis.com/`

Live school data. Requires an approved platform application. Production-level SLAs and stricter rate limits.

**Caution:** Never use production for development or experimentation. Test in the integration environment first!

---

## Rate Limiting

Our platform operates on the basis of the fair use principle. All requests made by every platform app are actively monitored.

**Note:** Nevertheless, there are strict limits:
Your app may send a **maximum of 40 requests per second**.

Furthermore, larger synchronisation jobs must be scheduled for off-peak hours. This means Monday to Friday between 7.00 pm and 5.00 am, or at weekends.
Please do not carry them out during the schools’ main working hours (06:00 to 09:00).

---

## Interactive Try it out

Every API reference page in these docs includes a live **Try it out** button on each endpoint. Requests are executed against a **dedicated sandbox school** — a separate, isolated tenant on the integration environment — with no setup or credentials needed on your end.

- Authentication is handled automatically. A short-lived access token is obtained server-side via the Client Credentials flow using the sandbox school’s credentials, then injected into every request.
- The sandbox school is a real, isolated tenant with synthetic data. It will not affect any other school.
- Responses reflect real API behavior since the integration environment mirrors production.
- The sandbox client has **read-only permissions** — data cannot be modified.

**Note:** Write operations (POST, PUT, DELETE) will be rejected by the sandbox school’s
permission scope. To test write flows, use your own integration tenant with
your own credentials.

---

## API families

The platform exposes two distinct API families. Choose based on your data access and write requirements — see [Which API to Choose](api-reference-which-api-to-choose.md) for a detailed decision guide.

OneRoster APIs

Standardized **read-only** access to roster data following the [IMS Global OneRoster 1.1 specification](https://www.imsglobal.org/oneroster-v11-final-specification).

**Endpoint pattern:** `{{API_URL}}/ims/oneroster/v1p1/{resource}`

Best for LMS integrations, student portals, and read-only data sync.

[OneRoster API Reference →](api-reference-oneroster-apis.md)

Untis Platform APIs

Comprehensive **read and write** access to masterdata and Untis Platform-specific features beyond the OneRoster standard.

**Endpoint pattern:** `{{API_URL}}/WebUntis/api/rest/extern/v{version}/{resource}`

Best for school management systems, admin tools, and bidirectional sync.

[Untis Platform API Reference →](api-reference-webuntis-apis.md)

---

## Versioning and deprecation

The platform uses **URL-based versioning**. Each API maintains an independent version lifecycle — an update to the Student Management API does not affect Teacher Management. OneRoster uses version `v1p1` (1.1) in the URL path; Untis Platform APIs use `v1`, `v2`, or `v3` depending on the API.

### Current Untis Platform APIs & their versions

| API | Current Version | Status |
| --- | --- | --- |
| Student Management | v3 | v1 and v2 deprecated |
| Teacher Management | v2 | v1 deprecated |
| Legal Guardian Management | v1 | Current |
| Class Management | v2 | v1 deprecated |
| Room Management | v1 | Current (read-only) |
| Subject Management | v1 | Current (read-only) |
| User Management | v1 | Current |
| Teacher Absence Management | v1 | Current |
| Teacher Absence Reasons | v1 | Current |
| Timetable | v3 | v1 and v2 deprecated |
| Class Register Absences | v1 | Current |
| Exams | v1 | Current |
| Lessons | v1 | Current |
| Messaging | v1 | Current |
| Timetable Event Push | v1 | Current |

Deprecated versions

Deprecated versions still function but receive no new features or fixes. Migrate to the current version.

- **Student Management** v1 and v2 → migrate to **v3**
- **Teacher Management** v1 → migrate to **v2**
- **Class Management** v1 → migrate to **v2**

See the [Changelog](support-community-changelog.md) for deprecation announcements and migration guidance.

---

## Related guides

[Which API to Choose](api-reference-which-api-to-choose.md)  Decision guide for choosing between OneRoster and Untis Platform APIs.

[Common API Concepts](api-reference-common-api-concepts.md)  Pagination, sorting, and filtering — shared across both API families.

[Authentication Model](core-concepts-authentication-model.md)  How to obtain tokens for API access — Client Credentials and OIDC flows.

[Authorization Model](core-concepts-authorization-model.md)  Scopes, permissions, and tenant isolation.
