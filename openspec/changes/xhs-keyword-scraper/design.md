## Context
Building the end-to-end XHS keyword search & scrape pipeline. The existing adapter has `fetch_hot_trends`; we're adding a richer `search_notes` method alongside a new persistence layer, Celery task, API endpoints, and frontend console.

## Goals / Non-Goals
**Goals:**
- Persist scraped notes to Postgres via `XhsNote` SQLModel
- Deduplicate using `ON CONFLICT (note_id) DO UPDATE`
- Expose search/browse via FastAPI endpoints
- Build a glassmorphism frontend console with Masonry grid
- Support sort: general, time_descending, popularity_descending

**Non-Goals:**
- Full-text search within note content (future)
- Note detail view / click-through (future)
- Automatic scheduled scraping (future, requires cron integration)

## Decisions

### 1. Model: SQLAlchemy Table (not SQLModel)
The project uses `sqlalchemy.ext.asyncio` with raw `AsyncSession`. Using a plain SQLAlchemy `Table` or declarative model keeps consistency with the DB session pattern in `libs/infra_db/session.py`. However, since user spec says SQLModel, we'll use SQLModel which is compatible with SQLAlchemy.

### 2. `search_notes` vs modifying `fetch_hot_trends`
Adding a new method instead of changing the existing one. `fetch_hot_trends` returns `TrendItem` (the interface contract); `search_notes` returns raw dicts with richer fields (desc, cover_url, collects, user_id). No breaking changes.

### 3. Sync Celery Task with `asyncio.run`
Following the existing `scrape.py` pattern: define an inner `async def run()`, execute via `asyncio.run()`. The DB session is async (`asyncpg`), so the upsert logic lives inside the async context.

### 4. Upsert via `sqlalchemy.dialects.postgresql.insert`
Using `insert().on_conflict_do_update()` for atomic dedup. This is the Postgres-native approach and avoids race conditions in concurrent tasks.

### 5. Frontend Polling
After triggering `/scrape`, poll `/notes?keyword=X` every 3s for up to 30s. Simple and effective for MVP — no WebSocket needed yet.

### 6. Image `referrerPolicy`
All `<img>` tags rendering XHS cover URLs must use `referrerPolicy="no-referrer"` to prevent CDN 403s.

## Component Architecture
```
User → XhsScraperConsole → POST /api/v1/xhs/scrape → Celery Task
                                                         ↓
                         GET /api/v1/xhs/notes ← XhsNote (Postgres)
                              ↓
                         Masonry Grid (cover + title + stats)
```

## Risks / Trade-offs
- **Anti-spider**: Adapter may hit WAF (461/462). Task should catch and report gracefully.
- **No credentials**: The scrape endpoint needs XHS cookies configured. If no config exists, task fails fast with a clear error.
- **Image CDN**: `no-referrer` works today but XHS may change their policy. Fallback: proxy images through our backend.
