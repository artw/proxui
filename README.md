# proxui

Web UI and REST API for ProxySQL administration. The data model is
code-generated from ProxySQL's C header, the UI is a zero-build-step
SPA (Alpine.js + Pico CSS + CodeMirror + uPlot), and the backend is
FastAPI connecting to ProxySQL's admin port via MySQL protocol.

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
make                  # create venv, install deps, generate code from C header
make test-up          # start MySQL + PostgreSQL + ProxySQL in podman
make test-run         # build container + run proxui on the same network
# open http://localhost:8080       → web UI (dashboard)
# open http://localhost:8080/api/docs → Swagger API docs
```

Only the admin connection needs configuration — proxy ports, backend servers,
and credentials are auto-discovered from ProxySQL's own state at runtime.

## Features

### Dashboard (`#dashboard`)
- Live-updating stats charts (uPlot) — connections, QPS, connection pool, memory
- Config sync status bar — grouped by MySQL / PgSQL / Admin
- Click a module to see memory↔runtime diff, with Load to Runtime / Save to Disk actions
- Command counters and top query digests with adjustable row limits (10/25/50/100/All)
- Background polling (5s interval), persists across tab switches, pause/resume button

### Tables (`#tables/mysql_servers`)
- Sidebar with categorized tables (MySQL, PgSQL, Config, ProxySQL, Runtime, Stats)
- Resizable sidebar, fuzzy search filter
- Sortable data table with per-column filter (funnel icon → floating filter popup)
- Adjustable row limit (10/25/50/100/All)
- Full CRUD: create/edit via modal, inline delete with confirmation
- Password fields blurred by default (click to reveal), `type=password` in forms
- Human-readable display names and descriptions

### Query (`#query`)
- CodeMirror 5 SQL editor with syntax highlighting (MySQL/PostgreSQL modes)
- Tab completion with fuzzy matching against live schema
- Target selector with brand icons — ProxySQL admin, MySQL proxy, PgSQL proxy, all backends
- Database selector populated from target
- Schema tree sidebar — databases → tables → columns, click to insert at cursor
- Results in sortable table with timing info

### General
- Dark/light theme toggle (persisted via Pico CSS `data-theme`)
- URL hash routing (`#dashboard`, `#tables/mysql_servers`, `#query`) — survives refresh
- Phosphor Icons (bold weight) throughout
- MySQL/PostgreSQL brand SVG logos from Simple Icons
- Zero build tooling — all from CDN + static files

## Code generation

`gen_fastapi_models.py` parses `ProxySQL_Admin_Tables_Definitions.h` and generates:

| File | Contents |
|------|----------|
| `models.py` | Pydantic models (read + create/update per writable table) |
| `crud_router.py` | FastAPI router (CRUD for config, GET-only for runtime/stats) |
| `table_metadata.py` | Column metadata dict for UI introspection |
| `db.py` | aiomysql connection pool |
| `app.py` | FastAPI app with API endpoints, config sync, query engine, schema browser, static UI mount |

Config tables get full CRUD. Runtime/stats tables are read-only.
Composite PKs become path parameters (e.g. `/mysql_servers/{hg}/{host}/{port}`).
Tables not present in the running ProxySQL instance are filtered out at runtime.

## Files

```
proxui/
├── gen_fastapi_models.py       # code generator
├── Containerfile               # podman image build
├── Makefile                    # build, run, test targets
├── requirements.txt            # python deps
├── ui/                         # web UI (hand-crafted)
│   ├── index.html
│   ├── app.js
│   ├── app.css
│   └── icons/                  # MySQL/PgSQL SVG logos
├── generated/                  # auto-generated — do not edit
│   ├── app.py
│   ├── crud_router.py
│   ├── db.py
│   ├── models.py
│   └── table_metadata.py
└── test/
    ├── bench.sh                # podman test bench
    ├── proxysql.cnf
    └── smoke_test.sh           # 20-point API smoke test
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
| `PROXYSQL_ADMIN_PORT` | `16032` | ProxySQL admin port |
| `PROXYSQL_ADMIN_USER` | `radmin` | Admin username (remote-capable) |
| `PROXYSQL_ADMIN_PASS` | `radmin` | Admin password |
| `PROXYSQL_SRC` | `~/src/proxysql` | ProxySQL source tree (for codegen) |

## Test bench

```bash
test/bench.sh up       # MySQL 8.4 + PostgreSQL 17 + ProxySQL 3.0
test/bench.sh run      # build + run proxui container on same network
test/bench.sh down     # tear down everything
test/bench.sh status   # show container status
```

Seeds ProxySQL with MySQL and PostgreSQL backends, remote admin credentials,
and a sample PostgreSQL table. Auto-detects distrobox and uses
`distrobox-host-exec podman`.

## Regenerating

```bash
cd ~/src/proxysql && git pull
cd ~/sync/code/proxui && make generate
```

Re-reads the header and overwrites `generated/`. Never hand-edit those files.
