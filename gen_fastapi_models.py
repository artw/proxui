#!/usr/bin/env python3
"""
Generate Pydantic models + FastAPI routers from ProxySQL's
ProxySQL_Admin_Tables_Definitions.h

Usage:
    python3 tools/gen_fastapi_models.py [--header include/ProxySQL_Admin_Tables_Definitions.h] [--outdir webui/generated]

The script:
  1. Preprocesses the header (resolves line continuations, follows #define aliases)
  2. Extracts only "current" table definitions (final alias targets)
  3. Parses each CREATE TABLE/VIEW into columns, types, constraints, PKs
  4. Emits:
     - models.py          — Pydantic models (Base read model + Create/Update variants)
     - crud_router.py     — FastAPI router with GET/POST/PUT/DELETE per config table,
                            GET-only for stats_*/runtime_* tables
     - table_metadata.py  — Raw table metadata dict for introspection
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import textwrap
from dataclasses import dataclass, field
from pathlib import Path


# ---------------------------------------------------------------------------
# 1. Header preprocessing
# ---------------------------------------------------------------------------

def read_header(path: str) -> str:
    """Read the header, resolve backslash line continuations."""
    with open(path) as f:
        raw = f.read()
    # join continuation lines
    raw = raw.replace("\\\n", "")
    return raw


def extract_defines(header: str) -> dict[str, str]:
    """
    Return {macro_name: value} for every #define in the header.
    Value is the raw string (may be another macro name or a quoted SQL string).
    """
    defs: dict[str, str] = {}
    for m in re.finditer(
        r'^\s*#define\s+(\w+)\s+(.+?)\s*$', header, re.MULTILINE
    ):
        name = m.group(1)
        value = m.group(2).strip()
        defs[name] = value
    return defs


def resolve_defines(defs: dict[str, str]) -> dict[str, str]:
    """
    Follow alias chains:  #define A B  where B is another macro name.
    Returns {name: resolved_sql_string} only for defines whose final value
    is a quoted CREATE TABLE/VIEW string.
    """
    resolved: dict[str, str] = {}
    for name, value in defs.items():
        seen = {name}
        v = value
        # follow aliases (value is just another macro name, no quotes)
        while not v.startswith('"') and v in defs:
            if v in seen:
                break
            seen.add(v)
            v = defs[v]
        if v.startswith('"'):
            # strip outer quotes and concatenate adjacent string literals
            sql = _unquote(v)
            resolved[name] = sql
    return resolved


def _unquote(s: str) -> str:
    """Strip C string literal quoting: "foo" "bar" -> foobar"""
    parts = re.findall(r'"((?:[^"\\]|\\.)*)"', s)
    return "".join(parts)


# ---------------------------------------------------------------------------
# 2. Filter to "current" definitions only
# ---------------------------------------------------------------------------

# We want definitions that look like:
#   ADMIN_SQLITE_TABLE_MYSQL_SERVERS         (not versioned _V1_1_0)
#   STATS_SQLITE_TABLE_MYSQL_*
#   ADMIN_SQLITE_RUNTIME_*
#   ADMIN_SQLITE_TABLE_RUNTIME_*
# but NOT the versioned variants (they're only kept for upgrade code).

_VERSION_SUFFIX = re.compile(r'_[Vv]\d+(_\d+)*[a-z]?$')


def is_current_table(macro_name: str, all_defs: dict[str, str]) -> bool:
    """Return True if this macro represents a current (non-versioned) table."""
    # Skip include guard
    if macro_name == "ProxySQL_Admin_Tables_Definitions":
        return False
    # Skip versioned definitions — they're only for upgrade paths
    if _VERSION_SUFFIX.search(macro_name):
        return False
    # Skip if this macro is an alias target that is also referenced by
    # a non-versioned alias (the alias itself is the canonical one)
    # i.e. we keep aliases, skip their versioned targets
    # Actually: alias macros point TO versioned targets, so the alias
    # passes this filter and the versioned target is already filtered above.
    # But we also need to skip macros whose resolved SQL is already
    # covered by another alias — handled via dedup in main().
    # Must start with one of the known prefixes
    prefixes = (
        "ADMIN_SQLITE_TABLE_",
        "ADMIN_SQLITE_RUNTIME_",
        "STATS_SQLITE_TABLE_",
    )
    return any(macro_name.startswith(p) for p in prefixes)


# ---------------------------------------------------------------------------
# 3. SQL DDL parser
# ---------------------------------------------------------------------------

@dataclass
class Column:
    name: str
    raw_type: str  # e.g. "INT", "VARCHAR", "INTEGER", "INT UNSIGNED", "BIGINT"
    nullable: bool  # True if NULL is allowed
    default: str | None  # raw default value or None
    autoincrement: bool
    is_pk_inline: bool  # column-level PRIMARY KEY
    check_expr: str | None  # raw CHECK expression
    check_in_values: list[str] | None  # extracted IN(...) values from CHECK

    @property
    def python_type(self) -> str:
        t = self.raw_type.upper().replace("UNSIGNED", "").strip()
        if t in ("INT", "INTEGER", "BIGINT"):
            return "int"
        if t in ("DOUBLE", "FLOAT", "REAL"):
            return "float"
        return "str"

    @property
    def python_type_annotation(self) -> str:
        base = self.python_type
        if self.nullable:
            return f"Optional[{base}]"
        return base


@dataclass
class TableDef:
    macro_name: str
    table_name: str
    columns: list[Column]
    pk_columns: list[str]  # from table-level PRIMARY KEY(...)
    unique_constraints: list[list[str]]
    is_view: bool = False
    view_sql: str | None = None

    @property
    def is_stats(self) -> bool:
        return self.table_name.startswith("stats_")

    @property
    def is_runtime(self) -> bool:
        return self.table_name.startswith("runtime_")

    @property
    def is_readonly(self) -> bool:
        return self.is_stats or self.is_runtime or self.is_view

    @property
    def model_class_name(self) -> str:
        """Convert table_name to PascalCase model name."""
        parts = self.table_name.split("_")
        return "".join(p.capitalize() for p in parts)

    @property
    def all_pk_columns(self) -> list[str]:
        """Merged PK: table-level PK + any inline PRIMARY KEY columns."""
        pks = list(self.pk_columns)
        for c in self.columns:
            if c.is_pk_inline and c.name not in pks:
                pks.append(c.name)
        return pks


def parse_create_table(sql: str, macro_name: str) -> TableDef:
    """Parse a CREATE TABLE or CREATE VIEW statement."""
    sql = sql.strip().rstrip(")")

    # Handle VIEW
    view_match = re.match(
        r"CREATE\s+VIEW\s+(\w+)\s+AS\s+(.*)", sql, re.IGNORECASE | re.DOTALL
    )
    if view_match:
        table_name = view_match.group(1)
        view_sql = view_match.group(2).strip()
        # Parse SELECT columns from the view alias list
        columns = _parse_view_columns(view_sql)
        return TableDef(
            macro_name=macro_name,
            table_name=table_name,
            columns=columns,
            pk_columns=[],
            unique_constraints=[],
            is_view=True,
            view_sql=view_sql,
        )

    # CREATE TABLE table_name ( ... )
    m = re.match(
        r"CREATE\s+TABLE\s+(\w+)\s*\((.*)", sql, re.IGNORECASE | re.DOTALL
    )
    if not m:
        raise ValueError(f"Cannot parse: {sql[:80]}...")

    table_name = m.group(1)
    body = m.group(2).strip()

    columns: list[Column] = []
    pk_columns: list[str] = []
    unique_constraints: list[list[str]] = []

    for part in _split_column_defs(body):
        part = part.strip()
        if not part:
            continue

        # Table-level PRIMARY KEY
        pk_match = re.match(
            r"PRIMARY\s+KEY\s*\(([^)]+)\)", part, re.IGNORECASE
        )
        if pk_match:
            pk_columns = [
                c.strip().strip("`'\"") for c in pk_match.group(1).split(",")
            ]
            continue

        # Table-level UNIQUE
        uniq_match = re.match(
            r"UNIQUE\s*\(([^)]+)\)", part, re.IGNORECASE
        )
        if uniq_match:
            cols = [
                c.strip().strip("`'\"") for c in uniq_match.group(1).split(",")
            ]
            unique_constraints.append(cols)
            continue

        # Column definition
        col = _parse_column(part)
        if col:
            columns.append(col)

    return TableDef(
        macro_name=macro_name,
        table_name=table_name,
        columns=columns,
        pk_columns=pk_columns,
        unique_constraints=unique_constraints,
    )


def _split_column_defs(body: str) -> list[str]:
    """
    Split column/constraint definitions by comma, respecting parenthesised
    expressions (CHECK, PRIMARY KEY, etc.).
    """
    parts: list[str] = []
    depth = 0
    current: list[str] = []
    for ch in body:
        if ch == "(":
            depth += 1
            current.append(ch)
        elif ch == ")":
            depth -= 1
            current.append(ch)
        elif ch == "," and depth == 0:
            parts.append("".join(current))
            current = []
        else:
            current.append(ch)
    if current:
        parts.append("".join(current))
    return parts


def _parse_column(part: str) -> Column | None:
    """Parse a single column definition string."""
    part = part.strip()
    if not part:
        return None

    # Extract and remove CHECK(...)
    check_expr = None
    check_in_values = None

    # We need to handle nested parens in CHECK
    check_match = _extract_check(part)
    if check_match:
        check_expr = check_match
        # Try to extract IN values
        in_match = re.search(
            r"\b\w+\s+IN\s*\(([^)]+)\)", check_expr, re.IGNORECASE
        )
        if in_match:
            vals = [v.strip().strip("'\"") for v in in_match.group(1).split(",")]
            check_in_values = vals
        # Remove CHECK from part for further parsing
        part = _remove_check(part)

    # Extract name and type
    # Column name may be backtick-quoted
    col_match = re.match(r"(`[^`]+`|\w+)\s+(.*)", part.strip())
    if not col_match:
        return None

    name = col_match.group(1).strip("`")
    rest = col_match.group(2).strip()

    # Parse type — first word(s) that look like a type
    type_match = re.match(
        r"(INTEGER|INT\s+UNSIGNED|INT|BIGINT|VARCHAR|TEXT|DOUBLE|FLOAT|REAL)\b",
        rest,
        re.IGNORECASE,
    )
    raw_type = type_match.group(1) if type_match else "VARCHAR"
    if type_match:
        rest = rest[type_match.end():].strip()

    # AUTOINCREMENT
    autoincrement = bool(re.search(r"\bAUTOINCREMENT\b", rest, re.IGNORECASE))

    # PRIMARY KEY (inline)
    is_pk = bool(re.search(r"\bPRIMARY\s+KEY\b", rest, re.IGNORECASE))

    # NOT NULL
    not_null = bool(re.search(r"\bNOT\s+NULL\b", rest, re.IGNORECASE))
    nullable = not not_null

    # DEFAULT
    default = None
    def_match = re.search(
        r"\bDEFAULT\s+('(?:[^']*)'|\"(?:[^\"]*)\"|[^\s,)]+)",
        rest,
        re.IGNORECASE,
    )
    if def_match:
        default = def_match.group(1).strip("'\"")

    return Column(
        name=name,
        raw_type=raw_type,
        nullable=nullable,
        default=default,
        autoincrement=autoincrement,
        is_pk_inline=is_pk,
        check_expr=check_expr,
        check_in_values=check_in_values,
    )


def _extract_check(part: str) -> str | None:
    """Extract CHECK(...) expression handling nested parens."""
    m = re.search(r"\bCHECK\s*\(", part, re.IGNORECASE)
    if not m:
        return None
    start = m.end()
    depth = 1
    i = start
    while i < len(part) and depth > 0:
        if part[i] == "(":
            depth += 1
        elif part[i] == ")":
            depth -= 1
        i += 1
    return part[start : i - 1]


def _remove_check(part: str) -> str:
    """Remove CHECK(...) from column definition string."""
    m = re.search(r"\bCHECK\s*\(", part, re.IGNORECASE)
    if not m:
        return part
    check_start = m.start()
    depth = 1
    i = m.end()
    while i < len(part) and depth > 0:
        if part[i] == "(":
            depth += 1
        elif part[i] == ")":
            depth -= 1
        i += 1
    return (part[:check_start] + part[i:]).strip()


def _parse_view_columns(view_sql: str) -> list[Column]:
    """
    Best-effort extraction of column names from a SELECT ... AS ... view.
    """
    # Match SELECT ... FROM
    sel_match = re.match(r"SELECT\s+(.*?)\s+FROM\s+", view_sql, re.IGNORECASE | re.DOTALL)
    if not sel_match:
        return []
    select_list = sel_match.group(1)
    columns = []
    for expr in _split_column_defs(select_list):
        expr = expr.strip()
        if not expr:
            continue
        # "expr AS alias" or just "colname"
        as_match = re.search(r"\bAS\s+(\w+)\s*$", expr, re.IGNORECASE)
        if as_match:
            name = as_match.group(1)
        else:
            name = expr.split(".")[-1].strip()
        columns.append(Column(
            name=name,
            raw_type="VARCHAR",
            nullable=True,
            default=None,
            autoincrement=False,
            is_pk_inline=False,
            check_expr=None,
            check_in_values=None,
        ))
    return columns


# ---------------------------------------------------------------------------
# 4. Code generation
# ---------------------------------------------------------------------------

def gen_models(tables: list[TableDef]) -> str:
    """Generate models.py content."""
    lines = [
        '"""',
        "Auto-generated Pydantic models from ProxySQL_Admin_Tables_Definitions.h",
        "",
        "DO NOT EDIT — regenerate with: python3 tools/gen_fastapi_models.py",
        '"""',
        "",
        "from __future__ import annotations",
        "",
        "from enum import Enum",
        "from typing import Optional",
        "",
        "from pydantic import BaseModel, ConfigDict, Field",
        "",
        "import warnings",
        "warnings.filterwarnings(",
        "    'ignore',",
        "    message='Field name.*shadows an attribute in parent',",
        "    category=UserWarning,",
        ")",
        "",
        "",
    ]

    # Collect enum types for CHECK IN values
    enums_emitted: set[str] = set()

    for t in tables:
        # Emit enums for columns with CHECK IN string values
        for c in t.columns:
            if c.check_in_values and c.python_type == "str":
                enum_name = f"{t.model_class_name}_{c.name}_enum"
                if enum_name not in enums_emitted:
                    enums_emitted.add(enum_name)
                    lines.append(f"class {enum_name}(str, Enum):")
                    for v in c.check_in_values:
                        safe = re.sub(r"[^a-zA-Z0-9_]", "_", v)
                        lines.append(f'    {safe} = "{v}"')
                    lines.append("")
                    lines.append("")

    for t in tables:
        lines.append("")
        lines.append(f"class {t.model_class_name}(BaseModel):")
        lines.append(f'    """Read model for table `{t.table_name}`."""')
        if not t.columns:
            lines.append("    pass")
            lines.append("")
            continue
        # Suppress pydantic warning when a column is named 'schema'
        has_reserved = any(c.name in ('schema', 'model') for c in t.columns)
        if has_reserved:
            lines.append('    model_config = ConfigDict(protected_namespaces=())')
        lines.append("")
        for c in t.columns:
            field_args = _build_field_args(t, c)
            type_ann = c.python_type_annotation
            # Use enum type for CHECK IN string values
            enum_name = f"{t.model_class_name}_{c.name}_enum"
            if c.check_in_values and c.python_type == "str" and enum_name in enums_emitted:
                base_type = enum_name
                type_ann = f"Optional[{base_type}]" if c.nullable else base_type
            lines.append(f"    {c.name}: {type_ann}{field_args}")
        lines.append("")

        # Create model (for writable tables only)
        if not t.is_readonly:
            create_cls = f"{t.model_class_name}Create"
            lines.append("")
            lines.append(f"class {create_cls}(BaseModel):")
            lines.append(f'    """Create/update model for `{t.table_name}`."""')
            lines.append("")
            for c in t.columns:
                # Skip autoincrement PKs from create model
                if c.autoincrement:
                    continue
                field_args = _build_field_args(t, c, for_create=True)
                type_ann = c.python_type_annotation
                enum_name = f"{t.model_class_name}_{c.name}_enum"
                if c.check_in_values and c.python_type == "str" and enum_name in enums_emitted:
                    base_type = enum_name
                    type_ann = f"Optional[{base_type}]" if c.nullable else base_type
                # Make columns with defaults optional in create model
                if c.default is not None and not c.nullable:
                    type_ann = f"Optional[{c.python_type}]"
                    if c.check_in_values and c.python_type == "str" and enum_name in enums_emitted:
                        type_ann = f"Optional[{enum_name}]"
                lines.append(f"    {c.name}: {type_ann}{field_args}")
            lines.append("")

    return "\n".join(lines)


