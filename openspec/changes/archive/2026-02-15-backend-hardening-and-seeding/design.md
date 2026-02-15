# Technical Design: Backend Hardening and Data Seeding

## Context
Initial setup is complete, but the project lacks local data for development, and code quality tools are not configured.

## Goals
1.  **Seeding**: Provide a one-click local setup script.
2.  **Hygiene**: Prevent committing artifacts to git.
3.  **Linting**: Enforce Python standards automatically.

## Decisions

### 1. Data Seeding Script (`scripts/seed.py`)
Use `asyncio` and `libs.infra_db.session` to reuse application logic.
- **Why**: Ensures seeding uses the same ORM models as the app.
- **Logic**:
    -   `get_or_create` logic for Tenant (name="System").
    -   `get_or_create` logic for User (email="admin@soulgravity.com").
    -   Password Hashing: Use `passlib.context.CryptContext` if available, or a simple mock/placeholder if the security module isn't fully ready (will verify `libs.security` first).

### 2. Git Ignore Strategy
Standard comprehensive ignore file.
```
__pycache__/
*.py[cod]
*$py.class
.venv
.env
.DS_Store
node_modules/
dist/
.vscode/
.idea/
*.log
celerybeat-schedule
```

### 3. Linting Configuration
- **Tool**: `ruff` (replaces Black, Isort, Flake8).
- **Config**: `pyproject.toml`
    -   `line-length = 100`
    -   `select = ["E", "F", "I"]` (Error, Pyflakes, Import sorting)
- **Hooks**: `pre-commit`
    -   `astral-sh/ruff-pre-commit`
    -   `pre-commit/pre-commit-hooks` (check-yaml, end-of-file-fixer)

## Risks
-   **Database Connection**: Script might fail if DB isn't running. Solution: Doc instructions to run `make up` first.
-   **Pre-commit Adoption**: Developers might skip hooks. Solution: Enforce in CI later (out of scope for now).
