"""
Database helpers for connecting to the ProxySQL admin interface.

Uses per-user connection pools created by the auth middleware.
Falls back to env-var based pool if no request context.
"""

from __future__ import annotations

import os
from typing import Any

import aiomysql
from fastapi import Request


_FALLBACK_POOL: aiomysql.Pool | None = None


async def _get_fallback_pool() -> aiomysql.Pool:
    global _FALLBACK_POOL
    if _FALLBACK_POOL is None:
        _FALLBACK_POOL = await aiomysql.create_pool(
            host=os.environ.get("PROXYSQL_ADMIN_HOST", "127.0.0.1"),
            port=int(os.environ.get("PROXYSQL_ADMIN_PORT", "6032")),
            user=os.environ.get("PROXYSQL_ADMIN_USER", "admin"),
            password=os.environ.get("PROXYSQL_ADMIN_PASS", "admin"),
            autocommit=True,
            minsize=1,
            maxsize=5,
        )
    return _FALLBACK_POOL


async def get_pool(request: Request | None = None) -> aiomysql.Pool:
    """Return the user's pool from request state, or fallback pool."""
    if request and hasattr(request.state, 'pool'):
        return request.state.pool
    return await _get_fallback_pool()


async def get_admin_conn(request: Request):
    """FastAPI dependency: yields a connection from the user's pool."""
    pool = await get_pool(request)
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
