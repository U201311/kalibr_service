/*
 * @Author: zhengjie.sheng
 * @Date: 2024-11-13 08:56:10
 * @LastEditors: zhengjie.sheng
 * @LastEditTime: 2024-11-13 18:30:21
 * @Description: 
 * @FilePath: /project/vite.config.ts
 */
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    host: '0.0.0.0',
    proxy: {
      "/kalib": {
        target: "http://10.112.12.60:8000/", // //目标域名
        changeOrigin: true, //需要代理跨域
      },
    }
  },
});