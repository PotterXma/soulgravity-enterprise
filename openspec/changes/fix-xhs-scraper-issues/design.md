## Decisions
1. Use env vars (`XHS_COOKIE`, `XHS_PROXY_URL`) with tenant_id prefix support (e.g., `XHS_COOKIE_default`). Fall back to unprefixed env var.
2. Raise `ValueError` with clear message if no cookie is configured.
