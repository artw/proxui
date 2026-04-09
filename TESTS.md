# proxui — Test Stack

## What Exists

### `test/smoke_test.sh`
23-point bash smoke test. Requires a live proxui + ProxySQL instance.

Covers:
- Login / auth check / logout
- GET on key config tables: `mysql_servers`, `mysql_users`, `mysql_query_rules`,
  `global_variables`, `proxysql_servers`, `mysql_replication_hostgroups`,
  `mysql_group_replication_hostgroups`
- Stats tables: `stats_mysql_global`, `stats_mysql_connection_pool`,
  `stats_mysql_query_digest`
- Runtime tables: `runtime_mysql_servers`, `runtime_mysql_users`
- Config sync endpoints: `/sync/status`, `/sync/apply`, `/sync/save`,
  `/sync/discard`
- Query engine: `POST /query`
- Schema browser: `GET /schema/databases`, `GET /schema/tables`

Run: `bash test/smoke_test.sh [http://host:port]`

### `test/bench.sh`
Podman-based test bench. Starts:
- MySQL 8.4 (`proxui-mysql`)
- PostgreSQL 17 (`proxui-pgsql`)
- ProxySQL 3.0 (`proxui-proxysql`) — image: `docker.io/proxysql/proxysql:3.0`

Seeds ProxySQL with MySQL/PgSQL backends, `radmin:radmin` remote admin creds,
and a sample PostgreSQL table.

Commands: `up | down | run | status | logs`

## What Is NOT Tested

- Write operations (POST/PUT/DELETE on config tables) — smoke test is GET-only
- ProxySQL schema versions other than 3.0 (bench pins to `proxysql:3.0`)
- Authentication edge cases (bad credentials, expired sessions, concurrent sessions)
- Config sync correctness (apply/save/discard responses checked but not verified
  against ProxySQL state)
- Frontend / UI logic (no browser tests)
- `gen_fastapi_models.py` parser (no unit tests for codegen)

## Integration Tests: `test/integration_test.sh`

Spins up each supported ProxySQL version, seeds fixtures, tests proxui against it,
then tears down. Run with `just integ`.

Supported versions: **2.7** (latest 2.7.x), **3.0** (latest stable 3.0.x).

### What it tests
- Login / logout
- GET on all common MySQL config, runtime, and stats tables
- CRUD on `mysql_servers` (create, read, delete, verify gone)
- Fixture data verification (≥ expected row counts)
- **Graceful degradation**: on v2.7, pgsql_* endpoints must return 200 (empty),
  not 500 — verifies proxui handles missing tables cleanly
- On v3.0: full pgsql_* table coverage (config, runtime, stats)

### Fixture storage: `test/fixtures/`

```
test/fixtures/
  v2.7/seed.sql    # self-contained mysql seed: hg0+hg10, users, 3 query rules, scheduler
  v3.0/seed.sql    # same + pgsql_servers, pgsql_users, pgsql_query_rules, pgsql_replication
```

- SQL files piped to ProxySQL admin port via mysql client (`admin:admin`)
- REPLACE INTO — idempotent, safe to re-run
- **Self-contained**: ProxySQL loads cnf into RUNTIME only; MEMORY starts empty.
  `LOAD TO RUNTIME` pushes MEMORY → RUNTIME, so seeds include ALL rows (not just extras)
- v2.7 has no pgsql support → no pgsql commands in its seed.sql

### `test/bench.sh` version support

```bash
just bench-up 2.7   # MySQL + ProxySQL 2.7.3 (no pgsql container)
just bench-up 3.0   # MySQL + PostgreSQL + ProxySQL 3.0 (default)
just bench-down
```

Image tag mapping (update when new patch released):
- `2.7` → `docker.io/proxysql/proxysql:2.7.3` (`proxysql:2.7` tag does not exist)
- `3.0` → `docker.io/proxysql/proxysql:3.0`

`admin:admin` is always the bootstrap credential. `radmin:radmin` is set explicitly via
`SET admin-admin_credentials` + `LOAD ADMIN VARIABLES TO RUNTIME` after startup.

### ProxySQL schema versions (reference)

The header `ProxySQL_Admin_Tables_Definitions.h` only exists in v3.0+.
v1.x/v2.x schema is in `lib/ProxySQL_Admin.cpp` via `#define` macros.
Only 7 distinct schema states across all v3.0+ release tags.
proxui is generated from the header — on v2.7, `execute_query` catches "no such table"
errors and returns `[]` so all endpoints respond 200 even for pgsql_* tables.
