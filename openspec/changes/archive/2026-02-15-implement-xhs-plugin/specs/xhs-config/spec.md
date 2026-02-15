# Capability: Xiaohongshu Configuration (xhs-config)

## ADDED Requirements

### Requirement: Plugin Configuration Schema
The system must support a dedicated configuration schema for Xiaohongshu accounts, versioned for backward compatibility.

#### Scenario: Define Configuration Structure
- **WHEN** a new plugin configuration is created
- **THEN** it must validate against a strict Pydantic model containing:
    - `cookie` (string, required, min 20 chars)
    - `user_agent` (string, required)
    - `proxy_url` (string, optional)
    - `proxy_type` (enum: sticky, random)
    - `version` (int, default=1)

### Requirement: Secure Cookie Storage
Sensitive authentication data (cookies) must never be stored in plaintext.

#### Scenario: Encrypt on Save
- **WHEN** the `cookie` field is saved to the database
- **THEN** it must be encrypted using Fernet symmetric encryption.

#### Scenario: Decrypt on Load
- **WHEN** the adapter is initialized with a tenant's configuration
- **THEN** the `cookie` must be decrypted in memory for immediate use.

### Requirement: Connection Health Check
The system must verify the validity of the provided credentials before saving or running tasks.

#### Scenario: Test Connection
- **WHEN** the "Test Connection" action is triggered
- **THEN** the system must make a real HTTP request to Xiaohongshu's user profile API.
- **AND** return structured health data: `is_valid` (bool), `message` (str), `nickname` (str, optional).
- **AND** fail if the response is 403 or redirects to login.
