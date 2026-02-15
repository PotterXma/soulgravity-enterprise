# Infrastructure Setup Specification

## Requirements

### 1. Nginx Reverse Proxy
A central Nginx reverse proxy must route traffic to appropriate services.
- **Requirement:** Configure Nginx to listen on port 80.
- **Requirement:** Route `/api` requests to `api_gateway:8000`.
- **Requirement:** Route `/` requests to `web_console:3000`.
- **Requirement:** Support WebSocket upgrades on `/api/ws` with `Upgrade` and `Connection` headers.

### 2. Full Stack Orchestration
Docker Compose must manage the entire application stack.
- **Requirement:** Update `deploy/docker-compose.yml` to include `nginx` and `web_console` services.
- **Requirement:** Ensure all service build contexts (`../`) point to the project root.
- **Requirement:** Mount `apps/`, `libs/`, and `plugins/` as volumes for hot-reloading.

## Scenarios

### Scenario: API Access
- **WHEN** a request is sent to `http://localhost/api/healthz`
- **THEN** it should reach the API Gateway and return 200 OK.

### Scenario: Frontend Access
- **WHEN** a user visits `http://localhost/`
- **THEN** the React application should load.
