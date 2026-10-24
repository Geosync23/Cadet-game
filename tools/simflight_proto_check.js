// Sim flight prototype check: NODE_PATH=$(npm root -g) node tools/simflight_proto_check.js
// Needs three.js r128 at /tmp/cadet-work/three/package/build/three.min.js (DEV_NOTES Testing: npm pack three@0.128.0).
// Phone (390x844, touch) and wide (1280x800, mouse and keys): the start card, the three tips (Next, Skip, once
// only), a one-finger drag steers and letting go levels out, draw calls, the three endings from scripted pilots
// (steady: soft; steep dive: hard; drift: miss), each the same twice, about a minute a go; right on the screen is
// right (the Tern is projected to the screen); screenshots.
const { chromium } = require('playwright');
const path = require('path'), ROOT = path.join(__dirname, '..');
const OUT = path.join(ROOT, 'plans/shots-simflight') + '/';
const URL = 'file://' + path.join(ROOT, 'simflight-proto.html');
let fails = 0; const ok = (c, m) => { console.log((c ? 'ok   ' : 'FAIL ') + m); if (!c) fails++; };
async function page(ctx) {
  const p = await ctx.newPage();
  await p.route('**/three.min.js', r => r.fulfill({ path: '/tmp/cadet-work/three/package/build/three.min.js', contentType: 'application/javascript' }));
  p.errs = []; p.on('console', m => { if (m.type() === 'error') p.errs.push(m.text()); }); p.on('pageerror', e => p.errs.push(String(e)));
  await p.goto(URL); await p.waitForFunction(() => window.FL); await p.waitForTimeout(500);
  return p;
}
const vis = (p, id) => p.evaluate(i => !document.getElementById(i).classList.contains('hide'), id);
async function land(p, name, shot) {                  // a live go flown by a scripted pilot: jump most of the way on paper, the rest in real frames
  await p.evaluate(() => FL.start()); await p.evaluate(n => { FL.jump(n, FL.BAY_Z - 40); FL.pilot(n); }, name);
  if (shot) await p.screenshot({ path: OUT + shot + '-bay.png' });
  await p.waitForFunction(() => !document.getElementById('result').classList.contains('hide'), null, { timeout: 30000 });
  await p.evaluate(() => FL.pilot(null));
  const t = await p.evaluate(() => [document.getElementById('resText').textContent, document.getElementById('again').textContent, FL.state().end]);
  if (shot) await p.screenshot({ path: OUT + shot + '-result.png' });
  return t;
}
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  // ---- the rules on paper ----
  {
    const p = await page(await b.newContext());
    for (const [n, want] of [['steady', 'soft'], ['dive', 'hard'], ['drift', 'miss']]) {
      const a = await p.evaluate(x => FL.sim(x), n), a2 = await p.evaluate(x => FL.sim(x), n);
      console.log(`     ${n}: ${JSON.stringify(a)}`);
      ok(a.end === want, `the ${n} pilot: ${a.end} (want ${want})`);
      ok(JSON.stringify(a) === JSON.stringify(a2), `the ${n} pilot flies the same twice`);
      ok(a.secs >= 45 && a.secs <= 90, `the ${n} go takes about a minute (${a.secs} s)`);
    }
    await p.close();
  }
  // ---- phone, portrait 390x844, touch ----
  const ctxP = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, hasTouch: true, isMobile: true });
  const p = await page(ctxP);
  await p.screenshot({ path: OUT + 'phone-1-start.png' });
  await p.tap('#start'); await p.waitForTimeout(400);
  ok(await vis(p, 'tip') && (await p.evaluate(() => FL.state().tip)) === 0, 'the first go shows tip 1 of 3');
  await p.screenshot({ path: OUT + 'phone-2-tip.png' });
  const z0 = await p.evaluate(() => FL.state().z); await p.waitForTimeout(500);
  ok((await p.evaluate(() => FL.state().z)) === z0, 'the Tern waits while a tip shows');
  await p.tap('#tipNext'); await p.tap('#tipNext');
  ok((await p.evaluate(() => document.getElementById('tipNext').textContent)) === 'Fly', 'the third tip says Fly');
  await p.tap('#tipNext'); await p.waitForTimeout(300);
  ok(!(await vis(p, 'tip')) && (await p.evaluate(() => FL.state().tip)) === -1, 'the tips are done and the go starts');
  const cdp = await ctxP.newCDPSession(p);
  const touch = (type, x, y) => cdp.send('Input.dispatchTouchEvent', { type, touchPoints: type === 'touchEnd' ? [] : [{ x, y }] });
  await touch('touchStart', 200, 600);
  for (let i = 0; i <= 8; i++) { await touch('touchMove', 200 + i * 12, 600 - i * 12); await p.waitForTimeout(30); }
  await p.waitForTimeout(1200);
  const s1 = await p.evaluate(() => FL.state());
  const sx = await p.evaluate(() => FL.screenX());
  ok(s1.vy > 2 && Math.abs(s1.vx) > 3, `a finger dragged up climbs and turns (vx ${s1.vx.toFixed(1)}, vy ${s1.vy.toFixed(1)})`);
  await p.waitForTimeout(800); const sx2 = await p.evaluate(() => FL.screenX());
  ok(sx > 390 / 2 + 20 && sx2 >= sx, `dragging right moves the Tern right on the screen (x ${sx.toFixed(0)} -> ${sx2.toFixed(0)} px of 390)`);
  await p.screenshot({ path: OUT + 'phone-3-flying.png' });
  await touch('touchEnd'); await p.waitForTimeout(2500);
  const s2 = await p.evaluate(() => FL.state());
  ok(Math.abs(s2.vx) < 1 && Math.abs(s2.vy) < 1, `letting go levels out (vx ${s2.vx.toFixed(2)}, vy ${s2.vy.toFixed(2)})`);
  const calls = await p.evaluate(() => FL.calls());
  ok(calls <= 25, `draw calls while flying: ${calls} (under 25)`);
  await p.evaluate(() => FL.jump('steady', 300)); await p.waitForTimeout(400);
  await p.screenshot({ path: OUT + 'phone-4-rings.png' });
  let r = await land(p, 'steady', 'phone-5-soft');
  ok(r[2] === 'soft' && /Soft landing/.test(r[0]) && r[1] === 'Again', `steady, live: "${r[0]}" [${r[1]}]`);
  r = await land(p, 'dive', 'phone-6-hard');
  ok(r[2] === 'hard' && /Hard landing/.test(r[0]), `steep dive, live: "${r[0]}"`);
  r = await land(p, 'drift', 'phone-7-miss');
  ok(r[2] === 'miss' && /overshoot/.test(r[0]) && r[1] === 'Try again', `drift, live: "${r[0]}" [${r[1]}]`);
  await p.tap('#again'); await p.waitForTimeout(300);
  ok(!(await vis(p, 'tip')), 'the tips show only the first time');
  await p.tap('#leave'); await p.waitForTimeout(200);
  ok(await vis(p, 'menu'), 'Leave goes back to the start card');
  ok(!p.errs.length, 'phone: no page errors ' + p.errs.join(' | '));
  // ---- wide, mouse and keys ----
  const ctxW = await b.newContext({ viewport: { width: 1280, height: 800 } });
  const w = await page(ctxW);
  await w.click('#start'); await w.waitForTimeout(200); await w.click('#tipSkip'); await w.waitForTimeout(200);
  ok((await w.evaluate(() => FL.state().tip)) === -1, 'Skip ends the tips');
  await w.mouse.move(640, 400); await w.mouse.down(); await w.mouse.move(540, 400, { steps: 6 }); await w.waitForTimeout(1200);
  const m = await w.evaluate(() => FL.state()); await w.mouse.up();
  const mx = await w.evaluate(() => FL.screenX());
  ok(Math.abs(m.vx) > 3 && mx < 640 - 10, `a mouse drag left moves the Tern left on the screen (x ${mx.toFixed(0)} of 1280)`);
  await w.waitForTimeout(2500); await w.keyboard.down('ArrowRight'); await w.waitForTimeout(1500);
  const kr = await w.evaluate(() => FL.screenX()); await w.keyboard.up('ArrowRight');
  ok(kr > 640 + 10, `the right arrow moves the Tern right on the screen (x ${kr.toFixed(0)} of 1280)`);
  await w.waitForTimeout(2500); await w.keyboard.down('ArrowDown'); await w.waitForTimeout(1200);
  const k = await w.evaluate(() => FL.state()); await w.keyboard.up('ArrowDown');
  ok(k.vy < -2, `the down arrow descends (vy ${k.vy.toFixed(1)})`);
  await w.screenshot({ path: OUT + 'wide-1-flying.png' });
  r = await land(w, 'steady', 'wide-2-soft');
  ok(r[2] === 'soft', 'wide: steady lands soft');
  await w.click('#done'); await w.waitForTimeout(200);
  ok(await vis(w, 'menu'), 'Done goes back to the start card');
  await w.check('#tipsAgain'); await w.click('#start'); await w.waitForTimeout(200);
  ok(await vis(w, 'tip'), '"Show the tips again" shows them');
  ok(!w.errs.length, 'wide: no page errors ' + w.errs.join(' | '));
  await b.close();
  console.log(fails ? `SIMFLIGHT CHECK FAILED (${fails})` : 'SIMFLIGHT CHECK OK');
  process.exit(fails ? 1 : 0);
})();
