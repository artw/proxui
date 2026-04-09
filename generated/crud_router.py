"""
Auto-generated FastAPI CRUD router from ProxySQL_Admin_Tables_Definitions.h

DO NOT EDIT — regenerate with: python3 tools/gen_fastapi_models.py
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query

from .db import get_admin_conn, execute_query, execute_modify
from .models import (
    StatsTsdb,
    StatsProxysqlGlobal,
    Scheduler,
    SchedulerCreate,
    McpConfig,
    McpConfigCreate,
    MysqlUsers,
    MysqlUsersCreate,
    PgsqlUsers,
    PgsqlUsersCreate,
    StatsMysqlUsers,
    StatsPgsqlUsers,
    DebugLevels,
    DebugLevelsCreate,
    GenaiConfig,
    GenaiConfigCreate,
    StatsMysqlErrors,
    StatsMysqlGlobal,
    StatsPgsqlErrors,
    StatsPgsqlGlobal,
    RuntimeMysqlUsers,
    DebugFilters,
    DebugFiltersCreate,
    MysqlServers,
    MysqlServersCreate,
    PgsqlServers,
    PgsqlServersCreate,
    RestapiRoutes,
    RestapiRoutesCreate,
    StatsMemoryMetrics,
    GlobalSettings,
    GlobalSettingsCreate,
    McpQueryRules,
    McpQueryRulesCreate,
    StatsMcpQueryRules,
    ClickhouseUsers,
    ClickhouseUsersCreate,
    CoredumpFilters,
    CoredumpFiltersCreate,
    GlobalVariables,
    GlobalVariablesCreate,
    MysqlCollations,
    MysqlCollationsCreate,
    ProxysqlServers,
    ProxysqlServersCreate,
    StatsMcpQueryDigest,
    StatsTlsCertificates,
    McpAuthProfiles,
    McpAuthProfilesCreate,
    MysqlQueryRules,
    MysqlQueryRulesCreate,
    PgsqlQueryRules,
    PgsqlQueryRulesCreate,
    RuntimeScheduler,
    StatsMysqlProcesslist,
    StatsMysqlQueryRules,
    StatsPgsqlProcesslist,
    StatsPgsqlQueryRules,
    RuntimeChecksumsValues,
    RuntimeCoredumpFilters,
    RuntimeGlobalVariables,
    MysqlLdapMapping,
    MysqlLdapMappingCreate,
    PgsqlLdapMapping,
    PgsqlLdapMappingCreate,
    RuntimeMcpConfig,
    StatsMysqlErrorsReset,
    StatsMysqlQueryDigest,
    StatsPgsqlErrorsReset,
    StatsPgsqlQueryDigest,
    StatsPgsqlQueryEvents,
    McpTargetProfiles,
    McpTargetProfilesCreate,
    RuntimePgsqlUsers,
    StatsMysqlGtidExecuted,
    StatsPgsqlStatActivity,
    RuntimeGenaiConfig,
    RuntimeMysqlServers,
    RuntimePgsqlServers,
    StatsMysqlConnectionPool,
    StatsPgsqlConnectionPool,
    RuntimeRestapiRoutes,
    StatsMcpQueryDigestReset,
    StatsMysqlFreeConnections,
    StatsPgsqlFreeConnections,
    MysqlGaleraHostgroups,
    MysqlGaleraHostgroupsCreate,
    RuntimeMcpQueryRules,
    StatsMysqlClientHostCache,
    StatsMysqlCommandsCounters,
    StatsPgsqlClientHostCache,
    StatsPgsqlCommandsCounters,
    StatsProxysqlServersStatus,
    MysqlServersSslParams,
    MysqlServersSslParamsCreate,
    PgsqlServersSslParams,
    PgsqlServersSslParamsCreate,
    RuntimeClickhouseUsers,
    RuntimeProxysqlServers,
    StatsMysqlQueryEvents,
    StatsMcpQueryToolsCounters,
    StatsMysqlQueryDigestReset,
    StatsPgsqlQueryDigestReset,
    StatsProxysqlMessageMetrics,
    StatsProxysqlServersMetrics,
    RuntimeMcpAuthProfiles,
    RuntimeMysqlQueryRules,
    RuntimePgsqlQueryRules,
    MysqlHostgroupAttributes,
    MysqlHostgroupAttributesCreate,
    PgsqlHostgroupAttributes,
    PgsqlHostgroupAttributesCreate,
    RuntimeMysqlLdapMapping,
    RuntimePgsqlLdapMapping,
    StatsProxysqlServersChecksums,
    MysqlAwsAuroraHostgroups,
    MysqlAwsAuroraHostgroupsCreate,
    RuntimeMcpTargetProfiles,
    StatsMysqlConnectionPoolReset,
    StatsPgsqlConnectionPoolReset,
    MysqlReplicationHostgroups,
    MysqlReplicationHostgroupsCreate,
    PgsqlReplicationHostgroups,
    PgsqlReplicationHostgroupsCreate,
    StatsMysqlClientHostCacheReset,
    StatsPgsqlClientHostCacheReset,
    MysqlFirewallWhitelistRules,
    MysqlFirewallWhitelistRulesCreate,
    MysqlFirewallWhitelistUsers,
    MysqlFirewallWhitelistUsersCreate,
    MysqlQueryRulesFastRouting,
    MysqlQueryRulesFastRoutingCreate,
    PgsqlFirewallWhitelistRules,
    PgsqlFirewallWhitelistRulesCreate,
    PgsqlFirewallWhitelistUsers,
    PgsqlFirewallWhitelistUsersCreate,
    PgsqlQueryRulesFastRouting,
    PgsqlQueryRulesFastRoutingCreate,
    StatsMcpQueryToolsCountersReset,
    StatsPgsqlPreparedStatementsInfo,
    StatsProxysqlMessageMetricsReset,
    RuntimeMysqlGaleraHostgroups,
    StatsProxysqlServersClientsStatus,
    RuntimeMysqlServersSslParams,
    RuntimePgsqlServersSslParams,
    MysqlGroupReplicationHostgroups,
    MysqlGroupReplicationHostgroupsCreate,
    RuntimeMysqlHostgroupAttributes,
    RuntimePgsqlHostgroupAttributes,
    RuntimeMysqlAwsAuroraHostgroups,
    RuntimeMysqlReplicationHostgroups,
    RuntimePgsqlReplicationHostgroups,
    StatsMysqlPreparedStatementsInfo,
    RuntimeMysqlFirewallWhitelistRules,
    RuntimeMysqlFirewallWhitelistUsers,
    RuntimeMysqlQueryRulesFastRouting,
    RuntimePgsqlFirewallWhitelistRules,
    RuntimePgsqlFirewallWhitelistUsers,
    RuntimePgsqlQueryRulesFastRouting,
    MysqlFirewallWhitelistSqliFingerprints,
    MysqlFirewallWhitelistSqliFingerprintsCreate,
    PgsqlFirewallWhitelistSqliFingerprints,
    PgsqlFirewallWhitelistSqliFingerprintsCreate,
    RuntimeMysqlGroupReplicationHostgroups,
    RuntimeMysqlFirewallWhitelistSqliFingerprints,
    RuntimePgsqlFirewallWhitelistSqliFingerprints,
)

router = APIRouter()


@router.get("/stats_tsdb", response_model=list[StatsTsdb], tags=["stats"])
async def list_stats_tsdb(conn=Depends(get_admin_conn)):
    """List all rows from `stats_tsdb`."""
    return await execute_query(conn, "SELECT * FROM stats_tsdb")


@router.get("/stats_proxysql_global", response_model=list[StatsProxysqlGlobal], tags=["stats"])
async def list_stats_proxysql_global(conn=Depends(get_admin_conn)):
    """List all rows from `stats_proxysql_global`."""
    return await execute_query(conn, "SELECT * FROM stats_proxysql_global")


@router.get("/scheduler", response_model=list[Scheduler], tags=["admin"])
async def list_scheduler(conn=Depends(get_admin_conn)):
    """List all rows from `scheduler`."""
    return await execute_query(conn, "SELECT * FROM scheduler")


@router.post("/scheduler", response_model=dict[str, str], tags=["admin"])
async def create_scheduler(item: SchedulerCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `scheduler`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO scheduler ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/scheduler/{id}", response_model=Scheduler, tags=["admin"])
async def get_scheduler(id: str, conn=Depends(get_admin_conn)):
    """Get a single row from `scheduler` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM scheduler WHERE id = %s", [id])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/scheduler/{id}", response_model=dict[str, str], tags=["admin"])
async def delete_scheduler(id: str, conn=Depends(get_admin_conn)):
    """Delete a row from `scheduler` by primary key."""
    await execute_modify(conn, "DELETE FROM scheduler WHERE id = %s", [id])
    return {"status": "ok"}


@router.put("/scheduler/{id}", response_model=dict[str, str], tags=["admin"])
async def update_scheduler(id: str, item: SchedulerCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `scheduler`."""
    data = item.model_dump(exclude_none=True)
    data["id"] = id
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO scheduler ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/mcp_config", response_model=list[McpConfig], tags=["mcp"])
async def list_mcp_config(conn=Depends(get_admin_conn)):
    """List all rows from `mcp_config`."""
    return await execute_query(conn, "SELECT * FROM mcp_config")


@router.post("/mcp_config", response_model=dict[str, str], tags=["mcp"])
async def create_mcp_config(item: McpConfigCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `mcp_config`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO mcp_config ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/mcp_config/{variable_name}", response_model=McpConfig, tags=["mcp"])
async def get_mcp_config(variable_name: str, conn=Depends(get_admin_conn)):
    """Get a single row from `mcp_config` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM mcp_config WHERE variable_name = %s", [variable_name])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/mcp_config/{variable_name}", response_model=dict[str, str], tags=["mcp"])
async def delete_mcp_config(variable_name: str, conn=Depends(get_admin_conn)):
    """Delete a row from `mcp_config` by primary key."""
    await execute_modify(conn, "DELETE FROM mcp_config WHERE variable_name = %s", [variable_name])
    return {"status": "ok"}


@router.put("/mcp_config/{variable_name}", response_model=dict[str, str], tags=["mcp"])
async def update_mcp_config(variable_name: str, item: McpConfigCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `mcp_config`."""
    data = item.model_dump(exclude_none=True)
    data["variable_name"] = variable_name
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO mcp_config ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/mysql_users", response_model=list[MysqlUsers], tags=["mysql"])
async def list_mysql_users(conn=Depends(get_admin_conn)):
    """List all rows from `mysql_users`."""
    return await execute_query(conn, "SELECT * FROM mysql_users")


@router.post("/mysql_users", response_model=dict[str, str], tags=["mysql"])
async def create_mysql_users(item: MysqlUsersCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `mysql_users`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO mysql_users ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/mysql_users/{username}/{backend}", response_model=MysqlUsers, tags=["mysql"])
async def get_mysql_users(username: str, backend: str, conn=Depends(get_admin_conn)):
    """Get a single row from `mysql_users` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM mysql_users WHERE username = %s AND backend = %s", [username, backend])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/mysql_users/{username}/{backend}", response_model=dict[str, str], tags=["mysql"])
async def delete_mysql_users(username: str, backend: str, conn=Depends(get_admin_conn)):
    """Delete a row from `mysql_users` by primary key."""
    await execute_modify(conn, "DELETE FROM mysql_users WHERE username = %s AND backend = %s", [username, backend])
    return {"status": "ok"}


@router.put("/mysql_users/{username}/{backend}", response_model=dict[str, str], tags=["mysql"])
async def update_mysql_users(username: str, backend: str, item: MysqlUsersCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `mysql_users`."""
    data = item.model_dump(exclude_none=True)
    data["username"] = username
    data["backend"] = backend
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO mysql_users ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/pgsql_users", response_model=list[PgsqlUsers], tags=["pgsql"])
async def list_pgsql_users(conn=Depends(get_admin_conn)):
    """List all rows from `pgsql_users`."""
    return await execute_query(conn, "SELECT * FROM pgsql_users")


@router.post("/pgsql_users", response_model=dict[str, str], tags=["pgsql"])
async def create_pgsql_users(item: PgsqlUsersCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `pgsql_users`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO pgsql_users ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/pgsql_users/{username}/{backend}", response_model=PgsqlUsers, tags=["pgsql"])
async def get_pgsql_users(username: str, backend: str, conn=Depends(get_admin_conn)):
    """Get a single row from `pgsql_users` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM pgsql_users WHERE username = %s AND backend = %s", [username, backend])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/pgsql_users/{username}/{backend}", response_model=dict[str, str], tags=["pgsql"])
async def delete_pgsql_users(username: str, backend: str, conn=Depends(get_admin_conn)):
    """Delete a row from `pgsql_users` by primary key."""
    await execute_modify(conn, "DELETE FROM pgsql_users WHERE username = %s AND backend = %s", [username, backend])
    return {"status": "ok"}


