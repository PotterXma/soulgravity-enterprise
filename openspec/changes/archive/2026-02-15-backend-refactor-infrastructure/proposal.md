## Why

The current project structure uses hyphenated directory names for some Python packages (e.g., `libs/core-kernel`), which are invalid in Python import statements. Additionally, the telemetry module is misplaced, and the deployment infrastructure (Nginx, Docker Compose) is not yet fully integrated for the master directory structure defined in Phase 3.

This change aims to enforce Python naming conventions, standardize imports, and provide a fully functional local development environment with proper reverse proxying and automation scripts.

## What Changes

1.  **Backend Refactoring**:
    -   Rename directories: `libs/core-kernel` -> `libs/core_kernel`, `libs/infra-db` -> `libs/infra_db`, `libs/infra-net` -> `libs/infra_net`.
    -   Refactor Telemetry: Move `libs/core_kernel/telemetry.py` to `libs/telemetry/__init__.py`.
    -   Global Search & Replace: Update all imports in `apps/` and `libs/` to reflect these changes.

2.  **Infrastructure Setup**:
    -   Configure `deploy/nginx/default.conf` to handle API requests, WebSocket upgrades, and Frontend routing.
    -   Update `deploy/docker-compose.yml` to orchestrate all services (API, Worker, Scraper, Nginx, Frontend, Database, Redis, RabbitMQ).

3.  **Automation**:
    -   Create a root `Makefile` to simplify development tasks (`up`, `down`, `logs`, `refactor`).

## Capabilities

### New Capabilities
-   `backend-refactoring`: Validates and corrects Python package names and imports.
-   `infrastructure-setup`: Provides Nginx reverse proxy and full-stack Docker Compose configuration.
-   `automation`: Provides a `Makefile` for consistent developer experience.

### Modified Capabilities
-   None.

## Impact

-   **Codebase**: Widespread changes to import statements in `apps/` and `libs/`.
-   **Structure**: Directories in `libs/` will be renamed.
-   **Deployment**: New configuration files in `deploy/` and `web-console/`.
