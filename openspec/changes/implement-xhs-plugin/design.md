# Design: Implement Xiaohongshu Plugin (MOD_01_XHS)

## Context

SoulGravity Enterprise has a working scaffold with `BasePlatformAdapter` ABC, `PluginManager`, Celery workers, and an API gateway. The Xiaohongshu adapter exists as a mock stub. This design details how to replace stubs with real implementations and wire up the full pipeline.

## Goals / Non-Goals

**Goals:**
- Replace mock `XiaohongshuAdapter` methods with real HTTP interactions.
- Define Pydantic V2 schemas for XHS-specific data structures.
- Expose a FastAPI router for configuration CRUD, connection testing, scrape triggering.
- Wire Celery tasks to invoke the adapter with real keyword scraping and publish logic.
- Encrypt cookies at rest (Fernet) and check cookie health proactively.

**Non-Goals:**
- Browser-based scraping (Playwright). Phase 1 uses direct HTTP API calls.
- Image / video generation. Only upload of pre-existing assets.
- Full publishing queue UI. Phase 1 uses a simple trigger endpoint.
- Analytics dashboard. `get_analytics` remains a stub for now.

## Decisions

### 1. HTTP Client Strategy
Use `curl_cffi.requests.AsyncSession` for all XHS API calls to bypass TLS fingerprinting.
Arguments: `(impersonate="chrome110")`.

**Rationale:** Standard `httpx` is blocked by XHS WAF (461/462). `curl_cffi` mimics a real Chrome browser's TLS handshake.

### 2. Configuration Model
A new Pydantic `XhsConfig` model in `plugins/platforms/xiaohongshu/config.py`:

```python
class XhsConfig(BaseModel):
    cookie: str            # Encrypted via Fernet before DB storage
    user_agent: str = "..."
    proxy_url: str | None = None
    proxy_type: Literal["sticky", "random"] = "sticky"
    version: int = 1
```

Stored in a new `platform_configs` table (generic, keyed by `tenant_id + platform_name`).

### 3. Anti-Detect Measures
- Random sleep 2-5s between requests via `asyncio.sleep(uniform(2, 5))`.
- Rotate `User-Agent` per session from a curated pool.
- Proxy support via `httpx` proxy parameter.
- Rate limit: max 5 concurrent keyword scrapes per tenant (via `asyncio.Semaphore`).

### 4. Cookie Health & Alerting
`check_cookie_health()` calls the user profile API. If it returns 403 or empty user data:
1. Mark config as `status=disconnected` in DB.
2. Fire a webhook alert (generic `AlertService.send(event_type="cookie_expired", ...)`).
3. Pause all scheduled tasks for that tenant+platform.

### 5. Error Handling & Retry
Publishing uses the existing `libs/core_kernel/resiliency/retry.py` decorator:
- Max 3 retries with exponential backoff (base=2s, max=30s).
- Dead-letter callback logs to `scraped_notes` table with `status=failed`.

### 6. File Structure

```
plugins/platforms/xiaohongshu/
├── __init__.py          # (existing)
├── adapter.py           # (MODIFY) Real XHS API implementation
├── config.py            # (NEW) XhsConfig Pydantic model
├── schemas.py           # (NEW) ScrapedNote, PublishRequest, SearchParams
├── signing.py           # (NEW) XS/XT header signing utility
└── constants.py         # (NEW) API endpoints, default UA pool

apps/api-gateway/routers/
└── xhs.py               # (NEW) FastAPI router for XHS endpoints
```

## Risks / Trade-offs

| Risk | Mitigation |
| :--- | :--- |
| XHS API changes or blocks requests | Signing algorithm is isolated in `signing.py` — easy to update. Circuit breaker will auto-pause on repeated failures. |
| Cookie lifetime is short (~24h) | Health check runs on every task invocation. Webhook alerts on expiration. |
| Rate limiting / anti-bot detection | Random delays, proxy rotation, and per-tenant semaphore limit (5 concurrent). |
| Fernet key management | Use `FERNET_KEY` env var. Document rotation procedure. |
