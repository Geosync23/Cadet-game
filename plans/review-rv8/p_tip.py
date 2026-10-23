# RV8 probe: FX3/FX5's lift-arrow part at a given screen size, with what the tip card does. p_tip.py GAME CT_DIR W H
import sys, json
exec(open(sys.argv[2] + '/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
ok = True
def check(cond, msg):
    global ok
    if not cond: ok = False; print('FAIL', msg)
    return cond
# FX3 (the user's, lead 28): a goal on another deck points at the lift's control panel (the thing you tap to choose a deck),
# not the middle of the landing; following it and tapping there opens the deck picker, and the goal's deck takes you there
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], int(sys.argv[3]), int(sys.argv[4])); g.page.add_style_tag(content='#devTip{opacity:1!important}'); g.step(5)
    print('== FX3: the arrow to the lift panel')
    LP = r"""(() => { const el = document.getElementById('ixGoal'), m = (el.style.transform.match(/translate\(([-\d.]+)px, ?([-\d.]+)px\)/) || []).slice(1).map(Number);
      const its = ITEMS.filter(i => i.lift && isShown(i.hit)).map(i => { i.hit.getWorldPosition(_wp); const v = _wp.clone().project(camera); return [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight]; });
      return { hidden: el.hidden, label: el.children[2].textContent, at: m, panels: its }; })()"""
    # on Decks 5, 3 and 4, inside the car and at the landing: the arrow on a lift panel you can see, and a real tap there opens the deck picker (FE1, lead 28)
    for deck, goal in ((5, 4), (3, 5), (4, 5)):
        for spot in ('inside', 'landing'):
            g.ev(f"goToDeck({deck})"); g.step(3)
            g.ev("(w => { const t = w === 'inside' ? ROOM_TILES['@'][Math.floor(ROOM_TILES['@'].length / 2)] : null; if (t) player.obj.position.copy(cellPos(...t)); else player.obj.position.set(LIFT_AT[0] + 3, 0, LIFT_AT[1]); player.stop(); SHIP.player.track = null; })('" + spot + "')")
            g.ev(f"setGoal({{ deck: {goal}, item: /job board/i, room: 'w', label: 'The job board' }})"); g.step(90)
            lp = g.ev(LP)
            near = min((((p[0] - lp['at'][0]) ** 2 + (p[1] - lp['at'][1]) ** 2) ** .5 for p in lp['panels']), default=999) if lp['at'] else 999
            tip = g.ev("(() => { const c = document.getElementById('devTip'); if (!c || c.hidden) return null; const r = c.getBoundingClientRect(); return [r.left, r.top, r.right, r.bottom, c.style.pointerEvents === 'none']; })()")
            if tip and lp['at']: check(tip[4] or not (tip[0] <= lp['at'][0] <= tip[2] and tip[1] <= lp['at'][1] <= tip[3]), f"Deck {deck} {spot}: the tip card isn't over the arrow's target, or lets the tap through (tip {[round(v) for v in tip[:4]]}, target {lp['at']}) (FX5)")
            print('   ', deck, spot, 'tip', tip and [round(v) for v in tip[:4]] + [tip[4]], 'target', lp['at'] and [round(v) for v in lp['at']], 'tiptext', (g.ev("(c => c && !c.hidden ? c.textContent.slice(0, 40) : null)(document.getElementById('devTip'))")))
            if tip: g.shot(f'tip-{sys.argv[3]}-{deck}-{spot}.png')
            opened = False
            if lp['at'] and near < 3:
                g.page.mouse.move(*lp['at']); g.page.mouse.down(); g.page.mouse.up()
                for k in range(120):
                    g.step(10)
                    if g.ev("!document.getElementById('lift').hidden"): opened = True; break
            print(f"   Deck {deck}, {spot}: {lp['label']} | {round(near, 1)} px from a panel you can see | picker {opened}")
            check(not lp['hidden'] and lp['label'].startswith(f'Tap the lift: Deck {goal}') and 'job board' in lp['label'], f"Deck {deck} {spot}: the label names the lift, the deck and the goal ({lp['label']})")
            check(near < 3, f"Deck {deck} {spot}: the arrow points at a lift panel you can see, not the landing ({near:.1f} px)")
            check(opened, f'Deck {deck} {spot}: tapping where the arrow points opens the deck picker')
            if opened and (deck, spot) == (4, 'landing'):
                g.ev("document.querySelector('#liftList button.goal').click()")
                for k in range(200):
                    g.step(10)
                    if g.ev("deckDef.num") == 5 and not g.ev("ride"): break
                check(g.ev("deckDef.num") == 5, f'the goal\'s deck button takes you there (Deck {g.ev("deckDef.num")})')
            elif opened: g.ev("closeLiftPanel()"); g.step(2)
    g.ev("clearGoal()")
    check(not g.errors, f'no console errors ({g.errors[:3]})')
    g.close()
print('TIP PROBE OK' if ok else 'TIP PROBE FAILED')
