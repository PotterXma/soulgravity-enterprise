# Phase 3: Master Directory Structure & Full-Stack Blueprint

## Abstract
Enforce the strict monorepo directory structure defined by the Chief System Architect. This involves reorganizing existing code, scaffolding the Frontend (`web-console`), adding Deployment Infrastructure (`deploy/`), and standardizing the Developer Experience via `Makefile`.

## Goals
1.  **Strict Layout Enforcement:** Align project structure exactly with the "Master Directory Structure" blueprint.
2.  **Frontend Scaffold:** Initialize `web-console` with React/Vite/AntDesign Pro.
3.  **Deployment Infrastructure:** Create `deploy/` directory with Nginx and Docker Compose configurations.
4.  **Developer Experience:** Create a `Makefile` for common operations (up, down, shell, logs).
5.  **Refactoring:** Move `libs/core_kernel/telemetry.py` to `libs/telemetry/` and ensure all imports are updated.

## Scope
### New Directories
-   `deploy/` (Nginx, Docker Compose)
-   `web-console/` (React SPA Scaffold)
-   `libs/telemetry/` (Observability)
-   `.github/` (CI/CD workflows - stub)
-   `Makefile`

### Refactoring
-   Move `libs/infra_net` to `libs/infra-net` (hyphenated as per blueprint? User said `libs/infra-net` but current is `libs/infra_net`. Python modules usually use underscores. I will use underscores for Python packages `infra_net` but user prompt had hyphens in commentary. Wait, user prompt said `libs/infra-net/`. I should stick to Python standards `infra_net` to avoid import issues, unless "Master Directory Structure" demands hyphens.
    -   *Correction:* User specified `libs/core-kernel`, `libs/infra-db`, etc. in the text tree. Python imports require underscores.
    -   *Decision:* I will use **underscores** for directory names that are Python packages (`core_kernel`, `infra_db`) to match existing working code and Python standards. The User's tree likely used hyphens for readability/convention in other languages, but for Python `core-kernel` is invalid. I will keep `web-console` (hyphen) as it's a Node app.

## Success Metrics
-   Project file structure matches the Blueprint (with Pythonic adjustments).
-   `make up` starts the full stack (Back + Front + DBs).
-   Frontend is accessible via Nginx reverse proxy.
