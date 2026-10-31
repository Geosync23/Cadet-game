# TB3 probe for TR1's item 4 (0.99.5, TRAD995_ON): Off the Tern on Day 21 (the first rotation). In the shuttle bay from 17:30:
# the star and the arrow at its host (Raman, else whoever leads), a tap joins you; and Tomas's crew-story scene there
# (stage 2, 17:45) still plays: his story card or lines while you stand with them. Then switched off, the same minutes.
#   python3 plans/tb3-probes/tern995.py starship-cadet.html
import sys, json, os, pathlib
sys.argv[0] = str(pathlib.Path(__file__).resolve().parents[2] / 'cadet_test.py')
exec(open(sys.argv[0]).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
build = sys.argv[1]; src = pathlib.Path(build).read_text()
FAILS = []
def check(c, m):
    print(('ok   ' if c else 'FAIL ') + m)
    if not c: FAILS.append(m)
def run(pw, text, label):
    w = WORK / 'test' / ('_tern995_%s_%d.html' % (label, os.getpid())); w.write_text(text)
    g = Game(pw, str(w), 900, 760)
    g.ev("(() => { skipTo(20 * 1440 + 1046); goToDeck(5, null); SHIP.device.settings.tips = false; for (const k of NEED_KEYS) SHIP.player.needs[k] = 90; clearGoal();"
         " window.__cards = []; const ds = dialogueShow; dialogueShow = function (id) { window.__cards.push([id, SHIP.time.min]); return ds.apply(this, arguments); };"
         " window.__said = []; const bs = bubbleSay; bubbleSay = function (h, t) { const a = DECK_CREW.find(c => c.h === h || h && h.p && c.p.id === h.p.id); window.__said.push([a ? a.p.id : '?', t, SHIP.time.min]); return bs.apply(this, arguments); };"
         " const c = cellPos(5, 9); player.obj.position.copy(cellPos(...nearestOpen(c.x, c.z, player))); player.stop(); })()")
    first = {}; tap = None
    for i in range(260):
        g.step(20)
        x = g.ev("[SHIP.time.min, TJ_NOW && TJ_NOW.e.id === 'off-the-tern' ? TJ_NOW.lead : null, IX_GOAL && IX_GOAL.tj || null, SHIP.events.joined.filter(k => k.startsWith('off-the-tern')).length, !!DIALOGUE && DIALOGUE.id]")
        if x[1] and 'lead' not in first: first['lead'] = (x[0], x[1])
        if x[2] and 'arrow' not in first and str(x[2]).startswith('off-the-tern'): first['arrow'] = x[0]
        if x[1] and tap is None and x[0] >= 1058: tap = g.ev("(() => { const a = TJ_NOW.agent; return [a.p.id, tradJoinTap(a), SHIP.events.joined.filter(k => k.startsWith('off-the-tern'))]; })()")
        if x[4] and x[4] != 'tern' and 'card' not in first: first['card'] = (x[0], x[4])
        if x[4]: g.ev("(() => { const v = dialogueView(); dialogueStep(v && v.choices ? 0 : undefined); })()")
        if x[0] >= 1085: break
    r = g.ev("({ cards: window.__cards, tomas: window.__said.filter(s => s[0] === 'tomas').map(s => s[2] + ' ' + s[1]).slice(0, 8), told: (() => { try { return JSON.stringify(storyPeekCS().told.tomas || []); } catch (e) { return null; } })() })")
    err = g.errors; g.close(); w.unlink(missing_ok=True)
    print(' %s: first %s; tap %s; cards %s; Tomas %s; told %s' % (label, first, tap, r['cards'], r['tomas'], r['told']))
    return first, tap, r, err
with sync_playwright() as pw:
    on = src.replace("const TRAD995_ON = false ||", "const TRAD995_ON = true ||", 1); assert on != src
    f1, t1, r1, e1 = run(pw, on, 'on')
    check('lead' in f1 and 'arrow' in f1, 'on: the star and the arrow at its host (%s)' % f1)
    check(bool(t1) and t1[1] and t1[2], 'on: a tap joins Off the Tern (%s)' % t1)
    check(not e1, 'on: no errors %s' % e1[:3])
    f0, t0, r0, e0 = run(pw, src, 'off')
    check(set(c[0] for c in r1['cards']) >= set(c[0] for c in r0['cards']) and r1['told'] == r0['told'], 'Tomas\'s scene plays as with it off (on %s / off %s; told %s / %s)' % ([c[0] for c in r1['cards']], [c[0] for c in r0['cards']], r1['told'], r0['told']))
print('TERN PROBE ' + ('OK' if not FAILS else 'FAILED (%d)' % len(FAILS)))
