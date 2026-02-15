import React from 'react';
import { motion } from 'framer-motion';
import {
    AreaChart,
    Area,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer,
    LineChart,
    Line,
} from 'recharts';
import {
    WarningOutlined,
    ThunderboltOutlined,
    SafetyCertificateOutlined,
    ExclamationCircleOutlined,
} from '@ant-design/icons';

/* ================================================================
 *  DESIGN TOKENS — synced from LoginPage.tsx
 *
 *  Glass bg   : rgba(255,255,255, 0.06)
 *  Glass border: rgba(255,255,255, 0.12)
 *  Blur       : 24px
 *  Radius     : 20px (cards) / 10px (inner elements)
 *  Heading    : linear-gradient(135deg, #fff 30%, #22d3ee 100%)
 *  Accent     : #6366F1 → #8B5CF6 → #a855f7
 *  Glow       : 0 8px 40px rgba(0,0,0,0.3), 0 0 80px rgba(99,102,241,0.08)
 *  Sub text   : rgba(255,255,255, 0.5)
 *  Muted text : rgba(255,255,255, 0.25)
 * ================================================================ */

/* ─── Mock Data ───────────────────────────────────────────────── */

const SPARKLINE = [
    { v: 820 }, { v: 932 }, { v: 1100 }, { v: 890 }, { v: 1240 },
    { v: 1050 }, { v: 1320 }, { v: 1180 }, { v: 1400 }, { v: 1100 },
    { v: 1350 }, { v: 1240 },
];

const HOURLY = Array.from({ length: 24 }, (_, i) => ({
    hour: `${String(i).padStart(2, '0')}:00`,
    notes: Math.floor(200 + Math.sin(i / 3) * 150 + Math.random() * 80 + (i > 8 && i < 22 ? 300 : 0)),
}));

interface Acct { platform: string; handle: string; status: 'active' | 'error' | 'warning'; detail: string; emoji: string; }
const ACCOUNTS: Acct[] = [
    { platform: '小红书', handle: '@DesignDaily', status: 'active', detail: '运行中', emoji: '🎨' },
    { platform: '小红书', handle: '@TechReview', status: 'error', detail: 'Cookie 过期', emoji: '💻' },
    { platform: '抖音', handle: '@FunnyCat', status: 'warning', detail: '代理缓慢', emoji: '🐱' },
    { platform: '小红书', handle: '@FoodieHub', status: 'active', detail: '运行中', emoji: '🍜' },
    { platform: '小红书', handle: '@TravelLog', status: 'active', detail: '运行中', emoji: '✈️' },
    { platform: '抖音', handle: '@GadgetPro', status: 'active', detail: '运行中', emoji: '📱' },
    { platform: '小红书', handle: '@BeautyQueen', status: 'error', detail: 'Cookie 过期', emoji: '💄' },
    { platform: '抖音', handle: '@DanceStar', status: 'active', detail: '运行中', emoji: '💃' },
];

/* ─── Animation ───────────────────────────────────────────────── */

const stagger = { hidden: {}, visible: { transition: { staggerChildren: 0.07 } } };
const fadeUp = {
    hidden: { y: 24, opacity: 0 },
    visible: { y: 0, opacity: 1, transition: { duration: 0.6, ease: 'easeOut' as const } },
};

/* ─── Shared Styles ───────────────────────────────────────────── */

const GLASS: React.CSSProperties = {
    background: 'rgba(255, 255, 255, 0.06)',
    backdropFilter: 'blur(24px)',
    WebkitBackdropFilter: 'blur(24px)',
    border: '1px solid rgba(255, 255, 255, 0.12)',
    borderRadius: 20,
    position: 'relative',
    overflow: 'hidden',
};

const GLOW = '0 8px 40px rgba(0, 0, 0, 0.3), 0 0 80px rgba(99, 102, 241, 0.08)';

/** Top-edge shimmer — same subtle highlight the login card gets from its border */
const Shimmer = () => (
    <div style={{
        position: 'absolute', top: 0, left: '10%', right: '10%', height: 1,
        background: 'linear-gradient(90deg, transparent, rgba(255,255,255,0.18), transparent)',
    }} />
);

const STATUS_CLR: Record<string, string> = { active: '#34d399', error: '#f87171', warning: '#fbbf24' };

/* ─── Tooltip (matching login glass aesthetic) ────────────────── */

const ChartTooltip = ({ active, payload, label }: any) => {
    if (!active || !payload?.length) return null;
    return (
        <div style={{
            ...GLASS,
            borderRadius: 10,
            padding: '10px 14px',
            boxShadow: '0 8px 32px rgba(0,0,0,0.45)',
        }}>
            <div style={{ fontSize: 11, color: 'rgba(255,255,255,0.4)' }}>{label}</div>
            <div style={{ fontSize: 14, fontWeight: 600, color: '#a5b4fc', marginTop: 2 }}>
                {payload[0].value.toLocaleString()} <span style={{ fontSize: 11, fontWeight: 400, color: 'rgba(255,255,255,0.35)' }}>笔记</span>
            </div>
        </div>
    );
};