@router.put("/pgsql_users/{username}/{backend}", response_model=dict[str, str], tags=["pgsql"])
async def update_pgsql_users(username: str, backend: str, item: PgsqlUsersCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `pgsql_users`."""
    data = item.model_dump(exclude_none=True)
    data["username"] = username
    data["backend"] = backend
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO pgsql_users ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/stats_mysql_users", response_model=list[StatsMysqlUsers], tags=["stats"])
async def list_stats_mysql_users(conn=Depends(get_admin_conn)):
    """List all rows from `stats_mysql_users`."""
    return await execute_query(conn, "SELECT * FROM stats_mysql_users")


@router.get("/stats_pgsql_users", response_model=list[StatsPgsqlUsers], tags=["stats"])
async def list_stats_pgsql_users(conn=Depends(get_admin_conn)):
    """List all rows from `stats_pgsql_users`."""
    return await execute_query(conn, "SELECT * FROM stats_pgsql_users")


@router.get("/debug_levels", response_model=list[DebugLevels], tags=["admin"])
async def list_debug_levels(conn=Depends(get_admin_conn)):
    """List all rows from `debug_levels`."""
    return await execute_query(conn, "SELECT * FROM debug_levels")


@router.post("/debug_levels", response_model=dict[str, str], tags=["admin"])
async def create_debug_levels(item: DebugLevelsCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `debug_levels`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO debug_levels ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/debug_levels/{module}", response_model=DebugLevels, tags=["admin"])
async def get_debug_levels(module: str, conn=Depends(get_admin_conn)):
    """Get a single row from `debug_levels` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM debug_levels WHERE module = %s", [module])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/debug_levels/{module}", response_model=dict[str, str], tags=["admin"])
async def delete_debug_levels(module: str, conn=Depends(get_admin_conn)):
    """Delete a row from `debug_levels` by primary key."""
    await execute_modify(conn, "DELETE FROM debug_levels WHERE module = %s", [module])
    return {"status": "ok"}


@router.put("/debug_levels/{module}", response_model=dict[str, str], tags=["admin"])
async def update_debug_levels(module: str, item: DebugLevelsCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `debug_levels`."""
    data = item.model_dump(exclude_none=True)
    data["module"] = module
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO debug_levels ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/genai_config", response_model=list[GenaiConfig], tags=["genai"])
async def list_genai_config(conn=Depends(get_admin_conn)):
    """List all rows from `genai_config`."""
    return await execute_query(conn, "SELECT * FROM genai_config")


@router.post("/genai_config", response_model=dict[str, str], tags=["genai"])
async def create_genai_config(item: GenaiConfigCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `genai_config`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO genai_config ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/genai_config/{variable_name}", response_model=GenaiConfig, tags=["genai"])
async def get_genai_config(variable_name: str, conn=Depends(get_admin_conn)):
    """Get a single row from `genai_config` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM genai_config WHERE variable_name = %s", [variable_name])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/genai_config/{variable_name}", response_model=dict[str, str], tags=["genai"])
async def delete_genai_config(variable_name: str, conn=Depends(get_admin_conn)):
    """Delete a row from `genai_config` by primary key."""
    await execute_modify(conn, "DELETE FROM genai_config WHERE variable_name = %s", [variable_name])
    return {"status": "ok"}


@router.put("/genai_config/{variable_name}", response_model=dict[str, str], tags=["genai"])
async def update_genai_config(variable_name: str, item: GenaiConfigCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `genai_config`."""
    data = item.model_dump(exclude_none=True)
    data["variable_name"] = variable_name
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO genai_config ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/stats_mysql_errors", response_model=list[StatsMysqlErrors], tags=["stats"])
async def list_stats_mysql_errors(conn=Depends(get_admin_conn)):
    """List all rows from `stats_mysql_errors`."""
    return await execute_query(conn, "SELECT * FROM stats_mysql_errors")


@router.get("/stats_mysql_global", response_model=list[StatsMysqlGlobal], tags=["stats"])
async def list_stats_mysql_global(conn=Depends(get_admin_conn)):
    """List all rows from `stats_mysql_global`."""
    return await execute_query(conn, "SELECT * FROM stats_mysql_global")


@router.get("/stats_pgsql_errors", response_model=list[StatsPgsqlErrors], tags=["stats"])
async def list_stats_pgsql_errors(conn=Depends(get_admin_conn)):
    """List all rows from `stats_pgsql_errors`."""
    return await execute_query(conn, "SELECT * FROM stats_pgsql_errors")


@router.get("/stats_pgsql_global", response_model=list[StatsPgsqlGlobal], tags=["stats"])
async def list_stats_pgsql_global(conn=Depends(get_admin_conn)):
    """List all rows from `stats_pgsql_global`."""
    return await execute_query(conn, "SELECT * FROM stats_pgsql_global")


@router.get("/runtime_mysql_users", response_model=list[RuntimeMysqlUsers], tags=["runtime"])
async def list_runtime_mysql_users(conn=Depends(get_admin_conn)):
    """List all rows from `runtime_mysql_users`."""
    return await execute_query(conn, "SELECT * FROM runtime_mysql_users")


@router.get("/debug_filters", response_model=list[DebugFilters], tags=["admin"])
async def list_debug_filters(conn=Depends(get_admin_conn)):
    """List all rows from `debug_filters`."""
    return await execute_query(conn, "SELECT * FROM debug_filters")


@router.post("/debug_filters", response_model=dict[str, str], tags=["admin"])
async def create_debug_filters(item: DebugFiltersCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `debug_filters`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO debug_filters ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/debug_filters/{filename}/{line}/{funct}", response_model=DebugFilters, tags=["admin"])
async def get_debug_filters(filename: str, line: str, funct: str, conn=Depends(get_admin_conn)):
    """Get a single row from `debug_filters` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM debug_filters WHERE filename = %s AND line = %s AND funct = %s", [filename, line, funct])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/debug_filters/{filename}/{line}/{funct}", response_model=dict[str, str], tags=["admin"])
async def delete_debug_filters(filename: str, line: str, funct: str, conn=Depends(get_admin_conn)):
    """Delete a row from `debug_filters` by primary key."""
    await execute_modify(conn, "DELETE FROM debug_filters WHERE filename = %s AND line = %s AND funct = %s", [filename, line, funct])
    return {"status": "ok"}


@router.put("/debug_filters/{filename}/{line}/{funct}", response_model=dict[str, str], tags=["admin"])
async def update_debug_filters(filename: str, line: str, funct: str, item: DebugFiltersCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `debug_filters`."""
    data = item.model_dump(exclude_none=True)
    data["filename"] = filename
    data["line"] = line
    data["funct"] = funct
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO debug_filters ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/mysql_servers", response_model=list[MysqlServers], tags=["mysql"])
async def list_mysql_servers(conn=Depends(get_admin_conn)):
    """List all rows from `mysql_servers`."""
    return await execute_query(conn, "SELECT * FROM mysql_servers")


@router.post("/mysql_servers", response_model=dict[str, str], tags=["mysql"])
async def create_mysql_servers(item: MysqlServersCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `mysql_servers`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO mysql_servers ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/mysql_servers/{hostgroup_id}/{hostname}/{port}", response_model=MysqlServers, tags=["mysql"])
async def get_mysql_servers(hostgroup_id: str, hostname: str, port: str, conn=Depends(get_admin_conn)):
    """Get a single row from `mysql_servers` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM mysql_servers WHERE hostgroup_id = %s AND hostname = %s AND port = %s", [hostgroup_id, hostname, port])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/mysql_servers/{hostgroup_id}/{hostname}/{port}", response_model=dict[str, str], tags=["mysql"])
async def delete_mysql_servers(hostgroup_id: str, hostname: str, port: str, conn=Depends(get_admin_conn)):
    """Delete a row from `mysql_servers` by primary key."""
    await execute_modify(conn, "DELETE FROM mysql_servers WHERE hostgroup_id = %s AND hostname = %s AND port = %s", [hostgroup_id, hostname, port])
    return {"status": "ok"}


@router.put("/mysql_servers/{hostgroup_id}/{hostname}/{port}", response_model=dict[str, str], tags=["mysql"])
async def update_mysql_servers(hostgroup_id: str, hostname: str, port: str, item: MysqlServersCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `mysql_servers`."""
    data = item.model_dump(exclude_none=True)
    data["hostgroup_id"] = hostgroup_id
    data["hostname"] = hostname
    data["port"] = port
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO mysql_servers ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/pgsql_servers", response_model=list[PgsqlServers], tags=["pgsql"])
async def list_pgsql_servers(conn=Depends(get_admin_conn)):
    """List all rows from `pgsql_servers`."""
    return await execute_query(conn, "SELECT * FROM pgsql_servers")


@router.post("/pgsql_servers", response_model=dict[str, str], tags=["pgsql"])
async def create_pgsql_servers(item: PgsqlServersCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `pgsql_servers`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO pgsql_servers ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/pgsql_servers/{hostgroup_id}/{hostname}/{port}", response_model=PgsqlServers, tags=["pgsql"])
async def get_pgsql_servers(hostgroup_id: str, hostname: str, port: str, conn=Depends(get_admin_conn)):
    """Get a single row from `pgsql_servers` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM pgsql_servers WHERE hostgroup_id = %s AND hostname = %s AND port = %s", [hostgroup_id, hostname, port])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/pgsql_servers/{hostgroup_id}/{hostname}/{port}", response_model=dict[str, str], tags=["pgsql"])
async def delete_pgsql_servers(hostgroup_id: str, hostname: str, port: str, conn=Depends(get_admin_conn)):
    """Delete a row from `pgsql_servers` by primary key."""
    await execute_modify(conn, "DELETE FROM pgsql_servers WHERE hostgroup_id = %s AND hostname = %s AND port = %s", [hostgroup_id, hostname, port])
    return {"status": "ok"}


@router.put("/pgsql_servers/{hostgroup_id}/{hostname}/{port}", response_model=dict[str, str], tags=["pgsql"])
async def update_pgsql_servers(hostgroup_id: str, hostname: str, port: str, item: PgsqlServersCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `pgsql_servers`."""
    data = item.model_dump(exclude_none=True)
    data["hostgroup_id"] = hostgroup_id
    data["hostname"] = hostname
    data["port"] = port
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO pgsql_servers ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/restapi_routes", response_model=list[RestapiRoutes], tags=["admin"])
async def list_restapi_routes(conn=Depends(get_admin_conn)):
    """List all rows from `restapi_routes`."""
    return await execute_query(conn, "SELECT * FROM restapi_routes")


@router.post("/restapi_routes", response_model=dict[str, str], tags=["admin"])
async def create_restapi_routes(item: RestapiRoutesCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `restapi_routes`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO restapi_routes ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/restapi_routes/{id}", response_model=RestapiRoutes, tags=["admin"])
async def get_restapi_routes(id: str, conn=Depends(get_admin_conn)):
    """Get a single row from `restapi_routes` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM restapi_routes WHERE id = %s", [id])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/restapi_routes/{id}", response_model=dict[str, str], tags=["admin"])
async def delete_restapi_routes(id: str, conn=Depends(get_admin_conn)):
    """Delete a row from `restapi_routes` by primary key."""
    await execute_modify(conn, "DELETE FROM restapi_routes WHERE id = %s", [id])
    return {"status": "ok"}


@router.put("/restapi_routes/{id}", response_model=dict[str, str], tags=["admin"])
async def update_restapi_routes(id: str, item: RestapiRoutesCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `restapi_routes`."""
    data = item.model_dump(exclude_none=True)
    data["id"] = id
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO restapi_routes ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/stats_memory_metrics", response_model=list[StatsMemoryMetrics], tags=["stats"])
async def list_stats_memory_metrics(conn=Depends(get_admin_conn)):
    """List all rows from `stats_memory_metrics`."""
    return await execute_query(conn, "SELECT * FROM stats_memory_metrics")


@router.get("/global_settings", response_model=list[GlobalSettings], tags=["admin"])
async def list_global_settings(conn=Depends(get_admin_conn)):
    """List all rows from `global_settings`."""
    return await execute_query(conn, "SELECT * FROM global_settings")


@router.post("/global_settings", response_model=dict[str, str], tags=["admin"])
async def create_global_settings(item: GlobalSettingsCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `global_settings`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO global_settings ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/global_settings/{variable_name}", response_model=GlobalSettings, tags=["admin"])
async def get_global_settings(variable_name: str, conn=Depends(get_admin_conn)):
    """Get a single row from `global_settings` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM global_settings WHERE variable_name = %s", [variable_name])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/global_settings/{variable_name}", response_model=dict[str, str], tags=["admin"])
async def delete_global_settings(variable_name: str, conn=Depends(get_admin_conn)):
    """Delete a row from `global_settings` by primary key."""
    await execute_modify(conn, "DELETE FROM global_settings WHERE variable_name = %s", [variable_name])
    return {"status": "ok"}


@router.put("/global_settings/{variable_name}", response_model=dict[str, str], tags=["admin"])
async def update_global_settings(variable_name: str, item: GlobalSettingsCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `global_settings`."""
    data = item.model_dump(exclude_none=True)
    data["variable_name"] = variable_name
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO global_settings ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/mcp_query_rules", response_model=list[McpQueryRules], tags=["mcp"])
async def list_mcp_query_rules(conn=Depends(get_admin_conn)):
    """List all rows from `mcp_query_rules`."""
    return await execute_query(conn, "SELECT * FROM mcp_query_rules")


@router.post("/mcp_query_rules", response_model=dict[str, str], tags=["mcp"])
async def create_mcp_query_rules(item: McpQueryRulesCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `mcp_query_rules`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO mcp_query_rules ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/mcp_query_rules/{rule_id}", response_model=McpQueryRules, tags=["mcp"])
async def get_mcp_query_rules(rule_id: str, conn=Depends(get_admin_conn)):
    """Get a single row from `mcp_query_rules` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM mcp_query_rules WHERE rule_id = %s", [rule_id])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/mcp_query_rules/{rule_id}", response_model=dict[str, str], tags=["mcp"])
