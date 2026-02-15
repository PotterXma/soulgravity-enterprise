## ADDED Requirements

### Requirement: Full Chinese Localization
All user-facing text must be in Simplified Chinese (zh-CN).

#### Scenario: Login Page
- **WHEN** the login page loads
- **THEN** the title should be "SoulGravity 灵犀·心引力"
- **THEN** input placeholders should be "请输入邮箱" and "请输入密码"
- **THEN** the login button should read "登 录"

#### Scenario: Navigation Menu
- **WHEN** the sidebar renders
- **THEN** "Dashboard" should be "仪表盘"
- **THEN** "Platform Plugins" should be "平台插件"
- **THEN** "Xiaohongshu" should be "小红书自动化"
- **THEN** "Settings" should be "系统设置"

#### Scenario: User Actions
- **WHEN** the user menu is opened
- **THEN** "Logout" should be "退出登录"
- **THEN** "User" should be "管理员" (or valid name)

### Requirement: Dashboard Placeholders
Content in placeholder pages must be localized.

#### Scenario: Dashboard Content
- **WHEN** viewing the dashboard
- **THEN** the greeting should be "欢迎使用 SoulGravity 企业版"
- **THEN** the instruction should be "请从左侧菜单选择模块开始工作"
