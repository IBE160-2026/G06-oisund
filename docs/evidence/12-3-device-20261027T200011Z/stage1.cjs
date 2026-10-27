const d=require('./driver.cjs');(async()=>{const {page,cdp}=await d.connect();
await d.record('Private login screen Night actual rendered measurements',()=>d.measure(page,'login-night'));
await d.record('Night persists after real Brave reload',async()=>{await page.reload();await d.expect(d.button(page,'Nattmodus')).toHaveAttribute('aria-pressed','true')});
await d.record('Day via injected touch and rendered measurements',async()=>{await d.tap(page,cdp,d.button(page,'Nattmodus'));await d.expect(d.button(page,'Nattmodus')).toHaveAttribute('aria-pressed','false');return d.measure(page,'login-day')});
d.write('login-ui.json',await d.ui(page));await d.shot(page,'login-day');process.exit(0)})().catch(e=>{d.write('stage1-error.txt',e.stack);console.error('Stage1 failed; see redacted record');process.exit(1)});
