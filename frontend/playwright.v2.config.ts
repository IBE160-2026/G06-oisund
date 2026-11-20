import { defineConfig } from '@playwright/test';

const origin = 'http://127.0.0.1:19651';
const chromiumChannel = process.platform === 'win32' ? 'msedge' : 'chromium';
const multiEngine = process.env.PLAYWRIGHT_V2_MULTI_ENGINE === '1';

export default defineConfig({
  testDir: './.v2-tests',
  testIgnore: ['tablet-transport.spec.ts', 'v2-*.test.ts'],
  workers: 1,
  timeout: 120_000,
  reporter: [['line'], ['json', { outputFile: '../tmp/v2-browser-report.json' }]],
  outputDir: '../tmp/v2-browser-results',
  projects: multiEngine ? [
    { name: chromiumChannel, use: { browserName: 'chromium', channel: chromiumChannel } },
    { name: 'firefox', use: { browserName: 'firefox' } },
    { name: 'webkit', use: { browserName: 'webkit' } },
  ] : undefined,
  use: {
    baseURL: origin,
    channel: multiEngine ? undefined : chromiumChannel,
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
