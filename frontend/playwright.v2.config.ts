import { defineConfig } from '@playwright/test';

const origin = 'http://127.0.0.1:19651';

export default defineConfig({
  testDir: './.v2-tests',
  testIgnore: 'tablet-transport.spec.ts',
  workers: 1,
  timeout: 120_000,
  reporter: [['line'], ['json', { outputFile: '../tmp/v2-browser-report.json' }]],
  outputDir: '../tmp/v2-browser-results',
  use: {
    baseURL: origin,
    channel: process.platform === 'win32' ? 'msedge' : 'chromium',
    headless: true,
    trace: 'off',
    screenshot: 'off',
    video: 'off',
  },
  webServer: {
    command: 'npm run start -- --outDir dist-ibe160-v2-tests --port 19651 --host 127.0.0.1',
    url: origin + '/private',
    reuseExistingServer: false,
  },
});
