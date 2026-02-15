import React from 'react';
import {
    DashboardOutlined,
    FireOutlined,
    SettingOutlined,
} from '@ant-design/icons';

// Type definition compatible with ProLayout route.routes
export interface MenuItem {
    path?: string;
    name?: string;
    icon?: React.ReactNode;
    routes?: MenuItem[];
}

export const menuConfig: MenuItem[] = [
    {
        path: '/dashboard',
        name: '仪表盘',
        icon: <DashboardOutlined />,
    },
    {
        name: '平台插件',
        icon: null,
        routes: [
            {
                path: '/plugins/xiaohongshu',
                name: '小红书自动化',
                icon: <FireOutlined />,
            },
        ],
    },
    {
        path: '/settings',
        name: '系统设置',
        icon: <SettingOutlined />,
    },
];
