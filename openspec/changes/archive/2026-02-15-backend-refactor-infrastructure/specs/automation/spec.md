# Automation Specification

## Requirements

### 1. Standard Developer Commands
A `Makefile` must exist at the project root to standardize common operations.
- **Requirement:** `make up` command to start the full stack in detached mode.
- **Requirement:** `make down` command to stop the stack.
- **Requirement:** `make logs` command to follow logs.
- **Requirement:** `make shell-api` command to enter the API container.
- **Requirement:** `make shell-db` command to access the database CLI.

### 2. Refactoring Tooling
The refactoring process should be automatable.
- **Requirement:** `make refactor` command to execute the backend refactoring script.

## Scenarios

### Scenario: Starting the Environment
- **WHEN** a developer runs `make up`
- **THEN** all containers (api, worker, scraper, db, redis, mq, nginx, frontend) should start.
