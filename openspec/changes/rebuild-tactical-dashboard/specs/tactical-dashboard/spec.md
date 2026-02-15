## ADDED Requirements

### Requirement: Zone 1 — Pulse Metrics
A row of 4 glass metric cards across the full width of the dashboard.

#### Scenario: Matrix Health
- **THEN** displays "32 / 35 Active" as a large number
- **THEN** if active < total, card has red/orange pulsing `box-shadow` glow
- **THEN** if all active, card has no warning glow

#### Scenario: Scraping Velocity
- **THEN** displays "1,240 Notes / Hour"
- **THEN** shows a mini sparkline (80×32px `LineChart`, no axes) with last-12-data-points trend
- **THEN** sparkline stroke color is `#22d3ee` (cyan)

#### Scenario: Pending Publish
- **THEN** displays "12 Tasks Queuing"
- **THEN** shows `ThunderboltOutlined` icon

#### Scenario: Risk Meter
- **THEN** displays "Safe" text with green shield icon
- **THEN** green glow on card when status is "Safe"

### Requirement: Zone 2 — Battlefield Chart
An area chart showing 24-hour scraping activity, occupying 65% width of the main content area.

#### Scenario: Chart Rendering
- **THEN** uses recharts `AreaChart` with gradient fill from `#6366F1` (indigo) to transparent
- **THEN** X-axis shows hours `00:00` to `23:00` (24 ticks)
- **THEN** Y-axis shows "Notes Scraped" count
- **THEN** tooltip shows exact count on hover
- **THEN** curve type is `monotone` for smooth appearance

#### Scenario: Glass Container
- **THEN** chart is wrapped in a `.glass-panel` card with title "数据采集趋势"

### Requirement: Zone 3 — Action Center
A scrollable account health monitor list, occupying 35% width, right sidebar.

#### Scenario: Account Health List
- **THEN** shows a scrollable list of "glass strip" rows inside a `.glass-panel` card
- **THEN** card title is "账号健康监控"
- **THEN** max-height is constrained, list scrolls vertically

#### Scenario: Account Strip — Active
- **GIVEN** an account with status "active"
- **THEN** shows 🟢 green dot, platform name, account handle, "Active" badge

#### Scenario: Account Strip — Cookie Expired
- **GIVEN** an account with status "error"
- **THEN** shows 🔴 red dot, platform name, account handle, "Cookie 过期" text
- **THEN** shows a ghost "修复" button on the right

#### Scenario: Account Strip — Proxy Slow
- **GIVEN** an account with status "warning"
- **THEN** shows 🟡 yellow dot, platform name, account handle, "代理缓慢" text

### Requirement: Animation
Staggered entrance animation for all cards on page load.

#### Scenario: Stagger
- **WHEN** dashboard mounts
- **THEN** each card fades in and slides up with 80ms delay between cards
- **THEN** uses `framer-motion` `motion.div` with `variants`

### Requirement: Responsive Layout
Dashboard adapts to smaller screens.

#### Scenario: Below 1024px
- **WHEN** viewport width < 1024px
- **THEN** main grid collapses to single column
- **THEN** chart and action center stack vertically