def _build_field_args(t: TableDef, c: Column, for_create: bool = False) -> str:
    """Build the ` = Field(...)` part for a column."""
    args: list[str] = []

    # Default value
    if c.default is not None:
        dv = c.default
        if c.python_type == "int":
            try:
                args.append(f"default={int(dv)}")
            except ValueError:
                args.append(f"default={dv!r}")
        elif c.python_type == "float":
            try:
                args.append(f"default={float(dv)}")
            except ValueError:
                args.append(f"default={dv!r}")
        else:
            args.append(f"default={dv!r}")
    elif c.nullable:
        args.append("default=None")

    # Description: include CHECK constraint
    if c.check_expr:
        safe_expr = c.check_expr.replace('"', '\\"')
        args.append(f'description="CHECK: {safe_expr}"')

    if args:
        return " = Field(" + ", ".join(args) + ")"
    return ""


def gen_crud_router(tables: list[TableDef]) -> str:
    """Generate crud_router.py — FastAPI APIRouter with endpoints."""
    lines = [
        '"""',
        "Auto-generated FastAPI CRUD router from ProxySQL_Admin_Tables_Definitions.h",
        "",
        "DO NOT EDIT — regenerate with: python3 tools/gen_fastapi_models.py",
        '"""',
        "",
        "from __future__ import annotations",
        "",
        "from typing import Any",
        "",
        "from fastapi import APIRouter, Depends, HTTPException, Query",
        "",
        "from .db import get_admin_conn, execute_query, execute_modify",
        "from .models import (",
    ]

    # Import all models
    for t in tables:
        lines.append(f"    {t.model_class_name},")
        if not t.is_readonly:
            lines.append(f"    {t.model_class_name}Create,")
    lines.append(")")
    lines.append("")
    lines.append("router = APIRouter()")
    lines.append("")

    for t in tables:
        tag = _table_tag(t)
        safe = t.table_name

        # GET list
        lines.append("")
        lines.append(f'@router.get("/{safe}", response_model=list[{t.model_class_name}], tags=["{tag}"])')
        lines.append(f"async def list_{safe}(conn=Depends(get_admin_conn)):")
        lines.append(f'    """List all rows from `{t.table_name}`."""')
        lines.append(f'    return await execute_query(conn, "SELECT * FROM {t.table_name}")')
        lines.append("")

        if t.is_readonly:
            continue

        pk_cols = t.all_pk_columns

        # POST create
        lines.append("")
        lines.append(f'@router.post("/{safe}", response_model=dict[str, str], tags=["{tag}"])')
        lines.append(f"async def create_{safe}(item: {t.model_class_name}Create, conn=Depends(get_admin_conn)):")
        lines.append(f'    """Insert a row into `{t.table_name}`."""')
        lines.append(f"    data = item.model_dump(exclude_none=True)")
        lines.append(f"    cols = ', '.join(data.keys())")
        lines.append(f"    placeholders = ', '.join(['%s'] * len(data))")
        lines.append(f'    sql = f"INSERT INTO {t.table_name} ({{cols}}) VALUES ({{placeholders}})"')
        lines.append(f"    await execute_modify(conn, sql, list(data.values()))")
        lines.append(f'    return {{"status": "ok"}}')
        lines.append("")

        if not pk_cols:
            continue

        # Build PK path
        pk_path_parts = "/".join(f"{{{pk}}}" for pk in pk_cols)
        pk_params = ", ".join(f"{pk}: str" for pk in pk_cols)

        # GET by PK
        lines.append("")
        lines.append(
            f'@router.get("/{safe}/{pk_path_parts}", response_model={t.model_class_name}, tags=["{tag}"])'
        )
        lines.append(f"async def get_{safe}({pk_params}, conn=Depends(get_admin_conn)):")
        lines.append(f'    """Get a single row from `{t.table_name}` by primary key."""')
        where = " AND ".join(f"{pk} = %s" for pk in pk_cols)
        pk_vars = ", ".join(pk_cols)
        lines.append(
            f'    rows = await execute_query(conn, "SELECT * FROM {t.table_name} WHERE {where}", [{pk_vars}])'
        )
        lines.append(f"    if not rows:")
        lines.append(f'        raise HTTPException(status_code=404, detail="Not found")')
        lines.append(f"    return rows[0]")
        lines.append("")

        # DELETE by PK
        lines.append("")
        lines.append(
            f'@router.delete("/{safe}/{pk_path_parts}", response_model=dict[str, str], tags=["{tag}"])'
        )
        lines.append(f"async def delete_{safe}({pk_params}, conn=Depends(get_admin_conn)):")
        lines.append(f'    """Delete a row from `{t.table_name}` by primary key."""')
        lines.append(
            f'    await execute_modify(conn, "DELETE FROM {t.table_name} WHERE {where}", [{pk_vars}])'
        )
        lines.append(f'    return {{"status": "ok"}}')
        lines.append("")

        # PUT (REPLACE) by PK
        lines.append("")
        lines.append(
            f'@router.put("/{safe}/{pk_path_parts}", response_model=dict[str, str], tags=["{tag}"])'
        )
        lines.append(f"async def update_{safe}({pk_params}, item: {t.model_class_name}Create, conn=Depends(get_admin_conn)):")
        lines.append(f'    """Update (REPLACE) a row in `{t.table_name}`."""')
        lines.append(f"    data = item.model_dump(exclude_none=True)")
        # Force PK values from path
        for pk in pk_cols:
            lines.append(f'    data["{pk}"] = {pk}')
        lines.append(f"    cols = ', '.join(data.keys())")
        lines.append(f"    placeholders = ', '.join(['%s'] * len(data))")
        lines.append(f'    sql = f"REPLACE INTO {t.table_name} ({{cols}}) VALUES ({{placeholders}})"')
        lines.append(f"    await execute_modify(conn, sql, list(data.values()))")
        lines.append(f'    return {{"status": "ok"}}')
        lines.append("")

    return "\n".join(lines)


