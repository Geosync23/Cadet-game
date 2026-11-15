# RV37's probes for FR2's playability fixes (claude/fable-review-play): cases frp_check.py does not cover.
# It prints what happens; the notes (plans/review-rv37.md) judge. Run it from a checkout of FR2's branch (it uses
# frp_check.py's and arrows_check.py's kit from the current folder):
#   python3 /path/to/rv37_frp_probe.py starship-cadet.html [pin food words]
import sys, os, json, re
RV_PARTS = [a for a in sys.argv[1:] if not a.endswith('.html')]; BUILD = next((a for a in sys.argv[1:] if a.endswith('.html')), 'starship-cadet.html')
sys.argv = [sys.argv[0], BUILD]
exec(open('frp_check.py').read().split('\ndef part_line')[0].replace('os.path.dirname(os.path.abspath(__file__))', 'os.getcwd()'))
TOASTS_RV = "(() => { window.__t = []; const t0 = toast; toast = function (a, b) { window.__t.push([a, Math.floor(shipNow())]); return t0.apply(this, arguments); }; window.__g = []; const g0 = needGoal; needGoal = function (k) { const r = g0.apply(this, arguments); if (r && k === 'hunger') window.__g.push(Math.floor(shipNow())); return r; }; })()"
def say(*a): print(*a, flush=True)

