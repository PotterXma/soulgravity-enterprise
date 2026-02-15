# Fix XHS Scraper Issues

## Goal
Fix 2 bugs discovered during verification of `xhs-keyword-scraper`:
1. **CRITICAL**: `XhsConfig.load(tenant_id=...)` is called in `xhs_tasks.py` but the method doesn't exist on `XhsConfig` (it's a plain Pydantic BaseModel).
2. **Minor**: Unused `from sqlalchemy import text` import in `xhs_tasks.py`.

## What Changes

### [MODIFY] `plugins/platforms/xiaohongshu/config.py`
- Add `@classmethod load(tenant_id)` that reads config from env vars or returns defaults.

### [MODIFY] `apps/worker_scraper/tasks/xhs_tasks.py`
- Remove unused `from sqlalchemy import text` import.

## Capabilities
- `fix-config-load`: Add missing `XhsConfig.load()` class method

## Impact
- Prevents runtime crash when Celery task tries to load XHS config
