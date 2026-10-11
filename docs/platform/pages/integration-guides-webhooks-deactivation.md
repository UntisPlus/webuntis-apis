# Deactivation Webhook

> Source: Untis GmbH developer documentation, `developer.untis.com/integration-guides/webhooks/deactivation/`.
> Reproduced here as an offline mirror so this repository is self-contained.
> © Untis GmbH; see [`NOTICE.md`](../../../NOTICE.md).

---

When a school deactivates or deletes your platform application, the Untis Platform sends a deactivation webhook to your configured endpoint. This notifies your application that access has been revoked for that tenant and that you should no longer use the associated credentials.

## When this webhook is sent

The `eventType` field indicates whether the application was deactivated or fully deleted, and the `reasonType` field provides the reason.

| eventType | Meaning |
| --- | --- |
| `DEACTIVATION` | The application was deactivated, but not deleted |
| `DELETION` | The application was permanently deleted |

| reasonType | Meaning |
| --- | --- |
| `NO_REASON` | No reason known |
| `SCHOOL_DEACTIVATION` | The entire Untis Platform school was deactivated |
| `SCHOOL_DELETION` | The entire Untis Platform school was deleted |
| `REMOTE_DEACTIVATION` | The application was deactivated by a remote service (also used when a licence expires) |
| `REMOTE_DELETION` | The application was deleted by a remote service |

## Endpoint requirements

All webhook endpoints share the same technical requirements — HTTPS, `POST`, `2xx` acknowledgement, and signature verification. See [Credentials Webhook](integration-guides-webhooks-credentials.md) for the full list.

The endpoint URL is configured in PAM when your platform application is set up. It can be the same endpoint as the credentials webhook or a separate one.

## Payload

The payload is a JSON object identifying the affected tenant and the reason for deactivation.

| Field | Type | Description |
| --- | --- | --- |
| `tenantId` | string | Unique identifier for the school/tenant that deactivated your application |
| `eventType` | string | `DEACTIVATION` or `DELETION` — see table above |
| `reasonType` | string | One of the `reasonType` values above |
| `reasonText` | string | Human-readable description of the reason, if provided |

**Example payload:**

```
{
  "tenantId": "12345",
  "eventType": "DEACTIVATION",
  "reasonType": "NO_REASON",
  "reasonText": "The tenant requested deactivation."
}
```

## Handling requirements

### 1. Verify the signature first

Always verify the request signature before acting on the payload. See [Verifying the Untis Platform Identity](integration-guides-webhooks-verifying-identity.md).

### 2. Immediately stop using the credentials

Once you receive a deactivation event for a tenant, the associated credentials are no longer valid. Mark the tenant as deactivated in your system immediately — any API calls using the revoked credentials will fail.

### 3. Decide how to handle tenant data

The Untis Platform does not prescribe what to do with tenant data. You have two main options:

Option A — Delete immediately

Remove all tenant-specific data (credentials, synced records, user
associations) as soon as the event is received. Use this if your application
has no need to retain historical data or if your data processing agreement
requires immediate deletion.

Option B — Mark as deactivated

Retain the data but flag the tenant as inactive. This preserves historical
records (e.g. past syncs, audit logs) and allows graceful re-activation if
the school reconnects. Deactivated tenants must not trigger new API calls.

Choose based on your data processing agreements, legal requirements, and product needs.

### 4. Respond `2xx` promptly

Return a success response quickly, even if your data cleanup runs asynchronously. A slow or failed response may cause the Untis Platform to retry delivery.

### 5. Handle duplicate delivery gracefully

Your handler must be **idempotent** — processing the same deactivation event twice must produce the same result as processing it once. An already-deactivated tenant must remain deactivated with no errors thrown.

## Re-activation

If a school reactivates your platform application, a new [Credentials Webhook](integration-guides-webhooks-credentials.md) will be delivered with an `eventType` of `REACTIVATED` and fresh credentials. Treat this as a new activation — store the new credentials and restore the tenant’s active status in your system.

## Relevant articles

[Verifying the Untis Platform Identity](integration-guides-webhooks-verifying-identity.md)  How to verify the request signature.

[Credentials Webhook](integration-guides-webhooks-credentials.md)  Credentials transfer on activation and re-activation.

[Authentication Model](core-concepts-authentication-model.md)  Conceptual overview of platform credentials.

[Get Your Platform Application](getting-started-get-platform-application.md)  Configure your webhook endpoint.
