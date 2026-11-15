const { chromium } = require('playwright'); const fs = require('fs');
const GAME = process.argv[2], RATE = +(process.argv[3] || 1), Q = process.argv[4] || '?nosave';
const THREE = fs.readFileSync('/tmp/cadet-work/three/package/build/three.min.js', 'utf8');
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--enable-precise-memory-info'] });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1, isMobile: true, hasTouch: true });
  const page = await ctx.newPage();
  await page.route(/three\.min\.js/, r => r.fulfill({ body: THREE, contentType: 'application/javascript' }));
  await page.addInitScript(() => { const raf = window.requestAnimationFrame.bind(window); let n = 0; window.__t = {}; window.requestAnimationFrame = cb => raf(t => { n++; if (n === 3) window.__t.thirdRaf = performance.now(); cb(t); }); });
  const cdp = await ctx.newCDPSession(page);
  if (RATE > 1) await cdp.send('Emulation.setCPUThrottlingRate', { rate: RATE });
  await b.startTracing(page, { categories: ['devtools.timeline', 'v8', 'disabled-by-default-v8.compile', 'blink.user_timing', 'loading'] });
  await page.goto('file://' + GAME + Q, { waitUntil: 'load' });
  await page.waitForFunction('window.__t && window.__t.thirdRaf', null, { timeout: 300000 });
  const third = await page.evaluate('window.__t.thirdRaf');
  const buf = await b.stopTracing(); const tr = JSON.parse(buf.toString()); const ev = tr.traceEvents || tr;
  const sum = {}; for (const e of ev) if (e.ph === 'X' && e.dur) { const k = e.name; (sum[k] = sum[k] || { n: 0, ms: 0, max: 0 }); sum[k].n++; sum[k].ms += e.dur / 1000; sum[k].max = Math.max(sum[k].max, e.dur / 1000); }
  const want = ['ParseHTML', 'EvaluateScript', 'v8.compile', 'v8.parseOnBackground', 'V8.CompileCode', 'v8.run', 'FunctionCall', 'Layout', 'UpdateLayoutTree', 'Paint', 'MajorGC', 'MinorGC', 'V8.GC_MC_BACKGROUND_MARKING', 'RunTask', 'V8.DeserializeContext', 'v8.compileModule', 'V8.ParseFunction', 'V8.CompileIgnition', 'TimerFire', 'FireAnimationFrame', 'GPUTask', 'ParseAuthorStyleSheet'];
  console.log('rate', RATE, 'third frame at ms', Math.round(third));
  for (const k of want) if (sum[k]) console.log(k.padEnd(28), String(sum[k].n).padStart(6), 'x', sum[k].ms.toFixed(0).padStart(7), 'ms  max', sum[k].max.toFixed(0));
  const others = Object.entries(sum).filter(([k]) => !want.includes(k)).sort((a, b) => b[1].ms - a[1].ms).slice(0, 12); for (const [k, v] of others) console.log(' other', k.padEnd(34), v.n, v.ms.toFixed(0));
  await b.close();
})();
