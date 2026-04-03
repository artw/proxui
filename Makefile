VENV     := .venv
PYTHON   := $(VENV)/bin/python
PIP      := $(VENV)/bin/pip
UVICORN  := $(VENV)/bin/uvicorn

HOST     ?= 127.0.0.1
PORT     ?= 8080

# ProxySQL admin connection (override for production)
PROXYSQL_ADMIN_HOST ?= 127.0.0.1
PROXYSQL_ADMIN_PORT ?= 16032
PROXYSQL_ADMIN_USER ?= radmin
PROXYSQL_ADMIN_PASS ?= radmin

export PROXYSQL_ADMIN_HOST PROXYSQL_ADMIN_PORT PROXYSQL_ADMIN_USER PROXYSQL_ADMIN_PASS

# Header path for codegen (from proxysql source tree)
PROXYSQL_SRC ?= $(HOME)/src/proxysql
HEADER       ?= $(PROXYSQL_SRC)/include/ProxySQL_Admin_Tables_Definitions.h
OUTDIR       ?= generated

.PHONY: all venv deps generate run dev clean help test-up test-down test-logs test-status test-run

all: venv deps generate  ## Set up everything (venv + deps + codegen)
	@echo ""
	@echo "proxui ready. Cheatsheet:"
	@echo "  make test-up      Start MySQL + ProxySQL containers"
	@echo "  make run          Start proxui on $(HOST):$(PORT)"
	@echo "  make dev          Start with auto-reload"
	@echo "  make test-down    Tear down containers"
	@echo "  make test-status  Show container status"
	@echo "  make test-logs    Tail ProxySQL logs"
	@echo "  make test-run     All-in-one: build + bench + server"
	@echo "  make generate     Regenerate models from C header"
	@echo "  make clean        Remove venv and pycache"
	@echo "  bash test/smoke_test.sh  Run 20-point API smoke test"
	@echo ""

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  %-14s %s\n", $$1, $$2}'

$(VENV)/bin/activate:
	python3 -m venv $(VENV)

venv: $(VENV)/bin/activate  ## Create virtualenv

deps: venv $(VENV)/.deps  ## Install dependencies
$(VENV)/.deps: requirements.txt $(VENV)/bin/activate
	$(PIP) install -r requirements.txt
	@touch $@

generate: deps  ## (Re)generate models from ProxySQL header
	$(PYTHON) gen_fastapi_models.py --header $(HEADER) --outdir $(OUTDIR)

run: deps  ## Run the server
	$(UVICORN) generated.app:app --host $(HOST) --port $(PORT)

dev: deps  ## Run with auto-reload
	$(UVICORN) generated.app:app --host $(HOST) --port $(PORT) --reload

# ── Test bench ───────────────────────────────────────────────────────────

test-up:      ## Start ProxySQL + MySQL test bench
	test/bench.sh up

test-down:    ## Stop test bench (all containers)
	test/bench.sh down

test-logs:    ## Tail proxui container logs
	test/bench.sh logs

test-status:  ## Show test bench container status
	test/bench.sh status

test-run: all test-up  ## Build + start bench + run proxui in container
	test/bench.sh run

clean:  ## Remove venv and pycache
	rm -rf $(VENV) $(OUTDIR)/__pycache__ $(OUTDIR)/*.pyc
