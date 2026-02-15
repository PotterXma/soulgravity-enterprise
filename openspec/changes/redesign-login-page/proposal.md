# Proposal: Redesign Login Page

## Goal
Completely redesign the login page to achieve a truly stunning glassmorphism UI with animated background blobs, frosted glass card, and premium visual effects.

## Why
The current login page is broken: Ant Design's `Card` component overrides all glassmorphism/Tailwind styles with its own opaque white background. The blob animation `@keyframes` are also missing from the CSS, so no animated background is visible.

## Root Causes
1. **`Card` component** forces white bg, ignoring `bg-white/10` and `backdrop-blur-xl` classes
2. **`@keyframes blob`** animation is referenced in `.blob` CSS class but never defined
3. **Ant Design's internal styles** (inputs, buttons) override Tailwind utility classes

## What Changes

### `src/features/auth/LoginPage.tsx`
- Remove Ant Design `Card` entirely — use a raw `<div>` with `.glass-panel` and `framer-motion` entry animation
- Use native `<input>` styling via CSS-in-JS or custom classes to avoid antd overrides
- Add gradient text for "SoulGravity" title (white → cyan)
- Use indigo-to-violet gradient button instead of antd `Button`

### `src/index.css`
- Add missing `@keyframes blob` animation for background blobs
- Add `.glass-input` and `.glass-button` utility classes that can't be overridden by antd

## Capabilities

### New Capabilities
- `login-redesign`: Complete visual overhaul of the login page

## Impact
- **System**: `web-console` — `LoginPage.tsx` and `index.css`
- **Users**: All users see the revamped login experience
