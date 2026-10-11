# SSO Integration

> Source: Untis GmbH developer documentation, `developer.untis.com/integration-guides/sso/`.
> Reproduced here as an offline mirror so this repository is self-contained.
> © Untis GmbH; see [`NOTICE.md`](../../../NOTICE.md).

---

SSO integration provides a “one login” experience: when a user opens your application from within the Untis Platform, they are authenticated automatically — no separate login screen in your app is required. The Untis Platform acts as the identity provider and your application receives a token identifying the user.

SSO is always used together with [UI Integration](integration-guides-ui-integration.md). UI integration defines the entry point (where your app is launched from); SSO handles authentication when the user arrives.

Note

Only v3 of the auth endpoints is supported. v1 and v2 are deprecated and have been shut down.

## When SSO is required

Use SSO when your application needs to know **who the user is** — i.e., when the integration is user-context. This covers the typical UI integration scenario: a teacher or student clicks your app in the Untis Platform and your application needs to identify them, load their data, or personalize the experience.

If your integration is server-to-server only (no user-facing UI launched from within the platform), SSO is not needed. Use the [Client Credentials flow](core-concepts-authentication-model.md) instead.

## Identity roles

Untis Platform as IdP

**This guide covers this scenario.** The Untis Platform authenticates the
user and issues tokens to your application. Used when your UI is integrated
via the platform.

Untis Platform as SP

The Untis Platform accepts sign-ins from an external identity provider —
your app is the IdP. Configured separately by school administrators.

## High-level authentication flow (Authorization Code)

The SSO flow follows the **OpenID Connect Authorization Code grant**. At a high level:

1. **Redirect to authorize** — when the user opens your app from within the Untis Platform, your app redirects the user’s browser to the Untis Platform authorize endpoint
2. **User is authenticated** — the Untis Platform confirms the user’s active session (the user is already logged in to the Untis Platform)
3. **Return with code** — the Untis Platform redirects back to your configured redirect URI with a short-lived authorization code
4. **Exchange code for tokens** — your backend exchanges the code at the token endpoint and receives an ID token and access token
5. **Establish user session** — your application reads the `sub` claim from the ID token to identify the user and establishes its own session

```
sequenceDiagram
    autonumber
    participant User
    participant PA as Partner App
    participant WU as Untis Platform

    User->>PA: Opens app from within Untis Platform
    PA->>WU: GET /v3/{tenantId}/authorize
    WU-->>PA: 302 redirect with ?code=...
    PA->>WU: POST /v3/{tenantId}/token
    WU-->>PA: id_token + access_token
    PA-->>User: Authenticated app content
```

### Step 1 – Call the authorize endpoint

```
GET {API_URL}/WebUntis/api/sso/v3/{tenantId}/authorize
  ?response_type=code
  &scope=roster-core.readonly openid
  &client_id={OIDC_CLIENT_ID}
  &redirect_uri={YOUR_REDIRECT_URI}
  &nonce={NONCE}
```

**Example:**

```
GET https://api.integration.webuntis.dev/WebUntis/api/sso/v3/1234/authorize?response_type=code&scope=roster-core.readonly%20openid&client_id=BestApp&redirect_uri=bestapp.example.domain.at/redirect&nonce=1234
```

**Important:**

- If there is no active Untis Platform session, the user is redirected to the Untis Platform login page. After entering the correct credentials, the user is redirected back to your application automatically
- Normally if there is an active Untis Platform session, the user is redirected to the platform-application with an authorization code. This behavior can be changed by passing `prompt=login` as a URL query parameter, which forces a logout of the current user and redirects the user to the Untis Platform login page.
- `redirect_uri` must exactly match the domain and SSO redirect path configured for your platform application in PAM — a mismatch results in an `invalid_resource` error
- Do not include the `untis-profile` scope. It is not backwards-compatible; changes to it may require development effort on your side. Use only `sub` from the token and call the [OneRoster users endpoint](api-reference-oneroster-apis-users.md) to retrieve user details
- Generate a unique `nonce` per request to prevent replay attacks

### Step 2 – Exchange the code for tokens

