import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// `npm run dev` outside the containers proxies /api to a locally running API.
export default defineConfig({
  plugins: [react()],
  server: {
    allowedHosts: true,
    // Bind mounts from Windows don't deliver file events, so poll when running in a container.
    watch: process.env.VITE_POLL ? { usePolling: true, interval: 300 } : undefined,
    proxy: { "/api": process.env.API_URL || "http://localhost:8000" },
  },
});
