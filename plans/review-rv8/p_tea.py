# RV8 probe: Day 1 tea with Zeke, real screen taps on every thing in the Tea corner at 390x844. p_tea.py GAME CT_DIR OUT
import sys, json
exec(open(sys.argv[2] + '/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
out = sys.argv[3]
ITEMS_T = """(() => ITEMS.filter(i => i.hit && (() => { const q = new THREE.Vector3(); i.hit.getWorldPosition(q); return roomAt(...cellAt(q.x, q.z)) === 't'; })()).map(i => i.t))()"""
def proj(g, k): return g.ev(f"""(() => {{ const its = ITEMS.filter(i => i.hit && (() => {{ const q = new THREE.Vector3(); i.hit.getWorldPosition(q); return roomAt(...cellAt(q.x, q.z)) === 't'; }})()), q = new THREE.Vector3(); its[{k}].hit.getWorldPosition(q); q.project(camera); return [(q.x + 1) / 2 * innerWidth, (1 - q.y) / 2 * innerHeight]; }})()""")
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.page.add_style_tag(content='#toast{opacity:1!important}'); g.step(3)
    g.ev('localStorage.clear()'); g.ev('newGameStart(true)'); g.step(5)
    g.page.fill('form input[maxlength="24"]', 'Sam'); g.page.click('form button'); g.step(5)
    g.ev("skipTo(introAbs(1, 13 * 60 - 2))"); g.ev("(() => { if (typeof DIALOGUE !== 'undefined' && DIALOGUE) dialogueEnd(); goToDeck(5); })()"); g.step(10)
    g.ev("(() => { const t = (ROOM_TILES.t || [])[0]; const n = nearestOpen(cellPos(...t).x, cellPos(...t).z, player); Object.assign(player.obj.position, cellPos(...n)); })()")
    g.step(30 * 40)
    names = g.ev(ITEMS_T); print('time', g.ev("hhmm(SHIP.time.min)"), 'teaOut', g.ev("teaOut()"), 'items in t:', names)
    print('places t busy:', g.ev("[...PLACE_OF.values()].filter(p => p.room === 't').map(p => [p.id, p.pose, !!heldBy(p.id), typeof placeBusy === 'function' && placeBusy(p.id)])"))
    for k, n in [(i, n) for i, n in enumerate(names) if n in ('Tea table', 'Armchair')]:
        if not g.ev("SHIP.player.teaDay !== 2") and False: pass
        g.ev("actEnd(true); SHIP.player.teaDay = null"); g.step(20)
        if len(sys.argv) > 4: g.ev("[...PLACE_OF.values()].filter(p => p.room === 't').forEach(p => { if (!heldBy(p.id)) BUSY.add(p.id); })")
        x, y = proj(g, k)
        g.page.mouse.click(x, y)
        for s in range(150):
            g.step(10)
            if g.ev("!!ACT && ACT.phase === 'do'"): break
        r = g.ev("[ACT && ACT.kind, ACT && ACT.def && ACT.def.title, ACT && ACT.placeId, document.getElementById('toast').innerText.slice(0, 90), SHIP.player.teaDay]")
        print(f'  tap {n!r} at {round(x)},{round(y)}:', r)
        g.page.screenshot(path=f'{out}-tea-{k}.png')
    print('errors', g.errors[:3]); g.close()