```
POST {API_URL}/WebUntis/api/sso/v3/{tenantId}/token
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code
&code={AUTHORIZATION_CODE}
&redirect_uri={YOUR_REDIRECT_URI}
&client_id={OIDC_CLIENT_ID}
&client_secret={OIDC_CLIENT_SECRET}
```

**Example:**

```
curl -X POST "https://api.integration.webuntis.dev/WebUntis/api/sso/v3/1234/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "code=HmToMB_iITpHLucs8RvrL8pEi6iizoKKK7_W8lJSi0k" \
  -d "redirect_uri=bestapp.example.domain.at/redirect" \
  -d "client_id=BestApp" \
  -d "client_secret=Rd5kweLWyww9TYPjjrrvCq3MnCnzezuUs"
```

**Important:**

- The request header must include `Content-Type: application/x-www-form-urlencoded`
- For the Authorization Code flow, use the **OIDC client secret** — not the platform-generated password (the password is only used for the Client Credentials flow)
- The response JWT contains the `sub` claim identifying the user

### PKCE support for OAuth Public Clients

PKCE (Proof Key for Code Exchange) is an extension to the Authorization Code flow that protects public clients (apps that cannot keep a client secret) against authorization code interception. Use PKCE when implementing the SSO flow from:

- Native/mobile apps and desktop apps (public clients)
- Browser-based apps without a secure backend (SPA) acting as a public client

Confidential clients (apps with a secure backend that can keep a client secret) continue to send the client secret. They MAY additionally use PKCE for defense-in-depth.

#### How PKCE works (summary)

1. Your app generates a high-entropy `code_verifier` (43–128 URL-safe chars).
2. Derive `code_challenge = BASE64URL(SHA-256(code_verifier))`.
3. Add `code_challenge` and `code_challenge_method=S256` to the authorize request.
4. When exchanging the code at the token endpoint, include the original `code_verifier`.
5. The Untis Platform validates that the `code_verifier` matches the earlier `code_challenge` before issuing tokens.

#### Authorize request (with PKCE)

```
GET {API_URL}/WebUntis/api/sso/v3/{tenantId}/authorize
  ?response_type=code
  &scope=roster-core.readonly openid
  &client_id={OIDC_CLIENT_ID}
  &redirect_uri={YOUR_REDIRECT_URI}
  &nonce={NONCE}
  &code_challenge={CODE_CHALLENGE}
  &code_challenge_method=S256
```

**Important:**

- Always use `S256` as the `code_challenge_method`.
- Generate a new `code_verifier` (and corresponding `code_challenge`) per request and store the `code_verifier` in a secure client session tied to the user.

#### Token request (public client)

The original `code_verifier` is sent in the token request.

```
POST {API_URL}/WebUntis/api/sso/v3/{tenantId}/token
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code
&code={AUTHORIZATION_CODE}
&redirect_uri={YOUR_REDIRECT_URI}
&client_id={OIDC_CLIENT_ID}
&code_verifier={CODE_VERIFIER}
```

#### Example authorize URL fragment with PKCE

```
.../authorize?response_type=code&scope=roster-core.readonly%20openid
  &client_id=BestApp
  &redirect_uri=bestapp.example.domain.at/redirect
  &nonce=1234
  &code_challenge=e6W7c4bq1y8b1pJ0s3yRrtkZ0q4c8JfXy3q0r2bqkCw
  &code_challenge_method=S256
```

#### Error handling

- Missing/invalid `code_verifier` at the token endpoint results in `invalid_grant`.
- For public clients, omitting PKCE in the authorize request results in `invalid_request`.

Caution

- Treat `code_verifier` as sensitive data. Do not log it and do not persist it longer than necessary.

Note

