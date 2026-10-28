import { defineConfig } from '@playwright/test';
const port = process.env.STORY124_TABLET_PORT ?? '18484';
if (port !== '18484') throw Error('Unexpected tablet preview port');
const baseURL = `http://127.0.0.1:${port}`;
export default defineConfig({
  testDir: './.story124-tests', testMatch: 'tablet-transport.spec.ts', workers: 1, timeout: 60000,
  reporter: [['line'], ['json', { outputFile: process.env.STORY124_REPORT ?? '../tmp/story124-tablet-report.json' }]],
  outputDir: process.env.STORY124_OUTPUT_DIR ?? '../tmp/story124-tablet-results',
  use: { baseURL, channel: process.platform === 'win32' ? 'msedge' : 'chromium', headless: true },
  // Always own this strict-port loopback listener; never reuse another preview.
  webServer: { command: `npx vite preview --config vite.story124-tablet.config.ts --host 127.0.0.1 --port ${port} --strictPort`, url: baseURL, reuseExistingServer: false },
});
