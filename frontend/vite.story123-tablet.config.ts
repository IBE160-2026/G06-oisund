import { defineConfig } from 'vite';
import { fileURLToPath } from 'node:url';
// The production tablet HTML and tablet.tsx are the only entry. Keep demo dist intact.
export default defineConfig({
  root: fileURLToPath(new URL('../deploy/tablet/', import.meta.url)),
  resolve: { alias: { '/src': fileURLToPath(new URL('./src', import.meta.url)) } },
  build: { outDir: fileURLToPath(new URL('./dist-story123-tablet', import.meta.url)), emptyOutDir: true },
});
