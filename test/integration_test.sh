#!/bin/bash
# Integration tests: spin up each ProxySQL version, seed fixtures, run checks
# Usage: integration_test.sh [VERSION...]
#        Defaults to all supported versions: 2.7 3.0
set -uo pipefail

TESTDIR="$(cd "$(dirname "$0")" && pwd)"
PROJDIR="$(cd "$TESTDIR/.." && pwd)"
BENCH="$TESTDIR/bench.sh"

if [ $# -eq 0 ]; then
    VERSIONS=(2.7 3.0)
else
    VERSIONS=("$@")
fi
TOTAL_PASS=0
TOTAL_FAIL=0

# ── per-version endpoint lists ─────────────────────────────────────────────
# Tables that must return 200 for each version.
# pgsql_* tables don't exist in 2.7 — proxui should return 200 (empty list),
# not 500, verifying graceful degradation.

common_tables=(
    mysql_servers
    mysql_users
    mysql_query_rules
    global_variables
    proxysql_servers
    scheduler
    mysql_replication_hostgroups
    mysql_group_replication_hostgroups
    mysql_galera_hostgroups
)

common_runtime=(
    runtime_mysql_servers
    runtime_mysql_users
    runtime_global_variables
    runtime_mysql_query_rules
)

common_stats=(
    stats_mysql_global
    stats_mysql_connection_pool
    stats_mysql_commands_counters
    stats_mysql_processlist
    stats_mysql_query_rules
    stats_memory_metrics
)

v30_tables=(
    pgsql_servers
    pgsql_users
    pgsql_query_rules
    pgsql_replication_hostgroups
)

v30_runtime=(
    runtime_pgsql_servers
    runtime_pgsql_users
    runtime_pgsql_query_rules
)

v30_stats=(
    stats_pgsql_global
    stats_pgsql_connection_pool
    stats_pgsql_processlist
)

# ── helpers ────────────────────────────────────────────────────────────────

PASS=0
FAIL=0
COOKIE_JAR=""

check() {
    local desc="$1" url="$2" expect="${3:-200}"
    local code
    code=$(curl -s -o /dev/null -w '%{http_code}' -b "$COOKIE_JAR" "$url")
    if [ "$code" = "$expect" ]; then
        echo "  ✓ $desc"
        ((PASS++))
    else
        echo "  ✗ $desc (expected $expect, got $code)"
        ((FAIL++))
    fi
}

wait_proxui() {
    local url="$1"
    printf "  Waiting for proxui"
    for i in $(seq 1 30); do
        code=$(curl -s -o /dev/null -w '%{http_code}' "$url/api/v1/health" 2>/dev/null || echo 000)
        [ "$code" = "200" ] && echo " ready" && return 0
        printf '.'; sleep 1
    done
    echo " TIMEOUT"
    return 1
}

run_version() {
    local version="$1"
    local API="http://127.0.0.1:8080/api/v1"
    local PROXUI_PID="" COOKIE_JAR=""
    PASS=0
    FAIL=0

    cleanup() {
        [ -n "$PROXUI_PID" ] && kill "$PROXUI_PID" 2>/dev/null || true
        [ -n "$COOKIE_JAR" ] && rm -f "$COOKIE_JAR"
        "$BENCH" down 2>/dev/null || true
    }
    trap cleanup RETURN

    echo ""
    echo "══════════════════════════════════════════"
    echo "  ProxySQL $version"
    echo "══════════════════════════════════════════"

    # Bring up bench for this version
    echo "── Starting bench ──"
    "$BENCH" up "$version" || { echo "FATAL: bench up failed"; return 1; }

    # Start proxui on host
    echo "── Starting proxui ──"
    cd "$PROJDIR"
    PROXYSQL_ADMIN_HOST=127.0.0.1 \
    PROXYSQL_ADMIN_PORT=16032 \
    PROXYSQL_ADMIN_USER=radmin \
    PROXYSQL_ADMIN_PASS=radmin \
    .venv/bin/uvicorn generated.app:app --host 127.0.0.1 --port 8080 \
        --log-level warning &
    PROXUI_PID=$!

    wait_proxui "http://127.0.0.1:8080" || { echo "FATAL: proxui failed to start"; return 1; }

    # Login
    COOKIE_JAR=$(mktemp)
    code=$(curl -s -o /dev/null -w '%{http_code}' -c "$COOKIE_JAR" \
        -X POST "$API/auth/login" \
        -H 'Content-Type: application/json' \
        -d '{"username": "radmin", "password": "radmin"}')
    if [ "$code" = "200" ]; then
        echo "  ✓ Login"
        ((PASS++))
    else
        echo "  ✗ Login failed ($code) — cannot continue"
        ((FAIL++))
        return
    fi

    # Common tables (both versions)
    echo "── MySQL config tables ──"
    for t in "${common_tables[@]}"; do check "$t" "$API/$t"; done

    echo "── MySQL runtime tables ──"
    for t in "${common_runtime[@]}"; do check "$t" "$API/$t"; done

    echo "── MySQL stats tables ──"
    for t in "${common_stats[@]}"; do check "$t" "$API/$t"; done

    # v3.0-only tables — on 2.7 these should return 200 (empty), not 500
    case "$version" in
        3.0*)
            echo "── PgSQL tables (v3.0) ──"
            for t in "${v30_tables[@]}"; do check "$t" "$API/$t"; done
            echo "── PgSQL runtime (v3.0) ──"
            for t in "${v30_runtime[@]}"; do check "$t" "$API/$t"; done
            echo "── PgSQL stats (v3.0) ──"
            for t in "${v30_stats[@]}"; do check "$t" "$API/$t"; done
            ;;
        2.7*)
            echo "── PgSQL tables (graceful degradation on 2.7) ──"
            for t in "${v30_tables[@]}"; do check "$t (→ empty on 2.7)" "$API/$t"; done
            ;;
    esac

    # CRUD on mysql_servers
    echo "── CRUD: mysql_servers ──"
    code=$(curl -s -o /dev/null -w '%{http_code}' -b "$COOKIE_JAR" \
        -X POST "$API/mysql_servers" \
        -H 'Content-Type: application/json' \
        -d '{"hostgroup_id": 99, "hostname": "integ-test-host", "port": 3306}')
    [ "$code" = "200" ] && { echo "  ✓ POST create"; ((PASS++)); } \
                        || { echo "  ✗ POST create (got $code)"; ((FAIL++)); }

    check "GET by PK" "$API/mysql_servers/99/integ-test-host/3306"

    code=$(curl -s -o /dev/null -w '%{http_code}' -b "$COOKIE_JAR" \
        -X DELETE "$API/mysql_servers/99/integ-test-host/3306")
    [ "$code" = "200" ] && { echo "  ✓ DELETE"; ((PASS++)); } \
                        || { echo "  ✗ DELETE (got $code)"; ((FAIL++)); }

    check "GET after DELETE → 404" "$API/mysql_servers/99/integ-test-host/3306" 404

    # Verify fixture data landed
    echo "── Fixture data verification ──"
    body=$(curl -s -b "$COOKIE_JAR" "$API/mysql_servers")
    count=$(echo "$body" | python3 -c "import sys,json; print(len(json.load(sys.stdin)))" 2>/dev/null || echo 0)
    if [ "$count" -ge 2 ]; then
        echo "  ✓ mysql_servers has $count rows (fixtures loaded)"
        ((PASS++))
    else
        echo "  ✗ mysql_servers has $count rows (expected ≥2 from fixtures)"
        ((FAIL++))
    fi

    body=$(curl -s -b "$COOKIE_JAR" "$API/mysql_query_rules")
    count=$(echo "$body" | python3 -c "import sys,json; print(len(json.load(sys.stdin)))" 2>/dev/null || echo 0)
    if [ "$count" -ge 3 ]; then
        echo "  ✓ mysql_query_rules has $count rows"
        ((PASS++))
    else
        echo "  ✗ mysql_query_rules has $count rows (expected ≥3 from fixtures)"
        ((FAIL++))
    fi

    # Auth: logout
    code=$(curl -s -o /dev/null -w '%{http_code}' -b "$COOKIE_JAR" \
        -X POST "$API/auth/logout")
    [ "$code" = "200" ] && { echo "  ✓ Logout"; ((PASS++)); } \
                        || { echo "  ✗ Logout (got $code)"; ((FAIL++)); }

    echo ""
    echo "  ProxySQL $version: $PASS passed, $FAIL failed"
    TOTAL_PASS=$((TOTAL_PASS + PASS))
    TOTAL_FAIL=$((TOTAL_FAIL + FAIL))
}

# ── main ───────────────────────────────────────────────────────────────────

# Build proxui once
cd "$PROJDIR"
if [ ! -f .venv/bin/uvicorn ]; then
    echo "Setting up venv..."
    just deps >/dev/null
fi

for version in "${VERSIONS[@]}"; do
    run_version "$version"
    sleep 2
done

echo ""
echo "══════════════════════════════════════════"
echo "  Total: $TOTAL_PASS passed, $TOTAL_FAIL failed"
echo "══════════════════════════════════════════"
[ "$TOTAL_FAIL" -eq 0 ] && exit 0 || exit 1
