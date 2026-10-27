import { defineConfig } from 'vite';
// Both launch modes serve /demo from the separate entry, without private modules.
const demoEntry = (req: { url?: string }, _res: unknown, next: () => void) => {
  if (req.url?.split('?')[0] === '/demo') req.url = req.url.replace('/demo', '/demo.html');
  next();
};
export default defineConfig({
  plugins: [{ name: 'fictional-demo-entry', configureServer(server) { server.middlewares.use(demoEntry); }, configurePreviewServer(server) { server.middlewares.use(demoEntry); } }],
  build: { rollupOptions: { input: { main: 'index.html', demo: 'demo.html' } } },
});
