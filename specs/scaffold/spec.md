# Specification: Core Architecture Scaffold

## ADDED Requirements

### Requirement: Plugin System Discovery
The system must dynamically discover and load platform adapters from the plugins directory at startup without hardcoded references.

#### Scenario: Application Startup with Valid Plugins
- **WHEN** The API Gateway or Worker service starts
- **THEN** The PluginManager scans `plugins/platforms/`
- **AND** Detected valid adapters (e.g., xiaohongshu, douyin) are registered in the internal registry
- **AND** The list of loaded platforms is available via the PluginManager

### Requirement: Tenant Context Isolation
API requests must carry context identifying the tenant to ensure data isolation across the system.

#### Scenario: Request with Valid Tenant ID
- **WHEN** An API request is received with header `X-Tenant-ID: valid-tenant`
- **THEN** The `TenantMiddleware` extracts the ID
- **AND** Sets the `tenant_context` ContextVar
- **AND** Downstream DB queries automatically filter results by this Tenant ID

#### Scenario: Request without Tenant ID
- **WHEN** An API request is received without `X-Tenant-ID` header
- **THEN** The API returns 400 Bad Request (except for health checks)

### Requirement: Universal Platform Interface
All platform plugins must implement a strictly defined interface to ensure interoperability.

#### Scenario: Adapter Implementation Verification
- **WHEN** A new platform adapter is instantiated
- **THEN** It must implement `login`, `fetch_hot_trends`, `publish_content`, `get_analytics`, `check_cookie_health`
- **AND** Inputs and outputs must strictly conform to defined Pydantic models (e.g., `PublishPayload`, `TrendItem`)

### Requirement: Anti-Detect Browser Abstraction
Browser automation must happen through an abstract factory to allow swapping underlying engines.

#### Scenario: Browser Context Creation
- **WHEN** A `BrowserFactory` creates a new context
- **THEN** It returns an object implementing `IBrowserContext`
- **AND** The underlying engine (e.g., Playwright) is transparent to the caller
