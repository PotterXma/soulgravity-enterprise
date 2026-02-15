## Context
The application needs a primary layout for authenticated users. We have a "Glassmorphism" design system ("Ethereal Nebula") established by the login page, but the dashboard currently lacks this structure. We also need to secure these routes.

## Goals / Non-Goals
**Goals:**
- Implement `GlassLayout` using `@ant-design/pro-components` (`ProLayout`).
- Create `ProtectedRoute` to guard dashboard routes.
- Achieve a "Hollow" layout effect where the background blobs are visible through the layout shell.
- Implement sidebar navigation and header actions (Logout).

**Non-Goals:**
- Implementing complex role-based access control (RBAC) at this stage (basic auth check only).
- Implementing breadcrumbs or complex page headers (keep it minimal).

## Decisions
1.  **Layout Library**:
    - Use `ProLayout` for rapid development of the sidebar and header structure.
    - Heavily override its default white/gray styles to achieve transparency.
2.  **"Hollow" Strategy**:
    - The `ProLayout` container will be set to `transparent`.
    - The global `BackgroundBlobs` (rendered in `App.tsx` or `GlassLayout`) will provide the visual backdrop.
    - Sidebar and Header will have semi-transparent backgrounds with blur filters (`backdrop-filter`) to ensure readability while maintaining the glass effect.
3.  **Routing**:
    - `GlassLayout` will wrap the authenticated routes.
    - `ProtectedRoute` will wrap `GlassLayout` (or be used within routes) to ensure only logged-in users can see the shell.
4.  **State**:
    - `useAuthStore` will be the source of truth for user data and authentication status.

## Risks / Trade-offs
-   **Style Overrides**: `ProLayout` allows extensive customization but sometimes requires deep CSS/Less overrides or `token` configuration. We will prioritize using the `token` prop for colors and `style` props for transparency to minimize fragile CSS selectors.
-   **Performance**: Blur effects can be costly. We will monitor rendering performance.
