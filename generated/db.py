"""
Database helpers for connecting to the ProxySQL admin interface.

Uses aiomysql to talk to the admin port (default 6032).
Configure via environment variables:
    PROXYSQL_ADMIN_HOST  (default: 127.0.0.1)
    PROXYSQL_ADMIN_PORT  (default: 6032)
    PROXYSQL_ADMIN_USER  (default: admin)
    PROXYSQL_ADMIN_PASS  (default: admin)
"""

from __future__ import annotations

import os
from typing import Any

import aiomysql


_POOL: aiomysql.Pool | None = None


async def get_pool() -> aiomysql.Pool:
    global _POOL
    if _POOL is None:
        _POOL = await aiomysql.create_pool(
            host=os.environ.get("PROXYSQL_ADMIN_HOST", "127.0.0.1"),
            port=int(os.environ.get("PROXYSQL_ADMIN_PORT", "6032")),
            user=os.environ.get("PROXYSQL_ADMIN_USER", "admin"),
            password=os.environ.get("PROXYSQL_ADMIN_PASS", "admin"),
            autocommit=True,
            minsize=1,
            maxsize=5,
        )
    return _POOL


async def get_admin_conn():
    """FastAPI dependency: yields a connection from the pool."""
    pool = await get_pool()
    async with pool.acquire() as conn:
        yield conn


async def execute_query(conn, sql: str, params: list | None = None) -> list[dict[str, Any]]:
    """Execute a SELECT and return rows as list of dicts."""
    async with conn.cursor(aiomysql.DictCursor) as cur:
        await cur.execute(sql, params)
        rows = await cur.fetchall()
    return [dict(r) for r in rows]


async def execute_modify(conn, sql: str, params: list | None = None) -> int:
    """Execute INSERT/UPDATE/DELETE and return affected rows."""
    async with conn.cursor() as cur:
        await cur.execute(sql, params)
        return cur.rowcount
