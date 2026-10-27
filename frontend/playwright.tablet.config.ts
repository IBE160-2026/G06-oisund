import { defineConfig } from '@playwright/test';

// Own local preview only. Every API request is mocked by the test fixture.
export default defineConfig({
  testDir: './tests', testMatch: 'tablet-transport.spec.ts', workers: 1,
  outputDir: '../tmp/tablet-main-browser-results',
  use: { baseURL: 'http://127.0.0.1:18481', channel: process.platform === 'win32' ? 'msedge' : 'chromium', headless: true },
  webServer: {
    command: 'npx vite build --config vite.story123-tablet.config.ts && npx vite preview --config vite.story123-tablet.config.ts --port 18481 --host 127.0.0.1 --strictPort',
    env: { VITE_PRIVATE_API_BASE: '/private-api' },
    url: 'http://127.0.0.1:18481', reuseExistingServer: false,
  },
});
