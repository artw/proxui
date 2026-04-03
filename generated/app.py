"""
ProxySQL Web UI — FastAPI application.

Run with:
    uvicorn webui.generated.app:app --reload --port 8080
"""

from __future__ import annotations

import base64
import hashlib
import os
import pathlib
import secrets
import time

import aiomysql
import asyncpg
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware

from .crud_router import router as crud_router
from .table_metadata import TABLE_METADATA

# ── Session secret ─────────────────────────────────────────────
_SESSION_SECRET = os.environ.get("PROXUI_SESSION_SECRET", secrets.token_hex(32))
_COOKIE_NAME = "proxui_session"
_PUBLIC_PATHS = {"/api/v1/health", "/api/v1/auth/login", "/api/v1/auth/logout", "/api/v1/auth/check", "/api/docs", "/api/openapi.json"}


def _sign(data: str) -> str:
    sig = hashlib.sha256((_SESSION_SECRET + data).encode()).hexdigest()[:16]
    return base64.b64encode(f"{sig}:{data}".encode()).decode()


def _verify(token: str) -> str | None:
    try:
        raw = base64.b64decode(token).decode()
        sig, data = raw.split(":", 1)
        expected = hashlib.sha256((_SESSION_SECRET + data).encode()).hexdigest()[:16]
        if sig == expected:
            return data
    except Exception:
        pass
    return None


# ── Per-user pool cache ────────────────────────────────────────
_user_pools: dict[str, aiomysql.Pool] = {}


async def _get_user_pool(user: str, password: str) -> aiomysql.Pool:
    key = f"{user}:{password}"
    if key not in _user_pools:
        _user_pools[key] = await aiomysql.create_pool(
            host=os.environ.get("PROXYSQL_ADMIN_HOST", "127.0.0.1"),
            port=int(os.environ.get("PROXYSQL_ADMIN_PORT", "6032")),
            user=user,
            password=password,
            autocommit=True,
            minsize=1,
            maxsize=5,
        )
    return _user_pools[key]


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        # Allow public paths and static UI files
        if path in _PUBLIC_PATHS or not path.startswith("/api/"):
            return await call_next(request)
        # Check session cookie
        token = request.cookies.get(_COOKIE_NAME)
        if not token:
            return JSONResponse({"error": "Not authenticated"}, status_code=401)
        creds = _verify(token)
        if not creds:
            return JSONResponse({"error": "Invalid session"}, status_code=401)
        user, password = creds.split(":", 1)
        try:
            request.state.pool = await _get_user_pool(user, password)
            request.state.user = user
        except Exception as e:
            return JSONResponse({"error": f"Auth failed: {e}"}, status_code=401)
        return await call_next(request)


