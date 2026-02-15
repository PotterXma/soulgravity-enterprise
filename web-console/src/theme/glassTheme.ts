import { type ThemeConfig, theme } from 'antd';

export const glassTheme: ThemeConfig = {
    algorithm: theme.defaultAlgorithm,
    token: {
        colorPrimary: '#6366F1', // Soul Indigo
        colorInfo: '#06B6D4',    // Soul Cyan

        // Glassmorphism Bases
        colorBgContainer: 'transparent',
        colorBgLayout: 'transparent',
        colorBgElevated: 'rgba(255, 255, 255, 0.8)', // For Dropdowns/Modals

        fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        borderRadius: 12,
    },
    components: {
        Table: {
            headerBg: 'rgba(255, 255, 255, 0.5)',
            headerColor: '#1e293b', // Slate-800
            rowHoverBg: 'rgba(99, 102, 241, 0.1)', // Soul Indigo Tint
            colorBgContainer: 'transparent',
        },
        Card: {
            headerBg: 'transparent',
            colorBgContainer: 'rgba(255, 255, 255, 0.6)',
            // We often use custom class .glass-panel instead of generic Card styles, 
            // but this ensures default cards blend in.
        },
        Input: {
            colorBgContainer: 'rgba(255, 255, 255, 0.4)',
            activeBorderColor: '#6366F1',
            hoverBorderColor: '#8B5CF6',
        },
        Button: {
            fontWeight: 500,
            defaultShadow: '0 2px 0 rgba(0, 0, 0, 0.02)',
            primaryShadow: '0 2px 0 rgba(0, 0, 0, 0.04)',
        },
        Layout: {
            bodyBg: 'transparent',
            headerBg: 'transparent',
            siderBg: 'rgba(255, 255, 255, 0.4)', // Glass sidebar
        },
        Menu: {
            itemBg: 'transparent',
            subMenuItemBg: 'transparent',
            activeBarBorderWidth: 0,
            itemSelectedBg: 'rgba(99, 102, 241, 0.1)',
            itemSelectedColor: '#6366F1',
        }
    },
};
