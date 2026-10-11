# Credentials Webhook

> Source: Untis GmbH developer documentation, `developer.untis.com/integration-guides/webhooks/credentials/`.
> Reproduced here as an offline mirror so this repository is self-contained.
> © Untis GmbH; see [`NOTICE.md`](../../../NOTICE.md).

---

When a school administrator activates your platform application, the Untis Platform sends a credentials transfer webhook to your configured endpoint. This webhook delivers everything your application needs to authenticate against the Untis Platform APIs on behalf of that school.

Credential transfer via webhook is the **recommended** approach. The alternative — manual entry by the school administrator — is error-prone and does not scale.

## When this webhook is sent

| eventType | Trigger |
| --- | --- |
| `CREATED` | A school administrator activates your application for the first time |
| `REACTIVATED` | An application that was previously deactivated is re-activated by the school |
| `RESET` | A password reset was triggered on the platform — new credentials are issued |

## Endpoint requirements

Your credentials webhook endpoint must:

- Be reachable via HTTPS
- Accept `POST` requests with `Content-Type: application/json`
- Return a `2xx` response to acknowledge receipt
- Verify the request signature before processing — see Step 1 in [Handling requirements](#handling-requirements) below

The endpoint URL is configured in PAM when your platform application is set up.

## Payload

The payload is a JSON object containing credentials and metadata for the activated tenant (Credentials API specification v2).

| Field | Type | Nullable\* | Description |
| --- | --- | --- | --- |
| `tenantId` | string | No | Unique identifier for the school/tenant |
| `clientId` | string | No | The OIDC client ID. Used as the `client_id` parameter in auth requests and as the Basic Auth username for Client Credentials token requests |
| `secret` | string | No | The OIDC client secret. Used as `client_secret` in the Authorization Code token exchange |
| `password` | string | No | The platform-generated password. Used as the Basic Auth password for Client Credentials token requests (not the OIDC secret) |
| `host` | string | No | The Untis Platform host for this school (e.g. `localhost`, or the school’s assigned subdomain) |
| `country` | string | Yes | Country of the school (e.g. `AT`, `DE`) |
| `region` | string | Yes | Region/state of the school (e.g. `AT-3`) |
| `language` | string | No | Primary language of the school (e.g. `de`) |
| `eventType` | string | No | The reason for this delivery: `CREATED`, `REACTIVATED`, or `RESET` |
| `activatorEmail` | string | Yes | Email address of the school administrator who activated the application |
| `activatorUsername` | string | No | Username of the school administrator who activated the application |
| `schoolEmail` | string | Yes | Contact email address of the school |
| `schoolPhoneNumber` | string | Yes | Contact phone number of the school |

\* In Untis Platform, not all fields are mandatory. If a field has no content, `null` is sent instead of omitting the field.

Attribute order and signature verification

The signature is computed over the raw JSON body bytes. The fields must be read and verified in the order they arrive — do not re-serialise the payload before verifying.

**Example payload:**

- [v2 (Current)](#tab-panel-3495)
- [v1 (Deprecated)](#tab-panel-3496)

```
{
  "tenantId": "12345",
  "clientId": "BestApp-tenant-12345",
  "secret": "test-secret",
  "password": "test-password",
  "host": "localhost",
  "country": "AT",
  "region": "AT-3",
  "language": "de",
  "eventType": "CREATED",
  "activatorEmail": "jane@doe.com",
  "activatorUsername": "Jane Doe",
  "schoolEmail": "school@entenhausen.com",
  "schoolPhoneNumber": "555 / 123 456 789"
}
```

Migrate to v2

v1 included a `schoolName` field and did not include `eventType`, `activatorEmail`, `activatorUsername`, `schoolEmail`, or `schoolPhoneNumber`. `schoolName` has been removed and is no longer delivered.

```
{
  "tenantId": "12345",
  "clientId": "BestApp-tenant-12345",
  "secret": "test-secret",
  "password": "test-password",
  "host": "localhost",
  "country": "AT",
  "region": "AT-3",
  "language": "de",
  "schoolName": "Example School"
}
```

 

## Handling requirements

1. **Verify the signature first** — before reading any field. See [Verifying the Untis Platform Identity](integration-guides-webhooks-verifying-identity.md).
2. **Store credentials per tenant** — use `tenantId` as the key. Never share credentials across tenants. Every school activation delivers a separate set of credentials.
3. **Store securely** — use a secrets manager or encrypted storage. Never log or store credentials in plain text.
4. **Overwrite on redelivery** — for `REACTIVATED` and `RESET` events, overwrite the stored credentials for the matching `tenantId` with the newly delivered values. The previous credentials are no longer valid.
5. **Respond `2xx` promptly** — acknowledge receipt quickly. Perform storage asynchronously if necessary to avoid timeout retries from the platform.
6. **Use metadata for routing** — `country`, `region`, and `language` are informational. Use them for routing requests to regional infrastructure or for localisation if your application requires it.

Activation process - Timing

The credentials will only be valid once the entire activation process has been successfully completed. This includes successful confirmation of your credentials endpoint.
This means you can only use the credentials once your endpoint has returned a successful status.
Ideally, you should also wait for another 1 to 2 seconds to be absolutely sure.

## What to do if the webhook is not received

If your endpoint was temporarily unavailable, the school administrator can re-trigger delivery or manually copy the credentials into your application’s UI. Build a manual credential entry fallback for resilience, even if webhook delivery is your primary path.

## Relevant articles

[Verifying the Untis Platform Identity](integration-guides-webhooks-verifying-identity.md)  How to verify the request signature.

[Deactivation Webhook](integration-guides-webhooks-deactivation.md)  Handling when a school deactivates.

[Authentication Model](core-concepts-authentication-model.md)  Conceptual overview of platform credentials.

[Get Your Platform Application](getting-started-get-platform-application.md)  Configure your webhook endpoint.
