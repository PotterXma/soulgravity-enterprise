# Proposal: SoulGravity Enterprise Scaffolding

## Abstract
Scaffold the foundational architecture for **"Lingxi · SoulGravity Enterprise"**, a next-generation social media automation middleware. This proposal establishes a Domain-Driven, Hexagonal Architecture monorepo designed for high scalability, multi-tenancy, and rapid plugin expansion.

## Problem Statement
Current social media automation tools often suffer from:
1.  **Tight Coupling:** Platform logic is intertwisted with core business logic, making it hard to add new platforms (e.g., adding TikTok breaks Instagram logic).
2.  **Lack of Isolation:** Single-tenant designs that fail to scale for enterprise needs; data leakage risks.
3.  **Fragility:** Poor handling of platform API limits, network jitter, and account bans.
4.  **Vendor Lock-in:** Hard dependencies on specific browser automation tools (e.g., only Selenium).

## Goals
1.  **Modular Architecture:** Implement a strict "Ports & Adapters" (Hexagonal) architecture to decouple core logic from infrastructure and external platforms.
2.  **Plugin-First Design:** Create a `BasePlatformAdapter` interface and a dynamic `PluginManager` so adding a platform is as simple as dropping in a new file.
3.  **Enterprise Readiness:** Built-in multi-tenancy (Tenant Context Middleware) and security standards (RBAC, Encryption).
4.  **Resiliency:** Core utilities for Circuit Breaking, Rate Limiting, and Retries.
5.  **Scalability:** Async-first (FastAPI + Celery) with ready-to-deploy Docker/K8s configuration.

## Scope
### In Scope
- Monorepo directory structure setup.
- Core Kernel implementation (Interfaces, Domain Objects, Plugin Loader).
- Infrastructure layer (Database Session, Generic Repository, Tenant mixins).
- API Gateway service scaffold (FastAPI).
- Worker service scaffolds (Scraper & Publisher via Celery).
- Anti-Detect Browser Factory abstraction.
- Docker and Docker Compose configuration.

### Out of Scope
- Implementation of specific platform logic (Xiaohongshu/Douyin adapters will be stubs only).
- Frontend UI development.
- Production K8s manifest generation (Docker Compose is sufficient for now).
- Comprehensive CI/CD pipelines.

## Success Metrics
- **Extensibility:** A developer can add a new platform plugin by implementing the `BasePlatformAdapter` interface without modifying the core kernel.
- **Tenant Isolation:** Database queries automatically filter by `X-Tenant-ID` without manual `WHERE` clauses in business logic.
- **Performance:** Plugin discovery adds negligible overhead (<100ms) to startup time.
- **Reliability:** The system successfully handles simulated network failures using the implemented resiliency patterns.