async def delete_mcp_query_rules(rule_id: str, conn=Depends(get_admin_conn)):
    """Delete a row from `mcp_query_rules` by primary key."""
    await execute_modify(conn, "DELETE FROM mcp_query_rules WHERE rule_id = %s", [rule_id])
    return {"status": "ok"}


@router.put("/mcp_query_rules/{rule_id}", response_model=dict[str, str], tags=["mcp"])
async def update_mcp_query_rules(rule_id: str, item: McpQueryRulesCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `mcp_query_rules`."""
    data = item.model_dump(exclude_none=True)
    data["rule_id"] = rule_id
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO mcp_query_rules ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/stats_mcp_query_rules", response_model=list[StatsMcpQueryRules], tags=["stats"])
async def list_stats_mcp_query_rules(conn=Depends(get_admin_conn)):
    """List all rows from `stats_mcp_query_rules`."""
    return await execute_query(conn, "SELECT * FROM stats_mcp_query_rules")


@router.get("/clickhouse_users", response_model=list[ClickhouseUsers], tags=["clickhouse"])
async def list_clickhouse_users(conn=Depends(get_admin_conn)):
    """List all rows from `clickhouse_users`."""
    return await execute_query(conn, "SELECT * FROM clickhouse_users")


@router.post("/clickhouse_users", response_model=dict[str, str], tags=["clickhouse"])
async def create_clickhouse_users(item: ClickhouseUsersCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `clickhouse_users`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO clickhouse_users ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/coredump_filters", response_model=list[CoredumpFilters], tags=["admin"])
async def list_coredump_filters(conn=Depends(get_admin_conn)):
    """List all rows from `coredump_filters`."""
    return await execute_query(conn, "SELECT * FROM coredump_filters")


@router.post("/coredump_filters", response_model=dict[str, str], tags=["admin"])
async def create_coredump_filters(item: CoredumpFiltersCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `coredump_filters`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO coredump_filters ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/coredump_filters/{filename}/{line}", response_model=CoredumpFilters, tags=["admin"])
async def get_coredump_filters(filename: str, line: str, conn=Depends(get_admin_conn)):
    """Get a single row from `coredump_filters` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM coredump_filters WHERE filename = %s AND line = %s", [filename, line])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/coredump_filters/{filename}/{line}", response_model=dict[str, str], tags=["admin"])
async def delete_coredump_filters(filename: str, line: str, conn=Depends(get_admin_conn)):
    """Delete a row from `coredump_filters` by primary key."""
    await execute_modify(conn, "DELETE FROM coredump_filters WHERE filename = %s AND line = %s", [filename, line])
    return {"status": "ok"}


@router.put("/coredump_filters/{filename}/{line}", response_model=dict[str, str], tags=["admin"])
async def update_coredump_filters(filename: str, line: str, item: CoredumpFiltersCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `coredump_filters`."""
    data = item.model_dump(exclude_none=True)
    data["filename"] = filename
    data["line"] = line
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO coredump_filters ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/global_variables", response_model=list[GlobalVariables], tags=["admin"])
async def list_global_variables(conn=Depends(get_admin_conn)):
    """List all rows from `global_variables`."""
    return await execute_query(conn, "SELECT * FROM global_variables")


@router.post("/global_variables", response_model=dict[str, str], tags=["admin"])
async def create_global_variables(item: GlobalVariablesCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `global_variables`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO global_variables ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/global_variables/{variable_name}", response_model=GlobalVariables, tags=["admin"])
async def get_global_variables(variable_name: str, conn=Depends(get_admin_conn)):
    """Get a single row from `global_variables` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM global_variables WHERE variable_name = %s", [variable_name])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/global_variables/{variable_name}", response_model=dict[str, str], tags=["admin"])
async def delete_global_variables(variable_name: str, conn=Depends(get_admin_conn)):
    """Delete a row from `global_variables` by primary key."""
    await execute_modify(conn, "DELETE FROM global_variables WHERE variable_name = %s", [variable_name])
    return {"status": "ok"}


@router.put("/global_variables/{variable_name}", response_model=dict[str, str], tags=["admin"])
async def update_global_variables(variable_name: str, item: GlobalVariablesCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `global_variables`."""
    data = item.model_dump(exclude_none=True)
    data["variable_name"] = variable_name
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO global_variables ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/mysql_collations", response_model=list[MysqlCollations], tags=["mysql"])
async def list_mysql_collations(conn=Depends(get_admin_conn)):
    """List all rows from `mysql_collations`."""
    return await execute_query(conn, "SELECT * FROM mysql_collations")


@router.post("/mysql_collations", response_model=dict[str, str], tags=["mysql"])
async def create_mysql_collations(item: MysqlCollationsCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `mysql_collations`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO mysql_collations ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/mysql_collations/{Id}", response_model=MysqlCollations, tags=["mysql"])
async def get_mysql_collations(Id: str, conn=Depends(get_admin_conn)):
    """Get a single row from `mysql_collations` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM mysql_collations WHERE Id = %s", [Id])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/mysql_collations/{Id}", response_model=dict[str, str], tags=["mysql"])
async def delete_mysql_collations(Id: str, conn=Depends(get_admin_conn)):
    """Delete a row from `mysql_collations` by primary key."""
    await execute_modify(conn, "DELETE FROM mysql_collations WHERE Id = %s", [Id])
    return {"status": "ok"}


@router.put("/mysql_collations/{Id}", response_model=dict[str, str], tags=["mysql"])
async def update_mysql_collations(Id: str, item: MysqlCollationsCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `mysql_collations`."""
    data = item.model_dump(exclude_none=True)
    data["Id"] = Id
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO mysql_collations ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/proxysql_servers", response_model=list[ProxysqlServers], tags=["proxysql"])
async def list_proxysql_servers(conn=Depends(get_admin_conn)):
    """List all rows from `proxysql_servers`."""
    return await execute_query(conn, "SELECT * FROM proxysql_servers")


@router.post("/proxysql_servers", response_model=dict[str, str], tags=["proxysql"])
async def create_proxysql_servers(item: ProxysqlServersCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `proxysql_servers`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO proxysql_servers ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/proxysql_servers/{hostname}/{port}", response_model=ProxysqlServers, tags=["proxysql"])
async def get_proxysql_servers(hostname: str, port: str, conn=Depends(get_admin_conn)):
    """Get a single row from `proxysql_servers` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM proxysql_servers WHERE hostname = %s AND port = %s", [hostname, port])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/proxysql_servers/{hostname}/{port}", response_model=dict[str, str], tags=["proxysql"])
async def delete_proxysql_servers(hostname: str, port: str, conn=Depends(get_admin_conn)):
    """Delete a row from `proxysql_servers` by primary key."""
    await execute_modify(conn, "DELETE FROM proxysql_servers WHERE hostname = %s AND port = %s", [hostname, port])
    return {"status": "ok"}


@router.put("/proxysql_servers/{hostname}/{port}", response_model=dict[str, str], tags=["proxysql"])
async def update_proxysql_servers(hostname: str, port: str, item: ProxysqlServersCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `proxysql_servers`."""
    data = item.model_dump(exclude_none=True)
    data["hostname"] = hostname
    data["port"] = port
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO proxysql_servers ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/stats_mcp_query_digest", response_model=list[StatsMcpQueryDigest], tags=["stats"])
async def list_stats_mcp_query_digest(conn=Depends(get_admin_conn)):
    """List all rows from `stats_mcp_query_digest`."""
    return await execute_query(conn, "SELECT * FROM stats_mcp_query_digest")


@router.get("/stats_tls_certificates", response_model=list[StatsTlsCertificates], tags=["stats"])
async def list_stats_tls_certificates(conn=Depends(get_admin_conn)):
    """List all rows from `stats_tls_certificates`."""
    return await execute_query(conn, "SELECT * FROM stats_tls_certificates")


@router.get("/mcp_auth_profiles", response_model=list[McpAuthProfiles], tags=["mcp"])
async def list_mcp_auth_profiles(conn=Depends(get_admin_conn)):
    """List all rows from `mcp_auth_profiles`."""
    return await execute_query(conn, "SELECT * FROM mcp_auth_profiles")


@router.post("/mcp_auth_profiles", response_model=dict[str, str], tags=["mcp"])
async def create_mcp_auth_profiles(item: McpAuthProfilesCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `mcp_auth_profiles`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO mcp_auth_profiles ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/mcp_auth_profiles/{auth_profile_id}", response_model=McpAuthProfiles, tags=["mcp"])
async def get_mcp_auth_profiles(auth_profile_id: str, conn=Depends(get_admin_conn)):
    """Get a single row from `mcp_auth_profiles` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM mcp_auth_profiles WHERE auth_profile_id = %s", [auth_profile_id])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/mcp_auth_profiles/{auth_profile_id}", response_model=dict[str, str], tags=["mcp"])
async def delete_mcp_auth_profiles(auth_profile_id: str, conn=Depends(get_admin_conn)):
    """Delete a row from `mcp_auth_profiles` by primary key."""
    await execute_modify(conn, "DELETE FROM mcp_auth_profiles WHERE auth_profile_id = %s", [auth_profile_id])
    return {"status": "ok"}


@router.put("/mcp_auth_profiles/{auth_profile_id}", response_model=dict[str, str], tags=["mcp"])
async def update_mcp_auth_profiles(auth_profile_id: str, item: McpAuthProfilesCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `mcp_auth_profiles`."""
    data = item.model_dump(exclude_none=True)
    data["auth_profile_id"] = auth_profile_id
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO mcp_auth_profiles ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/mysql_query_rules", response_model=list[MysqlQueryRules], tags=["mysql"])
async def list_mysql_query_rules(conn=Depends(get_admin_conn)):
    """List all rows from `mysql_query_rules`."""
    return await execute_query(conn, "SELECT * FROM mysql_query_rules")


@router.post("/mysql_query_rules", response_model=dict[str, str], tags=["mysql"])
async def create_mysql_query_rules(item: MysqlQueryRulesCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `mysql_query_rules`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO mysql_query_rules ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/mysql_query_rules/{rule_id}", response_model=MysqlQueryRules, tags=["mysql"])
async def get_mysql_query_rules(rule_id: str, conn=Depends(get_admin_conn)):
    """Get a single row from `mysql_query_rules` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM mysql_query_rules WHERE rule_id = %s", [rule_id])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/mysql_query_rules/{rule_id}", response_model=dict[str, str], tags=["mysql"])
async def delete_mysql_query_rules(rule_id: str, conn=Depends(get_admin_conn)):
    """Delete a row from `mysql_query_rules` by primary key."""
    await execute_modify(conn, "DELETE FROM mysql_query_rules WHERE rule_id = %s", [rule_id])
    return {"status": "ok"}


@router.put("/mysql_query_rules/{rule_id}", response_model=dict[str, str], tags=["mysql"])
async def update_mysql_query_rules(rule_id: str, item: MysqlQueryRulesCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `mysql_query_rules`."""
    data = item.model_dump(exclude_none=True)
    data["rule_id"] = rule_id
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO mysql_query_rules ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/pgsql_query_rules", response_model=list[PgsqlQueryRules], tags=["pgsql"])
async def list_pgsql_query_rules(conn=Depends(get_admin_conn)):
    """List all rows from `pgsql_query_rules`."""
    return await execute_query(conn, "SELECT * FROM pgsql_query_rules")


@router.post("/pgsql_query_rules", response_model=dict[str, str], tags=["pgsql"])
async def create_pgsql_query_rules(item: PgsqlQueryRulesCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `pgsql_query_rules`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO pgsql_query_rules ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/pgsql_query_rules/{rule_id}", response_model=PgsqlQueryRules, tags=["pgsql"])
async def get_pgsql_query_rules(rule_id: str, conn=Depends(get_admin_conn)):
    """Get a single row from `pgsql_query_rules` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM pgsql_query_rules WHERE rule_id = %s", [rule_id])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/pgsql_query_rules/{rule_id}", response_model=dict[str, str], tags=["pgsql"])
async def delete_pgsql_query_rules(rule_id: str, conn=Depends(get_admin_conn)):
    """Delete a row from `pgsql_query_rules` by primary key."""
    await execute_modify(conn, "DELETE FROM pgsql_query_rules WHERE rule_id = %s", [rule_id])
    return {"status": "ok"}


