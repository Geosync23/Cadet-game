# RV29: the Works tea corner on a build (TRAD995_ON as built): Day 2, 13:00-13:45 (tea and biscuits) at frame pace. Each ship
# minute: who's in the tea corner ('t') and where, whether the doorway tile [21, 1] is clear, the 5-tea-3 spot's tile. At 13:20
# you tap the hot water (ixTap on the 'Hot water' item from the doorway side): the act's kind and place. Then on Deck 4 the
# kettle. usage: tea_corner.py WT BUILD
import sys, json, types
from playwright.sync_api import sync_playwright
src = open(sys.argv[1] + '/cadet_test.py').read(); src = src[:src.index('import sys, json, hashlib')]
ct = types.ModuleType('ct'); exec(src, ct.__dict__)
TAP = """((name) => { const it = ITEMS.find(i => i.t === name); if (!it) return 'no ' + name; const w = new THREE.Vector3(); it.hit.getWorldPosition(w);
  if (ACT) actEnd(true); const r = ixTap(it, w.clone(), w.clone()); return { r, act: ACT ? [ACT.kind, ACT.placeId] : null, t: hhmm(SHIP.time.min) }; })"""
with sync_playwright() as pw:
    g = ct.Game(pw, sys.argv[2])
    print('TRAD995_ON', g.ev("TRAD995_ON"), '5-tea-3 at', g.ev("(DECKS[5].places.find(p => p.id === '5-tea-3') || {}).at"))
    g.ev("(() => { introSkip && introSkip(); skipTo((2 - 1) * 1440 + 12 * 60 + 55); goToDeck(5, null); const c = cellPos(20, 3); player.obj.position.set(c.x, 0, c.z); player.stop(); })()"); g.step(10)
    last = None; blocked = 0; mins = 0
    for k in range(3000):
        g.step(10)
        s = g.ev("""(() => ({ t: hhmm(SHIP.time.min), m: Math.floor(SHIP.time.min), door: DECK_CREW.filter(a => { const c = cellAt(a.x, a.z); return c[0] === 21 && c[1] === 1; }).map(a => a.p.id),
          tea: DECK_CREW.filter(a => roomAt(...cellAt(a.x, a.z)) === 't').map(a => a.p.id + (a.settled ? '*' : '') + '@' + cellAt(a.x, a.z).join(',')).sort() }))()""")
        if s['m'] != last:
            last = s['m']; mins += 1
            if s['door']: blocked += 1
            if s['m'] % 5 == 0 or s['door']: print(s['t'], 'doorway', s['door'] or 'clear', '| in the tea corner', ' '.join(s['tea']))
            if s['t'] == '13:20': print('  TAP hot water ->', json.dumps(g.ev(TAP + "('Hot water')"))); g.step(30); print('  after 30 frames', g.ev("ACT ? [ACT.kind, ACT.placeId, ACT.phase] : null"))
        if s['t'] >= '13:46': break
    print(f'doorway occupied in {blocked} of {mins} ship minutes')
    g.ev("(() => { if (ACT) actEnd(true); goToDeck(4, null); })()"); g.step(10)
    k4 = g.ev("ITEMS.filter(i => /kettle|hot water/i.test(i.t)).map(i => i.t)"); print('deck 4 kettles', k4)
    for name in k4[:2]: print('  TAP', name, '->', json.dumps(g.ev(TAP + f"({json.dumps(name)})")))
    print('errors', g.errors[:3]); g.close()
