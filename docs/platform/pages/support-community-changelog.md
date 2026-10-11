# Changelog

> Source: Untis GmbH developer documentation, `developer.untis.com/support-community/changelog/`.
> Reproduced here as an offline mirror so this repository is self-contained.
> © Untis GmbH; see [`NOTICE.md`](../../../NOTICE.md).

---

All notable changes to the Untis Platform integration APIs, authorization endpoints, and platform features are documented here in reverse chronological order.

**Tip:**

**Subscribe to the RSS feed** to get notified whenever a new entry is added to
this changelog. Point your RSS reader or CI pipeline to:

`https://developer.untis.com/rss.xml`

This is the recommended way for integration partners to stay informed about
API changes, new features, and deprecations. RSS is a pull-based mechanism —
updates are only delivered if you actively subscribe. If your team does not
have an RSS reader set up, consider using a service such as
[Feedly](https://feedly.com), [Inoreader](https://www.inoreader.com), or a
Slack RSS integration to route feed updates directly into your team’s
workflow.

**Note:** Dates in the **Release date** column indicate when the change became available
on production. A dash means the change was documentation-only.

| Change date | Release date | Description |
| --- | --- | --- |
| 21.09.2026 | 08.10.2026 | Field 'periodsPerWeek' added to getLessons. See [Lessons](api-reference-webuntis-apis-lessons.md). |
| 04.09.2026 | 16.09.2026 | Add missing information about nullable fields during platform application activation. See [Credentials Webhooks](integration-guides-webhooks-credentials.md) |
| 31.08.2026 | 16.09.2026 | New endpoint 'getStudentAbsences' in the extern **class register absences API** to retrieve absences for a given set of students. See [Absences & Class Register](api-reference-webuntis-apis-absences-class-register.md). |
| 19.08.2026 | 19.08.2026 | Updated descriptions in the external **platform calender events push API**. See [Timetable Push Events](api-reference-webuntis-apis-timetable-event-push.md). |
| 19.08.2026 | 19.08.2026 | Fixed name of field 'building.Id' to 'building.id' in extern room management api. See [Room Management](api-reference-webuntis-apis-room-management.md). |
| 28.07.2026 | 05.08.2026 | Field 'dateLastModifiedAfter' added to getTeacherAbsences. See [Teacher Absence Management](api-reference-webuntis-apis-teacher-absence-management.md). |
| 09.07.2026 | ca. 2026-08 | Field 'source' in the external **platform calender events push API** was removed. The source is now being extracted from the token. See [Timetable Push Events](api-reference-webuntis-apis-timetable-event-push.md). |
| 07.07.2026 | ca. 2026-08 | Renaming and removing of fields in the external **platform calender events push API** to push calendar events to the timetable. See [Timetable Push Events](api-reference-webuntis-apis-timetable-event-push.md). |
| 06.07.2026 | 15.07.2026 | **Federating a school's third-party identity provider** (O365, LDAP, SAML, OIDC). See [Federation to a school's third-party IdP](core-concepts-authentication-model.md). |
| 30.06.2026 | ca. 2026-08 | **New external API** to push calendar events to the timetable. See [Timetable Push Events](api-reference-webuntis-apis-timetable-event-push.md). |
| 24.06.2026 | 15.07.2026 | **prompt=login** added to the OIDC Authorization Code Flow. See [Step 1 – Call the authorize endpoint](integration-guides-sso.md). |
| 18.06.2026 | 15.07.2026 | **PKCE support** added to the OIDC Authorization Code Flow. See [PKCE for Public Clients](core-concepts-authentication-model.md). |
| 29.05.2026 | 24.06.2026 | **New external API** to read teacher absence reasons. See [Teacher Absence Reason Management](api-reference-webuntis-apis-teacher-absence-reason-management.md). |
| 26.05.2026 | 24.06.2026 | **New external API** to manage teacher absences. See [Teacher Absence Management](api-reference-webuntis-apis-teacher-absence-management.md). |
| 11.05.2026 | 02.06.2026 | **New external API** to read subject masterdata. See [Subject Management](api-reference-webuntis-apis-subject-management.md). |
| 03.02.2026 | 24.03.2026 | **Shutdown of deprecated Auth-Endpoints and old credentials transfer!**   v1 and v2 of the Auth-Endpoints (SSO) will be removed.  v1 of the credentials transfer will be removed. All Apps get upgraded to v2 automatically. |
| 19.02.2026 | 19.02.2026 | **Bug fix — OneRoster academic sessions:** Future academic sessions are no longer returned as `tobedeleted`. Academic sessions valid from/until today are now returned as `active`. |
| 10.02.2026 | 18.02.2026 | **New external API** to manage users (even without masterdata). See [User Management](api-reference-webuntis-apis-user-management.md). |
| 18.12.2025 | 28.01.2026 | **New external API** to read room masterdata. See [Room Management](api-reference-webuntis-apis-room-management.md). |
| 17.12.2025 | 28.01.2026 | Lessons returned by the external lesson API have a new field `lectureId`. It contains the Untis lecture ID if it is a regular lesson imported from Untis. |
| 04.11.2025 | 12.11.2025 | **New version of the external teacher API: Version 2.** Fixed target hours per week — now a decimal number instead of an integer. See [Teacher Management](api-reference-webuntis-apis-teacher-management.md). |
| 06.10.2025 | 22.10.2025 | Token endpoint now returns `expires_in` — the number of seconds the access token is valid. Only available in v3 (not in v1 or v2). |
| 23.09.2025 | 01.10.2025 | External WebUntis APIs can now be called with the user's access token. |
| 16.06.2025 | 23.06.2025 | **New version of auth endpoints: Version 3.** The issuer is now a valid URL (instead of `webuntis`). The userinfo endpoint returns correct JSON (instead of a JWT). The well-known endpoint now only returns URLs to the API gateway. |
| 10.06.2025 | 23.06.2025 | **Separate redirect path for SSO.** It is now possible to define a separate SSO-redirect-path instead of using the UI-integration redirect path. |
| 05.06.2025 | 23.06.2025 | **New endpoint for app deactivation.** The platform now notifies your system when an app is deactivated. See [Deactivation Webhook](integration-guides-webhooks-deactivation.md). |
| 05.06.2025 | 05.06.2025 | **New version of credentials endpoint (v2).** Provides more information about the school. V1 is deprecated — upgrade to v2. See [Credentials Webhook](integration-guides-webhooks-credentials.md). |
| 22.04.2025 | 07.05.2025 | **OneRoster — Enrollments:** `getAllEnrollments` for an entire school now returns only enrollments of the current school year. Other enrollment endpoints return enrollments independent of school years. |
| 07.04.2025 | 07.04.2025 | **New Messaging API.** Send information to users via the WebUntis messaging system. See [Messaging](api-reference-webuntis-apis-messaging.md). |
| 11.02.2025 | — | Documentation change: renamed `EAP_URL` to `API_URL`. |
| 20.01.2025 | 21.01.2025 | **All APIs (including authorize and token endpoints) can now be called via the `API_URL`.** It is no longer necessary to know the school-specific WebUntis URL. The only URLs you need: `api.integration.webuntis.dev` and `api.webuntis.com`. |
| 19.11.2024 | 04.12.2024 | Company name (name of the integration partner) is now shown for every app in the platform. |
| 22.10.2024 | 13.11.2024 | **New OneRoster APIs: Enrollments.** Get information about when a student or teacher starts and ends in a specific lesson. See [Enrollments](api-reference-oneroster-apis-enrollments.md). |
| 11.10.2024 | 23.10.2024 | **Version 2 of Class API** is now available for all endpoints. V1 is deprecated. See [Class Management](api-reference-webuntis-apis-class-management.md). |
| 23.09.2024 | 02.10.2024 | Refresh token now gets invalidated if password is changed in WebUntis. |
| 02.07.2024 | 31.07.2024 | **New API** to manage legal guardian masterdata and their users. See [Legal Guardian Management](api-reference-webuntis-apis-legal-guardian-management.md). |
| 20.06.2024 | 10.07.2024 | **New API** to manage teacher masterdata and their users. See [Teacher Management](api-reference-webuntis-apis-teacher-management.md). |
| 20.06.2024 | 10.07.2024 | Changes for Student API (v1 and v3): new optional attribute `attestationRequirementSince`. Updating a student no longer changes the school-specific sorting of students. |
| 21.05.2024 | 29.05.2024 | **New version v3 of the Student API.** New error handling, returns all classes of all school years by default, new `schoolyear` filter parameter, new `nationalId` attribute. See [Student Management](api-reference-webuntis-apis-student-management.md). |
| 12.04.2024 | 07.05.2024 | **New version v2 of the Class API.** Now returns all classes of all school years. Filter by `schoolyearId` for specific school years. |
| 12.04.2024 | 17.04.2024 | OneRoster API: new attribute `national_id` in user responses. |
| 12.04.2024 | 17.04.2024 | Student API and OneRoster API: fixed a bug in sorting, filtering, and pagination. |
| 08.03.2024 | 28.03.2024 | OneRoster classes now include the `terms` attribute, which refers to the related school year. Use this to filter for all classes (lessons) in a specific school year. |
| 08.03.2024 | 11.03.2024 | Maximum API payload size raised to 10 MB. |
| 30.11.2023 | 30.11.2023 | **New version of authorize and token endpoints.** V2 uses `tenantId` instead of `schoolname`. The old version with `schoolname` is deprecated. |
| 03.11.2023 | 16.11.2023 | New parameter `countingOnly` for the absence times API. |
| 12.10.2023 | 27.10.2023 | Refresh token is now valid for one year. |
| 30.08.2023 | 14.09.2023 | Student API: `forename` is no longer mandatory. |
| 14.08.2023 | 24.08.2023 | New authorization endpoints with `tenantId` instead of `schoolname`. |
| 14.08.2023 | 24.08.2023 | **New API** to read lessons and their students — without requiring users for the students. See [Lessons](api-reference-webuntis-apis-lessons.md). |
| 14.08.2023 | 24.08.2023 | **New version of the Timetable API (v3)** with different error handling. See [Timetable Data](api-reference-webuntis-apis-timetable-data.md). |
| 14.08.2023 | 03.08.2023 | **New API** to manage class masterdata. See [Class Management](api-reference-webuntis-apis-class-management.md). |
| 11.05.2023 | 01.06.2023 | Calendar specification to integrate your appointments in the timetable is ready to use. See [Calendar Integration](integration-guides-calendar.md). |
| 11.05.2023 | 01.06.2023 | OneRoster API: `orgs` endpoint now accepts alphanumeric IDs. |
| 11.05.2023 | 01.06.2023 | OneRoster API: `lessonName` is now returned for classes. |
| 10.05.2023 | 10.05.2023 | **Two new APIs** for reading exams and exam types. See [Exams](api-reference-webuntis-apis-exams.md). |
| 06.04.2023 | 06.04.2023 | **New API** for reading student absences from the class register. See [Absences & Class Register](api-reference-webuntis-apis-absences-class-register.md). |
| 16.03.2023 | 30.03.2023 | **New UI integration point in examinations.** Platform applications can now be configured with an entry point from the exam list in WebUntis. |
| 27.02.2023 | 09.03.2023 | **Timetable API v2:** multiple IDs as filter parameter, `period` as filter parameter, additional texts in `PeriodDto`, deprecation of `detailsUrl`, flag for online period, `relatedPeriod` ID for shifted periods, `modified` reacts to student assignment changes. |
| 23.02.2023 | 09.03.2023 | Added support to integrate calendar information in WebUntis. |
| 15.02.2023 | 09.03.2023 | Changed content type for credentials API call from `application/octet-stream` to `application/json`. |
| 15.02.2023 | 09.03.2023 | New parameter `exam_id` for UI integration via lesson details. |
| 14.02.2023 | 09.03.2023 | **New API** for academic session (school year) management. See [Academic Sessions](api-reference-oneroster-apis-academic-sessions.md). |
| 09.02.2023 | 09.03.2023 | Student API: better error message if `className` does not exist. |
| 05.02.2023 | 16.02.2023 | OneRoster API: `person-id` is now returned for users. |
| 06.12.2022 | 06.12.2022 | New YAML specification for the Student Management API. Changes: uniqueness of defined attributes. |
| 21.09.2022 | 06.10.2022 | OneRoster API for users extended with WebUntis-specific metadata: `usergroup` and `userrole`. |
| 05.08.2022 | 10.08.2022 | OneRoster API for classes: extended with from/to dates of the lesson. Lesson status is now correct — `active` for active lessons, `tobedeleted` for old lessons. |
| 06.07.2022 | — | Integration-stage API URL changed to `https://api.integration.webuntis.dev`. |
| 24.06.2022 | — | Integration-stage WebUntis URL changed to `https://tom.integration.webuntis.dev`. |
| 13.06.2022 | 15.06.2022 | **New API** for reading timetable data. See [Timetable Data](api-reference-webuntis-apis-timetable-data.md). |
| 03.06.2022 | — | Documentation about Code Flow changed (`nonce` parameter). |
| 12.05.2022 | 25.05.2022 | **New APIs** for student management (import/export). See [Student Management](api-reference-webuntis-apis-student-management.md). |
| 21.04.2022 | — | Documentation about the credentials API extended. |
| 21.04.2022 | 14.04.2022 | Single logout now works in Firefox. |
| 21.04.2022 | 14.04.2022 | Refresh endpoint now also returns the `id_token`. |
| 21.04.2022 | 14.04.2022 | Bug fix: wrong roles in the JWT. |
| 28.03.2022 | — | Removed `webuntis-loading-check`. |
| 18.03.2022 | — | Documentation change: `clientid` → `client_id`. |
| 11.03.2022 | — | Added example workflows and updated authorization description. |
| 23.02.2022 | 03.03.2022 | Changes within the JWT. **This change is not backwards-compatible.** |
| 07.03.2022 | — | Initial documentation. |
