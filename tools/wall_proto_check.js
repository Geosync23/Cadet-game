// Wall prototype check (Reach): NODE_PATH=$(npm root -g) node tools/wall_proto_check.js
// Needs three.js r128 at /tmp/cadet-work/three/package/build/three.min.js (or THREE_JS=path). Paths come from the repo.
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(ROOT, 'plans/shots-wall') + '/';
const URL = 'file://' + path.join(ROOT, 'wall-proto.html');
const THREE_JS = process.env.THREE_JS || '/tmp/cadet-work/three/package/build/three.min.js';
fs.mkdirSync(OUT, { recursive: true });
let fails = 0; const ok = (c, m) => { console.log((c ? 'ok   ' : 'FAIL ') + m); if (!c) fails++; };
async function page(b, vp, mobile) {
  const p = await b.newPage({ viewport: vp, deviceScaleFactor: mobile ? 2 : 1, hasTouch: mobile, isMobile: mobile });
  await p.route('**/three.min.js', r => r.fulfill({ path: THREE_JS, contentType: 'application/javascript' }));
  p.errs = []; p.on('console', m => { if (m.type() === 'error') p.errs.push(m.text()); }); p.on('pageerror', e => p.errs.push(String(e)));
  await p.goto(URL); await p.waitForFunction(() => window.WL);
  await p.evaluate(() => { try { localStorage.clear(); } catch (e) {} }); await p.reload(); await p.waitForFunction(() => window.WL); await p.waitForTimeout(700);
  return p;
}
const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
// the next hold up for the lower hand (what the autopilot would pick), worked out in the page
const NEXT = () => WL.advice();
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  // ---- phone, portrait 390x844 ----
  const p = await page(b, { width: 390, height: 844 }, true);
  await p.screenshot({ path: OUT + 'phone-1-menu.png' });
  await p.tap('.route[data-r="3"]'); await p.tap('.mode[data-m="alone"]');   // real taps: the green route, Climb
  await p.waitForTimeout(1300);
  ok(await p.evaluate(() => WL.state().how === 0 && WL.state().c[0].r === 3), 'the green route, How to play at step 1 of 3');
  await p.screenshot({ path: OUT + 'phone-2-howto.png' });
  const cdp = await p.context().newCDPSession(p);
  const touch = (type, pts) => cdp.send('Input.dispatchTouchEvent', { type, touchPoints: pts });
  const sc = (y, z) => p.evaluate(([y, z]) => WL.screen(y, z), [y, z]);
  // a real thumb: down, slide to just under the next hold (the hand shows above the thumb), lift
  const nx = await p.evaluate(NEXT), st0 = await p.evaluate(() => WL.state().c[0]);
  const [sx, sy] = await sc(nx.y, nx.z);
  await touch('touchStart', [{ x: sx + 40, y: Math.min(830, sy + 10), id: 1 }]);
  for (let i = 1; i <= 8; i++) { await touch('touchMove', [{ x: sx + 40 - i * 5, y: Math.min(830, sy + 10) - i * (Math.min(830, sy + 10) - sy) / 8, id: 1 }]); await p.waitForTimeout(40); }
  await p.waitForTimeout(700);
  const mid = await p.evaluate(() => WL.state().c[0]);
  const fh = mid.free >= 0 ? mid.hands[mid.free] : null;
  ok(mid.free >= 0 && fh && Math.hypot(fh.y - nx.y, fh.z - nx.z) < .06, 'thumb down frees your lower hand and it follows the thumb to the hold (' + (fh ? Math.hypot(fh.y - nx.y, fh.z - nx.z).toFixed(3) : '-') + ' m off)');
  await p.screenshot({ path: OUT + 'phone-3-reach.png' });
  await touch('touchEnd', []); await p.waitForTimeout(300);
  const st1 = await p.evaluate(() => WL.state().c[0]);
  ok(st1.moves === st0.moves + 1 && st1.free < 0 && st1.hands.some(h => h.hold === nx.plan), 'lift over a hold and you grab it (' + st1.moves + ' move)');
  ok(await p.evaluate(() => WL.state().how === 1), 'How to play moves on after your first hold');
  await p.tap('#howSkip'); await p.waitForTimeout(150);
  // lift over bare wall: the hand goes back to its hold
  const lo = await p.evaluate(() => { const c = WL.state().c[0], f = c.hands[0].y < c.hands[1].y ? 0 : 1, a = c.hands[1 - f]; return [a.y + .05, a.z + .45 * (a.z > 4.3 ? -1 : 1), c.moves, c.misses]; });
  const holdsNear = await p.evaluate(([y, z]) => WL.holds(3).some(h => Math.hypot(h.y - y, h.z - z) < .12), lo);
  const [bx, by] = await sc(lo[0], lo[1]);
  await touch('touchStart', [{ x: bx, y: by, id: 2 }]); await p.waitForTimeout(600); await touch('touchEnd', []); await p.waitForTimeout(700);
  const st2 = await p.evaluate(() => WL.state().c[0]);
  ok(holdsNear || (st2.moves === lo[2] && st2.misses === lo[3] + 1 && st2.free < 0), 'lift over bare wall and the hand goes back to its hold');
  // the reach: drag far up and the hand stops at the edge of your reach
  const far = await p.evaluate(() => { const c = WL.state().c[0]; return Math.max(c.hands[0].y, c.hands[1].y); });
  const [fx, fy] = await sc(far + 1.5, (await p.evaluate(() => WL.state().c[0].hands[0].z)));
  await touch('touchStart', [{ x: fx, y: Math.max(130, fy), id: 3 }]); await p.waitForTimeout(900);
  const rr = await p.evaluate(() => { const c = WL.state().c[0], h = c.hands[c.free], a = c.hands[1 - c.free]; return { up: h.y - a.y, d: Math.hypot(h.y - a.y, h.z - a.z) }; });
  ok(rr.up <= .281 && rr.d <= .601, 'you can only reach so far: ' + rr.up.toFixed(2) + ' m above your other hand at most');
  await touch('touchEnd', []); await p.waitForTimeout(900);
  // grip: small holds drain it, one hand drains it fast, a big hold refills it when you hang still
  const G1 = await p.evaluate(() => {
    const H = WL.holds(0), sm = H.filter(h => h.size === 2), bg = H.filter(h => h.size === 0 && !h.top && !h.start);
    WL.leave(); WL.start({ mode: 'alone', route: 0, how: false }); WL.steps(1);
    WL.hand(0, sm[0].i); WL.hand(1, sm[1].i); WL.set({ grip: 1, still: 0 });
    const a = WL.steps(120).c[0].grip;
    WL.set({ grip: .5 }); WL.steps(1, { down: 1, y: sm[1].y + .1, z: sm[1].z }); const b0 = WL.state().c[0].grip; WL.steps(60, { down: 1 }); const b = WL.state().c[0].grip;
    WL.steps(30, { down: 0 }); WL.hand(0, bg[0].i); WL.hand(1, bg[0].i); WL.set({ grip: .3, still: 0, free: -1, back: -1 });
    const c = WL.steps(120, { down: 0 }).c[0].grip;
    return { a, oneHand: b0 - b, c };
  });
  ok(G1.a < .95, 'two small holds drain your grip (1.00 → ' + G1.a.toFixed(2) + ' in 2 s)');
  ok(G1.oneHand > (1 - G1.a) / 2, 'hanging off one hand drains it faster (' + G1.oneHand.toFixed(3) + ' in 1 s)');
  ok(G1.c > .45, 'hang still on a big hold and it comes back (.30 → ' + G1.c.toFixed(2) + ' in 2 s)');
  // grip gone: the belay lowers you; the height you reached counts
  const fall = await p.evaluate(() => { const H = WL.holds(0); for (let k = 0; k < 6; k++) { const i = H.filter(h => !h.top).slice(-3)[k % 2].i; WL.hand(k % 2, i); } const c = WL.state().c[0]; WL.set({ best: Math.max(c.hands[0].y, c.hands[1].y), grip: .004 }); WL.steps(40, { down: 1, y: 3.3, z: c.hands[0].z }); return WL.state().c[0]; });
  ok(fall.phase === 'lower' && fall.fell > 0, 'grip gone: the auto-belay takes you');
  await p.evaluate(() => WL.steps(60 * 1.5)); await p.evaluate(() => WL.pause(true)); await p.waitForTimeout(1000);
  await p.screenshot({ path: OUT + 'phone-5-lowered.png' });
  await p.evaluate(() => { WL.pause(false); WL.steps(60 * 20); }); await p.waitForTimeout(900);
  const fr = await p.textContent('#resT');
  ok(await p.isVisible('#result') && /nearly to the top|two-thirds|halfway|third|few moves/.test(fr), 'lowered to the mats, and the height counts in words: "' + fr + '"');
  // a full climb of the green route with one thumb, in real time (4 steps a frame): the thumb follows the autopilot's pick
  await p.evaluate(() => { WL.leave(); WL.start({ mode: 'alone', route: 3, how: false, seed: 3 }); WL.rate = 4; });
  let maxCalls = 0, shotMid = false, moves = 0;
  for (let i = 0; i < 400; i++) {
    const s = await p.evaluate(() => [WL.state(), WL.calls()]); maxCalls = Math.max(maxCalls, s[1]);
    const c = s[0].c[0]; if (c.phase !== 'climb') break;
    if (c.free >= 0 || c.back >= 0) { await p.waitForTimeout(60); continue; }
    const a = await p.evaluate(NEXT);
    if (!a.down) { await p.waitForTimeout(80); continue; }        // resting, or thinking
    const [x, y] = await sc(a.y, a.z);
    await touch('touchStart', [{ x, y, id: 10 + i }]);
    for (let k = 0; k < 40; k++) { const h = await p.evaluate(() => { const c = WL.state().c[0]; return c.free >= 0 ? c.hands[c.free] : null; }); if (!h || Math.hypot(h.y - a.y, h.z - a.z) < .02) break; await p.waitForTimeout(30); }
    if (!shotMid && c.best > 2.1) { shotMid = true; await p.evaluate(() => { WL.rate = 1; WL.pause(true); }); await p.waitForTimeout(300); await p.screenshot({ path: OUT + 'phone-4-midclimb.png' }); await p.evaluate(() => { WL.pause(false); WL.rate = 4; }); }
    await touch('touchEnd', []); moves++;
    await p.waitForTimeout(40);
  }
  await p.waitForTimeout(500);
  const top = await p.evaluate(() => WL.state().c[0]);
  ok(top.rang > 0, 'a full climb with one thumb rings the bell (' + top.moves + ' moves, ' + top.misses + ' misses, ' + top.rests + ' rests)');
  ok(shotMid, 'mid-climb (shot)');
  ok(maxCalls > 0 && maxCalls < 200, 'draw calls in a go under 200 (max ' + maxCalls + ')');
  await p.evaluate(() => { WL.rate = 1; WL.steps(60 * 30); }); await p.waitForTimeout(900);
  const rt = await p.textContent('#result');
  ok(/You rang the bell/.test(rt) && /bell board/.test(rt), 'the result: the bell, and your name on the bell board');
  ok(!/\d+\s*(s\b|sec|:\d)/.test(rt), 'no times on the result: "' + rt.trim().replace(/\s+/g, ' ').slice(0, 120) + '"');
  await p.screenshot({ path: OUT + 'phone-6-result.png' });
  await p.tap('#again'); await p.waitForTimeout(300);
  ok(await p.evaluate(() => WL.state().c[0].moves === 0 && WL.state().phase === 'go'), 'Again starts a fresh climb');
  await p.tap('#leave'); await p.waitForTimeout(300);
  ok(await p.isVisible('#menu') && /You/.test(await p.textContent('#board')), 'Leave goes back to the menu, the bell board shows your name');
  // the rules: paper, clones and frame rates
  const R = await p.evaluate(() => { const o = { seed: 11, route: 1, friend: 'tomas', race: true, autoYou: true }; return { paper: WL.paper(o), again: WL.paper(o), f60: WL.fps(o, 60), f30: WL.fps(o, 30), f20: WL.fps(o, 20) }; });
  ok(same(R.paper, R.again), 'seeded climbs replay identically (' + R.paper.c.map(c => c.k + (c.rang ? ' rang' : ' fell')).join(', ') + ')');
  ok(same(R.f60, R.paper) && same(R.f30, R.paper) && same(R.f20, R.paper), 'the same go at 60, 30 and 20 fps equals the go on paper');
  await p.evaluate(() => { WL.start({ mode: 'race', route: 2, friend: 'rina', autoYou: true, how: false, seed: 5 }); WL.rate = 1; });
  await p.waitForTimeout(5000);
  const L = await p.evaluate(() => { WL.pause(true); const c30 = WL.fps(null, 30, true), c20 = WL.fps(null, 20, true), c60 = WL.fps(null, 60, true), at = WL.state().step; FAST = true; while (G.phase !== 'over') wlStep(G); FAST = false; G.ev.length = 0; return { at, live: WL.summary(), c30, c20, c60, paper: WL.paper({ seed: 5, route: 2, friend: 'rina', race: true, autoYou: true }) }; });
  ok(L.at > 60 && same(L.c30, L.live) && same(L.c20, L.live) && same(L.c60, L.live), 'a live go cloned at step ' + L.at + ' and run at 60, 30 and 20 fps ends the same as the live go');
  ok(same(L.live, L.paper), 'and the live go equals the same go on paper');
  const W = await p.evaluate(() => [1, 2, 3, 4].map(s => { const o = { seed: s, route: 0, friend: 'tomas', race: true, autoYou: true }; const a = WL.paper(o), b = WL.paper(o); return [JSON.stringify(a) === JSON.stringify(b), a.c.map(c => c.rang ? 'R' : 'F').join('')]; }));
  ok(W.every(w => w[0]), 'races replay the same for the same seed (' + W.map(w => w[1]).join(' ') + ')');
  // a friend beside you; a race
  await p.evaluate(() => { WL.pause(false); WL.leave(); document.getElementById('friend').value = 'tomas'; });
  await p.tap('.mode[data-m="friend"]'); await p.waitForTimeout(400);
  const fs_ = await p.evaluate(() => WL.state().c.map(c => [c.k, c.r]));
  ok(fs_.length === 2 && fs_[1][0] === 'tomas' && fs_[1][1] !== fs_[0][1], 'climb with a friend: Tomas on his own route beside you (' + JSON.stringify(fs_) + ')');
  await p.evaluate(() => { G.c[0].ai = 'auto'; WL.steps(60 * 12); }); await p.waitForTimeout(1200);
  await p.screenshot({ path: OUT + 'phone-7-friend.png' });
  ok(await p.evaluate(() => WL.state().c[1].moves > 3), 'Tomas climbs at his own pace');
  await p.evaluate(() => { WL.leave(); WL.start({ mode: 'race', route: 2, friend: 'pell', autoYou: true, how: false, seed: 2 }); WL.steps(60 * 400); });
  await p.waitForTimeout(900);
  const rc = await p.textContent('#result');
  ok(/first|higher/.test(rc), 'a race ends with who rang the bell first (or got higher): "' + (await p.textContent('#resT')) + '"');
  ok(p.errs.length === 0, 'phone: no console errors ' + JSON.stringify(p.errs));
  // ---- sideways phone 844x390 ----
  const s = await page(b, { width: 844, height: 390 }, true);
  await s.screenshot({ path: OUT + 'side-1-menu.png' });
  await s.evaluate(() => WL.start({ mode: 'friend', route: 2, friend: 'holt', how: true, seed: 4 })); await s.waitForTimeout(1300);
  await s.screenshot({ path: OUT + 'side-2-howto.png' });
  await s.tap('#howSkip'); await s.waitForTimeout(150);
  await s.evaluate(() => { G.c[0].ai = 'auto'; WL.steps(60 * 10); G.c[0].ai = null; WL.steps(2, { down: 1, y: Math.max(G.c[0].hands[0].y, G.c[0].hands[1].y) + .2, z: G.c[0].hands[0].z }); WL.pause(true); }); await s.waitForTimeout(1300);
  await s.screenshot({ path: OUT + 'side-3-midclimb.png' });
  await s.evaluate(() => { WL.pause(false); WL.set({ grip: .003 }); WL.steps(60 * 2); WL.pause(true); }); await s.waitForTimeout(1000);
  await s.screenshot({ path: OUT + 'side-4-lowered.png' });
  await s.evaluate(() => { WL.pause(false); WL.steps(60 * 300); }); await s.waitForTimeout(1000);
  ok(await s.isVisible('#again'), 'sideways: the result card');
  await s.screenshot({ path: OUT + 'side-5-result.png' });
  ok(s.errs.length === 0, 'sideways: no console errors ' + JSON.stringify(s.errs));
  // ---- desktop: hold the mouse to reach, let go to grab; Space and arrows; reduced motion ----
  const d = await page(b, { width: 1280, height: 800 }, false);
  await d.check('#rm'); await d.click('.mode[data-m="alone"]'); await d.waitForTimeout(400);
  await d.evaluate(() => { G.how = -1; howShow(); });
  const dn = await d.evaluate(() => WL.advice()), [mx, my] = await d.evaluate(([y, z]) => WL.screen(y, z), [dn.y, dn.z]);
  await d.mouse.move(mx + 30, my + 30); await d.mouse.down(); await d.mouse.move(mx, my, { steps: 5 }); await d.waitForTimeout(700); await d.mouse.up(); await d.waitForTimeout(300);
  ok(await d.evaluate(() => WL.state().c[0].moves === 1), 'the mouse: hold, move to a hold, let go to grab it');
  const m0 = await d.evaluate(() => WL.state().c[0].moves);
  await d.keyboard.press(' '); await d.keyboard.down('ArrowUp'); await d.waitForTimeout(250); await d.keyboard.up('ArrowUp'); await d.waitForTimeout(300);
  ok(await d.evaluate(() => WL.state().c[0].free >= 0), 'Space takes a hand off, the arrows move it');
  await d.keyboard.press(' '); await d.waitForFunction(() => WL.state().c[0].free < 0, null, { timeout: 4000 }).catch(() => {});
  ok(await d.evaluate(() => WL.state().c[0].free < 0), 'Space again lets go (grab or back)');
  ok(await d.evaluate(() => RM === true && camT === 1), 'reduced motion: the camera cuts instead of easing');
  await d.screenshot({ path: OUT + 'desk-1-climb.png' });
  ok(d.errs.length === 0, 'desktop: no console errors ' + JSON.stringify(d.errs));
  console.log(fails ? fails + ' FAILED' : 'ALL OK');
  await b.close();
  process.exit(fails ? 1 : 0);
})();
