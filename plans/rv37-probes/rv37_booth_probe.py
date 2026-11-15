# RV37: lead 52's round question (R4's fresh_walk, Day 2 18:00, the call booths' arrow): with someone standing on a
# room arrow's pin, where does a tap at the pin go, FRP_PINTAP_ON off against on, same state? Prints; judges nothing.
# Run from a checkout that has frp_check.py and arrows_check.py:  python3 rv37_booth_probe.py CANDIDATE.html
import sys, os, json, re
BUILD = sys.argv[1]; sys.argv = [sys.argv[0], BUILD]
exec(open('frp_check.py').read().split('\ndef part_line')[0].replace('os.path.dirname(os.path.abspath(__file__))', 'os.getcwd()'))
TAPS = r"""(() => {
  const tc = tapCrew, pt = playerTap, pg = playerGo, co = typeof chatOpen === 'function' ? chatOpen : null; let cur = null;
  tapCrew = function (cx, cy, who) { const a = who || crewAtScreen(cx, cy); if (!a) return false; cur.push('person:' + a.p.id); return true; };
  playerTap = function (it) { cur.push('thing:' + (it && it.t)); return true; };
  playerGo = function () { cur.push('walk'); return true; };
  const g = goalNow(), w = ixGoalWorld(g); _cp.set(w.x, .05, w.z).project(camera); const fl = [(_cp.x + 1) / 2 * innerWidth, (1 - _cp.y) / 2 * innerHeight];
  const was = FRP_PINTAP_ON, out = { goal: { room: g.room, crew: g.crew || null, place: g.place || null }, pin: [Math.round(IX_PIN.x), Math.round(IX_PIN.y)], floor: fl.map(Math.round), rows: [] };
  try { for (const [name, x, y] of [['the pin as drawn', IX_PIN.x, IX_PIN.y], ['the floor under it', fl[0], fl[1]], ['the pin head (20 px up)', IX_PIN.x, IX_PIN.y - 20], ['its label (14 px down)', IX_PIN.x, IX_PIN.y + 14]]) {
    const a = crewAtScreen(x, y), r = on => { FRP_PINTAP_ON = on; cur = []; IX_PIN.t = performance.now(); tap(x, y); return cur.join('+') || 'nothing'; };
    out.rows.push([name, a ? a.p.id : null, r(false), r(true)]); } }
  finally { tapCrew = tc; playerTap = pt; playerGo = pg; FRP_PINTAP_ON = was; }
  return out; })()"""
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}); pg = page(ctx, pathlib.Path(BUILD).read_text(), 'rvbooth')
    print('FRP_PINTAP_ON in this build:', pg.ev('FRP_PINTAP_ON'))
    jump(pg, 2, 18 * 60 + 1); pg.ev("goToDeck(3); for (const k of NEED_KEYS) SHIP.player.needs[k] = 90; needGoalClear()"); pg.step(60)
    print('the arrow at Day 2 18:01:', pg.ev("(() => { const g = goalNow(); return g && { label: g.label, room: g.room, crew: g.crew, place: g.place }; })()"))
    # the room arrow as the walk had it (no Leila in the room yet), with someone moved onto the pin's point
    pg.ev("clearGoal(); setGoal({ deck: 3, room: 'B', label: 'Calling home, the booths on Deck 3: Leila shows you how' })")
    w = pg.ev("(() => { const w = ixGoalWorld(goalNow()); return [w.x, w.z]; })()")
    pg.ev(f"(() => {{ const gl = nearestOpen({w[0]} + 1.5, {w[1]} + 1.5, player); player.obj.position.copy(cellPos(...gl)); player.stop(); }})()")
    who = pg.ev(f"(() => {{ const a = DECK_CREW.filter(x => x.p && x.h && x.settled).sort((p, q) => Math.hypot(p.x - {w[0]}, p.z - {w[1]}) - Math.hypot(q.x - {w[0]}, q.z - {w[1]}))[0]; return a ? [a.p.id, Math.hypot(a.x - {w[0]}, a.z - {w[1]})] : null; }})()")
    print('nearest person to the pin as the deck stands:', who)
    for moved in (False, True):
        if moved: pg.ev(f"(() => {{ const a = DECK_CREW.find(x => x.p && x.p.id === {json.dumps(who[0])}); a.x = {w[0]}; a.z = {w[1]}; if (a.h && a.h.position) a.h.position.set({w[0]}, a.h.position.y, {w[1]}); if (a.obj && a.obj.position) a.obj.position.set({w[0]}, a.obj.position.y, {w[1]}); }})()")
        pg.ev('window.__draw = true'); pg.step(90, 30); pg.ev('window.__draw = false'); print('   pin drawn in the last half second:', pg.ev('performance.now() - IX_PIN.t < 500'), '| player to pin:', pg.ev(f'Math.hypot(player.obj.position.x - {w[0]}, player.obj.position.z - {w[1]})'))
        r = pg.ev(TAPS); print(('with %s moved onto the pin' % who[0]) if moved else 'as the deck stands', '| goal', r['goal'], '| pin', r['pin'], 'floor', r['floor'])
        for name, a, off, on in r['rows']: print(f'    tap on {name}: someone there: {a}; switch off -> {off}; switch on -> {on}')
    print('errors', pg.errors[:2]); b.close()
