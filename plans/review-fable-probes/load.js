// load-time probe: real clock, optional CPU throttle; reports time to first frame and a CPU profile summary of the load
const { chromium } = require('playwright'); const fs = require('fs');
const GAME = process.argv[2], RATE = +(process.argv[3] || 1), Q = process.argv[4] || '?nosave';
const THREE = fs.readFileSync('/tmp/cadet-work/three/package/build/three.min.js', 'utf8');
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--enable-precise-memory-info'] });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1, isMobile: true, hasTouch: true });
  const page = await ctx.newPage();
  const errs = []; page.on('pageerror', e => errs.push(String(e))); page.on('console', m => m.type() === 'error' && errs.push(m.text()));
  await page.route(/three\.min\.js/, r => r.fulfill({ body: THREE, contentType: 'application/javascript' }));
  await page.addInitScript(() => { const raf = window.requestAnimationFrame.bind(window); let n = 0; window.__t = {}; window.requestAnimationFrame = cb => raf(t => { n++; if (n === 1) window.__t.firstRaf = performance.now(); if (n === 3) window.__t.thirdRaf = performance.now(); cb(t); });
    document.addEventListener('DOMContentLoaded', () => window.__t.dcl = performance.now()); });
  const cdp = await ctx.newCDPSession(page);
  if (RATE > 1) await cdp.send('Emulation.setCPUThrottlingRate', { rate: RATE });
  await cdp.send('Profiler.enable'); await cdp.send('Profiler.setSamplingInterval', { interval: 500 }); await cdp.send('Profiler.start');
  const t0 = Date.now();
  await page.goto('file://' + GAME + Q, { waitUntil: 'load' });
  await page.waitForFunction('window.__t && window.__t.thirdRaf', null, { timeout: 180000 });
  const wall = Date.now() - t0;
  const { profile } = await cdp.send('Profiler.stop');
  const t = await page.evaluate(() => ({ ...window.__t, nav: performance.getEntriesByType('navigation')[0].toJSON(), heap: performance.memory.usedJSHeapSize, total: performance.memory.totalJSHeapSize }));
  // self time by function
  const dt = profile.timeDeltas, ids = profile.samples, self = new Map(); const byId = new Map(profile.nodes.map(n => [n.id, n]));
  for (let i = 0; i < ids.length; i++) self.set(ids[i], (self.get(ids[i]) || 0) + dt[i]);
  const agg = new Map(); let tot = 0;
  for (const [id, us] of self) { const n = byId.get(id), f = n.callFrame; const k = (f.functionName || '(anon)') + (f.lineNumber >= 0 && f.url.startsWith('file') ? ':' + (f.lineNumber + 1) : f.url ? ' [' + f.url.split('/').pop().slice(0, 20) + ']' : ''); agg.set(k, (agg.get(k) || 0) + us); tot += us; }
  const top = [...agg].sort((a, b) => b[1] - a[1]).slice(0, 28).map(([k, us]) => `${(us / 1000).toFixed(0).padStart(6)} ms  ${k}`);
  console.log(JSON.stringify({ rate: RATE, wallMs: wall, dcl: Math.round(t.dcl), firstRaf: Math.round(t.firstRaf), thirdRaf: Math.round(t.thirdRaf), domInteractive: Math.round(t.nav.domInteractive), responseEnd: Math.round(t.nav.responseEnd), heapMB: (t.heap / 1e6).toFixed(1), totalHeapMB: (t.total / 1e6).toFixed(1), errs }));
  console.log('profile total ms', (tot / 1000).toFixed(0)); console.log(top.join('\n'));
  await b.close();
})();
