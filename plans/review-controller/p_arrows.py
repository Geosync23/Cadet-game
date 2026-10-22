# RV2 probe (arrows piece B, switch on in a copy): play a few minutes with the queue on: an entry for the lift, a
# level 1 over a direct goal, then done; five toasts in one frame; screenshots of the arrow. Run: p_arrows.py GAME_ON.html OUT
import sys, os, json
GAMEF, OUT = sys.argv[1], sys.argv[2]; sys.argv = [sys.argv[0]]
exec(open(os.path.join(os.path.dirname(os.path.abspath(GAMEF)), 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, GAMEF, 390, 844); g.ev("SHIP.device && SHIP.device.settings && (SHIP.device.settings.tips = false)"); g.step(20)
    st = lambda: g.ev("(() => { const n = goalNow(); return { goal: n && (n.label || n.guide || n.deck), shown: GUIDE.shown, list: guideList().map(e => e.id + ':' + e.level), toast: document.getElementById('tt').textContent, q: GUIDE.tq.length }; })()")
    print('start', st())
    g.ev("window.__d = false; guideAsk({ id: 'rv2:a', level: 4, goal: () => ({ deck: 3, label: 'RV2 shift thing' }), until: shipNow() + 120, done: () => window.__d, owner: 'rv2' })"); g.step(40)
    print('level 4 asked', st()); g.page.screenshot(path=f'{OUT}/ar_l4.png')
    g.ev("setGoal({ deck: 2, label: 'RV2 direct' })"); g.step(40); print('direct set', st())
    g.ev("guideAsk({ id: 'rv2:now', level: 1, goal: () => ({ deck: 5, label: 'RV2 emergency' }), until: shipNow() + 30, done: () => window.__d1, owner: 'rv2' })"); g.step(40)
    print('level 1 over direct', st()); g.page.screenshot(path=f'{OUT}/ar_l1.png')
    g.ev("window.__d1 = true"); g.step(40 * 30); print('level 1 done (a ship minute on)', st())
    g.ev("clearGoal()"); g.step(40 * 30); print('direct cleared', st())
    g.ev("window.__d = true"); g.step(40 * 30); print('level 4 done', st())
    g.ev("for (let k = 0; k < 5; k++) toast('T' + k, 'x'); toast('T1', 'x')"); seq = []
    for k in range(60):
        g.step(10); seq.append(g.ev("document.getElementById('tt').textContent"))
    print('toasts in order:', [x for i, x in enumerate(seq) if i == 0 or x != seq[i - 1]])
    print('errors', [e for e in g.errors if 'error' in e][:3])
    g.close()
