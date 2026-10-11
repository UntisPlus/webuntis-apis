# Machine-readable specs

The prose docs are the primary reference in this repository. The OpenAPI
fragments that back them live in upstream projects; this directory indexes them
rather than redistributing them, to keep their original licenses intact.

## Internal / mobile (reverse-engineered) 🔴

From the **BetterUntis** Android client (**GPL-3.0**):

| File | Contents |
|---|---|
| [`untis-mobile.yaml`](https://github.com/SapuSeven/BetterUntis/blob/master/api/spec/untis-intern/untis-mobile.yaml) | `api/mobile/v2/.../authentication`, JWT response |
| [`untis-rest.yaml`](https://github.com/SapuSeven/BetterUntis/blob/master/api/spec/untis-intern/untis-rest.yaml) | `api/rest/view/v1` messages, mobile data, home, contact data |

- Project: <https://github.com/SapuSeven/BetterUntis>
- License: GNU GPL v3.0 (the spec files are covered by that project's license).
- These describe reverse-engineered, undocumented endpoints.

## External timetable API

| Spec | Origin | Location |
|---|---|---|
| Timetable API v1/v2/v3 | 🟢 Untis GmbH | <https://developer.untis.com/api-reference/webuntis-apis/timetable-data/> |

## Public JSON-RPC

| Spec | Origin | Location |
|---|---|---|
| WebUntis JSON-RPC API (2018-09-20) | 🟡 Untis-authored PDF | [untis-sr.ch mirror](https://untis-sr.ch/wp-content/uploads/2019/11/2018-09-20-WebUntis_JSON_RPC_API.pdf) |

## Adding a spec

If you add a machine-readable spec, keep the original license and attribution in
this directory, and link it from the relevant page in [`docs/`](../docs).
