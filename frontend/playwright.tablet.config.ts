import { defineConfig } from '@playwright/test';

// Own local preview only. Every API request is mocked by the test fixture.
export default defineConfig({
  testDir: './tests', testMatch: 'tablet-transport.spec.ts', workers: 1,
  outputDir: '../tmp/tablet-main-browser-results',
  use: { baseURL: 'http://127.0.0.1:18481', channel: process.platform === 'win32' ? 'msedge' : 'chromium', headless: true },
  webServer: {
    command: 'npm run start -- --port 18481 --host 127.0.0.1',
    url: 'http://127.0.0.1:18481', reuseExistingServer: false,
  },
});