@router.put("/pgsql_query_rules/{rule_id}", response_model=dict[str, str], tags=["pgsql"])
async def update_pgsql_query_rules(rule_id: str, item: PgsqlQueryRulesCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `pgsql_query_rules`."""
    data = item.model_dump(exclude_none=True)
    data["rule_id"] = rule_id
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO pgsql_query_rules ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/runtime_scheduler", response_model=list[RuntimeScheduler], tags=["runtime"])
async def list_runtime_scheduler(conn=Depends(get_admin_conn)):
    """List all rows from `runtime_scheduler`."""
    return await execute_query(conn, "SELECT * FROM runtime_scheduler")


@router.get("/stats_mysql_processlist", response_model=list[StatsMysqlProcesslist], tags=["stats"])
async def list_stats_mysql_processlist(conn=Depends(get_admin_conn)):
    """List all rows from `stats_mysql_processlist`."""
    return await execute_query(conn, "SELECT * FROM stats_mysql_processlist")


@router.get("/stats_mysql_query_rules", response_model=list[StatsMysqlQueryRules], tags=["stats"])
async def list_stats_mysql_query_rules(conn=Depends(get_admin_conn)):
    """List all rows from `stats_mysql_query_rules`."""
    return await execute_query(conn, "SELECT * FROM stats_mysql_query_rules")


@router.get("/stats_pgsql_processlist", response_model=list[StatsPgsqlProcesslist], tags=["stats"])
async def list_stats_pgsql_processlist(conn=Depends(get_admin_conn)):
    """List all rows from `stats_pgsql_processlist`."""
    return await execute_query(conn, "SELECT * FROM stats_pgsql_processlist")


@router.get("/stats_pgsql_query_rules", response_model=list[StatsPgsqlQueryRules], tags=["stats"])
async def list_stats_pgsql_query_rules(conn=Depends(get_admin_conn)):
    """List all rows from `stats_pgsql_query_rules`."""
    return await execute_query(conn, "SELECT * FROM stats_pgsql_query_rules")


@router.get("/runtime_checksums_values", response_model=list[RuntimeChecksumsValues], tags=["runtime"])
async def list_runtime_checksums_values(conn=Depends(get_admin_conn)):
    """List all rows from `runtime_checksums_values`."""
    return await execute_query(conn, "SELECT * FROM runtime_checksums_values")


@router.get("/runtime_coredump_filters", response_model=list[RuntimeCoredumpFilters], tags=["runtime"])
async def list_runtime_coredump_filters(conn=Depends(get_admin_conn)):
    """List all rows from `runtime_coredump_filters`."""
    return await execute_query(conn, "SELECT * FROM runtime_coredump_filters")


@router.get("/runtime_global_variables", response_model=list[RuntimeGlobalVariables], tags=["runtime"])
async def list_runtime_global_variables(conn=Depends(get_admin_conn)):
    """List all rows from `runtime_global_variables`."""
    return await execute_query(conn, "SELECT * FROM runtime_global_variables")


@router.get("/mysql_ldap_mapping", response_model=list[MysqlLdapMapping], tags=["mysql"])
async def list_mysql_ldap_mapping(conn=Depends(get_admin_conn)):
    """List all rows from `mysql_ldap_mapping`."""
    return await execute_query(conn, "SELECT * FROM mysql_ldap_mapping")


@router.post("/mysql_ldap_mapping", response_model=dict[str, str], tags=["mysql"])
async def create_mysql_ldap_mapping(item: MysqlLdapMappingCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `mysql_ldap_mapping`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO mysql_ldap_mapping ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/mysql_ldap_mapping/{priority}", response_model=MysqlLdapMapping, tags=["mysql"])
async def get_mysql_ldap_mapping(priority: str, conn=Depends(get_admin_conn)):
    """Get a single row from `mysql_ldap_mapping` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM mysql_ldap_mapping WHERE priority = %s", [priority])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/mysql_ldap_mapping/{priority}", response_model=dict[str, str], tags=["mysql"])
async def delete_mysql_ldap_mapping(priority: str, conn=Depends(get_admin_conn)):
    """Delete a row from `mysql_ldap_mapping` by primary key."""
    await execute_modify(conn, "DELETE FROM mysql_ldap_mapping WHERE priority = %s", [priority])
    return {"status": "ok"}


@router.put("/mysql_ldap_mapping/{priority}", response_model=dict[str, str], tags=["mysql"])
async def update_mysql_ldap_mapping(priority: str, item: MysqlLdapMappingCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `mysql_ldap_mapping`."""
    data = item.model_dump(exclude_none=True)
    data["priority"] = priority
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO mysql_ldap_mapping ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/pgsql_ldap_mapping", response_model=list[PgsqlLdapMapping], tags=["pgsql"])
async def list_pgsql_ldap_mapping(conn=Depends(get_admin_conn)):
    """List all rows from `pgsql_ldap_mapping`."""
    return await execute_query(conn, "SELECT * FROM pgsql_ldap_mapping")


@router.post("/pgsql_ldap_mapping", response_model=dict[str, str], tags=["pgsql"])
async def create_pgsql_ldap_mapping(item: PgsqlLdapMappingCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `pgsql_ldap_mapping`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO pgsql_ldap_mapping ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/pgsql_ldap_mapping/{priority}", response_model=PgsqlLdapMapping, tags=["pgsql"])
async def get_pgsql_ldap_mapping(priority: str, conn=Depends(get_admin_conn)):
    """Get a single row from `pgsql_ldap_mapping` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM pgsql_ldap_mapping WHERE priority = %s", [priority])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/pgsql_ldap_mapping/{priority}", response_model=dict[str, str], tags=["pgsql"])
async def delete_pgsql_ldap_mapping(priority: str, conn=Depends(get_admin_conn)):
    """Delete a row from `pgsql_ldap_mapping` by primary key."""
    await execute_modify(conn, "DELETE FROM pgsql_ldap_mapping WHERE priority = %s", [priority])
    return {"status": "ok"}


@router.put("/pgsql_ldap_mapping/{priority}", response_model=dict[str, str], tags=["pgsql"])
async def update_pgsql_ldap_mapping(priority: str, item: PgsqlLdapMappingCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `pgsql_ldap_mapping`."""
    data = item.model_dump(exclude_none=True)
    data["priority"] = priority
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO pgsql_ldap_mapping ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/runtime_mcp_config", response_model=list[RuntimeMcpConfig], tags=["runtime"])
async def list_runtime_mcp_config(conn=Depends(get_admin_conn)):
    """List all rows from `runtime_mcp_config`."""
    return await execute_query(conn, "SELECT * FROM runtime_mcp_config")


@router.get("/stats_mysql_errors_reset", response_model=list[StatsMysqlErrorsReset], tags=["stats"])
async def list_stats_mysql_errors_reset(conn=Depends(get_admin_conn)):
    """List all rows from `stats_mysql_errors_reset`."""
    return await execute_query(conn, "SELECT * FROM stats_mysql_errors_reset")


@router.get("/stats_mysql_query_digest", response_model=list[StatsMysqlQueryDigest], tags=["stats"])
async def list_stats_mysql_query_digest(conn=Depends(get_admin_conn)):
    """List all rows from `stats_mysql_query_digest`."""
    return await execute_query(conn, "SELECT * FROM stats_mysql_query_digest")


@router.get("/stats_pgsql_errors_reset", response_model=list[StatsPgsqlErrorsReset], tags=["stats"])
async def list_stats_pgsql_errors_reset(conn=Depends(get_admin_conn)):
    """List all rows from `stats_pgsql_errors_reset`."""
    return await execute_query(conn, "SELECT * FROM stats_pgsql_errors_reset")


@router.get("/stats_pgsql_query_digest", response_model=list[StatsPgsqlQueryDigest], tags=["stats"])
async def list_stats_pgsql_query_digest(conn=Depends(get_admin_conn)):
    """List all rows from `stats_pgsql_query_digest`."""
    return await execute_query(conn, "SELECT * FROM stats_pgsql_query_digest")


@router.get("/stats_pgsql_query_events", response_model=list[StatsPgsqlQueryEvents], tags=["stats"])
async def list_stats_pgsql_query_events(conn=Depends(get_admin_conn)):
    """List all rows from `stats_pgsql_query_events`."""
    return await execute_query(conn, "SELECT * FROM stats_pgsql_query_events")


@router.get("/mcp_target_profiles", response_model=list[McpTargetProfiles], tags=["mcp"])
async def list_mcp_target_profiles(conn=Depends(get_admin_conn)):
    """List all rows from `mcp_target_profiles`."""
    return await execute_query(conn, "SELECT * FROM mcp_target_profiles")


@router.post("/mcp_target_profiles", response_model=dict[str, str], tags=["mcp"])
async def create_mcp_target_profiles(item: McpTargetProfilesCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `mcp_target_profiles`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO mcp_target_profiles ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/mcp_target_profiles/{target_id}", response_model=McpTargetProfiles, tags=["mcp"])
async def get_mcp_target_profiles(target_id: str, conn=Depends(get_admin_conn)):
    """Get a single row from `mcp_target_profiles` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM mcp_target_profiles WHERE target_id = %s", [target_id])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/mcp_target_profiles/{target_id}", response_model=dict[str, str], tags=["mcp"])
async def delete_mcp_target_profiles(target_id: str, conn=Depends(get_admin_conn)):
    """Delete a row from `mcp_target_profiles` by primary key."""
    await execute_modify(conn, "DELETE FROM mcp_target_profiles WHERE target_id = %s", [target_id])
    return {"status": "ok"}


@router.put("/mcp_target_profiles/{target_id}", response_model=dict[str, str], tags=["mcp"])
async def update_mcp_target_profiles(target_id: str, item: McpTargetProfilesCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `mcp_target_profiles`."""
    data = item.model_dump(exclude_none=True)
    data["target_id"] = target_id
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO mcp_target_profiles ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/runtime_pgsql_users", response_model=list[RuntimePgsqlUsers], tags=["runtime"])
async def list_runtime_pgsql_users(conn=Depends(get_admin_conn)):
    """List all rows from `runtime_pgsql_users`."""
    return await execute_query(conn, "SELECT * FROM runtime_pgsql_users")


@router.get("/stats_mysql_gtid_executed", response_model=list[StatsMysqlGtidExecuted], tags=["stats"])
async def list_stats_mysql_gtid_executed(conn=Depends(get_admin_conn)):
    """List all rows from `stats_mysql_gtid_executed`."""
    return await execute_query(conn, "SELECT * FROM stats_mysql_gtid_executed")


@router.get("/stats_pgsql_stat_activity", response_model=list[StatsPgsqlStatActivity], tags=["stats"])
async def list_stats_pgsql_stat_activity(conn=Depends(get_admin_conn)):
    """List all rows from `stats_pgsql_stat_activity`."""
    return await execute_query(conn, "SELECT * FROM stats_pgsql_stat_activity")


@router.get("/runtime_genai_config", response_model=list[RuntimeGenaiConfig], tags=["runtime"])
async def list_runtime_genai_config(conn=Depends(get_admin_conn)):
    """List all rows from `runtime_genai_config`."""
    return await execute_query(conn, "SELECT * FROM runtime_genai_config")


@router.get("/runtime_mysql_servers", response_model=list[RuntimeMysqlServers], tags=["runtime"])
async def list_runtime_mysql_servers(conn=Depends(get_admin_conn)):
    """List all rows from `runtime_mysql_servers`."""
    return await execute_query(conn, "SELECT * FROM runtime_mysql_servers")


@router.get("/runtime_pgsql_servers", response_model=list[RuntimePgsqlServers], tags=["runtime"])
async def list_runtime_pgsql_servers(conn=Depends(get_admin_conn)):
    """List all rows from `runtime_pgsql_servers`."""
    return await execute_query(conn, "SELECT * FROM runtime_pgsql_servers")


@router.get("/stats_mysql_connection_pool", response_model=list[StatsMysqlConnectionPool], tags=["stats"])
async def list_stats_mysql_connection_pool(conn=Depends(get_admin_conn)):
    """List all rows from `stats_mysql_connection_pool`."""
    return await execute_query(conn, "SELECT * FROM stats_mysql_connection_pool")


@router.get("/stats_pgsql_connection_pool", response_model=list[StatsPgsqlConnectionPool], tags=["stats"])
async def list_stats_pgsql_connection_pool(conn=Depends(get_admin_conn)):
    """List all rows from `stats_pgsql_connection_pool`."""
    return await execute_query(conn, "SELECT * FROM stats_pgsql_connection_pool")


@router.get("/runtime_restapi_routes", response_model=list[RuntimeRestapiRoutes], tags=["runtime"])
async def list_runtime_restapi_routes(conn=Depends(get_admin_conn)):
    """List all rows from `runtime_restapi_routes`."""
    return await execute_query(conn, "SELECT * FROM runtime_restapi_routes")


@router.get("/stats_mcp_query_digest_reset", response_model=list[StatsMcpQueryDigestReset], tags=["stats"])
async def list_stats_mcp_query_digest_reset(conn=Depends(get_admin_conn)):
    """List all rows from `stats_mcp_query_digest_reset`."""
    return await execute_query(conn, "SELECT * FROM stats_mcp_query_digest_reset")


@router.get("/stats_mysql_free_connections", response_model=list[StatsMysqlFreeConnections], tags=["stats"])
async def list_stats_mysql_free_connections(conn=Depends(get_admin_conn)):
    """List all rows from `stats_mysql_free_connections`."""
    return await execute_query(conn, "SELECT * FROM stats_mysql_free_connections")


@router.get("/stats_pgsql_free_connections", response_model=list[StatsPgsqlFreeConnections], tags=["stats"])
async def list_stats_pgsql_free_connections(conn=Depends(get_admin_conn)):
    """List all rows from `stats_pgsql_free_connections`."""
    return await execute_query(conn, "SELECT * FROM stats_pgsql_free_connections")


@router.get("/mysql_galera_hostgroups", response_model=list[MysqlGaleraHostgroups], tags=["mysql"])
async def list_mysql_galera_hostgroups(conn=Depends(get_admin_conn)):
    """List all rows from `mysql_galera_hostgroups`."""
    return await execute_query(conn, "SELECT * FROM mysql_galera_hostgroups")


@router.post("/mysql_galera_hostgroups", response_model=dict[str, str], tags=["mysql"])
async def create_mysql_galera_hostgroups(item: MysqlGaleraHostgroupsCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `mysql_galera_hostgroups`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO mysql_galera_hostgroups ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/mysql_galera_hostgroups/{writer_hostgroup}", response_model=MysqlGaleraHostgroups, tags=["mysql"])
async def get_mysql_galera_hostgroups(writer_hostgroup: str, conn=Depends(get_admin_conn)):
    """Get a single row from `mysql_galera_hostgroups` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM mysql_galera_hostgroups WHERE writer_hostgroup = %s", [writer_hostgroup])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/mysql_galera_hostgroups/{writer_hostgroup}", response_model=dict[str, str], tags=["mysql"])
