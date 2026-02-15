import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { ConfigProvider, theme } from 'antd'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ConfigProvider
      theme={{
        algorithm: theme.darkAlgorithm,
        token: {
          colorPrimary: '#6366F1',
          colorBgContainer: 'transparent',
          colorBgElevated: 'rgba(15, 23, 42, 0.9)',
          colorBgLayout: 'transparent',
          colorBorder: 'rgba(255, 255, 255, 0.08)',
          colorText: 'rgba(255, 255, 255, 0.85)',
          colorTextSecondary: 'rgba(255, 255, 255, 0.45)',
          borderRadius: 12,
          fontFamily: 'Inter, system-ui, Avenir, Helvetica, Arial, sans-serif',
        },
        components: {
          Layout: {
            bodyBg: 'transparent',
            headerBg: 'transparent',
            siderBg: 'transparent',
          },
          Menu: {
            darkItemBg: 'transparent',
            darkSubMenuItemBg: 'transparent',
            darkItemSelectedBg: 'rgba(99, 102, 241, 0.15)',
            darkItemSelectedColor: '#a5b4fc',
            darkItemColor: 'rgba(255, 255, 255, 0.55)',
            darkItemHoverColor: 'rgba(255, 255, 255, 0.85)',
            darkItemHoverBg: 'rgba(255, 255, 255, 0.04)',
          },
          Button: {
            colorBgContainer: 'rgba(255, 255, 255, 0.06)',
            colorBorder: 'rgba(255, 255, 255, 0.1)',
          },
          Dropdown: {
            colorBgElevated: 'rgba(15, 23, 42, 0.95)',
          },
        },
      }}
    >
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </ConfigProvider>
  </React.StrictMode>,
)
