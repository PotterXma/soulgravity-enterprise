# Specification: Ethereal Nebula Design System

## Requirements

### 1. Color Palette (Brand Identity)
- **Requirement:** Implement `soul-indigo` (#6366F1), `soul-cyan` (#06B6D4), `soul-violet` (#8B5CF6).
- **Requirement:** Implement `deep-space` (#0F172A) and `glass-white` (rgba(255, 255, 255, 0.7)).

### 2. Tailwind Configuration (`tailwind.config.js`)
- **Requirement:** Extend colors with the brand palette.
- **Requirement:** Add `blob` animation (infinite floating).
- **Requirement:** Add `fade-in-up` animation.
- **Requirement:** Add `.glass-panel` utility class.

### 3. Global Atmosphere (`index.css`)
- **Requirement:** Body background must use a mesh gradient strategy.
- **Requirement:** Implement `.animated-mesh-gradient` with 3 floating blobs (Indigo, Cyan, Violet).

### 4. Ant Design Theme (`glassTheme.ts`)
- **Requirement:** Override `colorPrimary` to Soul Indigo.
- **Requirement:** Set `colorBgContainer` and `colorBgLayout` to `transparent`.
- **Requirement:** Customize Table, Card, and Input components for glass effect.

### 5. Background Component
- **Requirement:** Create `BackgroundBlobs.tsx` to render the animated mesh gradient.

## Scenarios
### Scenario: Dashboard Rendering
- **WHEN** a user opens the web console
- **THEN** they should see a dark/deep-space background with slowly moving vivid blobs and glassmorphic panels.
