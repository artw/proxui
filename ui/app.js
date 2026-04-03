// proxui — Alpine.js application
const API = '/api/v1';

// ── Table descriptions & doc URLs ──────────────────────────────────────
const TABLE_INFO = {
  mysql_servers:                     { desc: 'Backend MySQL server pool',               doc: '/documentation/backend-server-configuration' },
  mysql_servers_ssl_params:          { desc: 'Per-server SSL/TLS settings',             doc: '/documentation/ssl-support' },
  mysql_users:                       { desc: 'Frontend MySQL user accounts',            doc: '/documentation/users-management/mysql-users-management' },
  mysql_query_rules:                 { desc: 'Query routing & rewrite rules',           doc: '/documentation/main-runtime/mysql-tables' },
  mysql_query_rules_fast_routing:    { desc: 'Fast-path routing by user/schema/flags',  doc: '/documentation/main-runtime/mysql-tables' },
  mysql_replication_hostgroups:      { desc: 'Read/write split via replication lag',     doc: '/documentation/main-runtime/mysql-tables' },
  mysql_group_replication_hostgroups:{ desc: 'Group replication hostgroup mapping',      doc: '/documentation/group-replication-configuration' },
  mysql_galera_hostgroups:           { desc: 'Galera cluster hostgroup mapping',         doc: '/documentation/galera-configuration' },
  mysql_aws_aurora_hostgroups:       { desc: 'AWS Aurora cluster hostgroup mapping',     doc: '/documentation/aws-aurora-configuration' },
  mysql_hostgroup_attributes:        { desc: 'Per-hostgroup settings & limits',          doc: '/documentation/main-runtime/mysql-tables' },
  mysql_collations:                  { desc: 'MySQL collation/charset mapping',          doc: null },
  mysql_firewall_whitelist_rules:    { desc: 'Firewall allow-list rules',               doc: '/documentation/firewall-whitelist' },
  mysql_firewall_whitelist_users:    { desc: 'Firewall per-user allow-list',             doc: '/documentation/firewall-whitelist' },
  mysql_firewall_whitelist_sqli_fingerprints: { desc: 'SQL injection fingerprint allow-list', doc: '/documentation/sql-injection-engine' },
  pgsql_servers:                     { desc: 'Backend PostgreSQL server pool',           doc: '/documentation/main-runtime/postgresql-tables' },
  pgsql_users:                       { desc: 'Frontend PostgreSQL user accounts',        doc: '/documentation/users-management/postgresql-users-management' },
  pgsql_query_rules:                 { desc: 'PostgreSQL query routing rules',           doc: '/documentation/main-runtime/postgresql-tables' },
  pgsql_query_rules_fast_routing:    { desc: 'PostgreSQL fast-path routing',             doc: '/documentation/main-runtime/postgresql-tables' },
  pgsql_replication_hostgroups:      { desc: 'PostgreSQL replication hostgroup mapping', doc: '/documentation/main-runtime/postgresql-tables' },
  pgsql_hostgroup_attributes:        { desc: 'Per-hostgroup settings (PostgreSQL)',      doc: '/documentation/main-runtime/postgresql-tables' },
  pgsql_ldap_mapping:                { desc: 'LDAP to hostgroup mapping',                doc: '/documentation/main-runtime/postgresql-tables' },
  pgsql_firewall_whitelist_rules:    { desc: 'PostgreSQL firewall allow-list rules',     doc: '/documentation/firewall-whitelist' },
  pgsql_firewall_whitelist_users:    { desc: 'PostgreSQL firewall per-user allow-list',  doc: '/documentation/firewall-whitelist' },
  pgsql_firewall_whitelist_sqli_fingerprints: { desc: 'PostgreSQL SQL injection fingerprint allow-list', doc: '/documentation/sql-injection-engine' },
  global_variables:                  { desc: 'All admin/mysql/pgsql runtime variables',  doc: '/documentation/global-variables' },
  scheduler:                         { desc: 'Scheduled tasks (external scripts)',        doc: '/documentation/scheduler' },
  restapi_routes:                    { desc: 'REST API endpoint definitions',            doc: '/documentation/rest-api' },
  proxysql_servers:                  { desc: 'ProxySQL cluster peer list',               doc: '/documentation/proxysql-cluster' },
  coredump_filters:                  { desc: 'Debug core dump trigger filters',          doc: null },
  runtime_mysql_servers:             { desc: 'Active backend servers (live)',             doc: null },
  runtime_mysql_users:               { desc: 'Active user accounts (live)',              doc: null },
  runtime_mysql_query_rules:         { desc: 'Active query rules (live)',                doc: null },
  runtime_global_variables:          { desc: 'Active global variables (live)',            doc: null },
  runtime_proxysql_servers:          { desc: 'Active cluster peers (live)',               doc: null },
  runtime_scheduler:                 { desc: 'Active scheduled tasks (live)',             doc: null },
  runtime_checksums_values:          { desc: 'Config checksums per module',              doc: null },
  stats_mysql_global:                { desc: 'Global counters (uptime, connections…)',    doc: '/documentation/the-admin-schemas/stats-statistics' },
  stats_mysql_connection_pool:       { desc: 'Per-server connection pool stats',          doc: '/documentation/the-admin-schemas/stats-statistics' },
  stats_mysql_connection_pool_reset: { desc: 'Connection pool stats (reset on read)',     doc: null },
  stats_mysql_commands_counters:     { desc: 'Per-command execution counts & latency',    doc: '/documentation/the-admin-schemas/stats-statistics' },
  stats_mysql_query_rules:           { desc: 'Per-rule hit count',                        doc: '/documentation/the-admin-schemas/stats-statistics' },
  stats_mysql_query_digest:          { desc: 'Query digest stats (latency, rows…)',       doc: '/documentation/the-admin-schemas/stats-statistics' },
  stats_mysql_query_digest_reset:    { desc: 'Query digest stats (reset on read)',        doc: null },
  stats_mysql_processlist:           { desc: 'Currently running queries',                 doc: '/documentation/the-admin-schemas/stats-statistics' },
  stats_mysql_free_connections:      { desc: 'Idle backend connections',                   doc: null },
  stats_mysql_users:                 { desc: 'Per-user connection counts',                doc: '/documentation/the-admin-schemas/stats-statistics' },
  stats_mysql_errors:                { desc: 'Per-server error counts',                   doc: null },
  stats_mysql_errors_reset:          { desc: 'Error counts (reset on read)',              doc: null },
  stats_mysql_gtid_executed:         { desc: 'GTID tracking per server',                  doc: null },
  stats_mysql_prepared_statements_info: { desc: 'Prepared statement cache info',          doc: null },
  stats_mysql_client_host_cache:     { desc: 'Client host connection cache',              doc: null },
  stats_mysql_client_host_cache_reset: { desc: 'Client host cache (reset on read)',       doc: null },
  stats_mysql_query_events:          { desc: 'Advanced per-query event log',              doc: '/documentation/advanced-event-and-query-logging' },
  stats_memory_metrics:              { desc: 'Memory allocator statistics',                doc: null },
  stats_pgsql_global:                { desc: 'PostgreSQL global counters',                doc: null },
  stats_pgsql_connection_pool:       { desc: 'PostgreSQL per-server pool stats',          doc: null },
  stats_pgsql_commands_counters:     { desc: 'PostgreSQL per-command stats',              doc: null },
  stats_pgsql_query_rules:           { desc: 'PostgreSQL per-rule hit count',             doc: null },
  stats_pgsql_query_digest:          { desc: 'PostgreSQL query digest stats',             doc: null },
  stats_pgsql_processlist:           { desc: 'PostgreSQL running queries',                doc: null },
  stats_pgsql_users:                 { desc: 'PostgreSQL per-user connections',           doc: null },
  stats_pgsql_stat_activity:         { desc: 'PostgreSQL pg_stat_activity view',          doc: null },
  stats_proxysql_servers_checksums:  { desc: 'Cluster config checksum comparison',        doc: null },
  stats_proxysql_servers_metrics:    { desc: 'Cluster peer health metrics',               doc: null },
  stats_proxysql_servers_status:     { desc: 'Cluster peer connection status',            doc: null },
  stats_proxysql_servers_clients_status: { desc: 'Cluster peer client stats',             doc: null },
  stats_proxysql_message_metrics:    { desc: 'Cluster message counters',                  doc: null },
  stats_proxysql_message_metrics_reset: { desc: 'Cluster message counters (reset)',       doc: null },
};

