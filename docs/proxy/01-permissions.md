# 01 — How it works & permissions

WebUntis upstream applies the rights of the authenticated school account.
UntisPlus can add timetable pooling, reconstruction and scoped use of saved
teacher sources. The proxy checks local capabilities before using these sources.

## Effective access

Use **Permissions** in the dashboard to create capability groups and assign them
to people. Groups stack, and role or everyone defaults also apply unless
excluded for a person. A direct account rule takes precedence over groups.
Server gates and feature switches set the ceiling. A school cannot re-enable
a server-disabled feature. Dashboard administrator status and upstream account
roles are separate from these timetable capabilities.

| Purpose | Current controls |
| --- | --- |
| Use upstream as the logged-in account | The upstream-only Basic preset and `timetable.upstream.view` |
| Donate a class | `pool.timetable.share` |
| Browse or read pooled classes | `pool.class.view` and `timetable.class.pooled.view` |
| Reconstruct a timetable | Separate teacher, room and subject reconstruction capabilities |
| Use a saved teacher source | Separate class, teacher, room, subject and personal timetable capabilities |
| Modify upstream records | Separate absence and lesson write capabilities, subject to source account restrictions |
| Manage Technik events and attendance | Individually granted actions described in [11](11-analytics-and-access.md#separate-technik-actions) |

The [Basic preset](13-basic-and-compatibility.md) is an explicit upstream-read
baseline. Assign it additively or use the confirmed reset to replace the
person's direct permissions and disable inherited defaults.

`GET /me` requires the caller's own session and exposes the legacy level and
flags for clients that use them. Administrators can inspect effective
capabilities for an account with `GET /admin/access/effective?school=NAME&user=USERNAME`.
Legacy Basic/Recon/Boosted/Editor/Techniker flags are compatibility shorthands.
Use capability groups for new configurations.

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
plus the absence/lesson writes) as the boosted teacher when the caller has the applicable class-scoped capability, on both the self-authenticating `jsonrpc_intern.do` path and the
session `jsonrpc.do` path. It is deliberately narrow:

- **Personal data stays personal.** The user's own timetable, own absences and
  `getUserData2017` keep running on their own account.
- **Class-scoped access is checked per request.** Callers without it use
  their own upstream account.
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

A user can sign in through upstream without pre-seeding credentials. Use a
normal enrolment flow if the proxy needs a replayable source for timetable
fetches. Dashboard administrator access requires explicit provisioning through
`UNTIS_ADMIN`, `-admin`, or `untisctl users admin --user USERNAME`.

See [10](10-untisctl.md) for operator commands. Review [compatibility diagnostics](13-basic-and-compatibility.md)
to check credential presence and upstream timetable support without exposing secrets.
