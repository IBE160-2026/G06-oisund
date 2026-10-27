import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './tests', testMatch: 'fictional-assessment.spec.ts', workers: 1,
  outputDir: `../tmp/story122-browser-results-${Date.now()}`,
  use: { baseURL: 'http://127.0.0.1:15222', channel: process.platform === 'win32' ? 'msedge' : 'chromium', headless: true },
  webServer: { command: 'npm run start -- --port 15222 --host 127.0.0.1', url: 'http://127.0.0.1:15222/demo.html', reuseExistingServer: false },
});
