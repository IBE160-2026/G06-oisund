import { test, expect } from '@playwright/test';
import { measure, measureFocus } from './tablet-pc-measurements';
import { measureChoices } from './tablet-pc-native';

test('focus pixel change passes a focus-only ring and rejects identical permanent rings despite cached signatures', async ({ page }, info) => {
  const fixture = (permanent: boolean) => `<style>body{margin:30px;background:white}button{width:140px;height:60px;margin:20px;color:white;background:black;border:2px solid black;outline-offset:4px}button${permanent ? '' : ':focus-visible'}{outline:3px solid black}</style><main><button>First</button><button>Second</button></main>`;
  await page.setContent(fixture(false)); await measureFocus(page, info, 'focus-only');
  await page.setContent(fixture(true));
  await expect(measureFocus(page, info, 'permanent')).rejects.toThrow('actual same-pixel focus change');
});

test('alpha layers are composited and unsupported opacity is explicitly unmeasured', async ({ page }, info) => {
  await page.setContent('<main style="background:white"><p style="background:rgba(0,0,0,.5);color:white">White over translucent black is below 4.5</p></main>');
  await expect(measure(page, info, 'alpha-low-contrast')).rejects.toThrow('measured text');
  await page.setContent('<main style="background:white;color:black"><p>Measured opaque text</p><p style="opacity:.5">Group opacity is unsupported</p></main>');
  const result = await measure(page, info, 'unsupported-opacity', true);
  expect(result.unmeasured).toContainEqual(expect.objectContaining({ reason: expect.stringContaining('opacity') }));
});

test('critical clipped text fails while intentional field and native modal scrolling remain measured', async ({ page }, info) => {
  await page.setContent('<main style="background:white;color:black;width:100px;overflow:hidden"><span style="white-space:nowrap">A very long critical destination label</span></main>');
  await expect(measure(page, info, 'clipped-label')).rejects.toThrow('critical content clipping');
  await page.setContent('<main style="background:white;color:black;width:100px;overflow:hidden"><input aria-label="Clipped field host" style="width:200px;background:white;color:black;border:2px solid black" value="Internally scrolling value"></main>');
  await expect(measure(page, info, 'clipped-input-host')).rejects.toThrow('critical content clipping');
  await page.setContent('<main><p>Outside text</p><dialog style="height:100px;width:250px;overflow:auto;background:white;color:black"><p style="height:200px">Scrollable native dialog text remains reachable</p><textarea style="width:150px;height:30px;background:white;color:black;border:2px solid black">Long\nfield\ncontent\nscrolls</textarea></dialog></main>');
  await page.locator('dialog').evaluate((e: HTMLDialogElement) => e.showModal());
  const result = await measure(page, info, 'modal-scrolling');
  expect(result.environment.scope).toContain('active native modal only');
  expect(result.text.some(row => row.label === 'Outside text')).toBe(false);
  expect(result.unmeasured).toEqual([]);
});

test('actual native checkmark passes and a checked appearance-none fill without glyph fails', async ({ page }, info) => {
  const fixture = (missing: boolean) => `<style>main{background:white;color:black}label{display:block;min-height:58px}input{width:24px;height:24px;accent-color:rgb(23,62,96);box-shadow:inset 0 0 0 3px rgb(23,62,96);${missing ? 'appearance:none;background:white' : ''}}${missing ? 'input:checked{background:rgb(23,62,96)}' : ''}</style><main><label><input type="checkbox"> Consent</label></main>`;
  await page.setContent(fixture(false)); await measureChoices(page, info, 'native-glyph');
  await page.setContent(fixture(true));
  await expect(measureChoices(page, info, 'missing-glyph')).rejects.toThrow('actual non-boundary checkmark component');
});
