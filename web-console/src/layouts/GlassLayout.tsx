import React from 'react';
import { ProLayout } from '@ant-design/pro-components';
import { Button, Dropdown } from 'antd';
import { LogoutOutlined, UserOutlined } from '@ant-design/icons';
import { useLocation, useNavigate, Outlet } from 'react-router-dom';
import { useAuthStore } from '../shared/stores/authStore';
import { menuConfig } from '../config/menu';

export const GlassLayout: React.FC = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const { user, logout } = useAuthStore();

    return (
        <div
            id="glass-layout"
            style={{
                height: '100vh',
                background: 'transparent',
            }}
        >
            <ProLayout
                location={location}
                title="SoulGravity"
                logo={null}
                siderWidth={240}
                layout="mix"
                splitMenus={false}
                fixedHeader
                fixSiderbar
                onMenuHeaderClick={() => navigate('/dashboard')}
                menuItemRender={(item: any, dom: React.ReactNode) => (
                    <div
                        onClick={() => {
                            if (item.path) navigate(item.path);
                        }}
                    >
                        {dom}
                    </div>
                )}
                route={{
                    path: '/',
                    routes: menuConfig,
                }}
                token={{
                    header: {
                        colorBgHeader: 'transparent', // Hollow Header
                        colorHeaderTitle: '#fff',
                        colorTextMenu: 'rgba(255,255,255,0.8)',
                        colorTextMenuSelected: '#22d3ee', // Soul Cyan
                        colorBgMenuItemSelected: 'rgba(34, 211, 238, 0.1)',
                    },
                    sider: {
                        colorMenuBackground: 'rgba(15, 23, 42, 0.4)', // More transparent
                        colorTextMenu: 'rgba(255,255,255,0.7)',
                        colorTextMenuTitle: 'rgba(255,255,255,0.9)',
                        colorTextMenuSelected: '#22d3ee',
                        colorBgMenuItemSelected: 'rgba(34, 211, 238, 0.1)',
                    },
                    pageContainer: {
                        colorBgPageContainer: 'transparent',
                    }
                }}
                // Styling overrides for glass effect
                bgLayoutImgList={[]}
                style={{
                    background: 'transparent',
                }}
                headerContentRender={() => (
                    // Custom Header Styles if needed
                    <div />
                )}
                rightContentRender={() => (
                    <Dropdown
                        menu={{
                            items: [
                                {
                                    key: 'logout',
                                    icon: <LogoutOutlined />,
                                    label: '退出登录',
                                    onClick: () => {
                                        logout();
                                        navigate('/login');
                                    },
                                },
                            ],
                        }}
                    >
                        <Button type="text" className="text-white hover:bg-white/10">
                            <UserOutlined /> {user?.name || '管理员'}
                        </Button>
                    </Dropdown>
                )}
            >
                <div className="p-6">
                    <Outlet />
                </div>
            </ProLayout>
            <style>{`
                /* Glass Layout Overrides — Dark Mode */
                .ant-pro-sider,
                .ant-pro-sider .ant-layout-sider,
                .ant-layout-sider {
                     backdrop-filter: blur(30px) saturate(120%);
                     -webkit-backdrop-filter: blur(30px) saturate(120%);
                     border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
                     background: rgba(10, 15, 30, 0.82) !important;
                }
                .ant-pro-global-header {
                    backdrop-filter: blur(24px) saturate(120%);
                     -webkit-backdrop-filter: blur(24px) saturate(120%);
                    border-bottom: 1px solid rgba(255, 255, 255, 0.06) !important;
                    background: rgba(10, 15, 30, 0.78) !important;
                }
                .ant-layout,
                .ant-layout-content,
                .ant-pro-layout-content,
                .ant-pro-layout-bg-list {
                    background: transparent !important;
                }
                /* Kill any remaining white backgrounds from antd */
                .ant-pro-sider-menu-container,
                .ant-pro-base-menu,
                .ant-menu-dark,
                .ant-menu-dark .ant-menu-sub {
                    background: transparent !important;
                }
                /* ProLayout logo area */
                .ant-pro-sider-logo {
                    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
                }
                /* Fix any antd popover/dropdown bg */
                .ant-dropdown,
                .ant-dropdown-menu {
                    background: rgba(10, 15, 30, 0.95) !important;
                    border: 1px solid rgba(255,255,255,0.08) !important;
                    backdrop-filter: blur(20px) !important;
                }
            `}</style>
        </div>
    );
};
