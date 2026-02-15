## Why

To prepare the project for team collaboration and production readiness, we need to establish developer experience baselines. Currently, fresh clones lack data, git hygiene is unenforced, and code style is inconsistent.

## What Changes

1.  **Data Seeding**: A script to populate the database with essential "System" tenant and "Super Admin" user data.
2.  **Git Hygiene**: A comprehensive `.gitignore` to prevent artifactcommit.
3.  **Linting & Formatting**: `ruff` configuration in `pyproject.toml` and pre-commit hooks to enforce standards automatically.

## Capabilities

### New Capabilities
- `data-seeding`: Automated population of initial system data (Tenants, Users).
- `git-hygiene`: Standardized ignore patterns for Python, Node.js, and IDE artifacts.
- `linting-standards`: Enforced code style and quality checks using Ruff and Pre-commit.
