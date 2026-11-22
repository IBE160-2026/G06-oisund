import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './tests', testMatch: /[\\\/]password-[^\\\/]*\.spec\.ts$/, workers: 1, timeout: 90000,
  reporter: [['line']], outputDir: '../tmp/password-browser-results',
  use: { baseURL: 'http://127.0.0.1:15440', channel: process.platform === 'win32' ? 'msedge' : 'chromium', headless: true, trace: 'off', screenshot: 'off', video: 'off' },
  webServer: { command: 'npm run start -- --port 15440 --host 127.0.0.1', url: 'http://127.0.0.1:15440/private', reuseExistingServer: false },
});
