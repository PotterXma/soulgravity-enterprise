## ADDED Requirements

### Requirement: Premium Glassmorphism
The UI must implement advanced glassmorphism effects to achieve a "stunning" look.

#### Scenario: Layout Transparency
- **WHEN** the `GlassLayout` sidebar and header are rendered
- **THEN** increase backdrop-filter blur to `20px` (or optimal value)
- **THEN** use a subtle white gradient overlay (linear-gradient) for depth
- **THEN** ensure borders are extremely subtle (`rgba(255,255,255,0.08)`)

#### Scenario: Login Card Polish
- **WHEN** the login card appears
- **THEN** it must have a strong shadow (`box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37)`)
- **THEN** border radius should be smooth and large (`rounded-2xl`)
- **THEN** input fields should blend seamlessly with the glass effect

### Requirement: Typography & Spacing
Typography must be modern, readable, and consistent.

#### Scenario: Global Font
- **WHEN** any text is rendered
- **THEN** use a font stack that prioritizes clean sans-serif fonts suitable for UI (e.g., Inter, system-ui)
- **THEN** ensure good contrast against the potentially busy background
