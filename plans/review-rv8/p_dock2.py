# RV8 probe: FX3's pin taps at 390x844 with the crew on, real clicks (from FX3's own interactions_check part). p_pin.py GAME CT_DIR
import sys, json
exec(open(sys.argv[2] + '/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
# FX3 (fresh-eyes batch 2, items 33 and 38; lead 29): the arrow's pin on the thing you need, and a tap at the pin is that thing:
# a part you make points at the lathe (it pointed at the machine shop's middle), and "Turn it in at the job board" opens the
# board from its pin (the pin sat on empty floor when the board's wall was cut away). Four camera turns, real taps at the pin
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.page.add_style_tag(content='#toast{opacity:1!important}'); g.step(5)
    if g.ev("typeof jobReserve === 'function' && typeof MAKE_AT !== 'undefined' && !!placeById('5-make-1')"):
        print('== FX3: the pin on the lathe and on the job board')
        g.ev("(() => { if (SHIP.device && SHIP.device.settings) SHIP.device.settings.tips = false; const t = document.getElementById('devTip'); if (t) t.hidden = true; })()")   # a first-time tip card can sit over the pin
        pass   # RV8: crew left on: someone standing at the pin takes the tap (her card), as they should
        PIN = r"""(() => { const el = document.getElementById('ixGoal'), m = (el.style.transform.match(/translate\(([-\d.]+)px, ?([-\d.]+)px\)/) || []).slice(1).map(Number);
          return el.hidden || !m.length ? null : [m[0], m[1], el.children[2].textContent]; })()"""
        MAKE = r"""(() => { actEnd(true); for (const k of NEED_KEYS) SHIP.player.needs[k] = 100; needsT = null; NEED_GOAL = null; clearGoal(); closeLiftPanel && 0; if (typeof ixBoard !== 'undefined' && ixBoard.close) ixBoard.close(); setShipNow(1440 * 2 + 10 * 60); machinesNow(); for (const j of SHIP.jobs) if (j.claimedBy === 'you') { j.claimedBy = null; j.status = 'open'; }
          SHIP.player.carry = []; SHIP.player.work = null; const id = jobReserve('lights', SHIP.time.day, Math.max(0, SHIP.time.min - 1), 3); claimJob(id); SHIP.player.track = id; myWork(); const j = myJob();
          for (const p of j.parts) if (p !== j.make) SHIP.player.carry.push(p); if (deckDef.num !== 5) goToDeck(5); const s = placeSpot('5-make-1'); player.obj.position.set(s.x + 1.5, 0, s.z + 1); player.stop(); return id; })()"""
        TURN = r"""(() => { actEnd(true); for (const k of NEED_KEYS) SHIP.player.needs[k] = 100; needsT = null; NEED_GOAL = null; clearGoal(); const j = myJob(); if (j) { j.workDone = true; MACH_REV++; } SHIP.player.carry = []; const c = cellPos(...placeById('5-jobboard-1').at); player.obj.position.set(c.x + 1, 0, c.z + 2.5); player.stop(); })()"""
        HAUL = r"""(() => { actEnd(true); const b = document.getElementById('ixBoard'); if (b) b.hidden = true; for (const k of NEED_KEYS) SHIP.player.needs[k] = 100; needsT = null; NEED_GOAL = null; clearGoal();
          setShipNow(1440 * 3 + 13 * 60); machinesNow(); for (const j of SHIP.jobs) if (j.claimedBy === 'you') { j.claimedBy = null; j.status = 'open'; } SHIP.jobs = SHIP.jobs.filter(j => j.id !== 'fx3-haul');
          SHIP.manifest = manifestFor(4); const j = haulJob(shipNow(), haulCrates(), { crew: false }); j.id = 'fx3-haul'; SHIP.jobs.push(j); MACH_REV++; claimJob('fx3-haul'); SHIP.player.track = 'fx3-haul'; SHIP.player.carry = [];
          if (deckDef.num !== 5) goToDeck(5); const s = placeSpot(haulDock()), rm = roomAt(...cellAt(s.x, s.z)), t = (ROOM_TILES[rm] || []).filter(c => free(...c)).map(c => cellPos(...c)).filter(q => Math.hypot(q.x - s.x, q.z - s.z) > 1.4).sort((a, b) => Math.hypot(a.x - s.x, a.z - s.z) - Math.hypot(b.x - s.x, b.z - s.z))[0]; player.obj.position.set(t.x, 0, t.z); player.stop(); window.__room = [rm, roomAt(...player.here())]; })()"""
        out = []
        for rot in range(4):
            g.ev(HAUL); g.step(80)
            xy = g.ev("(() => { const it = ITEMS.find(i => i.t === 'Cart dock 1'), q = new THREE.Vector3(); it.hit.getWorldPosition(q); q.project(camera); return [(q.x + 1) / 2 * innerWidth, (1 - q.y) / 2 * innerHeight]; })()")
            g.ev("(() => { window.__taps = []; const f0 = playerFloorTap; if (!f0.__w) { playerFloorTap = function (p) { const r = f0.apply(this, arguments); __taps.push('floor ' + r); return r; }; playerFloorTap.__w = 1; } const t0 = playerTap; if (!t0.__w) { playerTap = function (it) { const r = t0.apply(this, arguments); __taps.push('item ' + it.t + ' ' + r); return r; }; playerTap.__w = 1; } })()")
            g.shot(f'dock-{rot}-before.png'); g.page.mouse.click(*xy); g.step(300); print('  turn', rot, 'rooms', g.ev('__room'), 'taps', g.ev('__taps'), 'next stop', g.ev("(() => { const j = myJob(), n = j && ixNextStop(j); return n && [n.s.step, n.s.places]; })()"))
            out.append([rot, [round(v) for v in xy], g.ev("ACT && ACT.kind"), g.page.evaluate("document.getElementById('toast').innerText")[:50]])
            g.ev("actEnd(true)"); g.page.keyboard.press('Escape'); g.step(5); g.page.click('#rot'); g.step(30)
        print('Cart dock 1, real clicks:', out)
    g.close()
