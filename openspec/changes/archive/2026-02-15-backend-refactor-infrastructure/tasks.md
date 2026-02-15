# Tasks: Backend Refactor & Infrastructure

## 1. Backend Refactoring
- [x] Create `scripts/refactor_backend.sh` using the content from `design.md`
- [x] Execute `scripts/refactor_backend.sh` to rename directories and update imports
- [x] Verify no hyphenated imports remain (`grep -r "libs.core-kernel" apps libs` should be empty)

## 2. Infrastructure Setup
- [x] Create `deploy/nginx/default.conf` with WebSocket support
- [x] Create `deploy/docker-compose.yml` with full service orchestration

## 3. Automation
- [x] Create root `Makefile` with `up`, `down`, `refactor`, `logs`, `shell-api` commands
- [x] Verify `make up` starts the stack correctly
- [x] Verify `localhost/api/healthz` is accessible
- [x] Verify `localhost/` loads the frontend
