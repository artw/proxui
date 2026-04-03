#!/bin/bash
# Quick smoke test: hit the API and check responses
set -uo pipefail

BASE="${1:-http://127.0.0.1:8080}"
API="${BASE}/api/v1"
PASS=0
FAIL=0

# Login and capture session cookie
COOKIE_JAR=$(mktemp)
trap "rm -f $COOKIE_JAR" EXIT

login_code=$(curl -s -o /dev/null -w '%{http_code}' -c "$COOKIE_JAR" \
    -X POST "$API/auth/login" \
    -H 'Content-Type: application/json' \
    -d '{"username": "radmin", "password": "radmin"}')

if [ "$login_code" = "200" ]; then
    echo "  ✓ Login (radmin)"
    ((PASS++))
else
    echo "  ✗ Login failed ($login_code) — cannot continue"
    exit 1
fi

check() {
    local desc="$1" url="$2" expect="${3:-200}"
    local code
    code=$(curl -s -o /dev/null -w '%{http_code}' -b "$COOKIE_JAR" "$url")
    if [ "$code" = "$expect" ]; then
        echo "  ✓ $desc ($code)"
        ((PASS++))
    else
        echo "  ✗ $desc (got $code, expected $expect)"
        ((FAIL++))
    fi
}

echo "Smoke testing $API ..."
echo

echo "── Health ──"
check "health" "$API/health"

echo "── Auth ──"
auth_code=$(curl -s -o /dev/null -w '%{http_code}' -b "$COOKIE_JAR" "$API/auth/check")
if [ "$auth_code" = "200" ]; then
    echo "  ✓ Auth check ($auth_code)"
    ((PASS++))
else
    echo "  ✗ Auth check (got $auth_code)"
    ((FAIL++))
fi

echo "── Config tables (GET) ──"
check "mysql_servers"           "$API/mysql_servers"
check "mysql_users"             "$API/mysql_users"
check "mysql_query_rules"       "$API/mysql_query_rules"
check "global_variables"        "$API/global_variables"
check "proxysql_servers"        "$API/proxysql_servers"
check "scheduler"               "$API/scheduler"

echo "── Runtime tables (GET) ──"
check "runtime_mysql_servers"   "$API/runtime_mysql_servers"
check "runtime_mysql_users"     "$API/runtime_mysql_users"
check "runtime_global_variables" "$API/runtime_global_variables"

echo "── Stats tables (GET) ──"
check "stats_mysql_global"          "$API/stats_mysql_global"
check "stats_mysql_connection_pool" "$API/stats_mysql_connection_pool"
check "stats_mysql_commands_counters" "$API/stats_mysql_commands_counters"
check "stats_mysql_processlist"     "$API/stats_mysql_processlist"
check "stats_mysql_query_rules"     "$API/stats_mysql_query_rules"
check "stats_memory_metrics"        "$API/stats_memory_metrics"

echo "── Unauthenticated → 401 ──"
unauth_code=$(curl -s -o /dev/null -w '%{http_code}' "$API/mysql_servers")
if [ "$unauth_code" = "401" ]; then
    echo "  ✓ No cookie → 401 ($unauth_code)"
    ((PASS++))
else
    echo "  ✗ No cookie should be 401 (got $unauth_code)"
    ((FAIL++))
fi

echo "── CRUD: mysql_servers ──"
# Create
code=$(curl -s -o /dev/null -w '%{http_code}' -b "$COOKIE_JAR" -X POST "$API/mysql_servers" \
    -H 'Content-Type: application/json' \
    -d '{"hostgroup_id": 99, "hostname": "smoke-test-host", "port": 3306}')
if [ "$code" = "200" ]; then
    echo "  ✓ POST create ($code)"
    ((PASS++))
else
    echo "  ✗ POST create (got $code)"
    ((FAIL++))
fi

# Read back
check "GET by PK" "$API/mysql_servers/99/smoke-test-host/3306"

# Delete
code=$(curl -s -o /dev/null -w '%{http_code}' -b "$COOKIE_JAR" -X DELETE "$API/mysql_servers/99/smoke-test-host/3306")
if [ "$code" = "200" ]; then
    echo "  ✓ DELETE ($code)"
    ((PASS++))
else
    echo "  ✗ DELETE (got $code)"
    ((FAIL++))
fi

# Confirm gone
check "GET after delete → 404" "$API/mysql_servers/99/smoke-test-host/3306" 404

echo
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
