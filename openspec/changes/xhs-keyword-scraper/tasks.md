## 1. Database Model
- [x] 1.1 Create `plugins/platforms/xiaohongshu/models.py` with `XhsNote` table
- [ ] 1.2 Generate Alembic migration for `xhs_note` table

## 2. Adapter
- [x] 2.1 Add `search_notes(keyword, sort, page)` method to `XiaohongshuAdapter`

## 3. Celery Task
- [x] 3.1 Create `apps/worker_scraper/tasks/xhs_tasks.py` with `scrape_xhs_keyword_task`
- [x] 3.2 Implement `ON CONFLICT` upsert logic

## 4. API Endpoints
- [x] 4.1 Add `POST /scrape` endpoint to `apps/api_gateway/routers/xhs.py`
- [x] 4.2 Add `GET /notes` endpoint with pagination and keyword filter

## 5. Frontend Console
- [x] 5.1 Create `web-console/src/features/plugins/xiaohongshu/XhsScraperConsole.tsx`
- [x] 5.2 Wire into routing in `App.tsx` (lazy loaded)

## 6. Verification
- [x] 6.1 Frontend build (`npm run build`) — PASSED
- [ ] 6.2 Backend import check (requires venv + dependencies)
