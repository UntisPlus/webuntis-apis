# Authorization Model

> Source: Untis GmbH developer documentation, `developer.untis.com/core-concepts/authorization-model/`.
> Reproduced here as an offline mirror so this repository is self-contained.
> © Untis GmbH; see [`NOTICE.md`](../../../NOTICE.md).

---

Once your application is authenticated, authorization controls what it can do — specifically, which Untis Platform APIs it can call, which operations it can perform, and which data it can read or write. This page explains how that access-control model works at a conceptual level. For how to obtain tokens, see [Authentication Model](core-concepts-authentication-model.md).

Scopes & Permissions

Scopes control which APIs and operations your application can access.
Permissions are configured per application during registration.

User & Role Context

Authorization results differ based on whether a user or the application
itself is authenticated, and which role that user holds.

Tenant Isolation

Every school is a separate tenant. Credentials, tokens, and data are fully
isolated — one set of credentials cannot access another school’s data.

---

## Scopes and permissions

Scopes appear in token requests and determine which API families and operations are available to your integration.

|  |  |
| --- | --- |
| **`openid`** | Required for OIDC authentication — always include |
| **`roster-core.readonly`** | Read-only access to OneRoster Core endpoints |
| **Additional scopes** | Map to specific API permissions — see API Reference |

Permissions are configured per platform application during registration in the Platform Application Manager. The full list of configurable permissions (student masterdata, teacher masterdata, timetable, etc.) is managed there — see the API Reference for which permission each endpoint requires.

[Get Your Platform Application](getting-started-get-platform-application.md)  How API permissions are configured during registration.

[API Reference](api-reference-api-overview.md)  API endpoints, data models, and authorization scopes.

---

## User context and role influence

Authorization results depend on the authenticated context:

|  |  |
| --- | --- |
| **Server-to-server** | Application is authenticated via Client Credentials. Permissions are based on the platform application’s configuration only. |
| **User context** | A specific user is authenticated via Authorization Code. Permissions are based on application config AND the user’s role and school membership. |
| **User identity** | Always use the `sub` claim from the token to identify users. Call the OneRoster users endpoint to retrieve user details. |
| **`untis-profile` scope** | Not backwards-compatible — do not use it. Use `sub` + OneRoster API instead. |

[Authentication Model](core-concepts-authentication-model.md)  How tokens are obtained for each context.

---

## Tenant isolation (per-school)

Authorization is tenant-scoped. Every school is a separate tenant and access is strictly isolated.

|  |  |
| --- | --- |
| **Provisioned per tenant** | Each school activation delivers separate credentials for that school only |
| **Tokens are tenant-specific** | A token for school A cannot access data from school B |
| **Store credentials per tenant** | Your application must manage credentials and data independently per school |
| **Tenant metadata** | `country`, `region`, and `language` fields in the credentials transfer payload are informational — not access-control rules |

[Credentials Webhook](integration-guides-webhooks-credentials.md)  Tenant provisioning payload and credential metadata.

---

## Related guides

[Authentication Model](core-concepts-authentication-model.md)  How to obtain tokens and authenticate requests.

[Get Your Platform Application](getting-started-get-platform-application.md)  How permissions are configured during registration.

[API Reference](api-reference-api-overview.md)  Endpoint-specific permission requirements.

[SSO Integration](integration-guides-sso.md)  User authentication implementation.
