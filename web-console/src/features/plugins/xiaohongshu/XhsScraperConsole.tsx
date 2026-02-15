import React, { useState, useEffect, useRef, useCallback } from 'react';
import { message } from 'antd';
import { HeartFilled, SearchOutlined, LoadingOutlined } from '@ant-design/icons';

const API_BASE = '/api/v1/xhs';

interface XhsNoteItem {
    note_id: string;
    title: string;
    desc: string;
    cover_url: string;
    likes: number;
    comments: number;
    collects: number;
    user_nickname: string;
    keyword_search: string;
    last_scraped_at: string;
}

interface PaginatedResponse {
    items: XhsNoteItem[];
    total: number;
    page: number;
    page_size: number;
}

const SORT_OPTIONS = [
    { value: 'general', label: '综合' },
    { value: 'time_descending', label: '最新' },
    { value: 'popularity_descending', label: '最热' },
];

const XhsScraperConsole: React.FC = () => {
    const [keyword, setKeyword] = useState('');
    const [sortType, setSortType] = useState('general');
    const [loading, setLoading] = useState(false);
    const [notes, setNotes] = useState<XhsNoteItem[]>([]);
    const [total, setTotal] = useState(0);
    const pollingRef = useRef<ReturnType<typeof setInterval> | null>(null);

    // Fetch notes
    const fetchNotes = useCallback(async (kw?: string) => {
        try {
            const params = new URLSearchParams({ page: '1', page_size: '40' });
            if (kw) params.set('keyword', kw);

            const res = await fetch(`${API_BASE}/notes?${params}`);
            if (!res.ok) throw new Error('获取笔记失败');

            const data: PaginatedResponse = await res.json();
            setNotes(data.items);
            setTotal(data.total);
        } catch (err) {
            console.error(err);
        }
    }, []);

    // Load notes on mount
    useEffect(() => {
        fetchNotes();
    }, [fetchNotes]);

    // Cleanup polling on unmount
    useEffect(() => {
        return () => {
            if (pollingRef.current) clearInterval(pollingRef.current);
        };
    }, []);

    // Trigger scrape
    const handleScrape = async () => {
        if (!keyword.trim()) {
            message.warning('请输入搜索关键词');
            return;
        }

        setLoading(true);

        try {
            const res = await fetch(`${API_BASE}/scrape`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ keyword: keyword.trim(), sort_type: sortType }),
            });

            if (!res.ok) throw new Error('采集请求失败');

            const data = await res.json();
            message.success(`采集任务已启动 (${data.task_id.slice(0, 8)}...)`);

            // Poll for results
            let attempts = 0;
            pollingRef.current = setInterval(async () => {
                attempts++;
                await fetchNotes(keyword.trim());

                if (attempts >= 10) {
                    // Stop after 30s
                    if (pollingRef.current) clearInterval(pollingRef.current);
                    pollingRef.current = null;
                    setLoading(false);
                }
            }, 3000);

            // Also stop loading after first successful poll
            setTimeout(() => {
                setLoading(false);
            }, 5000);
        } catch (err: any) {
            message.error(err.message || '采集失败');
            setLoading(false);
        }
    };

    const formatCount = (n: number): string => {
        if (n >= 10000) return `${(n / 10000).toFixed(1)}万`;
        if (n >= 1000) return `${(n / 1000).toFixed(1)}k`;
        return String(n);
    };

    return (
        <div style={{ minHeight: '100%' }}>
            {/* Header */}
            <h1
                style={{
                    fontSize: 24,
                    fontWeight: 700,
                    color: '#fff',
                    marginBottom: 24,
                }}
            >
                小红书关键词采集
            </h1>

            {/* Control Bar */}
            <div
                style={{
                    display: 'flex',
                    gap: 12,
                    alignItems: 'center',
                    padding: '16px 20px',
                    borderRadius: 14,
                    background: 'rgba(255,255,255,0.05)',
                    backdropFilter: 'blur(12px)',
                    border: '1px solid rgba(255,255,255,0.08)',
                    marginBottom: 24,
                    flexWrap: 'wrap',
                }}
            >
                {/* Keyword Input */}
                <div style={{ flex: 1, minWidth: 200, position: 'relative' }}>
                    <SearchOutlined
                        style={{
                            position: 'absolute',
                            left: 14,
                            top: '50%',
                            transform: 'translateY(-50%)',
                            color: 'rgba(255,255,255,0.3)',
                            fontSize: 16,
                            zIndex: 1,
                        }}
                    />
                    <input
                        type="text"
                        value={keyword}
                        onChange={(e) => setKeyword(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && handleScrape()}
                        placeholder="输入关键词，如：护肤、穿搭、美食..."
                        style={{
                            width: '100%',
                            height: 44,
                            borderRadius: 10,
                            border: '1px solid rgba(255,255,255,0.1)',
                            background: 'rgba(255,255,255,0.04)',
                            color: '#fff',
                            fontSize: 14,
                            paddingLeft: 40,
                            paddingRight: 14,
                            outline: 'none',
                            transition: 'all 0.3s',
                        }}
                        onFocus={(e) => {
                            e.target.style.borderColor = 'rgba(34,211,238,0.4)';
                            e.target.style.boxShadow = '0 0 0 2px rgba(34,211,238,0.1)';
                        }}
                        onBlur={(e) => {
                            e.target.style.borderColor = 'rgba(255,255,255,0.1)';
                            e.target.style.boxShadow = 'none';
                        }}
                    />
                </div>

                {/* Sort Select */}
                <select
                    value={sortType}
                    onChange={(e) => setSortType(e.target.value)}
                    style={{
                        height: 44,
                        borderRadius: 10,
                        border: '1px solid rgba(255,255,255,0.1)',
                        background: 'rgba(255,255,255,0.06)',
                        color: '#fff',
                        fontSize: 14,
                        padding: '0 32px 0 14px',
                        outline: 'none',
                        cursor: 'pointer',
                        appearance: 'none',
                        backgroundImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='rgba(255,255,255,0.4)' d='M6 8L1 3h10z'/%3E%3C/svg%3E")`,
                        backgroundRepeat: 'no-repeat',
                        backgroundPosition: 'right 12px center',
                    }}
                >
                    {SORT_OPTIONS.map((opt) => (
                        <option key={opt.value} value={opt.value} style={{ background: '#1e293b' }}>
                            {opt.label}
                        </option>
                    ))}
                </select>

                {/* Scrape Button */}
                <button
                    onClick={handleScrape}
                    disabled={loading}
                    style={{
                        height: 44,
                        padding: '0 28px',
                        borderRadius: 10,
                        border: 'none',
                        background: loading
                            ? 'rgba(99,102,241,0.4)'
                            : 'linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #a855f7 100%)',
                        color: '#fff',
                        fontSize: 14,
                        fontWeight: 600,
                        cursor: loading ? 'not-allowed' : 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        gap: 8,
                        transition: 'all 0.3s',
                        boxShadow: loading ? 'none' : '0 4px 16px rgba(99,102,241,0.3)',
                        whiteSpace: 'nowrap',
                    }}
                >
                    {loading ? <LoadingOutlined /> : <SearchOutlined />}
                    {loading ? '采集中...' : '开始采集'}
                </button>
            </div>

            {/* Stats Bar */}
            {total > 0 && (
                <div
                    style={{
                        fontSize: 13,
                        color: 'rgba(255,255,255,0.4)',
                        marginBottom: 16,
                    }}
                >
                    共 <span style={{ color: '#22d3ee' }}>{total}</span> 条笔记
                </div>
            )}

            {/* Results Grid — Masonry-like with CSS columns */}
            {notes.length > 0 ? (
                <div
                    style={{
                        columnCount: 4,
                        columnGap: 16,
                    }}
                >
                    {notes.map((note) => (
                        <div
                            key={note.note_id}
                            style={{
                                breakInside: 'avoid',
                                marginBottom: 16,
                                borderRadius: 12,
                                overflow: 'hidden',
                                background: 'rgba(255,255,255,0.04)',
                                border: '1px solid rgba(255,255,255,0.06)',
                                transition: 'all 0.3s ease',
                                cursor: 'pointer',
                            }}
                            onMouseOver={(e) => {
                                e.currentTarget.style.transform = 'translateY(-2px)';
                                e.currentTarget.style.borderColor = 'rgba(255,255,255,0.12)';
                                e.currentTarget.style.boxShadow = '0 8px 24px rgba(0,0,0,0.2)';
                            }}
                            onMouseOut={(e) => {
                                e.currentTarget.style.transform = 'translateY(0)';
                                e.currentTarget.style.borderColor = 'rgba(255,255,255,0.06)';
                                e.currentTarget.style.boxShadow = 'none';
                            }}
                        >
                            {/* Cover Image */}
                            {note.cover_url && (
                                <img
                                    src={note.cover_url}
                                    alt={note.title}
                                    referrerPolicy="no-referrer"
                                    loading="lazy"
                                    style={{
                                        width: '100%',
                                        display: 'block',
                                        objectFit: 'cover',
                                    }}
                                    onError={(e) => {
                                        (e.target as HTMLImageElement).style.display = 'none';
                                    }}
                                />
                            )}

                            {/* Content */}
                            <div style={{ padding: '10px 12px 12px' }}>
                                <p
                                    style={{
                                        fontSize: 13,
                                        fontWeight: 500,
                                        color: 'rgba(255,255,255,0.85)',
                                        margin: 0,
                                        lineHeight: 1.4,
                                        display: '-webkit-box',
                                        WebkitLineClamp: 2,
                                        WebkitBoxOrient: 'vertical',
                                        overflow: 'hidden',
                                    }}
                                >
                                    {note.title || '无标题'}
                                </p>

                                {/* Stats Row */}
                                <div
                                    style={{
                                        display: 'flex',
                                        alignItems: 'center',
                                        justifyContent: 'space-between',
                                        marginTop: 8,
                                    }}
                                >
                                    <span
                                        style={{
                                            fontSize: 11,
                                            color: 'rgba(255,255,255,0.35)',
                                            maxWidth: '60%',
                                            overflow: 'hidden',
                                            textOverflow: 'ellipsis',
                                            whiteSpace: 'nowrap',
                                        }}
                                    >
                                        @{note.user_nickname}
                                    </span>
                                    <span
                                        style={{
                                            display: 'flex',
                                            alignItems: 'center',
                                            gap: 4,
                                            fontSize: 12,
                                            color: 'rgba(255,255,255,0.4)',
                                        }}
                                    >
                                        <HeartFilled style={{ color: '#f87171', fontSize: 12 }} />
                                        {formatCount(note.likes)}
                                    </span>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            ) : (
                !loading && (
                    <div
                        style={{
                            textAlign: 'center',
                            padding: 80,
                            color: 'rgba(255,255,255,0.2)',
                            fontSize: 14,
                        }}
                    >
                        输入关键词开始采集笔记
                    </div>
                )
            )}
        </div>
    );
};

export default XhsScraperConsole;