def gen_table_metadata(tables: list[TableDef]) -> str:
    """Generate table_metadata.py — dict of table info for introspection."""
    lines = [
        '"""',
        "Auto-generated table metadata from ProxySQL_Admin_Tables_Definitions.h",
        "",
        "DO NOT EDIT — regenerate with: python3 tools/gen_fastapi_models.py",
        '"""',
        "",
        "TABLE_METADATA: dict[str, dict] = {",
    ]
    for t in tables:
        lines.append(f'    "{t.table_name}": {{')
        lines.append(f'        "macro": "{t.macro_name}",')
        lines.append(f'        "readonly": {t.is_readonly},')
        lines.append(f'        "is_view": {t.is_view},')
        lines.append(f'        "pk_columns": {t.all_pk_columns!r},')
        lines.append(f'        "columns": [')
        for c in t.columns:
            lines.append(f'            {{"name": {c.name!r}, "type": {c.raw_type!r}, "nullable": {c.nullable}, "default": {c.default!r}, "autoincrement": {c.autoincrement}}},')
        lines.append(f'        ],')
        lines.append(f'    }},')
    lines.append("}")
    lines.append("")
    return "\n".join(lines)


def gen_db_module() -> str:
    """Generate db.py — async MySQL connection helper for the admin interface."""
    return textwrap.dedent('''\
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
    ''')