app = FastAPI(
    title="proxui",
    description="Auto-generated REST API for ProxySQL admin tables",
    version="0.1.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

app.add_middleware(AuthMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(crud_router, prefix="/api/v1")


# ── Auth endpoints ─────────────────────────────────────────────

class LoginRequest(BaseModel):
    username: str
    password: str


@app.post("/api/v1/auth/login")
async def auth_login(req: LoginRequest, response: Response):
    """Validate credentials against ProxySQL and set session cookie."""
    try:
        conn = await aiomysql.connect(
            host=os.environ.get("PROXYSQL_ADMIN_HOST", "127.0.0.1"),
            port=int(os.environ.get("PROXYSQL_ADMIN_PORT", "6032")),
            user=req.username,
            password=req.password,
            autocommit=True,
        )
        conn.close()
    except Exception as e:
        return JSONResponse({"error": f"Login failed: {e}"}, status_code=401)
    token = _sign(f"{req.username}:{req.password}")
    response.set_cookie(
        _COOKIE_NAME, token,
        httponly=True, samesite="strict", max_age=86400,
    )
    return {"ok": True, "user": req.username}


@app.post("/api/v1/auth/logout")
async def auth_logout(response: Response):
    response.delete_cookie(_COOKIE_NAME)
    return {"ok": True}


@app.get("/api/v1/auth/check")
async def auth_check(request: Request):
    token = request.cookies.get(_COOKIE_NAME)
    if not token:
        return JSONResponse({"authenticated": False}, status_code=401)
    creds = _verify(token)
    if not creds:
        return JSONResponse({"authenticated": False}, status_code=401)
    user = creds.split(":", 1)[0]
    return {"authenticated": True, "user": user}


@app.get("/api/v1/health")
async def health():
    return {"status": "ok"}


@app.get("/api/v1/tables")
async def list_tables(request: Request):
    """Return table metadata, filtered to tables that actually exist in ProxySQL."""
    from .db import get_pool
    pool = await get_pool(request)
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SHOW TABLES")
            live = {row[0] for row in await cur.fetchall()}
    # stats tables live in a separate schema; SHOW TABLES may miss them.
    for name in list(TABLE_METADATA.keys()):
        if name.startswith("stats_") and name not in live:
            try:
                async with pool.acquire() as conn:
                    async with conn.cursor() as cur:
                        await cur.execute(f"SELECT 1 FROM {name} LIMIT 0")
                live.add(name)
            except Exception:
                pass
    return {k: v for k, v in TABLE_METADATA.items() if k in live}


# ── Free-form SQL query endpoint ─────────────────────────────────

class QueryRequest(BaseModel):
    sql: str
    target: str = "admin"   # "admin", "proxy" or "backend:<hg>:<host>:<port>"
    database: str = ""      # optional: database/schema to use
    limit: int = 1000


async def _get_var(pool, name: str) -> str:
    async with pool.acquire() as c:
        async with c.cursor() as cur:
            await cur.execute(
                "SELECT variable_value FROM global_variables "
                "WHERE variable_name=%s", [name])
            row = await cur.fetchone()
            return row[0] if row else ""


async def _get_proxy_creds(pool):
    """Return (user, password) for the proxy port from mysql_users."""
    async with pool.acquire() as c:
        async with c.cursor() as cur:
            # Pick first active user with a plaintext password
            await cur.execute(
                "SELECT username, password FROM mysql_users "
                "WHERE active=1 AND password NOT LIKE '*%%' "
                "ORDER BY username LIMIT 1")
            row = await cur.fetchone()
            if row:
                return row[0], row[1]
            # Fallback: any active user (hashed pw won't work)
            await cur.execute(
                "SELECT username, password FROM mysql_users "
                "WHERE active=1 ORDER BY username LIMIT 1")
            row = await cur.fetchone()
            return (row[0], row[1]) if row else (None, None)


async def _adhoc_connect(target: str, database: str | None = None, request: Request | None = None):
    """Return (conn, is_pool_conn, label) for the given target."""
    from .db import get_pool
    pool = await get_pool(request)
    # For PG targets, default to 'postgres' if no db specified
    pg_db = database or "postgres"

    if target == "admin":
        return await pool.acquire(), True, "admin"

    elif target == "proxy":
        ifaces = await _get_var(pool, "mysql-interfaces")
        # Parse first interface: "0.0.0.0:6033" or "0.0.0.0:6033;/tmp/proxysql.sock"
        first = ifaces.split(";")[0].strip()
        if ":" in first:
            bind_host, bind_port = first.rsplit(":", 1)
        else:
            bind_host, bind_port = "127.0.0.1", first
        # Resolve 0.0.0.0 to the admin host we already know
        admin_host = os.environ.get("PROXYSQL_ADMIN_HOST", "127.0.0.1")
        host = admin_host if bind_host in ("0.0.0.0", "::") else bind_host
        user, pw = await _get_proxy_creds(pool)
        if not user:
            raise ValueError("No mysql_users configured — can't connect to proxy")
        conn = await aiomysql.connect(
            host=host, port=int(bind_port), user=user, password=pw,
            autocommit=True)
        return conn, False, f"proxy ({host}:{bind_port} as {user})"

    elif target.startswith("backend:"):
        # target = "backend:<hostgroup_id>:<hostname>:<port>"
        parts = target.split(":", 3)
        if len(parts) < 4:
            raise ValueError(f"Bad target format: {target}")
        _, hg, hostname, port = parts
        # Try mysql_users creds first (plaintext only), then monitor
        user, pw = await _get_proxy_creds(pool)
        errors = []
        if user:
            try:
                conn = await aiomysql.connect(
                    host=hostname, port=int(port), user=user, password=pw,
                    autocommit=True)
                return conn, False, f"{hostname}:{port} (hg{hg}, as {user})"
            except Exception as e:
                errors.append(f"{user}: {e}")
        # Fallback to monitor credentials
        mon_user = await _get_var(pool, "mysql-monitor_username")
        mon_pw = await _get_var(pool, "mysql-monitor_password")
        if mon_user and mon_user != user:
            try:
                conn = await aiomysql.connect(
                    host=hostname, port=int(port), user=mon_user, password=mon_pw,
                    autocommit=True)
                return conn, False, f"{hostname}:{port} (hg{hg}, as {mon_user})"
            except Exception as e:
                errors.append(f"{mon_user}: {e}")
        raise ValueError(
            f"Can't connect to {hostname}:{port} — " + "; ".join(errors)
            if errors else f"No usable credentials for {hostname}:{port}"
        )

    elif target == "pgsql_proxy":
        ifaces = await _get_var(pool, "pgsql-interfaces")
        if not ifaces:
            raise ValueError("pgsql-interfaces not configured")
        first = ifaces.split(";")[0].strip()
        if ":" in first:
            bind_host, bind_port = first.rsplit(":", 1)
        else:
            bind_host, bind_port = "127.0.0.1", first
        admin_host = os.environ.get("PROXYSQL_ADMIN_HOST", "127.0.0.1")
        host = admin_host if bind_host in ("0.0.0.0", "::") else bind_host
        # Get pgsql user creds
        async with pool.acquire() as c:
            async with c.cursor() as cur:
                await cur.execute(
                    "SELECT username, password FROM pgsql_users "
                    "WHERE active=1 AND password NOT LIKE '*%%' "
                    "ORDER BY username LIMIT 1")
                row = await cur.fetchone()
        if not row:
            raise ValueError("No pgsql_users with plaintext password")
        conn = await asyncpg.connect(
            host=host, port=int(bind_port),
            user=row[0], password=row[1], database=pg_db)
        return conn, False, f"pgsql proxy ({host}:{bind_port} as {row[0]})"

    elif target.startswith("pgbackend:"):
        parts = target.split(":", 3)
        if len(parts) < 4:
            raise ValueError(f"Bad target format: {target}")
        _, hg, hostname, port = parts
        # Try pgsql_users creds, then pgsql monitor
        errors = []
        async with pool.acquire() as c:
            async with c.cursor() as cur:
                await cur.execute(
                    "SELECT username, password FROM pgsql_users "
                    "WHERE active=1 AND password NOT LIKE '*%%' "
                    "ORDER BY username LIMIT 1")
                row = await cur.fetchone()
        if row:
            try:
                conn = await asyncpg.connect(
                    host=hostname, port=int(port),
                    user=row[0], password=row[1], database=pg_db)
                return conn, False, f"{hostname}:{port} (pg hg{hg}, as {row[0]})"
            except Exception as e:
                errors.append(f"{row[0]}: {e}")
        mon_user = await _get_var(pool, "pgsql-monitor_username")
        mon_pw = await _get_var(pool, "pgsql-monitor_password")
        if mon_user:
            try:
                conn = await asyncpg.connect(
                    host=hostname, port=int(port),
                    user=mon_user, password=mon_pw, database=pg_db)
                return conn, False, f"{hostname}:{port} (pg hg{hg}, as {mon_user})"
            except Exception as e:
                errors.append(f"{mon_user}: {e}")
        raise ValueError(
            f"Can't connect to PG {hostname}:{port} — " + "; ".join(errors)
            if errors else f"No usable PG credentials for {hostname}:{port}"
        )

    else:
        raise ValueError(f"Unknown target: {target}")


def _is_pg_conn(conn):
    return isinstance(conn, asyncpg.Connection)


async def _run_mysql(conn, sql, limit):
    t0 = time.monotonic()
    async with conn.cursor(aiomysql.DictCursor) as cur:
        await cur.execute(sql)
        desc = cur.description
        if desc:
            rows = await cur.fetchmany(limit)
            columns = [d[0] for d in desc]
            elapsed = time.monotonic() - t0
            return {
                "ok": True, "columns": columns,
                "rows": [dict(r) for r in rows],
                "row_count": len(rows),
                "truncated": len(rows) >= limit,
                "elapsed_ms": round(elapsed * 1000, 2),
            }
        else:
            elapsed = time.monotonic() - t0
            return {
                "ok": True, "columns": [], "rows": [],
                "row_count": cur.rowcount,
                "affected_rows": cur.rowcount,
                "truncated": False,
                "elapsed_ms": round(elapsed * 1000, 2),
            }


async def _run_pg(conn, sql, limit):
    t0 = time.monotonic()
    records = await conn.fetch(sql)
    elapsed = time.monotonic() - t0
    if records:
        cols = list(records[0].keys())
        rows = [dict(r) for r in records[:limit]]
        return {
            "ok": True, "columns": cols,
            "rows": rows,
            "row_count": len(rows),
            "truncated": len(records) > limit,
            "elapsed_ms": round(elapsed * 1000, 2),
        }
    else:
        return {
            "ok": True, "columns": [], "rows": [],
            "row_count": 0,
            "truncated": False,
            "elapsed_ms": round(elapsed * 1000, 2),
        }


@app.post("/api/v1/query")
async def run_query(req: QueryRequest, request: Request):
    """Execute free-form SQL against any target."""
    conn = None
    is_pool_conn = False
    try:
        conn, is_pool_conn, label = await _adhoc_connect(
            req.target, database=req.database or None, request=request)
        sql = req.sql
        # MySQL: USE <db> for non-admin targets
        if req.database and not _is_pg_conn(conn) and req.target != "admin":
            sql = "USE `" + req.database + "`;" + chr(10) + sql
        if _is_pg_conn(conn):
            result = await _run_pg(conn, sql, req.limit)
        else:
            result = await _run_mysql(conn, sql, req.limit)
        result["target"] = label
        return result
    except Exception as e:
        return {"ok": False, "error": str(e), "target": req.target}
    finally:
        if conn:
            if is_pool_conn:
                from .db import get_pool
                pool = await get_pool(request)
                pool.release(conn)
            elif _is_pg_conn(conn):
                await conn.close()
            else:
                conn.close()


# ── Config layer sync ───────────────────────────────────────────

# Module → {memory tables, runtime table prefix, disk tables,
#           load_runtime cmd, save_disk cmd, load_disk cmd}
CONFIG_MODULES = {
    "mysql_servers":    {
        "memory": ["mysql_servers"],
        "runtime": ["runtime_mysql_servers"],
        "disk": ["disk.mysql_servers"],
        "load_runtime": "LOAD MYSQL SERVERS TO RUNTIME",
        "save_disk":    "SAVE MYSQL SERVERS TO DISK",
        "load_disk":    "LOAD MYSQL SERVERS FROM DISK",
    },
    "mysql_users":      {
        "memory": ["mysql_users"],
        "runtime": ["runtime_mysql_users"],
        "disk": ["disk.mysql_users"],
        "load_runtime": "LOAD MYSQL USERS TO RUNTIME",
        "save_disk":    "SAVE MYSQL USERS TO DISK",
        "load_disk":    "LOAD MYSQL USERS FROM DISK",
    },
    "mysql_query_rules": {
        "memory": ["mysql_query_rules"],
        "runtime": ["runtime_mysql_query_rules"],
        "disk": ["disk.mysql_query_rules"],
        "load_runtime": "LOAD MYSQL QUERY RULES TO RUNTIME",
        "save_disk":    "SAVE MYSQL QUERY RULES TO DISK",
        "load_disk":    "LOAD MYSQL QUERY RULES FROM DISK",
    },
    "mysql_variables":  {
        "memory": ["global_variables"],
        "runtime": ["runtime_global_variables"],
        "disk": ["disk.global_variables"],
        "load_runtime": "LOAD MYSQL VARIABLES TO RUNTIME",
        "save_disk":    "SAVE MYSQL VARIABLES TO DISK",
        "load_disk":    "LOAD MYSQL VARIABLES FROM DISK",
    },
    "admin_variables":  {
        "memory": ["global_variables"],
        "runtime": ["runtime_global_variables"],
        "disk": ["disk.global_variables"],
        "load_runtime": "LOAD ADMIN VARIABLES TO RUNTIME",
        "save_disk":    "SAVE ADMIN VARIABLES TO DISK",
        "load_disk":    "LOAD ADMIN VARIABLES FROM DISK",
    },
    "pgsql_servers":    {
        "memory": ["pgsql_servers"],
        "runtime": ["runtime_pgsql_servers"],
        "disk": ["disk.pgsql_servers"],
        "load_runtime": "LOAD PGSQL SERVERS TO RUNTIME",
        "save_disk":    "SAVE PGSQL SERVERS TO DISK",
        "load_disk":    "LOAD PGSQL SERVERS FROM DISK",
    },
    "pgsql_users":      {
        "memory": ["pgsql_users"],
        "runtime": ["runtime_pgsql_users"],
        "disk": ["disk.pgsql_users"],
        "load_runtime": "LOAD PGSQL USERS TO RUNTIME",
        "save_disk":    "SAVE PGSQL USERS TO DISK",
        "load_disk":    "LOAD PGSQL USERS FROM DISK",
    },
    "pgsql_query_rules": {
        "memory": ["pgsql_query_rules"],
        "runtime": ["runtime_pgsql_query_rules"],
        "disk": ["disk.pgsql_query_rules"],
        "load_runtime": "LOAD PGSQL QUERY RULES TO RUNTIME",
        "save_disk":    "SAVE PGSQL QUERY RULES TO DISK",
        "load_disk":    "LOAD PGSQL QUERY RULES FROM DISK",
    },
    "proxysql_servers": {
        "memory": ["proxysql_servers"],
        "runtime": ["runtime_proxysql_servers"],
        "disk": ["disk.proxysql_servers"],
        "load_runtime": "LOAD PROXYSQL SERVERS TO RUNTIME",
        "save_disk":    "SAVE PROXYSQL SERVERS TO DISK",
        "load_disk":    "LOAD PROXYSQL SERVERS FROM DISK",
    },
    "scheduler":        {
        "memory": ["scheduler"],
        "runtime": ["runtime_scheduler"],
        "disk": ["disk.scheduler"],
        "load_runtime": "LOAD SCHEDULER TO RUNTIME",
        "save_disk":    "SAVE SCHEDULER TO DISK",
        "load_disk":    "LOAD SCHEDULER FROM DISK",
    },
}


async def _hash_rows(pool, table: str) -> str:
    """Return a content hash of a table's rows."""
    import hashlib
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(f"SELECT * FROM {table} ORDER BY 1")
            rows = await cur.fetchall()
    raw = str(rows).encode()
    return hashlib.md5(raw).hexdigest()


@app.get("/api/v1/config/status")
async def config_status(request: Request):
    """Compare memory vs runtime vs disk for each config module."""
    from .db import get_pool
    pool = await get_pool(request)
    result = []
    for mod_name, mod in CONFIG_MODULES.items():
        entry = {"module": mod_name, "in_sync": True,
                 "memory_eq_runtime": True, "memory_eq_disk": True}
        try:
            mem_hash = await _hash_rows(pool, mod["memory"][0])
            rt_hash = await _hash_rows(pool, mod["runtime"][0])
            dk_hash = await _hash_rows(pool, mod["disk"][0])
            entry["memory_eq_runtime"] = (mem_hash == rt_hash)
            entry["memory_eq_disk"] = (mem_hash == dk_hash)
            entry["in_sync"] = (mem_hash == rt_hash == dk_hash)
        except Exception as e:
            entry["error"] = str(e)
        result.append(entry)
    return result


class ConfigAction(BaseModel):
    module: str
    action: str   # "load_runtime", "save_disk", "load_disk"


@app.post("/api/v1/config/action")
async def config_action(req: ConfigAction, request: Request):
    """Execute a LOAD/SAVE command for a config module."""
    if req.module not in CONFIG_MODULES:
        return {"ok": False, "error": f"Unknown module: {req.module}"}
    mod = CONFIG_MODULES[req.module]
    if req.action not in ("load_runtime", "save_disk", "load_disk"):
        return {"ok": False, "error": f"Unknown action: {req.action}"}
    cmd = mod[req.action]
    from .db import get_pool
    pool = await get_pool(request)
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(cmd)
        return {"ok": True, "command": cmd}
    except Exception as e:
        return {"ok": False, "error": str(e), "command": cmd}


@app.get("/api/v1/config/diff/{module}")
async def config_diff(module: str, request: Request):
    """Return row-level diff between memory and runtime for a module."""
    if module not in CONFIG_MODULES:
        return {"error": f"Unknown module: {module}"}
    mod = CONFIG_MODULES[module]
    from .db import get_pool
    pool = await get_pool(request)
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(f"SELECT * FROM {mod['memory'][0]} ORDER BY 1")
            mem_rows = [dict(r) for r in await cur.fetchall()]
            await cur.execute(f"SELECT * FROM {mod['runtime'][0]} ORDER BY 1")
            rt_rows = [dict(r) for r in await cur.fetchall()]
    columns = list(mem_rows[0].keys()) if mem_rows else (
              list(rt_rows[0].keys()) if rt_rows else [])
    # Index rows by a string key of all values for comparison
    def row_key(r):
        return "|".join(str(r.get(c, "")) for c in columns)
    mem_set = {row_key(r): r for r in mem_rows}
    rt_set = {row_key(r): r for r in rt_rows}
    diff_rows = []
    all_keys = set(mem_set.keys()) | set(rt_set.keys())
    for k in sorted(all_keys):
        if k in mem_set and k not in rt_set:
            diff_rows.append({"memory": mem_set[k], "runtime": None,
                              "changed_cols": columns})
        elif k not in mem_set and k in rt_set:
            diff_rows.append({"memory": None, "runtime": rt_set[k],
                              "changed_cols": columns})
        # rows with same full key are identical, skip
    # Also check rows that exist in both but differ (same PK, different values)
    # For that we need PK-based comparison
    pk_cols = TABLE_METADATA.get(mod['memory'][0], {}).get('pk_columns', [])
    if pk_cols:
        def pk_key(r):
            return "|".join(str(r.get(c, "")) for c in pk_cols)
        mem_by_pk = {pk_key(r): r for r in mem_rows}
        rt_by_pk = {pk_key(r): r for r in rt_rows}
        for pk in set(mem_by_pk.keys()) & set(rt_by_pk.keys()):
            mr, rr = mem_by_pk[pk], rt_by_pk[pk]
            changed = [c for c in columns if str(mr.get(c, "")) != str(rr.get(c, ""))]
            if changed:
                diff_rows.append({"memory": mr, "runtime": rr,
                                  "changed_cols": changed})
    return {"columns": columns, "diff_rows": diff_rows,
            "memory_count": len(mem_rows), "runtime_count": len(rt_rows)}


# ── Schema tree endpoint ─────────────────────────────────────────

async def _schema_admin(pool):
    """Build schema tree for ProxySQL admin (sqlite-backed)."""
    tree = {}
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SHOW DATABASES")
            dbs = [row[1] for row in await cur.fetchall()]
    for db in dbs:
        tables = {}
        try:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(f"SHOW TABLES FROM {db}")
                    tbl_names = [row[0] for row in await cur.fetchall()]
            for tbl in sorted(tbl_names):
                cols = []
                try:
                    async with pool.acquire() as conn:
                        async with conn.cursor() as cur:
                            await cur.execute(f"PRAGMA table_info({tbl})")
                            for r in await cur.fetchall():
                                cols.append({"name": r[1], "type": r[2],
                                             "pk": bool(r[5])})
                except Exception:
                    # stats views: fall back to SELECT LIMIT 0
                    try:
                        async with pool.acquire() as conn:
                            async with conn.cursor() as cur:
                                await cur.execute(f"SELECT * FROM {db}.{tbl} LIMIT 0")
                                cols = [{"name": d[0], "type": "VARCHAR", "pk": False}
                                        for d in (cur.description or [])]
                    except Exception:
                        pass
                tables[tbl] = cols
        except Exception:
            pass
        tree[db] = tables
    return tree


async def _schema_mysql(conn):
    """Build schema tree for a real MySQL server."""
    tree = {}
    cur = await conn.cursor()
    try:
        await cur.execute("SHOW DATABASES")
        dbs = [row[0] for row in await cur.fetchall()]
    except Exception:
        return tree
    for db in dbs:
        if db in ("information_schema", "performance_schema", "sys"):
            continue
        tables = {}
        try:
            await cur.execute(f"SHOW TABLES FROM `{db}`")
            tbl_names = [row[0] for row in await cur.fetchall()]
            for tbl in sorted(tbl_names):
                cols = []
                try:
                    await cur.execute(f"SHOW COLUMNS FROM `{db}`.`{tbl}`")
                    for r in await cur.fetchall():
                        cols.append({"name": r[0], "type": r[1],
                                     "pk": r[3] == "PRI"})
                except Exception:
                    pass
                tables[tbl] = cols
        except Exception:
            pass
        tree[db] = tables
    return tree


async def _schema_pg(conn):
    """Build schema tree for a PostgreSQL server."""
    tree = {}
    rows = await conn.fetch(
        "SELECT schema_name FROM information_schema.schemata "
        "WHERE schema_name NOT IN ('pg_catalog','information_schema','pg_toast') "
        "ORDER BY schema_name")
    for row in rows:
        schema = row['schema_name']
        tables = {}
        try:
            tbl_rows = await conn.fetch(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema=$1 ORDER BY table_name", schema)
            for tr in tbl_rows:
                tbl = tr['table_name']
                cols = []
                try:
                    col_rows = await conn.fetch(
                        "SELECT c.column_name, c.data_type, "
                        "COALESCE(tc.constraint_type='PRIMARY KEY', false) AS is_pk "
                        "FROM information_schema.columns c "
                        "LEFT JOIN information_schema.key_column_usage kcu "
                        "  ON kcu.table_schema=c.table_schema "
                        "  AND kcu.table_name=c.table_name "
                        "  AND kcu.column_name=c.column_name "
                        "LEFT JOIN information_schema.table_constraints tc "
                        "  ON tc.constraint_name=kcu.constraint_name "
                        "  AND tc.table_schema=kcu.table_schema "
                        "  AND tc.constraint_type='PRIMARY KEY' "
                        "WHERE c.table_schema=$1 AND c.table_name=$2 "
                        "ORDER BY c.ordinal_position", schema, tbl)
                    for cr in col_rows:
                        cols.append({"name": cr['column_name'],
                                     "type": cr['data_type'],
                                     "pk": bool(cr['is_pk'])})
                except Exception:
                    pass
                tables[tbl] = cols
        except Exception:
            pass
        tree[schema] = tables
    return tree


@app.get("/api/v1/schema/{target:path}")
async def get_schema(target: str, db: str = "", request: Request = None):
    """Return schema tree {db: {table: [cols]}} for any target."""
    conn = None
    is_pool = False
    try:
        conn, is_pool, label = await _adhoc_connect(
            target, database=db or None, request=request)
        if target == "admin":
            from .db import get_pool as _gp
            pool = await _gp(request)
            pool.release(conn)
            conn = None
            return await _schema_admin(pool)
        elif _is_pg_conn(conn):
            return await _schema_pg(conn)
        else:
            return await _schema_mysql(conn)
    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn:
            if is_pool:
                from .db import get_pool as _gp2
                pool = await _gp2(request)
                pool.release(conn)
            elif _is_pg_conn(conn):
                await conn.close()
            else:
                conn.close()


# ── Database list for a target ──────────────────────────────

@app.get("/api/v1/databases/{target:path}")
async def list_databases(target: str, request: Request = None):
    """List databases for any target."""
    conn = None
    is_pool = False
    try:
        conn, is_pool, _ = await _adhoc_connect(target, request=request)
        if target == "admin":
            from .db import get_pool as _gp
            pool = await _gp(request)
            pool.release(conn)
            conn = None
            async with pool.acquire() as c:
                async with c.cursor() as cur:
                    await cur.execute("SHOW DATABASES")
                    return [row[1] for row in await cur.fetchall()]
        elif _is_pg_conn(conn):
            rows = await conn.fetch(
                "SELECT datname FROM pg_database "
                "WHERE datistemplate=false ORDER BY datname")
            return [r['datname'] for r in rows]
        else:
            async with conn.cursor() as cur:
                await cur.execute("SHOW DATABASES")
                return [r[0] for r in await cur.fetchall()
                        if r[0] not in ('information_schema',
                                        'performance_schema', 'sys')]
    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn:
            if is_pool:
                from .db import get_pool as _gp2
                pool = await _gp2(request)
                pool.release(conn)
            elif _is_pg_conn(conn):
                await conn.close()
            else:
                conn.close()


# ── Available query targets (auto-discovered) ──────────────────

@app.get("/api/v1/targets")
async def list_targets(request: Request):
    """Auto-discover query targets from ProxySQL state."""
    from .db import get_pool
    pool = await get_pool(request)

    admin_port = os.environ.get("PROXYSQL_ADMIN_PORT", "6032")
    targets = [{"id": "admin", "label": f"Admin (:{admin_port})",
                "type": "proxysql"}]

    # MySQL proxy interface
    try:
        ifaces = await _get_var(pool, "mysql-interfaces")
        if ifaces:
            first = ifaces.split(";")[0].strip()
            targets.append({"id": "proxy",
                            "label": f"MySQL Proxy ({first})",
                            "type": "mysql"})
    except Exception:
        pass

    # PostgreSQL proxy interface
    try:
        ifaces = await _get_var(pool, "pgsql-interfaces")
        if ifaces:
            first = ifaces.split(";")[0].strip()
            targets.append({"id": "pgsql_proxy",
                            "label": f"PgSQL Proxy ({first})",
                            "type": "postgresql"})
    except Exception:
        pass

    # MySQL backend servers
    try:
        async with pool.acquire() as c:
            async with c.cursor() as cur:
                await cur.execute(
                    "SELECT hostgroup_id, hostname, port, status "
                    "FROM mysql_servers ORDER BY hostgroup_id, hostname")
                for hg, host, port, status in await cur.fetchall():
                    tid = f"backend:{hg}:{host}:{port}"
                    label = f"{host}:{port} (hg{hg}"
                    if status != "ONLINE":
                        label += f", {status}"
                    label += ")"
                    targets.append({"id": tid, "label": label,
                                    "type": "mysql"})
    except Exception:
        pass

    # PostgreSQL backend servers
    try:
        async with pool.acquire() as c:
            async with c.cursor() as cur:
                await cur.execute(
                    "SELECT hostgroup_id, hostname, port, status "
                    "FROM pgsql_servers ORDER BY hostgroup_id, hostname")
                for hg, host, port, status in await cur.fetchall():
                    tid = f"pgbackend:{hg}:{host}:{port}"
                    label = f"{host}:{port} (hg{hg})"
                    targets.append({"id": tid, "label": label,
                                    "type": "postgresql"})
    except Exception:
        pass

    return targets


# Serve the UI — must be last (catch-all)
_ui_dir = pathlib.Path(__file__).resolve().parent.parent / "ui"
if _ui_dir.is_dir():
    app.mount("/", StaticFiles(directory=str(_ui_dir), html=True), name="ui")
