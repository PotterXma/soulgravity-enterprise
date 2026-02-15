## 1. Dependencies
- [x] 1.1 Install `recharts` in web-console (`npm install recharts`)

## 2. TacticalDashboard Component
- [x] 2.1 Create `web-console/src/features/dashboard/TacticalDashboard.tsx`
  - Zone 1: 4 PulseMetric glass cards (Matrix Health w/ conditional glow, Scraping Velocity w/ sparkline, Pending Publish, Risk Meter)
  - Zone 2: AreaChart with gradient fill (#6366F1 → transparent), 24h X-axis
  - Zone 3: Account health monitor (scrollable glass strips, status dots, "修复" ghost button)
  - framer-motion stagger animation (80ms delay)
  - CSS Grid layout (65%/35%), responsive collapse at 1024px
  - All mock data hardcoded

## 3. Routing
- [x] 3.1 Wire `TacticalDashboard` into `App.tsx` at `/dashboard` route (replace placeholder)

## 4. Verification
- [x] 4.1 `npm run build` passes
- [ ] 4.2 Visual check in browser at `/dashboard`