def gen_app_main() -> str:
    """Generate app.py — FastAPI application entry point."""
    return textwrap.dedent('''\
        """
        ProxySQL Web UI — FastAPI application.

        Run with:
            uvicorn webui.generated.app:app --reload --port 8080
        """

        from __future__ import annotations

        import os
        import pathlib
        import time

        import aiomysql
        import asyncpg
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        from fastapi.staticfiles import StaticFiles
        from pydantic import BaseModel

        from .crud_router import router as crud_router
        from .table_metadata import TABLE_METADATA

        app = FastAPI(
            title="proxui",
            description="Auto-generated REST API for ProxySQL admin tables",
            version="0.1.0",
            docs_url="/api/docs",
            openapi_url="/api/openapi.json",
        )

        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        app.include_router(crud_router, prefix="/api/v1")


        @app.get("/api/v1/health")
        async def health():
            return {"status": "ok"}


        @app.get("/api/v1/tables")
        async def list_tables():
            """Return table metadata, filtered to tables that actually exist in ProxySQL."""
            from .db import get_pool
            pool = await get_pool()
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


        async def _adhoc_connect(target: str, database: str | None = None):
            """Return (conn, is_pool_conn, label) for the given target."""
            from .db import get_pool
            pool = await get_pool()
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
        async def run_query(req: QueryRequest):
            """Execute free-form SQL against any target."""
            conn = None
            is_pool_conn = False
            try:
                conn, is_pool_conn, label = await _adhoc_connect(
                    req.target, database=req.database or None)
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
                        pool = await get_pool()
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
        async def config_status():
            """Compare memory vs runtime vs disk for each config module."""
            from .db import get_pool
            pool = await get_pool()
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
        async def config_action(req: ConfigAction):
            """Execute a LOAD/SAVE command for a config module."""
            if req.module not in CONFIG_MODULES:
                return {"ok": False, "error": f"Unknown module: {req.module}"}
            mod = CONFIG_MODULES[req.module]
            if req.action not in ("load_runtime", "save_disk", "load_disk"):
                return {"ok": False, "error": f"Unknown action: {req.action}"}
            cmd = mod[req.action]
            from .db import get_pool
            pool = await get_pool()
            try:
                async with pool.acquire() as conn:
                    async with conn.cursor() as cur:
                        await cur.execute(cmd)
                return {"ok": True, "command": cmd}
            except Exception as e:
                return {"ok": False, "error": str(e), "command": cmd}


        @app.get("/api/v1/config/diff/{module}")
        async def config_diff(module: str):
            """Return row-level diff between memory and runtime for a module."""
            if module not in CONFIG_MODULES:
                return {"error": f"Unknown module: {module}"}
            mod = CONFIG_MODULES[module]
            from .db import get_pool
            pool = await get_pool()
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
        async def get_schema(target: str, db: str = ""):
            """Return schema tree {db: {table: [cols]}} for any target."""
            conn = None
            is_pool = False
            try:
                conn, is_pool, label = await _adhoc_connect(
                    target, database=db or None)
                if target == "admin":
                    from .db import get_pool as _gp
                    pool = await _gp()
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
                        pool = await _gp2()
                        pool.release(conn)
                    elif _is_pg_conn(conn):
                        await conn.close()
                    else:
                        conn.close()


        # ── Database list for a target ──────────────────────────────

        @app.get("/api/v1/databases/{target:path}")
        async def list_databases(target: str):
            """List databases for any target."""
            conn = None
            is_pool = False
            try:
                conn, is_pool, _ = await _adhoc_connect(target)
                if target == "admin":
                    from .db import get_pool as _gp
                    pool = await _gp()
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
                        pool = await _gp2()
                        pool.release(conn)
                    elif _is_pg_conn(conn):
                        await conn.close()
                    else:
                        conn.close()


        # ── Available query targets (auto-discovered) ──────────────────

        @app.get("/api/v1/targets")
        async def list_targets():
            """Auto-discover query targets from ProxySQL state."""
            from .db import get_pool
            pool = await get_pool()

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
    ''')