/* ─── CSS Keyframes ───────────────────────────────────────────── */

const keyframes = `
@keyframes sg-ping { 0%,100%{transform:scale(1);opacity:.7}50%{transform:scale(2.4);opacity:0} }
@keyframes sg-pulse { 0%,100%{opacity:.55}50%{opacity:1} }
`;

/* ================================================================
 *  MAIN COMPONENT
 * ================================================================ */

const TacticalDashboard: React.FC = () => {
    const active = 32;
    const total = 35;
    const down = total - active;

    return (
        <>
            <style>{keyframes}</style>
            <motion.div variants={stagger} initial="hidden" animate="visible" style={{ minHeight: '100%' }}>

                {/* ═══ Header ═══ */}
                <motion.div variants={fadeUp} style={{ marginBottom: 32, display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end' }}>
                    <div>
                        <h1 style={{
                            fontSize: 28, fontWeight: 700, letterSpacing: 2, margin: 0,
                            /* Same gradient as login "SoulGravity" heading */
                            background: 'linear-gradient(135deg, #fff 30%, #22d3ee 100%)',
                            WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
                        }}>
                            战术指挥中心
                        </h1>
                        {/* Same style as login subtitle "灵犀 · 心引力" */}
                        <p style={{ fontSize: 13, letterSpacing: 4, color: 'rgba(255,255,255,0.5)', margin: '6px 0 0' }}>
                            实时矩阵运营态势感知
                        </p>
                    </div>
                    <div style={{
                        fontSize: 11, color: 'rgba(255,255,255,0.25)',
                        /* Same glass feel as login inputs */
                        padding: '6px 16px', borderRadius: 10,
                        background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)',
                    }}>
                        {new Date().toLocaleDateString('zh-CN', { month: 'long', day: 'numeric', weekday: 'long' })}
                    </div>
                </motion.div>

                {/* ═══ Zone 1 — Pulse Metrics ═══ */}
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>

                    {/* Matrix Health */}
                    <motion.div variants={fadeUp} style={{
                        ...GLASS, padding: '24px 28px',
                        boxShadow: down > 0
                            ? '0 0 50px rgba(248,113,113,0.12), inset 0 0 50px rgba(248,113,113,0.04)'
                            : GLOW,
                    }}>
                        <Shimmer />
                        <div style={{ fontSize: 11, color: 'rgba(255,255,255,0.5)', letterSpacing: 1, marginBottom: 14 }}>矩 阵 健 康</div>
                        <div style={{ display: 'flex', alignItems: 'baseline', gap: 6 }}>
                            <span style={{ fontSize: 40, fontWeight: 800, lineHeight: 1, fontVariantNumeric: 'tabular-nums', color: down > 0 ? '#f87171' : '#34d399' }}>
                                {active}
                            </span>
                            <span style={{ fontSize: 16, color: 'rgba(255,255,255,0.25)' }}>/ {total}</span>
                        </div>
                        {down > 0 && (
                            <div style={{
                                marginTop: 12, fontSize: 11, color: '#fbbf24',
                                display: 'flex', alignItems: 'center', gap: 5,
                                padding: '5px 12px', borderRadius: 10,
                                background: 'rgba(251,191,36,0.06)', border: '1px solid rgba(251,191,36,0.1)',
                            }}>
                                <ExclamationCircleOutlined style={{ fontSize: 11, animation: 'sg-pulse 2s infinite' }} /> {down} 账号需要关注
                            </div>
                        )}
                    </motion.div>

                    {/* Scraping Velocity */}
                    <motion.div variants={fadeUp} style={{ ...GLASS, padding: '24px 28px', boxShadow: GLOW }}>
                        <Shimmer />
                        <div style={{ fontSize: 11, color: 'rgba(255,255,255,0.5)', letterSpacing: 1, marginBottom: 14 }}>采 集 速 率</div>
                        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                            <div>
                                <span style={{ fontSize: 34, fontWeight: 800, lineHeight: 1, color: '#fff', fontVariantNumeric: 'tabular-nums' }}>1,240</span>
                                <div style={{ fontSize: 11, color: 'rgba(255,255,255,0.35)', marginTop: 4 }}>笔记/小时</div>
                            </div>
                            <div style={{ width: 76, height: 30 }}>
                                <ResponsiveContainer width="100%" height="100%">
                                    <LineChart data={SPARKLINE}>
                                        <defs>
                                            <linearGradient id="spk" x1="0" y1="0" x2="1" y2="0">
                                                <stop offset="0%" stopColor="#6366F1" />
                                                <stop offset="100%" stopColor="#22d3ee" />
                                            </linearGradient>
                                        </defs>
                                        <Line type="monotone" dataKey="v" stroke="url(#spk)" strokeWidth={2} dot={false} />
                                    </LineChart>
                                </ResponsiveContainer>
                            </div>
                        </div>
                    </motion.div>

                    {/* Pending Publish */}
                    <motion.div variants={fadeUp} style={{ ...GLASS, padding: '24px 28px', boxShadow: GLOW }}>
                        <Shimmer />
                        <div style={{ fontSize: 11, color: 'rgba(255,255,255,0.5)', letterSpacing: 1, marginBottom: 14 }}>待 发 布 任 务</div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
                            {/* Icon container — same border-radius as login inputs */}
                            <div style={{
                                width: 42, height: 42, borderRadius: 10,
                                background: 'rgba(167,139,250,0.08)', border: '1px solid rgba(167,139,250,0.12)',
                                display: 'flex', alignItems: 'center', justifyContent: 'center',
                            }}>
                                <ThunderboltOutlined style={{ fontSize: 18, color: '#a78bfa' }} />
                            </div>
                            <div>
                                <span style={{ fontSize: 34, fontWeight: 800, lineHeight: 1, color: '#fff', fontVariantNumeric: 'tabular-nums' }}>12</span>
                                <div style={{ fontSize: 11, color: 'rgba(255,255,255,0.35)', marginTop: 4 }}>排队中</div>
                            </div>
                        </div>
                    </motion.div>

                    {/* Risk Meter */}
                    <motion.div variants={fadeUp} style={{
                        ...GLASS, padding: '24px 28px',
                        boxShadow: '0 8px 40px rgba(0,0,0,0.3), 0 0 60px rgba(52,211,153,0.06)',
                    }}>
                        <Shimmer />
                        <div style={{ fontSize: 11, color: 'rgba(255,255,255,0.5)', letterSpacing: 1, marginBottom: 14 }}>风 险 评 估</div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
                            <div style={{
                                width: 42, height: 42, borderRadius: 10,
                                background: 'rgba(52,211,153,0.08)', border: '1px solid rgba(52,211,153,0.12)',
                                display: 'flex', alignItems: 'center', justifyContent: 'center',
                            }}>
                                <SafetyCertificateOutlined style={{ fontSize: 18, color: '#34d399' }} />
                            </div>
                            <div>
                                <span style={{ fontSize: 22, fontWeight: 700, color: '#34d399' }}>安全</span>
                                <div style={{ fontSize: 11, color: 'rgba(255,255,255,0.25)', marginTop: 2 }}>无异常风控</div>
                            </div>
                        </div>
                    </motion.div>
                </div>

                {/* ═══ Zone 2 + Zone 3 ═══ */}
                <div style={{ display: 'grid', gridTemplateColumns: '1.8fr 1fr', gap: 16 }}>

                    {/* Zone 2 — Trend Chart */}
                    <motion.div variants={fadeUp} style={{ ...GLASS, padding: '24px 24px 16px', boxShadow: GLOW }}>
                        <Shimmer />
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
                            <span style={{ fontSize: 14, fontWeight: 600, color: 'rgba(255,255,255,0.7)', letterSpacing: 1 }}>数据采集趋势</span>
                            <div style={{ display: 'flex', gap: 6 }}>
                                {['今日', '7天', '30天'].map((t, i) => (
                                    <button key={t} style={{
                                        padding: '4px 12px', borderRadius: 10, fontSize: 11, cursor: 'pointer',
                                        /* Same as login input style */
                                        border: '1px solid rgba(255,255,255,0.1)',
                                        background: i === 0 ? 'rgba(99,102,241,0.12)' : 'rgba(255,255,255,0.05)',
                                        color: i === 0 ? '#a5b4fc' : 'rgba(255,255,255,0.35)',
                                        transition: 'all 0.25s',
                                    }}>
                                        {t}
                                    </button>
                                ))}
                            </div>
                        </div>
                        <div style={{ width: '100%', height: 260 }}>
                            <ResponsiveContainer width="100%" height="100%">
                                <AreaChart data={HOURLY} margin={{ top: 4, right: 4, left: -20, bottom: 0 }}>
                                    <defs>
                                        <linearGradient id="areaBg" x1="0" y1="0" x2="0" y2="1">
                                            {/* Login button gradient colors repurposed */}
                                            <stop offset="0%" stopColor="#6366F1" stopOpacity={0.3} />
                                            <stop offset="60%" stopColor="#8B5CF6" stopOpacity={0.06} />
                                            <stop offset="100%" stopColor="#a855f7" stopOpacity={0} />
                                        </linearGradient>
                                    </defs>
                                    <XAxis dataKey="hour" stroke="transparent"
                                        tick={{ fontSize: 10, fill: 'rgba(255,255,255,0.2)' }}
                                        tickLine={false} axisLine={false} interval={3}
                                    />
                                    <YAxis stroke="transparent"
                                        tick={{ fontSize: 10, fill: 'rgba(255,255,255,0.15)' }}
                                        tickLine={false} axisLine={false}
                                    />
                                    <Tooltip content={<ChartTooltip />} />
                                    <Area type="monotone" dataKey="notes" stroke="#818cf8" strokeWidth={2} fill="url(#areaBg)" />
                                </AreaChart>
                            </ResponsiveContainer>
                        </div>
                    </motion.div>

                    {/* Zone 3 — Account Health */}
                    <motion.div variants={fadeUp} style={{ ...GLASS, padding: '24px 20px', display: 'flex', flexDirection: 'column', boxShadow: GLOW }}>
                        <Shimmer />
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 18 }}>
                            <span style={{ fontSize: 14, fontWeight: 600, color: 'rgba(255,255,255,0.7)', letterSpacing: 1 }}>账号健康监控</span>
                            <span style={{ fontSize: 11, color: 'rgba(255,255,255,0.25)' }}>{ACCOUNTS.length} 个</span>
                        </div>
                        <div style={{ flex: 1, overflow: 'auto', display: 'flex', flexDirection: 'column', gap: 6, maxHeight: 300 }}>
                            {ACCOUNTS.map((a, i) => (
                                <motion.div
                                    key={i} variants={fadeUp}
                                    whileHover={{ scale: 1.01, backgroundColor: 'rgba(255,255,255,0.06)' }}
                                    style={{
                                        display: 'flex', alignItems: 'center', gap: 10,
                                        padding: '10px 14px', borderRadius: 10,
                                        /* Same bg as login inputs */
                                        background: 'rgba(255,255,255,0.05)',
                                        border: '1px solid rgba(255,255,255,0.1)',
                                        cursor: 'default', transition: 'all 0.25s',
                                    }}
                                >
                                    {/* Emoji avatar */}
                                    <div style={{
                                        width: 32, height: 32, borderRadius: 10,
                                        background: 'rgba(255,255,255,0.05)',
                                        display: 'flex', alignItems: 'center', justifyContent: 'center',
                                        fontSize: 15, flexShrink: 0,
                                    }}>
                                        {a.emoji}
                                    </div>

                                    {/* Info */}
                                    <div style={{ flex: 1, minWidth: 0 }}>
                                        <div style={{
                                            fontSize: 13, fontWeight: 500, color: 'rgba(255,255,255,0.85)',
                                            whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis',
                                        }}>
                                            {a.handle}
                                        </div>
                                        <div style={{ fontSize: 10.5, color: 'rgba(255,255,255,0.3)', marginTop: 1 }}>{a.platform}</div>
                                    </div>

                                    {/* Status indicator */}
                                    {a.status === 'active' && (
                                        <div style={{ position: 'relative', width: 8, height: 8 }}>
                                            <div style={{
                                                position: 'absolute', inset: 0, borderRadius: '50%',
                                                background: STATUS_CLR.active, animation: 'sg-ping 2s infinite',
                                            }} />
                                            <div style={{ position: 'relative', width: 8, height: 8, borderRadius: '50%', background: STATUS_CLR.active }} />
                                        </div>
                                    )}
                                    {a.status === 'error' && (
                                        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                                            <span style={{ fontSize: 10.5, color: '#f87171' }}>{a.detail}</span>
                                            {/* "修复" button — same gradient as login button, smaller */}
                                            <button style={{
                                                padding: '3px 12px', borderRadius: 10, fontSize: 10.5, cursor: 'pointer',
                                                border: 'none',
                                                background: 'linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #a855f7 100%)',
                                                color: '#fff', fontWeight: 500,
                                                boxShadow: '0 2px 12px rgba(99,102,241,0.3)',
                                                transition: 'all 0.25s',
                                            }}
                                                onMouseOver={e => { e.currentTarget.style.boxShadow = '0 4px 20px rgba(99,102,241,0.5)'; }}
                                                onMouseOut={e => { e.currentTarget.style.boxShadow = '0 2px 12px rgba(99,102,241,0.3)'; }}
                                            >
                                                修复
                                            </button>
                                        </div>
                                    )}
                                    {a.status === 'warning' && (
                                        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                                            <span style={{ fontSize: 10.5, color: '#fbbf24' }}>{a.detail}</span>
                                            <WarningOutlined style={{ fontSize: 12, color: '#fbbf24' }} />
                                        </div>
                                    )}
                                </motion.div>
                            ))}
                        </div>
                    </motion.div>
                </div>

            </motion.div>
        </>
    );
};

export default TacticalDashboard;
