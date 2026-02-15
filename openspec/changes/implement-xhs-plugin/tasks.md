# Tasks: Implement Xiaohongshu Plugin (MOD_01_XHS)

## Dependencies & Setup
- [x] Add `curl_cffi` to `pyproject.toml` and install

## Core Implementation
- [x] Create `plugins/platforms/xiaohongshu/config.py` (Pydantic Schema)
- [x] Create `plugins/platforms/xiaohongshu/schemas.py` (Data Models)
- [x] Create `plugins/platforms/xiaohongshu/signing.py` (Header Signer Stub)
- [x] Create `plugins/platforms/xiaohongshu/adapter.py` (The Adapter Logic)
    - [x] `__init__` with `AsyncSession`
    - [x] `login` / `check_health`
    - [x] `fetch_hot_trends`
    - [x] `publish_content` (image upload flow)

## API Layer
- [x] Create `apps/api-gateway/routers/xhs.py` (Test Endpoint)
- [x] Register router in `apps/api-gateway/main.py`

## Verification
- [ ] Verify `check_health` with valid cookie
- [ ] Verify error handling (461/401)
