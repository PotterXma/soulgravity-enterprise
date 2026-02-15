# Tasks: Phase 3 - Master Directory Structure

## 1. Directory Structure Enforced
- [x] Create `deploy/nginx/` and `web-console/` directories
- [x] Move `docker-compose.yml` to `deploy/docker-compose.yml` and update paths
- [x] Create `deploy/nginx/default.conf`
- [x] Update `deploy/docker-compose.yml` to include `nginx` and `web_console`

## 2. Telemetry Refactor
- [x] Create `libs/telemetry/` package
- [x] Move `libs/core_kernel/telemetry.py` to `libs/telemetry/__init__.py`
- [x] Update imports in `libs/core_kernel/telemetry.py` (backward compat stub or full refactor)
- [x] Update `apps/api_gateway/main.py` imports
- [x] Update `apps/api_gateway/middleware/correlation.py` imports
- [x] Update `apps/worker_scraper/celery_config.py` imports

## 3. Frontend Scaffold
- [x] Initialize React/Vite app in `web-console/` (using npx create-vite if allowed, or manual file creation)
- [x] Configure `vite.config.ts` proxy for dev
- [x] Add basic Ant Design Pro layout

## 4. Developer Experience
- [x] Create root `Makefile` with `up`, `down`, `logs`, `shell` commands

## 5. Verification
- [x] Verify `make up` starts all containers
- [x] Verify API health check via Nginx (`http://localhost/api/healthz`)
- [x] Verify Frontend loads (`http://localhost/`)

## 6. Hardening & Integration
- [x] **Dockerfile & Path Audit:** Verify all `Dockerfile` `COPY` commands use underscores for Python libraries.
- [x] **Nginx WebSocket Config:** Update `deploy/nginx/default.conf` for `/api/ws` (Completed in initial setup).
- [x] **Automated DB Migration:** Modify entrypoint to run `alembic upgrade head` on startup.
- [x] **Frontend Code Generation:** Install `openapi-typescript-codegen` and add `codegen` script.
- [x] **Local Dev Proxy (Vite):** Configure `server.proxy` in `vite.config.ts` (Completed in initial setup).
