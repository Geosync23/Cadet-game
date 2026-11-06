# RV33: the arrow over the first week on a merged build, fresh save, intro on (paper run to Day 2), clocking in on work days.
import sys, json
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
build = sys.argv[1]; D0, D1 = int(sys.argv[2]), int(sys.argv[3])
with sync_playwright() as pw:
    g = Game(pw, build, 390, 844)
    g.ev('localStorage.clear()'); g.ev('newGameStart(true)'); g.step(5)
    g.page.fill('form input[maxlength="24"]', 'Sam'); g.page.locator('form button').first.click(); g.step(5)
    g.ev("""(() => { const t0 = introAbs(INTRO_START.day, INTRO_START.min); socInit(); SHIP.intro = introBlank(); introBegin('Sam');
      for (let t = t0; t <= %d * 1440 + 5 * 60; t++) { setShipNow(t); const st = SHIP.intro.step && introStepById(SHIP.intro.step);
        introAdvance(t, st && st.checkpoint ? { deck: st.checkpoint.deck, tile: st.checkpoint.tile } : { deck: 4, tile: [8, 3] }); } })()""" % (D0 - 1))
    for d in range(D0, D1 + 1):
        last = None; out = []
        for m in range(6 * 60, 22 * 60 + 35, 5):
            t = (d - 1) * 1440 + m
            g.ev(f"(() => {{ skipTo({t}); for (const k of NEED_KEYS) SHIP.player.needs[k] = 75; }})()"); g.step(4)
            if m == 8 * 60 + 50 and g.ev(f"weekday({d}) <= 4"): g.ev("(() => { try { clockPunch(false); clockUndoSettle(); } catch (e) {} })()")
            if m == 17 * 60 + 5 and g.ev(f"weekday({d}) <= 4"): g.ev("(() => { try { clockPunch(false); clockUndoSettle(); } catch (e) {} })()")
            lab = g.ev("(() => { const G = typeof goalNow === 'function' ? goalNow() : null; return G ? String(G.label || G.text || G.id || '?').slice(0, 70) : null; })()")
            if lab != last: out.append('%02d:%02d %s' % (m // 60, m % 60, lab)); last = lab
        print('Day %d (weekday %s):' % (d, g.ev(f"weekday({d})")))
        for o in out: print('   ', o)
    print('errors', [e for e in g.errors if 'pageerror' in e][:4])
