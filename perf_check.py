#!/usr/bin/env python3
# perf_check.py (the performance engineer, Pillar 4): phone-speed watchdog for a combined build.
#
#   CADET_CHROME=/opt/pw-browsers/chromium python3 perf_check.py NEW.html [OLD.html]
#
# For each busy moment in SCENES it starts a fresh game (?nosave&debug), skips to that ship time, goes to the deck,
# stands you in the room, lets the crew settle, and measures on phone-sized views (portrait 390x844 at the usual zoom
# 1.5 and the widest 0.7; landscape 844x390 at 1.15):
#   calls   draw calls in the main pass (renderer.info, the budget's number; shadows aren't counted there)
#   tris    triangles drawn (thousands)
#   js      milliseconds of game code per frame (the best of 3 batches of 20 frames) (simulation, crew, crowd, effects; rendering skipped). Headless
#           SwiftShader can't say how fast a real phone renders, so this is the part we can compare build to build.
#   gl      every draw sent to the GPU in that frame, the shadow pass included (the budget's 'calls' counts the picture only)
#           (a mid phone runs game code roughly 4 to 5 times slower; Chrome's CPU throttle gave no steady numbers headless)
#   crew    people on the deck (the crowd's count)
# Then a week of play (7 ship days, 28 deck changes) and a deck round trip (every deck, twice) check geometries, textures and the JS heap come back to the same numbers.
# With OLD.html it runs both and marks regressions: over BUDGET calls, calls up more than 10% or 25, js up more than
# 30%, or memory that grows across round trips. Ends "PERF CHECK OK" or "PERF CHECK: N problem(s)".
# Add a scene when a new tradition or moment lands: name, day (1 = the Monday of a new game), time, deck, room (a
# regexp on the room's name), and optionally setup (JS run after the skip, e.g. to start an event).
import sys, os, json, re, time
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

BUDGET = 450
VIEWS = [('portrait', 390, 844, 1.5), ('portrait-wide', 390, 844, 0.7), ('landscape', 844, 390, 1.15)]
SCENES = [
    # the arrival evening (Pillar 4 Part 1; until it's built: the same places at the same times on a Sunday)
    {'name': 'arrival: shuttle bay 17:40', 'day': 7, 'time': '17:40', 'deck': 5, 'room': r'^Shuttle bay'},
    {'name': 'arrival: Works bay door 17:46', 'day': 7, 'time': '17:46', 'deck': 5, 'room': r'^Works bay$'},
    {'name': 'Sunday dinner, the mess 18:30', 'day': 7, 'time': '18:30', 'deck': 3, 'room': r'^Mess'},
    {'name': 'junior wing, Sunday 20:30', 'day': 7, 'time': '20:30', 'deck': 4, 'room': r'common room'},
    # traditions (Sowing morning is day 6 in the garden; until it's built, the harvest morning there)
    {'name': 'Sowing / harvest morning, garden 10:00', 'day': 6, 'time': '10:00', 'deck': 3, 'room': r'garden'},
    {'name': 'Tiles night, bow lounge Tue 20:30', 'day': 2, 'time': '20:30', 'deck': 3, 'room': r'^Bow lounge$'},
    {'name': 'quiz night, bow lounge 20:30', 'day': 4, 'time': '20:30', 'deck': 3, 'room': r'^Bow lounge$'},
    {'name': 'breakfast rush, the mess 07:10', 'day': 2, 'time': '07:10', 'deck': 3, 'room': r'^Mess'},
]

SCENE_JS = r"""(sc => {
  const [h, m] = sc.time.split(':').map(Number); skipTo((sc.day - 1) * 1440 + h * 60 + m);
  if (sc.setup) eval(sc.setup);
  if (deckDef.num !== sc.deck) goToDeck(sc.deck);
  const re = new RegExp(sc.room, 'i'), k = Object.keys(ROOM_BOX).find(k => ROOMS[k] && re.test(ROOMS[k].name));
  if (!k) return { room: null };
  const b = ROOM_BOX[k], at = nearestOpen(Math.floor((b.i0 + b.i1) / 2), Math.floor((b.j0 + b.j1) / 2), player);
  player.obj.position.copy(cellPos(...at)); target.copy(player.obj.position).setY(.7);
  return { room: ROOMS[k].name };
})"""
GL_JS = r"""(() => {                                   // counts every real draw sent to the GPU, the shadow pass included
  if (window.__glOn) return; window.__glOn = true; window.__gl = 0; const gl = renderer.getContext(), wrap = (o, f) => { const g = o[f] && o[f].bind(o); if (g) o[f] = (...a) => { window.__gl++; return g(...a); }; };
  for (const f of ['drawElements', 'drawArrays', 'drawElementsInstanced', 'drawArraysInstanced']) wrap(gl, f);
  const ext = gl.getExtension('ANGLE_instanced_arrays'); if (ext) for (const f of ['drawElementsInstancedANGLE', 'drawArraysInstancedANGLE']) wrap(ext, f);
})()"""
MEASURE_JS = r"""(n => {
  window.__gl = 0; window.__skip = false; window.__step(1, 1000 / 30);   // one drawn frame: draw calls, triangles, crew (before the timing, so the ship time is the same every run)
  const st = crowd.stats(), r = { calls: renderer.info.render.calls, gl: window.__gl, tris: Math.round(renderer.info.render.triangles / 1000), crew: st.people };
  window.__skip = true; let js = 1e9; for (let k = 0; k < 3; k++) { const a = window.__realNow(); window.__step(n, 1000 / 30); js = Math.min(js, (window.__realNow() - a) / n); } window.__skip = false;   // the best of 3 batches (less noise)
  r.js = +js.toFixed(2); return r;
})"""
MEM_JS = r"""(() => { const m = renderer.info.memory; return { geo: m.geometries, tex: m.textures, heap: performance.memory ? Math.round(performance.memory.usedJSHeapSize / 1048576) : null }; })()"""

