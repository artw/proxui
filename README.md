# proxui

Web UI and REST API for ProxySQL administration. Data model is
code-generated from ProxySQL's C header. Zero-build-step SPA
(Alpine.js + Pico CSS + CodeMirror + uPlot). FastAPI backend
connects via MySQL protocol to ProxySQL's admin port.

```
┌──────────────┐       ┌────────────────┐       ┌────────────────┐
│   Browser    │─────▶│  proxui :8080  │─────▶│ ProxySQL :6032 │
│   Web UI /   │  REST │  FastAPI       │ MySQL │ admin iface    │
└──────────────┘       └────────────────┘       └────────────────┘
                                                       │
                                           ┌───────────┴───────────┐
                                           ▼                       ▼
                                    ┌────────────┐          ┌────────────┐
                                    │ MySQL      │          │ PostgreSQL │
                                    │ backends   │          │ backends   │
                                    └────────────┘          └────────────┘
```

## Quick start

```bash
make                  # venv + deps + generate code from C header
make test-up          # MySQL + PostgreSQL + ProxySQL in podman
make test-run         # build + run proxui container on same network
# http://localhost:8080       → web UI (login with radmin/radmin)
# http://localhost:8080/api/docs → Swagger
```

Only the admin connection needs configuration — proxy ports, backend
servers, and credentials are auto-discovered from ProxySQL state.

## Features

### Authentication
- Login with ProxySQL admin credentials (any user on the admin port)
- Server-side sessions — cookie contains HMAC-signed session ID only
  (no credentials in cookie)
- Per-session connection pools, cleaned up on logout
- All `/api/` routes require authentication
- Audit logging: login, SQL queries, config actions

### Tables (`#tables/mysql_servers`)
- Categorized sidebar: MySQL, PostgreSQL, ClickHouse, ProxySQL, Stats
- Runtime tables hidden (their state shown via inline diffs)
- Empty tables greyed out and sorted to bottom
- Collapsible sidebar with resize handle
- Groups with unapplied changes highlighted in blue

**Data table:**
- Resizable columns (drag header edge, double-click to auto-fit)
- Column sorting: click cycles ascending → descending → reset
- Per-column filter (funnel icon → floating filter popup)
- Row limit selector at bottom (10/25/50/100/All)
- Inline cell editing (double-click to edit, Enter to save)
- Strike-through delete with 3-second undo window
- Password fields blurred by default

**Config sync (Apply / Save / Discard):**
- Three-layer model: `DISK ↔ MEMORY ↔ RUNTIME`
- **Apply** — push memory → runtime (`LOAD TO RUNTIME`)
- **Save** — persist memory → disk (`SAVE TO DISK`)
- **Discard** — revert memory to runtime (`SAVE FROM RUNTIME`)
- Buttons solid when action needed, outline+disabled when in sync
- Inline row diffs: toggle Diff to see memory vs runtime side-by-side
  with git-style indicators (`+` new, `~` changed, `−` deleted)
- Bottom bar shows "Unapplied changes" or "Unsaved to disk"
  with clickable pills to navigate to affected tables

### Dashboard (`#dashboard`)
- Live stats charts (uPlot): connections, QPS, connection pool, memory
- Command counters and top query digests (adjustable row limits)
- Polls every 5s in background, keeps 120-point rolling window (10 min)
- Pause/resume button in nav bar
- Charts persist across tab switches

### Query Console (`#query`)
- CodeMirror 5 SQL editor with syntax highlighting
- Fuzzy tab completion against live schema
- Target selector: admin, MySQL proxy, PgSQL proxy, all backends
- Database selector populated from target
- Schema tree sidebar: databases → tables → columns
- Sortable results table with row count and timing

### General
- Dark/light theme toggle
- URL hash routing — survives refresh
- Phosphor Icons (bold) + MySQL/PostgreSQL SVG logos
- Monospace font throughout
- Zero build tooling — all CDN + static files

## Code generation

`gen_fastapi_models.py` parses `ProxySQL_Admin_Tables_Definitions.h`:

