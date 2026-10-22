# RV8 probe: a mess seat with no tray, real screen tap at 390x844; the card's words and its box. p_seat.py GAME CT_DIR OUT
import sys, json
exec(open(sys.argv[2] + '/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
out = sys.argv[3]
PROJ = """(() => { const it = ITEMS.find(i => /^Long table$/.test(i.t)), q = new THREE.Vector3(); it.hit.getWorldPosition(q);
  const p = player.obj.position; q.project(camera); return [(q.x + 1) / 2 * innerWidth, (1 - q.y) / 2 * innerHeight, Math.hypot(p.x - it.hit.getWorldPosition(new THREE.Vector3()).x, p.z - it.hit.getWorldPosition(new THREE.Vector3()).z)]; })()"""
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.page.add_style_tag(content='#toast{opacity:1!important}'); g.step(3)
    g.ev("(() => { if (deckDef.num !== 3) goToDeck(3); setShipNow(1440 + 18 * 60 + 5); SHIP.player.tray = null; })()"); g.step(30)
    # walk close: put the player near the table so it's on screen
    g.ev("(() => { const it = ITEMS.find(i => /^Long table$/.test(i.t)), q = new THREE.Vector3(); it.hit.getWorldPosition(q); const n = nearestOpen(q.x + 1.5, q.z, player); Object.assign(player.obj.position, cellPos(...n)); })()"); g.step(60)
    x, y, d = g.ev(PROJ); print('table on screen at', round(x), round(y), 'dist', round(d, 2))
    g.page.mouse.click(x, y)
    for k in range(200):
        g.step(10)
        if g.ev("!!ACT && ACT.phase === 'do'"): break
    r = g.ev("(() => { const t = document.getElementById('toast').getBoundingClientRect(); return [ACT && ACT.kind, document.getElementById('toast').innerText, Math.round(t.top), Math.round(t.bottom), innerHeight, ITEMS.find(i => /^Long table$/.test(i.t)).x]; })()")
    print(json.dumps(r, indent=1))
    g.page.screenshot(path=out + '-seat.png')
    print('errors', g.errors[:3]); g.close()
