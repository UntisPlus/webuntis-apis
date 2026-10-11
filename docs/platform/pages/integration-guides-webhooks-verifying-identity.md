# Verifying the Untis Platform Identity

> Source: Untis GmbH developer documentation, `developer.untis.com/integration-guides/webhooks/verifying-identity/`.
> Reproduced here as an offline mirror so this repository is self-contained.
> © Untis GmbH; see [`NOTICE.md`](../../../NOTICE.md).

---

Every request the Untis Platform sends to your webhook endpoints is **signed with an RSA private key**. Your application must verify the signature before trusting or acting on the payload.

Verification is a hard requirement — never skip it, even in development. Your webhook endpoints receive credentials and lifecycle events for your tenants. A forged or replayed request that bypasses verification can cause data loss or credential exposure.

## How signing works

1. The Untis Platform computes an **RSA signature** over the raw request body bytes.
2. The signature is base64-encoded and included in the `Authorization` request header.
3. The algorithm name is included in the `Algorithm` request header (e.g. `SHA256withRSA`).
4. You verify the signature using the **Untis Platform public key** for your environment.

## Request headers

| Header | Value |
| --- | --- |
| `Authorization` | Base64-encoded RSA signature over the raw request body |
| `Algorithm` | The signing algorithm used, e.g. `SHA256withRSA` |
| `Content-Type` | `application/json; charset=utf-8` |

## Public keys

The public keys are environment-specific. Both are X.509 SubjectPublicKeyInfo format, base64-encoded without PEM headers. Treat them as configuration values — do not hardcode them directly in your application logic.

