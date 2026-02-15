## Context
Replacing the generic dashboard placeholder with a "Tactical Command Center" for social media operators. Single-file component with mock data, recharts, framer-motion animations, and the Ethereal Nebula glassmorphism design system.

## Decisions

### 1. Single-File Component
One file: `TacticalDashboard.tsx`. No splitting — the dashboard is one cohesive view with 3 zones. Mock data is co-located for now.

### 2. Layout: CSS Grid (not Flexbox)
```
grid-template-columns: 65% 35%
grid-template-rows: auto 1fr
```
- Row 1 spans full width: 4 metric cards (Zone 1 "Pulse")
- Row 2 left: Area chart (Zone 2 "Battlefield")  
- Row 2 right: Account health list (Zone 3 "Action Center")

### 3. Charts: recharts
- **Area Chart** (Zone 2): `<AreaChart>` with gradient fill from `#6366F1` to transparent. 24-hour X-axis. Linear curve type.
- **Mini Sparkline** (Zone 1, Scraping Velocity card): `<LineChart>` without axes — just the line. Tiny (80×32px).

### 4. Animation: framer-motion stagger
Cards use `motion.div` with `variants` for staggered entrance:
```
container: { staggerChildren: 0.08 }
item: { y: 20, opacity: 0 → y: 0, opacity: 1 }
```

### 5. Conditional Glow on Metrics
- Matrix Health < 100% → red/orange `box-shadow` pulse via CSS animation
- Risk Meter "Safe" → green glow, "Warning" → amber glow

### 6. Responsive Breakpoint
Below 1024px, grid collapses to single column (chart full-width, action center below).

## Component Architecture
```
TacticalDashboard
├── Zone 1: PulseMetrics (4 glass cards in a row)
│   ├── MatrixHealth (big number + conditional glow)
│   ├── ScrapingVelocity (number + mini sparkline)
│   ├── PendingPublish (number + icon)
│   └── RiskMeter (shield icon + status text)
├── Zone 2: BattlefieldChart (AreaChart with gradient)
└── Zone 3: ActionCenter (scrollable account health list)
    └── AccountStrip × N (status dot + name + action button)
```

## Risks
- **recharts bundle size**: ~45KB gzipped. Acceptable for dashboard.
- **Mock data**: Hardcoded. Future: connect to real API endpoints (`/api/v1/xhs/notes`, `/api/v1/xhs/scrape`).