def part_food(ctx, src):
    # a player who never eats (Food held at 5, every other need at 90), nine days, awake 06:00 to 22:00, at the game's own pace
    for on in (False, True):
        pg = page(ctx, switched(src, 'FRP_FOOD_ON') if on else src, 'rvfood' + str(int(on)))
        jump(pg, 2, 6 * 60 + 1); pg.ev(TOASTS_RV)
        pin = "SHIP.player.needs.hunger = 5; for (const k of NEED_KEYS) if (k !== 'hunger') SHIP.player.needs[k] = 90;"
        for day in range(2, 11):
            pg.ev(f"devmodeRun('skip', () => devmodeSkipTo({(day - 1) * 1440 + 361}))"); pg.step(10)
            while pg.ev('shipNow()') < (day - 1) * 1440 + 22 * 60: pg.ev(pin); pg.step(200, 50)
        t = pg.ev('window.__t'); g = pg.ev('window.__g')
        hungry = [x[1] for x in t if x[0] == 'Very hungry']; perday = {}
        for m in hungry: perday[m // 1440 + 1] = perday.get(m // 1440 + 1, 0) + 1
        gday = {}
        for m in g: gday[m // 1440 + 1] = gday.get(m // 1440 + 1, 0) + 1
        say(f"food, switch {'on' if on else 'off'}: nine days never eating: 'Very hungry' said {len(hungry)} times, by day {perday}; at {[('%d %02d:%02d' % (m // 1440 + 1, m % 1440 // 60, m % 60)) for m in hungry][:24]}")
        say(f"   the Food marker set {len(g)} times, by day {gday}; all pop-ups by title: { {k: sum(1 for x in t if x[0] == k) for k in sorted(set(x[0] for x in t))} }; errors {pg.errors[:2]}")

GRID = r"""(() => {
  const rec = []; let cur = null;
  const tc = tapCrew, pt = playerTap, pg = playerGo;
  tapCrew = function (cx, cy, who) { const a = who || crewAtScreen(cx, cy); if (!a) return false; cur.push('person:' + a.p.id); return true; };
  playerTap = function (it) { cur.push('thing:' + (it && it.t)); return true; };
  playerGo = function () { cur.push('walk'); return true; };
  const out = { pts: 0, changed: 0, bodyChanged: 0, kinds: {}, sample: [] };
  const body = (a, x, y) => [.5, 1, 1.4].some(hy => { _cp.set(a.x, a.y + hy, a.z).project(camera); return Math.hypot((_cp.x + 1) / 2 * innerWidth - x, (1 - _cp.y) / 2 * innerHeight - y) < CREW_ON_PX; });
  try {
    for (let dx = -60; dx <= 60; dx += 10) for (let dy = -70; dy <= 70; dy += 10) {
      const x = IX_PIN.x + dx, y = IX_PIN.y + dy, a = crewAtScreen(x, y);
      const run = on => { FRP_PINTAP_ON = on; cur = []; IX_PIN.t = performance.now(); try { tap(x, y); } catch (e) { cur.push('error:' + String(e).slice(0, 60)); } return cur.join('+') || 'nothing'; };
      const off = run(false), onn = run(true); out.pts++;
      if (off !== onn) { out.changed++; const k = off + ' -> ' + onn; out.kinds[k] = (out.kinds[k] || 0) + 1;
        if (a && body(a, x, y) && Math.hypot(dx, dy) >= CREW_PIN_PX) { out.bodyChanged++; if (out.sample.length < 6) out.sample.push([dx, dy, k]); } }
    }
  } finally { tapCrew = tc; playerTap = pt; playerGo = pg; FRP_PINTAP_ON = true; }
  return out; })()"""
def part_pin(ctx, src):
    pg = page(ctx, switched(src, 'FRP_PINTAP_ON'), 'rvpin')
    jump(pg, 2, 18 * 60 + 12); pg.ev("goToDeck(3); for (const k of NEED_KEYS) SHIP.player.needs[k] = 90; needGoalClear(); clearGoal(); SHIP.player.track = null"); pg.step(60)
    say('pin: the mess at dinner, people on deck:', pg.ev('DECK_CREW.filter(a => a.h).length'))
    # goals to try: a seat with two people close by; a person with a neighbour; the room
    seat = pg.ev("(() => { let best = null; for (const pl of DECKS[3].places.filter(p => p.type === 'mess-seat')) { const c = cellPos(...pl.at); const n = DECK_CREW.filter(a => a.p && Math.hypot(a.x - c.x, a.z - c.z) < 1.6).length; if (!best || n > best[1]) best = [pl.id, n, c.x, c.z]; } return best; })()")
    person = pg.ev("(() => { let best = null; for (const a of DECK_CREW) { if (!a.p || !a.h) continue; const n = DECK_CREW.filter(b => b !== a && b.p && Math.hypot(a.x - b.x, a.z - b.z) < 1.4).length; if (!best || n > best[1]) best = [a.p.id, n, a.x, a.z]; } return best; })()")
    cases = [('a mess seat with %d people within 1.6' % seat[1], "{ deck: 3, place: %s, label: 'A test seat' }" % json.dumps(seat[0]), seat[2], seat[3]),
             ('a person (%s) with %d others within 1.4' % (person[0], person[1]), "{ deck: 3, crew: %s, label: 'A test person' }" % json.dumps(person[0]), person[2], person[3]),
             ('a room (the mess)', "{ deck: 3, room: placeRoom(%s), label: 'A test room' }" % json.dumps(seat[0]), seat[2], seat[3])]
    for name, goal, x, z in cases:
        pg.ev(f"(() => {{ clearGoal(); const gl = nearestOpen({x} + 2.5, {z} + 2.5, player); player.obj.position.copy(cellPos(...gl)); player.stop(); setGoal({goal}); }})()")
        pg.ev('window.__draw = true'); pg.step(12, 30); pg.ev('window.__draw = false')
        if pg.ev('performance.now() - IX_PIN.t >= 500'): say(f'pin, {name}: the pin is not on screen; skipped'); continue
        r = pg.ev(GRID)
        say(f"pin, {name}: {r['pts']} taps on a 10 px grid around the pin: {r['changed']} go somewhere else with the switch on; of those, on a person's own body and 22 px or more from the pin's point: {r['bodyChanged']} {r['sample']}")
        for k, n in sorted(r['kinds'].items(), key=lambda kv: -kv[1])[:8]: say(f'      {n:3d} x  {k}')
    say('   errors', pg.errors[:2])

def part_words(ctx, src):
    pg = page(ctx, switched(src, 'FRP_WORDS_ON', 'FRP_THANKS_ON', 'FRP_SAY_ON'), 'rvwords'); jump(pg, 2, 10 * 60)
    names = pg.ev("(() => { const out = {}; for (const m of machinesAll ? machinesAll() : []) { const n = machineName(m); out[n.replace(/\\s+\\d+$/, '')] = frpPlural(n); } return out; })()") if pg.ev("typeof machinesAll === 'function'") else pg.ev("(() => { const out = {}; for (const k in MACHINE_KINDS) { const n = String(MACHINE_KINDS[k].name || MACHINE_KINDS[k].label || k); out[n] = frpPlural(n); } return out; })()")
    say('words: machine names read as plural ("are running"):', sorted(k for k, v in names.items() if v))
    say('words: read as singular ("is running"):', sorted(k for k, v in names.items() if not v))
    th = pg.ev("SHIP_TRADITIONS.map(ev => [ev.id, frpThanksOk({ ev })])")
    say('thanks: still thanked by Mail:', sorted(i for i, v in th if v)); say('thanks: no Mail any more:', sorted(i for i, v in th if not v))
    cal = pg.ev("(() => { const out = new Set(); for (const k in CHORES) { try { for (const j of CHORES[k].where()) if (/^Calibrate/.test(j.title)) out.add(j.title); } catch (e) {} } return [...out]; })()")
    say('words: Calibrate jobs:', sorted(cal)[:30]); say('   errors', pg.errors[:2])

ALLP = [('pin', part_pin), ('words', part_words), ('food', part_food)]
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844})
    src = pathlib.Path(BUILD).read_text()
    for name, f in ALLP:
        if RV_PARTS and name not in RV_PARTS: continue
        say('--', name)
        try: f(ctx, src)
        except Exception as e: say('PROBE PART STOPPED', name, str(e)[:500])
    b.close()
