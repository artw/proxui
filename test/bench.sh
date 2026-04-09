#!/bin/bash
# proxui test bench — MySQL + PostgreSQL + ProxySQL + proxui in podman
# Usage: bench.sh {up [VERSION]|run|down|logs [ct]|status}
#        VERSION: 2.7 or 3.0 (default 3.0)
#        env PROXYSQL_VERSION overrides default; arg overrides env
set -euo pipefail

# Use host-exec if inside distrobox
if [ -n "${DISTROBOX_ENTER_PATH:-}" ]; then
    PODMAN="distrobox-host-exec podman"
else
    PODMAN="podman"
fi

NETWORK="proxui-test"
MYSQL_CT="proxui-mysql"
PGSQL_CT="proxui-pgsql"
PROXY_CT="proxui-proxysql"
APP_CT="proxui-app"
CONFDIR="$(cd "$(dirname "$0")" && pwd)"
PROJDIR="$(cd "$CONFDIR/.." && pwd)"

up() {
    local version="${1:-${PROXYSQL_VERSION:-3.0}}"
    local fixture_dir="$CONFDIR/fixtures/v${version}"

    # Map version shorthand to exact Docker Hub image tag and feature flags.
    # Update the image tag when a new latest patch is published.
    local image has_pgsql
    case "$version" in
        2.7) image="docker.io/proxysql/proxysql:2.7.3"; has_pgsql=0 ;;
        3.0) image="docker.io/proxysql/proxysql:3.0";   has_pgsql=1 ;;
        *) echo "Unsupported version: $version (supported: 2.7, 3.0)"; exit 1 ;;
    esac

    echo "Starting ProxySQL $version bench (pgsql: $( [ "$has_pgsql" = 1 ] && echo yes || echo no ))"

    $PODMAN network exists "$NETWORK" 2>/dev/null || $PODMAN network create "$NETWORK"

    # ── MySQL backend ──
    if ! $PODMAN container exists "$MYSQL_CT" 2>/dev/null; then
        $PODMAN run -d --name "$MYSQL_CT" --network "$NETWORK" \
            -e MYSQL_ROOT_PASSWORD=testroot \
            -e MYSQL_DATABASE=testdb \
            -e MYSQL_USER=testuser \
            -e MYSQL_PASSWORD=testpass \
            -p 13306:3306 \
            docker.io/mysql:8.4
    else
        $PODMAN start "$MYSQL_CT" 2>/dev/null || true
    fi

    printf "Waiting for MySQL"
    for i in $(seq 1 60); do
        $PODMAN exec "$MYSQL_CT" mysqladmin ping -utestuser -ptestpass >/dev/null 2>&1 && break
        printf '.'; sleep 1
    done
    echo " ready"

    # ── PostgreSQL backend (3.0 only) ──
    if [ "$has_pgsql" = 1 ]; then
        if ! $PODMAN container exists "$PGSQL_CT" 2>/dev/null; then
            $PODMAN run -d --name "$PGSQL_CT" --network "$NETWORK" \
                -e POSTGRES_DB=testdb \
                -e POSTGRES_USER=testuser \
                -e POSTGRES_PASSWORD=testpass \
                -p 15432:5432 \
                docker.io/postgres:17
        else
            $PODMAN start "$PGSQL_CT" 2>/dev/null || true
        fi

        printf "Waiting for PostgreSQL"
        for i in $(seq 1 30); do
            $PODMAN exec "$PGSQL_CT" pg_isready -U testuser -d testdb >/dev/null 2>&1 && break
            printf '.'; sleep 1
        done
        echo " ready"

        $PODMAN exec "$PGSQL_CT" psql -U testuser -d testdb -c "
            CREATE TABLE IF NOT EXISTS sample_data (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                value DOUBLE PRECISION DEFAULT 0,
                created_at TIMESTAMP DEFAULT NOW()
            );
            INSERT INTO sample_data (name, value) VALUES
                ('alpha', 1.1), ('beta', 2.2), ('gamma', 3.3)
            ON CONFLICT DO NOTHING;
        " >/dev/null 2>&1 || true
    fi

    # ── ProxySQL ──
    if ! $PODMAN container exists "$PROXY_CT" 2>/dev/null; then
        $PODMAN run -d --name "$PROXY_CT" --network "$NETWORK" \
            -v "$CONFDIR/proxysql.cnf:/etc/proxysql.cnf:ro" \
            -p 16032:6032 \
            -p 16033:6033 \
            -p 16070:6070 \
            "$image"
    else
        $PODMAN start "$PROXY_CT" 2>/dev/null || true
    fi

    # admin:admin is the bootstrap credential (always valid, set in cnf)
    printf "Waiting for ProxySQL"
    for i in $(seq 1 60); do
        $PODMAN exec "$PROXY_CT" \
            mysql -h127.0.0.1 -P6032 -uadmin -padmin -e "SELECT 1" >/dev/null 2>&1 && break
        printf '.'; sleep 1
    done
    echo " ready"

    # ── Ensure admin credentials are active at runtime ──
    # ProxySQL may not apply cnf admin_credentials without an explicit LOAD.
    # Use admin:admin (bootstrap) to set radmin:radmin and load to runtime.
    $PODMAN exec "$PROXY_CT" mysql -h127.0.0.1 -P6032 -uadmin -padmin -e "
        SET admin-admin_credentials='admin:admin;radmin:radmin';
        LOAD ADMIN VARIABLES TO RUNTIME;
        SAVE ADMIN VARIABLES TO DISK;
    "

    # ── Seed pgsql backends (3.0 only) ──
    if [ "$has_pgsql" = 1 ]; then
        $PODMAN exec "$PROXY_CT" mysql -h127.0.0.1 -P6032 -uadmin -padmin -e "
            REPLACE INTO pgsql_servers (hostgroup_id, hostname, port) VALUES (0, 'proxui-pgsql', 5432);
            REPLACE INTO pgsql_users (username, password, default_hostgroup) VALUES ('testuser', 'testpass', 0);
            LOAD PGSQL SERVERS TO RUNTIME;
            LOAD PGSQL USERS TO RUNTIME;
            SAVE PGSQL SERVERS TO DISK;
            SAVE PGSQL USERS TO DISK;
        "
    fi

    # ── Seed fixtures ──
    if [ -f "$fixture_dir/seed.sql" ]; then
        echo "Seeding fixtures from $fixture_dir/seed.sql ..."
        $PODMAN exec -i "$PROXY_CT" mysql -h127.0.0.1 -P6032 -uadmin -padmin \
            < "$fixture_dir/seed.sql"
    fi

    echo ""
    echo "ProxySQL $version admin: localhost:16032  (radmin/radmin)"
    echo "MySQL backend:           localhost:13306  (testuser/testpass)"
    [ "$has_pgsql" = 1 ] && \
    echo "PostgreSQL backend:      localhost:15432  (testuser/testpass)"
    true
}

