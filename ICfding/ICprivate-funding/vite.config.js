import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "path";

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"),
    },
  },
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:8000", // Local backend IP
        changeOrigin: true,
        secure: false,
      },
    },
    cors: true,
  },
   //EC2 deployment settings (uncomment when deploying to EC2)
  //server: {
    //proxy: {
     // "/api": {
      // target: "http://3.25.83.191:8000", 
      // changeOrigin: true,
      // secure: false,
      //},
   //},
   // cors: true,
 // },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
  },
});