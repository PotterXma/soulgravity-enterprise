# Rebuild Dashboard as Tactical Command Center

## Why
The current dashboard uses generic admin charts that provide no operational value. Social media operators need answers to 3 questions: "Are my accounts safe?", "Is the bot running?", "What did I get today?". The dashboard should function as a **Tactical Command Center**, not a BI report.

## What Changes

### [MODIFY] `web-console/src/App.tsx`
- Replace inline Dashboard placeholder with new `TacticalDashboard` component.

### [NEW] `web-console/src/features/dashboard/TacticalDashboard.tsx`
- Full dashboard with 3 zones, mock data, recharts integration, framer-motion staggered entrance.

### [NEW] `web-console/package.json` (dependency)
- Add `recharts` for sparklines and area chart.

## Capabilities
- `tactical-dashboard`: The 3-zone dashboard (Pulse metrics, Battlefield chart, Action Center health monitor)

## Impact
- **Visual:** Dashboard goes from "placeholder text" to a fully-realized tactical view.
- **Breaking:** None — replaces a placeholder `<div>`, no other components depend on it.
- **Dependencies:** Adds `recharts` to frontend.
