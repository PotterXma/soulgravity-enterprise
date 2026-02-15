## ADDED Requirements

### Requirement: Navigation Menu Structure
The centralized menu configuration must support nested items and icons.

#### Scenario: Menu Definition
- **WHEN** the layout requests the menu data
- **THEN** provide a structure with "Dashboard", "Platform Plugins" (Group), "Xiaohongshu", and "Settings"
- **THEN** associated icons (`DashboardOutlined`, `FireOutlined`, `SettingOutlined`) must be included

### Requirement: Route Definitions & Redirects
The application must correctly route URLs to the appropriate feature components.

#### Scenario: Root Access
- **WHEN** user visits `/`
- **THEN** redirect to `/dashboard`

#### Scenario: Dashboard Access
- **WHEN** user visits `/dashboard`
- **THEN** render the "Welcome" dashboard placeholder

#### Scenario: Xiaohongshu Config Access
- **WHEN** user visits `/plugins/xiaohongshu`
- **THEN** render the `XhsConfigForm` component

#### Scenario: Settings Access
- **WHEN** user visits `/settings`
- **THEN** render a placeholder Settings page
