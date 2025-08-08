import path from 'path'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

const SERVER_PORT = parseInt(process.env.PORT ?? '3500', 10) ?? 3500
const HTTPS_PORT = 443
const IS_RUNNING_GITPOD = process.env['GITPOD_WORKSPACE_ID'] !== null && process.env['GITPOD_WORKSPACE_ID'] !== undefined

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react(
    {
      babel: {
        plugins: ['styled-jsx/babel']
      }
    }

  )],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:5050/api',
        changeOrigin: true,
        rewrite: (path) => path.replace('\/api/', ''),
      }
    },
    port: IS_RUNNING_GITPOD ? HTTPS_PORT : SERVER_PORT,
    // hmr: {
    //   port: IS_RUNNING_GITPOD ? HTTPS_PORT : SERVER_PORT,
    // },
  }
})
