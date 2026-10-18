# Reviewer 1g: how often the polite word comes in ordinary walking (across the deck between far rooms, not chasing
# anyone), and whether it holds back a due need warning. Run: python3 shuffle_toast_probe.py BUILD.html
import sys
exec(open(__file__.replace('shuffle-ec6e8a0-bubble-probe.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
INST = """(() => { window.__t = { said: [], other: [], bub: [] }; const ob = bubbleSay; bubbleSay = (w, x, s) => { if (s === 2.5) __t.said.push([Math.round(performance.now() / 100) / 10, 'bubble', x]); return ob(w, x, s); }; const ot = toast; toast = (a, b) => { (/steps aside/.test(b || '') ? __t.said : __t.other).push([Math.round(performance.now() / 100) / 10, a, (b || '').slice(0, 50)]); return ot(a, b); }; return true; })()"""
WALK = """(() => { if (player.path.length || ACT) return 0; const ts = []; for (let i = 0; i < 60; i++) for (let j = 0; j < 30; j++) if (free(i, j)) ts.push([i, j]);
  const p = player.here(); const far = ts.filter(t => Math.abs(t[0] - p[0]) + Math.abs(t[1] - p[1]) > 12); const t = far[(%d * 7919) %% far.length]; if (!t || !findPath(p, t, null, player)) return -1; playerGo(t, () => {}); return 1; })()"""
with sync_playwright() as pw:
    for deck, at in ((3, 7 * 60 + 15), (3, 18 * 60 + 10)):
        g = Game(pw, sys.argv[1], 390, 844)
        g.ev(f"setShipNow(Math.floor(shipNow() / 1440) * 1440 + 1440 * 2 + {at}); needsT = null"); g.ev(f"goToDeck({deck})"); g.step(60)
        g.ev(INST); g.ev("WARN_SAID = {}; SHIP.player.needs.hunger = 30; Object.assign(POP, { toast: -1e9, card: -1e9, warn: -1e9 }); TOAST_AT = -1e9")
        walks = 0; first_warn = None
        for k in range(200):                      # about 200 s
            walks += g.ev(WALK % k) == 1; g.step(30)
            if k == 2: g.ev("SHIP.player.needs.hunger = 24")   # a warning falls due now
            if first_warn is None and g.ev("!!WARN_SAID.hunger"): first_warn = k
        T = g.ev("window.__t")
        gaps = [round(b[0] - a[0], 1) for a, b in zip(T['said'], T['said'][1:])]
        print(f"Deck {deck} at {at // 60:02d}:{at % 60:02d}: {walks} walks, {len(T['said'])} polite words in ~200 s; gaps {gaps[:25]}")
        print('   the hunger warning (due from ~3 s):', 'at ~%d s' % first_warn if first_warn is not None else 'NOT SHOWN in 200 s', '| other toasts:', T['other'][:4])
        g.close()
