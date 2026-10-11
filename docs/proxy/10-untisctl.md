# 10 — `untisctl`

The operator CLI for a proxy's SQLite database. It edits the DB directly (like
`cmd/perm` / `cmd/seed`), so it can run against a **live** server's data file.

```sh
untisctl [-db PATH] <command> [options]
```

Global flags (also read from the environment):

| Flag | Env | Notes |
|---|---|---|
| `-db PATH` | `UNTIS_DB` | SQLite path; else `untis.db` |
| `-server HOST` | `UNTIS_SERVER` | fallback upstream host |
| `-school NAME` | `UNTIS_SCHOOL` | upstream school name |

Commands that mint `.ics` links accept `--base URL` (fallback
`UNTIS_PUBLIC_BASE`) so no deployment's hostname is baked into the binary.

## `perms`

```sh
untisctl perms list [--user U]            # global switches + per-user overrides
untisctl perms grant  [--user U|--global] TYPE
untisctl perms revoke [--user U|--global] TYPE
untisctl perms clear  --user U            # drop overrides → fall back to global
untisctl perms reset                      # wipe all permissions (class-pool-only default)
```

`TYPE` accepts aliases: `recon`/`reconstruction`, `boosted`/`boost`, `editor`,
`techniker`. See [01 — Permissions](01-permissions.md).

## `users`

```sh
untisctl users list
untisctl users add      --user U --secret S [--method password|key]
untisctl users remove   --user U          # user + secret + overrides + personal tokens
untisctl users admin    --user U [--on|--off]
untisctl users check    [--remove-classless]
```

`users check` asks the **real** Untis API for every account's class;
`--remove-classless` deletes students the API reports without a class. Use it to
reconcile the local roster with upstream.

## `pool`

```sh
untisctl pool list      # pooled classes and their owners
untisctl pool owners    # which user(s) own each class
```

## `calendar` (alias `tokens`)

Mint, list and revoke calendar subscription tokens. See
[05 — Calendar](05-calendar.md).

```sh
untisctl calendar create [FLAGS]
  --class ID            class timetable (must be in pool)
  --teacher NAME_OR_ID  teacher timetable (fuzzy name lookup)
  --room NAME_OR_ID     room timetable (fuzzy name lookup)
  --subject NAME_OR_ID  subject timetable (fuzzy name lookup)
  --personal            personal student timetable (self)
  --personal --user U   personal timetable for user U
  --base URL            base URL for the printed .ics link

untisctl calendar student [--user U]   # pick a student from the DB (interactive
                                       # menu, or --user U non-interactively)
untisctl calendar list                 # all tokens
untisctl calendar revoke TOKEN

untisctl tokens list                   # aliases for the above
untisctl tokens revoke TOKEN
```

`--teacher`, `--room` and `--subject` take a numeric id or a fuzzy name; `--class`
requires the class be in the pool. `calendar student` mints a personal
`--personal` token and prints its `.ics` URL.

## `totp`

```sh
untisctl totp USER [--scan]
```

Prints the current 6-digit TOTP code and the seconds left for `USER`. `--scan`
prints the `otpauth://` URI and an ANSI QR code (when `qrencode` is installed) so
a 2FA-protected account can be enrolled.

## `status`

```sh
untisctl status
```

DB stats: users, pool, perms, recon coverage and tokens.

## `backup`

```sh
untisctl backup [--out PATH] [--keep N]
```

A **consistent** copy of the database via `VACUUM INTO` — safe while the server
runs. Defaults to `<db>.untis-backup-<UTC>.db`; `--keep N` prunes all but the `N`
newest backups.

## See also

- [08 — Admin API](08-admin-api.md): the same operations over HTTP.
- [09 — Configuration](09-configuration.md): the flags/env shared with the server.
