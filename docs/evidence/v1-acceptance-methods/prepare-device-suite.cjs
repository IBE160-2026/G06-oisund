const fs=require('node:fs'),path=require('node:path');
const root=process.cwd(),dir=path.join(root,'frontend/.v1followup-tests');
for(const name of fs.readdirSync(dir).filter(n=>n.endsWith('.ts')&&n!=='device-fixture.ts')){
 const file=path.join(dir,name);fs.writeFileSync(file,fs.readFileSync(file,'utf8').replaceAll("from '@playwright/test'","from './device-fixture'"));
}
fs.writeFileSync(path.join(dir,'device-fixture.ts'),`
import {test as base,chromium} from '@playwright/test';
export * from '@playwright/test';
export const test=base.extend({
 browser:[async({},use)=>{const browser=await chromium.connectOverCDP(process.env.V1_DEVICE_ENDPOINT!);await use(browser);await browser.close();},{scope:'worker'}],
 context:async({browser},use)=>{const context=await browser.newContext({viewport:null});await use(context);await context.close();},
 page:async({context},use)=>{const page=await context.newPage();await page.bringToFront();await use(page);await page.close();}
});
`);
fs.writeFileSync(path.join(root,'frontend/playwright.v1-device-temp.config.ts'),`
import {defineConfig} from '@playwright/test';
export default defineConfig({testDir:'./.v1followup-tests',workers:1,timeout:120000,reporter:[['line'],['json',{outputFile:process.env.V1FOLLOWUP_REPORT}]],outputDir:process.env.V1FOLLOWUP_OUTPUT_DIR,use:{baseURL:'http://127.0.0.1:15326',viewport:null,trace:'retain-on-failure'}});
`);
