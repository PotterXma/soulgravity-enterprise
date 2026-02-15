## Context
The current `web-console` lacks a dedicated login page. Authentication state exists (`useAuthStore`) but there is no UI to trigger it. We need a visually impressive entry point that aligns with the "Ethereal Nebula" design system.

## Goals / Non-Goals
**Goals:**
- Implement `LoginPage.tsx` with Glassmorphism aesthetics.
- Integrate with `useAuthStore` for real authentication.
- Provide visual feedback (loading state, toasts).
- Ensure responsiveness and smooth entrance animations.

**Non-Goals:**
- Implementing "Forgot Password" or "Sign Up" flows (these are future scope).
- Social login integration (scope is email/password only for now).

## Decisions
1. **Component Structure**:
   - `LoginPage` will be a standalone page in `src/features/auth/`.
   - It will use a `Layout` wrapper (or just `BackgroundBlobs`) to ensure the background is consistent.
   - The form will be built using Ant Design's `Form` component for validation, but styled with Tailwind to override default looks.
2. **Styling Strategy**:
   - Use Tailwind utility classes for layout and spacing.
   - Use custom CSS classes (e.g., `.glass-panel`, `.glass-input`) defined in `index.css` or inline styles via Tailwind `backdrop-blur` utilities to achieve the glass effect.
   - Override Ant Design variables/classes where necessary to remove default white backgrounds.
3. **State Management**:
   - Local state for form inputs is sufficient; global auth state is handled by `useAuthStore`.
   - `framer-motion` will handle the initial mount animation (`y` and `opacity`).

## Risks / Trade-offs
- **Performance**: High-resolution mesh gradients or complex animations might cause jank on lower-end devices. We will trust `framer-motion`'s optimizations and keep the blob count reasonable.
- **Accessibility**: Glassmorphism can have poor contrast. We must ensure text colors (white) have sufficient contrast against the background and inputs have clear focus states.
