import { defineConfig } from '@playwright/test';

const origin = 'http://127.0.0.1:19654';
const output = 'dist-ibe160-v2-tablet';

export default defineConfig({
  testDir: './.v2-tests',
  testMatch: 'tablet-transport.spec.ts',
  workers: 1,
  outputDir: '../tmp/v2-tablet-results',
  use: { baseURL: origin, channel: process.platform === 'win32' ? 'msedge' : 'chromium', headless: true },
  webServer: {
    command: `npm run build -- --outDir ${output} && npm run start -- --outDir ${output} --host 127.0.0.1 --port 19654`,
    env: { VITE_PRIVATE_API_BASE: '/private-api' },
    url: origin,
    reuseExistingServer: false,
  },
});
