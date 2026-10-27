import { expect, type Page, type TestInfo } from '@playwright/test';
import { focusPixelChange } from './tablet-pc-focus-pixels';

export async function measure(page: Page, info: TestInfo, state: string, allowUnmeasured = false) {
  const result = await page.evaluate(() => {
    type Color = [number, number, number, number];
    const unmeasured: { label: string; reason: string }[] = [];
    const parse = (s: string): Color | null => {
      const values = s.match(/^rgba?\(([^)]+)\)$/)?.[1].split(/[, /]+/).filter(Boolean).map(Number);
      return values && values.length >= 3 && values.every(Number.isFinite) ? [values[0], values[1], values[2], values[3] ?? 1] : null;
    };
    const over = (top: Color, bottom: Color): Color => { const a = top[3] + bottom[3] * (1 - top[3]); return [0, 1, 2].map(i => (top[i] * top[3] + bottom[i] * bottom[3] * (1 - top[3])) / (a || 1)).concat(a) as Color; };
    const lum = (c: Color) => c.slice(0, 3).map(v => { v /= 255; return v <= .04045 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4; }).reduce((sum, v, i) => sum + v * [.2126, .7152, .0722][i], 0);
    const ratio = (a: Color, b: Color) => (Math.max(lum(a), lum(b)) + .05) / (Math.min(lum(a), lum(b)) + .05);
    const modal = document.querySelector('dialog[open]');
    const scope = modal ?? document.querySelector('main')!;
    const visible = (e: Element) => e.checkVisibility({ contentVisibilityAuto: true }) && e.getClientRects().length > 0 && getComputedStyle(e).visibility !== 'hidden' && !e.closest('[hidden],dialog:not([open])');
    const background = (e: Element | null, label: string): Color | null => {
      const layers: Color[] = []; let opaque = false;
      for (let p = e; p; p = p.parentElement) {
        const css = getComputedStyle(p);
        if (Number(css.opacity) !== 1 || css.filter !== 'none' || css.mixBlendMode !== 'normal' || css.backgroundImage !== 'none' || css.backdropFilter !== 'none') { unmeasured.push({ label, reason: 'unsupported opacity/filter/blending/image background: ' + p.tagName + ' ' + JSON.stringify({ opacity: css.opacity, filter: css.filter, blend: css.mixBlendMode, image: css.backgroundImage, backdrop: css.backdropFilter }) }); return null; }
        const color = parse(css.backgroundColor);
        if (!color) { unmeasured.push({ label, reason: 'unsupported background color ' + css.backgroundColor }); return null; }
        layers.push(color);
        if (color[3] === 1) { opaque = true; break; }
        if (p === modal) { unmeasured.push({ label, reason: 'translucent modal over spatially varying page/backdrop is not inferred from CSS' }); return null; }
      }
      // Ancestor group opacity affects even an opaque child, so inspect it too.
      for (let p = e; p; p = p.parentElement) { const css = getComputedStyle(p); if (Number(css.opacity) !== 1 || css.filter !== 'none' || css.mixBlendMode !== 'normal') { unmeasured.push({ label, reason: 'unsupported ancestor group opacity/filter/blending' }); return null; } }
      let value: Color = [255, 255, 255, 1];
      for (const layer of layers.reverse()) value = over(layer, value);
      return opaque || !modal ? value : null;
    };
    const text: { label: string; ratio: number; color: Color; background: Color }[] = [];
    const clipping: { label: string; ancestor: string; axis: string }[] = [];
    const inspectClip = (e: Element, rects: DOMRect[], label: string, includeSelf = true) => {
      if (e.closest('input,textarea,select')) return; // Native field content intentionally scrolls.
      for (let p: Element | null = includeSelf ? e : e.parentElement; p && p !== document.documentElement; p = p.parentElement) {
        const css = getComputedStyle(p), box = p.getBoundingClientRect();
        const intentionalDialogScroll = p === modal && ['auto', 'scroll'].includes(css.overflowY);
        for (const axis of ['x', 'y']) {
          const overflow = axis === 'x' ? css.overflowX : css.overflowY;
          if (!['hidden', 'clip', 'auto', 'scroll'].includes(overflow) || intentionalDialogScroll && axis === 'y') continue;
          const start = axis === 'x' ? box.left + (p as HTMLElement).clientLeft : box.top + (p as HTMLElement).clientTop;
          const end = start + (axis === 'x' ? (p as HTMLElement).clientWidth : (p as HTMLElement).clientHeight);
          if (rects.some(r => (axis === 'x' ? r.left : r.top) < start - 1 || (axis === 'x' ? r.right : r.bottom) > end + 1)) clipping.push({ label, ancestor: p.tagName + '.' + p.className, axis });
        }
      }
      if (getComputedStyle(e).textOverflow === 'ellipsis' && e.scrollWidth > e.clientWidth + 1) clipping.push({ label, ancestor: e.tagName, axis: 'ellipsis' });
    };
    const addText = (e: Element, colorValue: string, label: string) => { const bg = background(e, label), color = parse(colorValue); if (bg && color) text.push({ label, ratio: ratio(over(color, bg), bg), color: over(color, bg), background: bg }); else if (!color) unmeasured.push({ label, reason: 'unsupported foreground ' + colorValue }); };
    const walker = document.createTreeWalker(scope, NodeFilter.SHOW_TEXT); let node: Node | null;
    while ((node = walker.nextNode())) {
      const e = node.parentElement!, label = node.textContent?.trim().slice(0, 100);
      if (!label || !visible(e) || e.closest('script,style,option,textarea')) continue;
      const range = document.createRange(); range.selectNodeContents(node); const rects = Array.from(range.getClientRects());
      if (!rects.length) continue;
      addText(e, getComputedStyle(e).color, label); inspectClip(e, rects, label);
    }
    for (const e of Array.from(scope.querySelectorAll('input,textarea,select')).filter(visible)) {
      if (e.matches('input[type=checkbox],input[type=radio]')) continue;
      addText(e, getComputedStyle(e).color, 'control value: ' + (e.getAttribute('aria-label') || e.tagName));
      if (e.getAttribute('placeholder')) addText(e, getComputedStyle(e, '::placeholder').color, 'placeholder');
    }
    const boundaries = Array.from(scope.querySelectorAll('button,input,select,textarea,summary')).filter(visible).filter(e => !e.matches('input[type=checkbox],input[type=radio]')).flatMap(e => {
      const label = e.textContent?.trim().slice(0, 80) || e.getAttribute('aria-label') || e.tagName;
      inspectClip(e, [e.getBoundingClientRect()], label, false);
      const css = getComputedStyle(e), outside = background(e.parentElement, label), inside = background(e, label), border = parse(css.borderTopColor), color = parse(css.color);
      if (!outside || !inside || !border || !color) return [];
      return [{ label, ratio: Math.max(parseFloat(css.borderTopWidth) > 0 && css.borderTopStyle !== 'none' ? ratio(over(border, outside), outside) : 0, ratio(inside, outside), e.matches('summary') ? ratio(over(color, outside), outside) : 0), height: e.getBoundingClientRect().height }];
    });
    return { environment: { userAgent: navigator.userAgent, viewport: { width: innerWidth, height: innerHeight }, rootFontSize: getComputedStyle(document.documentElement).fontSize, themeClass: document.documentElement.className, theme: document.documentElement.dataset.theme, scope: modal ? 'active native modal only; underlying backdrop/page excluded' : 'main' }, text, boundaries, clipping, unmeasured, overflow: document.documentElement.scrollWidth - innerWidth };
  });
  await info.attach(state, { body: JSON.stringify(result, null, 2), contentType: 'application/json' });
  const requestedScale = info.title.match(/(100|200)% text/)?.[1];
  if (requestedScale) expect(result.environment.rootFontSize, state + ' actual text scale').toBe(requestedScale === '200' ? '32px' : '16px');
  if (!allowUnmeasured) expect(result.unmeasured, state + ' unsupported layers explicitly unmeasured').toEqual([]);
  if (!result.unmeasured.length) expect(result.text.length, state).toBeGreaterThan(0);
  expect(result.text.filter(v => v.ratio < 4.5), state + ' measured text').toEqual([]);
  expect(result.boundaries.filter(v => v.ratio < 3), state + ' measured boundaries').toEqual([]);
  expect(result.clipping, state + ' critical content clipping').toEqual([]);
  expect(result.overflow, state + ' page overflow').toBeLessThanOrEqual(1);
  return result; // Unsupported layers are explicitly unmeasured, never a pass.
}

