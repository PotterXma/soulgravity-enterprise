# Proposal: XHS Keyword Scraper — End-to-End Search & Scrape

## Goal
Build the complete "Search & Scrape" pipeline for Xiaohongshu: model, adapter upgrade, Celery task with dedup, API endpoints, and a Masonry-grid frontend console.

## Why
The adapter can fetch search results but there's no persistence, no dedup, no API exposure, and no UI. Users need to search keywords, persist notes (without duplicates), and browse results visually.

## Key Technical Decisions

### ON CONFLICT Upsert Strategy
Notes are identified by `note_id` (XHS's unique ID). When the same note appears across searches:
```sql
INSERT INTO xhs_note (...) VALUES (...)
ON CONFLICT (note_id) DO UPDATE SET
  likes = EXCLUDED.likes,
  comments = EXCLUDED.comments,
  collects = EXCLUDED.collects,
  last_scraped_at = EXCLUDED.last_scraped_at,
  keyword_search = EXCLUDED.keyword_search
```
This keeps engagement metrics fresh while preventing row explosion.

### Image Hotlink Protection
XHS CDN verifies `Referer`. All `<img>` tags use `referrerPolicy="no-referrer"` to bypass.

## What Changes

### 1. [NEW] `plugins/platforms/xiaohongshu/models.py`
- `XhsNote` SQLModel table with `note_id` PK, engagement metrics, `tenant_id` FK, `keyword_search` field.

### 2. [MODIFY] `plugins/platforms/xiaohongshu/adapter.py`
- Add `search_notes(keyword, sort, page)` method returning raw dicts (richer than `TrendItem`).
- Sort mapping: `general`, `time_descending`, `popularity_descending`.

### 3. [NEW] `apps/worker_scraper/tasks/xhs_tasks.py`
- `scrape_xhs_keyword_task(tenant_id, keyword, sort_type)` — calls adapter, upserts via `ON CONFLICT`.

### 4. [MODIFY] `apps/api_gateway/routers/xhs.py`
- `POST /scrape` — triggers Celery task.
- `GET /notes` — paginated list with keyword filter, sorted by `last_scraped_at` DESC.

### 5. [NEW] `web-console/src/features/plugins/xiaohongshu/XhsScraperConsole.tsx`
- Glass control bar (keyword input, sort select, scrape button).
- Masonry grid of note cards with cover image, title, stats.

## Capabilities
- `xhs-search-scrape`: Keyword search → persist → browse pipeline

## Impact
- **Backend**: New model, new task, expanded router
- **Frontend**: New XhsScraperConsole component
- **Database**: New `xhs_note` table
