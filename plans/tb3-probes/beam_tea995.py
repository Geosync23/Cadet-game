# TB3 probe for 0.99.5 notes 8 (Name on the beam) and 10 (Tea and biscuits), on a copy with TRAD995_ON on (and off, to compare).
#   8: Day 1, the beam at 390x844: where you stand to paint vs your name's spot on the beam (x), and no speech bubble's
#      box over the name's box on the screen while you paint and after; screenshots in OUT.
#   10: Day 3 (a Wednesday) 12:50-13:55 with you in the tea corner: every minute who is in the corner, sitting or standing,
#      nobody on the doorway tile [21, 1], and a path out of the corner (to [20, 1]) from where you stand.
#   python3 plans/tb3-probes/beam_tea995.py starship-cadet.html OUT_DIR [8] [10]
import sys, json, os, pathlib
sys.argv[0] = str(pathlib.Path(__file__).resolve().parents[2] / 'cadet_test.py')
exec(open(sys.argv[0]).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

build = sys.argv[1]; OUT = pathlib.Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True); PARTS = set(sys.argv[3:]) or {'8', '10'}
src = pathlib.Path(build).read_text()
on = src.replace("const TRAD995_ON = false ||", "const TRAD995_ON = true ||", 1); assert on != src, 'no TRAD995_ON switch'
COPIES = {}
for k, s in (('on', on), ('off', src)):
    p = WORK / 'test' / ('_bt995_%s_%d.html' % (k, os.getpid())); p.write_text(s); COPIES[k] = str(p)
FAILS = []
def check(c, m):
    print(('ok   ' if c else 'FAIL ') + m)
    if not c: FAILS.append(m)

# the name's box on the screen (its slot plane: 1.2 m by .19 m) and every bubble's box; the overlap in px
OVER = """JSON.stringify((() => { const w = beamSlotWorld(); if (!w) return null; const v = new THREE.Vector3(), pts = [];
  for (const dx of [-.6, .6]) for (const dy of [-.1, .1]) { v.set(w.x + dx, w.y + dy, w.z).project(camera); pts.push([(v.x + 1) * innerWidth / 2, (1 - v.y) * innerHeight / 2]); }
  const nb = [Math.min(...pts.map(p => p[0])), Math.min(...pts.map(p => p[1])), Math.max(...pts.map(p => p[0])), Math.max(...pts.map(p => p[1]))];
  const bubs = bubbles.list.filter(b => b.el.style.display !== 'none').map(b => { const r = b.el.getBoundingClientRect(), a = DECK_CREW.find(c => c.h === b.who || c.h === (b.who && b.who.H) || b.who && b.who.p && c.p.id === b.who.p.id), id = a && a.p.id;
    return [r.left, r.top, r.right, r.bottom, id + '@' + (a ? a.goalId + ' ' + a.x.toFixed(1) + ',' + a.z.toFixed(1) : '?')]; });
  const ov = bubs.map(b => [Math.max(0, Math.min(b[2], nb[2]) - Math.max(b[0], nb[0])) * Math.max(0, Math.min(b[3], nb[3]) - Math.max(b[1], nb[1])), b[4]]).filter(x => x[0] > 0);
  const sp = placeSpot('5-beam-1'), pp = ACT && ACT.phase === 'do' ? { x: ACT.x, z: ACT.z } : player.obj.position;
  const bl = bubbles.list.filter(b => b.el.style.display !== 'none').map(b => [Math.round(b.ax), Math.round(b.ay), Math.round(b.x), Math.round(b.y), b.w, b.hh, (DECK_CREW.find(c => c.h === b.who) || { p: { id: b.who && b.who.isPlayer ? 'YOU' : '?' } }).p.id, b.text.slice(0, 25)]);
  return { bl, name: nb.map(Math.round), slotX: +w.x.toFixed(2), spotX: +sp.x.toFixed(2), you: [+pp.x.toFixed(2), +pp.z.toFixed(2)], act: ACT ? [ACT.kind, ACT.placeId, ACT.phase] : null, bubs: bubs.length, over: ov }; })())"""

