# Proposal: Wire Up Navigation Menu and Routes

## Goal
Wire up the **Navigation Menu** and **Application Routes** to connect the "GlassLayout" shell with the actual application features. This establishes the primary navigation structure and ensures users can access key areas like Dashboard, Plugins, and Settings.

## Why
Currently, `GlassLayout` has hardcoded/placeholder routes, causing navigation to be non-functional or misleading. To make the Web Console usable, we need a centralized menu configuration and properly defined routes that render the correct components.

## What Changes

### Frontend (Web Console)
- Create `src/config/menu.tsx` to define the navigation structure (Dashboard, Plugins/Xiaohongshu, Settings).
- Update `src/App.tsx` to:
    - Wrap routes with `ProtectedRoute` and `GlassLayout`.
    - Define authentic routes (`/dashboard`, `/plugins/xiaohongshu`, `/settings`).
    - Implement redirects (e.g., `/` -> `/dashboard`).

## Capabilities

### New Capabilities
- `navigation-system`: The centralized configuration and routing logic that connects the UI shell to application features, enabling user navigation.

## Impact
- **System**: `web-console`
- **Users**: All authenticated users.
