# Backend Refactoring Specification

## Requirements

### 1. Standardized Directory Naming
The project structure must use underscores for Python packages, replacing hyphens.
- **Requirement:** Rename `libs/core-kernel` to `libs/core_kernel`.
- **Requirement:** Rename `libs/infra-db` to `libs/infra_db`.
- **Requirement:** Rename `libs/infra-net` to `libs/infra_net`.

### 2. Telemetry Module Location
The telemetry module should reside in its own package for better organization.
- **Requirement:** Move `libs/core_kernel/telemetry.py` to `libs/telemetry/__init__.py`.

### 3. Import Statement Consistency
All import statements must match the new directory structure.
- **Requirement:** Update all imports referencing `libs.core-kernel`, `libs.infra-db`, and `libs.infra-net` to use underscores.
- **Requirement:** Update imports referencing `libs.core_kernel.telemetry` to `libs.telemetry`.

## Scenarios

### Scenario: Import Resolution
- **WHEN** the application starts
- **THEN** no `ModuleNotFoundError` should occur due to missing hyphenated packages.

### Scenario: Telemetry Usage
- **WHEN** a service logs using telemetry
- **THEN** it should import from `libs.telemetry` successfully.
