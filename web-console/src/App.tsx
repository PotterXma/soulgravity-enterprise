import React, { lazy, Suspense } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './features/auth/LoginPage';
import { ProtectedRoute } from './components/auth/ProtectedRoute';
import { GlassLayout } from './layouts/GlassLayout';
import { BackgroundBlobs } from './components/ui/BackgroundBlobs';

const XhsScraperConsole = lazy(() => import('./features/plugins/xiaohongshu/XhsScraperConsole'));
const TacticalDashboard = lazy(() => import('./features/dashboard/TacticalDashboard'));

const App: React.FC = () => {
  return (
    <>
      <BackgroundBlobs />
      <Routes>
        <Route path="/login" element={<LoginPage />} />

        {/* Protected Routes wrapped in GlassLayout */}
        <Route element={<ProtectedRoute />}>
          <Route element={<GlassLayout />}>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route
              path="/dashboard"
              element={
                <Suspense fallback={<div style={{ color: 'rgba(255,255,255,0.3)', padding: 40 }}>加载中...</div>}>
                  <TacticalDashboard />
                </Suspense>
              }
            />
            <Route path="/plugins">
              <Route
                path="xiaohongshu"
                element={
                  <Suspense fallback={<div style={{ color: 'rgba(255,255,255,0.3)', padding: 40 }}>加载中...</div>}>
                    <XhsScraperConsole />
                  </Suspense>
                }
              />
            </Route>
            <Route
              path="/settings"
              element={
                <div>
                  <h1 className="text-2xl font-bold text-white mb-4">系统设置</h1>
                  <div className="glass-panel p-6 rounded-lg text-white/80">
                    <p>系统全局设置。</p>
                  </div>
                </div>
              }
            />
          </Route>
        </Route>

        {/* Fallback Redirect */}
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </>
  );
};

export default App;
