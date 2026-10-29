
import {defineConfig} from '@playwright/test';
export default defineConfig({testDir:'./.v1followup-tests',workers:1,timeout:120000,reporter:[['line'],['json',{outputFile:process.env.V1FOLLOWUP_REPORT}]],outputDir:process.env.V1FOLLOWUP_OUTPUT_DIR,use:{baseURL:'http://127.0.0.1:15326',viewport:null,trace:'retain-on-failure'}});