- [Integration-Stage](#tab-panel-3487)
- [Calendar Integration - (Integration-Stage)](#tab-panel-3488)
- [Staging-Stage](#tab-panel-3489)
- [Calendar Integration - (Staging-Stage)](#tab-panel-3490)
- [Production](#tab-panel-3491)

```
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxmHgTa7Qf4buurWraH9MqcEipr4YrMpIg1NVbV7sx2p1yhZ5HQ5hPfsuRRqk9ss7UYJS4dnTsjLCwJ1j91PmxZBnceSkgjHunZ53AxsQP7h/A8g3igbi+tRw6+9agyM8zRLeAaufQFvm6/81obezB54vjv1qPGXgX07cmgj2w2EMC39Q4S0eKVU8svjw3QTE0ZD7Gc92T+rMIhVrX5sAKviczs8VSA8CZnM7PDASZ/kjZF9umMfEzmxGm5BVCqMqpCTFh3CMljMmoH3lCro3r9Ve2Unl5Cc8wRJekSOIbpKJ54eVL6zwEExfPlTKQZslLKBhaNtquLJJkgV057ANDwIDAQAB
```

```
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA5RoNcptXIbRuXlGAgmdgmKSuabMz6cUzVj7CTOKHpd1mBZanNkojUY+wJY2qobwuou5iwDFI58fR5QH8bp0H7NScg5oIiQW3c/0Idq82JhunhKRqco9KDNnT9Sehu6VdP8lmSa/IEtUkZMxJw/QQXrHE4veT78PmR0MfoNbiRrhRvQJYK4o2FdOLj3apY+JTfzL1n9xFDYAlNQssDS3QJ8KIXoz8d36wqALCxyC7PLKhceNWlION4XRFA1+AGYZ1ErvGHRk4RGim1sV/6Vev+JIo0E99VMg1Il3bDC6++RDOj9jMAwyLkGBwyIVmGbWUCknpqsI9BkSgKFInWSf4XwIDAQAB
```

```
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtmV6S87U7tZmKu5EQTui7wu4FTJybbzcl4PaMzO1cTcUckEmWSG9gck/Wl0rfm5bMmIbXvz3YgaxKYUsSLXFzEWXic9TG1EWnKHrbHFRYuhXSCmxAZe/+H8qzsU62p1yfOQOOPtWnZO/bPEeMNIzpKqy9ZweCyQ3lAj7TNFG4evxuZY47dnqRDVxFAQQbIbV70uiYxOtT/XS4vh0yhx/KwrRdYPxuMurqIkn8pWL+78vCrW7HLNakqUnhUUYjzFIFcCMLK9qDexqGQ/UAqKboFkojG+zjEjabhKl1fHT1GlFdJrU1ysg7yg/dbYjOFJ5oGFRZe7OCJks+RXHq6nnsQIDAQAB
```

```
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAy4SObQ2nfru24gRbrx7LqWbvbYyeMgWu6rWk5PdnZ5hFDoabRIdQPeL8EEp/vHz2AUjArYefoNuSY+0stSAdLYpH5OKLxao2fTpwpZxj70DNEPlFPsjQznX9OyXiNEEGKrXdXuuCHYjUsEwgbZijbJXWba/DqPqs9KIzRZBTjAOMKlPIm0cTtQ63GgD41AQoXY9PWnH8mDjrCrwXIgNiUw6imMUjsiR+kF9YP3+SizKDFoeiV7Xl6xdbi953OPVZ/KtSx2hn9RqH7jXv43TYXyRsRnDAH1mWt6ZAYJV+3JaCHGEwvN6yNQcnaBPWGXjw3s614iQgDR5EF0EpU4JtOwIDAQAB
```

```
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAy4SObQ2nfru24gRbrx7LqWbvbYyeMgWu6rWk5PdnZ5hFDoabRIdQPeL8EEp/vHz2AUjArYefoNuSY+0stSAdLYpH5OKLxao2fTpwpZxj70DNEPlFPsjQznX9OyXiNEEGKrXdXuuCHYjUsEwgbZijbJXWba/DqPqs9KIzRZBTjAOMKlPIm0cTtQ63GgD41AQoXY9PWnH8mDjrCrwXIgNiUw6imMUjsiR+kF9YP3+SizKDFoeiV7Xl6xdbi953OPVZ/KtSx2hn9RqH7jXv43TYXyRsRnDAH1mWt6ZAYJV+3JaCHGEwvN6yNQcnaBPWGXjw3s614iQgDR5EF0EpU4JtOwIDAQAB
```

 

## Attribute order matters

JSON attribute order requirement

The signature is computed over the **raw body bytes as received**. The Untis Platform serialises the JSON payload with a defined field order that matches the order documented in each webhook’s payload schema. If you re-serialise the JSON before verifying, the attribute order may differ and the signature check will fail.

**Always verify the signature against the original, unmodified request body bytes — not against a parsed-and-re-serialised object.**

## Verification steps

1. **Read the raw request body** as bytes before any parsing.
2. **Extract** the `Authorization` and `Algorithm` headers.
3. **Base64-decode** the `Authorization` header value to get the signature bytes.
4. **Load the public key** for your environment (X.509 DER format, base64-decoded).
5. **Initialise** an RSA signature verifier with the algorithm from the `Algorithm` header.
6. **Feed** it the raw request body bytes.
7. **Verify** the decoded signature against the body.
8. **Reject** with `401` if verification fails. Process the payload only if verification succeeds.

```
sequenceDiagram
    autonumber
    participant WU as Untis Platform
    participant YA as Your App

    WU->>YA: POST /webhook (Authorization + Algorithm headers)
    alt RSA signature valid
        YA-->>WU: 200 OK
        YA->>YA: Process payload
    else RSA signature invalid
        YA-->>WU: 401 Unauthorized
    end
```

## Code examples

- [Java](#tab-panel-3492)
- [Node.js](#tab-panel-3493)
- [Python](#tab-panel-3494)

```
@PostMapping("/credentials")
public ResponseEntity<?> receiveCredentials(
    @RequestBody String request,
    @RequestHeader("Authorization") String requestSignature,
    @RequestHeader("Algorithm") String algorithm
) throws Exception {

    // Load public key
    byte[] decoded = Base64.getDecoder().decode(PUBLIC_KEY_STRING.getBytes());
    X509EncodedKeySpec spec = new X509EncodedKeySpec(decoded);
    KeyFactory kf = KeyFactory.getInstance("RSA");
    PublicKey publicKey = kf.generatePublic(spec);

    // Verify signature
    Signature signature = Signature.getInstance(algorithm);
    signature.initVerify(publicKey);
    signature.update(request.getBytes(StandardCharsets.UTF_8));

    byte[] decodedSignature = Base64.getDecoder()
        .decode(requestSignature.getBytes(StandardCharsets.UTF_8));

    if (!signature.verify(decodedSignature)) {
        throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, "Invalid signature");
    }

    // Parse payload only after successful verification
    ObjectMapper mapper = new ObjectMapper();
    CredentialsPayload payload = mapper.readValue(request, CredentialsPayload.class);
    // ... handle payload
}
```

```
import express from "express";
import crypto from "crypto";

const app = express();

app.post("/credentials", express.raw({ type: "application/json" }), (req, res) => {
  const rawBody = req.body; // Buffer — must be read before any parsing
  const requestSignature = req.headers["authorization"];
  const algorithm = req.headers["algorithm"];

  // Map incoming algorithm header to Node.js algorithm name
  const algorithmMap = { "SHA256withRSA": "RSA-SHA256" };
  const nodeAlgorithm = algorithmMap[algorithm];
  if (!nodeAlgorithm) {
    return res.status(400).json({ error: "Missing or unsupported algorithm" });
  }

  // Load public key
  const publicKey = crypto.createPublicKey({
    key: Buffer.from(PUBLIC_KEY_BASE64, "base64"),
    format: "der",
    type: "spki",
  });

  // Verify signature
  const verify = crypto.createVerify(nodeAlgorithm);
  verify.update(rawBody);
  const signatureBytes = Buffer.from(requestSignature, "base64");

  if (!verify.verify(publicKey, signatureBytes)) {
    return res.status(401).json({ error: "Invalid signature" });
  }

  // Parse payload only after successful verification
  const payload = JSON.parse(rawBody.toString("utf-8"));
  // ... handle payload
  res.sendStatus(200);
});
```

```
from flask import Flask, request, abort
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

app = Flask(__name__)

@app.post("/credentials")
def receive_credentials():
    raw_body = request.get_data()  # bytes, before any parsing
    request_signature = request.headers.get("Authorization")
    algorithm = request.headers.get("Algorithm")

    # Map incoming algorithm header to a hash instance
    algorithm_map = {"SHA256withRSA": hashes.SHA256()}
    hash_algorithm = algorithm_map.get(algorithm)
    if hash_algorithm is None:
        abort(400)

    # Load public key
    public_key_der = base64.b64decode(PUBLIC_KEY_BASE64)
    public_key = serialization.load_der_public_key(public_key_der, backend=default_backend())

    # Verify signature
    signature = base64.b64decode(request_signature)
    try:
        public_key.verify(signature, raw_body, padding.PKCS1v15(), hash_algorithm)
    except Exception:
        abort(401)

    # Parse payload only after successful verification
    payload = request.get_json(force=True)
    # ... handle payload
    return "", 200
```

## Replay attack prevention

The platform-initiated webhooks do not currently include a request timestamp or nonce. As a baseline precaution:

- Process deactivation and credentials events **idempotently** — handling the same event twice should produce the same result as handling it once (see each webhook’s handling requirements).
- If you build additional infrastructure around webhook endpoints (e.g. an event queue), track and deduplicate event IDs where available.

## Relevant articles

[Integration Webhooks](integration-guides-webhooks.md)  Overview and common request flow.

[Credentials Webhook](integration-guides-webhooks-credentials.md)  Payload and handling for credentials transfer.

[Deactivation Webhook](integration-guides-webhooks-deactivation.md)  Payload and handling for deactivation events.

[Calendar API](integration-guides-calendar.md)  Calendar fetch request handling.
