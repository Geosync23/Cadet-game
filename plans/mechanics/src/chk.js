const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 390, height: 800 } });
for (const f of process.argv.slice(2)) { await p.goto('file://' + f); const r = await p.evaluate(() => [document.documentElement.scrollWidth, document.title, document.body.innerText.length]); console.log(f.split('/').pop(), r.join(' ')); }
await b.close(); })();
