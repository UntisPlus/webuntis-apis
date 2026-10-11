# 01 — How it works & permissions

The proxy exists because WebUntis is **per-user**: a student sees only their own
timetable and a teacher only theirs. Rather than escalate privileges, the proxy
pools what users already have and reconstructs the rest.

## The four mechanisms

### 1. Pooling

Every user automatically donates **their class** to the pool on login — student
and non-student alike. The pool is the union of all donated classes, and each
pooled class is fetched with its owner's student key. A class is in the pool as
soon as any user belongs to it (`class_id` set).

The result: any pool member can read any pooled class's timetable, with no
per-user WebUntis grant needed.

### 2. Reconstruction (`recon`)

A teacher, room or subject timetable is not stored anywhere by WebUntis. The
proxy *reconstructs* it by scanning the pooled classes and collecting every
period where that element appears. The reached date is persisted per class, so a
restart resumes rather than restarting; a class is re-scanned once its stored
horizon is more than `-recon-refresh` days (default `21`) behind the target.

This is what the **`recon`** permission grants.

### 3. Forwarding (`boosted`)

Where reconstruction is not wanted, a request can instead be re-authenticated as
a **saved teacher account** and forwarded raw — no reconstruction. This is what
the **`boosted`** permission grants. A boosted user's own personal (STUDENT)
timetable is served the same way, giving it teacher-grade visibility (e.g.
unlimited future weeks). Boosted alone grants **no** write powers. If no teacher
account is saved, boosted falls back to Basic.

### 4. Change detection

Every `-poll-interval` (default `60s`) the proxy re-fetches each pooled class,
diffs it against the last stored snapshot, and bumps a per-class version. Diffs
are persisted and fanned out to the [change stream](03-change-detection.md),
[webhooks and ntfy](04-notifications.md).

## Permission tiers

Access is a set of per-user flags on top of a Basic default.

| Tier | Flag | Scope | What you get |
|---|---|---|---|
| **Basic** | *(none)* | everyone | Pooled classes + your own personal student timetable + reading your own absences |
| **Reconstruction** | `recon` | global switch or per-user | Teacher / room / subject timetables reconstructed 100% from pooled class data |
| **Boosted** | `boosted` | per-user only | Class/teacher/room/subject timetables raw-forwarded through a saved teacher account |
| **Editor** | `editor` | per-user only | Boosted **plus editing**: unlocks absence + lesson/subject write methods; runs class-scoped editor calls as the boosted teacher |
| **Techniker** | `techniker` | per-user only | Sees a synthetic **Technik** class aggregating every student's admin-authored events, plus a proxy-local absence register |

Rules:

- **Boosted XOR Recon** — the flags are mutually exclusive per user; granting
  one auto-revokes the other.
- **`editor` implies `boosted`.** Holding `editor` alone is enough.
- **`boosted`, `editor` and `techniker` are per-user only** (no `--global`),
  because each grants access to data pooled from several accounts.
- **Being a proxy admin does not imply editing.** Admins manage accounts; they
  do not write to Untis unless they hold `editor`.
- Absence **reads** (`getStudentAbsences2017`) are available to everyone by
  default; only the **write/mutation** methods need `editor`.

Grant/revoke from the [dashboard](08-admin-api.md) *Users* section or with
[`untisctl perms`](10-untisctl.md).

### Reading the effective level

```
GET /me
```

```json
{"username":"Jdoe","level":"recon",
 "permissions":{"recon":true,"boosted":false,"editor":false}}
```

`level` is one of `basic`, `recon`, `boosted`, `boosted+editor`. Requires a
session; `401 {"error":"not logged in"}` otherwise.

## Why the editor needs a teacher identity

The app builds its absence editor (and the per-lesson editing sheet) from
`getPeriodData2017`. Upstream answers that method with the class roster, the
register, the absence state and the `can` capabilities **only when the request
authenticates as a teacher**. The identical call as a student comes back empty:

| field of a `getPeriodData2017` result | as a student | as a teacher |
|---|---|---|
| `referencedStudents` | `0` | class size |
| `studentIds` / `classRoles` | `0` | class size / entries |
| `absences` | `null` | the actual entries |
| `can` | `READ_HOMEWORK`, `READ_PERIODINFO` | includes `READ_STUD_ABSENCE`, `WRITE_STUD_ABSENCE`, `READ/WRITE_CLASSREGEVENT`, … |

So the proxy re-authenticates the **class-scoped methods** (`getPeriodData2017`
plus the absence/lesson writes) as the boosted teacher for users holding
`editor`, on both the self-authenticating `jsonrpc_intern.do` path and the
session `jsonrpc.do` path. It is deliberately narrow:

- **Personal data stays personal.** The user's own timetable, own absences and
  `getUserData2017` keep running on their own account.
- **Only editors are lifted.** A non-editor's `getPeriodData2017` is forwarded
  with their own account.
- **A write still needs the permission upstream grants it.** Routing through the
  teacher lets a legitimate editor's write succeed; it grants nothing extra.

The log prints `[intern] class-scoped <method>: <user> -> <teacher>` when a lift
happens.

## Capability rewriting

Upstream derives each period's `can` list from the account the request
authenticated as, and the app hides any UI whose capability is missing. The
proxy rewrites `can` on the way out:

- **`READ_LESSONTOPIC` is always added.** A pooled class is fetched with the
  class owner's student key (capabilities only `READ_HOMEWORK`/`READ_PERIODINFO`),
  so without this the app silently hides the lesson topic.
- **Every non-`READ_` capability is dropped unless the user holds `editor`.**
  A boosted user is forwarded through a teacher account that returns the full
  teacher capability set; without the rewrite the app would offer editing on
  classes the user only has read access to. The server-side write gate refuses
  those anyway, so this only removes dead buttons — with `editor` they return.

In the app, classes are always shown; **teacher/room/subject element types are
hidden unless the user has recon or is boosted** (the masterData
`displayAllowed` flags are set from the user's effective access). For a recon
user they are also narrowed to elements the pooled classes actually reference.

## Multi-school

One proxy process can serve many WebUntis schools:

- The **school name** identifies every dimension: pool, recon, master data,
  tt-cache, permissions, tokens, webhooks, ntfy topics.
- On the **first login from a school the proxy has never seen**, the school is
  auto-registered and its initial recon enumeration starts in the background —
  no restart needed.
- The change-detection poll loop re-reads the `schools` table periodically, so
  auto-registered schools get polled automatically.
- All in-memory caches are per-school; cache keys carry the school prefix.
- Clients select a school with `?school=` on login/JSON-RPC/REST requests (it is
  persisted on the user row); a `schoolname` cookie remembers it.

An admin can remove a school row from the dashboard's *Schools* section; its
data stays keyed by school name and becomes orphaned.

## Bootstrapping accounts

Once per person, provision their WebUntis account into the DB so the proxy can
authenticate as them (making them a pool owner / able to log in):

1. Add the account with `untisctl users add` (key or password).
2. Optionally grant reconstruction perms with `untisctl perms grant …`.
3. `untisctl users check` to confirm the stored logins actually work.

The seed tool (`cmd/seed`) does the same from an INI-style `credentials.txt` and
also fills in `person_id` / `class_id` by logging in live.

See [`10-untisctl.md`](10-untisctl.md) for the full command set.