async def delete_mysql_galera_hostgroups(writer_hostgroup: str, conn=Depends(get_admin_conn)):
    """Delete a row from `mysql_galera_hostgroups` by primary key."""
    await execute_modify(conn, "DELETE FROM mysql_galera_hostgroups WHERE writer_hostgroup = %s", [writer_hostgroup])
    return {"status": "ok"}


@router.put("/mysql_galera_hostgroups/{writer_hostgroup}", response_model=dict[str, str], tags=["mysql"])
async def update_mysql_galera_hostgroups(writer_hostgroup: str, item: MysqlGaleraHostgroupsCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `mysql_galera_hostgroups`."""
    data = item.model_dump(exclude_none=True)
    data["writer_hostgroup"] = writer_hostgroup
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO mysql_galera_hostgroups ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/runtime_mcp_query_rules", response_model=list[RuntimeMcpQueryRules], tags=["runtime"])
async def list_runtime_mcp_query_rules(conn=Depends(get_admin_conn)):
    """List all rows from `runtime_mcp_query_rules`."""
    return await execute_query(conn, "SELECT * FROM runtime_mcp_query_rules")


@router.get("/stats_mysql_client_host_cache", response_model=list[StatsMysqlClientHostCache], tags=["stats"])
async def list_stats_mysql_client_host_cache(conn=Depends(get_admin_conn)):
    """List all rows from `stats_mysql_client_host_cache`."""
    return await execute_query(conn, "SELECT * FROM stats_mysql_client_host_cache")


@router.get("/stats_mysql_commands_counters", response_model=list[StatsMysqlCommandsCounters], tags=["stats"])
async def list_stats_mysql_commands_counters(conn=Depends(get_admin_conn)):
    """List all rows from `stats_mysql_commands_counters`."""
    return await execute_query(conn, "SELECT * FROM stats_mysql_commands_counters")


@router.get("/stats_pgsql_client_host_cache", response_model=list[StatsPgsqlClientHostCache], tags=["stats"])
async def list_stats_pgsql_client_host_cache(conn=Depends(get_admin_conn)):
    """List all rows from `stats_pgsql_client_host_cache`."""
    return await execute_query(conn, "SELECT * FROM stats_pgsql_client_host_cache")


@router.get("/stats_pgsql_commands_counters", response_model=list[StatsPgsqlCommandsCounters], tags=["stats"])
async def list_stats_pgsql_commands_counters(conn=Depends(get_admin_conn)):
    """List all rows from `stats_pgsql_commands_counters`."""
    return await execute_query(conn, "SELECT * FROM stats_pgsql_commands_counters")


@router.get("/stats_proxysql_servers_status", response_model=list[StatsProxysqlServersStatus], tags=["stats"])
async def list_stats_proxysql_servers_status(conn=Depends(get_admin_conn)):
    """List all rows from `stats_proxysql_servers_status`."""
    return await execute_query(conn, "SELECT * FROM stats_proxysql_servers_status")


@router.get("/mysql_servers_ssl_params", response_model=list[MysqlServersSslParams], tags=["mysql"])
async def list_mysql_servers_ssl_params(conn=Depends(get_admin_conn)):
    """List all rows from `mysql_servers_ssl_params`."""
    return await execute_query(conn, "SELECT * FROM mysql_servers_ssl_params")


@router.post("/mysql_servers_ssl_params", response_model=dict[str, str], tags=["mysql"])
async def create_mysql_servers_ssl_params(item: MysqlServersSslParamsCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `mysql_servers_ssl_params`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO mysql_servers_ssl_params ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/mysql_servers_ssl_params/{hostname}/{port}/{username}", response_model=MysqlServersSslParams, tags=["mysql"])
async def get_mysql_servers_ssl_params(hostname: str, port: str, username: str, conn=Depends(get_admin_conn)):
    """Get a single row from `mysql_servers_ssl_params` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM mysql_servers_ssl_params WHERE hostname = %s AND port = %s AND username = %s", [hostname, port, username])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/mysql_servers_ssl_params/{hostname}/{port}/{username}", response_model=dict[str, str], tags=["mysql"])
async def delete_mysql_servers_ssl_params(hostname: str, port: str, username: str, conn=Depends(get_admin_conn)):
    """Delete a row from `mysql_servers_ssl_params` by primary key."""
    await execute_modify(conn, "DELETE FROM mysql_servers_ssl_params WHERE hostname = %s AND port = %s AND username = %s", [hostname, port, username])
    return {"status": "ok"}


@router.put("/mysql_servers_ssl_params/{hostname}/{port}/{username}", response_model=dict[str, str], tags=["mysql"])
async def update_mysql_servers_ssl_params(hostname: str, port: str, username: str, item: MysqlServersSslParamsCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `mysql_servers_ssl_params`."""
    data = item.model_dump(exclude_none=True)
    data["hostname"] = hostname
    data["port"] = port
    data["username"] = username
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO mysql_servers_ssl_params ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/pgsql_servers_ssl_params", response_model=list[PgsqlServersSslParams], tags=["pgsql"])
async def list_pgsql_servers_ssl_params(conn=Depends(get_admin_conn)):
    """List all rows from `pgsql_servers_ssl_params`."""
    return await execute_query(conn, "SELECT * FROM pgsql_servers_ssl_params")


@router.post("/pgsql_servers_ssl_params", response_model=dict[str, str], tags=["pgsql"])
async def create_pgsql_servers_ssl_params(item: PgsqlServersSslParamsCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `pgsql_servers_ssl_params`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO pgsql_servers_ssl_params ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/pgsql_servers_ssl_params/{hostname}/{port}/{username}", response_model=PgsqlServersSslParams, tags=["pgsql"])
async def get_pgsql_servers_ssl_params(hostname: str, port: str, username: str, conn=Depends(get_admin_conn)):
    """Get a single row from `pgsql_servers_ssl_params` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM pgsql_servers_ssl_params WHERE hostname = %s AND port = %s AND username = %s", [hostname, port, username])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/pgsql_servers_ssl_params/{hostname}/{port}/{username}", response_model=dict[str, str], tags=["pgsql"])
async def delete_pgsql_servers_ssl_params(hostname: str, port: str, username: str, conn=Depends(get_admin_conn)):
    """Delete a row from `pgsql_servers_ssl_params` by primary key."""
    await execute_modify(conn, "DELETE FROM pgsql_servers_ssl_params WHERE hostname = %s AND port = %s AND username = %s", [hostname, port, username])
    return {"status": "ok"}


@router.put("/pgsql_servers_ssl_params/{hostname}/{port}/{username}", response_model=dict[str, str], tags=["pgsql"])
async def update_pgsql_servers_ssl_params(hostname: str, port: str, username: str, item: PgsqlServersSslParamsCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `pgsql_servers_ssl_params`."""
    data = item.model_dump(exclude_none=True)
    data["hostname"] = hostname
    data["port"] = port
    data["username"] = username
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO pgsql_servers_ssl_params ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/runtime_clickhouse_users", response_model=list[RuntimeClickhouseUsers], tags=["runtime"])
async def list_runtime_clickhouse_users(conn=Depends(get_admin_conn)):
    """List all rows from `runtime_clickhouse_users`."""
    return await execute_query(conn, "SELECT * FROM runtime_clickhouse_users")


@router.get("/runtime_proxysql_servers", response_model=list[RuntimeProxysqlServers], tags=["runtime"])
async def list_runtime_proxysql_servers(conn=Depends(get_admin_conn)):
    """List all rows from `runtime_proxysql_servers`."""
    return await execute_query(conn, "SELECT * FROM runtime_proxysql_servers")


@router.get("/stats_mysql_query_events", response_model=list[StatsMysqlQueryEvents], tags=["stats"])
async def list_stats_mysql_query_events(conn=Depends(get_admin_conn)):
    """List all rows from `stats_mysql_query_events`."""
    return await execute_query(conn, "SELECT * FROM stats_mysql_query_events")


@router.get("/stats_mcp_query_tools_counters", response_model=list[StatsMcpQueryToolsCounters], tags=["stats"])
async def list_stats_mcp_query_tools_counters(conn=Depends(get_admin_conn)):
    """List all rows from `stats_mcp_query_tools_counters`."""
    return await execute_query(conn, "SELECT * FROM stats_mcp_query_tools_counters")


@router.get("/stats_mysql_query_digest_reset", response_model=list[StatsMysqlQueryDigestReset], tags=["stats"])
async def list_stats_mysql_query_digest_reset(conn=Depends(get_admin_conn)):
    """List all rows from `stats_mysql_query_digest_reset`."""
    return await execute_query(conn, "SELECT * FROM stats_mysql_query_digest_reset")


@router.get("/stats_pgsql_query_digest_reset", response_model=list[StatsPgsqlQueryDigestReset], tags=["stats"])
async def list_stats_pgsql_query_digest_reset(conn=Depends(get_admin_conn)):
    """List all rows from `stats_pgsql_query_digest_reset`."""
    return await execute_query(conn, "SELECT * FROM stats_pgsql_query_digest_reset")


@router.get("/stats_proxysql_message_metrics", response_model=list[StatsProxysqlMessageMetrics], tags=["stats"])
async def list_stats_proxysql_message_metrics(conn=Depends(get_admin_conn)):
    """List all rows from `stats_proxysql_message_metrics`."""
    return await execute_query(conn, "SELECT * FROM stats_proxysql_message_metrics")


@router.get("/stats_proxysql_servers_metrics", response_model=list[StatsProxysqlServersMetrics], tags=["stats"])
async def list_stats_proxysql_servers_metrics(conn=Depends(get_admin_conn)):
    """List all rows from `stats_proxysql_servers_metrics`."""
    return await execute_query(conn, "SELECT * FROM stats_proxysql_servers_metrics")


@router.get("/runtime_mcp_auth_profiles", response_model=list[RuntimeMcpAuthProfiles], tags=["runtime"])
async def list_runtime_mcp_auth_profiles(conn=Depends(get_admin_conn)):
    """List all rows from `runtime_mcp_auth_profiles`."""
    return await execute_query(conn, "SELECT * FROM runtime_mcp_auth_profiles")


@router.get("/runtime_mysql_query_rules", response_model=list[RuntimeMysqlQueryRules], tags=["runtime"])
async def list_runtime_mysql_query_rules(conn=Depends(get_admin_conn)):
    """List all rows from `runtime_mysql_query_rules`."""
    return await execute_query(conn, "SELECT * FROM runtime_mysql_query_rules")


@router.get("/runtime_pgsql_query_rules", response_model=list[RuntimePgsqlQueryRules], tags=["runtime"])
async def list_runtime_pgsql_query_rules(conn=Depends(get_admin_conn)):
    """List all rows from `runtime_pgsql_query_rules`."""
    return await execute_query(conn, "SELECT * FROM runtime_pgsql_query_rules")


@router.get("/mysql_hostgroup_attributes", response_model=list[MysqlHostgroupAttributes], tags=["mysql"])
async def list_mysql_hostgroup_attributes(conn=Depends(get_admin_conn)):
    """List all rows from `mysql_hostgroup_attributes`."""
    return await execute_query(conn, "SELECT * FROM mysql_hostgroup_attributes")


@router.post("/mysql_hostgroup_attributes", response_model=dict[str, str], tags=["mysql"])
async def create_mysql_hostgroup_attributes(item: MysqlHostgroupAttributesCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `mysql_hostgroup_attributes`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO mysql_hostgroup_attributes ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/mysql_hostgroup_attributes/{hostgroup_id}", response_model=MysqlHostgroupAttributes, tags=["mysql"])
async def get_mysql_hostgroup_attributes(hostgroup_id: str, conn=Depends(get_admin_conn)):
    """Get a single row from `mysql_hostgroup_attributes` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM mysql_hostgroup_attributes WHERE hostgroup_id = %s", [hostgroup_id])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/mysql_hostgroup_attributes/{hostgroup_id}", response_model=dict[str, str], tags=["mysql"])
async def delete_mysql_hostgroup_attributes(hostgroup_id: str, conn=Depends(get_admin_conn)):
    """Delete a row from `mysql_hostgroup_attributes` by primary key."""
    await execute_modify(conn, "DELETE FROM mysql_hostgroup_attributes WHERE hostgroup_id = %s", [hostgroup_id])
    return {"status": "ok"}


@router.put("/mysql_hostgroup_attributes/{hostgroup_id}", response_model=dict[str, str], tags=["mysql"])
async def update_mysql_hostgroup_attributes(hostgroup_id: str, item: MysqlHostgroupAttributesCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `mysql_hostgroup_attributes`."""
    data = item.model_dump(exclude_none=True)
    data["hostgroup_id"] = hostgroup_id
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO mysql_hostgroup_attributes ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/pgsql_hostgroup_attributes", response_model=list[PgsqlHostgroupAttributes], tags=["pgsql"])
async def list_pgsql_hostgroup_attributes(conn=Depends(get_admin_conn)):
    """List all rows from `pgsql_hostgroup_attributes`."""
    return await execute_query(conn, "SELECT * FROM pgsql_hostgroup_attributes")


@router.post("/pgsql_hostgroup_attributes", response_model=dict[str, str], tags=["pgsql"])
async def create_pgsql_hostgroup_attributes(item: PgsqlHostgroupAttributesCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `pgsql_hostgroup_attributes`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO pgsql_hostgroup_attributes ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/pgsql_hostgroup_attributes/{hostgroup_id}", response_model=PgsqlHostgroupAttributes, tags=["pgsql"])
async def get_pgsql_hostgroup_attributes(hostgroup_id: str, conn=Depends(get_admin_conn)):
    """Get a single row from `pgsql_hostgroup_attributes` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM pgsql_hostgroup_attributes WHERE hostgroup_id = %s", [hostgroup_id])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/pgsql_hostgroup_attributes/{hostgroup_id}", response_model=dict[str, str], tags=["pgsql"])
