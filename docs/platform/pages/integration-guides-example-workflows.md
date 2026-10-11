# Example Workflows

> Source: Untis GmbH developer documentation, `developer.untis.com/integration-guides/example-workflows/`.
> Reproduced here as an offline mirror so this repository is self-contained.
> © Untis GmbH; see [`NOTICE.md`](../../../NOTICE.md).

---

Common end-to-end integration scenarios using the Untis Platform building blocks. Read the diagram for your integration type, then follow the links to the relevant reference pages.

## SSO for UI-Integration

A school user launches the partner app from a Untis Platform UI entry point. Untis Platform passes context via the launch URL; the partner app uses the SSO Authorization Code flow to authenticate the user.

```
sequenceDiagram
    autonumber
    participant User
    participant WU as Untis Platform
    participant PA as Partner App

    User->>WU: Active session
    User->>WU: Click entry point
    WU->>PA: Launch URL + context params

    PA->>WU: GET /WebUntis/api/sso/v3/{tenantId}/authorize
    WU-->>PA: Redirect with ?code=...
    PA->>WU: POST /WebUntis/api/sso/v3/{tenantId}/token
    WU-->>PA: id_token + access_token

    PA->>User: Partner app content
```

**Read more:** [UI Integration](integration-guides-ui-integration.md) · [SSO](integration-guides-sso.md) · [Authorization Model](core-concepts-authorization-model.md)

---

## API Integration

A server-side application uses Client Credentials to obtain a token for a specific tenant, then calls the Untis Platform APIs directly — no UI or user session involved.

```
sequenceDiagram
    autonumber
    participant PA as Partner Server
    participant WU as Untis Platform

    PA->>WU: POST /WebUntis/api/sso/v3/{tenantId}/token (client_credentials)
    WU-->>PA: access_token (valid 3 min)

    PA->>WU: GET /WebUntis/api/rest/extern/v{n}/{resource} (Bearer token)
    WU-->>PA: Response data
```

**Read more:** [Authorization Model](core-concepts-authorization-model.md) · [Authentication Model](core-concepts-authentication-model.md)

---

## Activating the Platform App / Onboarding a New School

Three scenarios depending on how credentials are delivered and whether manual steps are required.

### Scenario 1 — All automatically

The school administrator activates the app; the platform delivers credentials via webhook immediately with no manual intervention.

```
sequenceDiagram
    autonumber
    participant Admin as School Admin
    participant UP as Untis Platform
    participant PA as Partner App

    Admin->>UP: Activate app in appstore
    UP->>PA: POST credentials webhook (signed)
    PA->>PA: Verify + store credentials
    PA-->>UP: 200 OK
```

### Scenario 2 — Additional information needed

Credentials are delivered via webhook, but the partner app requires the school administrator to provide additional configuration before the school is fully active.

```
sequenceDiagram
    autonumber
    participant Admin as School Admin
    participant UP as Untis Platform
    participant PA as Partner App

    Admin->>UP: Activate app in appstore
    UP->>PA: POST credentials webhook (signed)
    PA->>PA: Verify + store credentials
    PA-->>UP: 200 OK

    PA->>Admin: Request additional info
    Admin->>PA: Provide configuration

    PA->>PA: Complete school setup
```

### Scenario 3 — Manual configuration needed

No webhook is received; the school administrator manually copies credentials from the platform into the partner app’s configuration UI.

```
sequenceDiagram
    autonumber
    participant Admin as School Admin
    participant UP as Untis Platform
    participant PA as Partner App

    Admin->>UP: Activate app in appstore
    Note over PA: No webhook received

    Admin->>UP: Copy credentials manually
    Admin->>PA: Enter credentials in config UI

    PA->>PA: Store credentials
```

**Note:** Scenario 3 is a fallback. Implementing a [credentials webhook endpoint](integration-guides-webhooks-credentials.md) covers Scenarios 1 and 2 automatically.

**Read more:** [Get Your Platform Application](getting-started-get-platform-application.md) · [Credentials Webhook](integration-guides-webhooks-credentials.md) · [Deactivation Webhook](integration-guides-webhooks-deactivation.md)
