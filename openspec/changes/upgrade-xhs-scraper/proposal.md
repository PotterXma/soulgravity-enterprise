## Why

The XHS Scraper Console currently dumps all search results in a flat, unpaginated grid. This causes three problems:
1. **Performance** — Rendering hundreds of notes at once lags the browser.
2. **Data Depth** — Search results only contain title/cover/metrics. The full note content (`desc`, `images_list`) is never fetched, blocking downstream AI content-generation pipelines.
3. **UX** — Users cannot inspect a note's full detail (images, description, engagement) without leaving the dashboard.

## What Changes

- **Backend API** — `GET /notes` gains proper pagination (`page`, `page_size`) and returns `{ items, total, page }`. A new `POST /enrich/{note_id}` endpoint fetches and persists the full note content.
- **Adapter** — New `get_note_detail(note_id)` method on `XiaohongshuAdapter` that calls XHS feed API, returns full `desc` + `images_list`, and updates the DB row.
- **Model** — `XhsNote` gains an `images_list` (JSON text) column to store the full image gallery.
- **Frontend Console** — Paginated grid (20 per page) with Ant Design `<Pagination />`. Clicking a card opens a `NoteDetailDrawer` showing full images, description, stats, and a "Fetch Full Content" button.

## Capabilities

### New Capabilities
- `note-detail-enrichment`: Fetching and persisting full note content (desc + images) from XHS feed API, exposed via `POST /enrich/{note_id}`.
- `note-detail-drawer`: Frontend drawer component for viewing full note details with image gallery, content, stats, and enrichment trigger.

### Modified Capabilities
- `xhs-scraper`: Adding pagination to `GET /notes` API and paginated grid display in the frontend console.

## Impact

- **Backend**: `routers/xhs.py` (modified), `adapter.py` (new method), `models.py` (new column), `xhs_tasks.py` (no change)
- **Frontend**: `XhsScraperConsole.tsx` (modified), new `NoteDetailDrawer.tsx`
- **DB**: Requires Alembic migration for `images_list` column on `xhs_note` table
- **Dependencies**: No new deps — uses existing `curl_cffi`, `antd Drawer`, `antd Pagination`