run() {
    echo "Building proxui image..."
    $PODMAN build --format docker -f "$PROJDIR/Containerfile" -t proxui:dev "$PROJDIR"

    $PODMAN rm -f "$APP_CT" 2>/dev/null || true

    echo "Starting proxui..."
    $PODMAN run -d --name "$APP_CT" --network "$NETWORK" \
        -e PROXYSQL_ADMIN_HOST=proxui-proxysql \
        -e PROXYSQL_ADMIN_PORT=6032 \
        -e PROXYSQL_ADMIN_USER=radmin \
        -e PROXYSQL_ADMIN_PASS=radmin \
        -p 8080:8080 \
        proxui:dev

    printf "Waiting for proxui"
    for i in $(seq 1 15); do
        $PODMAN healthcheck run "$APP_CT" >/dev/null 2>&1 && break
        printf '.'; sleep 1
    done
    echo " ready"

    echo ""
    echo "proxui UI:   http://localhost:8080"
    echo "proxui API:  http://localhost:8080/api/docs"
}

down() {
    $PODMAN rm -f "$APP_CT" "$PROXY_CT" "$PGSQL_CT" "$MYSQL_CT" 2>/dev/null || true
    $PODMAN network rm "$NETWORK" 2>/dev/null || true
    echo "Test bench stopped"
}

logs() {
    $PODMAN logs -f "${1:-$APP_CT}"
}

status() {
    $PODMAN ps -a --filter name=proxui --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
}

case "${1:-up}" in
    up)     up "${2:-}" ;;
    run)    run ;;
    down)   down ;;
    logs)   logs "${2:-}" ;;
    status) status ;;
    *)      echo "Usage: $0 {up [VERSION]|run|down|logs [container]|status}"; exit 1 ;;
esac
