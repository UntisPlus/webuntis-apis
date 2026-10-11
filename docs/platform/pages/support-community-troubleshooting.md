# Troubleshooting

> Source: Untis GmbH developer documentation, `developer.untis.com/support-community/troubleshooting/`.
> Reproduced here as an offline mirror so this repository is self-contained.
> © Untis GmbH; see [`NOTICE.md`](../../../NOTICE.md).

---

A reference for diagnosing and resolving common integration issues. Each entry describes what you observe, why it happens, and how to fix it.

---

## `invalid_grant` error when obtaining an access token

The token endpoint returns `invalid_grant` when using the Client Credentials flow.

**Cause**

The OIDC client secret and the platform-generated password are not interchangeable. Each credential belongs to a specific flow:

| Flow | Credential to use |
| --- | --- |
| Client Credentials (server-to-server) | Platform-generated **password** sent via the credentials webhook |
| Authorization Code (SSO / user login) | **OIDC client secret** from PAM |

**Resolution**

For the Client Credentials flow, use the **password** delivered to your endpoint via the [Credentials Webhook](integration-guides-webhooks-credentials.md), not the OIDC client secret.

Caution

The OIDC client secret is only valid for the Authorization Code flow. Using it
in a Client Credentials request will always result in `invalid_grant`.

---

## `invalid_client` on the first token request after activation

The very first `client_credentials` token request made right after a school activates the application fails with `401 invalid_client` (“Client authentication failed”). A retry a few seconds later succeeds, and all subsequent token requests work normally.

**Cause**

The credentials delivered via the [Credentials Webhook](integration-guides-webhooks-credentials.md) are only valid once the entire activation process has fully completed on the platform side. If the token endpoint is called immediately after receiving the webhook, activation may not yet be finished, so the credentials are momentarily not yet valid.

**Resolution**

Add a short delay (1-2 seconds is generally sufficient) after receiving the credentials webhook before making the first token request. See the [Activation process - Timing note](integration-guides-webhooks-credentials.md) for details.

Caution

This same timing issue can resurface mid-sync: if a school administrator
deactivates the application while an initial data sync is still running, the
next token refresh will also fail with `401`. Since [token lifetime is only
3 minutes](core-concepts-authentication-model.md), a large initial sync should
proactively refresh the token — with some safety margin — before it expires,
rather than waiting for a request to fail. Advise school administrators to
leave the application active until the initial sync has completed, since a
full sync can take several minutes depending on school size.

---

## User is not redirected back to the application after IServ login

After completing IServ authentication, users land back on WebUntis rather than being returned to the partner application. Restarting the SSO flow after authentication succeeds as expected.

**Cause**

This occurs when a user does not already have an active browser session in WebUntis before the SSO flow begins. The intermediate redirect to an external identity provider (such as IServ) can cause the original redirect state to be lost.

**Status**

This is a **known issue** currently tracked in the Untis backlog. There is no workaround available at this time.

---

## Login URL does not start a new authentication flow

A user opens the application from the Untis Platform dashboard but is authenticated as a different user from a previous browser session.

**Cause**

If a partner application skips the authentication flow when a session already exists, and does not verify that the inbound user matches the active session, a different user account may be active than the one who launched the app.

**Resolution**

Treat every incoming request to your Login URL as the start of a new authentication flow. If your application already has an active session, terminate it and re-initiate the OIDC Authorization Code flow before establishing the new session. This ensures that the user authenticated in your application always matches the user who launched it from the Untis Platform.

Note

This is particularly important in shared-device environments, such as schools
where multiple users may use the same browser on the same device.

---

## OneRoster returns no students, but students exist in masterdata

Querying the OneRoster API returns no students (or an empty result), even though the school has students in WebUntis.

**Cause**

The OneRoster API is **user-account-centric**. It only returns persons who have an active user account in the system. Students who exist in the masterdata but have no user account are not exposed through OneRoster.

**Resolution**

If you need to access students who do not have user accounts, use the [Student Management API](api-reference-webuntis-apis-student-management.md), which operates on masterdata rather than user accounts.

---

## `students/{id}` returns no result

Calling `students/{id}` returns no result for an ID that is known to exist.

**Cause**

The `{id}` path parameter resolves against the `externalKey` field — the identifier used by upstream school management software — not the internal Untis record ID. The `externalKey` is not always populated; it is set when data originates from an external source but may be absent for records created directly in WebUntis.

**Resolution**

To retrieve a student by their internal Untis ID, use the `filter` query parameter instead:

```
GET /WebUntis/api/rest/extern/v3/students?filter=id='1'
```

This targets the internal `id` field directly and works regardless of whether an `externalKey` is set.

---

## Updating a class by `shortName` fails when the school year has ended

`PUT` requests to the [Class Management API](api-reference-webuntis-apis-class-management.md) fail with a `VALIDATION_ERROR` when updating a class that does not belong to the current school year, but only if `shortName` is included in the request:

```
{
  "errorCode": "VALIDATION_ERROR",
  "requestId": "3dfe0d74-7a5a-463f-bb15-53cca9ee565d",
  "traceId": "",
  "validationErrors": [
    {
      "errorKey": "entity.notFound",
      "path": "classes[0].id",
      "errorMessage": "Class with id [75] does not exists.",
      "index": 0
    }
  ]
}
```

**Cause**

Classes are identified hierarchically by `id`, `externKey`, and `shortName`, in that order. `shortName` is only unique **within an active school year** — once a school year ends and no new school year has been activated yet, there is no active school year to resolve `shortName` against, so lookup by `shortName` fails.

`id` and `externKey` are not affected, since both are globally unique regardless of school year.

**Resolution**

When updating classes that may not belong to the current school year (for example, right after a school year has ended), identify the class using `id` or `externKey` only, and omit `shortName` from the request.

Note

Once a new school year is activated, `shortName` resolves normally again,
including for classes carried over from a prior school year.
