## 1. CSS Foundation
- [x] 1.1 Add `@keyframes blob` animation to `src/index.css`
- [x] 1.2 Add `.login-glass-card` scoped overrides for antd inputs/buttons in `src/index.css`

## 2. LoginPage Component
- [x] 2.1 Rewrite `src/features/auth/LoginPage.tsx`:
  - Remove `Card` import and usage
  - Use `motion.div` with `.glass-panel` class
  - Add gradient text for title
  - Add gradient button styling
  - Keep Form validation logic unchanged

## 3. Verification
- [ ] 3.1 Build passes (`npm run build`)
- [ ] 3.2 Visual verification in browser