const DOC_BASE = 'https://proxysql.com';

function displayName(table) {
  // Strip category prefix and replace underscores with spaces
  const prefixes = [
    'runtime_mysql_', 'runtime_pgsql_', 'runtime_',
    'stats_mysql_', 'stats_pgsql_', 'stats_proxysql_', 'stats_',
    'mysql_', 'pgsql_', 'clickhouse_', 'proxysql_', 'genai_', 'mcp_',
  ];
  let name = table;
  for (const p of prefixes) {
    if (table.startsWith(p) && table.length > p.length) {
      name = table.slice(p.length);
      break;
    }
  }
  return name.replace(/_/g, ' ');
}


function proxui() {
  return {
    // Auth
    authenticated: false,
    authUser: '',
    loginUser: '',
    loginPass: '',
    loginError: '',
    loginLoading: false,

    // View
    view: 'dashboard',  // 'dashboard' | 'tables' | 'query'
    statsRunning: true,

    // Sidebar state
    tables: {},
    categories: [],
    filteredCategories: [],
    search: '',
    activeCategory: 'mysql',

    // Sidebar resize
    sidebarWidth: parseInt(localStorage.getItem('proxui-sidebar') || '260'),
    resizing: false,

    // Overview
    overview: null,

    // Config sync
    configModules: [],
    configGroups: [],
    configLoading: false,
    activeConfigModule: null,
    activeConfigDiff: null,

    // Table view
    currentTable: null,
    tableMeta: null,
    columns: [],
    rows: [],
    loading: false,
    error: '',
    sortCol: '',
    sortAsc: true,
    colFilters: {},
    colFilterOpen: null,
    colFilterStyle: '',
    rowLimit: 50,

    // Form
    showForm: false,
    editMode: false,
    formFields: [],
    formData: {},
    saving: false,

    // Query view
    queryTargets: [],
    queryTarget: 'admin',
    queryRunning: false,
    queryResult: null,
    _cm: null,

    // Schema tree (query sidebar) — shares queryTarget
    schemaTree: {},
    filteredSchemaKeys: [],
    schemaDbs: [],
    queryDb: '',
    _lastSchemaTarget: null,
    _hintWords: [],      // flat list for fuzzy completion
    schemaLoading: false,

    // Stats
    _statsInterval: null,
    _charts: {},
    _statsHistory: { ts: [], clientConn: [], serverConn: [], questions: [], lastQ: null,
                     sqliteMem: [], poolMem: [], cacheMem: [],
                     poolUsed: [], poolFree: [] },
    statsCmds: [],
    statsCmdsLimit: 10,
    statsDigests: [],
    statsDigestsLimit: 10,

    // Dashboard toggles
    showMySQL: JSON.parse(localStorage.getItem('proxui-show-mysql') ?? 'true'),
    showPgSQL: JSON.parse(localStorage.getItem('proxui-show-pgsql') ?? 'true'),
    showClickHouse: JSON.parse(localStorage.getItem('proxui-show-clickhouse') ?? 'true'),

    // Toast & theme
    toast: '',
    darkMode: true,

    async init() {
      this.darkMode = document.documentElement.getAttribute('data-theme') === 'dark';

      // Check auth
      try {
        const res = await fetch(`${API}/auth/check`);
        if (res.ok) {
          const data = await res.json();
          if (data.authenticated) {
            this.authenticated = true;
            this.authUser = data.user;
            await this._initApp();
          }
        }
      } catch (e) {}
    },

    async login() {
      this.loginError = '';
      this.loginLoading = true;
      try {
        const res = await fetch(`${API}/auth/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username: this.loginUser, password: this.loginPass }),
        });
        const data = await res.json();
        if (res.ok && data.ok) {
          this.authenticated = true;
          this.authUser = data.user;
          this.loginPass = '';
          await this._initApp();
        } else {
          this.loginError = data.error || 'Login failed';
        }
      } catch (e) {
        this.loginError = 'Connection error';
      } finally {
        this.loginLoading = false;
      }
    },

    async logout() {
      try { await fetch(`${API}/auth/logout`, { method: 'POST' }); } catch (e) {}
      this.authenticated = false;
      this.authUser = '';
      this.tables = {};
      this.categories = [];
      this.configModules = [];
      this.configGroups = [];
      this.stopStats();
    },

    async _initApp() {
      // Restore from URL hash: #view or #view/table
      this._restoreHash();

      // Load table metadata
      try {
        const res = await fetch(`${API}/tables`);
        this.tables = await res.json();
        this.buildCategories();
        this.filterTables();

        let config = 0, runtime = 0, stats = 0;
        for (const [name, meta] of Object.entries(this.tables)) {
          if (name.startsWith('stats_')) stats++;
          else if (name.startsWith('runtime_')) runtime++;
          else if (!meta.readonly) config++;
          else stats++;
        }
        this.overview = { config, runtime, stats };
      } catch (e) {
        console.error('Failed to load table metadata:', e);
      }

      // Load query targets
      try {
        const res = await fetch(`${API}/targets`);
        this.queryTargets = await res.json();
        if (this.queryTargets.length > 0) this.queryTarget = this.queryTargets[0].id;
      } catch (e) {
        this.queryTargets = [{ id: 'admin', label: 'ProxySQL Admin' }];
      }

      // Load config sync status
      this.loadConfigStatus();

      // Start stats polling
      this.startStats();
    },

    async loadConfigStatus() {
      this.configLoading = true;
      try {
        const res = await fetch(`${API}/config/status`);
        this.configModules = await res.json();
        this.buildConfigGroups();
      } catch (e) {
        this.configModules = [];
        this.configGroups = [];
      } finally {
        this.configLoading = false;
      }
    },

    buildConfigGroups() {
      const groups = {
        'MySQL':  [],
        'PgSQL':  [],
        'ClickHouse': [],
        'Admin':  [],
      };
      for (const m of this.configModules) {
        if (m.module.startsWith('mysql_')) groups['MySQL'].push(m);
        else if (m.module.startsWith('pgsql_')) groups['PgSQL'].push(m);
        else if (m.module.startsWith('clickhouse_')) groups['ClickHouse'].push(m);
        else groups['Admin'].push(m);
      }
      this.configGroups = Object.entries(groups)
        .filter(([, mods]) => mods.length > 0)
        .map(([label, modules]) => ({ label, modules }));
    },

    configShortName(module) {
      return module
        .replace(/^mysql_/, '').replace(/^pgsql_/, '')
        .replace(/^clickhouse_/, '').replace(/^admin_/, '')
        .replace(/_/g, ' ');
    },

    get activeConfigStatus() {
      if (!this.activeConfigModule) return null;
      return this.configModules.find(m => m.module === this.activeConfigModule);
    },

    async selectConfigModule(module) {
      if (this.activeConfigModule === module) {
        this.activeConfigModule = null;
        this.activeConfigDiff = null;
        return;
      }
      this.activeConfigModule = module;
      this.activeConfigDiff = null;
      try {
        const res = await fetch(`${API}/config/diff/${encodeURIComponent(module)}`);
        this.activeConfigDiff = await res.json();
      } catch (e) {
        this.activeConfigDiff = { columns: [], diff_rows: [] };
      }
    },

    async configAction(module, action) {
      try {
        const res = await fetch(`${API}/config/action`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ module, action }),
        });
        const data = await res.json();
        if (data.ok) {
          this.showToast(`${data.command}`);
          await this.loadConfigStatus();
          if (this.activeConfigModule === module) {
            await this.selectConfigModule(module);
          }
          if (this.currentTable) await this.loadRows();
        } else {
          this.showToast('Error: ' + data.error);
        }
      } catch (e) {
        this.showToast('Error: ' + e.message);
      }
    },

    _restoreHash() {
      const hash = location.hash.slice(1);
      if (!hash) return;
      const [view, table] = hash.split('/');
      if (['dashboard', 'tables', 'query'].includes(view)) {
        this.view = view;
        if (view === 'tables' && table) {
          this.$nextTick(() => this.selectTable(decodeURIComponent(table)));
        }
      }
    },

    _updateHash() {
      let hash = this.view;
      if (this.view === 'tables' && this.currentTable) {
        hash += '/' + encodeURIComponent(this.currentTable);
      }
      history.replaceState(null, '', '#' + hash);
    },

    setView(v) {
      this.view = v;
      this._updateHash();
      if (v === 'dashboard' && this._statsHistory.ts.length > 0) {
        // Re-render charts from accumulated data
        this.$nextTick(() => this.pollStats());
      }
      if (v === 'query') {
        this.$nextTick(() => {
          this.initCodeMirror();
          if (this._lastSchemaTarget !== this.queryTarget) {
            this.loadDatabases();
            this.loadSchemaTree();
          }
        });
      }
    },

    onTargetChange() {
      this.queryDb = '';
      this.loadDatabases();
      this.loadSchemaTree();
    },

    async loadDatabases() {
      try {
        const res = await fetch(`${API}/databases/${encodeURIComponent(this.queryTarget)}`);
        const data = await res.json();
        this.schemaDbs = Array.isArray(data) ? data : [];
        if (this.schemaDbs.length === 1) {
          this.queryDb = this.schemaDbs[0];
        }
      } catch (e) {
        this.schemaDbs = [];
      }
    },

    // ── Categories / sidebar ────────────────────────────────────────────

    buildCategories() {
      const cats = {};
      for (const name of Object.keys(this.tables)) {
        const cat = this.categorize(name);
        if (!cats[cat]) cats[cat] = [];
        cats[cat].push(name);
      }
      for (const c of Object.values(cats)) c.sort();

      const order = [
        'mysql', 'pgsql', 'clickhouse', 'genai', 'mcp',
        'config', 'proxysql', 'runtime', 'stats', 'other'
      ];
      this.categories = order
        .filter(k => cats[k])
        .map(k => ({ name: k, label: this.catLabel(k), tables: cats[k] }));
    },

    categorize(name) {
      const meta = this.tables[name];
      if (name.startsWith('stats_')) return 'stats';
      if (name.startsWith('runtime_')) return 'runtime';
      if (!meta.readonly) {
        for (const pfx of ['mysql_', 'pgsql_', 'clickhouse_', 'proxysql_', 'genai_', 'mcp_']) {
          if (name.startsWith(pfx)) return pfx.replace('_', '');
        }
        return 'config';
      }
      return 'other';
    },

    catLabel(cat) {
      return {
        config: 'Config', mysql: 'MySQL', pgsql: 'PostgreSQL',
        clickhouse: 'ClickHouse', genai: 'GenAI', mcp: 'MCP',
        proxysql: 'ProxySQL', runtime: 'Runtime', stats: 'Stats', other: 'Other',
      }[cat] || cat;
    },

    _fuzzyMatch(text, query) {
      // Every char in query must appear in text, in order
      let qi = 0;
      const tl = text.toLowerCase();
      for (let i = 0; i < tl.length && qi < query.length; i++) {
        if (tl[i] === query[qi]) qi++;
      }
      return qi === query.length;
    },

    filterTables() {
      const q = this.search.toLowerCase();
      if (!q) { this.filteredCategories = this.categories; return; }
      this.filteredCategories = this.categories
        .map(cat => ({
          ...cat,
          tables: cat.tables.filter(t =>
            this._fuzzyMatch(t, q) ||
            this._fuzzyMatch(TABLE_INFO[t]?.desc || '', q)
          ),
        }))
        .filter(cat => cat.tables.length > 0);
    },

    displayName(t) { return displayName(t); },

    openColFilter(col, event) {
      if (this.colFilterOpen === col) { this.colFilterOpen = null; return; }
      const rect = event.target.getBoundingClientRect();
      this.colFilterStyle = `top:${rect.bottom + 4}px; left:${rect.left - 20}px;`;
      this.colFilterOpen = col;
      this.$nextTick(() => {
        if (this.$refs.colFilterInput) this.$refs.colFilterInput.focus();
      });
    },

    isPasswordCol(col) {
      const c = col.toLowerCase();
      return c.includes('password') || c.includes('passwd') || c.includes('secret');
    },

    targetIconSrc(targetId) {
      const t = this.queryTargets.find(t => t.id === targetId);
      const type = t?.type;
      if (type === 'mysql') return '/icons/mysql.svg';
      if (type === 'postgresql') return '/icons/postgresql.svg';
      return null;
    },

    targetIconClass(targetId) {
      const t = this.queryTargets.find(t => t.id === targetId);
      return t?.type === 'proxysql' ? 'ph-lightning' : 'ph-hard-drives';
    },
    tableDesc(t) { return TABLE_INFO[t]?.desc || ''; },
    docUrl(t) {
      const info = TABLE_INFO[t];
      return info?.doc ? DOC_BASE + info.doc : null;
    },

    // ── Sidebar resize ──────────────────────────────────────────────────

    startResize(e) {
      this.resizing = true;
      document.body.classList.add('resizing');
      const startX = e.clientX;
      const startW = this.sidebarWidth;
      const onMove = (ev) => {
        this.sidebarWidth = Math.min(450, Math.max(180, startW + ev.clientX - startX));
      };
      const onUp = () => {
        this.resizing = false;
        document.body.classList.remove('resizing');
        localStorage.setItem('proxui-sidebar', String(this.sidebarWidth));
        document.removeEventListener('mousemove', onMove);
        document.removeEventListener('mouseup', onUp);
      };
      document.addEventListener('mousemove', onMove);
      document.addEventListener('mouseup', onUp);
    },

    // ── Table view ──────────────────────────────────────────────────────

    goToTable(name) {
      this.view = 'tables';
      this._updateHash();
      this.$nextTick(() => this.selectTable(name));
    },

    async selectTable(name) {
      this.currentTable = name;
      this.tableMeta = this.tables[name];
      this.columns = this.tableMeta.columns.map(c => c.name);
      this.error = '';
      this.showForm = false;
      this.sortCol = '';
      this.sortAsc = true;
      this.colFilters = {};
      this.colFilterOpen = null;
      for (const cat of this.categories) {
        if (cat.tables.includes(name)) { this.activeCategory = cat.name; break; }
      }
      this._updateHash();
      await this.loadRows();
    },

    async loadRows() {
      this.loading = true;
      this.error = '';
      try {
        const res = await fetch(`${API}/${this.currentTable}`);
        if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
        this.rows = await res.json();
      } catch (e) {
        this.error = e.message;
        this.rows = [];
      } finally {
        this.loading = false;
      }
    },

    sortBy(col) {
      if (this.sortCol === col) this.sortAsc = !this.sortAsc;
      else { this.sortCol = col; this.sortAsc = true; }
    },

    get filteredRows() {
      let rows = this.rows;
      for (const [col, q] of Object.entries(this.colFilters)) {
        if (!q) continue;
        const ql = q.toLowerCase();
        rows = rows.filter(r => String(r[col] ?? '').toLowerCase().includes(ql));
      }
      return rows;
    },

    get sortedRows() {
      let rows = this.filteredRows;
      if (this.sortCol) {
        const col = this.sortCol, dir = this.sortAsc ? 1 : -1;
        rows = [...rows].sort((a, b) => {
          const va = a[col] ?? '', vb = b[col] ?? '';
          if (typeof va === 'number' && typeof vb === 'number') return (va - vb) * dir;
          return String(va).localeCompare(String(vb)) * dir;
        });
      }
      return this.rowLimit ? rows.slice(0, this.rowLimit) : rows;
    },

    // ── CRUD forms ──────────────────────────────────────────────────────

    openCreateForm() {
      this.editMode = false;
      this.formFields = this.buildFormFields(false);
      this.formData = {};
      for (const f of this.formFields) {
        this.formData[f.name] = (f.default !== null && f.default !== undefined) ? f.default : '';
      }
      this.showForm = true;
    },

    openEditForm(row) {
      this.editMode = true;
      this.formFields = this.buildFormFields(true);
      this.formData = { ...row };
      this.showForm = true;
    },

    buildFormFields(isEdit) {
      return this.tableMeta.columns
        .filter(c => !(!isEdit && c.autoincrement))
        .map(c => ({
          name: c.name,
          type: this.fieldType(c.type),
          nullable: c.nullable,
          default: c.default,
          pk: this.tableMeta.pk_columns.includes(c.name),
          autoincrement: c.autoincrement,
        }));
    },

    fieldType(sqlType) {
      const t = (sqlType || '').toUpperCase();
      if (['INT', 'INTEGER', 'BIGINT'].some(x => t.includes(x))) return 'int';
      if (['DOUBLE', 'FLOAT', 'REAL'].some(x => t.includes(x))) return 'float';
      return 'text';
    },

    async saveRow() {
      this.saving = true;
      try {
        const payload = {};
        for (const f of this.formFields) {
          let val = this.formData[f.name];
          if (val === '' && f.nullable) val = null;
          else if (val === '' && f.default !== null) continue;
          else if (f.type === 'int') { val = parseInt(val, 10); if (isNaN(val)) val = 0; }
          else if (f.type === 'float') { val = parseFloat(val); if (isNaN(val)) val = 0; }
          payload[f.name] = val;
        }
        const method = this.editMode ? 'PUT' : 'POST';
        let url = `${API}/${this.currentTable}`;
        if (this.editMode) {
          url += '/' + this.tableMeta.pk_columns.map(pk => encodeURIComponent(this.formData[pk])).join('/');
        }
        const res = await fetch(url, {
          method, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload),
        });
        if (!res.ok) {
          const err = await res.json().catch(() => ({ detail: res.statusText }));
          throw new Error(err.detail || JSON.stringify(err));
        }
        this.showForm = false;
        this.showToast(this.editMode ? 'Row updated' : 'Row created');
        await this.loadRows();
        this.loadConfigStatus();
      } catch (e) {
        this.showToast('Error: ' + e.message);
      } finally {
        this.saving = false;
      }
    },

    async deleteRow(row) {
      if (!confirm('Delete this row?')) return;
      try {
        const pkParts = this.tableMeta.pk_columns.map(pk => encodeURIComponent(row[pk]));
        const res = await fetch(`${API}/${this.currentTable}/${pkParts.join('/')}`, { method: 'DELETE' });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        this.showToast('Row deleted');
        await this.loadRows();
        this.loadConfigStatus();
      } catch (e) {
        this.showToast('Error: ' + e.message);
      }
    },

    // ── Query view ──────────────────────────────────────────────────────

    initCodeMirror() {
      if (this._cm) return;
      const el = document.getElementById('query-editor');
      if (!el) return;

      const self = this;

      // Fuzzy hint function
      function fuzzyHint(cm) {
        const cur = cm.getCursor();
        const token = cm.getTokenAt(cur);
        let start = token.start;
        let query = token.string;
        // Don't complete inside strings or comments
        if (token.type === 'string' || token.type === 'comment') return;
        // If token starts with punctuation, skip it
        if (/^[`"'(,;]/.test(query)) {
          start += 1;
          query = query.slice(1);
        }
        query = query.toLowerCase();
        if (query.length < 1) return;
        // Fuzzy match: every char in query must appear in order
        const matches = self._hintWords.filter(w => {
          const wl = w.toLowerCase();
          let qi = 0;
          for (let i = 0; i < wl.length && qi < query.length; i++) {
            if (wl[i] === query[qi]) qi++;
          }
          return qi === query.length;
        });
        // Sort: exact prefix first, then by length
        matches.sort((a, b) => {
          const al = a.toLowerCase(), bl = b.toLowerCase();
          const ap = al.startsWith(query) ? 0 : 1;
          const bp = bl.startsWith(query) ? 0 : 1;
          if (ap !== bp) return ap - bp;
          return a.length - b.length;
        });
        if (matches.length === 0) return;
        return {
          list: matches.slice(0, 30),
          from: CodeMirror.Pos(cur.line, start),
          to: CodeMirror.Pos(cur.line, token.end),
        };
      }

      this._cm = CodeMirror(el, {
        value: '-- Type SQL here (Tab to complete)\nSELECT * FROM stats_mysql_global LIMIT 20',
        mode: 'text/x-mysql',
        theme: this.darkMode ? 'material-darker' : 'default',
        lineNumbers: true,
        autofocus: true,
        extraKeys: {
          'Ctrl-Enter': () => this.runQuery(),
          'Cmd-Enter': () => this.runQuery(),
          'Tab': (cm) => {
            const hint = fuzzyHint(cm);
            if (hint && hint.list.length === 1) {
              // Single match: insert directly
              cm.replaceRange(hint.list[0], hint.from, hint.to);
            } else if (hint && hint.list.length > 1) {
              cm.showHint({ hint: fuzzyHint, completeSingle: false });
            } else {
              // Default tab behavior (indent)
              cm.execCommand('defaultTab');
            }
          },
          'Ctrl-Space': (cm) => cm.showHint({ hint: fuzzyHint, completeSingle: false }),
        },
      });
    },

    async runQuery() {
      if (!this._cm) return;
      let sql = this._cm.getSelection() || this._cm.getValue();
      if (!sql.trim()) return;

      this.queryRunning = true;
      this.queryResult = null;
      try {
        const body = { sql, target: this.queryTarget, limit: 1000 };
        if (this.queryDb) body.database = this.queryDb;
        const res = await fetch(`${API}/query`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(body),
        });
        this.queryResult = await res.json();
      } catch (e) {
        this.queryResult = { ok: false, error: e.message };
      } finally {
        this.queryRunning = false;
      }
    },

    // ── Schema tree (query sidebar) ──────────────────────────────────────

    filterSchemaTree() {
      const q = this.search.toLowerCase();
      if (!q) {
        this.filteredSchemaKeys = Object.keys(this.schemaTree).sort();
        return;
      }
      this.filteredSchemaKeys = Object.keys(this.schemaTree).sort().filter(db => {
        if (this._fuzzyMatch(db, q)) return true;
        return Object.keys(this.schemaTree[db]).some(t => this._fuzzyMatch(t, q));
      });
    },

    filteredSchemaTables(db) {
      const q = this.search.toLowerCase();
      const tbls = Object.keys(this.schemaTree[db] || {}).sort();
      if (!q) return tbls;
      if (this._fuzzyMatch(db, q)) return tbls;
      return tbls.filter(t => this._fuzzyMatch(t, q));
    },

    async loadSchemaTree() {
      this.schemaLoading = true;
      this._lastSchemaTarget = this.queryTarget;
      try {
        let schemaUrl = `${API}/schema/${encodeURIComponent(this.queryTarget)}`;
        if (this.queryDb) schemaUrl += `?db=${encodeURIComponent(this.queryDb)}`;
        const res = await fetch(schemaUrl);
        const data = await res.json();
        this.schemaTree = data.error ? {} : data;
        this.filterSchemaTree();
        // Build flat word list for fuzzy completion
        this._hintWords = [];
        const seen = new Set();
        for (const [db, tbls] of Object.entries(this.schemaTree)) {
          if (!seen.has(db)) { this._hintWords.push(db); seen.add(db); }
          for (const [tbl, cols] of Object.entries(tbls)) {
            if (!seen.has(tbl)) { this._hintWords.push(tbl); seen.add(tbl); }
            const qual = `${db}.${tbl}`;
            if (!seen.has(qual)) { this._hintWords.push(qual); seen.add(qual); }
            for (const col of cols) {
              if (!seen.has(col.name)) { this._hintWords.push(col.name); seen.add(col.name); }
            }
          }
        }
      } catch (e) {
        console.error('Failed to load schema:', e);
        this.schemaTree = {};
        this.schemaDbs = [];
      } finally {
        this.schemaLoading = false;
      }
    },

    insertTableRef(db, tbl) {
      if (!this._cm) return;
      const ref = Object.keys(this.schemaTree).length > 1 ? `${db}.${tbl}` : tbl;
      const doc = this._cm.getDoc();
      doc.replaceSelection(ref);
      this._cm.focus();
    },

    insertColRef(col) {
      if (!this._cm) return;
      this._cm.getDoc().replaceSelection(col);
      this._cm.focus();
    },

    // ── Stats dashboard ───────────────────────────────────────────────

    startStats() {
      if (this._statsInterval) return;
      this.statsRunning = true;
      this.pollStats();
      this._statsInterval = setInterval(() => this.pollStats(), 5000);
    },

    stopStats() {
      if (this._statsInterval) {
        clearInterval(this._statsInterval);
        this._statsInterval = null;
      }
      this.statsRunning = false;
    },

    toggleStats() {
      if (this.statsRunning) this.stopStats(); else this.startStats();
    },

    async pollStats() {
      try {
        // Global stats
        const gRes = await fetch(`${API}/query`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ sql: 'SELECT * FROM stats_mysql_global', target: 'admin' }),
        });
        const gData = await gRes.json();
        if (gData.ok) {
          const g = {};
          for (const r of gData.rows) g[r.Variable_Name] = r.Variable_Value;
          const h = this._statsHistory;
          const now = Math.floor(Date.now() / 1000);
          h.ts.push(now);
          h.clientConn.push(+(g.Client_Connections_connected || 0));
          h.serverConn.push(+(g.Server_Connections_connected || 0));
          const q = +(g.Questions || 0);
          if (h.lastQ !== null) {
            h.questions.push(Math.max(0, (q - h.lastQ) / 5));
          } else {
            h.questions.push(0);
          }
          h.lastQ = q;
          h.sqliteMem.push(+(g.SQLite3_memory_bytes || 0) / 1048576);
          h.poolMem.push(+(g.ConnPool_memory_bytes || 0) / 1048576);
          h.cacheMem.push(+(g.Query_Cache_Memory_bytes || 0) / 1048576);

          // Trim to last 120 points (10 min at 5s)
          const max = 120;
          if (h.ts.length > max) {
            for (const k of Object.keys(h)) {
              if (Array.isArray(h[k])) h[k] = h[k].slice(-max);
            }
          }

          if (this.view === 'dashboard') {
          this.renderChart('chart-connections', 'Connections', [
            h.ts,
            h.clientConn,
            h.serverConn,
          ], [
            {},
            { label: 'Client', stroke: '#4dabf7', width: 2 },
            { label: 'Server', stroke: '#69db7c', width: 2 },
          ]);

          this.renderChart('chart-qps', 'QPS', [
            h.ts,
            h.questions,
          ], [
            {},
            { label: 'Queries/s', stroke: '#ffa94d', width: 2, fill: 'rgba(255,169,77,0.1)' },
          ]);

          this.renderChart('chart-memory', 'MB', [
            h.ts,
            h.sqliteMem,
            h.poolMem,
            h.cacheMem,
          ], [
            {},
            { label: 'SQLite', stroke: '#da77f2', width: 2 },
            { label: 'ConnPool', stroke: '#4dabf7', width: 2 },
            { label: 'QCache', stroke: '#69db7c', width: 2 },
          ]);
          } // end if dashboard visible
        }

        // Connection pool
        const pRes = await fetch(`${API}/query`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ sql: 'SELECT * FROM stats_mysql_connection_pool', target: 'admin' }),
        });
        const pData = await pRes.json();
        if (pData.ok) {
          const h = this._statsHistory;
          let used = 0, free = 0;
          for (const r of pData.rows) {
            used += +(r.ConnUsed || 0);
            free += +(r.ConnFree || 0);
          }
          h.poolUsed.push(used);
          h.poolFree.push(free);
          const max = 120;
          if (h.poolUsed.length > max) {
            h.poolUsed = h.poolUsed.slice(-max);
            h.poolFree = h.poolFree.slice(-max);
          }
          if (this.view === 'dashboard') {
            const ts = h.ts.slice(-h.poolUsed.length);
            this.renderChart('chart-pool', 'Conns', [
              ts,
              h.poolUsed,
              h.poolFree,
            ], [
              {},
              { label: 'Used', stroke: '#ff6b6b', width: 2, fill: 'rgba(255,107,107,0.1)' },
              { label: 'Free', stroke: '#69db7c', width: 2, fill: 'rgba(105,219,124,0.1)' },
            ]);
          }
        }

        // Commands
        const cRes = await fetch(`${API}/query`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ sql: 'SELECT * FROM stats_mysql_commands_counters WHERE Total_cnt > 0 ORDER BY Total_cnt DESC LIMIT 100', target: 'admin' }),
        });
        const cData = await cRes.json();
        if (cData.ok) {
          this.statsCmds = cData.rows.map(r => ({
            cmd: r.Command,
            cnt: r.Total_cnt,
            total: (+(r.Total_Time_us || 0) / 1000).toFixed(1) + ' ms',
            avg: r.Total_cnt > 0 ? (+(r.Total_Time_us || 0) / +r.Total_cnt / 1000).toFixed(2) : '0',
          }));
        }

        // Query digests
        const dRes = await fetch(`${API}/query`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ sql: 'SELECT hostgroup,schemaname,digest_text,count_star,sum_time FROM stats_mysql_query_digest ORDER BY count_star DESC LIMIT 100', target: 'admin' }),
        });
        const dData = await dRes.json();
        if (dData.ok) {
          this.statsDigests = dData.rows.map(r => ({
            hg: r.hostgroup,
            schema: r.schemaname,
            text: r.digest_text,
            digest: r.digest_text,
            cnt: r.count_star,
            total: (+(r.sum_time || 0) / 1000).toFixed(1),
            avg: r.count_star > 0 ? (+(r.sum_time || 0) / +r.count_star / 1000).toFixed(2) : '0',
          }));
        }
      } catch (e) {
        console.error('Stats poll error:', e);
      }
    },

    renderChart(elId, yLabel, data, series) {
      const el = document.getElementById(elId);
      if (!el) return;
      const isDark = this.darkMode;
      const w = el.parentElement.clientWidth - 24;  // card padding
      const opts = {
        width: Math.max(200, w),
        height: 180,
        cursor: { show: true },
        select: { show: false },
        legend: { show: true },
        axes: [
          {
            stroke: isDark ? '#888' : '#666',
            grid: { stroke: isDark ? '#333' : '#e0e0e0', width: 1 },
            ticks: { stroke: isDark ? '#444' : '#ccc', width: 1 },
          },
          {
            label: yLabel,
            stroke: isDark ? '#888' : '#666',
            grid: { stroke: isDark ? '#333' : '#e0e0e0', width: 1 },
            ticks: { stroke: isDark ? '#444' : '#ccc', width: 1 },
            size: 50,
          },
        ],
        series,
      };

      if (this._charts[elId]) {
        // Update existing chart
        this._charts[elId].setData(data);
        // Resize if container width changed
        const curW = this._charts[elId].width;
        if (Math.abs(curW - opts.width) > 10) {
          this._charts[elId].setSize({ width: opts.width, height: 180 });
        }
      } else {
        // Create new chart
        el.innerHTML = '';
        this._charts[elId] = new uPlot(opts, data, el);
      }
    },

    // ── Toast & theme ───────────────────────────────────────────────────

    persistDashToggle(key) {
      const lsKey = 'proxui-show-' + key.replace('show', '').toLowerCase();
      localStorage.setItem(lsKey, JSON.stringify(this[key]));
    },

    showToast(msg) {
      this.toast = msg;
      setTimeout(() => { this.toast = ''; }, 3000);
    },

    toggleTheme() {
      this.darkMode = !this.darkMode;
      document.documentElement.setAttribute('data-theme', this.darkMode ? 'dark' : 'light');
      if (this._cm) {
        this._cm.setOption('theme', this.darkMode ? 'material-darker' : 'default');
      }
    },
  };
}
