const { chromium } = require('playwright'); const fs=require('fs'); const path=require('path');
const THREE = fs.readFileSync(__dirname+'/package/build/three.min.js','utf8');
const [file, hash, tag] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport:{width:390,height:844}, hasTouch:true, isMobile:true, deviceScaleFactor:2 });
  const p = await ctx.newPage(); const errs=[];
  p.on('console', m => { if (m.type()==='error') errs.push(m.text()); }); p.on('pageerror', e => errs.push('pageerror '+e.message));
  await p.route(/three\.min\.js/, r => r.fulfill({ body: THREE, contentType:'application/javascript' }));
  const R = {};
  await p.goto('file://'+path.resolve(file)+(hash||''));
  await p.waitForFunction('window.__sc !== undefined', null, {timeout:60000});
  await p.waitForTimeout(3000);
  R.hash = await p.evaluate('location.hash');
  R.build = await p.evaluate("__sc('GAME_BUILD')");
  if (tag==='play') {
    R.wake = await p.isVisible('#tiWake'); await p.screenshot({path:`t/${tag}-title.png`});
    await p.touchscreen.tap(195,600); await p.waitForTimeout(1500);
    R.newVisible = await p.isVisible('#tiNew'); await p.screenshot({path:`t/${tag}-title2.png`});
    await p.tap('#tiNew'); await p.waitForTimeout(2000);
  }
  R.manifest = await p.isVisible('text=Sign and go aboard'); await p.screenshot({path:`t/${tag}-manifest.png`});
  await p.fill('form input','Testa'); await p.tap('text=Sign and go aboard'); await p.waitForTimeout(4000);
  R.hud = await p.isVisible('#clock'); await p.screenshot({path:`t/${tag}-hud.png`});
  await p.evaluate("__sc(\"introFlagSet('intro.device'); deviceShow('saves'); deviceShow('saves')\")"); await p.waitForTimeout(1000);
  const txt = (await p.evaluate('document.body.innerText')).toLowerCase();
  R.download = txt.includes('download my save'); R.load = txt.includes('load a save file');
  await p.screenshot({path:`t/${tag}-saves.png`});
  if (tag==='dev') {
    await p.evaluate("__sc('devmodeOpen(true)')"); await p.waitForTimeout(800);
    const jb = await p.$('.dmTabs button[data-tab=jump]'); R.jumpTab = !!jb;
    if (jb) { await jb.click(); await p.waitForTimeout(800); R.jumpOn = await p.evaluate("!!document.querySelector('.dmTabs button[data-tab=jump].on')"); }
    await p.screenshot({path:`t/${tag}-jump.png`});
  }
  R.errors = errs; console.log(JSON.stringify(R,null,1)); await b.close();
})().catch(e => { console.error('FAIL', e); process.exit(1); });
