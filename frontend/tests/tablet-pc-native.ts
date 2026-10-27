import { createRequire } from 'node:module';
import { expect, type Page, type TestInfo } from '@playwright/test';
const require = createRequire(import.meta.url);
// PNG is bundled in the exact locked Playwright version; no downloaded helper.
const { PNG } = require(require.resolve('playwright-core/package.json').replace('package.json', 'lib/utilsBundle.js'));
const lum = (rgb: number[]) => rgb.map(n => { n /= 255; return n <= .04045 ? n / 12.92 : ((n + .055) / 1.055) ** 2.4; }).reduce((s, n, i) => s + n * [.2126, .7152, .0722][i], 0);
const contrast = (a: number[], b: number[]) => (Math.max(lum(a), lum(b)) + .05) / (Math.min(lum(a), lum(b)) + .05);

// Inspect actual rendered indicator pixels, including both checked states. The
// input's original value is restored; this never sends a confirmation or save.
export async function measureChoices(page: Page, info: TestInfo, state: string) {
  const controls = page.locator('input[type=checkbox]:visible');
  const results = [];
  for (let i = 0; i < await controls.count(); i++) {
    const input = controls.nth(i), original = await input.isChecked();
    for (const checked of [false, true]) {
      await input.setChecked(checked);
      const context = await input.evaluate(e => {
        let parent = e.parentElement; let bg = 'rgb(255,255,255)';
        while (parent) { const c = getComputedStyle(parent).backgroundColor; if (c !== 'rgba(0, 0, 0, 0)') { bg = c; break; } parent = parent.parentElement; }
        return { accent: getComputedStyle(e).accentColor.match(/[\d.]+/g)?.slice(0, 3).map(Number), appearance: getComputedStyle(e).appearance, background: bg.match(/[\d.]+/g)!.slice(0, 3).map(Number), label: e.closest('label')?.textContent, labelHeight: e.closest('label')?.getBoundingClientRect().height };
      });
      const screenshot = await input.screenshot();
      await info.attach(`${state}-checkbox-${i}-${checked}.png`, { body: screenshot, contentType: 'image/png' });
      const png = PNG.sync.read(screenshot);
      const pixel = (x: number, y: number) => Array.from(png.data.subarray((y * png.width + x) * 4, (y * png.width + x) * 4 + 3)) as number[];
      // Sample the straight central portion of all four edges. For each edge,
      // find its rendered stroke/fill within a shallow strip; rounded corner
      // antialiasing is outside the sample. Use the weakest of the four edges.
      const edgeRatios = [];
      const depth = Math.max(4, Math.floor(Math.min(png.width, png.height) * .15));
      for (const edge of ['left', 'right', 'top', 'bottom']) {
        let strongest = 0;
        for (let d = 0; d < depth; d++) {
          const values = [];
          const length = ['left', 'right'].includes(edge) ? png.height : png.width;
          for (let n = Math.floor(length * .3); n < length * .7; n++) {
            const x = edge === 'left' ? d : edge === 'right' ? png.width - 1 - d : n;
            const y = edge === 'top' ? d : edge === 'bottom' ? png.height - 1 - d : n;
            values.push(contrast(pixel(x, y), context.background));
          }
          values.sort((a, b) => a - b); strongest = Math.max(strongest, values[Math.floor(values.length / 2)]);
        }
        edgeRatios.push(strongest);
      }
      const histogram = new Map<string, number>();
      for (let y = depth; y < png.height - depth; y++) for (let x = depth; x < png.width - depth; x++) { const key = pixel(x, y).join(','); histogram.set(key, (histogram.get(key) ?? 0) + 1); }
      const palette = [...histogram].sort((a, b) => b[1] - a[1]).filter(([, count]) => count >= 3).slice(0, 4);
      const fill = palette[0]?.[0].split(',').map(Number) ?? [0, 0, 0];
      const fillCoverage = (palette[0]?.[1] ?? 0) / ((png.width - 2 * depth) * (png.height - 2 * depth));
      const fillMatchesAccent = !!context.accent && fill.every((value, channel) => Math.abs(value - context.accent![channel]) <= 12);
      // Classify the dominant checked fill, then find an actual connected,
      // non-boundary glyph component against it. Arbitrary color pairs and
      // the author stroke cannot count as a checkmark.
      const candidates = new Set<string>();
      if (checked) for (let y = depth; y < png.height - depth; y++) for (let x = depth; x < png.width - depth; x++) if (contrast(pixel(x, y), fill) >= 3) candidates.add(x + ',' + y);
      const components = [];
      while (candidates.size) {
        const first = candidates.values().next().value!; candidates.delete(first);
        const queue = [first], points: number[][] = [];
        for (let n = 0; n < queue.length; n++) { const [x, y] = queue[n].split(',').map(Number); points.push([x, y]); for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) { const key = (x + dx) + ',' + (y + dy); if (candidates.delete(key)) queue.push(key); } }
        components.push({ area: points.length, width: Math.max(...points.map(p => p[0])) - Math.min(...points.map(p => p[0])) + 1, height: Math.max(...points.map(p => p[1])) - Math.min(...points.map(p => p[1])) + 1, points });
      }
      const glyph = components.filter(c => c.area >= 3 && c.width >= (png.width - 2 * depth) * .2 && c.height >= (png.height - 2 * depth) * .2).sort((a, b) => b.area - a.area)[0] ?? null;
      results.push({ ...context, checked, size: [png.width, png.height], edgeRatios, palette, fill, fillCoverage, fillMatchesAccent, glyph });
      await info.attach(`${state}-checkbox-${i}-${checked}-pixels`, { body: JSON.stringify(results[results.length - 1], null, 2), contentType: 'application/json' });
      expect(Math.min(...edgeRatios), 'actual checkbox edge ' + context.label).toBeGreaterThanOrEqual(3);
      if (checked) { expect(fillCoverage, 'dominant actual checked fill coverage ' + context.label).toBeGreaterThanOrEqual(.25); expect(glyph, 'actual non-boundary checkmark component ' + context.label).not.toBeNull(); }
      expect(context.labelHeight, 'forgiving checkbox label').toBeGreaterThanOrEqual(58);
    }
    await input.setChecked(original);
  }
  await info.attach(state + '-native-indicators', { body: JSON.stringify(results, null, 2), contentType: 'application/json' });
}
