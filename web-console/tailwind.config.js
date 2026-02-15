/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                'soul-indigo': '#6366F1',
                'soul-cyan': '#06B6D4',
                'soul-violet': '#8B5CF6',
                'deep-space': '#0F172A',
                'glass-white': 'rgba(255, 255, 255, 0.7)',
            },
            animation: {
                blob: "blob 7s infinite",
                'fade-in-up': 'fade-in-up 0.5s ease-out',
            },
            keyframes: {
                blob: {
                    "0%": {
                        transform: "translate(0px, 0px) scale(1)",
                    },
                    "33%": {
                        transform: "translate(30px, -50px) scale(1.1)",
                    },
                    "66%": {
                        transform: "translate(-20px, 20px) scale(0.9)",
                    },
                    "100%": {
                        transform: "translate(0px, 0px) scale(1)",
                    },
                },
                'fade-in-up': {
                    '0%': {
                        opacity: '0',
                        transform: 'translateY(10px)'
                    },
                    '100%': {
                        opacity: '1',
                        transform: 'translateY(0)'
                    },
                }
            },
        },
    },
    plugins: [
        function ({ addUtilities }) {
            addUtilities({
                '.glass-panel': {
                    'backdrop-filter': 'blur(16px)',
                    'background': 'rgba(255, 255, 255, 0.7)',
                    'border': '1px solid rgba(255, 255, 255, 0.3)',
                    'box-shadow': '0 4px 30px rgba(0, 0, 0, 0.1)',
                }
            })
        }
    ],
}
