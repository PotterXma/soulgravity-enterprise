# Tasks: Backend Hardening and Data Seeding

## 1. Data Seeding
- [x] Create `scripts/seed.py` using `libs.infra_db.session` to connect.
- [x] Implement robust check-or-create logic for "System" Tenant.
- [x] Implement robust check-or-create logic for "Super Admin" User with hashed password.
- [x] Ensure credentials are printed to console on success.

## 2. Git Hygiene
- [x] Create/Update root `.gitignore` to cover Python (pycache, venv, egg-info), Node (node_modules, dist), IDEs, and app logs.

## 3. Linting Configuration
- [x] Update `pyproject.toml` with `ruff` configuration (line-length 100, specific rulesets I, F, E).
- [x] Create `.pre-commit-config.yaml` with hooks for `ruff`, `ruff-format`, and `check-yaml`.

## 4. Verification
- [x] Run `python3 scripts/seed.py` and verify database population (check via psql or code).
- [x] Run `git status` to verify ignored files are not showing up.
- [x] Run `pre-commit run --all-files` to verify linting rules are applied.
