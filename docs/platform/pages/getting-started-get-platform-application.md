# Get Your Platform Application

> Source: Untis GmbH developer documentation, `developer.untis.com/getting-started/get-platform-application/`.
> Reproduced here as an offline mirror so this repository is self-contained.
> © Untis GmbH; see [`NOTICE.md`](../../../NOTICE.md).

---

Every integration with the Untis Platform starts here. Your platform application is configured by the Untis integration team — this page explains what to expect, what information to prepare, and how the process works.

## Overview

1. **Get in contact** — submit the integration partner contact form. The Untis integration team will reach out to discuss your use case.
2. **Prepare your configuration details** — once in contact, share the information listed below so we can configure your platform application.
3. **Integration-stage setup** — your platform application is configured on the integration environment. You’ll also be added to a dedicated Microsoft Teams channel for ongoing support.
4. **Develop and validate** — build your integration against the integration-stage environment and work with the team to validate your implementation.
5. **Production deployment** — once ready, your application is promoted to production and made available to schools.

---

## Contact us

**[Integration Partner Contact Form](https://www.untis.at/integrationen/kontaktformular-integrationspartner)**

Submit the form to start the process. The integration team will reach out to arrange an initial call and guide you through setup.

## What we need from you

Prepare the following details before or during your initial contact. Not everything is required upfront — the integration team will guide you through what applies to your integration.

- [General](#tab-panel-3482)
- [Webhooks](#tab-panel-3483)
- [UI Integration](#tab-panel-3484)
- [API Integration](#tab-panel-3485)
- [Calendar](#tab-panel-3486)

| Field | Notes |
| --- | --- |
| **Product name** | Max. 64 characters |
| **Company name** | Max. 100 characters |
| **Short description** | Max. 255 characters |
| **Use cases** | What you want to support |
| **Domain** | Publicly accessible domain or pattern, e.g. `www.yourapp.com`. Localhost is not supported. |
| **Restrictions** | Any country, region, or school restrictions |

We strongly recommend providing these endpoints to enable automatic processes. See [Credentials Webhook](integration-guides-webhooks-credentials.md) and [Deactivation Webhook](integration-guides-webhooks-deactivation.md) for full specifications.

| Endpoint | Example | Notes |
| --- | --- | --- |
| **Credential-Path** | `/credentials` | Enables automatic credential transfer on school activation. Without this, admins copy credentials manually. |
| **Deactivation-Path** | `/deactivate` | Notifies your app when it is deactivated or deleted. |
| **SSO-Redirect-Path** | `/login/oauth2/code/{TENANT_ID}` | Required for OIDC Authorization Code flow. |

Note

Credentials must be stored per school. See [Credential Transfer](getting-started-overview.md) in the overview for how this works.

**Menu placement** — where your application appears:

- **Main menu** – visible in the main navigation
- **Lesson details** – accessible from within lesson views
- **Examinations** – accessible from exam-related views

**Paths:**

| Path | Example | Notes |
| --- | --- | --- |
| **Redirect-Path** | `/untis` | Where users land when opening your app from Untis Platform. Must match the OIDC redirect URL if no SSO-Redirect-Path is set. |
| **Logout-Path** | `/logout` | Called when users log out of Untis Platform. |

**Role-based configuration** (optional) — configure different menu entry names, redirect paths, and display modes (new tab vs iFrame) per user role (Admin, Student, Teacher).

**Icon** (recommended) — 24×24px SVG in grey, PNG optional.

**Mobile** (optional) — if you have native mobile apps, provide your universal link and app IDs for Android and iOS. Confirm whether your redirect paths work on mobile.

See [UI Integration](integration-guides-ui-integration.md) for implementation details.

Tell us which data you need access to. We’ll configure the correct read/write permissions for your platform application.

See [API Reference](api-reference-api-overview.md) for the full list of available APIs and [Authorization Model](core-concepts-authorization-model.md) for authentication flows.

If you provide an iCal API, Untis Platform can read your calendar data and display it in the timetable. Provide a **Calendar-Path** endpoint to enable this.

See [Calendar Integration (iCal)](integration-guides-calendar.md) for the specification.

 

## Activation models

Platform applications can use one of three activation models:

Opt-in

Schools must explicitly activate your application and accept data exchange.

Opt-out

Your application is pre-activated for all schools in a region or country,
but schools can deactivate it.

Compulsion

Your application is activated automatically for specific schools and cannot
be removed.

Activation models are configured by Untis based on your agreement and use case.