def _table_tag(t: TableDef) -> str:
    """Derive an API tag from the table name."""
    name = t.table_name
    if name.startswith("stats_"):
        return "stats"
    if name.startswith("runtime_"):
        return "runtime"
    for prefix in ("mysql_", "pgsql_", "mcp_", "genai_", "clickhouse_", "proxysql_"):
        if name.startswith(prefix):
            return prefix.rstrip("_")
    return "admin"


# ---------------------------------------------------------------------------
# 5. Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Generate FastAPI models from ProxySQL table definitions")
    parser.add_argument(
        "--header",
        default="include/ProxySQL_Admin_Tables_Definitions.h",
        help="Path to the header file",
    )
    parser.add_argument(
        "--outdir",
        default="webui/generated",
        help="Output directory for generated files",
    )
    parser.add_argument(
        "--skip",
        nargs="*",
        default=[],
        metavar="FILE",
        help="Filenames to skip writing (e.g. app.py db.py for hand-crafted files)",
    )
    args = parser.parse_args()
    skip = set(args.skip or [])

    header_path = args.header
    if not os.path.exists(header_path):
        print(f"Error: header not found: {header_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Reading {header_path} ...")
    header = read_header(header_path)
    defs = extract_defines(header)
    resolved = resolve_defines(defs)

    # Filter to current tables
    current = {
        name: sql
        for name, sql in resolved.items()
        if is_current_table(name, defs)
    }

    print(f"Found {len(current)} current table definitions")

    # Parse all tables, dedup by table_name (prefer shorter macro name = the alias)
    tables: list[TableDef] = []
    seen_tables: dict[str, str] = {}  # table_name -> macro_name
    for macro_name in sorted(current.keys(), key=lambda n: (len(n), n)):
        sql = current[macro_name]
        try:
            t = parse_create_table(sql, macro_name)
            if t.table_name in seen_tables:
                # Keep the one with shorter macro name (canonical alias)
                continue
            seen_tables[t.table_name] = macro_name
            tables.append(t)
            pk_info = f" PK={t.all_pk_columns}" if t.all_pk_columns else ""
            kind = "VIEW" if t.is_view else ("RO" if t.is_readonly else "RW")
            print(f"  [{kind:4s}] {t.table_name} ({len(t.columns)} cols){pk_info}")
        except Exception as e:
            print(f"  WARN: skipping {macro_name}: {e}", file=sys.stderr)

    # Generate output
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    # __init__.py
    (outdir / "__init__.py").write_text("")

    models_path = outdir / "models.py"
    models_path.write_text(gen_models(tables))
    print(f"Wrote {models_path} ({len(tables)} models)")

    router_path = outdir / "crud_router.py"
    router_path.write_text(gen_crud_router(tables))
    print(f"Wrote {router_path}")

    meta_path = outdir / "table_metadata.py"
    meta_path.write_text(gen_table_metadata(tables))
    print(f"Wrote {meta_path}")

    db_path = outdir / "db.py"
    if "db.py" not in skip:
        db_path.write_text(gen_db_module())
        print(f"Wrote {db_path}")
    else:
        print(f"Skipped {db_path} (hand-crafted)")

    app_path = outdir / "app.py"
    if "app.py" not in skip:
        app_path.write_text(gen_app_main())
        print(f"Wrote {app_path}")
    else:
        print(f"Skipped {app_path} (hand-crafted)")

    print(f"\nDone. Run with:")
    print(f"  pip install fastapi uvicorn aiomysql pydantic")
    print(f"  uvicorn webui.generated.app:app --reload --port 8080")


if __name__ == "__main__":
    main()
