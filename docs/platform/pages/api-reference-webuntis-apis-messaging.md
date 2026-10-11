# Messaging

> Source: Untis GmbH developer documentation, `developer.untis.com/api-reference/webuntis-apis/messaging/`.
> Reproduced here as an offline mirror so this repository is self-contained.
> © Untis GmbH; see [`NOTICE.md`](../../../NOTICE.md).

---

Send messages to Untis Platform users — either as the platform app itself (using a client credential flow token) or on behalf of a specific user (using a OIDC code flow token).

v1  Send-only   **Endpoints:** 1

**Note:** This API **only sends** messages. Message retrieval and inbox access are not
supported.

---

## Use cases

Notifications

Send automated alerts, event reminders, and administrative announcements.

Communication bridge

Connect external communication systems to Untis Platform’s messaging.

---

## Endpoints

| Method | Operation ID | Description |
| --- | --- | --- |
| `POST` | `messages` | Send a message to one or more recipients |

---

## Sending context

| Token type | Behavior |
| --- | --- |
| **Platform token** | Message appears from the platform itself |
| **User token** | Message appears from the authenticated user |

---

## Recipients

Pass one or more user IDs in the request body. There is no built-in group or role targeting — if you need to message all students or all teachers, query the relevant API first to collect their IDs, then pass the full list to the messages endpoint.

---

## Message formatting

Message content supports **Markdown**, including links. For example:

```
Please review the [updated schedule](https://example.com/schedule) before Monday.
```

Untis Platform renders Markdown in the recipient’s inbox, so links, bold, and other inline formatting are displayed correctly.

---

## Related pages

[Authentication Model](core-concepts-authentication-model.md)  Understand platform vs. user tokens that control sending context.

[Legal Guardian Management](api-reference-webuntis-apis-legal-guardian-management.md)  Provision guardian accounts before sending them messages.

---

## API reference
