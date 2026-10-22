# RV8 probe: FX3's pin taps at 390x844 with the crew on, real clicks (from FX3's own interactions_check part). p_pin.py GAME CT_DIR
import sys, json
exec(open(sys.argv[2] + '/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
# FX3 (fresh-eyes batch 2, items 33 and 38; lead 29): the arrow's pin on the thing you need, and a tap at the pin is that thing:
# a part you make points at the lathe (it pointed at the machine shop's middle), and "Turn it in at the job board" opens the
# board from its pin (the pin sat on empty floor when the board's wall was cut away). Four camera turns, real taps at the pin
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.step(5)
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
        res = {'lathe': [], 'board': []}
        for rot in range(4):
            jid = g.ev(MAKE); g.step(80); p = g.ev(PIN); g.shot(f'{sys.argv[3]}-lathe-{rot}.png')
            if p:
                g.page.mouse.click(p[0], p[1]); g.step(400)
                res['lathe'].append([rot, p[2], g.ev("ACT && ACT.kind"), g.ev(f"(e => e && (e.id || e.tagName))(document.elementFromPoint({p[0]}, {p[1]}))")])
            g.ev(TURN); g.step(80); p = g.ev(PIN); g.shot(f'{sys.argv[3]}-board-{rot}.png')
            if p:
                g.page.mouse.click(p[0], p[1]); g.step(400)
                res['board'].append([rot, p[2], g.ev("!!document.getElementById('ixBoard') && !document.getElementById('ixBoard').hidden"), g.ev(f"(e => e && (e.id || e.tagName))(document.elementFromPoint({p[0]}, {p[1]}))")])
            g.ev("(() => { const b = document.getElementById('ixBoard'); if (b) b.hidden = true; const j = myJob(); if (j) dropJob(j.id); })()"); g.page.click('#rot'); g.step(30)
        print('   the lathe [turn, label, started]:', res['lathe'])
        print('   the job board [turn, label, opened]:', res['board'])
        print('CHECK', len(res['lathe']) == 4 and all(x[1].endswith('at the lathe') and x[2] == 'make' for x in res['lathe']), f'a part you make: the pin on the lathe, and a tap there makes it ({res["lathe"]})')
        print('CHECK', len(res['board']) == 4 and all(x[1].startswith('Turn it in') and x[2] for x in res['board']), f'turn it in: a tap at the pin opens the job board ({res["board"]})')
        # a manifest run's first stop, the cart at Cart dock 1 (lead 29): the pin stands over the docks; a tap at the pin, or on
        # Cart dock 1 itself, takes the cart (on 2b4a05db the pin over a dock did nothing)
        HAUL = r"""(() => { actEnd(true); const b = document.getElementById('ixBoard'); if (b) b.hidden = true; for (const k of NEED_KEYS) SHIP.player.needs[k] = 100; needsT = null; NEED_GOAL = null; clearGoal();
          setShipNow(1440 * 3 + 13 * 60); machinesNow(); for (const j of SHIP.jobs) if (j.claimedBy === 'you') { j.claimedBy = null; j.status = 'open'; } SHIP.jobs = SHIP.jobs.filter(j => j.id !== 'fx3-haul');
          SHIP.manifest = manifestFor(4); const j = haulJob(shipNow(), haulCrates(), { crew: false }); j.id = 'fx3-haul'; SHIP.jobs.push(j); MACH_REV++; claimJob('fx3-haul'); SHIP.player.track = 'fx3-haul'; SHIP.player.carry = [];
          if (deckDef.num !== 5) goToDeck(5); const s = placeSpot(haulDock()); player.obj.position.set(s.x + 1.5, 0, s.z + 1); player.stop(); })()"""
        hl = []
        if g.ev("typeof haulJob === 'function' && typeof haulDock === 'function' && !!haulDock()"):
            for rot in range(4):
                g.ev(HAUL); g.step(80); p = g.ev(PIN); g.shot(f'{sys.argv[3]}-haul-{rot}.png')
                if p:
                    g.page.mouse.click(p[0], p[1]); g.step(300)
                    hl.append([rot, p[2], g.ev("ACT && ACT.kind")])
                g.page.click('#rot'); g.step(30)
            g.ev(HAUL); dk = g.ev("(() => { const it = ITEMS.find(i => i.t === 'Cart dock 1'); it.hit.getWorldPosition(_wp); const r = playerTap(it, _wp.clone(), _wp.clone()); return [r, ACT && ACT.kind]; })()")
            print('   the cart stop [turn, label, started]:', hl, '| Cart dock 1 tapped:', dk)
            print('CHECK', len(hl) == 4 and all(x[1].startswith('Take a hover cart') and x[2] == 'ixStop' for x in hl) and dk == [True, 'ixStop'], f'a run\'s cart stop: a tap at the pin, or on Cart dock 1, takes the cart ({hl}, {dk})')
            g.ev("actEnd(true); SHIP.jobs = SHIP.jobs.filter(j => j.id !== 'fx3-haul')")
        print('CHECK', not g.errors, f'no console errors ({g.errors[:3]})')
    g.close()

