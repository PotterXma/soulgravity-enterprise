## Context

The XHS scraper pipeline currently supports:
- **Backend**: `GET /notes` already returns `PaginatedNotes { items, total, page, page_size }` with `page`/`page_size` query params. `POST /scrape` triggers a Celery task.
- **Adapter**: `search_notes()` fetches from XHS search API but only returns title, cover, desc (from search snippets — not full content), and engagement metrics.
- **Model**: `XhsNote` stores `note_id, title, desc, cover_url, likes, comments, collects, user_nickname, user_id, keyword_search, last_scraped_at, tenant_id`. No `images_list` field.
- **Frontend**: `XhsScraperConsole.tsx` already has `PaginatedResponse` type and fetches `GET /notes` but renders all results without using `<Pagination />`. No note detail view exists.

## Goals / Non-Goals

**Goals:**
- Integrate Ant Design `<Pagination />` in the frontend, wired to the existing paginated API
- Build a `NoteDetailDrawer` component showing full note content with image gallery, description, stats
- Add `POST /enrich/{note_id}` endpoint that fetches and persists full note content from XHS feed API
- Add `images_list` column to `XhsNote` model for storing image gallery URLs

**Non-Goals:**
- Changing the scrape/search flow itself (Celery task pipeline stays as-is)
- Adding new auth or tenant-resolution logic
- Building a standalone note CRUD beyond enrich
- Optimizing XHS signing/anti-spider beyond what `_request()` already handles

## Decisions

### 1. Enrichment API — `POST /api/v1/xhs/enrich/{note_id}`

**Choice**: Dedicated endpoint rather than auto-enriching during search.

**Rationale**: Search results intentionally return lightweight data. Full content fetching is expensive (extra API call per note, risk of triggering anti-spider). User-initiated enrichment lets users selectively fetch detail only for notes they care about.

**Flow**:
1. Frontend calls `POST /enrich/{note_id}`
2. Router loads `XhsNote` from DB to get `tenant_id` context
3. Router calls `adapter.get_note_detail(note_id)` 
4. Adapter hits XHS feed API (`/api/sns/web/v1/feed`) with the note ID
5. Adapter returns `{ desc, images_list }` 
6. Router updates the DB row and returns the enriched note

**Alternative considered**: Background Celery task for enrichment — rejected because the user needs instant feedback in the drawer, and the operation is fast enough for a synchronous call.

### 2. `get_note_detail()` — XHS Feed API

**Choice**: Use `/api/sns/web/v1/feed` endpoint with `source_note_id` param.

**Rationale**: This is the standard XHS web endpoint for fetching a single note's full content. It returns `desc` (full text), `image_list` (array of image URLs), and updated engagement metrics.

**Request shape**:
```python
POST /api/sns/web/v1/feed
{ "source_note_id": note_id, "image_formats": ["jpg", "webp", "avif"], "extra": {"need_body_topic": 1} }
```

**Response parsing**: Extract from `data.items[0].note_card` → `desc`, `image_list[].url_default`.

### 3. `images_list` Column Type

**Choice**: `Text` column storing JSON-serialized list of image URLs.

**Rationale**: SQLModel/SQLAlchemy `JSON` type has portability issues across MySQL versions. A simple `Text` column with `json.dumps/loads` is universally compatible and avoids introducing a new column type dependency.

**Schema**: `images_list: Optional[str] = Field(default=None, sa_type_kwargs={"length": None})` — same pattern as existing `desc` field.

### 4. Frontend Pagination

**Choice**: Use the existing `PaginatedResponse` type + Ant Design `<Pagination />` component.

**Rationale**: Backend already supports pagination. Frontend already has the type. Just need to:
- Track `currentPage` state
- Pass `page` param to `GET /notes`
- Render `<Pagination total={total} current={page} onChange={...} />`

### 5. NoteDetailDrawer Architecture

**Choice**: A standalone component receiving `noteId` + `open` state, fetching its own data from the existing note list (no extra GET endpoint needed initially — the note data is already in the parent's state). Enrichment is triggered by a button press.

**Component API**:
```tsx
<NoteDetailDrawer 
  open={boolean}
  note={XhsNoteItem | null}
  onClose={() => void}
  onEnriched={(note: XhsNoteItem) => void}  // callback to update parent state
/>
```

**Image gallery**: Use Ant Design `<Image.PreviewGroup>` + grid layout (not a heavy carousel dep).

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| XHS feed API may 461/462 anti-spider during enrichment | Existing `_request()` already handles these codes with `PlatformAntiSpiderError`. Frontend shows the error message. |
| `images_list` could be large (20+ images × URL length) | `Text` column has no practical size limit. JSON parsing overhead is negligible for a list of strings. |
| No Alembic auto-detect for new column | Manually write migration or use `alembic revision --autogenerate`. Document in tasks. |
| User spam-clicks "Fetch Full Content" | Disable button after first click until response arrives (loading state in drawer). |
