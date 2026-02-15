# Design System Specification: Ethereal Nebula (灵犀·星云)

| 项目 | 内容 |
| :--- | :--- |
| **项目** | Lingxi · SoulGravity Enterprise |
| **版本** | 1.0.0 |
| **状态** | Stable |
| **设计负责人** | SoulGravity UX Team |

---

## 1. 设计哲学 (Design Philosophy)

**"Ethereal Nebula" (星云)** 是 SoulGravity 的核心设计语言。它旨在平衡企业级数据的**重力 (Gravity)** 与社交媒体的**灵动 (Soul)**。

### 核心原则
1.  **Solid Data, Liquid Container (实数据，虚容器)**:
    *   **数据**是高对比度、清晰且不透明的，确保可读性。
    *   **容器**（卡片、面板、侧边栏）是半透明、流动的，模拟毛玻璃质感，让背景的星云隐约可见，创造通透感。
2.  **Breathing Background (呼吸的背景)**:
    *   背景绝不是静态的死黑。它由缓慢流动的极光色块（Indigo/Cyan/Violet）组成，模拟一种“心流 (Flow State)”，减少操作员的视觉疲劳。
3.  **Micro-Depth (微纵深)**:
    *   不使用沉重的黑色投影来区分层级。
    *   使用 1px 的高亮描边（Frost Line）和极其微弱的各向同性光晕来暗示物体的前后关系。

---

## 2. 色彩体系 (Color Palette)

我们定义了一套语义化的 "**Soul Tokens**"。请在开发中严格使用 Token Name，而非 Hex 值。

| Token Name | Hex Value | Tailwind Class | 用途 (Usage) |
| :--- | :--- | :--- | :--- |
| **Primary** | `#6366F1` | `bg-soul-indigo` | **主行动点**、激活状态、品牌识别色。代表“智慧”。 |
| **Secondary** | `#06B6D4` | `bg-soul-cyan` | **信息展示**、数据可视化、次要链接。代表“链接”。 |
| **Accent** | `#8B5CF6` | `bg-soul-violet` | **强调**、渐变色的尾部、特殊高亮。代表“灵感”。 |
| **Background** | `#0F172A` | `bg-deep-space` | **暗黑模式基底**。所有的光影都在此之上舞动。 |
| **Glass Base** | `rgba(255,255,255,0.7)` | `bg-white/70` | **面板基底**。用于浅色模式下的卡片背景。 |

---

## 3. 毛玻璃配方 (Glassmorphism Recipe)

这是所有容器组件（Card, Sidebar, Modal）的标准实现配方。

### The Formula (CSS / Tailwind)
```css
.glass-panel {
    /* 1. 模糊：核心特征 */
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);

    /* 2. 透明度：根据模式调整 */
    /* Light Mode */
    background: rgba(255, 255, 255, 0.6);
    /* Dark Mode */
    /* background: rgba(15, 23, 42, 0.6); */

    /* 3. 霜冻线 (Frost Line)：1px 的高亮边框 */
    border: 1px solid rgba(255, 255, 255, 0.3);

    /* 4. 微投影：提升层次感 */
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
}
```

---

## 4. 组件定制 (Ant Design Override)

我们不直接使用 Ant Design 的默认样式，而是通过 Token Override 将其“镂空”。

### 策略：Hollowing Out
*   **全局**: 将 `colorBgContainer` 和 `colorBgLayout` 设置为 `transparent`。让我们的 `.glass-panel` 背景透出来。
*   **Table**:
    *   Header 背景设为半透明白 (`rgba(255,255,255,0.5)`).
    *   Row Hover 使用 Primary 色调的极淡变体 (`rgba(99, 102, 241, 0.1)`).
*   **Card**:
    *   去除默认白色背景与阴影。
    *   应用 Glass Recipe。
*   **Input**:
    *   背景设为更通透的 `rgba(255, 255, 255, 0.4)`。
    *   Focus 时边框变为 `soul-indigo` 并带有光晕。

---

## 5. 排版与布局 (Typography & Layout)

### 字体栈
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
```
选择 `Inter` 是因为其在数字界面上极佳的可读性与中性气质。

### 视觉层级
*   **Headings**: Bold (700), High Contrast (Opacity 1.0).
*   **Body**: Medium (500), Medium Contrast (Opacity 0.85).
*   **Caption**: Regular (400), Low Contrast (Opacity 0.6).

### 布局网格 (FSD Layout)
采用经典的“三栏式”布局但赋予其流动性：
1.  **Sidebar**: 固定左侧，Glass 材质。
2.  **Header**: 顶部通栏，极高透明度 Glass。
3.  **Content**: 中央区域，流式布局，直接承载在流动的背景之上。

---

## 6. 动效与交互 (Motion & Interaction)

### Mesh Gradient Blob
背景中有 3 个巨大的圆形光斑在缓慢游动。
*   **动画时长**: 20s
*   **缓动**: Ease-in-out
*   **循环**: Infinite
*   **效果**: `transform: translate(x, y) scale(v)`

### 交互反馈
*   **Card Hover**:
    *   Scale: `1.02x` (轻微浮起)
    *   Border: 变亮 (`rgba(255,255,255,0.6)`)
*   **Button Click**:
    *   Scale: `0.95x` (按压感)
    *   Glow: 扩散
