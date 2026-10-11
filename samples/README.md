# Sample payloads

Illustrative request/response bodies for each API surface, so you can see the
shape of the data **without hitting a real server**. They are hand-built from
the schemas in [`../specs`](../specs) and the docs, using invented names —
**not** captured from a real school.

| File | Surface | Doc |
|---|---|---|
| [`public/authenticate.response.json`](public/authenticate.response.json) | Public JSON-RPC | [04](../docs/04-jsonrpc-public.md) |
| [`public/getKlassen.response.json`](public/getKlassen.response.json) | Public JSON-RPC | [04](../docs/04-jsonrpc-public.md) |
| [`public/getTimetable.response.json`](public/getTimetable.response.json) | Public JSON-RPC | [04](../docs/04-jsonrpc-public.md) |
| [`public/error.response.json`](public/error.response.json) | Public JSON-RPC | [11](../docs/11-conventions.md) |
| [`intern/getUserData2017.response.json`](intern/getUserData2017.response.json) | Intern JSON-RPC | [05](../docs/05-jsonrpc-intern.md) |
| [`intern/getTimetable2017.response.json`](intern/getTimetable2017.response.json) | Intern JSON-RPC | [05](../docs/05-jsonrpc-intern.md) |
| [`view/mobile-data.response.json`](view/mobile-data.response.json) | View REST | [07](../docs/07-rest-view.md) |
| [`extern/v3-timetable.response.json`](extern/v3-timetable.response.json) | Extern Timetable v3 | [09](../docs/09-extern-timetable-v3.md) |
| [`mobile/v2-authentication.response.json`](mobile/v2-authentication.response.json) | Mobile auth v2 | [06](../docs/06-mobile-rest-auth.md) |

> These files are examples of *structure*, not a contract. Fields may be
> omitted when empty (a JSON-RPC quirk), arrays may be empty, and the
> reverse-engineered surfaces can add or rename fields at any time.