def mem(g):                                              # memory after a full garbage collection, so garbage doesn't count
    g.page.context.new_cdp_session(g.page).send('HeapProfiler.collectGarbage'); return g.ev(MEM_JS)

def run(path):
    out = {'scenes': [], 'trip': None, 'errors': [], 'size': os.path.getsize(path), 'load': []}
    with sync_playwright() as pw:
        for k in range(3):                               # load time: a fresh page to playable (headless), 3 times
            t = time.time(); g = Game(pw, path, 390, 844, out['errors']); out['load'].append(round(time.time() - t, 1)); g.close()
        for sc in SCENES:
            row = {'name': sc['name'], 'views': {}}
            for vname, w, h, zoom in VIEWS:
                g = Game(pw, path, w, h, out['errors'])
                g.page.evaluate("window.__realNow = (() => { const f = Object.getPrototypeOf(performance).now.bind(performance); return () => f(); })()")
                g.ev(GL_JS)
                r = g.page.evaluate(f"s => window.__sc(s)({json.dumps(sc)})", SCENE_JS)
                row['room'] = r.get('room')
                g.ev(f"camera.zoom = {zoom}; camera.updateProjectionMatrix()")
                g.step(90)
                row['views'][vname] = g.page.evaluate("s => window.__sc(s)(20)", MEASURE_JS)
                g.close()
            out['scenes'].append(row)
        # the deck round trip: every deck twice, memory after each lap back on Deck 4
        g = Game(pw, path, 390, 844, out['errors'])
        laps = []
        for lap in range(3):
            for n in g.ev("Object.keys(DECKS).map(Number)") + [4]:
                g.ev(f"goToDeck({n})"); g.step(3)
            g.step(10); laps.append(mem(g))
        out['trip'] = laps
        g.close()
        # long play: a week of ship days, four deck changes a day, back on Deck 4 at the end; memory then vs after day 1
        g = Game(pw, path, 390, 844, out['errors'])
        for n in g.ev("Object.keys(DECKS).map(Number)") + [4]: g.ev(f"goToDeck({n})"); g.step(3)   # every deck once first: shared kit uploads once
        g.step(10); start = mem(g)
        for d in range(1, 8):
            for k, n in enumerate((3, 5, 2, 4)):
                g.ev(f"skipTo({d * 1440 + 420 + k * 180}); goToDeck({n})"); g.step(20)
        g.ev("goToDeck(4)"); g.step(10); out['long'] = [start, mem(g)]
        g.close()
    return out

def show(tag, o):
    print(f'== {tag}')
    for s in o['scenes']:
        v = '  '.join(f"{k} {x['calls']}c/{x.get('gl', '?')}gl {x['tris']}kt {x['js']}ms {x['crew']}p" for k, x in s['views'].items())
        print(f"  {s['name']:<42} [{s.get('room')}]  {v}")
    print(f"  file {o['size'] / 1e6:.2f} MB, load {o['load']} s")
    if o.get('long'): print('  a week of play (geometries, textures, JS heap MB): after day 1', '/'.join(str(v) for v in o['long'][0].values()), '-> after day 8', '/'.join(str(v) for v in o['long'][1].values()))
    print('  deck round trips (geometries, textures, JS heap MB):', ' -> '.join(f"{m['geo']}/{m['tex']}/{m['heap']}" for m in o['trip']))

def problems(new, old):
    bad = []
    for i, s in enumerate(new['scenes']):
        if not s.get('room'): bad.append(f"{s['name']}: room not found")
        for k, x in s['views'].items():
            if x['calls'] > BUDGET: bad.append(f"{s['name']} {k}: {x['calls']} draw calls (budget {BUDGET})")
            if old:
                y = old['scenes'][i]['views'][k]
                if x['calls'] > y['calls'] * 1.1 and x['calls'] > y['calls'] + 25: bad.append(f"{s['name']} {k}: draw calls {y['calls']} -> {x['calls']}")
                if x['js'] > y['js'] * 1.3 and x['js'] > y['js'] + 1: bad.append(f"{s['name']} {k}: js {y['js']} -> {x['js']} ms a frame")
    if old and new['size'] > old['size'] * 1.25: print(f"NOTE file size {old['size'] / 1e6:.2f} -> {new['size'] / 1e6:.2f} MB (more to download on a phone; not a failure)")
    t = new['trip']
    if t[-1]['geo'] != t[1]['geo'] or t[-1]['tex'] != t[1]['tex']: bad.append(f"memory grows across deck round trips: {t}")
    L = new.get('long')
    if L and (L[1]['geo'] > L[0]['geo'] + 20 or L[1]['tex'] > L[0]['tex'] + 2 or (L[1]['heap'] or 0) > (L[0]['heap'] or 0) + 60): bad.append(f"memory grows over a week of play: {L}")
    if new['errors']: bad.append(f"errors: {new['errors'][:4]}")
    return bad

if __name__ == '__main__':
    new = run(sys.argv[1]); old = run(sys.argv[2]) if len(sys.argv) > 2 else None
    if old: show('OLD ' + sys.argv[2], old)
    show('NEW ' + sys.argv[1], new)
    json.dump({'new': new, 'old': old}, open('perf_check.json', 'w'), indent=1)
    bad = problems(new, old)
    for b in bad: print('PROBLEM', b)
    print('PERF CHECK OK' if not bad else f'PERF CHECK: {len(bad)} problem(s)')
    sys.exit(1 if bad else 0)   # so a failing check fails for the computer too (split rehearsal SX1; SR2 N1)