You can discover PKCE capabilities for a tenant using the well-known configuration’s `code_challenge_methods_supported` field. See [Discovering endpoint URLs (well-known configuration)](#discovering-endpoint-urls-well-known-configuration).

## Configuration dependencies

SSO relies on your platform application being correctly configured in PAM. A mismatch in any of these will cause the authorize endpoint to return an error.

OIDC client ID

Used as `client_id` in both the authorize and token requests.

OIDC client secret

Used as `client_secret` in the token request (Authorization Code flow only).

SSO redirect path

The path the Untis Platform redirects back to after authentication. Must
exactly match the `redirect_uri` in your authorize request.

Domain

Your application’s domain must be registered in PAM. A domain mismatch
causes an `invalid_resource` error.

See [Get Your Platform Application](getting-started-get-platform-application.md) for how these are configured during registration.

## Discovering endpoint URLs (well-known configuration)

The Untis Platform exposes an OpenID Connect discovery endpoint that returns all endpoint URLs and supported configuration values for a given tenant:

```
GET {API_URL}/WebUntis/api/sso/v3/{tenantId}/.well-known/openid-configuration
```

Use this to programmatically resolve the authorize and token endpoint URLs rather than hardcoding them.

## Token contexts: user vs. service

There are two distinct token contexts in the Untis Platform, obtained through different flows:

| Context | Flow | Use case | Credentials used |
| --- | --- | --- | --- |
| **User context** | Authorization Code (this guide) | User-facing UI launched from the platform | OIDC client secret |
| **Service context** | Client Credentials | Server-to-server API calls, no user session | Platform-generated password |

Both flows use the same token endpoint (`/v3/{tenantId}/token`) but with different `grant_type` values and different credentials.

### Service context (API access — Client Credentials)

For server-to-server integrations that call APIs without a user session:

```
POST {API_URL}/WebUntis/api/sso/v3/{tenantId}/token
  ?grant_type=client_credentials
```

- Header: `Authorization: Basic {base64(client_id:password)}` — use the **platform-generated password**, not the OIDC secret
- Header: `Content-Type: application/x-www-form-urlencoded`
- Tokens are valid for 3 minutes (check `expires_in` in the response and avoid unnecessary token requests)

See [Authentication Model](core-concepts-authentication-model.md) for full details.

## ID token claims

The `id_token` returned from the token endpoint is a JWT. Which claims it contains depends on the scopes used in the authorize request. The tables below are based on a token requested with `openid roster-core.readonly`, and the same token requested with `openid roster-core.readonly untis-profile` added.

### Standard OIDC claims

| Claim | Description |
| --- | --- |
| `sub` | Stable subject identifier for the user. This is the only claim you should use to identify a user — see [User context and role influence](core-concepts-authorization-model.md). |
| `iss` | Issuer URL. Includes the tenant ID (`/v3/{tenantId}`). |
| `aud` | Audience — matches your OIDC `client_id`. |
| `iat` | Issued-at timestamp (Unix epoch, seconds). |
| `exp` | Expiry timestamp (Unix epoch, seconds). |

### WebUntis claims (always present, regardless of scope)

| Claim | Description |
| --- | --- |
| `tenant_id` | The school’s tenant ID. |
| `user_id` | Internal user ID. |
| `person_id` | Internal person ID (distinct from `user_id`). |
| `username` | The user’s login username. |
| `roles` | The user’s role, e.g. `TEACHER`. |
| `user_type` | `USER` for user-context tokens (Authorization Code flow). |
| `scopes` | The granted scopes, **comma-separated** — note this differs from the space-separated `scope` request parameter. |
| `locale` | The user’s WebUntis language. See [The `locale` claim](#the-locale-claim) below. |
| `sc` | School country — the country the school is located in (e.g. `at`). |
| `sr` | School region — the region (Bundesland) the school is located in (e.g. `AT-3`). |
| `sn` | School name. |

Note

The token also contains a small number of additional claims (e.g. `route`, `host`, `per`) that are reserved for internal platform use. They are not documented here, may change without notice, and must not be read or relied upon by integrations.

### Profile claims (only present with the `untis-profile` scope)

| Claim | Description |
| --- | --- |
| `given_name` | First name |
| `family_name` | Last name |
| `name` | Full/display name |
| `gender` | e.g. `MALE`, `FEMALE` |
| `birthdate` | Date of birth as a Unix epoch timestamp. Can hold implausible values (e.g. a large negative number resolving to year `0000`) when no birthdate is on file — treat such values as “not set” rather than a real date. |

Caution

Do not request the `untis-profile` scope for new integrations — as noted in [Step 1](#step-1--call-the-authorize-endpoint) above, it is not backwards-compatible and these claims may change without notice. Use `sub` together with the [OneRoster users endpoint](api-reference-oneroster-apis-users.md) to retrieve user details instead.

## The `locale` claim

The ID token’s `locale` claim identifies the user’s language in WebUntis. It is currently the single source of truth for the user’s language — there is no other endpoint or claim to cross-check it against.

- Always present — never `null` or empty.
- For standard languages, the claim contains only the language subtag (e.g. `de`) — not a full locale with region (e.g. not `de-AT`), though the value is still valid per the locale standard.
- Because only the language subtag is returned, there is no separator in practice. If a region were ever included, the expected separator would be a dash (`-`), not an underscore.

Caution

WebUntis also supports **custom languages**. For these, the `locale` claim does not contain a valid language subtag — it returns an internal WebUntis code instead. Known custom languages and their `locale` values:

| WebUntis language | `locale` value |
| --- | --- |
| Österreichisch | `deat` |
| Deutsch (Nicht gegendert) | `deng` |
| Deutsch Hochschule | `desh` |
| Norsk Høyskole (Norwegisch Hochschule) | `nohs` |

This list reflects the custom languages known at the time of writing. Don’t assume `locale` is always a standard language code; handle unrecognized values gracefully (e.g. fall back to a default language) rather than failing.

---

## Java examples

The following examples use **Spring `RestClient`** (Spring Framework 6.1+). No Spring Boot auto-configuration is assumed — the client can be used in any Java application.

### Discover per-tenant OIDC endpoints

Resolve the authorize and token endpoint URLs for a specific tenant dynamically instead of hardcoding them.

```
import org.springframework.web.client.RestClient;
import java.util.Map;

public class OidcDiscoveryClient {

    private static final String API_URL = "https://api.integration.webuntis.dev";

    private final RestClient http = RestClient.create();

    public Map<String, Object> discover(String tenantId) {
        String url = API_URL + "/WebUntis/api/sso/v3/" + tenantId
                   + "/.well-known/openid-configuration";
        return http.get().uri(url).retrieve().body(Map.class);
    }
}
```

Note

Use the discovered `authorization_endpoint` and `token_endpoint` values rather than constructing URLs manually. This makes your integration resilient to infrastructure changes.

### Build the authorization request and exchange the code

Build the authorization redirect URL (using the discovered `authorization_endpoint` from the previous step), then exchange the returned code for tokens at the `token_endpoint`.

```
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestClient;
import org.springframework.web.util.UriComponentsBuilder;
import java.security.SecureRandom;
import java.util.Base64;
import java.util.Map;

public class OidcAuthorizationClient {

    public String buildRedirectUrl(String authorizationEndpoint,
                                   String clientId,
                                   String redirectUri,
                                   String state,
                                   String nonce) {
        return UriComponentsBuilder.fromUriString(authorizationEndpoint)
                .queryParam("response_type", "code")
                .queryParam("scope", "roster-core.readonly openid")
                .queryParam("client_id", clientId)
                .queryParam("redirect_uri", redirectUri)
                .queryParam("state", state)
                .queryParam("nonce", nonce)
                .build()
                .encode()
                .toUriString();
    }

    /** Generates a cryptographically random string for use as state or nonce. */
    public static String generateSecureString() {
        byte[] bytes = new byte[32];
        new SecureRandom().nextBytes(bytes);
        return Base64.getUrlEncoder().withoutPadding().encodeToString(bytes);
    }
}

class TokenExchangeClient {

    private final RestClient http = RestClient.create();

    public Map<String, Object> exchangeCode(String tokenEndpoint,
                                            String code,
                                            String clientId,
                                            String clientSecret,
                                            String redirectUri) {
        MultiValueMap<String, String> form = new LinkedMultiValueMap<>();
        form.add("grant_type",    "authorization_code");
        form.add("code",          code);
        form.add("redirect_uri",  redirectUri);
        form.add("client_id",     clientId);
        form.add("client_secret", clientSecret);

        return http.post()
                .uri(tokenEndpoint)
                .header(HttpHeaders.CONTENT_TYPE,
                        MediaType.APPLICATION_FORM_URLENCODED_VALUE)
                .body(form)
                .retrieve()
                .body(Map.class);
    }
}
```

Note

Use `OidcAuthorizationClient.generateSecureString()` for both `state` and `nonce` — store them in the user’s session so you can verify `state` on the redirect callback and `nonce` inside the JWT (next step). Pass the `tokenEndpoint` value returned by the discovery call above.

Caution

Use the **OIDC client secret** in the form body — not the platform-generated password. The platform-generated password is only used for the Client Credentials flow.

### Parse and validate the ID token

Decode the returned `id_token` JWT, verify the `nonce` to prevent replay attacks, check expiry, and extract the `sub` claim to identify the user.

```
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import java.security.PublicKey;

public class IdTokenParser {

    private final PublicKey signingKey;
    private final String expectedIssuer;
    private final String clientId;

    /**
     * @param signingKey     the RSA public key from the tenant's JWKS endpoint
     *                       ({@code jwks_uri} in the well-known configuration)
     * @param expectedIssuer the issuer URL from the well-known OIDC configuration
     * @param clientId       your OIDC client ID (expected audience)
     */
    public IdTokenParser(PublicKey signingKey, String expectedIssuer, String clientId) {
        this.signingKey = signingKey;
        this.expectedIssuer = expectedIssuer;
        this.clientId = clientId;
    }

    public record ParsedIdToken(String sub, long exp) {}

    public ParsedIdToken parse(String idToken, String expectedNonce) {
        // JJWT validates the signature, structure, and expiry automatically.
        Claims claims = Jwts.parser()
                .verifyWith(signingKey)
                .requireIssuer(expectedIssuer)
                .requireAudience(clientId)
                .build()
                .parseSignedClaims(idToken)
                .getPayload();

        if (!expectedNonce.equals(claims.get("nonce", String.class))) {
            throw new SecurityException("Nonce mismatch — possible replay attack");
        }

        String sub = claims.getSubject();
        if (sub == null || sub.isBlank()) {
            throw new IllegalArgumentException("'sub' claim missing from id_token");
        }

        return new ParsedIdToken(sub, claims.getExpiration().toInstant().getEpochSecond());
    }
}
```

Note

`sub` is the only claim you should use to identify a user. Do not use the `untis-profile` scope or rely on name/email claims — those are not guaranteed stable. Call the [OneRoster users endpoint](api-reference-oneroster-apis-users.md) with the `sub` value to retrieve full user details.

Requires `io.jsonwebtoken:jjwt-api`, `jjwt-impl`, and `jjwt-jackson` on the classpath. The `signingKey` is the RSA public key from the `jwks_uri` field in the [well-known OIDC configuration](#discovering-endpoint-urls-well-known-configuration).

### Generate PKCE verifier and challenge

```
// Generate a 32-byte code-verifier and derive an S256 code-challenge
public static String generateCodeVerifier() throws NoSuchAlgorithmException {
    byte[] bytes = new byte[32];
    SecureRandom.getInstanceStrong().nextBytes(bytes);

    return Base64.getUrlEncoder()
            .withoutPadding()
            .encodeToString(bytes);
}

// Generate a code-challenge from the code-verifier
public static String generateCodeChallenge(String codeVerifier) throws Exception {
    MessageDigest sha256 = MessageDigest.getInstance("SHA-256");

    byte[] hash = sha256.digest(
            codeVerifier.getBytes(StandardCharsets.UTF_8));

    return Base64.getUrlEncoder()
            .withoutPadding()
            .encodeToString(hash);
}
```

## Relevant articles

[UI Integration](integration-guides-ui-integration.md)  How to embed your app in the Untis Platform — prerequisite for SSO.

[Authentication Model](core-concepts-authentication-model.md)  Conceptual overview of all authentication flows.

[Authorization Model](core-concepts-authorization-model.md)  Scopes, permissions, and tenant isolation.

[Get Your Platform Application](getting-started-get-platform-application.md)  Configure client ID, secret, and redirect paths.

[OneRoster Users](api-reference-oneroster-apis-users.md)  Retrieve user details from the sub claim.
