import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './.story123-tests', testMatch: 'tablet-transport.spec.ts', workers: 1, timeout: 60000,
  reporter: [['line'], ['json', { outputFile: process.env.STORY123_REPORT ?? '../tmp/story123-tablet-report.json' }]],
  outputDir: process.env.STORY123_OUTPUT_DIR ?? '../tmp/story123-tablet-results',
  use: { baseURL: 'http://127.0.0.1:18483', channel: process.platform === 'win32' ? 'msedge' : 'chromium', headless: true },
  // Always own this strict-port loopback listener; never reuse another preview.
  webServer: { command: 'npx vite preview --config vite.story123-tablet.config.ts --host 127.0.0.1 --port 18483 --strictPort', url: 'http://127.0.0.1:18483', reuseExistingServer: false },
});
