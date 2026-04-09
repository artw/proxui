# proxui — Session Notes

## Current State

Integration test infrastructure complete and validated. 68/68 passing across both
supported ProxySQL versions (2.7.3 and 3.0).

## What Was Built This Session

### Build system
- Replaced `Makefile` with `justfile` (consistent with brood/huski)

### Integration test infrastructure
- `test/bench.sh up [VERSION]` — parameterized by ProxySQL version
  - `2.7` → image `proxysql:2.7.3`, MySQL only, no pgsql
  - `3.0` → image `proxysql:3.0`, MySQL + PostgreSQL
  - Explicitly sets `admin-admin_credentials` + `LOAD ADMIN VARIABLES TO RUNTIME`
    (cnf alone doesn't activate radmin at runtime on some ProxySQL versions)
  - Pipes `test/fixtures/v{VERSION}/seed.sql` via `admin:admin` after startup
- `test/fixtures/v2.7/seed.sql` — fully self-contained MySQL seed (hg0+hg10, rules 1-3)
- `test/fixtures/v3.0/seed.sql` — same + full pgsql seed
  - Seeds are self-contained: ProxySQL loads cnf into RUNTIME only, MEMORY starts empty;
    seed.sql populates MEMORY then LOAD TO RUNTIME makes them consistent
- `test/integration_test.sh` — runs v2.7 then v3.0 sequentially:
  - bench up → seed → proxui on host → login → all table GET checks → CRUD → row count checks → logout → bench down
  - v2.7: pgsql_* endpoints return 200+[] (graceful degradation, not 500)
- `generated/db.py` — `execute_query` catches "no such table" → returns `[]`
- `gen_fastapi_models.py` — added `--skip` flag; justfile uses `--skip app.py db.py`
  to prevent codegen from overwriting hand-crafted files

### Key lessons
- ProxySQL cnf initializes RUNTIME, not MEMORY — seed.sql must be self-contained
- `proxysql:2.7` tag doesn't exist on Docker Hub; use `proxysql:2.7.3`
- `admin:admin` is the reliable bootstrap credential for wait loops and setup SQL

## Next Steps

- Nothing actively in flight
