# Specification: Data Seeding

## Requirements

### 1. Robust Seeding Script
A script `scripts/seed.py` must populate initial data without duplicating or erroring on re-runs.
- **Requirement:** Connect to the database using `libs.infra_db.session`.
- **Requirement:** Check if "System" Tenant exists; create if missing.
- **Requirement:** Check if "admin@soulgravity.com" User exists; create if missing with a hashed password (default: `Admin@123`).
- **Requirement:** Print credentials to stdout upon successful creation or verification.

## Scenarios

### Scenario: First Run
- **WHEN** the script is run on an empty database
- **THEN** it creates the Tenant and User and prints credentials.

### Scenario: Re-run
- **WHEN** the script is run on a populated database
- **THEN** it finds existing records, does not duplicate them, and prints credentials.
