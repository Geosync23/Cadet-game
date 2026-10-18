# reviewer 1f: with a repair job held, does a tap on an everyday thing near that machine's panel (< 1.5 m) start the repair instead? (0.28.52)
import sys, json
src = open('cadet_test.py').read().split('import sys, json, hashlib')[0]
exec(src)
from playwright.sync_api import sync_playwright
MK = r"""((mid) => { const t = shipNow(), m = machineList().find(m => m.id === mid);
  for (const j of SHIP.jobs) if (j.claimedBy === 'you' && j.status === 'claimed') { j.claimedBy = null; j.status = 'open'; }
  const j = { id: 'probe-' + mid, machine: m.id, deck: m.deck, room: m.room, kind: Object.keys(JOB_TYPES)[0], urgency: 1, posted: t, found: t, claimedBy: 'you', status: 'claimed', start: t, parts: ['seal'], title: 'Repair' };
  SHIP.jobs.push(j); SHIP.player.carry = []; SHIP.player.work = null; MACH_REV++; return j.id; })"""
DROP = "(() => { SHIP.jobs = SHIP.jobs.filter(j => !String(j.id).startsWith('probe-')); SHIP.player.carry = []; SHIP.player.work = null; MACH_REV++; })()"
AT = r"""((name) => { const it = ITEMS.find(i => i.t === name && i.hit), v = new THREE.Vector3(); it.hit.getWorldPosition(v);
  const gl = nearestOpen(v.x + 1.2, v.z + 1.2, player); player.obj.position.copy(cellPos(...gl)); player.stop(); actEnd(true); return [v.x, v.y, v.z]; })"""
SCR = r"""((p) => { const v = new THREE.Vector3(p[0], p[1], p[2]).project(camera); return [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight]; })"""
ST = "JSON.stringify([ACT ? ACT.kind + ':' + (ACT.label || ACT.t || ACT.phase || '') : null, document.getElementById('tt').textContent, document.getElementById('tx').textContent.slice(0, 80)])"
CASES = [(5, '4-washer-1', 'Welding bench')]
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1]); g.step(30)
    for deck, mid, thing in CASES:
        if g.ev('deckDef.num') != deck: g.ev(f"goToDeck({deck})"); g.step(5)
        for held in (True,):
            g.ev(DROP)
            if held: g.ev(f"({MK})('{mid}')")
            p = g.ev(f"({AT})('{thing}')"); g.step(20)
            x, y = g.ev(f"({SCR})({json.dumps(p)})")
            g.ev("document.getElementById('tt').textContent = ''; document.getElementById('tx').textContent = ''")
            print('   pick:', g.ev(f"(h => h ? [h.object.name, (h.object.userData.item || {{}}).t, Math.round(h.distance * 10) / 10] : null)(pick({x}, {y}))"), 'player', g.ev("[player.obj.position.x, player.obj.position.z]"))
            g.page.mouse.click(x, y)
            for k in range(11):
                g.step(30); print('     t', k, g.ev("JSON.stringify([ACT && ACT.kind, roomAt(...player.here()), (() => { const it = ITEMS.find(i => i.t === `Welding bench`); it.hit.getWorldPosition(_wp); return Math.round(Math.hypot(_wp.x - player.obj.position.x, _wp.z - player.obj.position.z) * 10) / 10; })(), (() => { const m = machineList().find(m => m.id === `5-battery-1`); const s = placeSpot(panelPlace(m.id)); return s ? Math.round(Math.hypot(s.x - player.obj.position.x, s.z - player.obj.position.z) * 10) / 10 : null; })(), player.path.length, Math.round(player.obj.position.x * 10) / 10, Math.round(player.obj.position.z * 10) / 10, document.getElementById('tx').textContent.slice(0, 60)])"))
            print(f'{thing:14} near {mid:13} job held={held!s:5}:', g.ev(ST))
            g.ev("actEnd(true); player.stop()")
    g.close()

