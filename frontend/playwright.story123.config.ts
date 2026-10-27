import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './.story123-tests', workers: 1, timeout: 120000,
  reporter: [['line'], ['json', { outputFile: process.env.STORY123_REPORT ?? '../tmp/story123-report.json' }]],
  outputDir: process.env.STORY123_OUTPUT_DIR ?? '../tmp/story123-browser-results',
  use: { baseURL: 'http://127.0.0.1:15323', channel: process.platform === 'win32' ? 'msedge' : 'chromium', headless: true },
  webServer: process.env.STORY123_EXTERNAL_SERVER === '1' ? undefined : { command: 'npm run start -- --port 15323 --host 127.0.0.1', url: 'http://127.0.0.1:15323/demo.html', reuseExistingServer: false },
});
