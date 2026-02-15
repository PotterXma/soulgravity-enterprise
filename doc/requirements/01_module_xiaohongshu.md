# 01. Module Requirements: Xiaohongshu Automation (小红书自动化)

| Metadata | Value |
| :--- | :--- |
| **Module ID** | MOD_01_XHS |
| **Name** | Xiaohongshu Automation |
| **Priority** | P0 (Critical) |
| **Status** | Draft |
| **Owner** | Product Team |

---

## 1. Overview & Goals (概述与目标)

### Core Value
赋能企业用户无需人工干预即可监控关键词并发布笔记到小红书平台。
**Enable enterprise users to monitor keywords and publish notes to Xiaohongshu without manual operation.**

### Scope
1.  **Account Configuration**: Cookie-based authentication.
2.  **Connection Testing**: Health check via user profile verification.
3.  **Data Scraping**: Keyword search and data extraction.
4.  **Note Publishing**: Image/Video note creation.

---

## 2. User Stories (用户故事)

### Configuration
> "As an Admin, I want to input my Cookie and Proxy, and click 'Test Connection' to see if my account is valid immediately."

### Data Scraping
> "As an Operator, I want to set up a periodic task to search for 'AI Tools' every hour and save top 50 notes."

### Reliability & Safety
> "As a System, I want to automatically pause tasks if the Cookie expires or 403 Forbidden is detected."

---

## 3. Functional Specifications (功能详述)

### 3.1 Configuration Management (配置管理)

#### Fields
| Field | Type | Description |
| :--- | :--- | :--- |
| `cookie` | Textarea (Encrypted) | The web session string. |
| `user_agent` | String | Custom UA string for fingerprinting. |
| `proxy_type` | Select | Sticky (Fixed IP) vs Random (Rotating Proxy). |

#### Logic
*   **Versioning**: Configuration schema must include `version: 1`.
*   **Validation**: The "Test Connection" action must verify the cookie by fetching the user's nickname and avatar before saving the configuration.

### 3.2 Data Scraper (数据采集)

#### Input
*   **Keywords**: List of search terms.
*   **Sort Type**: General (综合) or Latest (最新).
*   **Limit**: Number of items to scrape.

#### Output
JSON structure containing:
*   `note_id`
*   `title`
*   `likes_count`
*   `comments_count`
*   `author_info`

#### Anti-Detect
*   Must implement random sleep intervals (2-5s) between requests to mimic human behavior.

### 3.3 Note Publisher (内容发布)

#### Input
*   **Title**: Note title.
*   **Content**: Description text.
*   **Images/Video**: List of media assets.
*   **Topics**: Hash tags (#).

#### Logic
*   Support queuing mechanism.
*   If publishing fails, retry 3 times with exponential backoff.

---

## 4. Non-Functional Requirements (非功能需求)

*   **Performance**: Support concurrent scraping of 5 keywords per tenant.
*   **Reliability**: Cookie expiration must trigger a generic Alert via Webhook.
*   **Security**: Cookies must be stored encrypted (Fernet) in the database.

---

## 5. UI/UX Guidelines (界面交互)

### Style
Follow **"Ethereal Nebula"** Design System (Glassmorphism).

### Components
*   **Config Form**: Wrap in `GlassCard` container.
*   **Status Badge**: Use a Green dot for "Connected", Red dot for "Disconnected".
*   **Help Text**: Provide instructions: *"Press F12 -> Application -> Cookies -> Copy 'web_session'"*.
