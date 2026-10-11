# Machine-readable specs

Everything lives in this repository — you should never need to leave it to work
with the WebUntis/Untis APIs. This directory holds the OpenAPI documents that
back the prose in [`docs/`](../docs), vendored here so the repo is a single,
complete reference.

## Index

| File | Origin | Contents |
|---|---|---|
| [`untis-intern/untis-mobile.yaml`](untis-intern/untis-mobile.yaml) | 🔴 BetterUntis | `api/mobile/v2/.../authentication`, JWT response |
| [`untis-intern/untis-rest.yaml`](untis-intern/untis-rest.yaml) | 🔴 BetterUntis | `api/rest/view/v1` messages, mobile data, home, contact data |
| [`untis-extern/untis-extern-timetable-api-v3.yaml`](untis-extern/untis-extern-timetable-api-v3.yaml) | 🟢 Untis GmbH | External Timetable API v1/v2/v3 |
| [`untis-extern/schemas/error/`](untis-extern/schemas/error) | 🟢 Untis GmbH | Error schemas for the external timetable API |
| [`untis-platform/*.yaml`](untis-platform/README.md) | 🟢 Untis GmbH | Full OpenAPI specs for all 15 Untis Platform APIs |

> The public JSON-RPC method set is documented **in full** in
> [`docs/04-jsonrpc-public.md`](../docs/04-jsonrpc-public.md), so you don't need
> the original Untis PDF to use it.

## Licenses & attribution

The repository is mixed-license. Attribution and license texts are kept next to
the files they cover:

- **`untis-intern/`** — reverse-engineered by the
  [BetterUntis](https://github.com/SapuSeven/BetterUntis) project and licensed
  under the **GNU GPL v3.0**. A copy of the license is at
  [`untis-intern/LICENSE-GPL-3.0.txt`](untis-intern/LICENSE-GPL-3.0.txt). These
  files describe undocumented endpoints and are covered by that project's
  license, **not** the repository's CC BY 4.0.
- Everything else in this repository (prose docs, examples, samples) is
  licensed [CC BY 4.0](../LICENSE); see [`../NOTICE.md`](../NOTICE.md) for the
  full breakdown.

## The official JSON-RPC PDF

Untis authored a PDF titled *WebUntis JSON-RPC API* (dated 2018-09-20) that
specifies the public `jsonrpc.do` methods. It is redistributable only by Untis,
so it is **not** committed to this repository. Its full method set is reproduced
in prose in [`docs/04-jsonrpc-public.md`](../docs/04-jsonrpc-public.md), so this
repository remains self-sufficient without it.

If you want the original PDF locally, drop it in `specs/reference/` — that path
is gitignored, so it stays on your machine and never gets published. It is
available from the community mirror at
`git.dergrimm.net/dergrimm/untis.rs` (the earlier `untis-sr.ch` mirror is
offline), or directly from Untis GmbH on request.

## Adding a spec

When you add a machine-readable spec, place it here, keep its original license
and attribution alongside it, note it in the table above, and link it from the
relevant page in [`docs/`](../docs).
