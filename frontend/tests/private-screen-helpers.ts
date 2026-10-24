import { expect, type Page } from '@playwright/test';

export async function preparation(page: Page) {
  const back = page.getByRole('button', { name: 'Tilbake til dagen', exact: true }); if (await back.isVisible()) await back.click();
  // A just-clicked plan may still be opening and about to leave preparation.
  await expect(page.locator('.private-confirmation')).toHaveAttribute('aria-busy', 'false');
  if (!await page.getByRole('heading', { name: 'Mine utkast', exact: true }).isVisible()) await page.getByRole('button', { name: 'Forberedelse og planlister', exact: true }).click();
}
export async function editor(page: Page) {
  const back = page.getByRole('button', { name: 'Tilbake til dagen', exact: true }); if (await back.isVisible()) await back.click();
  if (!await page.getByRole('heading', { name: /^(Rediger utkast|Nytt manuelt utkast)$/ }).isVisible()) await page.getByRole('button', { name: 'Kontroller og rediger utkast', exact: true }).click();
}
export async function planScreen(page: Page) {
  if (!await page.getByRole('region', { name: 'Bekreftet plan', exact: true }).isVisible()) await page.getByRole('button', { name: 'Til den åpne planen', exact: true }).click();
}