async def delete_pgsql_hostgroup_attributes(hostgroup_id: str, conn=Depends(get_admin_conn)):
    """Delete a row from `pgsql_hostgroup_attributes` by primary key."""
    await execute_modify(conn, "DELETE FROM pgsql_hostgroup_attributes WHERE hostgroup_id = %s", [hostgroup_id])
    return {"status": "ok"}


@router.put("/pgsql_hostgroup_attributes/{hostgroup_id}", response_model=dict[str, str], tags=["pgsql"])
async def update_pgsql_hostgroup_attributes(hostgroup_id: str, item: PgsqlHostgroupAttributesCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `pgsql_hostgroup_attributes`."""
    data = item.model_dump(exclude_none=True)
    data["hostgroup_id"] = hostgroup_id
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO pgsql_hostgroup_attributes ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/runtime_mysql_ldap_mapping", response_model=list[RuntimeMysqlLdapMapping], tags=["runtime"])
async def list_runtime_mysql_ldap_mapping(conn=Depends(get_admin_conn)):
    """List all rows from `runtime_mysql_ldap_mapping`."""
    return await execute_query(conn, "SELECT * FROM runtime_mysql_ldap_mapping")


@router.get("/runtime_pgsql_ldap_mapping", response_model=list[RuntimePgsqlLdapMapping], tags=["runtime"])
async def list_runtime_pgsql_ldap_mapping(conn=Depends(get_admin_conn)):
    """List all rows from `runtime_pgsql_ldap_mapping`."""
    return await execute_query(conn, "SELECT * FROM runtime_pgsql_ldap_mapping")


@router.get("/stats_proxysql_servers_checksums", response_model=list[StatsProxysqlServersChecksums], tags=["stats"])
async def list_stats_proxysql_servers_checksums(conn=Depends(get_admin_conn)):
    """List all rows from `stats_proxysql_servers_checksums`."""
    return await execute_query(conn, "SELECT * FROM stats_proxysql_servers_checksums")


@router.get("/mysql_aws_aurora_hostgroups", response_model=list[MysqlAwsAuroraHostgroups], tags=["mysql"])
async def list_mysql_aws_aurora_hostgroups(conn=Depends(get_admin_conn)):
    """List all rows from `mysql_aws_aurora_hostgroups`."""
    return await execute_query(conn, "SELECT * FROM mysql_aws_aurora_hostgroups")


@router.post("/mysql_aws_aurora_hostgroups", response_model=dict[str, str], tags=["mysql"])
async def create_mysql_aws_aurora_hostgroups(item: MysqlAwsAuroraHostgroupsCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `mysql_aws_aurora_hostgroups`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO mysql_aws_aurora_hostgroups ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/mysql_aws_aurora_hostgroups/{writer_hostgroup}", response_model=MysqlAwsAuroraHostgroups, tags=["mysql"])
async def get_mysql_aws_aurora_hostgroups(writer_hostgroup: str, conn=Depends(get_admin_conn)):
    """Get a single row from `mysql_aws_aurora_hostgroups` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM mysql_aws_aurora_hostgroups WHERE writer_hostgroup = %s", [writer_hostgroup])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/mysql_aws_aurora_hostgroups/{writer_hostgroup}", response_model=dict[str, str], tags=["mysql"])
async def delete_mysql_aws_aurora_hostgroups(writer_hostgroup: str, conn=Depends(get_admin_conn)):
    """Delete a row from `mysql_aws_aurora_hostgroups` by primary key."""
    await execute_modify(conn, "DELETE FROM mysql_aws_aurora_hostgroups WHERE writer_hostgroup = %s", [writer_hostgroup])
    return {"status": "ok"}


@router.put("/mysql_aws_aurora_hostgroups/{writer_hostgroup}", response_model=dict[str, str], tags=["mysql"])
async def update_mysql_aws_aurora_hostgroups(writer_hostgroup: str, item: MysqlAwsAuroraHostgroupsCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `mysql_aws_aurora_hostgroups`."""
    data = item.model_dump(exclude_none=True)
    data["writer_hostgroup"] = writer_hostgroup
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO mysql_aws_aurora_hostgroups ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/runtime_mcp_target_profiles", response_model=list[RuntimeMcpTargetProfiles], tags=["runtime"])
async def list_runtime_mcp_target_profiles(conn=Depends(get_admin_conn)):
    """List all rows from `runtime_mcp_target_profiles`."""
    return await execute_query(conn, "SELECT * FROM runtime_mcp_target_profiles")


@router.get("/stats_mysql_connection_pool_reset", response_model=list[StatsMysqlConnectionPoolReset], tags=["stats"])
async def list_stats_mysql_connection_pool_reset(conn=Depends(get_admin_conn)):
    """List all rows from `stats_mysql_connection_pool_reset`."""
    return await execute_query(conn, "SELECT * FROM stats_mysql_connection_pool_reset")


@router.get("/stats_pgsql_connection_pool_reset", response_model=list[StatsPgsqlConnectionPoolReset], tags=["stats"])
async def list_stats_pgsql_connection_pool_reset(conn=Depends(get_admin_conn)):
    """List all rows from `stats_pgsql_connection_pool_reset`."""
    return await execute_query(conn, "SELECT * FROM stats_pgsql_connection_pool_reset")


@router.get("/mysql_replication_hostgroups", response_model=list[MysqlReplicationHostgroups], tags=["mysql"])
async def list_mysql_replication_hostgroups(conn=Depends(get_admin_conn)):
    """List all rows from `mysql_replication_hostgroups`."""
    return await execute_query(conn, "SELECT * FROM mysql_replication_hostgroups")


@router.post("/mysql_replication_hostgroups", response_model=dict[str, str], tags=["mysql"])
async def create_mysql_replication_hostgroups(item: MysqlReplicationHostgroupsCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `mysql_replication_hostgroups`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO mysql_replication_hostgroups ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/mysql_replication_hostgroups/{writer_hostgroup}", response_model=MysqlReplicationHostgroups, tags=["mysql"])
async def get_mysql_replication_hostgroups(writer_hostgroup: str, conn=Depends(get_admin_conn)):
    """Get a single row from `mysql_replication_hostgroups` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM mysql_replication_hostgroups WHERE writer_hostgroup = %s", [writer_hostgroup])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/mysql_replication_hostgroups/{writer_hostgroup}", response_model=dict[str, str], tags=["mysql"])
async def delete_mysql_replication_hostgroups(writer_hostgroup: str, conn=Depends(get_admin_conn)):
    """Delete a row from `mysql_replication_hostgroups` by primary key."""
    await execute_modify(conn, "DELETE FROM mysql_replication_hostgroups WHERE writer_hostgroup = %s", [writer_hostgroup])
    return {"status": "ok"}


@router.put("/mysql_replication_hostgroups/{writer_hostgroup}", response_model=dict[str, str], tags=["mysql"])
async def update_mysql_replication_hostgroups(writer_hostgroup: str, item: MysqlReplicationHostgroupsCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `mysql_replication_hostgroups`."""
    data = item.model_dump(exclude_none=True)
    data["writer_hostgroup"] = writer_hostgroup
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO mysql_replication_hostgroups ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/pgsql_replication_hostgroups", response_model=list[PgsqlReplicationHostgroups], tags=["pgsql"])
async def list_pgsql_replication_hostgroups(conn=Depends(get_admin_conn)):
    """List all rows from `pgsql_replication_hostgroups`."""
    return await execute_query(conn, "SELECT * FROM pgsql_replication_hostgroups")


@router.post("/pgsql_replication_hostgroups", response_model=dict[str, str], tags=["pgsql"])
async def create_pgsql_replication_hostgroups(item: PgsqlReplicationHostgroupsCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `pgsql_replication_hostgroups`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO pgsql_replication_hostgroups ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/pgsql_replication_hostgroups/{writer_hostgroup}", response_model=PgsqlReplicationHostgroups, tags=["pgsql"])
async def get_pgsql_replication_hostgroups(writer_hostgroup: str, conn=Depends(get_admin_conn)):
    """Get a single row from `pgsql_replication_hostgroups` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM pgsql_replication_hostgroups WHERE writer_hostgroup = %s", [writer_hostgroup])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/pgsql_replication_hostgroups/{writer_hostgroup}", response_model=dict[str, str], tags=["pgsql"])
async def delete_pgsql_replication_hostgroups(writer_hostgroup: str, conn=Depends(get_admin_conn)):
    """Delete a row from `pgsql_replication_hostgroups` by primary key."""
    await execute_modify(conn, "DELETE FROM pgsql_replication_hostgroups WHERE writer_hostgroup = %s", [writer_hostgroup])
    return {"status": "ok"}


@router.put("/pgsql_replication_hostgroups/{writer_hostgroup}", response_model=dict[str, str], tags=["pgsql"])
async def update_pgsql_replication_hostgroups(writer_hostgroup: str, item: PgsqlReplicationHostgroupsCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `pgsql_replication_hostgroups`."""
    data = item.model_dump(exclude_none=True)
    data["writer_hostgroup"] = writer_hostgroup
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO pgsql_replication_hostgroups ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/stats_mysql_client_host_cache_reset", response_model=list[StatsMysqlClientHostCacheReset], tags=["stats"])
async def list_stats_mysql_client_host_cache_reset(conn=Depends(get_admin_conn)):
    """List all rows from `stats_mysql_client_host_cache_reset`."""
    return await execute_query(conn, "SELECT * FROM stats_mysql_client_host_cache_reset")


@router.get("/stats_pgsql_client_host_cache_reset", response_model=list[StatsPgsqlClientHostCacheReset], tags=["stats"])
async def list_stats_pgsql_client_host_cache_reset(conn=Depends(get_admin_conn)):
    """List all rows from `stats_pgsql_client_host_cache_reset`."""
    return await execute_query(conn, "SELECT * FROM stats_pgsql_client_host_cache_reset")


@router.get("/mysql_firewall_whitelist_rules", response_model=list[MysqlFirewallWhitelistRules], tags=["mysql"])
async def list_mysql_firewall_whitelist_rules(conn=Depends(get_admin_conn)):
    """List all rows from `mysql_firewall_whitelist_rules`."""
    return await execute_query(conn, "SELECT * FROM mysql_firewall_whitelist_rules")


@router.post("/mysql_firewall_whitelist_rules", response_model=dict[str, str], tags=["mysql"])
async def create_mysql_firewall_whitelist_rules(item: MysqlFirewallWhitelistRulesCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `mysql_firewall_whitelist_rules`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO mysql_firewall_whitelist_rules ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/mysql_firewall_whitelist_rules/{username}/{client_address}/{schemaname}/{flagIN}/{digest}", response_model=MysqlFirewallWhitelistRules, tags=["mysql"])
async def get_mysql_firewall_whitelist_rules(username: str, client_address: str, schemaname: str, flagIN: str, digest: str, conn=Depends(get_admin_conn)):
    """Get a single row from `mysql_firewall_whitelist_rules` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM mysql_firewall_whitelist_rules WHERE username = %s AND client_address = %s AND schemaname = %s AND flagIN = %s AND digest = %s", [username, client_address, schemaname, flagIN, digest])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/mysql_firewall_whitelist_rules/{username}/{client_address}/{schemaname}/{flagIN}/{digest}", response_model=dict[str, str], tags=["mysql"])
async def delete_mysql_firewall_whitelist_rules(username: str, client_address: str, schemaname: str, flagIN: str, digest: str, conn=Depends(get_admin_conn)):
    """Delete a row from `mysql_firewall_whitelist_rules` by primary key."""
    await execute_modify(conn, "DELETE FROM mysql_firewall_whitelist_rules WHERE username = %s AND client_address = %s AND schemaname = %s AND flagIN = %s AND digest = %s", [username, client_address, schemaname, flagIN, digest])
    return {"status": "ok"}


@router.put("/mysql_firewall_whitelist_rules/{username}/{client_address}/{schemaname}/{flagIN}/{digest}", response_model=dict[str, str], tags=["mysql"])
async def update_mysql_firewall_whitelist_rules(username: str, client_address: str, schemaname: str, flagIN: str, digest: str, item: MysqlFirewallWhitelistRulesCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `mysql_firewall_whitelist_rules`."""
    data = item.model_dump(exclude_none=True)
    data["username"] = username
    data["client_address"] = client_address
    data["schemaname"] = schemaname
    data["flagIN"] = flagIN
    data["digest"] = digest
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO mysql_firewall_whitelist_rules ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/mysql_firewall_whitelist_users", response_model=list[MysqlFirewallWhitelistUsers], tags=["mysql"])
async def list_mysql_firewall_whitelist_users(conn=Depends(get_admin_conn)):
    """List all rows from `mysql_firewall_whitelist_users`."""
    return await execute_query(conn, "SELECT * FROM mysql_firewall_whitelist_users")


@router.post("/mysql_firewall_whitelist_users", response_model=dict[str, str], tags=["mysql"])
async def create_mysql_firewall_whitelist_users(item: MysqlFirewallWhitelistUsersCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `mysql_firewall_whitelist_users`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO mysql_firewall_whitelist_users ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/mysql_firewall_whitelist_users/{username}/{client_address}", response_model=MysqlFirewallWhitelistUsers, tags=["mysql"])
async def get_mysql_firewall_whitelist_users(username: str, client_address: str, conn=Depends(get_admin_conn)):
    """Get a single row from `mysql_firewall_whitelist_users` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM mysql_firewall_whitelist_users WHERE username = %s AND client_address = %s", [username, client_address])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/mysql_firewall_whitelist_users/{username}/{client_address}", response_model=dict[str, str], tags=["mysql"])
