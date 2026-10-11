# Untis Platform API documentation (offline mirror)

This directory is an **offline mirror of the official Untis GmbH developer
documentation** (developer.untis.com), converted to Markdown so that everything
you need to integrate with the official Platform and OneRoster APIs lives inside
this repository.

- Every page keeps its original "Source:" line pointing at the canonical URL.
- Content is © Untis GmbH and reproduced for reference; see
  [`../../NOTICE.md`](../../NOTICE.md).
- This is a snapshot. Untis may change the live docs; treat the portal as the
  source of truth for your production integration.

For the short orientation to these APIs, see
[`../10-platform-api.md`](../10-platform-api.md).

## Getting started

| Page | Contents |
|---|---|
| [Overview](pages/getting-started-overview.md) | What the platform is, concepts |
| [Quick start](pages/getting-started-quick-start.md) | First call, step by step |
| [Get your platform application](pages/getting-started-get-platform-application.md) | Requesting credentials |

## Identity & access

| Page | Contents |
|---|---|
| [Authentication model](pages/core-concepts-authentication-model.md) | Client Credentials + OIDC flows |
| [Authorization model](pages/core-concepts-authorization-model.md) | Scopes, permissions, tenant isolation |

## API reference — general

| Page | Contents |
|---|---|
| [API overview & base URLs](pages/api-reference-api-overview.md) | Environments, rate limits, versioning |
| [Common API concepts](pages/api-reference-common-api-concepts.md) | Pagination, sorting, filtering |
| [Error handling](pages/api-reference-error-handling.md) | Error bodies for every family |
| [Which API to choose](pages/api-reference-which-api-to-choose.md) | OneRoster vs. Platform APIs |

## API reference — Untis Platform APIs

| Page | Contents |
|---|---|
| [Platform APIs overview](pages/api-reference-webuntis-apis.md) | Resource families |
| [User management](pages/api-reference-webuntis-apis-user-management.md) | |
| [Student management](pages/api-reference-webuntis-apis-student-management.md) | |
| [Teacher management](pages/api-reference-webuntis-apis-teacher-management.md) | |
| [Legal guardian management](pages/api-reference-webuntis-apis-legal-guardian-management.md) | |
| [Class management](pages/api-reference-webuntis-apis-class-management.md) | |
| [Room management](pages/api-reference-webuntis-apis-room-management.md) | |
| [Subject management](pages/api-reference-webuntis-apis-subject-management.md) | |
| [Teacher absence management](pages/api-reference-webuntis-apis-teacher-absence-management.md) | |
| [Teacher absence reason management](pages/api-reference-webuntis-apis-teacher-absence-reason-management.md) | |
| [Timetable data](pages/api-reference-webuntis-apis-timetable-data.md) | v3 (+ deleted-periods) |
| [Timetable event push](pages/api-reference-webuntis-apis-timetable-event-push.md) | |
| [Absences & class register](pages/api-reference-webuntis-apis-absences-class-register.md) | |
| [Exams](pages/api-reference-webuntis-apis-exams.md) | |
| [Lessons](pages/api-reference-webuntis-apis-lessons.md) | |
| [Messaging](pages/api-reference-webuntis-apis-messaging.md) | |

## API reference — OneRoster

| Page | Contents |
|---|---|
| [OneRoster overview](pages/api-reference-oneroster-apis.md) | |
| [Organizations & schools](pages/api-reference-oneroster-apis-organizations-schools.md) | |
| [Users](pages/api-reference-oneroster-apis-users.md) | |
| [Classes](pages/api-reference-oneroster-apis-classes.md) | |
| [Academic sessions](pages/api-reference-oneroster-apis-academic-sessions.md) | |
| [Enrollments](pages/api-reference-oneroster-apis-enrollments.md) | |

## Integration guides

| Page | Contents |
|---|---|
| [UI integration](pages/integration-guides-ui-integration.md) | |
| [SSO integration](pages/integration-guides-sso.md) | |
| [Webhooks overview](pages/integration-guides-webhooks.md) | |
| [Verifying platform identity](pages/integration-guides-webhooks-verifying-identity.md) | |
| [Credentials webhook](pages/integration-guides-webhooks-credentials.md) | |
| [Deactivation webhook](pages/integration-guides-webhooks-deactivation.md) | |
| [Calendar integration (iCal)](pages/integration-guides-calendar.md) | |
| [Example workflows](pages/integration-guides-example-workflows.md) | |

## Support & community

| Page | Contents |
|---|---|
| [Changelog](pages/support-community-changelog.md) | |
| [FAQ](pages/support-community-faq.md) | |
| [Troubleshooting](pages/support-community-troubleshooting.md) | |
