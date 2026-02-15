# Design: Phase 2 - Operational Excellence

## 1. Directory Structure Updates

```
libs/
├── core_kernel/
│   ├── telemetry.py            # [NEW] Structlog & CorrelationIdContext
│   └── interfaces/
│       ├── proxy_provider.py   # [NEW] IProxyProvider ABC
│       └── platform_config.py  # [NEW] BasePlatformConfig & Polymorphism
├── infra_net/
│   └── simple_proxy.py         # [NEW] Reference Proxy Implementation
apps/
├── api_gateway/
│   └── middleware/
│       └── correlation.py      # [NEW] Request ID Middleware
└── worker_scraper/
    └── celery_config.py        # [MODIFY] Add DLX/DLQ & Signal Handlers
alembic/                        # [NEW] Migration scripts
└── env.py                      # [NEW] Async migration environment
```

## 2. Distributed Tracing & Logging Design

### 2.1 Context Propagation
- **Core:** Use `contextvars.ContextVar("correlation_id")` to store trace ID.
- **API:** Middleware extracts `X-Request-ID` or generates UUID, sets context.
- **Celery:**
    - `before_task_publish`: Reads context var, injects into task headers (`headers={'correlation_id': '...'}`).
    - `task_prerun`: Reads task header, sets context var in worker thread.
- **Logging:** `structlog` configured to auto-bind `correlation_id` from context.

## 3. Proxy Infrastructure

### 3.1 Interface (`IProxyProvider`)
- `get_proxy(protocol: str, strategy: Strategy) -> ProxyDTO`
- **Strategy:**
    - `RANDOM`: Returns any healthy proxy.
    - `STICKY`: Returns consistent proxy for a session (hash based).

## 4. Database Migrations

### 4.1 Alembic Layout
- **Async Pattern:** `env.py` creates `async_engine`, runs `run_migrations_online` in asyncio loop.
- **Metadata:** Imports `libs.infra_db.base.Base` to detect model changes.

## 5. Task Reliability (DLQ)

### 5.1 RabbitMQ Topology
- **Main Exchange:** `scraper.exchange` (Direct)
- **Main Queue:** `scraper.tasks` (bound to `scraper.exchange`)
    - Arguments: `x-dead-letter-exchange: scraper.dlx`, `x-dead-letter-routing-key: scraper.dlq`
- **DLX Exchange:** `scraper.dlx` (Fanout/Direct)
- **DLQ Queue:** `scraper.dlq` (bound to `scraper.dlx`)

## 6. Polymorphic Configuration

### 6.1 Pydantic Strategy
- **Base:** `BasePlatformConfig` (Pydantic model).
- **Discriminator:** `platform_name` field.
- **Storage:** stored as JSONB in PostgreSQL `tenants` table.
- **Validation:** Pydantic `Adapter` or `Union` types to hydrate correct subclass based on platform name.
