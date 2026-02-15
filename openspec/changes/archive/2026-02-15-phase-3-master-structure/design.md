# Design: Phase 3 - Master Directory Structure

## 1. Directory Structure

```
soulgravity-enterprise/
├── .github/                       # CI/CD Workflows
├── deploy/                        # Infrastructure as Code
│   ├── nginx/
│   │   └── default.conf           # [NEW] Reverse Proxy
│   └── docker-compose.yml         # [MOVED/MODIFIED] Full Stack
├── apps/                          # Backend Services
│   ├── api_gateway/               # [EXISTING]
│   ├── worker_scraper/            # [EXISTING]
│   └── worker_publisher/          # [EXISTING]
├── libs/                          # Shared Kernel
│   ├── core_kernel/               # [EXISTING]
│   ├── infra_db/                  # [EXISTING]
│   ├── infra_net/                 # [EXISTING: simple_proxy.py]
│   └── telemetry/                 # [NEW/REFACTORED] Structlog & Tracing
│       └── __init__.py            # (was libs/core_kernel/telemetry.py)
├── web_console/                   # [NEW] Frontend SPA
│   ├── src/
│   │   ├── features/              # FSD Design
│   │   ├── lib/
│   │   └── components/
│   └── package.json
├── Makefile                       # [NEW] CLI Automation
└── pyproject.toml                 # [EXISTING/UPDATED]
```

## 2. Infrastructure (deploy/)

### 2.1 Nginx Reverse Proxy
- **Path:** `deploy/nginx/default.conf`
- **Port:** 80
- **Upstreams:**
    - `/api` -> `api_gateway:8000`
    - `/api/ws` -> `api_gateway:8000` (WebSocket Upgrade)
    - `/` -> `web_console:3000` (Dev Server) or static files (Prod Build)

### 2.2 Docker Compose
- **Moved:** `root/docker-compose.yml` -> `deploy/docker-compose.yml`
- **Updated:** Services now reference `../apps/...` context.
- **Added:** `nginx` service linking `api` and `web_console`.
- **Added:** `web_console` service (Node 18 image).

## 3. Frontend Scaffold (web_console/)

### 3.1 Technology Stack
- **Framework:** React 18 + Vite + TypeScript
- **UI Lib:** Ant Design Pro (v5/v6 components)
- **State:** Zustand
- **Networking:** Axios + TanStack Query

### 3.2 Directory Layout (Feature-Sliced Design Lite)
- `src/app/` (Global providers, router)
- `src/features/` (e.g., `auth/`, `dashboard/`, `plugins/`)
- `src/shared/` (UI Kit, Utils)

## 4. Telemetry Refactor
- Move `libs/core_kernel/telemetry.py` to `libs/telemetry/__init__.py`.
- Update all imports in `api_gateway`, `worker_scraper`, `celery_config`.
