# Specification: SoulGravity Enterprise Scaffolding

## 1. Functional Requirements

### 1.1 Plugin System
- **Discovery**: The system must dynamically discover and load platform adapters from `plugins/platforms/` at startup.
- **Interface**: All platform plugins must implement `libs.core_kernel.interfaces.BasePlatformAdapter`.
- **Isolation**: Plugins must not directly import database models or infrastructure code; they must communicate via DTOs/Value Objects.

### 1.2 Core Platform Operations
The `BasePlatformAdapter` must enforce implementation of:
- `login(credentials)`: Authenticate with platform.
- `fetch_hot_trends(keyword)`: Retrieve trending content.
- `publish_content(payload)`: Post content (text/image/video).
- `get_analytics(post_id)`: Retrieve engagement metrics.
- `check_cookie_health()`: Verify session validity.

### 1.3 Tenant Context
- **Middleware**: API requests must process `X-Tenant-ID` header.
- **Propagation**: The Tenant ID must be available to all layers via `contextvars`.
- **Data Isolation**: All database queries must automatically filter by the current Tenant ID.

### 1.4 Browser Automation
- **Abstraction**: An `IBrowserContext` interface must wrap underlying automation tools.
- **Factory**: A factory must provide browser instances, supporting reconfiguration (e.g., swapping Playwright for Selenium).
- **Anti-Detect**: Configuration hooks for stealth plugins (stealth.min.js, fingerprint masking) must be available.

## 2. Non-Functional Requirements

### 2.1 Technology Stack
- **Language**: Python 3.11+.
- **Web Framework**: FastAPI.
- **Task Queue**: Celery with Redis (Broker & Backend).
- **Database**: PostgreSQL with Async SQLAlchemy 2.0.

### 2.2 Architecture & Design
- **Domain-Driven Design (DDD)**: Clear separation of bounded contexts (Acquisition, Cognitive, Distribution, Identity).
- **Hexagonal Architecture**: Core logic depends only on interfaces (Ports); Infrastructure implements interfaces (Adapters).

### 2.3 Resiliency
- **Circuit Breaker**: Prevent cascading failures when external platforms are down.
- **Rate Limiting**: Enforce API usage limits per tenant/platform.
- **Retry Mechanism**: Exponential backoff for transient errors.

### 2.4 Deployment
- **Containerization**: Docker images for API and Workers.
- **Orchestration**: Docker Compose for local development (API, Worker-Scraper, Worker-Publisher, DB, Redis, RabbitMQ).
