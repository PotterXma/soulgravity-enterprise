# Tasks: Phase 2 - Operational Excellence

## 1. Observability (Tracing & Logging)
- [x] Implement `libs/core_kernel/telemetry.py` (Structlog config, `CorrelationIdContext`)
- [x] Implement `apps/api_gateway/middleware/correlation.py` (Middleware)
- [x] Update `apps/api_gateway/main.py` to use middleware & logging
- [x] Implement Celery signal handlers for trace propagation

## 2. Proxy Infrastructure
- [x] Define `libs/core_kernel/interfaces/proxy_provider.py` (ABC)
- [x] Implement `libs/infra_net/simple_proxy.py` (Reference implementation)

## 3. Database Migrations
- [x] Initialize Alembic with `alembic init -t asyncio alembic`
- [x] Configure `alembic.ini`
- [x] Configure `alembic/env.py` for async support with `libs.infra_db.base.Base`

## 4. Task Reliability (DLQ)
- [x] Update `apps/worker_scraper/celery_app.py` for DLX/DLQ configuration
- [x] Verify DLQ routing with a failing task test

## 5. Polymorphic Configuration
- [x] Define `libs/core_kernel/interfaces/platform_config.py` (BasePlatformConfig)
- [x] Create `plugins/platforms/xiaohongshu/config.py`
- [x] Demonstrate config validation usage
