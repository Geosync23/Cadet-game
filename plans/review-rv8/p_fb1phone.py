# RV8 probe: FB1's parts at 390x844 (copied from FB1's interactions_check 228de58). p_fb1phone.py GAME CT_DIR
import sys, json
exec(open(sys.argv[2] + '/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
ok = True
def check(cond, msg):
    global ok
    if not cond: ok = False; print('FAIL', msg)
    return cond
TAP = r"""(({ title, near, place }) => {
  const its = ITEMS.filter(i => i.t === title); if (!its.length) return 'no item';
  const c = near ? cellPos(...near) : null;
  const it = its.map(i => { i.hit.getWorldPosition(_wp); return [i, _wp.clone()]; }).sort((a, b) => c ? a[1].distanceTo(c) - b[1].distanceTo(c) : 0)[0];
  if (place !== false) { const g = nearestOpen(it[1].x, it[1].z, player); player.obj.position.copy(cellPos(...g)); player.stop(); }
  return playerTap(it[0], it[1].clone(), it[1].clone());
})"""

with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.step(5)
    if g.ev("typeof manifestRun === 'function' && !!JOB_KINDS.haul && !!placeById('5-cart-1')"):
        print('== FB1: the hover cart at Cart dock 1')
        g.ev("goToDeck(5)"); g.step(5)
        TIPOFF = "(() => { if (SHIP.device && SHIP.device.settings) SHIP.device.settings.tips = false; const t = document.getElementById('devTip'); if (t) t.hidden = true; })()"   # a first-time tip card can sit over the thing
        SET = r"""(tag => { actEnd(true); setShipNow(1440 * 2 + 10 * 60); machinesNow(); for (const j of SHIP.jobs) if (j.claimedBy === 'you') { j.claimedBy = null; j.status = 'open'; }
          SHIP.jobs = SHIP.jobs.filter(j => !/^parts-fb1/.test(j.id)); SHIP.player.carry = []; SHIP.player.cart = null; SHIP.stores.relay = Math.max(SHIP.stores.relay || 0, 5);
          for (const k of NEED_KEYS) SHIP.player.needs[k] = 80;
          const id = manifestRun(['relay'], '3-store-drop', { for: 'fb1' }); if (!id) return null; claimJob(id);
          const st = jobStops(myJob()), k = st.findIndex(x => x.step === tag); for (let i = 0; i < k; i++) jobStepDone(id, i);
          const s = placeSpot('5-cart-1'); player.obj.position.set(s.x + 1.2, 0, s.z + 1.2); player.stop(); return [k, st[k].places[0]]; })"""
        # a point on the screen where the dock itself is under the finger (pick says so), as a player taps it
        ON = r"""(() => { const i = ITEMS.find(i => i.t === 'Cart dock 1'), b = new THREE.Box3().setFromObject(i.hit);
          for (let fy = .5; fy <= .9; fy += .2) for (let fx = .5, n = 0; n < 5; n++, fx = .5 + (n % 2 ? 1 : -1) * Math.ceil(n / 2) * .15) for (const fz of [.5, .3, .7]) {
            const v = new THREE.Vector3(b.min.x + (b.max.x - b.min.x) * fx, b.min.y + (b.max.y - b.min.y) * fy, b.min.z + (b.max.z - b.min.z) * fz).project(camera), x = (v.x + 1) / 2 * innerWidth, y = (1 - v.y) / 2 * innerHeight, h = pick(x, y);
            if (h && h.object.userData.item === i) return [x, y]; }
          return null; })()"""
        res = []
        for tag in ('cart', 'return'):
            for rot in range(4):
                kp = g.ev(f"({SET})('{tag}')"); g.step(60)
                for _ in range(rot): g.page.click('#rot'); g.step(30)
                g.ev(TIPOFF); xy = g.ev(ON)
                if not xy: res.append([tag, rot, 'no point on the dock', None, '']); continue
                g.page.mouse.move(*xy); g.page.mouse.down(); g.page.mouse.up(); g.step(60)
                a = g.ev("JSON.stringify(ACT && [ACT.kind, ACT.o && ACT.o.ixStep])")
                res.append([tag, rot, kp, a, g.ev("document.getElementById('tt').textContent + ': ' + document.getElementById('tx').textContent")[:50]])
        print('   [stop, camera turn, (stop, its place), what started, the toast]:', res)
        for tag in ('cart', 'return'):
            check(sum(1 for r in res if r[0] == tag and r[3]) >= 2, f'the dock under the finger in at least two camera turns for the "{tag}" stop ({res})')
        for r in res:
            if r[3]: check(json.loads(r[3]) == ['ixStop', r[2][0]], f'a real tap on Cart dock 1 does the haul\'s "{r[0]}" stop (camera turn {r[1]}: {r[3]}, {r[4]})')
        # out of reach: the machines further from a haul stop keep their own (JOB_REACH 1.5 from the thing's edge)
        far = g.ev(r"""(() => { const s = placeSpot('5-cart-1'); return ITEMS.filter(i => /^(Lathe|Breaker cabinet)$/.test(i.t) && isShown(i.hit)).map(i => [i.t, Math.round(ixDist(i, s) * 100) / 100]); })()""")
        print('   by the dock, out of reach:', far)
        check(far and all(d >= 1.5 for _, d in far), f'the Lathe and the Breaker cabinet are out of the dock stop\'s reach ({far})')
        g.ev("actEnd(true); SHIP.jobs = SHIP.jobs.filter(j => !/^parts-fb1/.test(j.id))")
        # pushing a haul's cart to its drop, anything in reach does the stop (lead 29): the linen's drop in the laundry, where
        # the Folding table nearest the pin started your own laundry (0.28.55's rule) and the arrows_check follower looped there
        if g.ev("!!placeById('4-laundry-drop')"):
            g.ev("goToDeck(4)"); g.step(5)
            HSET = r'''(() => { actEnd(true); setShipNow(1440 * 2 + 12 * 60 + 20); machinesNow(); for (const j of SHIP.jobs) if (j.claimedBy === 'you') { j.claimedBy = null; j.status = 'open'; }
              SHIP.jobs = SHIP.jobs.filter(j => !/^haul.*fb1|^haul@.*y$/.test(j.id)); SHIP.player.carry = []; for (const k of NEED_KEYS) SHIP.player.needs[k] = 80;
              const j = haulJob(shipNow(), [{ id: 'linen', dest: '4-laundry-drop' }], { yours: true }); SHIP.jobs.push(j); MACH_REV++; claimJob(j.id);
              const st = jobStops(myJob()), k = st.findIndex(x => x.step === 'deliver'); for (let i = 0; i < k; i++) jobStepDone(j.id, i);
              const s = placeSpot('4-laundry-drop'); player.obj.position.set(s.x + 1, 0, s.z + 1); player.stop(); return [k, j.id]; })()'''
            ONT = ON.replace("i.t === 'Cart dock 1'", "i.t === 'Folding table' && isShown(i.hit) && ixDist(i, placeSpot('4-laundry-drop')) < 1.5")
            fres = []
            for rot in range(4):
                kp = g.ev(HSET); g.step(60)
                for _ in range(rot): g.page.click('#rot'); g.step(30)
                g.ev(TIPOFF); xy = g.ev(ONT)
                if not xy: fres.append([rot, 'no point on the table', None]); continue
                g.page.mouse.move(*xy); g.page.mouse.down(); g.page.mouse.up(); g.step(60)
                fres.append([rot, kp, g.ev(f"(k => {{ const j = SHIP.jobs.find(x => x.id === {json.dumps(kp[1])}); return j && jobStops(j)[k].done ? JSON.stringify(['ixStop', k]) : JSON.stringify(ACT && [ACT.kind, ACT.o && ACT.o.ixStep]); }})({kp[0]})")])   # done already counts
            print('   the linen\'s drop, a tap on the Folding table [camera turn, (stop, job), what started]:', fres)
            check(sum(1 for r in fres if r[2]) >= 2, f'the Folding table under the finger in at least two camera turns ({fres})')
            for r in fres:
                if r[2]: check(json.loads(r[2]) == ['ixStop', r[1][0]], f'pushing the linen to the laundry, a tap on the Folding table by the drop delivers it (camera turn {r[0]}: {r[2]})')
            # with no haul the table is your laundry again (0.28.55; parity above taps it too)
            g.ev("actEnd(true); for (const j of SHIP.jobs) if (j.claimedBy === 'you') { j.claimedBy = null; j.status = 'open'; } SHIP.jobs = SHIP.jobs.filter(j => !/^haul@.*y$/.test(j.id)); MACH_REV++")
            g.step(5); g.ev(f"(() => {{ const s = placeSpot('4-laundry-drop'); player.obj.position.set(s.x + 1, 0, s.z + 1); player.stop(); }})()"); g.step(30)
            g.ev(TIPOFF); xy = g.ev(ONT)
            if xy:
                g.page.mouse.move(*xy); g.page.mouse.down(); g.page.mouse.up(); g.step(60)
                a = g.ev("ACT && ACT.kind"); print('   no haul, the Folding table:', a)
                check(a == 'ixFold', f'with no haul, the Folding table by the drop is your laundry ({a})')
            g.ev("actEnd(true)")
        check(not g.errors, f'no console errors ({g.errors[:3]})')
    g.close()

# FB1 (lead 29, RV7): every pick-up and drop of a haul and of a delivery, with real screen taps: at the arrow's pin, and on the
# thing nearest the stop when it's in reach, four camera turns each. RV7 found "Crew store stock to the crew store", "Linen to
# the laundry", "Pick up a crate of linen" and the infirmary's medical supplies stuck: the thing under the finger did its own
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.step(5)
    if g.ev("typeof haulJob === 'function' && typeof DELIVERIES !== 'undefined' && !!haulDock() && !!haulLoadAt()"):
        print('== FB1: every pick-up and drop of a haul and a delivery, real taps')
        g.ev("(() => { if (SHIP.device && SHIP.device.settings) SHIP.device.settings.tips = false; const t = document.getElementById('devTip'); if (t) t.hidden = true; if (typeof bridgeInvite === 'function') bridgeInvite(); else SHIP.bridgeInvited = true; })()")
        g.page.click('#crew'); g.step(5)   # the crew hidden: someone standing at a pin takes the tap (their card), as they should
        PIN = r"""(() => { const el = document.getElementById('ixGoal'), m = (el.style.transform.match(/translate\(([-\d.]+)px, ?([-\d.]+)px\)/) || []).slice(1).map(Number);
          return el.hidden || !m.length ? null : [m[0], m[1], el.children[2].textContent]; })()"""
        # (kind, key, the stop's step): a haul of one crate per drop (its cart, load, deliver and return), a delivery's pickup and drop
        STOPS = g.ev(r"""(() => { const out = [['haul', 'linen', 'cart'], ['haul', 'linen', 'load'], ['haul', 'linen', 'return']];
          for (const k of Object.keys(MANIFEST_DROP)) if (placeById(MANIFEST_DROP[k])) out.push(['haul', k, 'deliver']);
          for (const d of DELIVERIES) if (placeById(d.from) && placeById(d.to)) { out.push(['delivery', d.key, 'pickup']); out.push(['delivery', d.key, 'drop']); }
          return out; })()""")
        SET = r"""(([kind, key, step]) => { actEnd(true); const b = document.getElementById('ixBoard'); if (b) b.hidden = true; for (const k of NEED_KEYS) SHIP.player.needs[k] = 100; needsT = null; NEED_GOAL = null; clearGoal();
          setShipNow(1440 * 2 + 10 * 60); machinesNow(); for (const j of SHIP.jobs) if (j.claimedBy === 'you') { j.claimedBy = null; j.status = 'open'; } SHIP.jobs = SHIP.jobs.filter(j => !/^fb1-/.test(j.id));
          SHIP.player.carry = []; SHIP.player.work = null; if (SHIP.player.crate) SHIP.player.crate = null; const t = shipNow(); let j;
          if (kind === 'haul') { j = haulJob(t, [{ id: key, dest: MANIFEST_DROP[key] }], { crew: false }); j.id = 'fb1-haul'; }
          else { const d = DELIVERIES.find(x => x.key === key), to = placeById(d.to), fr = placeById(d.from);
            j = { id: 'fb1-del', machine: null, deck: to.deck, room: to.room, kind: 'chore', chore: 'delivery', title: d.title, bring: d.bring, tier: 1, urgency: 1, posted: t, found: t, claimedBy: null, parts: [], status: 'open',
              stops: [{ deck: fr.deck, placeId: d.from, mins: 3, tag: 'pickup' }, { deck: to.deck, placeId: d.to, mins: 3, tag: 'drop' }] }; }
          SHIP.jobs.push(j); MACH_REV++; claimJob(j.id); SHIP.player.track = j.id;
          const st = jobStops(myJob()), k = st.findIndex(x => x.step === step); for (let i = 0; i < k; i++) jobStepDone(j.id, i);
          const pid = st[k].places[0], pl = placeById(pid); if (deckDef.num !== pl.deck) goToDeck(pl.deck);
          const s = placeSpot(pid); player.obj.position.copy(cellPos(...nearestOpen(s.x + 1.3, s.z + 1.3, player))); player.stop(); return [k, pid]; })"""
        # a screen point on the thing nearest the stop (in reach, shown), where pick() says that thing is under the finger
        ON = r"""(pid => { const s = placeSpot(pid), its = ITEMS.filter(i => i.hit && isShown(i.hit) && ixDist(i, s) < JOB_REACH).sort((a, b) => ixDist(a, s) - ixDist(b, s));
          for (const i of its) { const b = new THREE.Box3().setFromObject(i.hit);
            for (const fy of [.5, .7, .3, .9]) for (const fx of [.5, .35, .65, .2, .8]) for (const fz of [.5, .35, .65, .2, .8]) {
              const v = new THREE.Vector3(b.min.x + (b.max.x - b.min.x) * fx, b.min.y + (b.max.y - b.min.y) * fy, b.min.z + (b.max.z - b.min.z) * fz).project(camera), x = (v.x + 1) / 2 * innerWidth, y = (1 - v.y) / 2 * innerHeight, h = pick(x, y);
              if (x > 0 && y > 0 && x < innerWidth && y < innerHeight && h && h.object.userData.item === i) return [x, y, i.t]; } }
          return null; })"""
        bad, n = [], {'pin': 0, 'thing': 0}
        for stop in STOPS:
            row = []
            for rot in range(4):
                for how in ('pin', 'thing'):
                    kp = g.ev(f"({SET})({json.dumps(stop)})"); g.step(60)
                    for _ in range(rot): g.page.click('#rot'); g.step(30)
                    g.ev("(() => { const t = document.getElementById('devTip'); if (t) t.hidden = true; })()")   # a first-time tip card can sit over the pin
                    p = g.ev(PIN) if how == 'pin' else g.ev(f"({ON})({json.dumps(kp[1])})")
                    if not p: row.append(f'{rot}{how[0]}:-'); continue
                    g.page.mouse.move(p[0], p[1]); g.page.mouse.down(); g.page.mouse.up(); g.step(400)
                    a = g.ev(f"(k => {{ const j = SHIP.jobs.find(x => /^fb1-/.test(x.id)); return j && jobStops(j)[k].done ? 'done' : JSON.stringify(ACT && [ACT.kind, ACT.o && ACT.o.ixStep]); }})({kp[0]})")
                    good = a == 'done' or a == json.dumps(['ixStop', kp[0]]).replace(' ', '')   # the stop done, or under way (a short stop is over by now)
                    n[how] += 1; row.append(f'{rot}{how[0]}:{"ok" if good else a}' + ('' if how == 'pin' else '(' + p[2] + ')'))
                    if not good: bad.append([stop, rot, how, p[2], a, g.ev("document.getElementById('tt').textContent + ': ' + document.getElementById('tx').textContent")[:60]])
                g.page.click('#rot'); g.step(30)
            print(f'   {stop[0]} {stop[1]} {stop[2]} ({kp[1]}):', ' '.join(row))
        print(f'   taps: {n["pin"]} at the pin, {n["thing"]} on the thing')
        check(n['pin'] >= 3 * len(STOPS) and n['thing'] >= len(STOPS), f'the pin and a thing in reach under the finger for every stop ({n}, {len(STOPS)} stops)')
        for b in bad: check(False, f'a real tap does the stop: {b}')
        g.ev("actEnd(true); SHIP.jobs = SHIP.jobs.filter(j => !/^fb1-/.test(j.id))")
        check(not g.errors, f'no console errors ({g.errors[:3]})')
    g.close()

# FB1 (lead 29, arrows_check week Day 6): "Put the seal back: main storage" (FX3's fix 9) stuck over 3 hours: a tap on the shelf
# nearest the arrow's pin walked you round to the shelf's front, 7 tiles away, and the follower's next step pulled you back.
# Now a part goes back from the shelf's spot nearest the tap, as a fetch does (a step or two from the pin, under 2.2 m): real taps
# on the shelf nearest the pin, four camera turns
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.step(5)
    if g.ev("typeof ixLoose === 'function' && typeof shelfOf === 'function' && !!shelfOf('seal')"):
        print('== FB1: put a part back from the arrow\'s pin')
        g.ev("goToDeck(5)"); g.step(5); g.page.click('#crew'); g.step(5)
        PB = r"""(() => { actEnd(true); for (const k of NEED_KEYS) SHIP.player.needs[k] = 100; needsT = null; NEED_GOAL = null; clearGoal(); if (SHIP.device && SHIP.device.settings) SHIP.device.settings.tips = false; const t = document.getElementById('devTip'); if (t) t.hidden = true;
          setShipNow(1440 * 5 + 7 * 60 + 30); machinesNow(); for (const j of SHIP.jobs) if (j.claimedBy === 'you') { j.claimedBy = null; j.status = 'open'; } MACH_REV++; SHIP.player.carry = ['seal']; SHIP.player.work = null; SHIP.player.track = undefined;
          const w = placeSpot(shelfOf('seal')); player.obj.position.copy(cellPos(...nearestOpen(w.x, w.z, player))); player.stop(); return [w.x, w.z]; })()"""
        ONS = r"""(w => { const its = ITEMS.filter(i => i.hit && isShown(i.hit) && /^(Lights|Filters|Plumbing|Galley parts)$/.test(i.t)).map(i => { i.hit.getWorldPosition(_wp); return [i, Math.hypot(_wp.x - w[0], _wp.z - w[1])]; }).sort((a, b) => a[1] - b[1]);
          for (const [i] of its.slice(0, 2)) { const b = new THREE.Box3().setFromObject(i.hit);
            for (const fy of [.5, .7, .3]) for (const fx of [.5, .35, .65, .2, .8]) for (const fz of [.5, .35, .65, .2, .8]) {
              const v = new THREE.Vector3(b.min.x + (b.max.x - b.min.x) * fx, b.min.y + (b.max.y - b.min.y) * fy, b.min.z + (b.max.z - b.min.z) * fz).project(camera), x = (v.x + 1) / 2 * innerWidth, y = (1 - v.y) / 2 * innerHeight, h = pick(x, y);
              if (x > 0 && y > 0 && x < innerWidth && y < innerHeight && h && h.object.userData.item === i) return [x, y, i.t]; } }
          return null; })"""
        res = []
        for rot in range(4):
            w = g.ev(PB); g.step(30)
            for _ in range(rot): g.page.click('#rot'); g.step(30)
            lab = g.ev("(goalNow() || {}).label"); p = g.ev(f"({ONS})({json.dumps(w)})")
            if not p: res.append([rot, lab, 'no shelf under the finger']); continue
            g.page.mouse.move(p[0], p[1]); g.page.mouse.down(); g.page.mouse.up(); g.step(3)
            a = g.ev(f"(w => ACT && ACT.kind === 'stow' && ACT.spot ? ['stow', Math.round(Math.hypot(ACT.spot.x - w[0], ACT.spot.z - w[1]) * 10) / 10] : [ACT && ACT.kind, null])({json.dumps(w)})")
            g.step(600); res.append([rot, lab, p[2], a, g.ev("JSON.stringify(SHIP.player.carry)")])
        print('   [camera turn, the arrow, shelf tapped, (started, its spot from the pin in m), in hand after]:', res)
        check(len([r for r in res if len(r) > 3]) >= 3, f'a shelf by the pin under the finger in at least three camera turns ({res})')
        for r in res:
            if len(r) > 3: check(r[1] == 'Put the seal back: main storage' and r[3][0] == 'stow' and r[3][1] is not None and r[3][1] < 2.2 and r[4] == '[]',
                                 f'a tap on the shelf by the put-back pin puts the seal back from the spot by the pin (camera turn {r[0]}: {r})')
        check(not g.errors, f'no console errors ({g.errors[:3]})')
    g.close()

print('PHONE OK' if ok else 'PHONE FAILED')
