// Lightdisc prototype check: NODE_PATH=$(npm root -g) node tools/lightdisc_proto_check.js
// Needs three.js r128 at /tmp/cadet-work/three/package/build/three.min.js (DEV_NOTES Testing: npm pack three@0.128.0).
const { chromium } = require('playwright');
const OUT = '/home/user/Cadet-game/plans/shots-lightdisc/';
const URL = 'file:///home/user/Cadet-game/lightdisc-proto.html';
let fails = 0; const ok = (c, m) => { console.log((c ? 'ok   ' : 'FAIL ') + m); if (!c) fails++; };
async function page(b, vp, mobile) {
  const p = await b.newPage({ viewport: vp, deviceScaleFactor: mobile ? 2 : 1, hasTouch: mobile, isMobile: mobile });
  await p.route('**/three.min.js', r => r.fulfill({ path: '/tmp/cadet-work/three/package/build/three.min.js', contentType: 'application/javascript' }));
  p.errs = []; p.on('console', m => { if (m.type() === 'error') p.errs.push(m.text()); }); p.on('pageerror', e => p.errs.push(String(e)));
  await p.goto(URL); await p.waitForFunction(() => window.LD); await p.waitForTimeout(600);
  return p;
}
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  // ---- phone, portrait 390x844 ----
  const p = await page(b, { width: 390, height: 844 }, true);
  await p.screenshot({ path: OUT + 'phone-1-menu.png' });
  await p.tap('.opp[data-k="pell"]');                       // a real tap on the picker
  await p.waitForTimeout(1200);
  ok(await p.evaluate(() => LD.state().how === 0), 'How to play starts at step 1');
  await p.screenshot({ path: OUT + 'phone-2-howto.png' });
  // thumb drag: put the thumb down at the right of the screen and drag to the left edge
  const cdp = await p.context().newCDPSession(p);
  const touch = (type, x, y) => cdp.send('Input.dispatchTouchEvent', { type, touchPoints: type === 'touchEnd' ? [] : [{ x, y }] });
  await touch('touchStart', 300, 760);
  for (let i = 0; i <= 10; i++) { await touch('touchMove', 300 - i * 29, 760 - i * 4); await p.waitForTimeout(40); }
  await p.waitForTimeout(500);
  const s1 = await p.evaluate(() => LD.state());
  ok(s1.you.x < -1.9, 'thumb at the left edge puts you at the left of the court (x=' + s1.you.x.toFixed(2) + ')');
  ok(s1.you.z < 6.1, 'dragging up moves you forward (z=' + s1.you.z.toFixed(2) + ')');
  await touch('touchEnd'); await p.waitForTimeout(300);
  const xa = (await p.evaluate(() => LD.state())).you.x; await p.waitForTimeout(400);
  ok(Math.abs((await p.evaluate(() => LD.state())).you.x - xa) < 1e-6, 'lift the thumb and you stop');
  ok(await p.evaluate(() => LD.state().how !== 0), 'How to play moves on once you move');
  // play live for a few seconds with the thumb following the disc (a crude human)
  let maxCalls = 0;
  await touch('touchStart', 195, 760);
  for (let i = 0; i < 240; i++) {
    if (i > 90 && (await p.evaluate(() => LD.state().you.hits)) > 0) break;
    const st = await p.evaluate(() => [LD.state(), LD.calls()]); maxCalls = Math.max(maxCalls, st[1]);
    const x = Math.max(5, Math.min(385, (st[0].disc.x / (2.25 * 1.12) + 1) / 2 * 390));
    await touch('touchMove', x, 760); await p.waitForTimeout(60);
    if (i === 40) await p.screenshot({ path: OUT + 'phone-3-rally.png' });
  }
  await touch('touchEnd');
  const s2 = await p.evaluate(() => LD.state());
  ok(s2.you.hits > 0, 'you returned the disc by standing in its way (' + s2.you.hits + ' returns, score ' + s2.score.join(':') + ')');
  ok(maxCalls > 0 && maxCalls < 60, 'draw calls in the game view under 60 (max ' + maxCalls + ')');
  // a scripted game to the end: your side on autopilot, run in fixed steps
  await p.evaluate(() => LD.start({ opp: 'rina', seed: 4, autoYou: true, how: false }));
  await p.waitForTimeout(900);
  await p.evaluate(() => LD.steps(60 * 25));
  await p.waitForTimeout(300);
  await p.screenshot({ path: OUT + 'phone-4-midgame.png' });
  const fin = await p.evaluate(() => LD.steps(60 * 60 * 30));
  ok(fin.phase === 'over' && fin.over, 'scripted game reached the end: ' + fin.score.join(':'));
  const [a, c] = fin.score; ok(Math.max(a, c) >= 7 && Math.abs(a - c) >= 2, 'first to 7, win by 2');
  await p.waitForTimeout(1000);
  ok(await p.isVisible('#again') && await p.isVisible('#done'), 'result shows Again and Leave');
  await p.screenshot({ path: OUT + 'phone-5-result.png' });
  await p.tap('#again'); await p.waitForTimeout(400);
  ok(await p.evaluate(() => LD.state().phase === 'serve' && LD.state().score.join() === '0,0'), 'Again starts a fresh game');
  await p.tap('#leave'); await p.waitForTimeout(400);
  ok(await p.isVisible('#menu'), 'Leave goes back to the picker');
  // quick game
  const q = await p.evaluate(() => LD.paper({ opp: 'holt', seed: 9, autoYou: true, quick: true }));
  ok(Math.max(...q.score) >= 5 && Math.max(...q.score) <= 7 || Math.abs(q.score[0] - q.score[1]) === 2, 'quick game to 5: ' + q.score.join(':'));
  // crew v crew: same seed, same game; different frame rates, same game
  const w1 = await p.evaluate(() => LD.paper({ watch: ['holt', 'rina'], seed: 12 }));
  const w2 = await p.evaluate(() => LD.paper({ watch: ['holt', 'rina'], seed: 12 }));
  ok(JSON.stringify(w1) === JSON.stringify(w2), 'crew v crew replays the same (' + w1.score.join(':') + ' in ' + w1.steps + ' steps)');
  await p.selectOption('#wa', 'vance'); await p.selectOption('#wb', 'pell'); await p.tap('#watch');
  await p.waitForTimeout(1500);
  await p.evaluate(() => LD.steps(60 * 8)); await p.waitForTimeout(700);
  await p.screenshot({ path: OUT + 'phone-6-watch.png' });
  // the live game (frame by frame, real time) and a paper game end up the same
  const live = await p.evaluate(() => { LD.leave(); LD.start({ watch: ['pell', 'holt'], seed: 21 }); return 1; });
  await p.evaluate(() => LD.steps(1)); await p.waitForTimeout(3000);                 // real frames at whatever rate the page gets
  const livePart = await p.evaluate(() => LD.steps(60 * 60 * 30));
  const paperAll = await p.evaluate(() => LD.paper({ watch: ['pell', 'holt'], seed: 21 }));
  ok(livePart.score.join() === paperAll.score.join() && livePart.step === paperAll.steps, 'frame rate does not change the game (' + livePart.score.join(':') + ', ' + livePart.step + ' steps both ways)');
  ok(p.errs.length === 0, 'phone: no console errors ' + JSON.stringify(p.errs));
  // landscape phone
  await p.setViewportSize({ width: 844, height: 390 });
  await p.evaluate(() => { LD.leave(); LD.start({ opp: 'vance', seed: 2, how: false }); });
  await p.waitForTimeout(2600);
  await p.screenshot({ path: OUT + 'phone-7-sideways.png' });
  // ---- desktop ----
  const d = await page(b, { width: 1280, height: 800 }, false);
  await d.screenshot({ path: OUT + 'desk-1-menu.png' });
  await d.check('#rm'); await d.click('.opp[data-k="holt"]'); await d.waitForTimeout(1200);
  await d.keyboard.down('ArrowLeft'); await d.waitForTimeout(500); await d.keyboard.up('ArrowLeft');
  const k1 = await d.evaluate(() => LD.state());
  ok(k1.you.x < -1, 'arrow keys move you (x=' + k1.you.x.toFixed(2) + ')');
  await d.mouse.move(1100, 500); await d.waitForTimeout(500);
  const k2 = await d.evaluate(() => LD.state());
  ok(k2.you.x > 1, 'the mouse moves you (x=' + k2.you.x.toFixed(2) + ')');
  await d.waitForTimeout(1500);
  await d.screenshot({ path: OUT + 'desk-2-game.png' });
  ok(await d.evaluate(() => RM === true && camT === 1), 'reduced motion: the camera cuts instead of easing');
  await d.evaluate(() => LD.steps(60 * 20)); ok(d.errs.length === 0, 'reduced motion game runs');
  ok(d.errs.length === 0, 'desktop: no console errors ' + JSON.stringify(d.errs));
  console.log(fails ? fails + ' FAILED' : 'ALL OK');
  await b.close();
})();
