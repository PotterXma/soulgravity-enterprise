## ADDED Requirements

### Requirement: Security & Route Protection
The application must prevent unauthorized access to dashboard routes.

#### Scenario: Unauthenticated Access
- **WHEN** a user without a valid token accesses any path starting with `/` (except `/login`)
- **THEN** they must be redirected effectively to `/login`
- **THEN** the browser history should be replaced (prevent back navigation)

#### Scenario: Authenticated Access
- **WHEN** a logged-in user accesses a protected route
- **THEN** reference the `authStore` to validate the session
- **THEN** check hydratation status before rendering content (show spinner if hydrating)
- **THEN** render the requested page component (`<Outlet />`)

### Requirement: Glassmorphism Layout ("Hollow" Design)
The main layout must provide a persistent shell that integrates with the "Ethereal Nebula" background.

#### Scenario: Layout Rendering
- **WHEN** the dashboard loads
- **THEN** the layout container must be transparent to show the global `BackgroundBlobs`
- **THEN** render a fixed Sidebar with `siderWidth={240}`
- **THEN** render a fixed Header at the top
- **THEN** render the main content area with padding (`p-6`)

#### Scenario: Sidebar Styling
- **WHEN** the sidebar is visible
- **THEN** it must have a semi-transparent dark background (`rgba(15, 23, 42, 0.6)`)
- **THEN** it must have a right border (`rgba(255, 255, 255, 0.1)`)
- **THEN** navigation items must highlight with "Soul-Cyan" when active

#### Scenario: Header Styling & Actions
- **WHEN** the header is visible
- **THEN** it must be transparent or very low opacity blur
- **THEN** it must have a bottom border (`rgba(255, 255, 255, 0.1)`)
- **THEN** display the current user's name and avatar on the right
- **THEN** provide a Logout button that clears session and redirects to login
