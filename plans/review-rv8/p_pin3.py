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
        for wait in (80, 400):
            jid = g.ev(MAKE); g.step(wait); p = g.ev(PIN)
            w = g.ev("(() => { const w = ixGoalWorld(goalNow()), q = new THREE.Vector3(w.x, 0, w.z); q.project(camera); return [Math.round((q.x + 1) / 2 * innerWidth), Math.round((1 - q.y) / 2 * innerHeight)]; })()")
            g.ev("(() => { window.__taps = []; const f0 = playerFloorTap; playerFloorTap = function (p) { const r = f0.apply(this, arguments); __taps.push('floor ' + r); return r; }; const t0 = playerTap; playerTap = function (it) { const r = t0.apply(this, arguments); __taps.push('item ' + it.t + ' ' + r); return r; }; })()")
            g.page.mouse.click(p[0], p[1]); g.step(200)
            print('  wait', wait, 'pin', [round(p[0]), round(p[1])], 'goal point on screen', w, 'taps', g.ev("__taps"), 'ACT', g.ev("ACT && ACT.kind"), 'toast', repr(g.page.evaluate("document.getElementById('toast').innerText")[:60]))
            g.shot(f'{sys.argv[3]}-w{wait}.png')
    g.close()
