# Design: SoulGravity Enterprise Scaffolding

## 1. Directory Structure

```
soulgravity-enterprise/
├── apps/                          # Application Entry Points (Ports)
│   ├── api-gateway/               # Main HTTP Service
│   │   ├── main.py
│   │   ├── middleware/            # Tenant Context Middleware
│   │   └── routers/
│   ├── worker-scraper/            # Dedicated Scraping Node
│   │   └── celery_app.py
│   └── worker-publisher/          # Dedicated Publishing Node
│       └── celery_app.py
├── libs/                          # Shared Libraries (Kernel & Adapters)
│   ├── core-kernel/               # The "Hexagon" (Inner)
│   │   ├── interfaces/            # Abstract Base Classes
│   │   │   ├── platform.py        # BasePlatformAdapter
│   │   │   ├── content_generator.py # IContentGenerator
│   │   │   └── browser.py         # IBrowserContext
│   │   ├── plugin_loader.py       # Dynamic Plugin Registry
│   │   ├── domain/                # DDD Value Objects
│   │   │   ├── acquisition.py
│   │   │   ├── cognitive.py
│   │   │   ├── distribution.py
│   │   │   └── identity.py
│   │   └── resiliency/            # Circuit Breaker, Rate Limiter
│   ├── infra-db/                  # Database Infrastructure (Outer)
│   │   ├── session.py             # Async Session Factory
│   │   ├── base.py                # TenantMixin + DeclarativeBase
│   │   └── repository.py          # GenericRepository[T]
│   └── security/                  # Security Utilities
│       ├── jwt.py
│       ├── rbac.py
│       └── encryption.py
├── plugins/                       # Pluggable Implementations (Adapters)
│   └── platforms/
│       ├── xiaohongshu/           # Concrete Platform Adapter
│       └── douyin/
└── docker-compose.yml             # Orchestration
```

## 2. Core Components

### 2.1 Plugin Loader (`libs.core_kernel.plugin_loader`)
A singleton `PluginManager` uses `importlib` to scan `plugins/platforms/*/adapter.py`.
It looks for subclasses of `BasePlatformAdapter` and registers them in a dictionary: `platform_name -> adapter_class`.
This loaded at application startup (lifespan event).

### 2.2 Tenant Context Middleware (`apps.api-gateway.middleware.tenant`)
- **Key**: `X-Tenant-ID`
- **Output**: `contextvars.ContextVar("tenant_id")`
- **Mechanism**: Inherits from `BaseHTTPMiddleware`. Checks header, sets context var for the duration of the request.
- **DB Integration**: The DB session factory or models will inspect this context var to apply filters automatically.

### 2.3 Base Platform Adapter (`libs.core_kernel.interfaces.platform`)
All platforms must inherit from `BasePlatformAdapter`.
Abstract methods enforce a unified API for scraping and publishing, ensuring higher-level services (like "Campaign Manager") don't need to know platform specifics.

### 2.4 Resiliency Decorators (`libs.core_kernel.resiliency`)
- `@circuit_breaker(failure_threshold=5, recovery_timeout=60)`: Wraps external calls. Opens circuit after 5 failures, rejecting calls for 60s.
- `@retry(backoff=2, max_retries=3)`: Retries with exponential backoff on specific exceptions (e.g., `NetworkError`, `RateLimitError`).

## 3. Data Architecture

### 3.1 Tenant Isolation
- **Approach**: Row-Level Security (Application Layer).
- **Implementation**: A `TenantMixin` adds a `tenant_id` column to every model.
- **Safety**: `GenericRepository` automatically appends `.where(Model.tenant_id == current_tenant_id())` to every query, preventing accidental data leakage.

## 4. Infrastructure

### 4.1 Docker
- **Base Image**: `python:3.11-slim`
- **Multi-stage Build**: optimize size.
- **Services**:
    - `api`: FastAPI (uvicorn)
    - `worker-scraper`: Celery (concurrency=autoscale)
    - `worker-publisher`: Celery (concurrency=1) - strict serial publishing to avoid blocks.
    - `redis`: Broker & Backend.
    - `postgres`: Persistent storage.
