// Kayak prototype check (White water): NODE_PATH=$(npm root -g) node tools/kayak_proto_check.js
// Needs three.js r128 at /tmp/cadet-work/three/package/build/three.min.js (DEV_NOTES Testing: npm pack three@0.128.0).
// Paths come from this file's own place in the repo (the Lightdisc check hard-coded them).
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(ROOT, 'plans/shots-kayak') + '/';
const URL = 'file://' + path.join(ROOT, 'kayak-proto.html');
const THREE_JS = process.env.THREE_JS || '/tmp/cadet-work/three/package/build/three.min.js';
fs.mkdirSync(OUT, { recursive: true });
let fails = 0; const ok = (c, m) => { console.log((c ? 'ok   ' : 'FAIL ') + m); if (!c) fails++; };
async function page(b, vp, mobile) {
  const p = await b.newPage({ viewport: vp, deviceScaleFactor: mobile ? 2 : 1, hasTouch: mobile, isMobile: mobile });
  await p.route('**/three.min.js', r => r.fulfill({ path: THREE_JS, contentType: 'application/javascript' }));
  p.errs = []; p.on('console', m => { if (m.type() === 'error') p.errs.push(m.text()); }); p.on('pageerror', e => p.errs.push(String(e)));
  await p.goto(URL); await p.waitForFunction(() => window.KY); await p.waitForTimeout(700);
  await p.evaluate(() => { try { localStorage.clear(); } catch (e) {} });
  return p;
}
const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  // ---- phone, portrait 390x844 ----
  const p = await page(b, { width: 390, height: 844 }, true);
  await p.reload(); await p.waitForFunction(() => window.KY); await p.waitForTimeout(700);   // fresh menu (How to play ticked)
  await p.screenshot({ path: OUT + 'phone-1-menu.png' });
  await p.tap('.mode[data-m="alone"]');                     // a real tap on the menu
  await p.waitForTimeout(1200);
  ok(await p.evaluate(() => KY.state().how === 0), 'How to play starts at step 1 of 3');
  await p.screenshot({ path: OUT + 'phone-2-howto.png' });
  await p.waitForFunction(() => KY.state().phase === 'go', null, { timeout: 8000 });
  // a real thumb: down in the middle, slide to the left edge
  const cdp = await p.context().newCDPSession(p);
  const touch = (type, pts) => cdp.send('Input.dispatchTouchEvent', { type, touchPoints: pts });
  const ref = () => p.evaluate(() => { const s = KY.state().b[0], L = KY.loc(s.x, s.z); let r = Math.atan2(L.nx, -L.nz) - s.h; while (r > Math.PI) r -= 2 * Math.PI; while (r < -Math.PI) r += 2 * Math.PI; return -r; });
  await touch('touchStart', [{ x: 195, y: 740, id: 1 }]);
  for (let i = 0; i <= 10; i++) { await touch('touchMove', [{ x: 195 - i * 17, y: 740, id: 1 }]); await p.waitForTimeout(40); }
  await p.waitForTimeout(700);
  const a1 = await p.evaluate(() => KY.state().a), rel1 = await ref();
  ok(a1 < -.6, 'the thumb at the left aims you left (aim ' + a1.toFixed(2) + ')');
  ok(rel1 < -.4, 'and the kayak turns that way (' + (rel1 * 57.3).toFixed(0) + '° off the channel)');
  await touch('touchEnd', []); await p.waitForTimeout(400);
  const a2 = await p.evaluate(() => KY.state().a), r2 = await ref(); await p.waitForTimeout(500); const r3 = await ref();
  ok(Math.abs(a2 - a1) < 1e-9 && Math.abs(r3 - r2) < .06, 'lift the thumb and you hold your line (aim kept, heading ' + (r2 * 57.3).toFixed(0) + '° then ' + (r3 * 57.3).toFixed(0) + '°)');
  ok(await p.evaluate(() => KY.state().how === 1), 'How to play moves on once you steer');
  // taps are strokes
  const st0 = await p.evaluate(() => KY.state().b[0]);
  await touch('touchStart', [{ x: 195, y: 740, id: 2 }]); await p.waitForTimeout(60); await touch('touchEnd', []); await p.waitForTimeout(450);
  await touch('touchStart', [{ x: 195, y: 740, id: 3 }]); await p.waitForTimeout(60); await touch('touchEnd', []); await p.waitForTimeout(150);
  const st1 = await p.evaluate(() => KY.state().b[0]);
  ok(st1.strokes === st0.strokes + 2, 'two taps, two strong strokes (' + st0.strokes + ' → ' + st1.strokes + ')');
  ok(st1.S < st0.S - .1, 'strokes cost stamina (' + st0.S.toFixed(2) + ' → ' + st1.S.toFixed(2) + ')');
  ok(await p.evaluate(() => KY.state().how === 2), 'How to play moves on after two strokes');
  await p.tap('#howNext'); await p.waitForTimeout(200);
  ok(await p.evaluate(() => KY.state().how === -1), 'How to play ends on Done');
  // stamina rules, measured on the live go
  const fight = await p.evaluate(() => {
    const L = KY.state().loop, s = 21.3, [x, z] = KY.posAt(s, 1.35); KY.set({ x, z, s, h: Math.PI / 2, S: 1, tired: 0, u: 0 });
    const b0 = KY.state().b[0]; KY.steps(120, { a: 0 }); const b1 = KY.state().b[0]; return { w: KY.water(x, z), S0: b0.S, S1: b1.S, fight: b1.fight };
  });
  ok(fight.w.vs < -.15 && fight.S1 < fight.S0 - .2, 'fighting the bend\'s current costs stamina (' + fight.S0.toFixed(2) + ' → ' + fight.S1.toFixed(2) + ' in 2 s; the water ' + fight.w.vs.toFixed(2) + ' against you)');
  const eddy = await p.evaluate(() => {
    let best = null; for (let x = 3; x < 13.6; x += .1) for (let z = .5; z < 5.6; z += .1) { const w = KY.water(x, z); if (w.eddy > .95 && (!best || x > best[0])) best = [x, z]; }
    KY.set({ x: best[0], z: best[1], S: .3, tired: 0, u: 0 }); const L = KY.loc(best[0], best[1]); KY.set({ s: L.s, h: Math.atan2(L.nx, -L.nz) });
    const S0 = KY.state().b[0].S; KY.steps(30, { a: 0 }); return { at: best, S0, S1: KY.state().b[0].S, e: KY.state().b[0].eddy };
  });
  ok(eddy.S1 > eddy.S0 + .05, 'resting in an eddy refills it (' + eddy.S0.toFixed(2) + ' → ' + eddy.S1.toFixed(2) + ' in half a second, at ' + eddy.at.map(v => v.toFixed(1)) + ')');
  const ride = await p.evaluate(() => { const s = 14.2, [x, z] = KY.posAt(s, .8); KY.set({ x, z, s, h: 0, S: .4, tired: 0, u: .15 }); KY.steps(60, { a: 0 }); return KY.state().b[0].S; });
  ok(ride > .42, 'riding the white water refills it a little (.40 → ' + ride.toFixed(2) + ')');
  // run it dry: you drift with the current (safe, slow), slumped, then get your breath back
  const dry = await p.evaluate(() => { const s = 21.3, [x, z] = KY.posAt(s, 1.35); KY.set({ x, z, s, h: Math.PI / 2, S: .03, tired: 0, u: .1 }); KY.steps(40, { a: 0, stroke: 0 }); KY.steps(1, { a: 0, stroke: 1 }); const b = KY.state().b[0]; return b; });
  ok(dry.tired === 1 && dry.strokes === st1.strokes, 'run it dry and you\'re tired: strokes do nothing (' + dry.tiredN + ' time)');
  await p.evaluate(() => KY.steps(60)); const dr = await p.evaluate(() => KY.state().b[0]);
  ok(dr.tired === 1 && dr.u < .05 && Math.hypot(dr.x - dry.x, dr.z - dry.z) > .05, 'tired, you stop paddling and drift with the current (your paddling ' + dr.u.toFixed(3) + ', carried ' + Math.hypot(dr.x - dry.x, dr.z - dry.z).toFixed(2) + ')');
  await p.evaluate(() => { const s = 15.6, [x, z] = KY.posAt(s, .9); KY.set({ x, z, s, h: 0 }); KY.steps(20); KY.pause(true); }); await p.waitForTimeout(900);   // the shot: drifting tired in the white water
  await p.screenshot({ path: OUT + 'phone-4-tired.png' });
  ok(await p.evaluate(() => getComputedStyle(document.getElementById('stam')).display !== 'none' && document.getElementById('stam').classList.contains('tired')), 'the meter says you\'re getting your breath back');
  await p.evaluate(() => KY.pause(false));
  const back = await p.evaluate(() => { let n = 0; while (KY.state().b[0].tired && n++ < 60 * 10) KY.steps(1); return { n, b: KY.state().b[0] }; });
  ok(back.b.tired === 0 && back.n < 60 * 6, 'and you get your breath back in ' + (back.n / 60).toFixed(1) + ' s');
  // a full lap with one thumb, in real time (the test runs 4 steps a frame): the thumb follows the autopilot's advice
  await p.evaluate(() => { KY.leave(); KY.start({ mode: 'alone', how: false, seed: 3 }); KY.rate = 4; });
  let maxCalls = 0, shotW = false, taps = 0;
  await touch('touchStart', [{ x: 195, y: 740, id: 9 }]);
  for (let i = 0; i < 2400; i++) {
    const st = await p.evaluate(() => [KY.state(), KY.calls(), KY.advice()]);
    if (!st[0] || st[0].phase === 'over' || st[0].b[0].done) break;
    maxCalls = Math.max(maxCalls, st[1]);
    const x = Math.round((st[2].a / 1.2 + 1) / 2 * 390);
    await touch('touchMove', [{ x, y: 740, id: 9 }]);
    if (st[2].stroke && st[0].phase === 'go') {                  // lift and tap where the thumb is: a stroke (a tap also aims there)
      await touch('touchEnd', []); await touch('touchStart', [{ x, y: 740, id: 10 + i }]); await touch('touchEnd', []); await touch('touchStart', [{ x, y: 740, id: 9 }]); taps++;
    }
    if (!shotW && st[0].b[0].s > 15.2 && st[0].b[0].s < 17) { shotW = true; await p.evaluate(() => KY.rate = 1); await p.waitForTimeout(150); await p.screenshot({ path: OUT + 'phone-3-whitewater.png' }); await p.evaluate(() => KY.rate = 4); }
    await p.waitForTimeout(30);
  }
  await touch('touchEnd', []);
  const lap = await p.evaluate(() => KY.state());
  ok(lap.b[0].done > 0, 'a full lap with one thumb (' + (lap.b[0].done / 60).toFixed(0) + ' s of play, ' + lap.b[0].strokes + ' strokes from ' + taps + ' taps, ' + lap.b[0].tiredN + ' times out of puff)');
  ok(shotW, 'mid-run in the white water (shot)');
  ok(maxCalls > 0 && maxCalls < 200, 'draw calls in a go under 200 (max ' + maxCalls + ')');
  await p.evaluate(() => KY.rate = 1); await p.waitForTimeout(1200);
  ok(await p.isVisible('#again') && await p.isVisible('#done'), 'the result card shows Again and Done');
  const resT = await p.textContent('#result'); ok(/first lap|best lap|steady lap/i.test(resT) && !/\d+\s*(s|sec|:)/.test(resT.replace(/\d+(st|nd|rd|th)/g, '')), 'bests in words, no times: "' + resT.trim().slice(0, 90) + '"');
  await p.screenshot({ path: OUT + 'phone-5-result.png' });
  await p.tap('#again'); await p.waitForTimeout(300);
  ok(await p.evaluate(() => KY.state().phase === 'count' && KY.state().b[0].p === 0), 'Again starts a fresh go');
  await p.tap('#leave'); await p.waitForTimeout(300);
  ok(await p.isVisible('#menu'), 'Leave goes back to the menu');
  // the rules: paper, clones and frame rates
  const R = await p.evaluate(() => {
    const o = { seed: 11, crew: ['holt', 'rina'], race: true, autoYou: true };
    const paper = KY.paper(o), again = KY.paper(o);
    return { paper, again, f60: KY.fps(o, 60), f30: KY.fps(o, 30), f20: KY.fps(o, 20) };
  });
  ok(same(R.paper, R.again), 'seeded crew laps replay identically (' + R.paper.order.join(', ') + ' in ' + R.paper.steps + ' steps)');
  ok(same(R.f60, R.paper) && same(R.f30, R.paper) && same(R.f20, R.paper), 'the same go at 60, 30 and 20 fps equals the go on paper');
  // a live go (real frames at whatever rate the page gets), cloned mid-go and finished at 30 and 20 fps, equals the live go finished
  await p.evaluate(() => { KY.start({ mode: 'race', crew: ['pell', 'vance'], autoYou: true, how: false, seed: 5 }); KY.rate = 1; });
  await p.waitForTimeout(4500);
  const L = await p.evaluate(() => { KY.pause(true); const c30 = KY.fps(null, 30, true), c20 = KY.fps(null, 20, true), c60 = KY.fps(null, 60, true); const s = KY.state().step; FAST = true; while (G.phase !== 'over') kyStep(G); FAST = false; G.ev.length = 0; return { at: s, live: KY.summary(), c30, c20, c60, paper: KY.paper({ seed: 5, crew: ['pell', 'vance'], race: true, autoYou: true }) }; });
  ok(L.at > 60 && same(L.c30, L.live) && same(L.c20, L.live) && same(L.c60, L.live), 'a live go cloned at step ' + L.at + ' and run at 60, 30 and 20 fps ends the same as the live go');
  ok(same(L.live, L.paper), 'and the live go equals the same go on paper (' + L.live.order.join(', ') + ')');
  const H = await p.evaluate(() => [1, 2, 3].map(s => [KY.paper({ seed: s, crew: ['pell', 'rina', 'vance'], regatta: true, autoYou: true }).order.join(','), KY.paper({ seed: s, crew: ['pell', 'rina', 'vance'], regatta: true, autoYou: true }).order.join(',')]));
  ok(H.every(([a, c]) => a === c), 'a regatta heat\'s order is the same each time for the same seed (' + H.map(h => h[0]).join(' / ') + ')');
  // crew paddle beside you, a race, a regatta heat
  await p.evaluate(() => { KY.pause(false); KY.leave(); });
  await p.evaluate(() => { document.querySelector('#crewPick input[data-k="pell"]').checked = true; });
  await p.tap('.mode[data-m="crew"]'); await p.waitForTimeout(500);
  const cr = await p.evaluate(() => KY.state().b.map(b => b.k));
  ok(cr.length === 3 && cr[1] === 'holt' && cr[2] === 'pell', 'paddle with crew: Holt and Pell beside you (' + cr.join(', ') + ')');
  await p.evaluate(() => KY.steps(60 * 18)); await p.waitForTimeout(900);
  await p.screenshot({ path: OUT + 'phone-6-crew.png' });
  const crp = await p.evaluate(() => KY.state().b.map(b => b.p));
  ok(crp[1] > 2 && crp[2] > 2, 'the crew paddle round at their own pace');
  await p.evaluate(() => { KY.leave(); KY.start({ mode: 'regatta', autoYou: true, how: false, seed: 2 }); });
  await p.waitForTimeout(400);
  const rg = await p.evaluate(() => { const n = KY.state().b.length; KY.steps(60 * 300); return { n, st: KY.state() }; });
  await p.waitForTimeout(900);
  const rgT = await p.textContent('#result');
  ok(rg.n === 4 && rg.st.phase === 'over' && /Heat 1: 1st/.test(rgT) && /Heat 2 \(worked out on paper\)/.test(rgT), 'a regatta heat of four runs to placings, the next heat on paper');
  await p.screenshot({ path: OUT + 'phone-7-regatta.png' });
  ok(p.errs.length === 0, 'phone: no console errors ' + JSON.stringify(p.errs));
  // ---- sideways phone 844x390 ----
  const s = await page(b, { width: 844, height: 390 }, true);
  await s.reload(); await s.waitForFunction(() => window.KY); await s.waitForTimeout(700);
  await s.screenshot({ path: OUT + 'side-1-menu.png' });
  await s.evaluate(() => KY.start({ mode: 'race', crew: ['rina'], how: true, seed: 4 })); await s.waitForTimeout(1200);
  await s.screenshot({ path: OUT + 'side-2-howto.png' });
  await s.tap('#howSkip'); await s.waitForTimeout(200);
  await s.evaluate(() => { G.b[0].ai = 'auto'; KY.steps(60 * 3); let n = 0; while (KY.state().b[0].s < 15.4 && n++ < 60 * 120) KY.steps(1); });
  await s.waitForTimeout(1200); await s.screenshot({ path: OUT + 'side-3-whitewater.png' });
  await s.evaluate(() => { KY.set({ S: 0, tired: 1 }); KY.steps(30); KY.pause(true); }); await s.waitForTimeout(900);
  ok(await s.evaluate(() => KY.state().b[0].tired === 1), 'sideways: tired and drifting');
  await s.screenshot({ path: OUT + 'side-4-tired.png' });
  await s.evaluate(() => { KY.pause(false); KY.steps(60 * 300); }); await s.waitForTimeout(1000);
  await s.screenshot({ path: OUT + 'side-5-result.png' });
  ok(await s.isVisible('#again'), 'sideways: the result card');
  ok(s.errs.length === 0, 'sideways: no console errors ' + JSON.stringify(s.errs));
  // ---- desktop: mouse, keys, reduced motion ----
  const d = await page(b, { width: 1280, height: 800 }, false);
  await d.check('#rm'); await d.click('.mode[data-m="alone"]'); await d.waitForTimeout(400);
  await d.evaluate(() => { G.how = -1; KY.steps(200); });
  await d.keyboard.down('ArrowRight'); await d.waitForTimeout(600); const ka = await d.evaluate(() => KY.state().a); await d.keyboard.up('ArrowRight');
  ok(ka > .3, 'arrow keys aim you (aim ' + ka.toFixed(2) + ')');
  await d.mouse.move(80, 500); await d.waitForTimeout(200);
  ok(await d.evaluate(() => KY.state().a < -.8), 'the mouse aims you');
  const k0 = await d.evaluate(() => KY.state().b[0].strokes); await d.keyboard.press(' '); await d.waitForTimeout(200);
  ok(await d.evaluate(() => KY.state().b[0].strokes) === k0 + 1, 'Space is a stroke');
  ok(await d.evaluate(() => RM === true && camT === 1), 'reduced motion: the camera cuts instead of easing');
  await d.screenshot({ path: OUT + 'desk-1-go.png' });
  ok(d.errs.length === 0, 'desktop: no console errors ' + JSON.stringify(d.errs));
  console.log(fails ? fails + ' FAILED' : 'ALL OK');
  await b.close();
  process.exit(fails ? 1 : 0);
})();
