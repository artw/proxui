-- proxui integration test fixtures — ProxySQL 3.0.x
-- Self-contained: includes ALL rows needed for tests.
-- ProxySQL loads cnf into RUNTIME only; MEMORY starts empty.
-- pgsql_servers/users base rows (HG 0) are seeded by bench.sh before this runs.
-- REPLACE INTO is idempotent.

-- mysql_servers: write HG 0 (primary) + read HG 10
REPLACE INTO mysql_servers
    (hostgroup_id, hostname, port, status, weight, max_connections, comment)
VALUES
    (0,  'proxui-mysql', 3306, 'ONLINE', 1, 100, 'write hostgroup'),
    (10, 'proxui-mysql', 3306, 'ONLINE', 1, 200, 'read hostgroup');

-- mysql_users
REPLACE INTO mysql_users
    (username, password, active, default_hostgroup, max_connections, comment)
VALUES
    ('testuser', 'testpass', 1, 0,  1000, 'primary user'),
    ('readuser', 'readpass', 1, 10,  500, 'read-only user');

-- mysql_query_rules
REPLACE INTO mysql_query_rules
    (rule_id, active, match_pattern, destination_hostgroup, apply, comment)
VALUES
    (1, 1, '^SELECT .* FOR UPDATE$', 0,  1, 'writes to primary'),
    (2, 1, '^SELECT',               10,  1, 'reads to replica'),
    (3, 0, '^INSERT',                0,  1, 'inserts to primary (inactive)');

-- mysql_replication_hostgroups
REPLACE INTO mysql_replication_hostgroups
    (writer_hostgroup, reader_hostgroup, comment)
VALUES
    (0, 10, 'primary/replica split');

-- scheduler
REPLACE INTO scheduler
    (id, active, interval_ms, filename, arg1, comment)
VALUES
    (1, 0, 60000, '/bin/true', '', 'disabled test entry');

-- pgsql_servers: HG 0 (write, seeded by bench.sh) + HG 20 (read)
REPLACE INTO pgsql_servers
    (hostgroup_id, hostname, port, status, weight, max_connections, comment)
VALUES
    (0,  'proxui-pgsql', 5432, 'ONLINE', 1, 100, 'pgsql write hostgroup'),
    (20, 'proxui-pgsql', 5432, 'ONLINE', 1, 100, 'pgsql read hostgroup');

-- pgsql_users
REPLACE INTO pgsql_users
    (username, password, active, default_hostgroup, max_connections, comment)
VALUES
    ('testuser', 'testpass', 1, 0,  1000, 'pgsql primary user'),
    ('readuser', 'readpass', 1, 20,  200, 'pgsql read-only user');

-- pgsql_query_rules
REPLACE INTO pgsql_query_rules
    (rule_id, active, match_pattern, destination_hostgroup, apply, comment)
VALUES
    (1, 1, '^SELECT', 20, 1, 'pgsql reads to read HG');

-- pgsql_replication_hostgroups
REPLACE INTO pgsql_replication_hostgroups
    (writer_hostgroup, reader_hostgroup, comment)
VALUES
    (0, 20, 'pgsql primary/replica split');

LOAD MYSQL SERVERS TO RUNTIME;
LOAD MYSQL USERS TO RUNTIME;
LOAD MYSQL QUERY RULES TO RUNTIME;
LOAD PGSQL SERVERS TO RUNTIME;
LOAD PGSQL USERS TO RUNTIME;
LOAD PGSQL QUERY RULES TO RUNTIME;
SAVE MYSQL SERVERS TO DISK;
SAVE MYSQL USERS TO DISK;
SAVE MYSQL QUERY RULES TO DISK;
SAVE PGSQL SERVERS TO DISK;
SAVE PGSQL USERS TO DISK;
SAVE PGSQL QUERY RULES TO DISK;
