# proxui — TODO

## Open Tasks

### Testing
- [ ] Consider containerized proxui in integration_test.sh for cleaner isolation
      (currently starts proxui on host, requires venv)

### Codegen
- [ ] v2.x schema support: `ProxySQL_Admin.cpp` `#define` macros (different parser needed)

### Known Gaps
- No unit tests for `gen_fastapi_models.py`
- No browser/UI tests
