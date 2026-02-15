## Context
The current login page uses Ant Design's `Card` component which forces an opaque white background, completely breaking the glassmorphism design. Additionally, the `@keyframes blob` animation is missing from the CSS.

## Goals / Non-Goals
**Goals:**
- Replace `Card` with a raw `<div>` using `.glass-panel` class
- Add missing `@keyframes blob` animation to `index.css`
- Override ant input/button styles with CSS `!important` rules
- Use `framer-motion` for entry animation
- Add gradient text for the title
- Use gradient button instead of flat antd button

**Non-Goals:**
- Changing authentication logic (stays the same)
- Replacing the Ant Design Form component (it provides validation; just override styles)

## Decisions
1. **Drop `Card`, keep `Form`**: The `Card` is the root cause of the white bg. `Form` is fine since it's invisible (no visual rendering). We'll use a raw `<div className="glass-panel">` instead.
2. **CSS `!important` overrides**: Ant Design uses very specific selectors. We'll add `.login-form .ant-input` overrides in `index.css` with `!important` to ensure glass styling wins.
3. **`framer-motion` animation**: Use `motion.div` for the card entrance (fade + slide up), matching the existing design system.
4. **Gradient text**: Use `bg-gradient-to-r from-white to-cyan-400 bg-clip-text text-transparent` for the "SoulGravity" title.

## Risks / Trade-offs
- Using `!important` is a smell, but necessary to override antd's inline styles. Scoped to `.login-form` to minimize blast radius.
