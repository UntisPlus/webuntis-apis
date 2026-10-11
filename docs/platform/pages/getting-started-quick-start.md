# Quick Start

> Source: Untis GmbH developer documentation, `developer.untis.com/getting-started/quick-start/`.
> Reproduced here as an offline mirror so this repository is self-contained.
> © Untis GmbH; see [`NOTICE.md`](../../../NOTICE.md).

---

Get your integration working as fast as possible. This page walks you through what you need, how to choose your integration path, and where to start.

## Before you begin

Understand the platform

Not sure how the Untis Platform works or what a platform application is? Start with the overview.

[Platform Overview](getting-started-overview.md)

Request a platform application

Every integration starts with a platform application. Contact Untis to have yours configured in the platform application manager (PAM).

[Get Your Platform Application](getting-started-get-platform-application.md)

Choose the right APIs

If you plan to exchange data, review which APIs are available and which one fits your use case.

[Which API to Choose](api-reference-which-api-to-choose.md)

Review core concepts

Authentication flows, authorization model, and tenant isolation — read this before you implement.

[Core Concepts](core-concepts-authentication-model.md)

## What you can build

The Untis Platform provides three building blocks — UI Integration, Single Sign-On, and API Integration — that you can combine freely. See the [Platform Overview](getting-started-overview.md) for descriptions of each.

## Choose your integration path

UI + API + SSO ★ Recommended

Your app is embedded in the Untis Platform, users sign in automatically via SSO, and data flows between systems via API. The most complete integration pattern.

[Get Platform Application](getting-started-get-platform-application.md) · [UI Integration](integration-guides-ui-integration.md) · [SSO](integration-guides-sso.md) · [API Reference](api-reference-api-overview.md)

UI + SSO

Your app is embedded in the Untis Platform and users sign in automatically — no data exchange via API. The Untis Platform acts as the identity provider even if users originally authenticated via an external IdP.

[Get Platform Application](getting-started-get-platform-application.md) · [UI Integration](integration-guides-ui-integration.md) · [SSO](integration-guides-sso.md)

API-only

Server-to-server data exchange. No UI integration, no SSO. Best for data pipelines, rostering, and backend synchronization.

[Get Platform Application](getting-started-get-platform-application.md) · [Authentication Model](core-concepts-authentication-model.md) · [API Reference](api-reference-api-overview.md)

UI-only

Your web app is embedded in the Untis Platform with no SSO or data exchange. Rarely successful — only use this when SSO is genuinely not possible (e.g. a public website with no user accounts).

[Get Platform Application](getting-started-get-platform-application.md) · [UI Integration](integration-guides-ui-integration.md)

## Stay informed

Tip

**Subscribe to the RSS feed** to get notified whenever the changelog is
updated with new API changes, features, or deprecations. Point your RSS reader
or CI pipeline to:

`https://developer.untis.com/rss.xml`

If your team does not have an RSS reader, consider services such as
[Feedly](https://feedly.com), [Inoreader](https://www.inoreader.com), or a
Slack RSS integration to receive updates directly in your workflow.
