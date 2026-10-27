import { test, expect } from '@playwright/test';

test('two actual tabs apply Day after a cross-tab storage clear', async ({ page, context }) => {
  await page.goto('/demo');
  await page.getByRole('button', { name: 'Bytt til nattvisning', exact: true }).click();
  const other = await context.newPage(); await other.goto('/demo');
  await expect(other.getByText('Visning: Natt', { exact: true })).toBeVisible();
  await other.evaluate(() => localStorage.clear());
  await expect(page.getByText('Visning: Dag', { exact: true })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Bytt til nattvisning', exact: true })).toHaveAttribute('aria-pressed', 'false');
  await other.reload(); await expect(other.getByText('Visning: Dag', { exact: true })).toBeVisible();
  expect(await other.evaluate(() => localStorage.length)).toBe(0);
  await other.close();
});
