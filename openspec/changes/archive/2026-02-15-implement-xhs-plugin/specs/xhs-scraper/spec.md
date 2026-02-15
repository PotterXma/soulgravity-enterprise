# Capability: Xiaohongshu Scraper (xhs-scraper)

## ADDED Requirements

### Requirement: Keyword-Based Data Scraping
The system must be able to search for keywords on Xiaohongshu and extract note metadata.

#### Scenario: Fetch Hot Trends
- **WHEN** a scrape task is triggered with a keyword like "AI Tools"
- **THEN** the adapter must use the search API to fetch results.
- **AND** parse the response into a standardized list of `TrendItem` objects.
- **AND** include fields: `title`, `author`, `likes`, `comments`, `url`.

### Requirement: Anti-Detect Behavior
To avoid platform bans, the scraper must mimic human behavior.

#### Scenario: Request Throttling and Randomization
- **WHEN** multiple requests are made in sequence
- **THEN** the system must insert a random sleep interval (2-5 seconds) between them.
- **AND** requests must use a valid, rotating User-Agent string.
- **AND** requests may be routed through a proxy if configured.

### Requirement: Rate Limiting
The system must prevent overwhelming the target platform or local resources.

#### Scenario: Concurrent Task limit
- **WHEN** multiple scrape tasks are scheduled for the same tenant
- **THEN** the system must limit execution to a maximum of 5 concurrent scrapes.
- **AND** queue remaining tasks until a slot becomes available.
