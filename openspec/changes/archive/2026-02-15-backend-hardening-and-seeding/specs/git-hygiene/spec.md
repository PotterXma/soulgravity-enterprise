# Specification: Git Hygiene

## Requirements

### 1. Comprehensive Ignore File
A root `.gitignore` must prevent accidental commit of artifacts.
- **Requirement:** Ignore Python artifacts: `__pycache__`, `.venv`, `.env`, `.pytest_cache`, `*.egg-info`.
- **Requirement:** Ignore Node.js artifacts: `node_modules`, `dist`, `.DS_Store`.
- **Requirement:** Ignore IDE configs: `.vscode`, `.idea`.
- **Requirement:** Ignore App logs: `*.log`, `celerybeat-schedule`.

## Scenarios

### Scenario: Clean Status
- **WHEN** `git status` is run in a dirty directory containing `__pycache__` or `node_modules`
- **THEN** these directories should not be listed as untracked files.
