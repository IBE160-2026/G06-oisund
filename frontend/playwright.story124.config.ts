import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './.story124-tests', workers: 1, timeout: 120000,
  reporter: [['line'], ['json', { outputFile: process.env.STORY124_REPORT ?? '../tmp/story124-report.json' }]],
  outputDir: process.env.STORY124_OUTPUT_DIR ?? '../tmp/story124-browser-results',
  use: { baseURL: 'http://127.0.0.1:15324', channel: process.platform === 'win32' ? 'msedge' : 'chromium', headless: true, trace: 'retain-on-failure' },
  webServer: { command: 'npm run start -- --port 15324 --host 127.0.0.1', url: 'http://127.0.0.1:15324/demo.html', reuseExistingServer: false },
});
