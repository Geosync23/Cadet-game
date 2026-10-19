// Pool prototype check (Lengths): NODE_PATH=$(npm root -g) node tools/pool_proto_check.js
// Needs three.js r128 at /tmp/cadet-work/three/package/build/three.min.js (or THREE_JS=path). Paths come from the repo.
// Rhythm needs exact timing, which a software renderer's frames can't give: so the touch tests pause the frame loop,
// step the go to the moment (PL.toBeat / PL.toWall), make a real touch, and step on with it (PL.live).
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(ROOT, 'plans/shots-pool') + '/';
const URL = 'file://' + path.join(ROOT, 'pool-proto.html');
const THREE_JS = process.env.THREE_JS || '/tmp/cadet-work/three/package/build/three.min.js';
fs.mkdirSync(OUT, { recursive: true });
let fails = 0; const ok = (c, m) => { console.log((c ? 'ok   ' : 'FAIL ') + m); if (!c) fails++; };
async function page(b, vp, mobile) {
  const p = await b.newPage({ viewport: vp, deviceScaleFactor: mobile ? 2 : 1, hasTouch: mobile, isMobile: mobile });
  await p.route('**/three.min.js', r => r.fulfill({ path: THREE_JS, contentType: 'application/javascript' }));
  p.errs = []; p.on('console', m => { if (m.type() === 'error') p.errs.push(m.text()); }); p.on('pageerror', e => p.errs.push(String(e)));
  await p.goto(URL); await p.waitForFunction(() => window.PL);
  await p.evaluate(() => { try { localStorage.clear(); } catch (e) {} }); await p.reload(); await p.waitForFunction(() => window.PL); await p.waitForTimeout(700);
  return p;
}
const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  // ---- phone, portrait 390x844 ----
  const p = await page(b, { width: 390, height: 844 }, true);
  await p.screenshot({ path: OUT + 'phone-1-menu.png' });
  await p.tap('.mode[data-m="alone"]'); await p.waitForTimeout(1300);
  ok(await p.evaluate(() => PL.state().how === 0), 'How to play starts at step 1 of 3');
  const cdp = await p.context().newCDPSession(p);
  const touch = (type, pts) => cdp.send('Input.dispatchTouchEvent', { type, touchPoints: pts });
  let tid = 1;
  const tap = async () => { const id = tid++; await touch('touchStart', [{ x: 200, y: 700, id }]); await touch('touchEnd', []); };
  await p.evaluate(() => { PL.pause(true); PL.toBeat(.5); PL.pause(false); }); await p.waitForTimeout(500);
  await p.evaluate(() => PL.pause(true));
  await p.screenshot({ path: OUT + 'phone-2-howto.png' });
  // a tap on the beat: a clean stroke
  const s0 = await p.evaluate(() => { const s = PL.state().s[0]; if (s.breathBeat) PL.steps(80); return PL.toBeat(.005).s[0]; });
  await tap(); const s1 = await p.evaluate(() => PL.live(2).s[0]);
  ok(s1.clean === s0.clean + 1, 'a real tap on the beat is a clean stroke (' + s1.lastJ + ')');
  ok(s1.v > s0.v + .3, 'and it pushes you on (' + s0.v.toFixed(2) + ' → ' + s1.v.toFixed(2) + ' m/s)');
  // a tap well off the beat: a splash
  const s2 = await p.evaluate(() => { let st = PL.state().s[0]; let n = 0; while ((st.breathBeat || st.used) && n++ < 400) { PL.steps(5); st = PL.state().s[0]; } return PL.toBeat(.6).s[0]; });
  await tap(); const s3 = await p.evaluate(() => PL.live(2).s[0]);
  ok(s3.splash === s2.splash + 1 && s3.lastJ === 'splash', 'a tap well before the beat is a splash');
  ok(s3.flow === 0, 'and it breaks your rhythm');
  // a breath: hold through the blue ring
  const b0 = await p.evaluate(() => { let n = 0; while (!PL.state().s[0].breathBeat && n++ < 1000) PL.steps(1); return PL.toBeat(.005).s[0]; });
  ok(b0.breathBeat, 'every few strokes the ring is a breath');
  await p.evaluate(() => PL.set({ air: .4 }));
  const id = tid++; await touch('touchStart', [{ x: 200, y: 700, id }]);
  const b1 = await p.evaluate(() => PL.live(40).s[0]); await touch('touchEnd', []); const b2 = await p.evaluate(() => PL.live(2).s[0]);
  ok(b2.breaths === b0.breaths + 1 && b2.air > .99, 'holding the thumb down through it is a breath (air ' + b2.air.toFixed(2) + ')');
  // skipping breaths: you run out of air and stop to catch it (no failing, just slow)
  const g = await p.evaluate(() => { PL.set({ air: .3 }); let n = 0; while (PL.state().s[0].phase !== 'gasp' && n++ < 1500) PL.steps(1); const a = PL.state().s[0]; PL.pause(false); return a; });
  ok(g.phase === 'gasp' && g.gasps === 1, 'miss your breaths and you stop to catch your breath');
  await p.waitForTimeout(700); await p.evaluate(() => PL.pause(true));
  await p.screenshot({ path: OUT + 'phone-5-gasp.png' });
  const g2 = await p.evaluate(() => { let n = 0; while (PL.state().s[0].phase === 'gasp' && n++ < 600) PL.steps(1); return { n, s: PL.state().s[0] }; });
  ok(g2.s.phase === 'swim' && g2.n < 60 * 2, 'then swim on (' + (g2.n / 60).toFixed(1) + ' s later)');
  // a turn: swipe up near the wall
  const w0 = await p.evaluate(() => PL.toWall(.45).s[0]);
  await p.evaluate(() => { PL.pause(false); }); await p.waitForTimeout(400); await p.evaluate(() => PL.pause(true));
  ok(await p.isVisible('#turn'), 'near the wall: "Swipe up to turn"');
  await p.screenshot({ path: OUT + 'phone-4-turn.png' });
  await p.evaluate(() => { const s = PL.state().s[0]; if (s.wall > .45) PL.toWall(.45); });
  const sid = tid++; await touch('touchStart', [{ x: 200, y: 720, id: sid }]); for (let k = 1; k <= 5; k++) await touch('touchMove', [{ x: 200, y: 720 - k * 18, id: sid }]); await touch('touchEnd', []);
  const w1 = await p.evaluate(() => PL.live(2).s[0]);
  ok(w1.turns.length === w0.turns.length + 1 && w1.turns[w1.turns.length - 1] > .7, 'a real swipe up turns you, close to the wall (quality ' + w1.turns[w1.turns.length - 1] + ')');
  const w2 = await p.evaluate(() => PL.live(60).s[0]);
  ok(w2.dir === -w0.dir && w2.len === w0.len + 1, 'you push off the other way: length ' + (w2.len + 1));
  // a whole swim with one thumb: real taps on each beat, a held thumb for each breath, a swipe at each wall
  await p.evaluate(() => { PL.leave(); PL.start({ mode: 'alone', how: false, seed: 3 }); PL.pause(true); PL.steps(150); });
  let maxCalls = 0, shot = false;
  for (let i = 0; i < 400; i++) {
    const s = await p.evaluate(() => PL.state().s[0]);
    if (s.done) break;
    if (s.len < 3 && s.wall < 1.2 && s.phase === 'swim') { await p.evaluate(() => PL.toWall(.4)); const id = tid++; await touch('touchStart', [{ x: 200, y: 720, id }]); for (let k = 1; k <= 4; k++) await touch('touchMove', [{ x: 200, y: 720 - k * 20, id }]); await touch('touchEnd', []); await p.evaluate(() => PL.live(50)); continue; }
    const st = await p.evaluate(() => PL.toBeat(.005).s[0]);
    if (st.done || st.len < 3 && st.wall < 1.2) continue;
    const id = tid++; await touch('touchStart', [{ x: 200, y: 700, id }]);
    if (st.breathBeat) await p.evaluate(() => PL.live(35));
    else await p.evaluate(() => PL.live(1));
    await touch('touchEnd', []); await p.evaluate(() => PL.live(2));
    if (!shot && st.len === 1 && st.wall < 4) { shot = true; await p.evaluate(() => { PL.pause(false); }); await p.waitForTimeout(250); maxCalls = Math.max(maxCalls, await p.evaluate(() => PL.calls())); await p.evaluate(() => PL.pause(true)); await p.screenshot({ path: OUT + 'phone-3-swim.png' }); }
  }
  const fin = await p.evaluate(() => PL.state().s[0]);
  ok(fin.done > 0, 'four lengths with one thumb (' + ((fin.done / 60) - 2.5).toFixed(0) + ' s of swimming: ' + fin.clean + ' clean, ' + fin.splash + ' splashes, ' + fin.breaths + ' breaths, turns ' + fin.turns.join('/') + ')');
  ok(shot && maxCalls > 0 && maxCalls < 200, 'draw calls under 200 (' + maxCalls + ')');
  await p.evaluate(() => { PL.pause(false); PL.steps(60 * 5); }); await p.waitForTimeout(900);
  const rt = await p.textContent('#result');
  ok(await p.isVisible('#again') && /Four lengths/.test(rt) && /first four lengths|best/.test(rt), 'the result card in words: "' + rt.trim().replace(/\s+/g, ' ').slice(0, 110) + '"');
  ok(!/\d+\s*(s\b|sec|:\d)/.test(rt), 'no times on the result');
  await p.screenshot({ path: OUT + 'phone-6-result.png' });
  await p.tap('#again'); await p.waitForTimeout(300);
  ok(await p.evaluate(() => PL.state().phase === 'count' && PL.state().s[0].len === 0), 'Again starts a fresh swim');
  await p.tap('#leave'); await p.waitForTimeout(300);
  ok(await p.isVisible('#menu'), 'Leave goes back to the menu');
  // the rules: paper, clones and frame rates
  const R = await p.evaluate(() => { const o = { seed: 11, crew: ['rina', 'tomas', 'pell'], race: true, autoYou: true }; return { paper: PL.paper(o), again: PL.paper(o), f60: PL.fps(o, 60), f30: PL.fps(o, 30), f20: PL.fps(o, 20) }; });
  ok(same(R.paper, R.again), 'seeded swims replay identically (' + R.paper.order.join(', ') + ')');
  ok(same(R.f60, R.paper) && same(R.f30, R.paper) && same(R.f20, R.paper), 'the same go at 60, 30 and 20 fps equals the go on paper');
  await p.evaluate(() => { PL.start({ mode: 'race', autoYou: true, how: false, seed: 5 }); PL.rate = 1; });
  await p.waitForTimeout(5000);
  const L = await p.evaluate(() => { PL.pause(true); const c30 = PL.fps(null, 30, true), c20 = PL.fps(null, 20, true), c60 = PL.fps(null, 60, true), at = PL.state().step; FAST = true; while (G.phase !== 'over') plStep(G); FAST = false; G.ev.length = 0; return { at, live: PL.summary(), c30, c20, c60, paper: PL.paper({ seed: 5, crew: ['rina', 'tomas', 'pell'], race: true, autoYou: true }) }; });
  ok(L.at > 60 && same(L.c30, L.live) && same(L.c20, L.live) && same(L.c60, L.live), 'a live go cloned at step ' + L.at + ' and run at 60, 30 and 20 fps ends the same as the live go');
  ok(same(L.live, L.paper), 'and the live go equals the same go on paper');
  // crew in the other lanes; a race; Dawn swim with Rina
  await p.evaluate(() => { PL.pause(false); PL.leave(); });
  await p.tap('.mode[data-m="crew"]'); await p.waitForTimeout(400);
  const cr = await p.evaluate(() => PL.state().s.map(s => s.k + ':' + s.lane));
  ok(cr.length === 4 && new Set(cr.map(c => c.split(':')[1])).size === 4, 'swim with crew: three crew, one a lane (' + cr.join(', ') + ')');
  await p.evaluate(() => { G.s[0].ai = 'auto'; G.how = -1; howShow(); PL.steps(60 * 9); }); await p.waitForTimeout(1200);
  await p.screenshot({ path: OUT + 'phone-7-crew.png' });
  await p.evaluate(() => { PL.leave(); PL.start({ mode: 'race', autoYou: true, how: false, seed: 2 }); PL.steps(60 * 300); }); await p.waitForTimeout(800);
  ok(/won the race/.test(await p.textContent('#resT')), 'a race ends in placings in words: "' + await p.textContent('#resT') + '"');
  const D = await p.evaluate(() => { PL.leave(); PL.start({ mode: 'dawn', autoYou: true, how: false, seed: 4 }); const k = PL.state().s.map(s => s.k); PL.steps(60 * 300); return k; }); await p.waitForTimeout(800);
  const dt = await p.textContent('#resT');
  ok(D.join() === 'you,rina' && /Rina/.test(dt), 'Dawn swim: Rina in the next lane, keeping with her in words: "' + dt + '"');
  await p.screenshot({ path: OUT + 'phone-8-dawn.png' });
  ok(p.errs.length === 0, 'phone: no console errors ' + JSON.stringify(p.errs));
  // ---- sideways phone 844x390 ----
  const s = await page(b, { width: 844, height: 390 }, true);
  await s.screenshot({ path: OUT + 'side-1-menu.png' });
  await s.evaluate(() => PL.start({ mode: 'crew', how: true, seed: 4, crawl: true })); await s.waitForTimeout(1500);
  await s.evaluate(() => { PL.pause(true); PL.toBeat(.4); }); await s.waitForTimeout(300);
  await s.screenshot({ path: OUT + 'side-2-howto.png' });
  await s.tap('#howSkip');
  await s.evaluate(() => { PL.pause(false); G.s[0].ai = 'auto'; PL.steps(60 * 7); PL.toBeat(.4); PL.pause(true); }); await s.waitForTimeout(1200);
  await s.screenshot({ path: OUT + 'side-3-swim.png' });
  await s.evaluate(() => { PL.toWall(.6); PL.pause(false); }); await s.waitForTimeout(300); await s.evaluate(() => PL.pause(true)); await s.waitForTimeout(300);
  await s.screenshot({ path: OUT + 'side-4-turn.png' });
  await s.evaluate(() => { PL.pause(false); PL.steps(60 * 300); }); await s.waitForTimeout(900);
  ok(await s.isVisible('#again'), 'sideways: the result card');
  await s.screenshot({ path: OUT + 'side-5-result.png' });
  ok(s.errs.length === 0, 'sideways: no console errors ' + JSON.stringify(s.errs));
  // ---- desktop: Space to stroke and to hold a breath, the up arrow to turn; reduced motion ----
  const d = await page(b, { width: 1280, height: 800 }, false);
  await d.check('#rm'); await d.click('.mode[data-m="alone"]'); await d.waitForTimeout(400);
  const k0 = await d.evaluate(() => { G.how = -1; howShow(); PL.pause(true); let st = PL.state().s[0]; while (st.breathBeat || st.phase !== 'swim' || G.phase !== 'go') { PL.steps(5); st = PL.state().s[0]; } return PL.toBeat(.005).s[0]; });
  await d.keyboard.down(' '); await d.evaluate(() => PL.live(1)); await d.keyboard.up(' ');
  const k1 = await d.evaluate(() => PL.live(2).s[0]);
  ok(k1.clean + k1.good === k0.clean + k0.good + 1, 'Space on the beat is a stroke');
  await d.evaluate(() => PL.toWall(.45)); await d.keyboard.press('ArrowUp'); const k2 = await d.evaluate(() => PL.live(2).s[0]);
  ok(k2.turns.length === 1, 'the up arrow turns you');
  ok(await d.evaluate(() => RM === true && camT === 1), 'reduced motion: the camera cuts instead of easing');
  await d.evaluate(() => PL.pause(false)); await d.waitForTimeout(500);
  await d.screenshot({ path: OUT + 'desk-1-swim.png' });
  ok(d.errs.length === 0, 'desktop: no console errors ' + JSON.stringify(d.errs));
  console.log(fails ? fails + ' FAILED' : 'ALL OK');
  await b.close();
  process.exit(fails ? 1 : 0);
})();