async def delete_mysql_firewall_whitelist_users(username: str, client_address: str, conn=Depends(get_admin_conn)):
    """Delete a row from `mysql_firewall_whitelist_users` by primary key."""
    await execute_modify(conn, "DELETE FROM mysql_firewall_whitelist_users WHERE username = %s AND client_address = %s", [username, client_address])
    return {"status": "ok"}


@router.put("/mysql_firewall_whitelist_users/{username}/{client_address}", response_model=dict[str, str], tags=["mysql"])
async def update_mysql_firewall_whitelist_users(username: str, client_address: str, item: MysqlFirewallWhitelistUsersCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `mysql_firewall_whitelist_users`."""
    data = item.model_dump(exclude_none=True)
    data["username"] = username
    data["client_address"] = client_address
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO mysql_firewall_whitelist_users ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/mysql_query_rules_fast_routing", response_model=list[MysqlQueryRulesFastRouting], tags=["mysql"])
async def list_mysql_query_rules_fast_routing(conn=Depends(get_admin_conn)):
    """List all rows from `mysql_query_rules_fast_routing`."""
    return await execute_query(conn, "SELECT * FROM mysql_query_rules_fast_routing")


@router.post("/mysql_query_rules_fast_routing", response_model=dict[str, str], tags=["mysql"])
async def create_mysql_query_rules_fast_routing(item: MysqlQueryRulesFastRoutingCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `mysql_query_rules_fast_routing`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO mysql_query_rules_fast_routing ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/mysql_query_rules_fast_routing/{username}/{schemaname}/{flagIN}", response_model=MysqlQueryRulesFastRouting, tags=["mysql"])
async def get_mysql_query_rules_fast_routing(username: str, schemaname: str, flagIN: str, conn=Depends(get_admin_conn)):
    """Get a single row from `mysql_query_rules_fast_routing` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM mysql_query_rules_fast_routing WHERE username = %s AND schemaname = %s AND flagIN = %s", [username, schemaname, flagIN])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/mysql_query_rules_fast_routing/{username}/{schemaname}/{flagIN}", response_model=dict[str, str], tags=["mysql"])
async def delete_mysql_query_rules_fast_routing(username: str, schemaname: str, flagIN: str, conn=Depends(get_admin_conn)):
    """Delete a row from `mysql_query_rules_fast_routing` by primary key."""
    await execute_modify(conn, "DELETE FROM mysql_query_rules_fast_routing WHERE username = %s AND schemaname = %s AND flagIN = %s", [username, schemaname, flagIN])
    return {"status": "ok"}


@router.put("/mysql_query_rules_fast_routing/{username}/{schemaname}/{flagIN}", response_model=dict[str, str], tags=["mysql"])
async def update_mysql_query_rules_fast_routing(username: str, schemaname: str, flagIN: str, item: MysqlQueryRulesFastRoutingCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `mysql_query_rules_fast_routing`."""
    data = item.model_dump(exclude_none=True)
    data["username"] = username
    data["schemaname"] = schemaname
    data["flagIN"] = flagIN
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO mysql_query_rules_fast_routing ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/pgsql_firewall_whitelist_rules", response_model=list[PgsqlFirewallWhitelistRules], tags=["pgsql"])
async def list_pgsql_firewall_whitelist_rules(conn=Depends(get_admin_conn)):
    """List all rows from `pgsql_firewall_whitelist_rules`."""
    return await execute_query(conn, "SELECT * FROM pgsql_firewall_whitelist_rules")


@router.post("/pgsql_firewall_whitelist_rules", response_model=dict[str, str], tags=["pgsql"])
async def create_pgsql_firewall_whitelist_rules(item: PgsqlFirewallWhitelistRulesCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `pgsql_firewall_whitelist_rules`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO pgsql_firewall_whitelist_rules ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/pgsql_firewall_whitelist_rules/{username}/{client_address}/{database}/{flagIN}/{digest}", response_model=PgsqlFirewallWhitelistRules, tags=["pgsql"])
async def get_pgsql_firewall_whitelist_rules(username: str, client_address: str, database: str, flagIN: str, digest: str, conn=Depends(get_admin_conn)):
    """Get a single row from `pgsql_firewall_whitelist_rules` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM pgsql_firewall_whitelist_rules WHERE username = %s AND client_address = %s AND database = %s AND flagIN = %s AND digest = %s", [username, client_address, database, flagIN, digest])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/pgsql_firewall_whitelist_rules/{username}/{client_address}/{database}/{flagIN}/{digest}", response_model=dict[str, str], tags=["pgsql"])
async def delete_pgsql_firewall_whitelist_rules(username: str, client_address: str, database: str, flagIN: str, digest: str, conn=Depends(get_admin_conn)):
    """Delete a row from `pgsql_firewall_whitelist_rules` by primary key."""
    await execute_modify(conn, "DELETE FROM pgsql_firewall_whitelist_rules WHERE username = %s AND client_address = %s AND database = %s AND flagIN = %s AND digest = %s", [username, client_address, database, flagIN, digest])
    return {"status": "ok"}


@router.put("/pgsql_firewall_whitelist_rules/{username}/{client_address}/{database}/{flagIN}/{digest}", response_model=dict[str, str], tags=["pgsql"])
async def update_pgsql_firewall_whitelist_rules(username: str, client_address: str, database: str, flagIN: str, digest: str, item: PgsqlFirewallWhitelistRulesCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `pgsql_firewall_whitelist_rules`."""
    data = item.model_dump(exclude_none=True)
    data["username"] = username
    data["client_address"] = client_address
    data["database"] = database
    data["flagIN"] = flagIN
    data["digest"] = digest
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO pgsql_firewall_whitelist_rules ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/pgsql_firewall_whitelist_users", response_model=list[PgsqlFirewallWhitelistUsers], tags=["pgsql"])
async def list_pgsql_firewall_whitelist_users(conn=Depends(get_admin_conn)):
    """List all rows from `pgsql_firewall_whitelist_users`."""
    return await execute_query(conn, "SELECT * FROM pgsql_firewall_whitelist_users")


@router.post("/pgsql_firewall_whitelist_users", response_model=dict[str, str], tags=["pgsql"])
async def create_pgsql_firewall_whitelist_users(item: PgsqlFirewallWhitelistUsersCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `pgsql_firewall_whitelist_users`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO pgsql_firewall_whitelist_users ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/pgsql_firewall_whitelist_users/{username}/{client_address}", response_model=PgsqlFirewallWhitelistUsers, tags=["pgsql"])
async def get_pgsql_firewall_whitelist_users(username: str, client_address: str, conn=Depends(get_admin_conn)):
    """Get a single row from `pgsql_firewall_whitelist_users` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM pgsql_firewall_whitelist_users WHERE username = %s AND client_address = %s", [username, client_address])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/pgsql_firewall_whitelist_users/{username}/{client_address}", response_model=dict[str, str], tags=["pgsql"])
async def delete_pgsql_firewall_whitelist_users(username: str, client_address: str, conn=Depends(get_admin_conn)):
    """Delete a row from `pgsql_firewall_whitelist_users` by primary key."""
    await execute_modify(conn, "DELETE FROM pgsql_firewall_whitelist_users WHERE username = %s AND client_address = %s", [username, client_address])
    return {"status": "ok"}


@router.put("/pgsql_firewall_whitelist_users/{username}/{client_address}", response_model=dict[str, str], tags=["pgsql"])
async def update_pgsql_firewall_whitelist_users(username: str, client_address: str, item: PgsqlFirewallWhitelistUsersCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `pgsql_firewall_whitelist_users`."""
    data = item.model_dump(exclude_none=True)
    data["username"] = username
    data["client_address"] = client_address
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO pgsql_firewall_whitelist_users ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/pgsql_query_rules_fast_routing", response_model=list[PgsqlQueryRulesFastRouting], tags=["pgsql"])
async def list_pgsql_query_rules_fast_routing(conn=Depends(get_admin_conn)):
    """List all rows from `pgsql_query_rules_fast_routing`."""
    return await execute_query(conn, "SELECT * FROM pgsql_query_rules_fast_routing")


@router.post("/pgsql_query_rules_fast_routing", response_model=dict[str, str], tags=["pgsql"])
async def create_pgsql_query_rules_fast_routing(item: PgsqlQueryRulesFastRoutingCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `pgsql_query_rules_fast_routing`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO pgsql_query_rules_fast_routing ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/pgsql_query_rules_fast_routing/{username}/{database}/{flagIN}", response_model=PgsqlQueryRulesFastRouting, tags=["pgsql"])
async def get_pgsql_query_rules_fast_routing(username: str, database: str, flagIN: str, conn=Depends(get_admin_conn)):
    """Get a single row from `pgsql_query_rules_fast_routing` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM pgsql_query_rules_fast_routing WHERE username = %s AND database = %s AND flagIN = %s", [username, database, flagIN])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/pgsql_query_rules_fast_routing/{username}/{database}/{flagIN}", response_model=dict[str, str], tags=["pgsql"])
async def delete_pgsql_query_rules_fast_routing(username: str, database: str, flagIN: str, conn=Depends(get_admin_conn)):
    """Delete a row from `pgsql_query_rules_fast_routing` by primary key."""
    await execute_modify(conn, "DELETE FROM pgsql_query_rules_fast_routing WHERE username = %s AND database = %s AND flagIN = %s", [username, database, flagIN])
    return {"status": "ok"}


@router.put("/pgsql_query_rules_fast_routing/{username}/{database}/{flagIN}", response_model=dict[str, str], tags=["pgsql"])
async def update_pgsql_query_rules_fast_routing(username: str, database: str, flagIN: str, item: PgsqlQueryRulesFastRoutingCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `pgsql_query_rules_fast_routing`."""
    data = item.model_dump(exclude_none=True)
    data["username"] = username
    data["database"] = database
    data["flagIN"] = flagIN
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO pgsql_query_rules_fast_routing ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/stats_mcp_query_tools_counters_reset", response_model=list[StatsMcpQueryToolsCountersReset], tags=["stats"])
async def list_stats_mcp_query_tools_counters_reset(conn=Depends(get_admin_conn)):
    """List all rows from `stats_mcp_query_tools_counters_reset`."""
    return await execute_query(conn, "SELECT * FROM stats_mcp_query_tools_counters_reset")


@router.get("/stats_pgsql_prepared_statements_info", response_model=list[StatsPgsqlPreparedStatementsInfo], tags=["stats"])
async def list_stats_pgsql_prepared_statements_info(conn=Depends(get_admin_conn)):
    """List all rows from `stats_pgsql_prepared_statements_info`."""
    return await execute_query(conn, "SELECT * FROM stats_pgsql_prepared_statements_info")


@router.get("/stats_proxysql_message_metrics_reset", response_model=list[StatsProxysqlMessageMetricsReset], tags=["stats"])
async def list_stats_proxysql_message_metrics_reset(conn=Depends(get_admin_conn)):
    """List all rows from `stats_proxysql_message_metrics_reset`."""
    return await execute_query(conn, "SELECT * FROM stats_proxysql_message_metrics_reset")


@router.get("/runtime_mysql_galera_hostgroups", response_model=list[RuntimeMysqlGaleraHostgroups], tags=["runtime"])
async def list_runtime_mysql_galera_hostgroups(conn=Depends(get_admin_conn)):
    """List all rows from `runtime_mysql_galera_hostgroups`."""
    return await execute_query(conn, "SELECT * FROM runtime_mysql_galera_hostgroups")


@router.get("/stats_proxysql_servers_clients_status", response_model=list[StatsProxysqlServersClientsStatus], tags=["stats"])
async def list_stats_proxysql_servers_clients_status(conn=Depends(get_admin_conn)):
    """List all rows from `stats_proxysql_servers_clients_status`."""
    return await execute_query(conn, "SELECT * FROM stats_proxysql_servers_clients_status")


@router.get("/runtime_mysql_servers_ssl_params", response_model=list[RuntimeMysqlServersSslParams], tags=["runtime"])
async def list_runtime_mysql_servers_ssl_params(conn=Depends(get_admin_conn)):
    """List all rows from `runtime_mysql_servers_ssl_params`."""
    return await execute_query(conn, "SELECT * FROM runtime_mysql_servers_ssl_params")


@router.get("/runtime_pgsql_servers_ssl_params", response_model=list[RuntimePgsqlServersSslParams], tags=["runtime"])
async def list_runtime_pgsql_servers_ssl_params(conn=Depends(get_admin_conn)):
    """List all rows from `runtime_pgsql_servers_ssl_params`."""
    return await execute_query(conn, "SELECT * FROM runtime_pgsql_servers_ssl_params")


@router.get("/mysql_group_replication_hostgroups", response_model=list[MysqlGroupReplicationHostgroups], tags=["mysql"])
async def list_mysql_group_replication_hostgroups(conn=Depends(get_admin_conn)):
    """List all rows from `mysql_group_replication_hostgroups`."""
    return await execute_query(conn, "SELECT * FROM mysql_group_replication_hostgroups")


@router.post("/mysql_group_replication_hostgroups", response_model=dict[str, str], tags=["mysql"])
async def create_mysql_group_replication_hostgroups(item: MysqlGroupReplicationHostgroupsCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `mysql_group_replication_hostgroups`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO mysql_group_replication_hostgroups ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/mysql_group_replication_hostgroups/{writer_hostgroup}", response_model=MysqlGroupReplicationHostgroups, tags=["mysql"])
async def get_mysql_group_replication_hostgroups(writer_hostgroup: str, conn=Depends(get_admin_conn)):
    """Get a single row from `mysql_group_replication_hostgroups` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM mysql_group_replication_hostgroups WHERE writer_hostgroup = %s", [writer_hostgroup])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/mysql_group_replication_hostgroups/{writer_hostgroup}", response_model=dict[str, str], tags=["mysql"])
