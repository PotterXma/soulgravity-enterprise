## ADDED Requirements

### Requirement: XhsNote Model
A SQLModel table to persist scraped Xiaohongshu notes with deduplication support.

#### Scenario: Schema
- **GIVEN** the `xhs_note` table
- **THEN** `note_id` (str) is the primary key (XHS's unique note ID)
- **THEN** `title` (str), `desc` (text), `cover_url` (str) store note content
- **THEN** `likes` (int), `comments` (int), `collects` (int) store engagement metrics
- **THEN** `user_nickname` (str), `user_id` (str) store author info
- **THEN** `keyword_search` (str) stores the search keyword used
- **THEN** `tenant_id` (str, indexed) scopes data per tenant
- **THEN** `last_scraped_at` (datetime) tracks when the note was last fetched

#### Scenario: Upsert Deduplication
- **WHEN** a note with the same `note_id` already exists
- **THEN** `INSERT ... ON CONFLICT (note_id) DO UPDATE SET` updates `likes`, `comments`, `collects`, `last_scraped_at`, `keyword_search`
- **THEN** no duplicate rows are created

### Requirement: Adapter Search Method
Extend `XiaohongshuAdapter` with a dedicated `search_notes` method returning richer data than `TrendItem`.

#### Scenario: Search with Sort
- **GIVEN** keyword = "护肤", sort = "time_descending"
- **WHEN** `search_notes(keyword, sort, page)` is called
- **THEN** it POSTs to `/api/sns/web/v1/search/notes` with the sort param
- **THEN** returns a list of dicts with: `note_id`, `title`, `desc`, `cover_url`, `likes`, `comments`, `collects`, `user_nickname`, `user_id`

#### Scenario: Sort Mapping
- **WHEN** sort = "general" → `sort: "general"`
- **WHEN** sort = "time_descending" → `sort: "time_descending"`
- **WHEN** sort = "popularity_descending" → `sort: "popularity_descending"`

### Requirement: Celery Scrape Task
A Celery task that orchestrates adapter → upsert pipeline.

#### Scenario: Task Execution
- **WHEN** `scrape_xhs_keyword_task(tenant_id, keyword, sort_type)` runs
- **THEN** it initializes the adapter, calls `search_notes`
- **THEN** upserts all results using `ON CONFLICT` via SQLAlchemy
- **THEN** returns `{"saved": count, "keyword": keyword}`

### Requirement: API Endpoints
REST endpoints to trigger scraping and browse results.

#### Scenario: POST /api/v1/xhs/scrape
- **WHEN** called with `{ keyword, sort_type }`
- **THEN** dispatches `scrape_xhs_keyword_task.delay(...)` 
- **THEN** returns `{ task_id }` immediately (async)

#### Scenario: GET /api/v1/xhs/notes
- **WHEN** called with optional `keyword` filter and `page`/`page_size` params
- **THEN** returns paginated `XhsNote` list for the tenant
- **THEN** default sort is `last_scraped_at DESC`

### Requirement: XhsScraperConsole Frontend
A glassmorphism console for searching and browsing scraped notes.

#### Scenario: Control Bar
- **THEN** displays a keyword input, sort dropdown (最新/综合/热门), and "开始采集" button
- **THEN** button shows loading state while task is in progress

#### Scenario: Results Grid
- **THEN** displays notes in a Masonry/CSS Grid layout
- **THEN** each card shows cover image, title (2-line truncated), and like count
- **THEN** images use `referrerPolicy="no-referrer"` to bypass XHS CDN checks

#### Scenario: Polling
- **WHEN** scrape task is dispatched
- **THEN** the UI polls `GET /notes` every 3 seconds until new results appear
- **THEN** stops polling after 30 seconds or on new data
