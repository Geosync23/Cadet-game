# patch #5 probe: the spine ladder. GAME=..., Q='&ladder'
import sys, os; sys.path.insert(0, '/home/user/Cadet-game/plans/patch-plan-probes')
from pp import *
OUT = sys.argv[1] if len(sys.argv) > 1 else '/tmp'
g = start('?nosave&debug' + os.environ.get('Q', '')); g.step(5)
def scr(x, y, z): return g.ev(f"(() => {{ const v = new THREE.Vector3({x},{y},{z}).project(camera); return [(v.x+1)/2*innerWidth, (1-v.y)/2*innerHeight]; }})()")
def tap_hatch():
    e = g.ev("(() => { const e = ladderHatch(); if (!e) return null; const s = reachableSide(e); player.obj.position.copy(cellPos(s[0], s[1])); target.copy(player.obj.position).setY(.7); return [e.key, e.cx, e.cz]; })()")
    g.step(30)
    if not e: return None
    for yy in (.08, 1.2):                                 # its foot, then its middle (on Deck 1 the relay racks' tap box covers the foot)
        x, y = scr(e[1], yy, e[2])
        hit = g.ev(f"(() => {{ const h = pick({x}, {y}); return h ? (h.object.userData.closedDoor || (h.object.userData.item && h.object.userData.item.t) || 'other') : null; }})()")
        if hit in (e[0], 'Spine ladder'):
            g.page.mouse.click(x, y); g.secs(3); return e[0] + ' (tapped ' + hit + ' at y ' + str(yy) + ')'
    return e[0] + ' (not tappable: ' + str(hit) + ')'
def panel(): return g.ev("(() => { const el = document.getElementById('ladderPanel'); return el && !el.hidden ? el.innerText.replace(/\\n+/g, ' | ') : null; })()")
def st(): return g.ev("({ t: clockText(), deck: deckDef.num, me: player.here(), room: roomAt(...player.here()), e: Math.round(SHIP.player.needs.energy), f: Math.round(SHIP.player.needs.fitness), ride: !!ride, toast: document.getElementById('toast').innerText.replace(/\\n/g, ' ') })")
def climb(label):
    g.page.locator('#ladderPanel button.deckbtn', has_text=label).first.click(); g.step(2)
    for k in range(60):
        g.step(5)
        if not g.ev("!!ride"): break
    g.step(5); return st()
g.ev("skipTo(10*60)"); g.ev("goToDeck(4)"); g.step(5)
print('Deck 4 hatch tapped:', tap_hatch()); print('panel:', panel()); g.page.screenshot(path=OUT + '/05-panel-deck4.png')
print('before', st()); print('-> Operations', climb('Operations'))
g.page.screenshot(path=OUT + '/05-landed-deck5.png')
print('Deck 5 hatch tapped:', tap_hatch()); print('panel:', panel())
g.ev("liftHold(true)"); print('lift held:', g.ev("liftHeld()"))
print('-> Bridge', climb('Bridge')); g.ev("liftHold(false)")
print('Deck 1 hatch tapped:', tap_hatch()); print('panel:', panel()); print('-> Engineering', climb('Engineering'))
print('Engine control reachable:', g.ev("(() => { const t = (ROOM_TILES['K'] || [])[0]; return t ? (findPath(player.here(), t, null, player) || []).length > 0 : null; })()"),
      'Reactor:', g.ev("(() => { const t = (ROOM_TILES['R'] || [])[0]; return [(findPath(player.here(), t, null, player) || []).length > 0, (CLOSED_DOORS['v,27,3'] || {}).x]; })()"))
g.ev("goToDeck(2)"); g.step(3); print('Sensor array reachable:', g.ev("(() => { const t = (ROOM_TILES['A'] || [])[0]; return (findPath(player.here(), t, null, player) || []).length > 0; })()"))
tier = []
for n in [1, 2, 3, 4, 7, 5, 6]:
    g.ev(f"goToDeck({n})"); g.step(2)
    tier += g.ev(f"""(() => {{ const out = [], re = /Tier \\d/; for (const [k, c] of Object.entries(CLOSED_DOORS)) if (c && re.test(c.x || '')) out.push([{n}, 'door', k, c.x]);
      for (const r in ROOMS) if (re.test(ROOMS[r].tap || '')) out.push([{n}, 'room', r, ROOMS[r].tap]); for (const i of ITEMS) if (re.test(i.x || '')) out.push([{n}, 'item', i.t, i.x]); return out; }})()""")
    print('Deck', n, 'ladder hatch', g.ev("(() => { const e = ladderHatch(); return e && [e.key, reachableSide(e).slice(0, 2), free(...reachableSide(e).slice(0, 2))]; })()"))
print('tier wording left:', len(tier)); [print('  ', x) for x in tier[:12]]
print('errors', g.errors[:5]); g.close()
