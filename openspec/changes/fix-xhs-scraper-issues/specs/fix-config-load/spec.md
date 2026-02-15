## ADDED Requirements

### Requirement: XhsConfig.load classmethod
Add a `load(tenant_id)` class method to `XhsConfig` that constructs an instance from environment variables or defaults.

#### Scenario: Load from env
- **WHEN** `XhsConfig.load(tenant_id="default")` is called
- **THEN** it reads `XHS_COOKIE` and `XHS_PROXY_URL` from env vars
- **THEN** returns an `XhsConfig` instance with those values
- **THEN** if `XHS_COOKIE` is not set, raises `ValueError`

### Requirement: Clean unused import
Remove `from sqlalchemy import text` from `xhs_tasks.py`.