async def delete_mysql_group_replication_hostgroups(writer_hostgroup: str, conn=Depends(get_admin_conn)):
    """Delete a row from `mysql_group_replication_hostgroups` by primary key."""
    await execute_modify(conn, "DELETE FROM mysql_group_replication_hostgroups WHERE writer_hostgroup = %s", [writer_hostgroup])
    return {"status": "ok"}


@router.put("/mysql_group_replication_hostgroups/{writer_hostgroup}", response_model=dict[str, str], tags=["mysql"])
async def update_mysql_group_replication_hostgroups(writer_hostgroup: str, item: MysqlGroupReplicationHostgroupsCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `mysql_group_replication_hostgroups`."""
    data = item.model_dump(exclude_none=True)
    data["writer_hostgroup"] = writer_hostgroup
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO mysql_group_replication_hostgroups ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/runtime_mysql_hostgroup_attributes", response_model=list[RuntimeMysqlHostgroupAttributes], tags=["runtime"])
async def list_runtime_mysql_hostgroup_attributes(conn=Depends(get_admin_conn)):
    """List all rows from `runtime_mysql_hostgroup_attributes`."""
    return await execute_query(conn, "SELECT * FROM runtime_mysql_hostgroup_attributes")


@router.get("/runtime_pgsql_hostgroup_attributes", response_model=list[RuntimePgsqlHostgroupAttributes], tags=["runtime"])
async def list_runtime_pgsql_hostgroup_attributes(conn=Depends(get_admin_conn)):
    """List all rows from `runtime_pgsql_hostgroup_attributes`."""
    return await execute_query(conn, "SELECT * FROM runtime_pgsql_hostgroup_attributes")


@router.get("/runtime_mysql_aws_aurora_hostgroups", response_model=list[RuntimeMysqlAwsAuroraHostgroups], tags=["runtime"])
async def list_runtime_mysql_aws_aurora_hostgroups(conn=Depends(get_admin_conn)):
    """List all rows from `runtime_mysql_aws_aurora_hostgroups`."""
    return await execute_query(conn, "SELECT * FROM runtime_mysql_aws_aurora_hostgroups")


@router.get("/runtime_mysql_replication_hostgroups", response_model=list[RuntimeMysqlReplicationHostgroups], tags=["runtime"])
async def list_runtime_mysql_replication_hostgroups(conn=Depends(get_admin_conn)):
    """List all rows from `runtime_mysql_replication_hostgroups`."""
    return await execute_query(conn, "SELECT * FROM runtime_mysql_replication_hostgroups")


@router.get("/runtime_pgsql_replication_hostgroups", response_model=list[RuntimePgsqlReplicationHostgroups], tags=["runtime"])
async def list_runtime_pgsql_replication_hostgroups(conn=Depends(get_admin_conn)):
    """List all rows from `runtime_pgsql_replication_hostgroups`."""
    return await execute_query(conn, "SELECT * FROM runtime_pgsql_replication_hostgroups")


@router.get("/stats_mysql_prepared_statements_info", response_model=list[StatsMysqlPreparedStatementsInfo], tags=["stats"])
async def list_stats_mysql_prepared_statements_info(conn=Depends(get_admin_conn)):
    """List all rows from `stats_mysql_prepared_statements_info`."""
    return await execute_query(conn, "SELECT * FROM stats_mysql_prepared_statements_info")


@router.get("/runtime_mysql_firewall_whitelist_rules", response_model=list[RuntimeMysqlFirewallWhitelistRules], tags=["runtime"])
async def list_runtime_mysql_firewall_whitelist_rules(conn=Depends(get_admin_conn)):
    """List all rows from `runtime_mysql_firewall_whitelist_rules`."""
    return await execute_query(conn, "SELECT * FROM runtime_mysql_firewall_whitelist_rules")


@router.get("/runtime_mysql_firewall_whitelist_users", response_model=list[RuntimeMysqlFirewallWhitelistUsers], tags=["runtime"])
async def list_runtime_mysql_firewall_whitelist_users(conn=Depends(get_admin_conn)):
    """List all rows from `runtime_mysql_firewall_whitelist_users`."""
    return await execute_query(conn, "SELECT * FROM runtime_mysql_firewall_whitelist_users")


@router.get("/runtime_mysql_query_rules_fast_routing", response_model=list[RuntimeMysqlQueryRulesFastRouting], tags=["runtime"])
async def list_runtime_mysql_query_rules_fast_routing(conn=Depends(get_admin_conn)):
    """List all rows from `runtime_mysql_query_rules_fast_routing`."""
    return await execute_query(conn, "SELECT * FROM runtime_mysql_query_rules_fast_routing")


@router.get("/runtime_pgsql_firewall_whitelist_rules", response_model=list[RuntimePgsqlFirewallWhitelistRules], tags=["runtime"])
async def list_runtime_pgsql_firewall_whitelist_rules(conn=Depends(get_admin_conn)):
    """List all rows from `runtime_pgsql_firewall_whitelist_rules`."""
    return await execute_query(conn, "SELECT * FROM runtime_pgsql_firewall_whitelist_rules")


@router.get("/runtime_pgsql_firewall_whitelist_users", response_model=list[RuntimePgsqlFirewallWhitelistUsers], tags=["runtime"])
async def list_runtime_pgsql_firewall_whitelist_users(conn=Depends(get_admin_conn)):
    """List all rows from `runtime_pgsql_firewall_whitelist_users`."""
    return await execute_query(conn, "SELECT * FROM runtime_pgsql_firewall_whitelist_users")


@router.get("/runtime_pgsql_query_rules_fast_routing", response_model=list[RuntimePgsqlQueryRulesFastRouting], tags=["runtime"])
async def list_runtime_pgsql_query_rules_fast_routing(conn=Depends(get_admin_conn)):
    """List all rows from `runtime_pgsql_query_rules_fast_routing`."""
    return await execute_query(conn, "SELECT * FROM runtime_pgsql_query_rules_fast_routing")


@router.get("/mysql_firewall_whitelist_sqli_fingerprints", response_model=list[MysqlFirewallWhitelistSqliFingerprints], tags=["mysql"])
async def list_mysql_firewall_whitelist_sqli_fingerprints(conn=Depends(get_admin_conn)):
    """List all rows from `mysql_firewall_whitelist_sqli_fingerprints`."""
    return await execute_query(conn, "SELECT * FROM mysql_firewall_whitelist_sqli_fingerprints")


@router.post("/mysql_firewall_whitelist_sqli_fingerprints", response_model=dict[str, str], tags=["mysql"])
async def create_mysql_firewall_whitelist_sqli_fingerprints(item: MysqlFirewallWhitelistSqliFingerprintsCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `mysql_firewall_whitelist_sqli_fingerprints`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO mysql_firewall_whitelist_sqli_fingerprints ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/mysql_firewall_whitelist_sqli_fingerprints/{fingerprint}", response_model=MysqlFirewallWhitelistSqliFingerprints, tags=["mysql"])
async def get_mysql_firewall_whitelist_sqli_fingerprints(fingerprint: str, conn=Depends(get_admin_conn)):
    """Get a single row from `mysql_firewall_whitelist_sqli_fingerprints` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM mysql_firewall_whitelist_sqli_fingerprints WHERE fingerprint = %s", [fingerprint])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/mysql_firewall_whitelist_sqli_fingerprints/{fingerprint}", response_model=dict[str, str], tags=["mysql"])
async def delete_mysql_firewall_whitelist_sqli_fingerprints(fingerprint: str, conn=Depends(get_admin_conn)):
    """Delete a row from `mysql_firewall_whitelist_sqli_fingerprints` by primary key."""
    await execute_modify(conn, "DELETE FROM mysql_firewall_whitelist_sqli_fingerprints WHERE fingerprint = %s", [fingerprint])
    return {"status": "ok"}


@router.put("/mysql_firewall_whitelist_sqli_fingerprints/{fingerprint}", response_model=dict[str, str], tags=["mysql"])
async def update_mysql_firewall_whitelist_sqli_fingerprints(fingerprint: str, item: MysqlFirewallWhitelistSqliFingerprintsCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `mysql_firewall_whitelist_sqli_fingerprints`."""
    data = item.model_dump(exclude_none=True)
    data["fingerprint"] = fingerprint
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO mysql_firewall_whitelist_sqli_fingerprints ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/pgsql_firewall_whitelist_sqli_fingerprints", response_model=list[PgsqlFirewallWhitelistSqliFingerprints], tags=["pgsql"])
async def list_pgsql_firewall_whitelist_sqli_fingerprints(conn=Depends(get_admin_conn)):
    """List all rows from `pgsql_firewall_whitelist_sqli_fingerprints`."""
    return await execute_query(conn, "SELECT * FROM pgsql_firewall_whitelist_sqli_fingerprints")


@router.post("/pgsql_firewall_whitelist_sqli_fingerprints", response_model=dict[str, str], tags=["pgsql"])
async def create_pgsql_firewall_whitelist_sqli_fingerprints(item: PgsqlFirewallWhitelistSqliFingerprintsCreate, conn=Depends(get_admin_conn)):
    """Insert a row into `pgsql_firewall_whitelist_sqli_fingerprints`."""
    data = item.model_dump(exclude_none=True)
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO pgsql_firewall_whitelist_sqli_fingerprints ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/pgsql_firewall_whitelist_sqli_fingerprints/{fingerprint}", response_model=PgsqlFirewallWhitelistSqliFingerprints, tags=["pgsql"])
async def get_pgsql_firewall_whitelist_sqli_fingerprints(fingerprint: str, conn=Depends(get_admin_conn)):
    """Get a single row from `pgsql_firewall_whitelist_sqli_fingerprints` by primary key."""
    rows = await execute_query(conn, "SELECT * FROM pgsql_firewall_whitelist_sqli_fingerprints WHERE fingerprint = %s", [fingerprint])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    return rows[0]


@router.delete("/pgsql_firewall_whitelist_sqli_fingerprints/{fingerprint}", response_model=dict[str, str], tags=["pgsql"])
async def delete_pgsql_firewall_whitelist_sqli_fingerprints(fingerprint: str, conn=Depends(get_admin_conn)):
    """Delete a row from `pgsql_firewall_whitelist_sqli_fingerprints` by primary key."""
    await execute_modify(conn, "DELETE FROM pgsql_firewall_whitelist_sqli_fingerprints WHERE fingerprint = %s", [fingerprint])
    return {"status": "ok"}


@router.put("/pgsql_firewall_whitelist_sqli_fingerprints/{fingerprint}", response_model=dict[str, str], tags=["pgsql"])
async def update_pgsql_firewall_whitelist_sqli_fingerprints(fingerprint: str, item: PgsqlFirewallWhitelistSqliFingerprintsCreate, conn=Depends(get_admin_conn)):
    """Update (REPLACE) a row in `pgsql_firewall_whitelist_sqli_fingerprints`."""
    data = item.model_dump(exclude_none=True)
    data["fingerprint"] = fingerprint
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f"REPLACE INTO pgsql_firewall_whitelist_sqli_fingerprints ({cols}) VALUES ({placeholders})"
    await execute_modify(conn, sql, list(data.values()))
    return {"status": "ok"}


@router.get("/runtime_mysql_group_replication_hostgroups", response_model=list[RuntimeMysqlGroupReplicationHostgroups], tags=["runtime"])
async def list_runtime_mysql_group_replication_hostgroups(conn=Depends(get_admin_conn)):
    """List all rows from `runtime_mysql_group_replication_hostgroups`."""
    return await execute_query(conn, "SELECT * FROM runtime_mysql_group_replication_hostgroups")


@router.get("/runtime_mysql_firewall_whitelist_sqli_fingerprints", response_model=list[RuntimeMysqlFirewallWhitelistSqliFingerprints], tags=["runtime"])
async def list_runtime_mysql_firewall_whitelist_sqli_fingerprints(conn=Depends(get_admin_conn)):
    """List all rows from `runtime_mysql_firewall_whitelist_sqli_fingerprints`."""
    return await execute_query(conn, "SELECT * FROM runtime_mysql_firewall_whitelist_sqli_fingerprints")


@router.get("/runtime_pgsql_firewall_whitelist_sqli_fingerprints", response_model=list[RuntimePgsqlFirewallWhitelistSqliFingerprints], tags=["runtime"])
async def list_runtime_pgsql_firewall_whitelist_sqli_fingerprints(conn=Depends(get_admin_conn)):
    """List all rows from `runtime_pgsql_firewall_whitelist_sqli_fingerprints`."""
    return await execute_query(conn, "SELECT * FROM runtime_pgsql_firewall_whitelist_sqli_fingerprints")
