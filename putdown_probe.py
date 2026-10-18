# Starship Cadet: Put down probe (0.28.60; a one-off targeted check, kept next to the other checks)
# Holds a part, a tray and a delivery crate and puts each down with the real #putDown button, on a phone-sized view:
#   hidden with empty hands; clear of the needs strip, the Device and Pause buttons; a part goes back on the shelf
#   (and a chore's fetch stop opens again); a tray goes; a crate is set down where you stand, the drop stop waits for
#   it, the pointer leads to it, a tap on it picks it up, and left overnight the crew take it back (pickup opens again)
# Run:  python3 putdown_probe.py BUILD.html
import sys, json
exec(open(__file__.replace('putdown_probe.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
ok = True
def check(cond, msg):
    global ok
    print('ok  ' if cond else 'FAIL', msg)
    if not cond: ok = False
    return cond
TOAST = "document.getElementById('tt').textContent + ': ' + document.getElementById('tx').textContent"
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844)
    vis = lambda: g.ev("!document.getElementById('putDown').hidden")
    g.ev("goToDeck(5)"); g.step(5)
    check(not vis(), 'hidden with empty hands')
    # a loose part
    g.ev("SHIP.stores.filter = 2; SHIP.player.carry.push('filter')"); g.step(3)
    check(vis(), 'shown with a part in hand')
    r = g.ev("""(() => { const b = document.getElementById('putDown').getBoundingClientRect(), hit = (id) => { const e = document.getElementById(id); if (!e || e.hidden || !e.offsetParent && getComputedStyle(e).position !== 'fixed') return false;
      const q = e.getBoundingClientRect(); return q.width > 0 && !(q.right <= b.left || q.left >= b.right || q.bottom <= b.top || q.top >= b.bottom); };
      return { w: b.width, h: b.height, right: innerWidth - b.right, bottom: innerHeight - b.bottom, over: ['needStrip', 'devBtn', 'pauseBtn', 'room'].filter(hit) }; })()""")
    print('    button', r)
    check(r['h'] >= 44 and r['w'] >= 44 and r['right'] < 30 and r['bottom'] < 40, 'thumb-sized, in the bottom-right corner')
    check(not r['over'], f"clear of the needs strip, Device and Pause ({r['over']})")
    g.page.click('#putDown'); g.step(3)
    check(g.ev("SHIP.player.carry.length") == 0 and g.ev("SHIP.stores.filter") == 3, 'the part goes back on the shelf')
    t = g.ev(TOAST); print('   ', t); check('back on the shelf' in t, 'with a toast')
    check(not vis(), 'hidden again')
    # a lamp chore: the part comes back and the fetch stop opens again
    job = g.ev("""(() => { const c = choreWhere('lamp')[0]; if (!c) return null; const C = CHORES.lamp, t = shipNow();
      (C.parts || []).forEach(p => SHIP.stores[p] = Math.max(SHIP.stores[p] || 0, 3));
      const j = { id: 'pd-lamp@1', machine: null, deck: c.deck, room: c.room, kind: 'chore', chore: 'lamp', target: c.key, title: c.title, bring: c.bring || null, tier: 1,
        stops: c.stops.map(x => ({ ...x })), urgency: 0, posted: t, found: t, claimedBy: null, parts: C.parts.slice(), status: 'open' };
      SHIP.jobs.push(j); MACH_REV++; return claimJob(j.id) && j.id; })()""")
    if check(job, 'a lamp chore taken'):
        g.ev("(() => { const j = myJob(); for (const p of j.parts) if (takePart(p)) SHIP.player.carry.push(p); jobStepDone(j.id, 0); })()"); g.step(3)
        before = g.ev("[jobStops(myJob())[0].done, SHIP.stores[myJob().parts[0]]]")
        g.page.click('#putDown'); g.step(3)
        after = g.ev("[jobStops(myJob())[0].done, SHIP.stores[myJob().parts[0]], !!myJob()]")
        check(before[0] and not after[0] and after[1] == before[1] + 1 and after[2], f'lamp back on the shelf, fetch stop open again, job still yours ({before} -> {after})')
        g.ev("dropJob(myJob().id)")
    # a tray
    g.ev("goToDeck(3)"); g.step(5)
    g.ev("SHIP.player.tray = 'the stew'"); g.step(3)
    check(vis() and g.ev("player.holding") == 'tray', 'shown with a tray')
    g.page.click('#putDown'); g.step(3)
    check(not g.ev("SHIP.player.tray") and not vis(), 'the tray goes'); t = g.ev(TOAST); print('   ', t); check('tray return' in t, 'to the tray return')
    # a delivery crate
    job = g.ev("""(() => { const c = choreWhere('delivery')[0]; if (!c) return null; const C = CHORES.delivery, t = shipNow();
      const j = { id: 'pd-del@1', machine: null, deck: c.deck, room: c.room, kind: 'chore', chore: 'delivery', target: c.key, title: c.title, bring: c.bring || null, tier: 1,
        stops: c.stops.map(x => ({ ...x })), urgency: 0, posted: t, found: t, claimedBy: null, parts: (C.parts || []).slice(), status: 'open' };
      SHIP.jobs.push(j); MACH_REV++; return claimJob(j.id) && [j.id, jobStops(j).map(x => x.step + '@' + x.deck)]; })()""")
    if check(job, f'a delivery chore taken {job}'):
        pick = g.ev("jobStops(myJob()).findIndex(x => x.step === 'pickup')")
        g.ev(f"jobStepDone(myJob().id, {pick})"); g.step(3)
        check(g.ev("player.holding") == 'carry' and vis(), 'crate in hand, button shown')
        g.ev("SHIP.player.track = undefined")                # tracking on, as taking it at the board does
        deck = g.ev("deckDef.num"); g.page.click('#putDown'); g.step(5)
        c = g.ev("SHIP.player.crate")
        check(c and c['deck'] == deck and g.ev("player.holding") != 'carry' and not vis(), f'crate set down here ({c})')
        check(g.ev("!!(PUT_CRATE && PUT_CRATE.visible)"), 'the crate is on the floor')
        g.step(40); lab = g.ev("document.getElementById('ixGoal').hidden ? null : document.querySelector('#ixGoal .ixlab').textContent")
        check(lab and 'crate' in lab.lower(), f'the pointer leads to it ({lab})')
        check(g.ev("!!myJob() && myJob().id === 'pd-del@1'"), 'the job stays yours')
        # the drop stop waits for the crate
        drop = g.ev("(() => { const st = jobStops(myJob()), k = st.findIndex(x => x.step === 'drop'); return [k, st[k].deck, st[k].places[0]]; })()")
        g.ev(f"goToDeck({drop[1]})"); g.step(5)
        r = g.ev(f"""(() => {{ const s = placeSpot('{drop[2]}'); const it = ITEMS.filter(i => !i.lift && !i.see).map(i => [i, ixDist(i, s)]).sort((a, b) => a[1] - b[1])[0][0];
          it.hit.getWorldPosition(_wp); return [ixChoreTap(it, _wp.clone()), ACT && ACT.kind]; }})()""")
        t = g.ev(TOAST); check(r[0] is True and r[1] is None and 'Pick it up first' in t, f'the drop waits for the crate ({r}, {t[:90]})')
        # tap the crate to pick it up
        g.ev(f"goToDeck({deck})"); g.step(5)
        xy = g.ev("""(() => { const c = SHIP.player.crate, p = nearestOpen(c.x + 1.5, c.z, player); player.obj.position.copy(cellPos(...p)); player.stop(); return true; })()"""); g.step(30)
        xy = g.ev("(() => { const c = SHIP.player.crate, v = new THREE.Vector3(c.x, .25, c.z).project(camera); return [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight]; })()")
        for tries in range(4):                           # a crew member passing in front takes the tap: try again
            g.page.mouse.click(xy[0], xy[1])
            for k in range(20):
                g.step(15)
                if not g.ev("SHIP.player.crate"): break
            if not g.ev("SHIP.player.crate"): break
            print('    retry:', g.ev(TOAST)[:80])
        check(not g.ev("SHIP.player.crate") and g.ev("player.holding") == 'carry', f'a tap on the crate picks it up ({xy}, {g.ev(TOAST)[:80]})')
        # left overnight: the crew take it back to the pickup
        g.page.click('#putDown'); g.step(3)
        g.step(5); check(g.ev("!!SHIP.player.crate"), 'set down this morning: still there (the tidy is tomorrow 05:00)')
        check(g.ev("[putTidyAt(1440 * 3 + 23 * 60 + 55), 1440 * 4 + 10 < putTidyAt(1440 * 3 + 23 * 60 + 55), putTidyAt(1440 * 3 + 180), putTidyAt(1440 * 3 + 300)]") == [1440 * 4 + 300, True, 1440 * 3 + 300, 1440 * 4 + 300],
              'the tidy is the first 05:00 after: 23:55 is still down at 00:10, gone at 05:00')
        g.ev("SHIP.player.crate.at = Math.floor(shipNow() / 1440) * 1440 - 1440 + 600"); g.step(5)   # set down yesterday morning: past this 05:00
        t = g.ev(TOAST)
        check(not g.ev("SHIP.player.crate") and not g.ev(f"jobStops(myJob())[{pick}].done") and 'night tidy' in t, f'at 05:00 the crew take it back; pickup open again ({t[:90]})')
        check(not g.ev("PUT_CRATE.visible"), 'gone from the floor')
        # saved
        g.ev(f"jobStepDone(myJob().id, {pick})"); g.step(2); g.page.click('#putDown'); g.step(2)
        sv = g.ev("(() => { const s = {}; SAVE_EXTRA.forEach(f => { try { f(s); } catch (e) {} }); return s.player && s.player.crate; })()")
        check(sv and sv['job'] == 'pd-del@1', f'the set-down crate is saved ({sv})')
        g.ev("dropJob(myJob().id)"); g.step(3)
        check(not g.ev("SHIP.player.crate"), 'job dropped: the crew take the crate back')
    # never mid lift ride (reviewer 1g's LOW): hidden, and putDown refuses
    g.ev("SHIP.player.tray = null; SHIP.player.carry.push('filter')"); g.step(3)
    g.ev("startRide(deckDef.num === 4 ? 5 : 4)"); g.step(3)
    check(g.ev("!!ride") and not vis() and g.ev("putDown()") is False and g.ev("SHIP.player.carry.length") == 1, 'hidden mid lift ride, and putDown does nothing')
    for k in range(40):
        g.step(15)
        if not g.ev("!!ride"): break
    check(vis(), 'back after the ride')
    g.ev("SHIP.player.carry.length = 0"); g.step(3)
    # a gift alone and the kit bag alone don't show the button
    g.ev("SHIP.player.carry.push(KIT_BAG)"); g.step(3); check(not vis(), 'not for the kit bag (your locker)')
    g.ev("SHIP.player.carry.length = 0"); g.step(2)
    check(not g.errors, f'no console errors ({g.errors[:3]})')
    g.close()
print('PUT DOWN PROBE OK' if ok else 'PUT DOWN PROBE FAILED')
