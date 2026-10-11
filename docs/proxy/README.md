# UntisPlus Proxy — extra API surface

The [UntisPlus Proxy](../..) is a Go reverse-proxy that sits in front of a
WebUntis school server and adds a set of capabilities WebUntis itself does not
offer. This directory documents every endpoint, permission, and behaviour it
adds **on top of** the raw WebUntis APIs described in the rest of this
repository.

It is a **non-upstream** surface: everything here is implemented by the proxy,
not by Untis GmbH, and can change with the proxy version. The upstream
WebUntis APIs it forwards are documented in [`../`](../README.md).

> Provenance: 🔴 **community / proxy-implemented**. Not authored or endorsed by
> Untis GmbH. See [`../../NOTICE.md`](../../NOTICE.md).

## What the proxy adds

| Capability | Why it exists | Doc |
|---|---|---|
| **Class pooling + reconstruction** | WebUntis is per-user; the pool makes every donated class readable by everyone, and teacher/room/subject timetables are *reconstructed* from it | [01](01-permissions.md) |
| **Raw forwarding ("boosted")** | Serve an element's timetable by re-authenticating as a saved teacher account, instead of reconstructing | [01](01-permissions.md) |
| **Editing ("editor")** | Unlock the absence / lesson write methods, run class-scoped calls as a teacher | [01](01-permissions.md) |
| **Technik / student events** | Admin-authored dated entries on one student's timetable, with a local absence register | [07](07-student-events.md) |
| **Change detection** | Poll each pooled class, diff against the last snapshot, bump a version | [03](03-change-detection.md) |
| **SSE change stream** | Live push of detected changes to a client | [03](03-change-detection.md) |
| **Webhooks + ntfy** | Durable, element-targeted notifications of changes | [04](04-notifications.md) |
| **iCal subscriptions** | Bookmarkable `.ics` feed for any class/person/teacher/room/subject | [05](05-calendar.md) |
| **Server-rendered `/week` page** | A JS-free week view for a parent's phone, from the same token | [05](05-calendar.md) |
| **Homework flags** | A student's own "done" mark, separate from the teacher's `completed` | [06](06-homework-and-absences.md) |
| **Absence notes + derived metadata** | A private note per absence plus resolved subject/reason | [06](06-homework-and-absences.md) |
| **Admin dashboard + JSON API** | Manage users, perms, pool, tokens, schools, subscriptions, events | [08](08-admin-api.md) |
| **Multi-school** | One process serves many schools; a new school self-registers on first login | [01](01-permissions.md) |
| **Operator CLI (`untisctl`)** | Manage the database without the server | [10](10-untisctl.md) |

## Page index

| Page | Contents |
|---|---|
| [01 — How it works & permissions](01-permissions.md) | Pooling, reconstruction, boosted, editor, techniker, multi-school |
| [02 — HTTP endpoint reference](02-endpoints.md) | Every route, method, auth and response |
| [03 — Change detection](03-change-detection.md) | `/api/timetable/changes`, `/api/timetable/stream`, the digest |
| [04 — Notifications](04-notifications.md) | Webhooks, ntfy, the durable outbox, signatures |
| [05 — Calendar subscriptions](05-calendar.md) | `/api/calendar/token`, the `.ics` feed, `/week/{token}` |
| [06 — Homework & absences](06-homework-and-absences.md) | `done` flags, notes, the `derived` block |
| [07 — Student events (Technik)](07-student-events.md) | Custom events, event absences, room map, import |
| [08 — Admin API](08-admin-api.md) | `/admin` dashboard and its JSON endpoints |
| [09 — Configuration](09-configuration.md) | Flags / env vars, metrics, public surface |
| [10 — `untisctl`](10-untisctl.md) | Operator CLI reference |

## Login: the proxy's own auth

The proxy does not change how you authenticate to WebUntis — it accepts the
same flows described in [`../02-authentication.md`](../02-authentication.md) and
[`../06-mobile-rest-auth.md`](../06-mobile-rest-auth.md) — but it adds one
convenience:

> **Paste the base32 shared secret itself.** At the `getUserData2017` /
> `keyLogin` login you may put the **base32 TOTP secret** (the authenticator
> setup key) in the `otp` field instead of a live 6-digit code. The proxy
> derives the current code, validates it upstream, and then **remembers the
> secret** so the account is replayable on later logins. A wrong or foreign
> paste never overwrites a stored key — the secret is only persisted after the
> real server accepts the login. Six-digit codes keep working unchanged.

The client binds a session to a school with `?school=<name>`; the proxy returns
a `JSESSIONID` cookie that the following `jsonrpc.do` / REST calls carry.

## Notes on scope

- Endpoints under `/WebUntis/…` are **forwarded** to the upstream school server
  after the proxy's permission, capability and enrichment passes. Their
  request/response bodies are the upstream ones, decorated as described on the
  pages above.
- All other routes (`/api/...`, `/admin`, `/status`, `/healthz`, `/me`,
  `/week/...`) are **implemented by the proxy** and have no upstream
  equivalent.
