import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './submission-tests',
  workers: 1,
  timeout: 180000,
  reporter: [['line'], ['json', { outputFile: '../tmp/submission-browser-report.json' }]],
  outputDir: '../tmp/submission-browser-results',
  use: {
    baseURL: 'http://127.0.0.1:15325',
    channel: 'chromium',
    headless: true,
    actionTimeout: 15000,
    trace: 'retain-on-failure',
  },
});
