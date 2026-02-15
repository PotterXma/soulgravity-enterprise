import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const apiUrl = env.VITE_API_URL || 'http://localhost:8000'

  return {
    plugins: [react()],
    server: {
      host: true, // Listen on all addresses (for Docker)
      port: 3000,
      proxy: {
        '/api': {
          target: apiUrl,
          changeOrigin: true,
          // rewrite: (path) => path.replace(/^\/api/, ''), // Don't rewrite if backend expects /api or handles strict paths
        },
      },
    },
  }
})
