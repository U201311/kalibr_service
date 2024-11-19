import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    host: 'localhost',
    proxy: {
      "/kalib": {
        target: "http://127.0.0.1:8000/",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/kalib/, ''),
      },
    },
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    // Generate source maps for better debugging
    sourcemap: true,
    // Optimize deps bundling
    // rollupOptions: {
    //   output: {
    //     manualChunks: {
    //       'element-plus': ['element-plus'],
    //       'vue': ['vue']
    //     }
    //   }
    // }
  },
  base: '/', // This ensures assets are loaded correctly from root path
});