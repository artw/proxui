# proxui — Architecture

## Overview

Web UI + REST API for ProxySQL administration. Backend is code-generated from
ProxySQL's C header; frontend is a zero-build SPA.

```
Browser ──REST──▶ FastAPI :8080 ──MySQL──▶ ProxySQL :6032 admin port
                   (generated/)                │
                   ui/ (static)          MySQL / PgSQL backends
```

## Key Design Decisions

- **Codegen-first**: `gen_fastapi_models.py` parses
  `ProxySQL_Admin_Tables_Definitions.h` from `~/src/proxysql` and emits all
  backend Python. Never hand-edit `generated/`.
- **Schema-version-aware**: the header changes per ProxySQL release.
  `just generate` regenerates from whatever tag is checked out in `~/src/proxysql`.
- **Auth**: server-side sessions; cookie holds HMAC-signed session ID only.
  Per-session aiomysql connection pools to ProxySQL admin port.
- **No build step**: UI uses Alpine.js, Pico CSS, CodeMirror, uPlot from CDN.

## Package Map

```
proxui/
├── gen_fastapi_models.py   # parser + code emitter (source of truth)
├── Containerfile           # podman image
├── justfile
├── requirements.txt        # fastapi, uvicorn, aiomysql, pydantic
├── ui/
│   ├── index.html          # Alpine.js SPA shell
│   ├── app.js              # ~1350 lines — all UI logic
│   ├── app.css             # ~870 lines
│   └── icons/              # MySQL/PgSQL SVGs
└── generated/
    ├── app.py              # HAND-CRAFTED — auth, sessions, config sync, query engine
    ├── db.py               # HAND-CRAFTED — per-session aiomysql pools, error handling
    ├── crud_router.py      # generated — ~2400 routes (CRUD config, GET-only stats/runtime)
    ├── models.py           # generated — Pydantic models (Base + Create/Update per table)
    └── table_metadata.py   # generated — column metadata dict for UI introspection
```

`just generate` passes `--skip app.py db.py` — codegen never overwrites the hand-crafted files.

## Codegen Pipeline

1. `read_header()` — load + resolve backslash continuations
2. `extract_defines()` — collect all `#define` macros
3. `resolve_defines()` — follow alias chains to final `CREATE TABLE` SQL
4. Parse each table: columns, types, constraints, PKs, writable vs read-only
5. Emit `models.py`, `crud_router.py`, `table_metadata.py` (skips `app.py`, `db.py`)

Config tables → full CRUD. `stats_*` / `runtime_*` → GET-only.
Composite PKs → path params (e.g. `/mysql_servers/{hg}/{host}/{port}`).
`execute_query` catches "no such table" → returns `[]` (graceful degradation for version mismatches).

## ProxySQL Schema Versioning

The header (`ProxySQL_Admin_Tables_Definitions.h`) only exists in v3.0+.
v1.x/v2.x define schemas via `#define` macros in `lib/ProxySQL_Admin.cpp`.

Unique schema states across all v3.0+ release tags (by header SHA-256 prefix):

| Hash prefix   | Tags                              | Tables |
|---------------|-----------------------------------|--------|
| `69b54ba3e41d`| v3.0.0-alpha                      | 141    |
| `535bb3529dba`| v3.0.1                            | 142    |
| `3067f76adbd9`| v3.0.2                            | 143    |
| `8bfd4dce8f3e`| v3.0.3                            | 144    |
| `8713c542cb80`| v3.0.4, v3.0.5                    | 144    |
| `fb0bda61a562`| v3.0.6, v3.1.6, v4.0.6           | 163    |
| `afc832bbc6d1`| v3.0.7, v3.0.8, v3.1.7, v4.0.7  | 165    |

Many tags share the same schema — only 7 distinct fixture sets needed for all
current v3.0+ releases.

## Config Layer Model

```
  DISK  ←─ Save ──  MEMORY  ── Apply ──▶  RUNTIME
              │                    ↑
              └──── Discard ───────┘
```

- MEMORY: config tables you edit in the UI
- RUNTIME: what ProxySQL is actively using
- DISK: persisted to SQLite, survives restart

## Auth / Session Flow

1. POST `/api/v1/auth/login` → credentials validated against ProxySQL admin port
2. Server creates session: stores credentials + aiomysql pool, returns HMAC-signed cookie
3. All `/api/` routes → session middleware looks up pool, executes queries
4. POST `/api/v1/auth/logout` → pool closed, session deleted
