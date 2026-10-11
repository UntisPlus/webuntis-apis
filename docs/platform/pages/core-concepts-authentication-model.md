# Authentication Model

> Source: Untis GmbH developer documentation, `developer.untis.com/core-concepts/authentication-model/`.
> Reproduced here as an offline mirror so this repository is self-contained.
> © Untis GmbH; see [`NOTICE.md`](../../../NOTICE.md).

---

Authentication in the Untis Platform covers three distinct concerns depending on who is making the request.

User

Identifying an end user in UI/SSO scenarios — who is this person?

Application

Identifying your backend for server-to-server API access — which application
is making this request?

Request

Verifying that an incoming webhook actually came from Untis Platform — is
this request legitimate?

What a token allows you to access (scopes and permissions) is a separate concern — see [Authorization Model](core-concepts-authorization-model.md).

---

## User authentication — OIDC Authorization Code

User sign-in uses **OpenID Connect Authorization Code flow**. For platform applications, Untis Platform acts as the identity provider — users authenticate with Untis Platform and your app receives tokens to establish a session.

### PKCE for Public Clients

The Untis Platform supports **Proof Key for Code Exchange (PKCE)** for public clients (e.g., mobile apps) and as an additional security layer for confidential clients.

|  |  |
| --- | --- |
| **Flow** | OIDC Authorization Code (with PKCE support) |
| **Authorize endpoint** | v3 authorize endpoint |
| **Token endpoint** | v3 token endpoint |
| **API version** | v3 only — earlier endpoints not supported |

[SSO Integration guide](integration-guides-sso.md)  Redirect URI rules, well-known configuration, token endpoint requirements, and parameter handling.

### Federation to a school’s third-party IdP

A school (tenant) can configure its own third-party identity provider in WebUntis instead of having users authenticate directly against Untis Platform with a username and password. **O365**, **LDAP**, **SAML** and **OpenID Connect (OIDC)** are supported.

This is configured per-tenant in WebUntis under Administration → Integration, and is independent of your application’s own OIDC integration — it does not change the flow described above. Untis Platform remains the identity provider your app talks to; when a tenant has a third-party IdP configured, Untis Platform redirects the user onward to that IdP during the login step, then continues the OIDC Authorization Code flow once the user returns authenticated. From your app’s perspective, no additional handling is required.

[Integrationseinstellungen in WebUntis (Help Center)](https://help.untis.at/hc/de/sections/360004357219--Integrationseinstellungen-in-WebUntis)  School-admin documentation for configuring SAML/OIDC third-party identity providers in WebUntis.

---

## Application authentication — Client Credentials

Server-to-server integrations obtain access tokens using the **OAuth Client Credentials grant**.

|  |  |
| --- | --- |
| **Flow** | OAuth Client Credentials |
| **Token endpoint** | v3 token endpoint with `grant_type=client_credentials` |
| **Auth method** | Basic Auth — username = OIDC client ID, password = platform-generated password (not the OIDC client secret) |
| **Token lifetime** | Short-lived (3 minutes) — use `expires_in` and cache tokens |

[API Reference](api-reference-api-overview.md)  API endpoints, data models, and authorization scopes.

### Java example

The `OneRosterClient` handles token acquisition via the Client Credentials grant internally. Construct it with the tenant ID, client ID, and platform-generated password — the token is fetched and applied automatically.

```
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestClient;
import java.nio.charset.StandardCharsets;
import java.util.Base64;
import java.util.Map;

public class OneRosterClient {

    private static final String API_URL = "https://api.integration.webuntis.dev";

    private final RestClient http;

    public OneRosterClient(String tenantId, String clientId, String password) {
        String accessToken = fetchAccessToken(tenantId, clientId, password);
        this.http = RestClient.builder()
                .baseUrl(API_URL)
                .defaultHeader(HttpHeaders.AUTHORIZATION, "Bearer " + accessToken)
                .defaultHeader(HttpHeaders.ACCEPT, MediaType.APPLICATION_JSON_VALUE)
                .build();
    }

    private String fetchAccessToken(String tenantId, String clientId, String password) {
        String credentials = Base64.getEncoder()
                .encodeToString((clientId + ":" + password).getBytes(StandardCharsets.UTF_8));

        MultiValueMap<String, String> form = new LinkedMultiValueMap<>();
        form.add("grant_type", "client_credentials");

        Map<String, Object> response = RestClient.create().post()
                .uri(API_URL + "/WebUntis/api/sso/v3/" + tenantId + "/token")
                .header(HttpHeaders.AUTHORIZATION, "Basic " + credentials)
                .header(HttpHeaders.CONTENT_TYPE,
                        MediaType.APPLICATION_FORM_URLENCODED_VALUE)
                .body(form)
                .retrieve()
                .body(Map.class);

        if (response == null || !(response.get("access_token") instanceof String token)) {
            throw new IllegalStateException("Token endpoint did not return an access_token");
        }
        return token;
    }
}
```

Caution

Use the **platform-generated password** (not the OIDC client secret) as the credential. Tokens are valid for **3 minutes** — check `expires_in` in the response and cache the token to avoid unnecessary requests.

---

## Request authentication — RSA signature

When Untis Platform calls your endpoints (webhooks), requests are authenticated via **RSA request signing** — not OAuth tokens. Your endpoint must verify the signature on every incoming request.

|  |  |
| --- | --- |
| **Method** | RSA request signing |
| **Direction** | Untis Platform → Your App |
| **Required action** | Verify signature before processing any webhook payload |

[Verifying Untis Platform Identity](integration-guides-webhooks-verifying-identity.md)  Signature verification, canonicalization rules, and key handling.

---

## Related guides

[Authorization Model](core-concepts-authorization-model.md)  Scopes, permissions, and tenant boundaries.

[SSO Integration](integration-guides-sso.md)  Step-by-step OIDC implementation guide.

[Verifying Untis Platform Identity](integration-guides-webhooks-verifying-identity.md)  RSA signature verification for incoming webhooks.

[API Reference](api-reference-api-overview.md)  API endpoints and data models.
