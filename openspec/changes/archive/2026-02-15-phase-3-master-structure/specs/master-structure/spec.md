# Specification: Master Directory Structure

## Requirements

### 1. Strict Monorepo Layout
The project must adhere to the Master Directory Blueprint:
-   `deploy/` for infrastructure (Nginx, Docker Compose)
-   `web-console/` for React Frontend
-   `Makefile` at root for CLI automation
-   `libs/telemetry/` for standardized observability helper (moved from `core_kernel`)

### 2. Deployment Infrastructure
-   **Nginx:** Reverse Proxy configuration (`deploy/nginx/default.conf`) routing `/api` to Backend and `/` to Frontend.
-   **Docker Compose:** Updated `deploy/docker-compose.yml` orchestrating API, Scraper, Publisher, Postgres, Redis, RabbitMQ, and Nginx.

### 3. Frontend Scaffold
-   **Stack:** React + Vite + TypeScript.
-   **Structure:** Feature-Sliced Design (`src/features`, `src/lib`, `src/components`).
-   **Library:** Ant Design Pro components.

### 4. Developer Experience (Makefile)
-   `make up`: Start entire stack.
-   `make down`: Stop stack.
-   `make shell-api`: Enter API container shell.
-   `make logs`: Stream logs.

### 5. Telemetry Refactor
-   Refactor `libs.core_kernel.telemetry` to `libs.telemetry`.
-   Ensure existing code (`api-gateway`, `celery_config`) updates imports.
