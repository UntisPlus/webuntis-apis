# Integration Webhooks

> Source: Untis GmbH developer documentation, `developer.untis.com/integration-guides/webhooks/`.
> Reproduced here as an offline mirror so this repository is self-contained.
> © Untis GmbH; see [`NOTICE.md`](../../../NOTICE.md).

---

## What integration webhooks are

Integration webhooks are **platform-initiated HTTP callbacks** — the Untis Platform calls endpoints you provide, rather than the other way round. Each webhook has a fixed purpose in the integration lifecycle:

- **Credentials transfer** — the platform sends your application the credentials it needs to authenticate on behalf of a school.
- **Deactivation** — the platform notifies your application that a school’s access has been revoked.

Events and webhooks

In the Untis Platform context, **event** and **webhook** are often used
interchangeably — for example, “deactivation event” and “deactivation webhook”
refer to the same thing. **Webhook** emphasises the HTTP delivery mechanism (a
signed POST request to your endpoint), while **event** emphasises what
triggered it (something happening in the integration lifecycle, such as a
school deactivating your app).

Webhooks are not OAuth-authenticated. They are covered by this section, not by the [Authentication](core-concepts-authentication-model.md) or [Authorization](core-concepts-authorization-model.md) documentation, which cover token-based flows your application initiates.

## Common request flow

Every inbound platform request follows the same three-step pattern:

1. **Receive** — the Untis Platform sends an HTTPS `POST` request to your configured endpoint with a JSON body and signature headers.
2. **Verify** — you check the request signature against the public key to confirm the request genuinely came from the Untis Platform. This is a **hard requirement** — never skip it.
3. **Handle** — once the signature is valid, you process the payload according to the specific webhook’s documented purpose and return a `2xx` response.

## Security requirements

All platform-initiated requests are **signed with an RSA private key** held by the Untis Platform. Your application must verify the signature using the published public key before trusting any payload data.

- Every request carries two headers: `Authorization` (the base64-encoded RSA signature) and `Algorithm` (the algorithm used, e.g. `SHA256withRSA`).
- Signature verification is a prerequisite for all webhook handlers — credentials transfer and deactivation alike.
- How to verify is fully documented in [Verifying the Untis Platform Identity](integration-guides-webhooks-verifying-identity.md).

## Available webhook types

| Webhook | Your endpoint role | Purpose |
| --- | --- | --- |
| [Credentials transfer](integration-guides-webhooks-credentials.md) | Receiver | Receive credentials when a school activates your app |
| [Deactivation](integration-guides-webhooks-deactivation.md) | Receiver | Receive notification when a school deactivates or deletes your app |

Endpoint URLs for credentials transfer and deactivation are configured in your platform application setup in PAM. See [Get Your Platform Application](getting-started-get-platform-application.md) for details.

## Relevant articles

[Verifying the Untis Platform Identity](integration-guides-webhooks-verifying-identity.md)  How to verify signed requests from the Untis Platform.

[Credentials Webhook](integration-guides-webhooks-credentials.md)  Credentials transfer payload and handling.

[Deactivation Webhook](integration-guides-webhooks-deactivation.md)  Deactivation event payload and handling.
