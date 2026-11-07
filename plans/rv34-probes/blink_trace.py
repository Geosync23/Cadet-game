# RV34: the Last Light's blink (EV999_BLINK_ON), frame by frame on every deck. usage: blink_trace.py BUILD.html TAG [calm]
# For each deck: a fresh page, skip to Day 4 14:07:50, go to the deck, then step 1/30 s frames to 14:09:30, recording the
# light (hemi, sun, lamps, exposure, background, sky wash), the feel's kinds, toasts and (every 6th frame drawn) draw calls.
import sys, json
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
build, tag = sys.argv[1], sys.argv[2]
calm = len(sys.argv) > 3 and sys.argv[3] == 'calm'
if calm: INIT = "(() => { const mm = window.matchMedia.bind(window); window.matchMedia = q => /reduced-motion/.test(q) ? { matches: true, media: q, addListener() {}, removeListener() {}, addEventListener() {}, removeEventListener() {} } : mm(q); })();\n" + INIT
TRACE = r"""(n => { const out = [];
  for (let i = 0; i < n; i++) { const draw = i % 6 === 0; window.__skip = !draw; window.__step(1, 1000/30); window.__skip = false;
    const L = LAMPS.reduce((a, x) => a + x.l.intensity, 0);
    out.push([+(SHIP.time.min).toFixed(3), FEEL_S.kinds.join(), simNow()/1000 - FEEL_S.t0, hemi.color.r, hemi.color.g, hemi.color.b, hemi.intensity, sun.color.r, sun.color.g, sun.color.b, sun.intensity, L,
      renderer.toneMappingExposure, scene.background.getHexString(), SKY.mat.uniforms.uWash.value, draw ? renderer.info.render.calls : null, (document.getElementById('toast') || {}).textContent || '']); }
  return out; })"""
res = {}
with sync_playwright() as pw:
    for d in [1, 2, 3, 4, 5, 6, 7]:
        g = Game(pw, build, 390, 844); g.step(3)
        g.ev("window.__toasts = []; { const ts = toast; toast = function (a, b) { window.__toasts.push([+SHIP.time.min.toFixed(2), a, String(b||'')]); return ts.apply(this, arguments); }; }")
        g.ev(f"(() => {{ skipTo(3 * 1440 + 14 * 60 + 7); goToDeck({d}, null); }})()"); g.step(40)
        info = g.ev("JSON.stringify([SHIP.time.day, SHIP.time.min, deckDef && deckDef.num, SHIP.event && SHIP.event.id, typeof eventNow === 'function' && eventNow() ? eventNow().phase : null, FEEL_CALM])")
        tr = g.page.evaluate("s => window.__sc(s)", TRACE + "(200)")
        felt = g.ev("JSON.stringify([SHIP.event && SHIP.event.mine && SHIP.event.mine['felt:lastLightBlink'], window.__toasts])")
        res[d] = {'info': info, 'trace': tr, 'felt': felt, 'errors': [e for e in g.errors if 'pageerror' in e][:3]}
        print(d, info, felt[:300], res[d]['errors'], flush=True)
        g.close()
json.dump(res, open(f'/tmp/rv34/trace_{tag}.json', 'w'))