export async function measureFocus(page: Page, info: TestInfo, state: string) {
  // Census actual Tab candidates in the modal or document. A native date/time
  // host can consume several Tab presses; count controls only when their host
  // is reached, then require a complete traversal cycle and every census item.
  const census = await page.evaluate(() => {
    document.querySelectorAll<HTMLElement>('[data-focus-census]').forEach(e => delete e.dataset.focusCensus);
    const scope = document.querySelector('dialog[open]') ?? document.querySelector('main')!;
    return Array.from(scope.querySelectorAll<HTMLElement>('button,input,textarea,select,a[href],summary,[tabindex]')).filter(e => e.tabIndex >= 0 && !e.matches(':disabled') && e.checkVisibility({ contentVisibilityAuto: true }) && e.getClientRects().length > 0 && !e.closest('[hidden],dialog:not([open])') && getComputedStyle(e).visibility !== 'hidden').map((e, index) => {
      const id = String(index); e.dataset.focusCensus = id;
      return { id, label: e.getAttribute('aria-label') || e.textContent?.slice(0, 80) || e.tagName };
    });
  });
  const results = [], seen = new Set<string>(), pixelSeen = new Set<string>(), pixelResults = [];
  let first: string | undefined, leftFirst = false, completedCycle = false;
  for (let i = 0; i < (census.length + 1) * 12 + 40; i++) {
    // Returning from browser chrome revalidates private access and briefly
    // disables controls. Wait for the censused ready state before the next Tab.
    await page.waitForFunction(ids => ids.every(id => { const e = document.querySelector(`[data-focus-census="${id}"]`); return !e || !e.getClientRects().length || !e.matches(':disabled'); }), census.map(control => control.id));
    await page.keyboard.press('Tab');
    // Native subfield focus and browser scrolling settle on the next paint.
    await page.evaluate(() => new Promise<void>(resolve => requestAnimationFrame(() => requestAnimationFrame(() => resolve()))));
    const value = await page.evaluate(() => {
      const e = document.activeElement!;
      if (e === document.body) return null;
      const css = getComputedStyle(e), box = e.getBoundingClientRect();
      const rgb = (s: string) => s.match(/[\d.]+/g)!.slice(0, 3).map(Number);
      const lum = (s: string) => rgb(s).map(n => { n /= 255; return n <= .04045 ? n / 12.92 : ((n + .055) / 1.055) ** 2.4; }).reduce((sum, n, i) => sum + n * [.2126, .7152, .0722][i], 0);
      let parent = e.parentElement; let bg = 'rgb(255,255,255)';
      while (parent) { const c = getComputedStyle(parent).backgroundColor; if (c !== 'rgba(0, 0, 0, 0)') { bg = c; break; } parent = parent.parentElement; }
      const ratio = (Math.max(lum(css.outlineColor), lum(bg)) + .05) / (Math.min(lum(css.outlineColor), lum(bg)) + .05);
      const x = Math.max(0, Math.min(innerWidth - 1, box.left + box.width / 2)), y = Math.max(0, Math.min(innerHeight - 1, box.top + box.height / 2));
      const hit = document.elementFromPoint(x, y);
      const exposed = Math.max(0, Math.min(box.right, innerWidth) - Math.max(box.left, 0)) * (Number(box.top >= 0 && box.top <= innerHeight) + Number(box.bottom >= 0 && box.bottom <= innerHeight)) + Math.max(0, Math.min(box.bottom, innerHeight) - Math.max(box.top, 0)) * (Number(box.left >= 0 && box.left <= innerWidth) + Number(box.right >= 0 && box.right <= innerWidth));
      const visibleOutlineArea = exposed * parseFloat(css.outlineWidth);
      return { censusId: (e as HTMLElement).dataset.focusCensus, rect: { top: box.top, bottom: box.bottom, left: box.left, right: box.right }, visibleOutlineArea, requiredOutlineArea: 2 * (2 * (box.width + box.height)), label: e.textContent?.slice(0, 70) || e.tagName, ratio, width: parseFloat(css.outlineWidth), visible: css.outlineStyle !== 'none' && (e.matches(':focus-visible') || e.matches(':focus-within')), inModal: !document.querySelector('dialog[open]') || !!e.closest('dialog[open]'), onscreen: box.bottom > 0 && box.top < innerHeight && box.right > 0 && box.left < innerWidth && !!hit && (e.contains(hit) || hit.contains(e)) };
    });
    if (value) {
      results.push(value);
      if (value.censusId !== undefined && !pixelSeen.has(value.censusId)) {
        pixelResults.push(await focusPixelChange(page, info, state, value.censusId)); pixelSeen.add(value.censusId);
      }
      if (value.censusId !== undefined) {
        if (first === undefined) first = value.censusId;
        else if (value.censusId !== first) leftFirst = true;
        else if (leftFirst || census.length === 1 && results.length > 1) { completedCycle = true; break; }
        seen.add(value.censusId);
      }
    }
  }
  const missing = census.filter(control => !seen.has(control.id));
  await info.attach(state + '-focus', { body: JSON.stringify({ pixelResults, census, visited: [...seen], missing, completedCycle, results }, null, 2), contentType: 'application/json' });
  expect(pixelResults.filter(result => result.changedArea < result.requiredArea), state + ' actual same-pixel focus change').toEqual([]);
  expect(completedCycle, state + ' bounded keyboard traversal completed a cycle').toBe(true);
  expect(missing, state + ' all reachable controls visited').toEqual([]);
  expect(results.filter(v => !v.visible || v.width < 2 || v.ratio < 3 || !v.inModal || !v.onscreen || v.visibleOutlineArea < v.requiredOutlineArea), state).toEqual([]);
}
