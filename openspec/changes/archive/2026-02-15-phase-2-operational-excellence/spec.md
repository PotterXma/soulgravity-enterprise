# Specification: Operational Excellence

## Requirements

### 1. Distributed Tracing & Structured Logging
-   **Tracing:** Every request must have a unique `trace_id`. This ID must propagate from API Gateway to Celery Workers.
-   **Logging:** Logs must be in JSON format and include the `trace_id`, timestamp, log level, and service name.
-   **Context:** The `trace_id` must be accessible via a context variable (`CorrelationIdContext`) throughout the request lifecycle.

### 2. Proxy Infrastructure
-   **Interface:** A standard `IProxyProvider` interface must be defined.
-   **Capabilities:** Support for 'sticky' (same session) and 'random' proxy selection strategies.
-   **Implementation:** A reference `SimpleProxyProvider` should be implemented (e.g., env var based).

### 3. Database Migrations
-   **Tooling:** Use Alembic for schema migrations.
-   **Async Support:** Migration environment (`env.py`) must support `asyncio` loop execution for `asyncpg`.
-   **Metadata:** Must integrate with `libs.infra_db.base.Base` for autogeneration.

### 4. Task Reliability (DLQ)
-   **Retry Policy:** Tasks must retry on transient failures with exponential backoff.
-   **Dead Letter Queue:** Tasks failing after max retries must be routed to a dedicated `dlq` queue via a Dead Letter Exchange (DLX).
-   **Ack Late:** Tasks must only be acknowledged after successful execution or routing to DLQ.

### 5. Polymorphic Configuration
-   **Storage:** Platform-specific configurations must be stored in a JSON column in the `Tenant` table (or similar).
-   **Validation:** Configurations must be validated against specific Pydantic models (e.g., `XiaohongshuConfig`) based on the platform type.
-   **Extensibility:** Adding a new platform config type should not require schema changes, only a new Pydantic model.
