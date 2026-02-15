import React, { useState } from 'react';
import { Form, Input, message } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import { motion } from 'framer-motion';
import { useAuthStore } from '../../shared/stores/authStore';
import { useNavigate, useLocation } from 'react-router-dom';
import { BackgroundBlobs } from '../../components/ui/BackgroundBlobs';

const LoginPage: React.FC = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const login = useAuthStore((state) => state.login);
    const [loading, setLoading] = useState(false);

    const onFinish = async (values: any) => {
        setLoading(true);
        try {
            await login(values);
            message.success('登录成功');
            const from = (location.state as any)?.from?.pathname || '/dashboard';
            navigate(from, { replace: true });
        } catch (error) {
            message.error('登录失败：' + (error as Error).message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div
            style={{
                position: 'relative',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                width: '100vw',
                height: '100vh',
                overflow: 'hidden',
                background: '#0F172A',
            }}
        >
            <BackgroundBlobs />

            <motion.div
                initial={{ y: 24, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ duration: 0.6, ease: 'easeOut' }}
                className="login-glass-card"
                style={{
                    position: 'relative',
                    zIndex: 10,
                    width: '100%',
                    maxWidth: 400,
                    margin: '0 auto',
                    padding: '40px 36px 32px',
                    borderRadius: 20,
                    background: 'rgba(255, 255, 255, 0.06)',
                    backdropFilter: 'blur(24px)',
                    WebkitBackdropFilter: 'blur(24px)',
                    border: '1px solid rgba(255, 255, 255, 0.12)',
                    boxShadow: '0 8px 40px rgba(0, 0, 0, 0.3), 0 0 80px rgba(99, 102, 241, 0.08)',
                }}
            >
                {/* Header */}
                <div style={{ textAlign: 'center', marginBottom: 32 }}>
                    <h1
                        style={{
                            fontSize: 32,
                            fontWeight: 700,
                            letterSpacing: 2,
                            margin: 0,
                            background: 'linear-gradient(135deg, #fff 30%, #22d3ee 100%)',
                            WebkitBackgroundClip: 'text',
                            WebkitTextFillColor: 'transparent',
                        }}
                    >
                        SoulGravity
                    </h1>
                    <p style={{ fontSize: 14, letterSpacing: 6, color: 'rgba(255,255,255,0.5)', margin: '4px 0 0' }}>
                        灵犀 · 心引力
                    </p>
                    <p style={{ fontSize: 11, color: 'rgba(255,255,255,0.25)', margin: '12px 0 0' }}>
                        企业级多平台社交媒体矩阵管理系统
                    </p>
                </div>

                {/* Form */}
                <Form
                    name="login"
                    onFinish={onFinish}
                    layout="vertical"
                    size="large"
                    autoComplete="off"
                >
                    <Form.Item
                        name="username"
                        rules={[
                            { required: true, message: '请输入用户名' },
                        ]}
                        style={{ marginBottom: 16 }}
                    >
                        <Input
                            prefix={<UserOutlined />}
                            placeholder="用户名"
                            autoComplete="username"
                        />
                    </Form.Item>

                    <Form.Item
                        name="password"
                        rules={[{ required: true, message: '请输入密码' }]}
                        style={{ marginBottom: 24 }}
                    >
                        <Input.Password
                            prefix={<LockOutlined />}
                            placeholder="密码"
                            autoComplete="current-password"
                        />
                    </Form.Item>

                    <Form.Item style={{ marginBottom: 0 }}>
                        <button
                            type="submit"
                            disabled={loading}
                            style={{
                                width: '100%',
                                height: 46,
                                border: 'none',
                                borderRadius: 12,
                                background: 'linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #a855f7 100%)',
                                color: '#fff',
                                fontSize: 16,
                                fontWeight: 600,
                                letterSpacing: 4,
                                cursor: loading ? 'not-allowed' : 'pointer',
                                opacity: loading ? 0.7 : 1,
                                boxShadow: '0 4px 24px rgba(99, 102, 241, 0.35)',
                                transition: 'all 0.3s ease',
                            }}
                            onMouseOver={(e) => {
                                e.currentTarget.style.transform = 'scale(1.02)';
                                e.currentTarget.style.boxShadow = '0 6px 30px rgba(99, 102, 241, 0.5)';
                            }}
                            onMouseOut={(e) => {
                                e.currentTarget.style.transform = 'scale(1)';
                                e.currentTarget.style.boxShadow = '0 4px 24px rgba(99, 102, 241, 0.35)';
                            }}
                        >
                            {loading ? '登录中...' : '登 录'}
                        </button>
                    </Form.Item>
                </Form>
            </motion.div>

            {/* Footer */}
            <div
                style={{
                    position: 'absolute',
                    bottom: 24,
                    width: '100%',
                    textAlign: 'center',
                    fontSize: 11,
                    color: 'rgba(255,255,255,0.12)',
                    zIndex: 10,
                }}
            >
                &copy; 2026 SoulGravity Enterprise
            </div>
        </div>
    );
};

export default LoginPage;
