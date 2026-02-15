# Capability: Xiaohongshu Publisher (xhs-publisher)

## ADDED Requirements

### Requirement: Note Publishing
The system must allow users to publish content (images or videos) to Xiaohongshu.

#### Scenario: Publish with Media
- **WHEN** a publish task is executed
- **THEN** it must first upload all media assets (images/video) to Xiaohongshu's OSS.
- **AND** use the returned asset IDs to create the note.
- **AND** support tagging with topics (hashtags).

### Requirement: Reliability (Retry Mechanism)
Publishing is a critical operation that must be resilient to transient network failures.

#### Scenario: Transient Failure Recovery
- **WHEN** a publish attempt fails due to a network error or server error (5xx)
- **THEN** the system must automatically retry the operation up to 3 times.
- **AND** apply exponential backoff (e.g., 2s, 4s, 8s) between attempts.
- **AND** mark the task as 'failed' only after all retries are exhausted.

### Requirement: Asynchronous Processing
Publishing can take time (media upload) and should not block the user interface.

#### Scenario: Queueing
- **WHEN** a publish request is received via the API
- **THEN** it must be acknowledged immediately (HTTP 202 Accepted).
- **AND** the actual processing must be offloaded to a background worker queue (Celery).
