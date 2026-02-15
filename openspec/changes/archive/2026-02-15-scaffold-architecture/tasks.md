# Tasks: SoulGravity Enterprise Scaffolding

## 1. Directory Structure Setup
- [x] Create directory structure (`apps/`, `libs/`, `plugins/`)
- [x] Create `apps/api_gateway/main.py`
- [x] Create `apps/worker_scraper/celery_app.py`
- [x] Create `apps/worker_publisher/celery_app.py`

## Core Kernel Implementation
- [x] Define `libs/core_kernel/interfaces/platform.py` (`BasePlatformAdapter`)
- [x] Define `libs/core_kernel/interfaces/content_generator.py` (`IContentGenerator`)
- [x] Define `libs/core_kernel/interfaces/browser.py` (`IBrowserContext`)
- [x] Implement `libs/core_kernel/plugin_loader.py` (`PluginManager`)
- [x] Implement `libs/core_kernel/resiliency/circuit_breaker.py`
- [x] Implement `libs/core_kernel/resiliency/rate_limiter.py`
- [x] Implement `libs/core_kernel/resiliency/retry.py`

## Infrastructure Layer
- [x] Create `libs/infra_db/session.py` (Async session factory)
- [x] Create `libs/infra_db/base.py` (`Base`, `TenantMixin`)
- [x] Create `libs/infra_db/repository.py` (`GenericRepository`)
- [x] Create `libs/security/jwt.py`
- [x] Create `libs/security/rbac.py`
- [x] Create `libs/security/encryption.py`

## Service & Plugins
- [x] Implement `apps/api_gateway/middleware/tenant.py`
- [x] Implement stub `plugins/platforms/xiaohongshu/adapter.py`
- [x] Implement stub `plugins/platforms/douyin/adapter.py`
- [x] Implement stub `apps/worker_scraper/tasks/scrape.py`
- [x] Implement stub `apps/worker_publisher/tasks/publish.py`

## Deployment & Config
- [x] Create `Dockerfile` (Multi-stage build)
- [x] Create `docker-compose.yml` (App + DB + Redis + RabbitMQ)
- [x] Create `pyproject.toml` and `requirements.txt`

## Verification
- [x] Verify interface imports work.
- [x] Verify plugin loader discovers plugins.
- [x] Verify API starts and responds to `X-Tenant-ID`.
- [x] Verify Docker Compose builds and runs.
