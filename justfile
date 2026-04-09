venv         := ".venv"
python       := venv + "/bin/python"
uvicorn      := venv + "/bin/uvicorn"
pip          := venv + "/bin/pip"

host         := env("HOST", "127.0.0.1")
port         := env("PORT", "8080")

proxysql_src     := env("PROXYSQL_SRC", env("HOME") + "/src/proxysql")
header           := proxysql_src + "/include/ProxySQL_Admin_Tables_Definitions.h"
outdir           := "generated"

proxysql_version := env("PROXYSQL_VERSION", "3.0")

# list recipes
default:
    @just --list

# ── Setup ─────────────────────────────────────────────────────────────────────

# create venv + install deps + generate code (full setup)
all: deps generate

# create virtualenv
venv:
    python3 -m venv {{venv}}

# install dependencies
deps: venv
    {{pip}} install -q -r requirements.txt

# (re)generate models from ProxySQL header (writes models.py, crud_router.py, table_metadata.py)
# NOTE: app.py and db.py in generated/ contain hand-crafted code — codegen skips them
generate: deps
    {{python}} gen_fastapi_models.py --header {{header}} --outdir {{outdir}} --skip app.py db.py

# ── Run ───────────────────────────────────────────────────────────────────────

# start server
run: deps
    {{uvicorn}} generated.app:app --host {{host}} --port {{port}}

# start server with auto-reload
dev: deps
    {{uvicorn}} generated.app:app --host {{host}} --port {{port}} --reload

# ── Test bench ────────────────────────────────────────────────────────────────

# start MySQL + ProxySQL test bench (PROXYSQL_VERSION=2.7|3.0, default 3.0)
bench-up version=proxysql_version:
    test/bench.sh up {{version}}

# stop test bench
bench-down:
    test/bench.sh down

# show bench container status
bench-status:
    test/bench.sh status

# tail bench logs (defaults to proxui-app)
bench-logs ct="proxui-app":
    test/bench.sh logs {{ct}}

# build proxui image + start it on the test bench network
bench-run: deps
    test/bench.sh run

# ── Tests ─────────────────────────────────────────────────────────────────────

# run smoke test against a live proxui (pass URL as arg, default localhost:8080)
smoke url="http://127.0.0.1:8080":
    bash test/smoke_test.sh {{url}}

# run integration tests against all supported ProxySQL versions (2.7, 3.0)
integ:
    test/integration_test.sh

# run integration tests against a single version
integ-version version:
    test/integration_test.sh {{version}}

# ── Cleanup ───────────────────────────────────────────────────────────────────

# remove venv and generated pyc files
clean:
    rm -rf {{venv}} {{outdir}}/__pycache__ {{outdir}}/*.pyc
