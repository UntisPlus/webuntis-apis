# UI Integration

> Source: Untis GmbH developer documentation, `developer.untis.com/integration-guides/ui-integration/`.
> Reproduced here as an offline mirror so this repository is self-contained.
> © Untis GmbH; see [`NOTICE.md`](../../../NOTICE.md).

---

UI integration adds entry points inside the Untis Platform that launch your application. When a user clicks the entry point, the Untis Platform opens your app — either in a new tab or embedded as an iFrame — and passes contextual parameters so your app knows which school, lesson, or exam was selected.

UI integration is independent of SSO, but the two are commonly combined: UI integration provides the entry point and launch context, while SSO authenticates the user automatically when your app opens. See [SSO Integration](integration-guides-sso.md) for details.

## Supported entry points

### Untis Platform (web)

| Entry point | Modes supported | Context passed |
| --- | --- | --- |
| **Main menu** | New tab, iFrame | School (tenant) |
| **Lesson details** | New tab, iFrame | School, lesson, period, classes, subjects, time |
| **Examinations** | New tab only | School, exam |
| **Timetable view** | New tab (via button) | Configured via [Calendar API](integration-guides-calendar.md) |

### Untis Mobile (iOS / Android)

| Entry point | What can be integrated |
| --- | --- |
| **Home tab** | Your native iOS/Android app or a web app in an embedded browser |
| **Lesson details** | Your native iOS/Android app or a web app in an embedded browser |

## Integration modes

New tab (redirect)

Opens your app in a new browser tab. The simplest mode — supported at **all
entry points**. Context is passed as query parameters on your configured
redirect URL.

iFrame (embedded)

Embeds your app inside the Untis Platform UI without a new tab. Available
for **main menu** and **lesson details** only — not for Examinations.

**iFrame constraints to be aware of:**

- Your application must allow being loaded inside an iFrame (do not send `X-Frame-Options: DENY` or a restrictive `frame-ancestors` CSP directive)
- Browser cookie restrictions (e.g. `SameSite`) apply — ensure your session cookies are set with `SameSite=None; Secure`
- Some browser security features (e.g. popups, clipboard access) may be restricted inside iFrames
- HTTPS is required

## Context parameters

When launching your application, the Untis Platform appends the following query parameters to your configured URL. Your application should read and use these to load the correct context for the user.

### Main menu

| Parameter | Description | Example |
| --- | --- | --- |
| `tenant_id` | Unique ID of the school | `1600` |
| `school` | Unique name of the school | `integration16` |

**Example URL:**

```
https://www.yourdomain.com/redirect?tenant_id=1600&school=integration16
```

### Lesson details

| Parameter | Description | Example |
| --- | --- | --- |
| `tenant_id` | Unique ID of the school | `1600` |
| `school` | Unique name of the school | `integration16` |
| `lesson_id` | Unique ID of the lesson | `1200` |
| `period_id` | Unique ID of the specific period instance | `5769` |
| `exam_id` | Unique ID of an exam (optional, only present if an exam is associated) | `432` |
| `classes` | Name(s) of the class(es) (URL-encoded) | `1.%20Class%20A` |
| `subjects` | Name(s) of the subject(s) | `Mathematics` |
| `start` | Start time of the period (ISO 8601, URL-encoded) | `2021-08-17T08%3A55%3A00` |
| `end` | End time of the period (ISO 8601, URL-encoded) | `2021-08-17T09%3A40%3A00` |

**Example URL:**

```
https://yourdomain.com/redirect?tenant_id=1600&school=integration16&lesson_id=48&period_id=6575&exam_id=432&classes=1.%20Class%20A&subjects=Mathematics&start=2021-08-17T08%3A55%3A00&end=2021-08-17T09%3A40%3A00
```

### Examinations

| Parameter | Description | Example |
| --- | --- | --- |
| `tenant_id` | Unique ID of the school | `1600` |
| `school` | Unique name of the school | `integration16` |
| `exam_id` | Unique ID of the exam | `1203` |

## Role-based behavior

The visibility and behavior of your application’s entry points can differ by user role. Default values (menu name, redirect path, etc.) are configured per role for your platform application by the Untis Platform. School administrators can override some of these values directly in Untis Platform.

This means you can present different entry points or target different URLs for students, teachers, and admins — without your application needing to handle the routing itself.

## Custom icon

Your application can display a custom icon in Untis Platform and Untis Mobile. The icon is configured as part of your platform application setup. Contact the Untis Platform to provide your icon asset.

## Mobile considerations

Mobile integration (Untis Mobile) supports two entry points — **home tab** and **lesson details** — and two integration types:

Native app

Untis Mobile launches your iOS/Android app via a deep link or app store
link.

Web app (embedded browser)

Untis Mobile opens your web app inside its embedded browser. Same context
parameters apply. Ensure your app has a responsive mobile layout.

iFrame embedding is **not** used in Untis Mobile. To test, set up the Untis Mobile app with a test school on the integration environment — see the [Untis Mobile profile setup guide](https://help.untis.at/hc/de/articles/360010794740-Wie-lege-ich-mein-Profil-in-Untis-Mobile-an).

## UI guidelines

If you want to align your application’s design with the Untis Platform, a style guide and media kit are available. Contact the Untis Platform team to request them.

## Relevant articles

[SSO Integration](integration-guides-sso.md)  Authenticate the user automatically when your app is launched.

[Authentication Model](core-concepts-authentication-model.md)  Authentication flows overview.

[Get Your Platform Application](getting-started-get-platform-application.md)  Request and configure your platform application.
