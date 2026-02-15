## Context
We need to connect the `GlassLayout` sidebar to the actual application routes. Currently, the menu items are hardcoded in the layout component, and the routes are minimal. We need a Scalable way to manage navigation.

## Goals / Non-Goals
**Goals:**
- Centralize menu configuration in `src/config/menu.tsx`.
- Implement `Dashboard`, `Plugins > Xiaohongshu`, and `Settings` navigation items.
- Ensure correct routing and redirects in `App.tsx`.
- Use correct Ant Design icons (`DashboardOutlined`, `FireOutlined`, `SettingOutlined`).

**Non-Goals:**
- Dynamic menu generation from backend (loading from API is out of scope for now).
- Role-based menu filtering (everyone sees the same menu for now).

## Decisions
1.  **Configuration Object**:
    - We will export a `menuConfig` object from `src/config/menu.tsx` that matches the `ProLayout` `route` prop structure (`path`, `name`, `icon`, `routes`).
    - This keeps the layout component clean and separates data from presentation.
2.  **Icon Handling**:
    - Icons will be imported directly in the config file.
3.  **Route Structure**:
    - `/dashboard`: Main landing page after login.
    - `/plugins`: Parent route for plugins.
    - `/plugins/xiaohongshu`: Specific plugin route.
    - `/settings`: Settings page.

## Risks / Trade-offs
-   **Static Config**: Hardcoding the menu means we need to redeploy to change it. This is acceptable for the early stage.
