import { readFileSync } from "node:fs";
import { fileURLToPath, URL } from "node:url";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const releasePath = fileURLToPath(new URL("../workspace_app/release.json", import.meta.url));
const release = JSON.parse(readFileSync(releasePath, "utf8"));

export default defineConfig({
  plugins: [react()],
  define: {
    __ARVECTUM_WORKSPACE_RELEASE__: JSON.stringify(release.release_id),
  },
  build: {
    manifest: true,
    outDir: "dist",
    emptyOutDir: true,
    sourcemap: false,
  },
  test: {
    environment: "jsdom",
    setupFiles: ["./src/test-setup.ts"],
  },
});
