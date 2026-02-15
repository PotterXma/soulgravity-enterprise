## Context
We need to localize the Web Console to Simplified Chinese and significantly enhance the visual aesthetics. The current UI is functional but lacks the desired "premium" feel.

## Goals / Non-Goals
**Goals:**
- Replace all English text with Simplified Chinese.
- Implement "premium" glassmorphism with deeper blurs, subtle gradients, and refined borders.
- Improve `LoginPage` layout and typography.
- Update `GlassLayout` transparency and sidebar styling.

**Non-Goals:**
- Implementation of a full i18n framework (react-i18next etc.) - we will hardcode Chinese for now as requested for the specific target audience.
- Dark/Light mode toggle (focus on the specific "Ethereal Nebula" dark theme).

## Decisions
1.  **Hardcoded Localization**:
    - We will directly modify the React components (`LoginPage.tsx`, `menu.tsx`, `App.tsx`, `GlassLayout.tsx`) to use Chinese strings. This is the fastest way to meet the requirement without introducing new dependencies.
2.  **Glassmorphism Style**:
    - **Blur**: Increase `backdrop-filter: blur()` from ~10px to `20px` or `40px` for a smoother look.
    - **Border**: Use highly transparent white borders (`rgba(255,255,255,0.08)`) instead of solid lines.
    - **Shadows**: Add `box-shadow` to floating elements (like the login card) to create depth.
    - **Gradients**: Use subtle linear gradients for backgrounds to avoid a "flat" look.

## Risks / Trade-offs
-   **Hardcoding**: Hardcoding strings makes future multi-language support harder, but it aligns with the immediate goal of a dedicated Chinese interface.
