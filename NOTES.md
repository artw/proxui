# proxui — Session Notes

## Current State

v0.1.0 release. All infrastructure complete and validated:
- 68/68 integration tests passing across ProxySQL 2.7.3 and 3.0
- Image published: `quay.io/artw/proxui:latest` (and `:0.1`)
- GitHub: `github.com/artw/proxui`, CI pipeline active (codegen check + quay.io push on master)

## Architecture Snapshot

- **Backend**: FastAPI, code-generated from `ProxySQL_Admin_Tables_Definitions.h`
- **Frontend**: Zero-build SPA — Alpine.js, Pico CSS, CodeMirror, uPlot (all CDN)
- **Auth**: Server-side sessions, HMAC-signed cookie, per-session aiomysql pools
- **Hand-crafted** (despite living in `generated/`): `app.py`, `db.py`
  — excluded from codegen via `--skip app.py db.py`
- **Graceful degradation**: `execute_query` catches "no such table" → returns `[]`
  (pgsql_* tables missing on v2.7 → 200+[] not 500)

## Key Lessons (permanent)

- ProxySQL cnf initializes RUNTIME only; MEMORY starts empty
  → seed.sql must be self-contained (all rows), not just deltas
- `proxysql:2.7` tag doesn't exist on Docker Hub → use `proxysql:2.7.3`
- Bootstrap credential is always `admin:admin`; `radmin:radmin` requires explicit
  `SET admin-admin_credentials` + `LOAD ADMIN VARIABLES TO RUNTIME`

## Next Steps

- Nothing actively in flight
- Set `QUAY_USERNAME` + `QUAY_TOKEN` secrets on GitHub repo for CI image push to work