def beam(pw, k):
    g = Game(pw, COPIES[k], 390, 844)
    g.ev("""(() => { goToDeck(5); actEnd(true); clearGoal(); const d = 1, e = eventsOn(d).find(x => x.id === 'name-on-the-beam');
      SHIP.traces.length = 0; SHIP.events.joined = []; setShipNow((d - 1) * 1440 + e.from + 1); deckCrewFill(); SHIP.device.settings.tips = false;
      const sp = placeSpot('5-beam-6'); player.obj.position.set(sp.x, 0, sp.z + .6); player.stop(); EV_MIN = -1; eventsTick();
      if (typeof GUIDE_ON !== 'undefined' && GUIDE_ON) { GUIDE.tq.length = 0; guideToast = () => false; } })()""")
    for _ in range(160):
        g.step(30)
        if g.ev('beamReady()'): break
    ready = g.ev('beamReady()'); paint = g.ev('beamPaint()')
    worst = []; shots = 0
    for i in range(60):
        g.step(15); r = json.loads(g.ev(OVER))
        if r and r['act'] and r['act'][2] == 'do': worst.append(r)
        if r and r['act'] and r['act'][2] == 'do' and shots < 1: g.shot(str(OUT / ('beam_%s_painting.png' % k))); shots += 1
        if not g.ev('!!(ACT && ACT.o && ACT.o.beam)'): break
    after = []
    for i in range(30):
        g.step(30); r = json.loads(g.ev(OVER)); after.append(r)
        if i == 2: g.shot(str(OUT / ('beam_%s_after.png' % k)))
    ov = [x for r in worst if r for x in r['over']]; ova = [x for r in after if r and len(r['bl']) == 1 for x in r['over']]   # after: a lone bubble over it fails; a pair (a cheer lifted by other chatter) is reported
    pairs = [x for r in after if r and len(r['bl']) > 1 for x in r['over']]; print('  %s after, lifted by another bubble (reported): %s' % (k, pairs))
    print('  %s after (the crowd breaking up): %s' % (k, ova))
    for r in after:
        if r and r['over']: print('    ', r['name'], r['bl'], r['over'])
    print('  %s: ready %s, paint %s; painting at %s, name %s (x %.2f), spot x %.2f; bubbles over the name: %s' % (k, ready, paint, worst[0]['you'] if worst else None, worst[0]['name'] if worst else None, worst[0]['slotX'] if worst else 0, worst[0]['spotX'] if worst else 0, ov))
    err = g.errors; g.close()
    return worst, ov, ova, err

def tea(pw, k):
    g = Game(pw, COPIES[k], 900, 760)
    g.ev("(() => { skipTo(2 * 1440 + 765); goToDeck(5, null); SHIP.device.settings.tips = false; clearGoal(); for (const n of NEED_KEYS) SHIP.player.needs[n] = 90; })()")
    g.step(5)
    g.ev("(() => { const c = cellPos(22, 2); player.obj.position.set(c.x, 0, c.z); player.stop(); })()")
    rows = []
    for i in range(400):
        g.step(20)
        r = json.loads(g.ev("""JSON.stringify((() => { const m = SHIP.time.min, me = player.here(), att = DECK_CREW.filter(a => a.p && roomAt(...a.here()) === 't');
          const door = DECK_CREW.filter(a => a.p && a.settled && K(a.here()) === K([21, 1])).map(a => a.p.id);   // standing there, not walking through
          const out = !!findPath(me, [20, 1], occupiedBy(player), player);
          return [m, att.map(a => [a.p.id, a.goalId, a.settled ? (a.pose || '') : 'walk']), door, out, K(me)]; })())"""))
        rows.append(r)
        if r[0] >= 835: break
    err = g.errors; g.close()
    return rows, err

with sync_playwright() as pw:
    if '8' in PARTS:
        for k in ('off', 'on'):
            worst, ov, ova, err = beam(pw, k)
            if k == 'on':
                w = worst[0] if worst else None
                check(bool(w) and abs(w['you'][0] - w['slotX']) <= .45, '8: you paint standing under your name (you x %s, name x %s)' % (w and w['you'][0], w and w['slotX']))
                check(not ov, '8: no speech bubble over the name while you paint (%s)' % ov[:4]); check(not ova, '8: none over it while they cheer and go (%s)' % ova[:4])
                check(not err, '8: no errors %s' % err[:3])
    if '10' in PARTS:
        for k in ('off', 'on'):
            rows, err = tea(pw, k)
            mins = {}
            for r in rows: mins.setdefault(int(r[0]), r)
            sit = sum(1 for r in mins.values() for a in r[1] if a[1] in ('5-tea-1', '5-tea-2') and str(a[2]).startswith('sit'))
            stand = [(int(r[0]), a[0], a[1]) for r in mins.values() for a in r[1] if a[1] == '5-tea-3' and 780 <= r[0] < 840]
            door = [(int(r[0]), r[2]) for r in mins.values() if r[2]]
            stuck = [int(r[0]) for r in mins.values() if not r[3]]
            print('  %s: seated minute-people %d; at 5-tea-3 during tea %s; on the doorway %s; no way out at %s' % (k, sit, stand[:5], door[:6], stuck[:10]))
            for m in (782, 795, 810, 825):
                if m in mins: print('    %d: %s' % (m, mins[m][1]))
            if k == 'on':
                check(sit > 0, '10: crew sit down for tea (%d seated minute-people)' % sit)
                check(not stand, '10: nobody stands at 5-tea-3 for the 13:00 tea (%s)' % stand[:4])
                check(not door, '10: nobody on the doorway tile [21, 1] (%s)' % door[:4])
                check(not stuck, '10: you can walk out of the corner every minute (%s)' % stuck[:6])
                check(not err, '10: no errors %s' % err[:3])
for p in COPIES.values(): pathlib.Path(p).unlink(missing_ok=True)
print('BEAM TEA PROBE ' + ('OK' if not FAILS else 'FAILED (%d)' % len(FAILS)))
