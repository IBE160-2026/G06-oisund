import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  workers: 1,
  use: { baseURL: 'http://127.0.0.1:5173', channel: process.platform === 'win32' ? 'msedge' : 'chromium', headless: true },
});
