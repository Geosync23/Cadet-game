# RV21: VB1 V-2 live at phone size, switched on: the arrow/goal at each beat, the ramp scene, the lights gathering
import sys, os
G = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
exec(open(os.path.join(os.path.dirname(G), 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
src = open(G).read().replace("const EV_VESSEL_ON = URL_FLAGS.has('evvessel');", "const EV_VESSEL_ON = true;", 1)
vp = WORK / 'test' / '_rv21_v2.html'; vp.write_text(src)
GOAL = "(() => { const g = goalNow(); const q = (GUIDE.list||[]).filter(x => /^vessel:/.test(x.id)).map(x => x.id + ':' + x.level); return { clock: clockText(), goal: g && g.label, deck: g && g.deck, q, dlg: DIALOGUE && DIALOGUE.id, toasts: (window.__t||[]).slice(-3) }; })()"
def to(g, abs):
    g.ev(f"(() => {{ for (let t = Math.max(shipNow() + 1, {abs} - 2); t <= {abs}; t++) {{ setShipNow(t); EV_MIN = -1; eventsTick(); }} }})()")
with sync_playwright() as pw:
    g = Game(pw, str(vp), 390, 844)
    g.ev("(() => { window.__t = []; const T = toast; toast = (a, b) => { window.__t.push(a + ': ' + b); T(a, b); }; if (typeof GUIDE_ON !== 'undefined') {} })()")
    g.ev("skipTo(26 * 1440 + 360)"); g.step(5)
    print('due', g.ev("SHIP.event && SHIP.event.id"), g.ev("JSON.stringify(evCalPlan ? evCalPlan().map(r=>r.id+':'+r.day) : null)"))
    for (k, m, tag) in ((0, 610, 's1_sat1010_sheet'), (0, 850, 's2_sat1410_view'), (1, 555, 's3_sun0915_ramp_arrow')):
        to(g, (26 + k) * 1440 + m); g.step(30); print(tag, g.ev(GOAL)); g.shot(f'{OUT}/{tag}.png')
    # stand at the ramp's foot and wait for Taavek
    g.ev("(() => { goToDeck(5); const s = placeSpot(ROT_TERN_FOOT); player.obj.position.set(s.x, player.obj.position.y, s.z); player.stop(); })()")
    for m in range(565, 580):
        to(g, 27 * 1440 + m); g.step(25)
        if g.ev("!!DIALOGUE"): break
    print('ramp', g.ev(GOAL)); g.shot(f'{OUT}/s4_sun_ramp_scene.png')
    n = 0
    while g.ev("!!DIALOGUE") and n < 40:
        g.ev("(() => { const v = dialogueView(); if (v && v.choices) dialogueChoose(1); else dialogueNext(); })()"); g.step(2); n += 1
    print('after ramp', g.ev("JSON.stringify(SHIP.event.mine)"))
    to(g, 27 * 1440 + 597); g.step(30); print('bench arrow', g.ev(GOAL)); g.shot(f'{OUT}/s5_sun0957_bench.png')
    to(g, 28 * 1440 + 1040); g.step(30); print('lights arrow', g.ev(GOAL)); g.shot(f'{OUT}/s6_mon1720_lights_arrow.png')
    print('errors', g.errors[:5]); g.close()