| Generated file | Contents |
|----------------|----------|
| `models.py` | Pydantic models (read + create/update per writable table) |
| `crud_router.py` | FastAPI router (CRUD for config, GET-only for runtime/stats) |
| `table_metadata.py` | Column metadata dict for UI introspection |
| `db.py` | aiomysql connection pool with per-session support |
| `app.py` | FastAPI app: auth, config sync, query engine, schema browser |

Config tables get full CRUD. Runtime/stats are read-only.
Composite PKs become path params (`/mysql_servers/{hg}/{host}/{port}`).
Tables not present in the running instance are filtered at runtime.

## Security

- **No credentials in cookies** — server-side session store, cookie
  contains only HMAC-signed random session ID
- **No CORS** — UI served same-origin, no cross-origin access
- **Database name sanitization** — regex whitelist before SQL interpolation
- **Audit logging** — login, queries (user + target + SQL[:200]),
  config actions logged at INFO level
- **Session cleanup** — pool closed and session removed on logout
- **Sessions invalidated on restart** — secret regenerates unless
  `PROXUI_SESSION_SECRET` is set

## Files

```
proxui/
├── gen_fastapi_models.py       # code generator
├── Containerfile               # podman image
├── Makefile                    # build / run / test
├── requirements.txt
├── ui/                         # web UI (hand-crafted)
│   ├── index.html              # Alpine.js SPA
│   ├── app.js                  # ~1350 lines
│   ├── app.css                 # ~870 lines
│   └── icons/                  # MySQL/PostgreSQL SVG logos
├── generated/                  # auto-generated — do not edit
│   ├── app.py                  # FastAPI app (~1000 lines)
│   ├── crud_router.py          # ~2400 routes
│   ├── db.py                   # connection pool
│   ├── models.py               # ~2300 Pydantic models
│   └── table_metadata.py       # ~2100 table defs
└── test/
    ├── bench.sh                # podman test bench
    ├── proxysql.cnf
    └── smoke_test.sh           # 23-point test suite
```

## Makefile targets

| Target | Description |
|--------|-------------|
| `make` | Set up venv + deps + codegen |
| `make run` | Start server (`HOST:PORT`, default `127.0.0.1:8080`) |
| `make dev` | Start with `--reload` |
| `make generate` | Regenerate from C header |
| `make test-up` | Start MySQL + PostgreSQL + ProxySQL containers |
| `make test-run` | Build + start bench + run proxui in container |
| `make test-down` | Stop and remove all containers |
| `make test-status` | Show container status |
| `make test-logs` | Tail proxui container logs |
| `make clean` | Remove venv and pycache |

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `127.0.0.1` | Uvicorn bind address |
| `PORT` | `8080` | Uvicorn bind port |
| `PROXYSQL_ADMIN_HOST` | `127.0.0.1` | ProxySQL admin host |
| `PROXYSQL_ADMIN_PORT` | `6032` | ProxySQL admin port |
| `PROXUI_SESSION_SECRET` | *(random)* | HMAC key for session cookies |
| `PROXYSQL_SRC` | `~/src/proxysql` | ProxySQL source tree (for codegen) |

No admin username/password env vars — credentials are provided at
login and stored server-side per session.

## Test bench

```bash
test/bench.sh up       # MySQL 8.4 + PostgreSQL 17 + ProxySQL 3.0
test/bench.sh run      # build + run proxui container on same network
test/bench.sh down     # tear down everything
test/bench.sh status   # container status
```

Seeds ProxySQL with MySQL and PostgreSQL backends, remote admin
credentials (`radmin:radmin`), and a sample PostgreSQL table.
Auto-detects distrobox and uses `distrobox-host-exec podman`.

## Config layer model

```
  DISK  ←── Save ───  MEMORY  ─── Apply ──→  RUNTIME
              │                       ↑
              │        Discard ───────┘
              │
              └── (load_disk: MEMORY ← DISK, available via API)
```

- **MEMORY** — the config tables you edit in the UI
- **RUNTIME** — what ProxySQL is actively using right now
- **DISK** — persisted to SQLite, survives restart
- Users tables always show diffs (ProxySQL splits/hashes at runtime)

## Regenerating

```bash
cd ~/src/proxysql && git pull
cd ~/sync/code/proxui && make generate
```

Overwrites `generated/`. Never hand-edit those files.
