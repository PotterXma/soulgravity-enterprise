# Design: Ethereal Nebula Design System

## Component Design

### 1. Configuration (`web-console/tailwind.config.js`)
- **Responsibility**: Define design tokens (colors, animations) and utility classes.
- **Key Changes**: Extend `theme.extend.colors` and `theme.extend.animation`.

### 2. Global Styles (`web-console/src/index.css`)
- **Responsibility**: Applied global background and mesh gradient classes.
- **Key Changes**: CSS variables for colors (optional) and `.animated-mesh-gradient` implementation.

### 3. Theme Override (`web-console/src/theme/glassTheme.ts`)
- **Responsibility**: Bridge Ant Design with our custom palette and glass effect.
- **Key Changes**: `token` overrides for primary color and background transparency. `components` overrides for Input, Table, Card.

### 4. Visual Component (`web-console/src/components/ui/BackgroundBlobs.tsx`)
- **Responsibility**: Render the animated background elements.
- **Key Changes**: Functional component returning the div structure defined in `index.css`.

## Data Flow
N/A - Purely visual/frontend change.

## User Interface
- **Look & Feel**: Deep space background, glowing/floating blobs, glassmorphic containers.
