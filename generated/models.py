"""
Auto-generated Pydantic models from ProxySQL_Admin_Tables_Definitions.h

DO NOT EDIT — regenerate with: python3 tools/gen_fastapi_models.py
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

import warnings
warnings.filterwarnings(
    'ignore',
    message='Field name.*shadows an attribute in parent',
    category=UserWarning,
)


class McpTargetProfiles_protocol_enum(str, Enum):
    mysql = "mysql"
    pgsql = "pgsql"


class RuntimeMcpTargetProfiles_protocol_enum(str, Enum):
    mysql = "mysql"
    pgsql = "pgsql"


class MysqlFirewallWhitelistUsers_mode_enum(str, Enum):
    OFF = "OFF"
    DETECTING = "DETECTING"
    PROTECTING = "PROTECTING"


class PgsqlFirewallWhitelistUsers_mode_enum(str, Enum):
    OFF = "OFF"
    DETECTING = "DETECTING"
    PROTECTING = "PROTECTING"


class RuntimeMysqlFirewallWhitelistUsers_mode_enum(str, Enum):
    OFF = "OFF"
    DETECTING = "DETECTING"
    PROTECTING = "PROTECTING"


class RuntimePgsqlFirewallWhitelistUsers_mode_enum(str, Enum):
    OFF = "OFF"
    DETECTING = "DETECTING"
    PROTECTING = "PROTECTING"



class StatsTsdb(BaseModel):
    """Read model for table `stats_tsdb`."""

    Variable_Name: str
    Variable_Value: str


class StatsProxysqlGlobal(BaseModel):
    """Read model for table `stats_proxysql_global`."""

    Variable_Name: str
    Variable_Value: str


class Scheduler(BaseModel):
    """Read model for table `scheduler`."""

    id: int
    active: int = Field(default=1, description="CHECK: active IN (0,1)")
    interval_ms: int = Field(description="CHECK: interval_ms>=100 AND interval_ms<=100000000")
    filename: str
    arg1: Optional[str] = Field(default=None)
    arg2: Optional[str] = Field(default=None)
    arg3: Optional[str] = Field(default=None)
    arg4: Optional[str] = Field(default=None)
    arg5: Optional[str] = Field(default=None)
    comment: str = Field(default='')


class SchedulerCreate(BaseModel):
    """Create/update model for `scheduler`."""

    active: Optional[int] = Field(default=1, description="CHECK: active IN (0,1)")
    interval_ms: int = Field(description="CHECK: interval_ms>=100 AND interval_ms<=100000000")
    filename: str
    arg1: Optional[str] = Field(default=None)
    arg2: Optional[str] = Field(default=None)
    arg3: Optional[str] = Field(default=None)
    arg4: Optional[str] = Field(default=None)
    arg5: Optional[str] = Field(default=None)
    comment: Optional[str] = Field(default='')


class McpConfig(BaseModel):
    """Read model for table `mcp_config`."""

    variable_name: str
    variable_value: str


class McpConfigCreate(BaseModel):
    """Create/update model for `mcp_config`."""

    variable_name: str
    variable_value: str


class MysqlUsers(BaseModel):
    """Read model for table `mysql_users`."""

    username: str
    password: Optional[str] = Field(default=None)
    active: int = Field(default=1, description="CHECK: active IN (0,1)")
    use_ssl: int = Field(default=0, description="CHECK: use_ssl IN (0,1)")
    default_hostgroup: int = Field(default=0)
    default_schema: Optional[str] = Field(default=None)
    schema_locked: int = Field(default=0, description="CHECK: schema_locked IN (0,1)")
    transaction_persistent: int = Field(default=1, description="CHECK: transaction_persistent IN (0,1)")
    fast_forward: int = Field(default=0, description="CHECK: fast_forward IN (0,1)")
    backend: int = Field(default=1, description="CHECK: backend IN (0,1)")
    frontend: int = Field(default=1, description="CHECK: frontend IN (0,1)")
    max_connections: int = Field(default=10000, description="CHECK: max_connections >=0")
    attributes: str = Field(default='', description="CHECK: JSON_VALID(attributes) OR attributes = ''")
    comment: str = Field(default='')
    UNIQUE: Optional[str] = Field(default=None)


class MysqlUsersCreate(BaseModel):
    """Create/update model for `mysql_users`."""

    username: str
    password: Optional[str] = Field(default=None)
    active: Optional[int] = Field(default=1, description="CHECK: active IN (0,1)")
    use_ssl: Optional[int] = Field(default=0, description="CHECK: use_ssl IN (0,1)")
    default_hostgroup: Optional[int] = Field(default=0)
    default_schema: Optional[str] = Field(default=None)
    schema_locked: Optional[int] = Field(default=0, description="CHECK: schema_locked IN (0,1)")
    transaction_persistent: Optional[int] = Field(default=1, description="CHECK: transaction_persistent IN (0,1)")
    fast_forward: Optional[int] = Field(default=0, description="CHECK: fast_forward IN (0,1)")
    backend: Optional[int] = Field(default=1, description="CHECK: backend IN (0,1)")
    frontend: Optional[int] = Field(default=1, description="CHECK: frontend IN (0,1)")
    max_connections: Optional[int] = Field(default=10000, description="CHECK: max_connections >=0")
    attributes: Optional[str] = Field(default='', description="CHECK: JSON_VALID(attributes) OR attributes = ''")
    comment: Optional[str] = Field(default='')
    UNIQUE: Optional[str] = Field(default=None)


class PgsqlUsers(BaseModel):
    """Read model for table `pgsql_users`."""

    username: str
    password: Optional[str] = Field(default=None)
    active: int = Field(default=1, description="CHECK: active IN (0,1)")
    use_ssl: int = Field(default=0, description="CHECK: use_ssl IN (0,1)")
    default_hostgroup: int = Field(default=0)
    transaction_persistent: int = Field(default=1, description="CHECK: transaction_persistent IN (0,1)")
    fast_forward: int = Field(default=0, description="CHECK: fast_forward IN (0,1)")
    backend: int = Field(default=1, description="CHECK: backend IN (0,1)")
    frontend: int = Field(default=1, description="CHECK: frontend IN (0,1)")
    max_connections: int = Field(default=10000, description="CHECK: max_connections >=0")
    attributes: str = Field(default='', description="CHECK: JSON_VALID(attributes) OR attributes = ''")
    comment: str = Field(default='')
    UNIQUE: Optional[str] = Field(default=None)


class PgsqlUsersCreate(BaseModel):
    """Create/update model for `pgsql_users`."""

    username: str
    password: Optional[str] = Field(default=None)
    active: Optional[int] = Field(default=1, description="CHECK: active IN (0,1)")
    use_ssl: Optional[int] = Field(default=0, description="CHECK: use_ssl IN (0,1)")
    default_hostgroup: Optional[int] = Field(default=0)
    transaction_persistent: Optional[int] = Field(default=1, description="CHECK: transaction_persistent IN (0,1)")
    fast_forward: Optional[int] = Field(default=0, description="CHECK: fast_forward IN (0,1)")
    backend: Optional[int] = Field(default=1, description="CHECK: backend IN (0,1)")
    frontend: Optional[int] = Field(default=1, description="CHECK: frontend IN (0,1)")
    max_connections: Optional[int] = Field(default=10000, description="CHECK: max_connections >=0")
    attributes: Optional[str] = Field(default='', description="CHECK: JSON_VALID(attributes) OR attributes = ''")
    comment: Optional[str] = Field(default='')
    UNIQUE: Optional[str] = Field(default=None)


class StatsMysqlUsers(BaseModel):
    """Read model for table `stats_mysql_users`."""

    username: Optional[str] = Field(default=None)
    frontend_connections: int
    frontend_max_connections: int


class StatsPgsqlUsers(BaseModel):
    """Read model for table `stats_pgsql_users`."""

    username: Optional[str] = Field(default=None)
    frontend_connections: int
    frontend_max_connections: int


class DebugLevels(BaseModel):
    """Read model for table `debug_levels`."""

    module: str
    verbosity: int = Field(default=0)


class DebugLevelsCreate(BaseModel):
    """Create/update model for `debug_levels`."""

    module: str
    verbosity: Optional[int] = Field(default=0)


class GenaiConfig(BaseModel):
    """Read model for table `genai_config`."""

    variable_name: str
    variable_value: str


class GenaiConfigCreate(BaseModel):
    """Create/update model for `genai_config`."""

    variable_name: str
    variable_value: str


class StatsMysqlErrors(BaseModel):
    """Read model for table `stats_mysql_errors`."""

    hostgroup: int
    hostname: str
    port: int
    username: str
    client_address: str
    schemaname: str
    errno: int
    count_star: int
    first_seen: int
    last_seen: int
    last_error: str = Field(default='')


class StatsMysqlGlobal(BaseModel):
    """Read model for table `stats_mysql_global`."""

    Variable_Name: str
    Variable_Value: str


class StatsPgsqlErrors(BaseModel):
    """Read model for table `stats_pgsql_errors`."""

    hostgroup: int
    hostname: str
    port: int
    username: str
    client_address: str
    database: str
    sqlstate: str
    count_star: int
    first_seen: int
    last_seen: int
    last_error: str = Field(default='')


class StatsPgsqlGlobal(BaseModel):
    """Read model for table `stats_pgsql_global`."""

    Variable_Name: str
    Variable_Value: str


class RuntimeMysqlUsers(BaseModel):
    """Read model for table `runtime_mysql_users`."""

    username: str
    password: Optional[str] = Field(default=None)
    active: int = Field(default=1, description="CHECK: active IN (0,1)")
    use_ssl: int = Field(default=0, description="CHECK: use_ssl IN (0,1)")
    default_hostgroup: int = Field(default=0)
    default_schema: Optional[str] = Field(default=None)
    schema_locked: int = Field(default=0, description="CHECK: schema_locked IN (0,1)")
    transaction_persistent: int = Field(default=1, description="CHECK: transaction_persistent IN (0,1)")
    fast_forward: int = Field(default=0, description="CHECK: fast_forward IN (0,1)")
    backend: int = Field(default=1, description="CHECK: backend IN (0,1)")
    frontend: int = Field(default=1, description="CHECK: frontend IN (0,1)")
    max_connections: int = Field(default=10000, description="CHECK: max_connections >=0")
    attributes: str = Field(default='', description="CHECK: JSON_VALID(attributes) OR attributes = ''")
    comment: str = Field(default='')
    UNIQUE: Optional[str] = Field(default=None)


class DebugFilters(BaseModel):
    """Read model for table `debug_filters`."""

    filename: str
    line: int
    funct: str


class DebugFiltersCreate(BaseModel):
    """Create/update model for `debug_filters`."""

    filename: str
    line: int
    funct: str


class MysqlServers(BaseModel):
    """Read model for table `mysql_servers`."""

    hostgroup_id: int = Field(default=0, description="CHECK: hostgroup_id>=0")
    hostname: str
    port: int = Field(default=3306, description="CHECK: port >= 0 AND port <= 65535")
    gtid_port: int = Field(default=0, description="CHECK: (gtid_port <> port OR gtid_port=0) AND gtid_port >= 0 AND gtid_port <= 65535")
    status: str = Field(default='ONLINE', description="CHECK: UPPER(status) IN ('ONLINE','SHUNNED','OFFLINE_SOFT', 'OFFLINE_HARD')")
    weight: int = Field(default=1, description="CHECK: weight >= 0 AND weight <=10000000")
    compression: int = Field(default=0, description="CHECK: compression IN(0,1)")
    max_connections: int = Field(default=1000, description="CHECK: max_connections >=0")
    max_replication_lag: int = Field(default=0, description="CHECK: max_replication_lag >= 0 AND max_replication_lag <= 126144000")
    use_ssl: int = Field(default=0, description="CHECK: use_ssl IN(0,1)")
    max_latency_ms: int = Field(default=0, description="CHECK: max_latency_ms>=0")
    comment: str = Field(default='')


class MysqlServersCreate(BaseModel):
    """Create/update model for `mysql_servers`."""

    hostgroup_id: Optional[int] = Field(default=0, description="CHECK: hostgroup_id>=0")
    hostname: str
    port: Optional[int] = Field(default=3306, description="CHECK: port >= 0 AND port <= 65535")
    gtid_port: Optional[int] = Field(default=0, description="CHECK: (gtid_port <> port OR gtid_port=0) AND gtid_port >= 0 AND gtid_port <= 65535")
    status: Optional[str] = Field(default='ONLINE', description="CHECK: UPPER(status) IN ('ONLINE','SHUNNED','OFFLINE_SOFT', 'OFFLINE_HARD')")
    weight: Optional[int] = Field(default=1, description="CHECK: weight >= 0 AND weight <=10000000")
    compression: Optional[int] = Field(default=0, description="CHECK: compression IN(0,1)")
    max_connections: Optional[int] = Field(default=1000, description="CHECK: max_connections >=0")
    max_replication_lag: Optional[int] = Field(default=0, description="CHECK: max_replication_lag >= 0 AND max_replication_lag <= 126144000")
    use_ssl: Optional[int] = Field(default=0, description="CHECK: use_ssl IN(0,1)")
    max_latency_ms: Optional[int] = Field(default=0, description="CHECK: max_latency_ms>=0")
    comment: Optional[str] = Field(default='')


class PgsqlServers(BaseModel):
    """Read model for table `pgsql_servers`."""

    hostgroup_id: int = Field(default=0, description="CHECK: hostgroup_id>=0")
    hostname: str
    port: int = Field(default=5432, description="CHECK: port >= 0 AND port <= 65535")
    status: str = Field(default='ONLINE', description="CHECK: UPPER(status) IN ('ONLINE','SHUNNED','OFFLINE_SOFT', 'OFFLINE_HARD')")
    weight: int = Field(default=1, description="CHECK: weight >= 0 AND weight <=10000000")
    compression: int = Field(default=0, description="CHECK: compression IN(0,1)")
    max_connections: int = Field(default=1000, description="CHECK: max_connections >=0")
    max_replication_lag: int = Field(default=0, description="CHECK: max_replication_lag >= 0 AND max_replication_lag <= 126144000")
    use_ssl: int = Field(default=0, description="CHECK: use_ssl IN(0,1)")
    max_latency_ms: int = Field(default=0, description="CHECK: max_latency_ms>=0")
    comment: str = Field(default='')


class PgsqlServersCreate(BaseModel):
    """Create/update model for `pgsql_servers`."""

    hostgroup_id: Optional[int] = Field(default=0, description="CHECK: hostgroup_id>=0")
    hostname: str
    port: Optional[int] = Field(default=5432, description="CHECK: port >= 0 AND port <= 65535")
    status: Optional[str] = Field(default='ONLINE', description="CHECK: UPPER(status) IN ('ONLINE','SHUNNED','OFFLINE_SOFT', 'OFFLINE_HARD')")
    weight: Optional[int] = Field(default=1, description="CHECK: weight >= 0 AND weight <=10000000")
    compression: Optional[int] = Field(default=0, description="CHECK: compression IN(0,1)")
    max_connections: Optional[int] = Field(default=1000, description="CHECK: max_connections >=0")
    max_replication_lag: Optional[int] = Field(default=0, description="CHECK: max_replication_lag >= 0 AND max_replication_lag <= 126144000")
    use_ssl: Optional[int] = Field(default=0, description="CHECK: use_ssl IN(0,1)")
    max_latency_ms: Optional[int] = Field(default=0, description="CHECK: max_latency_ms>=0")
    comment: Optional[str] = Field(default='')


class RestapiRoutes(BaseModel):
    """Read model for table `restapi_routes`."""

    id: int
    active: int = Field(default=1, description="CHECK: active IN (0,1)")
    timeout_ms: int = Field(description="CHECK: timeout_ms>=100 AND timeout_ms<=100000000")
    method: str = Field(description="CHECK: UPPER(method) IN ('GET','POST')")
    uri: str
    script: str
    comment: str = Field(default='')


class RestapiRoutesCreate(BaseModel):
    """Create/update model for `restapi_routes`."""

    active: Optional[int] = Field(default=1, description="CHECK: active IN (0,1)")
    timeout_ms: int = Field(description="CHECK: timeout_ms>=100 AND timeout_ms<=100000000")
    method: str = Field(description="CHECK: UPPER(method) IN ('GET','POST')")
    uri: str
    script: str
    comment: Optional[str] = Field(default='')


class StatsMemoryMetrics(BaseModel):
    """Read model for table `stats_memory_metrics`."""

    Variable_Name: str
    Variable_Value: str


class GlobalSettings(BaseModel):
    """Read model for table `global_settings`."""

    variable_name: str
    variable_value: str


class GlobalSettingsCreate(BaseModel):
    """Create/update model for `global_settings`."""

    variable_name: str
    variable_value: str


class McpQueryRules(BaseModel):
    """Read model for table `mcp_query_rules`."""

    rule_id: int
    active: int = Field(default=0, description="CHECK: active IN (0,1)")
    username: Optional[str] = Field(default=None)
    target_id: Optional[str] = Field(default=None)
    schemaname: Optional[str] = Field(default=None)
    tool_name: Optional[str] = Field(default=None)
    match_pattern: Optional[str] = Field(default=None)
    negate_match_pattern: int = Field(default=0, description="CHECK: negate_match_pattern IN (0,1)")
    re_modifiers: Optional[str] = Field(default='CASELESS')
    flagIN: int = Field(default=0)
    flagOUT: Optional[int] = Field(default=None, description="CHECK: flagOUT >= 0")
    replace_pattern: Optional[str] = Field(default=None)
    timeout_ms: Optional[int] = Field(default=None, description="CHECK: timeout_ms >= 0")
    error_msg: Optional[str] = Field(default=None)
    OK_msg: Optional[str] = Field(default=None)
    log: Optional[int] = Field(default=None, description="CHECK: log IN (0,1)")
    apply: int = Field(default=1, description="CHECK: apply IN (0,1)")
    comment: Optional[str] = Field(default=None)


class McpQueryRulesCreate(BaseModel):
    """Create/update model for `mcp_query_rules`."""

    active: Optional[int] = Field(default=0, description="CHECK: active IN (0,1)")
    username: Optional[str] = Field(default=None)
    target_id: Optional[str] = Field(default=None)
    schemaname: Optional[str] = Field(default=None)
    tool_name: Optional[str] = Field(default=None)
    match_pattern: Optional[str] = Field(default=None)
    negate_match_pattern: Optional[int] = Field(default=0, description="CHECK: negate_match_pattern IN (0,1)")
    re_modifiers: Optional[str] = Field(default='CASELESS')
    flagIN: Optional[int] = Field(default=0)
    flagOUT: Optional[int] = Field(default=None, description="CHECK: flagOUT >= 0")
    replace_pattern: Optional[str] = Field(default=None)
    timeout_ms: Optional[int] = Field(default=None, description="CHECK: timeout_ms >= 0")
    error_msg: Optional[str] = Field(default=None)
    OK_msg: Optional[str] = Field(default=None)
    log: Optional[int] = Field(default=None, description="CHECK: log IN (0,1)")
    apply: Optional[int] = Field(default=1, description="CHECK: apply IN (0,1)")
    comment: Optional[str] = Field(default=None)


class StatsMcpQueryRules(BaseModel):
    """Read model for table `stats_mcp_query_rules`."""

    rule_id: int
    username: Optional[str] = Field(default=None)
    target_id: Optional[str] = Field(default=None)
    hits: int


class ClickhouseUsers(BaseModel):
    """Read model for table `clickhouse_users`."""

    username: str
    password: Optional[str] = Field(default=None)
    active: int = Field(default=1, description="CHECK: active IN (0,1)")
    max_connections: int = Field(default=10000, description="CHECK: max_connections >=0")
    PRIMARY: Optional[str] = Field(default=None)


class ClickhouseUsersCreate(BaseModel):
    """Create/update model for `clickhouse_users`."""

    username: str
    password: Optional[str] = Field(default=None)
    active: Optional[int] = Field(default=1, description="CHECK: active IN (0,1)")
    max_connections: Optional[int] = Field(default=10000, description="CHECK: max_connections >=0")
    PRIMARY: Optional[str] = Field(default=None)


class CoredumpFilters(BaseModel):
    """Read model for table `coredump_filters`."""

    filename: str
    line: int


class CoredumpFiltersCreate(BaseModel):
    """Create/update model for `coredump_filters`."""

    filename: str
    line: int


class GlobalVariables(BaseModel):
    """Read model for table `global_variables`."""

    variable_name: str
    variable_value: str


class GlobalVariablesCreate(BaseModel):
    """Create/update model for `global_variables`."""

    variable_name: str
    variable_value: str


class MysqlCollations(BaseModel):
    """Read model for table `mysql_collations`."""

    Id: int
    Collation: str
    Charset: str
    Default: str


class MysqlCollationsCreate(BaseModel):
    """Create/update model for `mysql_collations`."""

    Id: int
    Collation: str
    Charset: str
    Default: str


class ProxysqlServers(BaseModel):
    """Read model for table `proxysql_servers`."""

    hostname: str
    port: int = Field(default=6032)
    weight: int = Field(default=0, description="CHECK: weight >= 0")
    comment: str = Field(default='')


class ProxysqlServersCreate(BaseModel):
    """Create/update model for `proxysql_servers`."""

    hostname: str
    port: Optional[int] = Field(default=6032)
    weight: Optional[int] = Field(default=0, description="CHECK: weight >= 0")
    comment: Optional[str] = Field(default='')


class StatsMcpQueryDigest(BaseModel):
    """Read model for table `stats_mcp_query_digest`."""

    tool_name: str
    run_id: Optional[int] = Field(default=None)
    digest: str
    digest_text: str
    count_star: int
    first_seen: int
    last_seen: int
    sum_time: int
    min_time: int
    max_time: int
    PRIMARY: Optional[str] = Field(default=None)


class StatsTlsCertificates(BaseModel):
    """Read model for table `stats_tls_certificates`."""

    cert_type: str
    file_path: str
    subject_cn: Optional[str] = Field(default=None)
    issuer_cn: Optional[str] = Field(default=None)
    serial_number: Optional[str] = Field(default=None)
    not_before: Optional[str] = Field(default=None)
    not_after: Optional[str] = Field(default=None)
    days_until_expiry: Optional[int] = Field(default=None)
    sha256_fingerprint: Optional[str] = Field(default=None)
    loaded_at: int = Field(default=0)


class McpAuthProfiles(BaseModel):
    """Read model for table `mcp_auth_profiles`."""

    auth_profile_id: str
    db_username: str
    db_password: str
    default_schema: Optional[str] = Field(default='')
    use_ssl: int = Field(default=0, description="CHECK: use_ssl IN (0,1)")
    ssl_mode: Optional[str] = Field(default='')
    comment: Optional[str] = Field(default='')


class McpAuthProfilesCreate(BaseModel):
    """Create/update model for `mcp_auth_profiles`."""

    auth_profile_id: str
    db_username: str
    db_password: str
    default_schema: Optional[str] = Field(default='')
    use_ssl: Optional[int] = Field(default=0, description="CHECK: use_ssl IN (0,1)")
    ssl_mode: Optional[str] = Field(default='')
    comment: Optional[str] = Field(default='')


class MysqlQueryRules(BaseModel):
    """Read model for table `mysql_query_rules`."""

    rule_id: int
    active: int = Field(default=0, description="CHECK: active IN (0,1)")
    username: Optional[str] = Field(default=None)
    schemaname: Optional[str] = Field(default=None)
    flagIN: int = Field(default=0, description="CHECK: flagIN >= 0")
    client_addr: Optional[str] = Field(default=None)
    proxy_addr: Optional[str] = Field(default=None)
    proxy_port: Optional[int] = Field(default=None, description="CHECK: proxy_port >= 0 AND proxy_port <= 65535")
    digest: Optional[str] = Field(default=None)
    match_digest: Optional[str] = Field(default=None)
    match_pattern: Optional[str] = Field(default=None)
    negate_match_pattern: int = Field(default=0, description="CHECK: negate_match_pattern IN (0,1)")
    re_modifiers: Optional[str] = Field(default='CASELESS')
    flagOUT: Optional[int] = Field(default=None, description="CHECK: flagOUT >= 0")
    replace_pattern: Optional[str] = Field(default=None, description="CHECK: CASE WHEN replace_pattern IS NULL THEN 1 WHEN replace_pattern IS NOT NULL AND match_pattern IS NOT NULL THEN 1 ELSE 0 END")
    destination_hostgroup: Optional[int] = Field(default='NULL')
    cache_ttl: Optional[int] = Field(default=None, description="CHECK: cache_ttl > 0")
    cache_empty_result: Optional[int] = Field(default='NULL', description="CHECK: cache_empty_result IN (0,1)")
    cache_timeout: Optional[int] = Field(default=None, description="CHECK: cache_timeout >= 0")
    reconnect: Optional[int] = Field(default='NULL', description="CHECK: reconnect IN (0,1)")
    timeout: Optional[int] = Field(default=None, description="CHECK: timeout >= 0")
    retries: Optional[int] = Field(default=None, description="CHECK: retries>=0 AND retries <=1000")
    delay: Optional[int] = Field(default=None, description="CHECK: delay >=0")
    next_query_flagIN: Optional[int] = Field(default=None)
    mirror_flagOUT: Optional[int] = Field(default=None)
    mirror_hostgroup: Optional[int] = Field(default=None)
    error_msg: Optional[str] = Field(default=None)
    OK_msg: Optional[str] = Field(default=None)
    sticky_conn: Optional[int] = Field(default=None, description="CHECK: sticky_conn IN (0,1)")
    multiplex: Optional[int] = Field(default=None, description="CHECK: multiplex IN (0,1,2)")
    gtid_from_hostgroup: Optional[int] = Field(default=None)
    log: Optional[int] = Field(default=None, description="CHECK: log IN (0,1)")
    apply: int = Field(default=0, description="CHECK: apply IN (0,1)")
    attributes: str = Field(default='', description="CHECK: JSON_VALID(attributes) OR attributes = ''")
    comment: Optional[str] = Field(default=None)


class MysqlQueryRulesCreate(BaseModel):
    """Create/update model for `mysql_query_rules`."""

    active: Optional[int] = Field(default=0, description="CHECK: active IN (0,1)")
    username: Optional[str] = Field(default=None)
    schemaname: Optional[str] = Field(default=None)
    flagIN: Optional[int] = Field(default=0, description="CHECK: flagIN >= 0")
    client_addr: Optional[str] = Field(default=None)
    proxy_addr: Optional[str] = Field(default=None)
    proxy_port: Optional[int] = Field(default=None, description="CHECK: proxy_port >= 0 AND proxy_port <= 65535")
    digest: Optional[str] = Field(default=None)
    match_digest: Optional[str] = Field(default=None)
    match_pattern: Optional[str] = Field(default=None)
    negate_match_pattern: Optional[int] = Field(default=0, description="CHECK: negate_match_pattern IN (0,1)")
    re_modifiers: Optional[str] = Field(default='CASELESS')
    flagOUT: Optional[int] = Field(default=None, description="CHECK: flagOUT >= 0")
    replace_pattern: Optional[str] = Field(default=None, description="CHECK: CASE WHEN replace_pattern IS NULL THEN 1 WHEN replace_pattern IS NOT NULL AND match_pattern IS NOT NULL THEN 1 ELSE 0 END")
    destination_hostgroup: Optional[int] = Field(default='NULL')
    cache_ttl: Optional[int] = Field(default=None, description="CHECK: cache_ttl > 0")
    cache_empty_result: Optional[int] = Field(default='NULL', description="CHECK: cache_empty_result IN (0,1)")
    cache_timeout: Optional[int] = Field(default=None, description="CHECK: cache_timeout >= 0")
    reconnect: Optional[int] = Field(default='NULL', description="CHECK: reconnect IN (0,1)")
    timeout: Optional[int] = Field(default=None, description="CHECK: timeout >= 0")
    retries: Optional[int] = Field(default=None, description="CHECK: retries>=0 AND retries <=1000")
    delay: Optional[int] = Field(default=None, description="CHECK: delay >=0")
    next_query_flagIN: Optional[int] = Field(default=None)
    mirror_flagOUT: Optional[int] = Field(default=None)
    mirror_hostgroup: Optional[int] = Field(default=None)
    error_msg: Optional[str] = Field(default=None)
    OK_msg: Optional[str] = Field(default=None)
    sticky_conn: Optional[int] = Field(default=None, description="CHECK: sticky_conn IN (0,1)")
    multiplex: Optional[int] = Field(default=None, description="CHECK: multiplex IN (0,1,2)")
    gtid_from_hostgroup: Optional[int] = Field(default=None)
    log: Optional[int] = Field(default=None, description="CHECK: log IN (0,1)")
    apply: Optional[int] = Field(default=0, description="CHECK: apply IN (0,1)")
    attributes: Optional[str] = Field(default='', description="CHECK: JSON_VALID(attributes) OR attributes = ''")
    comment: Optional[str] = Field(default=None)


class PgsqlQueryRules(BaseModel):
    """Read model for table `pgsql_query_rules`."""

    rule_id: int
    active: int = Field(default=0, description="CHECK: active IN (0,1)")
    username: Optional[str] = Field(default=None)
    database: Optional[str] = Field(default=None)
    flagIN: int = Field(default=0, description="CHECK: flagIN >= 0")
    client_addr: Optional[str] = Field(default=None)
    proxy_addr: Optional[str] = Field(default=None)
    proxy_port: Optional[int] = Field(default=None, description="CHECK: proxy_port >= 0 AND proxy_port <= 65535")
    digest: Optional[str] = Field(default=None)
    match_digest: Optional[str] = Field(default=None)
    match_pattern: Optional[str] = Field(default=None)
    negate_match_pattern: int = Field(default=0, description="CHECK: negate_match_pattern IN (0,1)")
    re_modifiers: Optional[str] = Field(default='CASELESS')
    flagOUT: Optional[int] = Field(default=None, description="CHECK: flagOUT >= 0")
    replace_pattern: Optional[str] = Field(default=None, description="CHECK: CASE WHEN replace_pattern IS NULL THEN 1 WHEN replace_pattern IS NOT NULL AND match_pattern IS NOT NULL THEN 1 ELSE 0 END")
    destination_hostgroup: Optional[int] = Field(default='NULL')
    cache_ttl: Optional[int] = Field(default=None, description="CHECK: cache_ttl > 0")
    cache_empty_result: Optional[int] = Field(default='NULL', description="CHECK: cache_empty_result IN (0,1)")
    cache_timeout: Optional[int] = Field(default=None, description="CHECK: cache_timeout >= 0")
    reconnect: Optional[int] = Field(default='NULL', description="CHECK: reconnect IN (0,1)")
    timeout: Optional[int] = Field(default=None, description="CHECK: timeout >= 0")
    retries: Optional[int] = Field(default=None, description="CHECK: retries>=0 AND retries <=1000")
    delay: Optional[int] = Field(default=None, description="CHECK: delay >=0")
    next_query_flagIN: Optional[int] = Field(default=None)
    mirror_flagOUT: Optional[int] = Field(default=None)
    mirror_hostgroup: Optional[int] = Field(default=None)
    error_msg: Optional[str] = Field(default=None)
    OK_msg: Optional[str] = Field(default=None)
    sticky_conn: Optional[int] = Field(default=None, description="CHECK: sticky_conn IN (0,1)")
    multiplex: Optional[int] = Field(default=None, description="CHECK: multiplex IN (0,1,2)")
    log: Optional[int] = Field(default=None, description="CHECK: log IN (0,1)")
    apply: int = Field(default=0, description="CHECK: apply IN (0,1)")
    attributes: str = Field(default='', description="CHECK: JSON_VALID(attributes) OR attributes = ''")
    comment: Optional[str] = Field(default=None)


class PgsqlQueryRulesCreate(BaseModel):
    """Create/update model for `pgsql_query_rules`."""

    active: Optional[int] = Field(default=0, description="CHECK: active IN (0,1)")
    username: Optional[str] = Field(default=None)
    database: Optional[str] = Field(default=None)
    flagIN: Optional[int] = Field(default=0, description="CHECK: flagIN >= 0")
    client_addr: Optional[str] = Field(default=None)
    proxy_addr: Optional[str] = Field(default=None)
    proxy_port: Optional[int] = Field(default=None, description="CHECK: proxy_port >= 0 AND proxy_port <= 65535")
    digest: Optional[str] = Field(default=None)
    match_digest: Optional[str] = Field(default=None)
    match_pattern: Optional[str] = Field(default=None)
    negate_match_pattern: Optional[int] = Field(default=0, description="CHECK: negate_match_pattern IN (0,1)")
    re_modifiers: Optional[str] = Field(default='CASELESS')
    flagOUT: Optional[int] = Field(default=None, description="CHECK: flagOUT >= 0")
    replace_pattern: Optional[str] = Field(default=None, description="CHECK: CASE WHEN replace_pattern IS NULL THEN 1 WHEN replace_pattern IS NOT NULL AND match_pattern IS NOT NULL THEN 1 ELSE 0 END")
    destination_hostgroup: Optional[int] = Field(default='NULL')
    cache_ttl: Optional[int] = Field(default=None, description="CHECK: cache_ttl > 0")
    cache_empty_result: Optional[int] = Field(default='NULL', description="CHECK: cache_empty_result IN (0,1)")
    cache_timeout: Optional[int] = Field(default=None, description="CHECK: cache_timeout >= 0")
    reconnect: Optional[int] = Field(default='NULL', description="CHECK: reconnect IN (0,1)")
    timeout: Optional[int] = Field(default=None, description="CHECK: timeout >= 0")
    retries: Optional[int] = Field(default=None, description="CHECK: retries>=0 AND retries <=1000")
    delay: Optional[int] = Field(default=None, description="CHECK: delay >=0")
    next_query_flagIN: Optional[int] = Field(default=None)
    mirror_flagOUT: Optional[int] = Field(default=None)
    mirror_hostgroup: Optional[int] = Field(default=None)
    error_msg: Optional[str] = Field(default=None)
    OK_msg: Optional[str] = Field(default=None)
    sticky_conn: Optional[int] = Field(default=None, description="CHECK: sticky_conn IN (0,1)")
    multiplex: Optional[int] = Field(default=None, description="CHECK: multiplex IN (0,1,2)")
    log: Optional[int] = Field(default=None, description="CHECK: log IN (0,1)")
    apply: Optional[int] = Field(default=0, description="CHECK: apply IN (0,1)")
    attributes: Optional[str] = Field(default='', description="CHECK: JSON_VALID(attributes) OR attributes = ''")
    comment: Optional[str] = Field(default=None)


class RuntimeScheduler(BaseModel):
    """Read model for table `runtime_scheduler`."""

    id: int
    active: int = Field(default=1, description="CHECK: active IN (0,1)")
    interval_ms: int = Field(description="CHECK: interval_ms>=100 AND interval_ms<=100000000")
    filename: str
    arg1: Optional[str] = Field(default=None)
    arg2: Optional[str] = Field(default=None)
    arg3: Optional[str] = Field(default=None)
    arg4: Optional[str] = Field(default=None)
    arg5: Optional[str] = Field(default=None)
    comment: str = Field(default='')


class StatsMysqlProcesslist(BaseModel):
    """Read model for table `stats_mysql_processlist`."""

    ThreadID: int
    SessionID: Optional[int] = Field(default=None)
    user: Optional[str] = Field(default=None)
    db: Optional[str] = Field(default=None)
    cli_host: Optional[str] = Field(default=None)
    cli_port: Optional[int] = Field(default=None)
    hostgroup: Optional[int] = Field(default=None)
    l_srv_host: Optional[str] = Field(default=None)
    l_srv_port: Optional[int] = Field(default=None)
    srv_host: Optional[str] = Field(default=None)
    srv_port: Optional[int] = Field(default=None)
    command: Optional[str] = Field(default=None)
    time_ms: int
    info: Optional[str] = Field(default=None)
    status_flags: Optional[int] = Field(default=None)
    extended_info: Optional[str] = Field(default=None)


class StatsMysqlQueryRules(BaseModel):
    """Read model for table `stats_mysql_query_rules`."""

    rule_id: Optional[int] = Field(default=None)
    hits: int


class StatsPgsqlProcesslist(BaseModel):
    """Read model for table `stats_pgsql_processlist`."""

    ThreadID: int
    SessionID: Optional[int] = Field(default=None)
    user: Optional[str] = Field(default=None)
    database: Optional[str] = Field(default=None)
    cli_host: Optional[str] = Field(default=None)
    cli_port: Optional[int] = Field(default=None)
    hostgroup: Optional[int] = Field(default=None)
    l_srv_host: Optional[str] = Field(default=None)
    l_srv_port: Optional[int] = Field(default=None)
    srv_host: Optional[str] = Field(default=None)
    srv_port: Optional[int] = Field(default=None)
    backend_pid: Optional[int] = Field(default=None)
    backend_state: Optional[str] = Field(default=None)
    command: Optional[str] = Field(default=None)
    time_ms: int
    info: Optional[str] = Field(default=None)
    status_flags: Optional[int] = Field(default=None)
    extended_info: Optional[str] = Field(default=None)


class StatsPgsqlQueryRules(BaseModel):
    """Read model for table `stats_pgsql_query_rules`."""

    rule_id: Optional[int] = Field(default=None)
    hits: int


class RuntimeChecksumsValues(BaseModel):
    """Read model for table `runtime_checksums_values`."""

    name: str
    version: int
    epoch: int
    checksum: str
    PRIMARY: Optional[str] = Field(default=None)


class RuntimeCoredumpFilters(BaseModel):
    """Read model for table `runtime_coredump_filters`."""

    filename: str
    line: int


class RuntimeGlobalVariables(BaseModel):
    """Read model for table `runtime_global_variables`."""

    variable_name: str
    variable_value: str


class MysqlLdapMapping(BaseModel):
    """Read model for table `mysql_ldap_mapping`."""

    priority: Optional[int] = Field(default=None, description="CHECK: priority >= 1 AND priority <= 1000000")
    frontend_entity: str
    backend_entity: str
    comment: str = Field(default='')
    UNIQUE: Optional[str] = Field(default=None)


class MysqlLdapMappingCreate(BaseModel):
    """Create/update model for `mysql_ldap_mapping`."""

    priority: Optional[int] = Field(default=None, description="CHECK: priority >= 1 AND priority <= 1000000")
    frontend_entity: str
    backend_entity: str
    comment: Optional[str] = Field(default='')
    UNIQUE: Optional[str] = Field(default=None)


class PgsqlLdapMapping(BaseModel):
    """Read model for table `pgsql_ldap_mapping`."""

    priority: Optional[int] = Field(default=None, description="CHECK: priority >= 1 AND priority <= 1000000")
    frontend_entity: str
    backend_entity: str
    comment: str = Field(default='')
    UNIQUE: Optional[str] = Field(default=None)


class PgsqlLdapMappingCreate(BaseModel):
    """Create/update model for `pgsql_ldap_mapping`."""

    priority: Optional[int] = Field(default=None, description="CHECK: priority >= 1 AND priority <= 1000000")
    frontend_entity: str
    backend_entity: str
    comment: Optional[str] = Field(default='')
    UNIQUE: Optional[str] = Field(default=None)


class RuntimeMcpConfig(BaseModel):
    """Read model for table `runtime_mcp_config`."""

    variable_name: str
    variable_value: str


class StatsMysqlErrorsReset(BaseModel):
    """Read model for table `stats_mysql_errors_reset`."""

    hostgroup: int
    hostname: str
    port: int
    username: str
    client_address: str
    schemaname: str
    errno: int
    count_star: int
    first_seen: int
    last_seen: int
    last_error: str = Field(default='')


class StatsMysqlQueryDigest(BaseModel):
    """Read model for table `stats_mysql_query_digest`."""

    hostgroup: Optional[int] = Field(default=None)
    schemaname: str
    username: str
    client_address: str
    digest: str
    digest_text: str
    count_star: int
    first_seen: int
    last_seen: int
    sum_time: int
    min_time: int
    max_time: int
    sum_rows_affected: int
    sum_rows_sent: int
    PRIMARY: Optional[str] = Field(default=None)


class StatsPgsqlErrorsReset(BaseModel):
    """Read model for table `stats_pgsql_errors_reset`."""

    hostgroup: int
    hostname: str
    port: int
    username: str
    client_address: str
    database: str
    sqlstate: str
    count_star: int
    first_seen: int
    last_seen: int
    last_error: str = Field(default='')


class StatsPgsqlQueryDigest(BaseModel):
    """Read model for table `stats_pgsql_query_digest`."""

    hostgroup: Optional[int] = Field(default=None)
    database: str
    username: str
    client_address: str
    digest: str
    digest_text: str
    count_star: int
    first_seen: int
    last_seen: int
    sum_time: int
    min_time: int
    max_time: int
    sum_rows_affected: int
    sum_rows_sent: int
    PRIMARY: Optional[str] = Field(default=None)


class StatsPgsqlQueryEvents(BaseModel):
    """Read model for table `stats_pgsql_query_events`."""

    id: Optional[int] = Field(default=None)
    thread_id: Optional[int] = Field(default=None)
    username: Optional[str] = Field(default=None)
    database: Optional[str] = Field(default=None)
    start_time: Optional[int] = Field(default=None)
    end_time: Optional[int] = Field(default=None)
    query_digest: Optional[str] = Field(default=None)
    query: Optional[str] = Field(default=None)
    server: Optional[str] = Field(default=None)
    client: Optional[str] = Field(default=None)
    event_type: Optional[int] = Field(default=None)
    hid: Optional[int] = Field(default=None)
    extra_info: Optional[str] = Field(default=None)
    affected_rows: Optional[int] = Field(default=None)
    rows_sent: Optional[int] = Field(default=None)
    client_stmt_name: Optional[str] = Field(default=None)
    sqlstate: Optional[str] = Field(default=None)
    error: Optional[str] = Field(default=None)


class McpTargetProfiles(BaseModel):
    """Read model for table `mcp_target_profiles`."""

    target_id: str
    protocol: McpTargetProfiles_protocol_enum = Field(description="CHECK: protocol IN ('mysql','pgsql')")
    hostgroup_id: int = Field(description="CHECK: hostgroup_id >= 0")
    auth_profile_id: str
    description: Optional[str] = Field(default='')
    max_rows: int = Field(default=200, description="CHECK: max_rows > 0")
    timeout_ms: int = Field(default=2000, description="CHECK: timeout_ms >= 0")
    allow_explain: int = Field(default=1, description="CHECK: allow_explain IN (0,1)")
    allow_discovery: int = Field(default=1, description="CHECK: allow_discovery IN (0,1)")
    active: int = Field(default=1, description="CHECK: active IN (0,1)")
    comment: Optional[str] = Field(default='')


class McpTargetProfilesCreate(BaseModel):
    """Create/update model for `mcp_target_profiles`."""

    target_id: str
    protocol: McpTargetProfiles_protocol_enum = Field(description="CHECK: protocol IN ('mysql','pgsql')")
    hostgroup_id: int = Field(description="CHECK: hostgroup_id >= 0")
    auth_profile_id: str
    description: Optional[str] = Field(default='')
    max_rows: Optional[int] = Field(default=200, description="CHECK: max_rows > 0")
    timeout_ms: Optional[int] = Field(default=2000, description="CHECK: timeout_ms >= 0")
    allow_explain: Optional[int] = Field(default=1, description="CHECK: allow_explain IN (0,1)")
    allow_discovery: Optional[int] = Field(default=1, description="CHECK: allow_discovery IN (0,1)")
    active: Optional[int] = Field(default=1, description="CHECK: active IN (0,1)")
    comment: Optional[str] = Field(default='')


class RuntimePgsqlUsers(BaseModel):
    """Read model for table `runtime_pgsql_users`."""

    username: str
    password: Optional[str] = Field(default=None)
    active: int = Field(default=1, description="CHECK: active IN (0,1)")
    use_ssl: int = Field(default=0, description="CHECK: use_ssl IN (0,1)")
    default_hostgroup: int = Field(default=0)
    transaction_persistent: int = Field(default=1, description="CHECK: transaction_persistent IN (0,1)")
    fast_forward: int = Field(default=0, description="CHECK: fast_forward IN (0,1)")
    backend: int = Field(default=1, description="CHECK: backend IN (0,1)")
    frontend: int = Field(default=1, description="CHECK: frontend IN (0,1)")
    max_connections: int = Field(default=10000, description="CHECK: max_connections >=0")
    attributes: str = Field(default='', description="CHECK: JSON_VALID(attributes) OR attributes = ''")
    comment: str = Field(default='')
    UNIQUE: Optional[str] = Field(default=None)


class StatsMysqlGtidExecuted(BaseModel):
    """Read model for table `stats_mysql_gtid_executed`."""

    hostname: str
    port: int = Field(default=3306)
    gtid_executed: Optional[str] = Field(default=None)
    events: int


class StatsPgsqlStatActivity(BaseModel):
    """Read model for table `stats_pgsql_stat_activity`."""

    thread_id: Optional[str] = Field(default=None)
    datname: Optional[str] = Field(default=None)
    pid: Optional[str] = Field(default=None)
    usename: Optional[str] = Field(default=None)
    client_addr: Optional[str] = Field(default=None)
    client_port: Optional[str] = Field(default=None)
    hostgroup: Optional[str] = Field(default=None)
    l_srv_host: Optional[str] = Field(default=None)
    l_srv_port: Optional[str] = Field(default=None)
    srv_host: Optional[str] = Field(default=None)
    srv_port: Optional[str] = Field(default=None)
    backend_pid: Optional[str] = Field(default=None)
    state: Optional[str] = Field(default=None)
    command: Optional[str] = Field(default=None)
    duration_ms: Optional[str] = Field(default=None)
    query: Optional[str] = Field(default=None)
    status_flags: Optional[str] = Field(default=None)
    extended_info: Optional[str] = Field(default=None)


class RuntimeGenaiConfig(BaseModel):
    """Read model for table `runtime_genai_config`."""

    variable_name: str
    variable_value: str


class RuntimeMysqlServers(BaseModel):
    """Read model for table `runtime_mysql_servers`."""

    hostgroup_id: int = Field(default=0, description="CHECK: hostgroup_id>=0")
    hostname: str
    port: int = Field(default=3306, description="CHECK: port >= 0 AND port <= 65535")
    gtid_port: int = Field(default=0, description="CHECK: (gtid_port <> port OR gtid_port=0) AND gtid_port >= 0 AND gtid_port <= 65535")
    status: str = Field(default='ONLINE', description="CHECK: UPPER(status) IN ('ONLINE','SHUNNED','OFFLINE_SOFT', 'OFFLINE_HARD')")
    weight: int = Field(default=1, description="CHECK: weight >= 0 AND weight <=10000000")
    compression: int = Field(default=0, description="CHECK: compression IN(0,1)")
    max_connections: int = Field(default=1000, description="CHECK: max_connections >=0")
    max_replication_lag: int = Field(default=0, description="CHECK: max_replication_lag >= 0 AND max_replication_lag <= 126144000")
    use_ssl: int = Field(default=0, description="CHECK: use_ssl IN(0,1)")
    max_latency_ms: int = Field(default=0, description="CHECK: max_latency_ms>=0")
    comment: str = Field(default='')


class RuntimePgsqlServers(BaseModel):
    """Read model for table `runtime_pgsql_servers`."""

    hostgroup_id: int = Field(default=0, description="CHECK: hostgroup_id>=0")
    hostname: str
    port: int = Field(default=5432, description="CHECK: port >= 0 AND port <= 65535")
    status: str = Field(default='ONLINE', description="CHECK: UPPER(status) IN ('ONLINE','SHUNNED','OFFLINE_SOFT', 'OFFLINE_HARD')")
    weight: int = Field(default=1, description="CHECK: weight >= 0 AND weight <=10000000")
    compression: int = Field(default=0, description="CHECK: compression IN(0,1)")
    max_connections: int = Field(default=1000, description="CHECK: max_connections >=0")
    max_replication_lag: int = Field(default=0, description="CHECK: max_replication_lag >= 0 AND max_replication_lag <= 126144000")
    use_ssl: int = Field(default=0, description="CHECK: use_ssl IN(0,1)")
    max_latency_ms: int = Field(default=0, description="CHECK: max_latency_ms>=0")
    comment: str = Field(default='')


class StatsMysqlConnectionPool(BaseModel):
    """Read model for table `stats_mysql_connection_pool`."""

    hostgroup: Optional[int] = Field(default=None)
    srv_host: Optional[str] = Field(default=None)
    srv_port: Optional[int] = Field(default=None)
    status: Optional[str] = Field(default=None)
    ConnUsed: Optional[int] = Field(default=None)
    ConnFree: Optional[int] = Field(default=None)
    ConnOK: Optional[int] = Field(default=None)
    ConnERR: Optional[int] = Field(default=None)
    MaxConnUsed: Optional[int] = Field(default=None)
    Queries: Optional[int] = Field(default=None)
    Queries_GTID_sync: Optional[int] = Field(default=None)
    Bytes_data_sent: Optional[int] = Field(default=None)
    Bytes_data_recv: Optional[int] = Field(default=None)
    Latency_us: Optional[int] = Field(default=None)


class StatsPgsqlConnectionPool(BaseModel):
    """Read model for table `stats_pgsql_connection_pool`."""

    hostgroup: Optional[int] = Field(default=None)
    srv_host: Optional[str] = Field(default=None)
    srv_port: Optional[int] = Field(default=None)
    status: Optional[str] = Field(default=None)
    ConnUsed: Optional[int] = Field(default=None)
    ConnFree: Optional[int] = Field(default=None)
    ConnOK: Optional[int] = Field(default=None)
    ConnERR: Optional[int] = Field(default=None)
    MaxConnUsed: Optional[int] = Field(default=None)
    Queries: Optional[int] = Field(default=None)
    Bytes_data_sent: Optional[int] = Field(default=None)
    Bytes_data_recv: Optional[int] = Field(default=None)
    Latency_us: Optional[int] = Field(default=None)


class RuntimeRestapiRoutes(BaseModel):
    """Read model for table `runtime_restapi_routes`."""

    id: int
    active: int = Field(default=1, description="CHECK: active IN (0,1)")
    timeout_ms: int = Field(description="CHECK: timeout_ms>=100 AND timeout_ms<=100000000")
    method: str = Field(description="CHECK: UPPER(method) IN ('GET','POST')")
    uri: str
    script: str
    comment: str = Field(default='')


class StatsMcpQueryDigestReset(BaseModel):
    """Read model for table `stats_mcp_query_digest_reset`."""

    tool_name: str
    run_id: Optional[int] = Field(default=None)
    digest: str
    digest_text: str
    count_star: int
    first_seen: int
    last_seen: int
    sum_time: int
    min_time: int
    max_time: int
    PRIMARY: Optional[str] = Field(default=None)


class StatsMysqlFreeConnections(BaseModel):
    """Read model for table `stats_mysql_free_connections`."""
    model_config = ConfigDict(protected_namespaces=())

    fd: int
    hostgroup: int
    srv_host: str
    srv_port: int
    user: str
    schema: Optional[str] = Field(default=None)
    init_connect: Optional[str] = Field(default=None)
    time_zone: Optional[str] = Field(default=None)
    sql_mode: Optional[str] = Field(default=None)
    autocommit: Optional[str] = Field(default=None)
    idle_ms: Optional[int] = Field(default=None)
    statistics: Optional[str] = Field(default=None)
    mysql_info: Optional[str] = Field(default=None)


class StatsPgsqlFreeConnections(BaseModel):
    """Read model for table `stats_pgsql_free_connections`."""

    fd: int
    hostgroup: int
    srv_host: str
    srv_port: int
    user: str
    database: Optional[str] = Field(default=None)
    init_connect: Optional[str] = Field(default=None)
    time_zone: Optional[str] = Field(default=None)
    sql_mode: Optional[str] = Field(default=None)
    idle_ms: Optional[int] = Field(default=None)
    statistics: Optional[str] = Field(default=None)
    pgsql_info: Optional[str] = Field(default=None)


class MysqlGaleraHostgroups(BaseModel):
    """Read model for table `mysql_galera_hostgroups`."""

    writer_hostgroup: int = Field(description="CHECK: writer_hostgroup>=0")
    backup_writer_hostgroup: int = Field(description="CHECK: backup_writer_hostgroup>=0 AND backup_writer_hostgroup<>writer_hostgroup")
    reader_hostgroup: int = Field(description="CHECK: reader_hostgroup<>writer_hostgroup AND backup_writer_hostgroup<>reader_hostgroup AND reader_hostgroup>0")
    offline_hostgroup: int = Field(description="CHECK: offline_hostgroup<>writer_hostgroup AND offline_hostgroup<>reader_hostgroup AND backup_writer_hostgroup<>offline_hostgroup AND offline_hostgroup>=0")
    active: int = Field(default=1, description="CHECK: active IN (0,1)")
    max_writers: int = Field(default=1, description="CHECK: max_writers >= 0")
    writer_is_also_reader: int = Field(default=0, description="CHECK: writer_is_also_reader IN (0,1,2)")
    max_transactions_behind: int = Field(default=0, description="CHECK: max_transactions_behind>=0")
    comment: Optional[str] = Field(default=None)
    UNIQUE: Optional[str] = Field(default=None)


class MysqlGaleraHostgroupsCreate(BaseModel):
    """Create/update model for `mysql_galera_hostgroups`."""

    writer_hostgroup: int = Field(description="CHECK: writer_hostgroup>=0")
    backup_writer_hostgroup: int = Field(description="CHECK: backup_writer_hostgroup>=0 AND backup_writer_hostgroup<>writer_hostgroup")
    reader_hostgroup: int = Field(description="CHECK: reader_hostgroup<>writer_hostgroup AND backup_writer_hostgroup<>reader_hostgroup AND reader_hostgroup>0")
    offline_hostgroup: int = Field(description="CHECK: offline_hostgroup<>writer_hostgroup AND offline_hostgroup<>reader_hostgroup AND backup_writer_hostgroup<>offline_hostgroup AND offline_hostgroup>=0")
    active: Optional[int] = Field(default=1, description="CHECK: active IN (0,1)")
    max_writers: Optional[int] = Field(default=1, description="CHECK: max_writers >= 0")
    writer_is_also_reader: Optional[int] = Field(default=0, description="CHECK: writer_is_also_reader IN (0,1,2)")
    max_transactions_behind: Optional[int] = Field(default=0, description="CHECK: max_transactions_behind>=0")
    comment: Optional[str] = Field(default=None)
    UNIQUE: Optional[str] = Field(default=None)


class RuntimeMcpQueryRules(BaseModel):
    """Read model for table `runtime_mcp_query_rules`."""

    rule_id: int
    active: int = Field(default=0, description="CHECK: active IN (0,1)")
    username: Optional[str] = Field(default=None)
    target_id: Optional[str] = Field(default=None)
    schemaname: Optional[str] = Field(default=None)
    tool_name: Optional[str] = Field(default=None)
    match_pattern: Optional[str] = Field(default=None)
    negate_match_pattern: int = Field(default=0, description="CHECK: negate_match_pattern IN (0,1)")
    re_modifiers: Optional[str] = Field(default='CASELESS')
    flagIN: int = Field(default=0)
    flagOUT: Optional[int] = Field(default=None, description="CHECK: flagOUT >= 0")
    replace_pattern: Optional[str] = Field(default=None)
    timeout_ms: Optional[int] = Field(default=None, description="CHECK: timeout_ms >= 0")
    error_msg: Optional[str] = Field(default=None)
    OK_msg: Optional[str] = Field(default=None)
    log: Optional[int] = Field(default=None, description="CHECK: log IN (0,1)")
    apply: int = Field(default=1, description="CHECK: apply IN (0,1)")
    comment: Optional[str] = Field(default=None)


class StatsMysqlClientHostCache(BaseModel):
    """Read model for table `stats_mysql_client_host_cache`."""

    client_address: str
    error_count: int
    last_updated: int


class StatsMysqlCommandsCounters(BaseModel):
    """Read model for table `stats_mysql_commands_counters`."""

    Command: str
    Total_Time_us: int
    Total_cnt: int
    cnt_100us: int
    cnt_500us: int
    cnt_1ms: int
    cnt_5ms: int
    cnt_10ms: int
    cnt_50ms: int
    cnt_100ms: int
    cnt_500ms: int
    cnt_1s: int
    cnt_5s: int
    cnt_10s: int


class StatsPgsqlClientHostCache(BaseModel):
    """Read model for table `stats_pgsql_client_host_cache`."""

    client_address: str
    error_count: int
    last_updated: int


class StatsPgsqlCommandsCounters(BaseModel):
    """Read model for table `stats_pgsql_commands_counters`."""

    Command: str
    Total_Time_us: int
    Total_cnt: int
    cnt_100us: int
    cnt_500us: int
    cnt_1ms: int
    cnt_5ms: int
    cnt_10ms: int
    cnt_50ms: int
    cnt_100ms: int
    cnt_500ms: int
    cnt_1s: int
    cnt_5s: int
    cnt_10s: int


class StatsProxysqlServersStatus(BaseModel):
    """Read model for table `stats_proxysql_servers_status`."""

    hostname: str
    port: int = Field(default=6032)
    weight: int = Field(default=0, description="CHECK: weight >= 0")
    master: str
    global_version: int
    check_age_us: int
    ping_time_us: int
    checks_OK: int
    checks_ERR: int


class MysqlServersSslParams(BaseModel):
    """Read model for table `mysql_servers_ssl_params`."""

    hostname: str
    port: int = Field(default=3306, description="CHECK: port >= 0 AND port <= 65535")
    username: str = Field(default='')
    ssl_ca: str = Field(default='')
    ssl_cert: str = Field(default='')
    ssl_key: str = Field(default='')
    ssl_capath: str = Field(default='')
    ssl_crl: str = Field(default='')
    ssl_crlpath: str = Field(default='')
    ssl_cipher: str = Field(default='')
    tls_version: str = Field(default='')
    comment: str = Field(default='')


class MysqlServersSslParamsCreate(BaseModel):
    """Create/update model for `mysql_servers_ssl_params`."""

    hostname: str
    port: Optional[int] = Field(default=3306, description="CHECK: port >= 0 AND port <= 65535")
    username: Optional[str] = Field(default='')
    ssl_ca: Optional[str] = Field(default='')
    ssl_cert: Optional[str] = Field(default='')
    ssl_key: Optional[str] = Field(default='')
    ssl_capath: Optional[str] = Field(default='')
    ssl_crl: Optional[str] = Field(default='')
    ssl_crlpath: Optional[str] = Field(default='')
    ssl_cipher: Optional[str] = Field(default='')
    tls_version: Optional[str] = Field(default='')
    comment: Optional[str] = Field(default='')


class RuntimeClickhouseUsers(BaseModel):
    """Read model for table `runtime_clickhouse_users`."""

    username: str
    password: Optional[str] = Field(default=None)
    active: int = Field(default=1, description="CHECK: active IN (0,1)")
    max_connections: int = Field(default=10000, description="CHECK: max_connections >=0")
    PRIMARY: Optional[str] = Field(default=None)


class RuntimeProxysqlServers(BaseModel):
    """Read model for table `runtime_proxysql_servers`."""

    hostname: str
    port: int = Field(default=6032)
    weight: int = Field(default=0, description="CHECK: weight >= 0")
    comment: str = Field(default='')


class StatsMysqlQueryEvents(BaseModel):
    """Read model for table `stats_mysql_query_events`."""

    id: Optional[int] = Field(default=None)
    thread_id: Optional[int] = Field(default=None)
    username: Optional[str] = Field(default=None)
    schemaname: Optional[str] = Field(default=None)
    start_time: Optional[int] = Field(default=None)
    end_time: Optional[int] = Field(default=None)
    query_digest: Optional[str] = Field(default=None)
    query: Optional[str] = Field(default=None)
    server: Optional[str] = Field(default=None)
    client: Optional[str] = Field(default=None)
    event_type: Optional[int] = Field(default=None)
    hid: Optional[int] = Field(default=None)
    extra_info: Optional[str] = Field(default=None)
    affected_rows: Optional[int] = Field(default=None)
    last_insert_id: Optional[int] = Field(default=None)
    rows_sent: Optional[int] = Field(default=None)
    client_stmt_id: Optional[int] = Field(default=None)
    gtid: Optional[str] = Field(default=None)
    errno: Optional[int] = Field(default=None)
    error: Optional[str] = Field(default=None)


class StatsMcpQueryToolsCounters(BaseModel):
    """Read model for table `stats_mcp_query_tools_counters`."""
    model_config = ConfigDict(protected_namespaces=())

    endpoint: str
    tool: str
    schema: str
    count: int
    first_seen: int
    last_seen: int
    sum_time: int
    min_time: int
    max_time: int
    PRIMARY: Optional[str] = Field(default=None)


class StatsMysqlQueryDigestReset(BaseModel):
    """Read model for table `stats_mysql_query_digest_reset`."""

    hostgroup: Optional[int] = Field(default=None)
    schemaname: str
    username: str
    client_address: str
    digest: str
    digest_text: str
    count_star: int
    first_seen: int
    last_seen: int
    sum_time: int
    min_time: int
    max_time: int
    sum_rows_affected: int
    sum_rows_sent: int
    PRIMARY: Optional[str] = Field(default=None)


class StatsPgsqlQueryDigestReset(BaseModel):
    """Read model for table `stats_pgsql_query_digest_reset`."""

    hostgroup: Optional[int] = Field(default=None)
    database: str
    username: str
    client_address: str
    digest: str
    digest_text: str
    count_star: int
    first_seen: int
    last_seen: int
    sum_time: int
    min_time: int
    max_time: int
    sum_rows_affected: int
    sum_rows_sent: int
    PRIMARY: Optional[str] = Field(default=None)


class StatsProxysqlMessageMetrics(BaseModel):
    """Read model for table `stats_proxysql_message_metrics`."""

    message_id: str
    filename: str
    line: int = Field(default=0, description="CHECK: line >= 0")
    func: str
    count_star: int
    first_seen: int
    last_seen: int


class StatsProxysqlServersMetrics(BaseModel):
    """Read model for table `stats_proxysql_servers_metrics`."""

    hostname: str
    port: int = Field(default=6032)
    weight: int = Field(default=0, description="CHECK: weight >= 0")
    comment: str = Field(default='')
    response_time_ms: int
    Uptime_s: int
    last_check_ms: int
    Queries: int
    Client_Connections_connected: int
    Client_Connections_created: int


class RuntimeMcpAuthProfiles(BaseModel):
    """Read model for table `runtime_mcp_auth_profiles`."""

    auth_profile_id: str
    db_username: str
    db_password: str
    default_schema: Optional[str] = Field(default='')
    use_ssl: int = Field(default=0, description="CHECK: use_ssl IN (0,1)")
    ssl_mode: Optional[str] = Field(default='')
    comment: Optional[str] = Field(default='')


class RuntimeMysqlQueryRules(BaseModel):
    """Read model for table `runtime_mysql_query_rules`."""

    rule_id: int
    active: int = Field(default=0, description="CHECK: active IN (0,1)")
    username: Optional[str] = Field(default=None)
    schemaname: Optional[str] = Field(default=None)
    flagIN: int = Field(default=0, description="CHECK: flagIN >= 0")
    client_addr: Optional[str] = Field(default=None)
    proxy_addr: Optional[str] = Field(default=None)
    proxy_port: Optional[int] = Field(default=None, description="CHECK: proxy_port >= 0 AND proxy_port <= 65535")
    digest: Optional[str] = Field(default=None)
    match_digest: Optional[str] = Field(default=None)
    match_pattern: Optional[str] = Field(default=None)
    negate_match_pattern: int = Field(default=0, description="CHECK: negate_match_pattern IN (0,1)")
    re_modifiers: Optional[str] = Field(default='CASELESS')
    flagOUT: Optional[int] = Field(default=None, description="CHECK: flagOUT >= 0")
    replace_pattern: Optional[str] = Field(default=None, description="CHECK: CASE WHEN replace_pattern IS NULL THEN 1 WHEN replace_pattern IS NOT NULL AND match_pattern IS NOT NULL THEN 1 ELSE 0 END")
    destination_hostgroup: Optional[int] = Field(default='NULL')
    cache_ttl: Optional[int] = Field(default=None, description="CHECK: cache_ttl > 0")
    cache_empty_result: Optional[int] = Field(default='NULL', description="CHECK: cache_empty_result IN (0,1)")
    cache_timeout: Optional[int] = Field(default=None, description="CHECK: cache_timeout >= 0")
    reconnect: Optional[int] = Field(default='NULL', description="CHECK: reconnect IN (0,1)")
    timeout: Optional[int] = Field(default=None, description="CHECK: timeout >= 0")
    retries: Optional[int] = Field(default=None, description="CHECK: retries>=0 AND retries <=1000")
    delay: Optional[int] = Field(default=None, description="CHECK: delay >=0")
    next_query_flagIN: Optional[int] = Field(default=None)
    mirror_flagOUT: Optional[int] = Field(default=None)
    mirror_hostgroup: Optional[int] = Field(default=None)
    error_msg: Optional[str] = Field(default=None)
    OK_msg: Optional[str] = Field(default=None)
    sticky_conn: Optional[int] = Field(default=None, description="CHECK: sticky_conn IN (0,1)")
    multiplex: Optional[int] = Field(default=None, description="CHECK: multiplex IN (0,1,2)")
    gtid_from_hostgroup: Optional[int] = Field(default=None)
    log: Optional[int] = Field(default=None, description="CHECK: log IN (0,1)")
    apply: int = Field(default=0, description="CHECK: apply IN (0,1)")
    attributes: str = Field(default='', description="CHECK: JSON_VALID(attributes) OR attributes = ''")
    comment: Optional[str] = Field(default=None)


class RuntimePgsqlQueryRules(BaseModel):
    """Read model for table `runtime_pgsql_query_rules`."""

    rule_id: int
    active: int = Field(default=0, description="CHECK: active IN (0,1)")
    username: Optional[str] = Field(default=None)
    database: Optional[str] = Field(default=None)
    flagIN: int = Field(default=0, description="CHECK: flagIN >= 0")
    client_addr: Optional[str] = Field(default=None)
    proxy_addr: Optional[str] = Field(default=None)
    proxy_port: Optional[int] = Field(default=None, description="CHECK: proxy_port >= 0 AND proxy_port <= 65535")
    digest: Optional[str] = Field(default=None)
    match_digest: Optional[str] = Field(default=None)
    match_pattern: Optional[str] = Field(default=None)
    negate_match_pattern: int = Field(default=0, description="CHECK: negate_match_pattern IN (0,1)")
    re_modifiers: Optional[str] = Field(default='CASELESS')
    flagOUT: Optional[int] = Field(default=None, description="CHECK: flagOUT >= 0")
    replace_pattern: Optional[str] = Field(default=None, description="CHECK: CASE WHEN replace_pattern IS NULL THEN 1 WHEN replace_pattern IS NOT NULL AND match_pattern IS NOT NULL THEN 1 ELSE 0 END")
    destination_hostgroup: Optional[int] = Field(default='NULL')
    cache_ttl: Optional[int] = Field(default=None, description="CHECK: cache_ttl > 0")
    cache_empty_result: Optional[int] = Field(default='NULL', description="CHECK: cache_empty_result IN (0,1)")
    cache_timeout: Optional[int] = Field(default=None, description="CHECK: cache_timeout >= 0")
    reconnect: Optional[int] = Field(default='NULL', description="CHECK: reconnect IN (0,1)")
    timeout: Optional[int] = Field(default=None, description="CHECK: timeout >= 0")
    retries: Optional[int] = Field(default=None, description="CHECK: retries>=0 AND retries <=1000")
    delay: Optional[int] = Field(default=None, description="CHECK: delay >=0")
    next_query_flagIN: Optional[int] = Field(default=None)
    mirror_flagOUT: Optional[int] = Field(default=None)
    mirror_hostgroup: Optional[int] = Field(default=None)
    error_msg: Optional[str] = Field(default=None)
    OK_msg: Optional[str] = Field(default=None)
    sticky_conn: Optional[int] = Field(default=None, description="CHECK: sticky_conn IN (0,1)")
    multiplex: Optional[int] = Field(default=None, description="CHECK: multiplex IN (0,1,2)")
    log: Optional[int] = Field(default=None, description="CHECK: log IN (0,1)")
    apply: int = Field(default=0, description="CHECK: apply IN (0,1)")
    attributes: str = Field(default='', description="CHECK: JSON_VALID(attributes) OR attributes = ''")
    comment: Optional[str] = Field(default=None)


class MysqlHostgroupAttributes(BaseModel):
    """Read model for table `mysql_hostgroup_attributes`."""

    hostgroup_id: int
    max_num_online_servers: int = Field(default=1000000, description="CHECK: max_num_online_servers>=0 AND max_num_online_servers <= 1000000")
    autocommit: int = Field(default=-1, description="CHECK: autocommit IN (-1, 0, 1)")
    free_connections_pct: int = Field(default=10, description="CHECK: free_connections_pct >= 0 AND free_connections_pct <= 100")
    init_connect: str = Field(default='')
    multiplex: int = Field(default=1, description="CHECK: multiplex IN (0, 1)")
    connection_warming: int = Field(default=0, description="CHECK: connection_warming IN (0, 1)")
    throttle_connections_per_sec: int = Field(default=1000000, description="CHECK: throttle_connections_per_sec >= 1 AND throttle_connections_per_sec <= 1000000")
    ignore_session_variables: str = Field(default='', description="CHECK: JSON_VALID(ignore_session_variables) OR ignore_session_variables = ''")
    hostgroup_settings: str = Field(default='', description="CHECK: JSON_VALID(hostgroup_settings) OR hostgroup_settings = ''")
    servers_defaults: str = Field(default='', description="CHECK: JSON_VALID(servers_defaults) OR servers_defaults = ''")
    comment: str = Field(default='')


class MysqlHostgroupAttributesCreate(BaseModel):
    """Create/update model for `mysql_hostgroup_attributes`."""

    hostgroup_id: int
    max_num_online_servers: Optional[int] = Field(default=1000000, description="CHECK: max_num_online_servers>=0 AND max_num_online_servers <= 1000000")
    autocommit: Optional[int] = Field(default=-1, description="CHECK: autocommit IN (-1, 0, 1)")
    free_connections_pct: Optional[int] = Field(default=10, description="CHECK: free_connections_pct >= 0 AND free_connections_pct <= 100")
    init_connect: Optional[str] = Field(default='')
    multiplex: Optional[int] = Field(default=1, description="CHECK: multiplex IN (0, 1)")
    connection_warming: Optional[int] = Field(default=0, description="CHECK: connection_warming IN (0, 1)")
    throttle_connections_per_sec: Optional[int] = Field(default=1000000, description="CHECK: throttle_connections_per_sec >= 1 AND throttle_connections_per_sec <= 1000000")
    ignore_session_variables: Optional[str] = Field(default='', description="CHECK: JSON_VALID(ignore_session_variables) OR ignore_session_variables = ''")
    hostgroup_settings: Optional[str] = Field(default='', description="CHECK: JSON_VALID(hostgroup_settings) OR hostgroup_settings = ''")
    servers_defaults: Optional[str] = Field(default='', description="CHECK: JSON_VALID(servers_defaults) OR servers_defaults = ''")
    comment: Optional[str] = Field(default='')


class PgsqlHostgroupAttributes(BaseModel):
    """Read model for table `pgsql_hostgroup_attributes`."""

    hostgroup_id: int
    max_num_online_servers: int = Field(default=1000000, description="CHECK: max_num_online_servers>=0 AND max_num_online_servers <= 1000000")
    autocommit: int = Field(default=-1, description="CHECK: autocommit IN (-1, 0, 1)")
    free_connections_pct: int = Field(default=10, description="CHECK: free_connections_pct >= 0 AND free_connections_pct <= 100")
    init_connect: str = Field(default='')
    multiplex: int = Field(default=1, description="CHECK: multiplex IN (0, 1)")
    connection_warming: int = Field(default=0, description="CHECK: connection_warming IN (0, 1)")
    throttle_connections_per_sec: int = Field(default=1000000, description="CHECK: throttle_connections_per_sec >= 1 AND throttle_connections_per_sec <= 1000000")
    ignore_session_variables: str = Field(default='', description="CHECK: JSON_VALID(ignore_session_variables) OR ignore_session_variables = ''")
    hostgroup_settings: str = Field(default='', description="CHECK: JSON_VALID(hostgroup_settings) OR hostgroup_settings = ''")
    servers_defaults: str = Field(default='', description="CHECK: JSON_VALID(servers_defaults) OR servers_defaults = ''")
    comment: str = Field(default='')


class PgsqlHostgroupAttributesCreate(BaseModel):
    """Create/update model for `pgsql_hostgroup_attributes`."""

    hostgroup_id: int
    max_num_online_servers: Optional[int] = Field(default=1000000, description="CHECK: max_num_online_servers>=0 AND max_num_online_servers <= 1000000")
    autocommit: Optional[int] = Field(default=-1, description="CHECK: autocommit IN (-1, 0, 1)")
    free_connections_pct: Optional[int] = Field(default=10, description="CHECK: free_connections_pct >= 0 AND free_connections_pct <= 100")
    init_connect: Optional[str] = Field(default='')
    multiplex: Optional[int] = Field(default=1, description="CHECK: multiplex IN (0, 1)")
    connection_warming: Optional[int] = Field(default=0, description="CHECK: connection_warming IN (0, 1)")
    throttle_connections_per_sec: Optional[int] = Field(default=1000000, description="CHECK: throttle_connections_per_sec >= 1 AND throttle_connections_per_sec <= 1000000")
    ignore_session_variables: Optional[str] = Field(default='', description="CHECK: JSON_VALID(ignore_session_variables) OR ignore_session_variables = ''")
    hostgroup_settings: Optional[str] = Field(default='', description="CHECK: JSON_VALID(hostgroup_settings) OR hostgroup_settings = ''")
    servers_defaults: Optional[str] = Field(default='', description="CHECK: JSON_VALID(servers_defaults) OR servers_defaults = ''")
    comment: Optional[str] = Field(default='')


class RuntimeMysqlLdapMapping(BaseModel):
    """Read model for table `runtime_mysql_ldap_mapping`."""

    priority: int
    frontend_entity: str
    backend_entity: str
    comment: str = Field(default='')
    UNIQUE: Optional[str] = Field(default=None)


class RuntimePgsqlLdapMapping(BaseModel):
    """Read model for table `runtime_pgsql_ldap_mapping`."""

    priority: int
    frontend_entity: str
    backend_entity: str
    comment: str = Field(default='')
    UNIQUE: Optional[str] = Field(default=None)


class StatsProxysqlServersChecksums(BaseModel):
    """Read model for table `stats_proxysql_servers_checksums`."""

    hostname: str
    port: int = Field(default=6032)
    name: str
    version: int
    epoch: int
    checksum: str
    changed_at: int
    updated_at: int
    diff_check: int


class MysqlAwsAuroraHostgroups(BaseModel):
    """Read model for table `mysql_aws_aurora_hostgroups`."""

    writer_hostgroup: int = Field(description="CHECK: writer_hostgroup>=0")
    reader_hostgroup: int = Field(description="CHECK: reader_hostgroup<>writer_hostgroup AND reader_hostgroup>0")
    active: int = Field(default=1, description="CHECK: active IN (0,1)")
    aurora_port: int = Field(default=3306)
    domain_name: str = Field(description="CHECK: SUBSTR(domain_name,1,1) = '.'")
    max_lag_ms: int = Field(default=600000, description="CHECK: max_lag_ms>= 10 AND max_lag_ms <= 600000")
    check_interval_ms: int = Field(default=1000, description="CHECK: check_interval_ms >= 100 AND check_interval_ms <= 600000")
    check_timeout_ms: int = Field(default=800, description="CHECK: check_timeout_ms >= 80 AND check_timeout_ms <= 3000")
    writer_is_also_reader: int = Field(default=0, description="CHECK: writer_is_also_reader IN (0,1)")
    new_reader_weight: int = Field(default=1, description="CHECK: new_reader_weight >= 0 AND new_reader_weight <=10000000")
    add_lag_ms: int = Field(default=30, description="CHECK: add_lag_ms >= 0 AND add_lag_ms <= 600000")
    min_lag_ms: int = Field(default=30, description="CHECK: min_lag_ms >= 0 AND min_lag_ms <= 600000")
    lag_num_checks: int = Field(default=1, description="CHECK: lag_num_checks >= 1 AND lag_num_checks <= 16")
    comment: Optional[str] = Field(default=None)
    UNIQUE: Optional[str] = Field(default=None)


class MysqlAwsAuroraHostgroupsCreate(BaseModel):
    """Create/update model for `mysql_aws_aurora_hostgroups`."""

    writer_hostgroup: int = Field(description="CHECK: writer_hostgroup>=0")
    reader_hostgroup: int = Field(description="CHECK: reader_hostgroup<>writer_hostgroup AND reader_hostgroup>0")
    active: Optional[int] = Field(default=1, description="CHECK: active IN (0,1)")
    aurora_port: Optional[int] = Field(default=3306)
    domain_name: str = Field(description="CHECK: SUBSTR(domain_name,1,1) = '.'")
    max_lag_ms: Optional[int] = Field(default=600000, description="CHECK: max_lag_ms>= 10 AND max_lag_ms <= 600000")
    check_interval_ms: Optional[int] = Field(default=1000, description="CHECK: check_interval_ms >= 100 AND check_interval_ms <= 600000")
    check_timeout_ms: Optional[int] = Field(default=800, description="CHECK: check_timeout_ms >= 80 AND check_timeout_ms <= 3000")
    writer_is_also_reader: Optional[int] = Field(default=0, description="CHECK: writer_is_also_reader IN (0,1)")
    new_reader_weight: Optional[int] = Field(default=1, description="CHECK: new_reader_weight >= 0 AND new_reader_weight <=10000000")
    add_lag_ms: Optional[int] = Field(default=30, description="CHECK: add_lag_ms >= 0 AND add_lag_ms <= 600000")
    min_lag_ms: Optional[int] = Field(default=30, description="CHECK: min_lag_ms >= 0 AND min_lag_ms <= 600000")
    lag_num_checks: Optional[int] = Field(default=1, description="CHECK: lag_num_checks >= 1 AND lag_num_checks <= 16")
    comment: Optional[str] = Field(default=None)
    UNIQUE: Optional[str] = Field(default=None)


class RuntimeMcpTargetProfiles(BaseModel):
    """Read model for table `runtime_mcp_target_profiles`."""

    target_id: str
    protocol: RuntimeMcpTargetProfiles_protocol_enum = Field(description="CHECK: protocol IN ('mysql','pgsql')")
    hostgroup_id: int = Field(description="CHECK: hostgroup_id >= 0")
    auth_profile_id: str
    description: Optional[str] = Field(default='')
    max_rows: int = Field(default=200, description="CHECK: max_rows > 0")
    timeout_ms: int = Field(default=2000, description="CHECK: timeout_ms >= 0")
    allow_explain: int = Field(default=1, description="CHECK: allow_explain IN (0,1)")
    allow_discovery: int = Field(default=1, description="CHECK: allow_discovery IN (0,1)")
    active: int = Field(default=1, description="CHECK: active IN (0,1)")
    comment: Optional[str] = Field(default='')


class StatsMysqlConnectionPoolReset(BaseModel):
    """Read model for table `stats_mysql_connection_pool_reset`."""

    hostgroup: Optional[int] = Field(default=None)
    srv_host: Optional[str] = Field(default=None)
    srv_port: Optional[int] = Field(default=None)
    status: Optional[str] = Field(default=None)
    ConnUsed: Optional[int] = Field(default=None)
    ConnFree: Optional[int] = Field(default=None)
    ConnOK: Optional[int] = Field(default=None)
    ConnERR: Optional[int] = Field(default=None)
    MaxConnUsed: Optional[int] = Field(default=None)
    Queries: Optional[int] = Field(default=None)
    Queries_GTID_sync: Optional[int] = Field(default=None)
    Bytes_data_sent: Optional[int] = Field(default=None)
    Bytes_data_recv: Optional[int] = Field(default=None)
    Latency_us: Optional[int] = Field(default=None)


class StatsPgsqlConnectionPoolReset(BaseModel):
    """Read model for table `stats_pgsql_connection_pool_reset`."""

    hostgroup: Optional[int] = Field(default=None)
    srv_host: Optional[str] = Field(default=None)
    srv_port: Optional[int] = Field(default=None)
    status: Optional[str] = Field(default=None)
    ConnUsed: Optional[int] = Field(default=None)
    ConnFree: Optional[int] = Field(default=None)
    ConnOK: Optional[int] = Field(default=None)
    ConnERR: Optional[int] = Field(default=None)
    MaxConnUsed: Optional[int] = Field(default=None)
    Queries: Optional[int] = Field(default=None)
    Bytes_data_sent: Optional[int] = Field(default=None)
    Bytes_data_recv: Optional[int] = Field(default=None)
    Latency_us: Optional[int] = Field(default=None)


class MysqlReplicationHostgroups(BaseModel):
    """Read model for table `mysql_replication_hostgroups`."""

    writer_hostgroup: int = Field(description="CHECK: writer_hostgroup>=0")
    reader_hostgroup: int = Field(description="CHECK: reader_hostgroup<>writer_hostgroup AND reader_hostgroup>=0")
    check_type: str = Field(default='read_only', description="CHECK: LOWER(check_type) IN ('read_only','innodb_read_only','super_read_only','read_only|innodb_read_only','read_only&innodb_read_only')")
    comment: str = Field(default='')
    UNIQUE: Optional[str] = Field(default=None)


class MysqlReplicationHostgroupsCreate(BaseModel):
    """Create/update model for `mysql_replication_hostgroups`."""

    writer_hostgroup: int = Field(description="CHECK: writer_hostgroup>=0")
    reader_hostgroup: int = Field(description="CHECK: reader_hostgroup<>writer_hostgroup AND reader_hostgroup>=0")
    check_type: Optional[str] = Field(default='read_only', description="CHECK: LOWER(check_type) IN ('read_only','innodb_read_only','super_read_only','read_only|innodb_read_only','read_only&innodb_read_only')")
    comment: Optional[str] = Field(default='')
    UNIQUE: Optional[str] = Field(default=None)


class PgsqlReplicationHostgroups(BaseModel):
    """Read model for table `pgsql_replication_hostgroups`."""

    writer_hostgroup: int = Field(description="CHECK: writer_hostgroup>=0")
    reader_hostgroup: int = Field(description="CHECK: reader_hostgroup<>writer_hostgroup AND reader_hostgroup>=0")
    check_type: str = Field(default='read_only', description="CHECK: LOWER(check_type) IN ('read_only')")
    comment: str = Field(default='')
    UNIQUE: Optional[str] = Field(default=None)


class PgsqlReplicationHostgroupsCreate(BaseModel):
    """Create/update model for `pgsql_replication_hostgroups`."""

    writer_hostgroup: int = Field(description="CHECK: writer_hostgroup>=0")
    reader_hostgroup: int = Field(description="CHECK: reader_hostgroup<>writer_hostgroup AND reader_hostgroup>=0")
    check_type: Optional[str] = Field(default='read_only', description="CHECK: LOWER(check_type) IN ('read_only')")
    comment: Optional[str] = Field(default='')
    UNIQUE: Optional[str] = Field(default=None)


class StatsMysqlClientHostCacheReset(BaseModel):
    """Read model for table `stats_mysql_client_host_cache_reset`."""

    client_address: str
    error_count: int
    last_updated: int


class StatsPgsqlClientHostCacheReset(BaseModel):
    """Read model for table `stats_pgsql_client_host_cache_reset`."""

    client_address: str
    error_count: int
    last_updated: int


class MysqlFirewallWhitelistRules(BaseModel):
    """Read model for table `mysql_firewall_whitelist_rules`."""

    active: int = Field(default=1, description="CHECK: active IN (0,1)")
    username: str
    client_address: str
    schemaname: str
    flagIN: int = Field(default=0)
    digest: str
    comment: str


class MysqlFirewallWhitelistRulesCreate(BaseModel):
    """Create/update model for `mysql_firewall_whitelist_rules`."""

    active: Optional[int] = Field(default=1, description="CHECK: active IN (0,1)")
    username: str
    client_address: str
    schemaname: str
    flagIN: Optional[int] = Field(default=0)
    digest: str
    comment: str


class MysqlFirewallWhitelistUsers(BaseModel):
    """Read model for table `mysql_firewall_whitelist_users`."""

    active: int = Field(default=1, description="CHECK: active IN (0,1)")
    username: str
    client_address: str
    mode: MysqlFirewallWhitelistUsers_mode_enum = Field(default="('OFF", description="CHECK: mode IN ('OFF','DETECTING','PROTECTING')")
    comment: str


class MysqlFirewallWhitelistUsersCreate(BaseModel):
    """Create/update model for `mysql_firewall_whitelist_users`."""

    active: Optional[int] = Field(default=1, description="CHECK: active IN (0,1)")
    username: str
    client_address: str
    mode: Optional[MysqlFirewallWhitelistUsers_mode_enum] = Field(default="('OFF", description="CHECK: mode IN ('OFF','DETECTING','PROTECTING')")
    comment: str


class MysqlQueryRulesFastRouting(BaseModel):
    """Read model for table `mysql_query_rules_fast_routing`."""

    username: str
    schemaname: str
    flagIN: int = Field(default=0)
    destination_hostgroup: int = Field(description="CHECK: destination_hostgroup >= 0")
    comment: str


class MysqlQueryRulesFastRoutingCreate(BaseModel):
    """Create/update model for `mysql_query_rules_fast_routing`."""

    username: str
    schemaname: str
    flagIN: Optional[int] = Field(default=0)
    destination_hostgroup: int = Field(description="CHECK: destination_hostgroup >= 0")
    comment: str


class PgsqlFirewallWhitelistRules(BaseModel):
    """Read model for table `pgsql_firewall_whitelist_rules`."""

    active: int = Field(default=1, description="CHECK: active IN (0,1)")
    username: str
    client_address: str
    database: str
    flagIN: int = Field(default=0)
    digest: str
    comment: str


class PgsqlFirewallWhitelistRulesCreate(BaseModel):
    """Create/update model for `pgsql_firewall_whitelist_rules`."""

    active: Optional[int] = Field(default=1, description="CHECK: active IN (0,1)")
    username: str
    client_address: str
    database: str
    flagIN: Optional[int] = Field(default=0)
    digest: str
    comment: str


class PgsqlFirewallWhitelistUsers(BaseModel):
    """Read model for table `pgsql_firewall_whitelist_users`."""

    active: int = Field(default=1, description="CHECK: active IN (0,1)")
    username: str
    client_address: str
    mode: PgsqlFirewallWhitelistUsers_mode_enum = Field(default="('OFF", description="CHECK: mode IN ('OFF','DETECTING','PROTECTING')")
    comment: str


class PgsqlFirewallWhitelistUsersCreate(BaseModel):
    """Create/update model for `pgsql_firewall_whitelist_users`."""

    active: Optional[int] = Field(default=1, description="CHECK: active IN (0,1)")
    username: str
    client_address: str
    mode: Optional[PgsqlFirewallWhitelistUsers_mode_enum] = Field(default="('OFF", description="CHECK: mode IN ('OFF','DETECTING','PROTECTING')")
    comment: str


class PgsqlQueryRulesFastRouting(BaseModel):
    """Read model for table `pgsql_query_rules_fast_routing`."""

    username: str
    database: str
    flagIN: int = Field(default=0)
    destination_hostgroup: int = Field(description="CHECK: destination_hostgroup >= 0")
    comment: str


class PgsqlQueryRulesFastRoutingCreate(BaseModel):
    """Create/update model for `pgsql_query_rules_fast_routing`."""

    username: str
    database: str
    flagIN: Optional[int] = Field(default=0)
    destination_hostgroup: int = Field(description="CHECK: destination_hostgroup >= 0")
    comment: str


class StatsMcpQueryToolsCountersReset(BaseModel):
    """Read model for table `stats_mcp_query_tools_counters_reset`."""
    model_config = ConfigDict(protected_namespaces=())

    endpoint: str
    tool: str
    schema: str
    count: int
    first_seen: int
    last_seen: int
    sum_time: int
    min_time: int
    max_time: int
    PRIMARY: Optional[str] = Field(default=None)


class StatsPgsqlPreparedStatementsInfo(BaseModel):
    """Read model for table `stats_pgsql_prepared_statements_info`."""

    global_stmt_id: int
    database: str
    username: str
    digest: str
    ref_count_client: int
    ref_count_server: int
    num_param_types: int
    query: str


class StatsProxysqlMessageMetricsReset(BaseModel):
    """Read model for table `stats_proxysql_message_metrics_reset`."""

    message_id: str
    filename: str
    line: int = Field(default=0, description="CHECK: line >= 0")
    func: str
    count_star: int
    first_seen: int
    last_seen: int


class RuntimeMysqlGaleraHostgroups(BaseModel):
    """Read model for table `runtime_mysql_galera_hostgroups`."""

    writer_hostgroup: int = Field(description="CHECK: writer_hostgroup>=0")
    backup_writer_hostgroup: int = Field(description="CHECK: backup_writer_hostgroup>=0 AND backup_writer_hostgroup<>writer_hostgroup")
    reader_hostgroup: int = Field(description="CHECK: reader_hostgroup<>writer_hostgroup AND backup_writer_hostgroup<>reader_hostgroup AND reader_hostgroup>0")
    offline_hostgroup: int = Field(description="CHECK: offline_hostgroup<>writer_hostgroup AND offline_hostgroup<>reader_hostgroup AND backup_writer_hostgroup<>offline_hostgroup AND offline_hostgroup>=0")
    active: int = Field(default=1, description="CHECK: active IN (0,1)")
    max_writers: int = Field(default=1, description="CHECK: max_writers >= 0")
    writer_is_also_reader: int = Field(default=0, description="CHECK: writer_is_also_reader IN (0,1,2)")
    max_transactions_behind: int = Field(default=0, description="CHECK: max_transactions_behind>=0")
    comment: Optional[str] = Field(default=None)
    UNIQUE: Optional[str] = Field(default=None)


class StatsProxysqlServersClientsStatus(BaseModel):
    """Read model for table `stats_proxysql_servers_clients_status`."""

    uuid: str
    hostname: str
    port: int
    admin_mysql_ifaces: str
    last_seen_at: int


class RuntimeMysqlServersSslParams(BaseModel):
    """Read model for table `runtime_mysql_servers_ssl_params`."""

    hostname: str
    port: int = Field(default=3306, description="CHECK: port >= 0 AND port <= 65535")
    username: str = Field(default='')
    ssl_ca: str = Field(default='')
    ssl_cert: str = Field(default='')
    ssl_key: str = Field(default='')
    ssl_capath: str = Field(default='')
    ssl_crl: str = Field(default='')
    ssl_crlpath: str = Field(default='')
    ssl_cipher: str = Field(default='')
    tls_version: str = Field(default='')
    comment: str = Field(default='')


class MysqlGroupReplicationHostgroups(BaseModel):
    """Read model for table `mysql_group_replication_hostgroups`."""

    writer_hostgroup: int = Field(description="CHECK: writer_hostgroup>=0")
    backup_writer_hostgroup: int = Field(description="CHECK: backup_writer_hostgroup>=0 AND backup_writer_hostgroup<>writer_hostgroup")
    reader_hostgroup: int = Field(description="CHECK: reader_hostgroup<>writer_hostgroup AND backup_writer_hostgroup<>reader_hostgroup AND reader_hostgroup>0")
    offline_hostgroup: int = Field(description="CHECK: offline_hostgroup<>writer_hostgroup AND offline_hostgroup<>reader_hostgroup AND backup_writer_hostgroup<>offline_hostgroup AND offline_hostgroup>=0")
    active: int = Field(default=1, description="CHECK: active IN (0,1)")
    max_writers: int = Field(default=1, description="CHECK: max_writers >= 0")
    writer_is_also_reader: int = Field(default=0, description="CHECK: writer_is_also_reader IN (0,1,2)")
    max_transactions_behind: int = Field(default=0, description="CHECK: max_transactions_behind>=0")
    comment: Optional[str] = Field(default=None)
    UNIQUE: Optional[str] = Field(default=None)


class MysqlGroupReplicationHostgroupsCreate(BaseModel):
    """Create/update model for `mysql_group_replication_hostgroups`."""

    writer_hostgroup: int = Field(description="CHECK: writer_hostgroup>=0")
    backup_writer_hostgroup: int = Field(description="CHECK: backup_writer_hostgroup>=0 AND backup_writer_hostgroup<>writer_hostgroup")
    reader_hostgroup: int = Field(description="CHECK: reader_hostgroup<>writer_hostgroup AND backup_writer_hostgroup<>reader_hostgroup AND reader_hostgroup>0")
    offline_hostgroup: int = Field(description="CHECK: offline_hostgroup<>writer_hostgroup AND offline_hostgroup<>reader_hostgroup AND backup_writer_hostgroup<>offline_hostgroup AND offline_hostgroup>=0")
    active: Optional[int] = Field(default=1, description="CHECK: active IN (0,1)")
    max_writers: Optional[int] = Field(default=1, description="CHECK: max_writers >= 0")
    writer_is_also_reader: Optional[int] = Field(default=0, description="CHECK: writer_is_also_reader IN (0,1,2)")
    max_transactions_behind: Optional[int] = Field(default=0, description="CHECK: max_transactions_behind>=0")
    comment: Optional[str] = Field(default=None)
    UNIQUE: Optional[str] = Field(default=None)


class RuntimeMysqlHostgroupAttributes(BaseModel):
    """Read model for table `runtime_mysql_hostgroup_attributes`."""

    hostgroup_id: int
    max_num_online_servers: int = Field(default=1000000, description="CHECK: max_num_online_servers>=0 AND max_num_online_servers <= 1000000")
    autocommit: int = Field(default=-1, description="CHECK: autocommit IN (-1, 0, 1)")
    free_connections_pct: int = Field(default=10, description="CHECK: free_connections_pct >= 0 AND free_connections_pct <= 100")
    init_connect: str = Field(default='')
    multiplex: int = Field(default=1, description="CHECK: multiplex IN (0, 1)")
    connection_warming: int = Field(default=0, description="CHECK: connection_warming IN (0, 1)")
    throttle_connections_per_sec: int = Field(default=1000000, description="CHECK: throttle_connections_per_sec >= 1 AND throttle_connections_per_sec <= 1000000")
    ignore_session_variables: str = Field(default='', description="CHECK: JSON_VALID(ignore_session_variables) OR ignore_session_variables = ''")
    hostgroup_settings: str = Field(default='', description="CHECK: JSON_VALID(hostgroup_settings) OR hostgroup_settings = ''")
    servers_defaults: str = Field(default='', description="CHECK: JSON_VALID(servers_defaults) OR servers_defaults = ''")
    comment: str = Field(default='')


class RuntimePgsqlHostgroupAttributes(BaseModel):
    """Read model for table `runtime_pgsql_hostgroup_attributes`."""

    hostgroup_id: int
    max_num_online_servers: int = Field(default=1000000, description="CHECK: max_num_online_servers>=0 AND max_num_online_servers <= 1000000")
    autocommit: int = Field(default=-1, description="CHECK: autocommit IN (-1, 0, 1)")
    free_connections_pct: int = Field(default=10, description="CHECK: free_connections_pct >= 0 AND free_connections_pct <= 100")
    init_connect: str = Field(default='')
    multiplex: int = Field(default=1, description="CHECK: multiplex IN (0, 1)")
    connection_warming: int = Field(default=0, description="CHECK: connection_warming IN (0, 1)")
    throttle_connections_per_sec: int = Field(default=1000000, description="CHECK: throttle_connections_per_sec >= 1 AND throttle_connections_per_sec <= 1000000")
    ignore_session_variables: str = Field(default='', description="CHECK: JSON_VALID(ignore_session_variables) OR ignore_session_variables = ''")
    hostgroup_settings: str = Field(default='', description="CHECK: JSON_VALID(hostgroup_settings) OR hostgroup_settings = ''")
    servers_defaults: str = Field(default='', description="CHECK: JSON_VALID(servers_defaults) OR servers_defaults = ''")
    comment: str = Field(default='')


class RuntimeMysqlAwsAuroraHostgroups(BaseModel):
    """Read model for table `runtime_mysql_aws_aurora_hostgroups`."""

    writer_hostgroup: int = Field(description="CHECK: writer_hostgroup>=0")
    reader_hostgroup: int = Field(description="CHECK: reader_hostgroup<>writer_hostgroup AND reader_hostgroup>0")
    active: int = Field(default=1, description="CHECK: active IN (0,1)")
    aurora_port: int = Field(default=3306)
    domain_name: str = Field(description="CHECK: SUBSTR(domain_name,1,1) = '.'")
    max_lag_ms: int = Field(default=600000, description="CHECK: max_lag_ms>= 10 AND max_lag_ms <= 600000")
    check_interval_ms: int = Field(default=1000, description="CHECK: check_interval_ms >= 100 AND check_interval_ms <= 600000")
    check_timeout_ms: int = Field(default=800, description="CHECK: check_timeout_ms >= 80 AND check_timeout_ms <= 3000")
    writer_is_also_reader: int = Field(default=0, description="CHECK: writer_is_also_reader IN (0,1)")
    new_reader_weight: int = Field(default=1, description="CHECK: new_reader_weight >= 0 AND new_reader_weight <=10000000")
    add_lag_ms: int = Field(default=30, description="CHECK: add_lag_ms >= 0 AND add_lag_ms <= 600000")
    min_lag_ms: int = Field(default=30, description="CHECK: min_lag_ms >= 0 AND min_lag_ms <= 600000")
    lag_num_checks: int = Field(default=1, description="CHECK: lag_num_checks >= 1 AND lag_num_checks <= 16")
    comment: Optional[str] = Field(default=None)
    UNIQUE: Optional[str] = Field(default=None)


class RuntimeMysqlReplicationHostgroups(BaseModel):
    """Read model for table `runtime_mysql_replication_hostgroups`."""

    writer_hostgroup: int = Field(description="CHECK: writer_hostgroup>=0")
    reader_hostgroup: int = Field(description="CHECK: reader_hostgroup<>writer_hostgroup AND reader_hostgroup>=0")
    check_type: str = Field(default='read_only', description="CHECK: LOWER(check_type) IN ('read_only','innodb_read_only','super_read_only','read_only|innodb_read_only','read_only&innodb_read_only')")
    comment: str = Field(default='')
    UNIQUE: Optional[str] = Field(default=None)


class RuntimePgsqlReplicationHostgroups(BaseModel):
    """Read model for table `runtime_pgsql_replication_hostgroups`."""

    writer_hostgroup: int = Field(description="CHECK: writer_hostgroup>=0")
    reader_hostgroup: int = Field(description="CHECK: reader_hostgroup<>writer_hostgroup AND reader_hostgroup>=0")
    check_type: str = Field(default='read_only', description="CHECK: LOWER(check_type) IN ('read_only')")
    comment: str = Field(default='')
    UNIQUE: Optional[str] = Field(default=None)


class StatsMysqlPreparedStatementsInfo(BaseModel):
    """Read model for table `stats_mysql_prepared_statements_info`."""

    global_stmt_id: int
    schemaname: str
    username: str
    digest: str
    ref_count_client: int
    ref_count_server: int
    num_columns: int
    num_params: int
    query: str


class RuntimeMysqlFirewallWhitelistRules(BaseModel):
    """Read model for table `runtime_mysql_firewall_whitelist_rules`."""

    active: int = Field(default=1, description="CHECK: active IN (0,1)")
    username: str
    client_address: str
    schemaname: str
    flagIN: int = Field(default=0)
    digest: str
    comment: str


class RuntimeMysqlFirewallWhitelistUsers(BaseModel):
    """Read model for table `runtime_mysql_firewall_whitelist_users`."""

    active: int = Field(default=1, description="CHECK: active IN (0,1)")
    username: str
    client_address: str
    mode: RuntimeMysqlFirewallWhitelistUsers_mode_enum = Field(default="('OFF", description="CHECK: mode IN ('OFF','DETECTING','PROTECTING')")
    comment: str


class RuntimeMysqlQueryRulesFastRouting(BaseModel):
    """Read model for table `runtime_mysql_query_rules_fast_routing`."""

    username: str
    schemaname: str
    flagIN: int = Field(default=0)
    destination_hostgroup: int = Field(description="CHECK: destination_hostgroup >= 0")
    comment: str


class RuntimePgsqlFirewallWhitelistRules(BaseModel):
    """Read model for table `runtime_pgsql_firewall_whitelist_rules`."""

    active: int = Field(default=1, description="CHECK: active IN (0,1)")
    username: str
    client_address: str
    database: str
    flagIN: int = Field(default=0)
    digest: str
    comment: str


class RuntimePgsqlFirewallWhitelistUsers(BaseModel):
    """Read model for table `runtime_pgsql_firewall_whitelist_users`."""

    active: int = Field(default=1, description="CHECK: active IN (0,1)")
    username: str
    client_address: str
    mode: RuntimePgsqlFirewallWhitelistUsers_mode_enum = Field(default="('OFF", description="CHECK: mode IN ('OFF','DETECTING','PROTECTING')")
    comment: str


class RuntimePgsqlQueryRulesFastRouting(BaseModel):
    """Read model for table `runtime_pgsql_query_rules_fast_routing`."""

    username: str
    database: str
    flagIN: int = Field(default=0)
    destination_hostgroup: int = Field(description="CHECK: destination_hostgroup >= 0")
    comment: str


class MysqlFirewallWhitelistSqliFingerprints(BaseModel):
    """Read model for table `mysql_firewall_whitelist_sqli_fingerprints`."""

    active: int = Field(default=1, description="CHECK: active IN (0,1)")
    fingerprint: str


class MysqlFirewallWhitelistSqliFingerprintsCreate(BaseModel):
    """Create/update model for `mysql_firewall_whitelist_sqli_fingerprints`."""

    active: Optional[int] = Field(default=1, description="CHECK: active IN (0,1)")
    fingerprint: str


class PgsqlFirewallWhitelistSqliFingerprints(BaseModel):
    """Read model for table `pgsql_firewall_whitelist_sqli_fingerprints`."""

    active: int = Field(default=1, description="CHECK: active IN (0,1)")
    fingerprint: str


class PgsqlFirewallWhitelistSqliFingerprintsCreate(BaseModel):
    """Create/update model for `pgsql_firewall_whitelist_sqli_fingerprints`."""

    active: Optional[int] = Field(default=1, description="CHECK: active IN (0,1)")
    fingerprint: str


class RuntimeMysqlGroupReplicationHostgroups(BaseModel):
    """Read model for table `runtime_mysql_group_replication_hostgroups`."""

    writer_hostgroup: int = Field(description="CHECK: writer_hostgroup>=0")
    backup_writer_hostgroup: int = Field(description="CHECK: backup_writer_hostgroup>=0 AND backup_writer_hostgroup<>writer_hostgroup")
    reader_hostgroup: int = Field(description="CHECK: reader_hostgroup<>writer_hostgroup AND backup_writer_hostgroup<>reader_hostgroup AND reader_hostgroup>0")
    offline_hostgroup: int = Field(description="CHECK: offline_hostgroup<>writer_hostgroup AND offline_hostgroup<>reader_hostgroup AND backup_writer_hostgroup<>offline_hostgroup AND offline_hostgroup>=0")
    active: int = Field(default=1, description="CHECK: active IN (0,1)")
    max_writers: int = Field(default=1, description="CHECK: max_writers >= 0")
    writer_is_also_reader: int = Field(default=0, description="CHECK: writer_is_also_reader IN (0,1,2)")
    max_transactions_behind: int = Field(default=0, description="CHECK: max_transactions_behind>=0")
    comment: Optional[str] = Field(default=None)
    UNIQUE: Optional[str] = Field(default=None)


class RuntimeMysqlFirewallWhitelistSqliFingerprints(BaseModel):
    """Read model for table `runtime_mysql_firewall_whitelist_sqli_fingerprints`."""

    active: int = Field(default=1, description="CHECK: active IN (0,1)")
    fingerprint: str


class RuntimePgsqlFirewallWhitelistSqliFingerprints(BaseModel):
    """Read model for table `runtime_pgsql_firewall_whitelist_sqli_fingerprints`."""

    active: int = Field(default=1, description="CHECK: active IN (0,1)")
    fingerprint: str
