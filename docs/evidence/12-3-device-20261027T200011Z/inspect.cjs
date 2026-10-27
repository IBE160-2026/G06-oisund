const d=require('./driver.cjs');(async()=>{const{page}=await d.connect();console.log(JSON.stringify(await d.ui(page)));process.exit(0)})();
