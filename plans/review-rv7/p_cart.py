# RV7: a haul run held by you, at the cart stop: (1) the follower's direct playerTap on the nearest item, (2) a real screen tap at the pin
import sys, os, json
BUILD = sys.argv[1]; sys.argv = [sys.argv[0], BUILD]
exec(open('arrows_check.py').read().split("GUIDE = 'guide' in")[0]); GUIDE = False
SET = r"""(() => { actEnd(true); const t = shipNow(); for (const j of SHIP.jobs) if (j.claimedBy === 'you') { j.claimedBy = null; j.status = 'open'; }
  const cs = (typeof manifestFor === 'function' ? manifestFor(SHIP.time.day) : []) || []; const j = haulJob(t, cs.slice(0, 1).length ? cs.slice(0, 1) : [{ id: 'medical supplies', key: 'rv7a', dest: '3-infirmary-1' }], { yours: true });
  SHIP.jobs.push(j); MACH_REV++; const ok = claimJob(j.id); if (deckDef.num !== 5) goToDeck(5);
  const st = jobStops(j)[0], s = placeSpot(st.places[0]); player.obj.position.set(s.x + 1.0, 0, s.z + 1.0); player.stop();
  return { ok, stop: st.step, place: st.places[0], goal: (goalNow() || {}).label }; })()"""
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    pg = Page(ctx, BUILD); real_game(pg, 3); pg.ev("devmodeSkipTo(2 * 1440 + 13 * 60)"); pg.step(10)
    print('set:', pg.ev(SET)); pg.step(60)
    for i in range(2):
        r = pg.ev(FOLLOW); pg.step(60)
        print('follower:', r, '| ACT', pg.ev("ACT && ACT.kind"), '| toast', pg.ev("document.getElementById('tt').textContent + ': ' + document.getElementById('tx').textContent"))
    pg.ev("actEnd(true)")
    xy = pg.ev("(() => { const g = goalNow(), w = ixGoalWorld(g), v = new THREE.Vector3(w.x, .05, w.z).project(camera); return [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight]; })()")
    under = pg.ev(f"(() => {{ const h = pick({xy[0]}, {xy[1]}); return h && h.object.userData.item ? h.object.userData.item.t : 'floor'; }})()")
    pg.page.mouse.click(*xy); pg.step(90)
    print('real tap at the pin: under', under, '| ACT', pg.ev("ACT && ACT.kind"), '| toast', pg.ev("document.getElementById('tt').textContent + ': ' + document.getElementById('tx').textContent"), '| goal', pg.ev("(goalNow() || {}).label"))
    print('errors', pg.errors[:3])
