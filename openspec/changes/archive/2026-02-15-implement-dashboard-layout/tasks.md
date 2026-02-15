## 1. Components
- [ ] 1.1 Create `src/components/auth/ProtectedRoute.tsx` to handle authentication checks with `useAuthStore` and redirect unauthorized users.

## 2. Layouts
- [ ] 2.1 Create `src/layouts/GlassLayout.tsx` using `@ant-design/pro-components`. Implement the "Hollow" design, custom sidebar/header styles, and user actions (Logout).

## 3. Integration
- [x] 3.1 Update `src/App.tsx` to wrap dashboard routes with `ProtectedRoute` and `GlassLayout`.
- [x] 3.2 Verify authorized and unauthorized access scenarios.
