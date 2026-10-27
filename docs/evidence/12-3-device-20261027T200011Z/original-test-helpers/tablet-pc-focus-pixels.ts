import { createRequire } from 'node:module';
import { expect, type Page, type TestInfo } from '@playwright/test';
const require = createRequire(import.meta.url);
const { PNG } = require(require.resolve('playwright-core/package.json').replace('package.json', 'lib/utilsBundle.js'));
const lum = (c: number[]) => c.map(v => { v /= 255; return v <= .04045 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4; }).reduce((s, v, i) => s + v * [.2126, .7152, .0722][i], 0);
const ratio = (a: number[], b: number[]) => (Math.max(lum(a), lum(b)) + .05) / (Math.min(lum(a), lum(b)) + .05);
const caches = new WeakMap<TestInfo, Map<string, { changedArea: number; requiredArea: number; representative: string }>>();

// Every host is blurred and its actual unfocused CSS/surface signature checked.
// Only identical geometry/style/surface pairs reuse a representative pixel pair.
// This deliberately distinguishes a permanent outline from a focus-only outline.
export async function focusPixelChange(page: Page, info: TestInfo, state: string, id: string) {
  const signature = async () => page.evaluate(() => {
    const e = document.querySelector<HTMLElement>('[data-focus-pixel-target]')!;
    const properties = ['outlineStyle', 'outlineColor', 'outlineWidth', 'outlineOffset', 'boxShadow', 'borderRadius', 'borderWidth', 'borderColor', 'backgroundColor', 'backgroundImage', 'opacity', 'filter', 'transform'];
    const chain = []; for (let p: Element | null = e; p; p = p.parentElement) { const c = getComputedStyle(p); chain.push(properties.map(key => (c as any)[key])); }
    const r = e.getBoundingClientRect();
    return { chain, rect: { x: r.x, y: r.y, width: r.width, height: r.height }, scroll: { x: scrollX, y: scrollY }, dpr: devicePixelRatio };
  });
  await page.evaluate(() => { document.querySelector('[data-focus-pixel-target]')?.removeAttribute('data-focus-pixel-target'); document.activeElement?.setAttribute('data-focus-pixel-target', ''); });
  const focused = await signature();
  const pad = 12, r = focused.rect;
  const viewport = page.viewportSize()!;
  const clip = { x: Math.max(0, Math.floor(r.x - pad)), y: Math.max(0, Math.floor(r.y - pad)), width: 0, height: 0 };
  clip.width = Math.min(viewport.width, Math.ceil(r.x + r.width + pad)) - clip.x;
  clip.height = Math.min(viewport.height, Math.ceil(r.y + r.height + pad)) - clip.y;
  await page.evaluate(() => (document.activeElement as HTMLElement)?.blur());
  const unfocused = await signature();
  const key = JSON.stringify({ focused: focused.chain, unfocused: unfocused.chain, width: r.width, height: r.height, dpr: focused.dpr, clip, unsupportedSurfaceIdentity: focused.chain.some(layer => layer[9] !== 'none' || layer[10] !== '1' || layer[11] !== 'none') ? state + '-' + id : null });
  let cache = caches.get(info); if (!cache) { cache = new Map(); caches.set(info, cache); }
  const previous = cache.get(key);
  const before = previous ? undefined : await page.screenshot({ clip, animations: 'disabled', scale: 'css' });
  // Restore through the keyboard, never element.focus(). Sequential navigation
  // retains the blurred host as its origin, including native editable subfields.
  await page.keyboard.press('Shift+Tab'); await page.keyboard.press('Tab');
  await page.evaluate(({ scroll }) => window.scrollTo(scroll.x, scroll.y), focused);
  await page.evaluate(() => new Promise<void>(resolve => requestAnimationFrame(() => resolve())));
  const restored = await page.evaluate(() => document.activeElement?.hasAttribute('data-focus-pixel-target'));
  expect(restored, state + ' pixel probe restored actual keyboard host ' + id).toBe(true);
  if (previous) return { ...previous, coverage: 'representative pixel pair; this host unfocused signature independently checked', cacheHit: true };
  const after = await page.screenshot({ clip, animations: 'disabled', scale: 'css' });
  const a = PNG.sync.read(before), b = PNG.sync.read(after);
  let changedArea = 0;
  for (let y = 0; y < Math.min(a.height, b.height); y++) for (let x = 0; x < Math.min(a.width, b.width); x++) {
    const px = clip.x + x + .5, py = clip.y + y + .5;
    // Count only pixels outside the host border box: caret/text/hover changes
    // cannot masquerade as a perimeter focus indicator.
    if (px >= r.x && px < r.x + r.width && py >= r.y && py < r.y + r.height) continue;
    const index = (y * a.width + x) * 4;
    if (ratio(Array.from(a.data.subarray(index, index + 3)), Array.from(b.data.subarray(index, index + 3))) >= 3) changedArea++;
  }
  const result = { changedArea, requiredArea: 2 * (2 * (r.width + r.height)), representative: `${state}-${id}`, coverage: 'actual same-pixel focused/unfocused perimeter change at >=3:1', cacheHit: false };
  await info.attach(result.representative + '-unfocused.png', { body: before!, contentType: 'image/png' });
  await info.attach(result.representative + '-focused.png', { body: after, contentType: 'image/png' });
  await info.attach(result.representative + '-change', { body: JSON.stringify(result), contentType: 'application/json' });
  cache.set(key, result);
  return result;
}
