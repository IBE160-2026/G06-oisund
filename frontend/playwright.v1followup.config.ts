import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './.v1followup-tests', workers: 1, timeout: 120000,
  reporter: [['line'], ['json', { outputFile: process.env.V1FOLLOWUP_REPORT ?? '../tmp/v1followup-report.json' }]],
  outputDir: process.env.V1FOLLOWUP_OUTPUT_DIR ?? '../tmp/v1followup-browser-results',
  use: { baseURL: 'http://127.0.0.1:15326', channel: process.platform === 'win32' ? 'msedge' : 'chromium', headless: true, trace: 'retain-on-failure' },
  webServer: { command: 'npm run start -- --port 15326 --host 127.0.0.1', url: 'http://127.0.0.1:15326/demo.html', reuseExistingServer: false },
});
