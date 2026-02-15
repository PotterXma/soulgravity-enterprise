# Proposal: Implement Xiaohongshu Automation Plugin (MOD_01_XHS)

## Why

Xiaohongshu is the pilot module to validate our Plugin Architecture, Pydantic Schema, Celery task pipeline, and Glassmorphism UI. This is the first concrete business feature that exercises the entire stack end-to-end: from frontend config forms through API gateway to async workers performing real platform interactions. Without a working plugin, the architecture remains theoretical.

## What Changes

- **MODIFY**: `plugins/platforms/xiaohongshu/adapter.py` — Replace `NotImplementedError` stubs with real implementation (cookie login, keyword scraping, note publishing).
- **NEW**:    `plugins/platforms/xiaohongshu/config.py` — Pydantic settings model for plugin configuration (cookie, proxy, user_agent).
- **NEW**:    `plugins/platforms/xiaohongshu/schemas.py` — Pydantic V2 request/response models for scraping results and publish payloads.
- **NEW**:    `apps/api-gateway/routers/xhs.py` — FastAPI router with endpoints for config CRUD, test connection, trigger scrape, trigger publish.
- **MODIFY**: `apps/worker-scraper/tasks/scrape.py` — Wire up XHS adapter for actual keyword scraping with anti-detect delays.
- **MODIFY**: `apps/worker-publisher/tasks/publish.py` — Wire up XHS adapter for note publishing with retry logic.
- **NEW**:    `web-console/src/pages/xhs/` — Frontend pages: Config form (GlassCard), Scrape dashboard, Publish queue.

## Capabilities

### New Capabilities
- `xhs-config`: Account configuration management (Cookie input, proxy settings, connection testing).
- `xhs-scraper`: Keyword-based data scraping with anti-detect measures and periodic scheduling.
- `xhs-publisher`: Note publishing with image/video support, queuing, and retry.

## Impact

- **Backend**: New API endpoints under `/api/xhs/`. Celery task implementations become functional.
- **Frontend**: New pages under `/xhs/` route with Ethereal Nebula styling.
- **Database**: New `xhs_config` and `scraped_notes` tables (via Alembic migration).
- **Security**: Cookie encryption via Fernet. Cookie health monitoring with webhook alerts.
