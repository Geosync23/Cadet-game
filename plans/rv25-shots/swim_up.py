# RV25: backlog FX8-1 on BB1's build: a swimmer or climber getting up from a rec deck place with its own moves glides from
# where the body is drawn to the walk-to tile. Follows the first few who get up on deck 7 (Day 2 from 06:00 and Day 6 from
# 14:00), frame by frame: the drawn spot (x + hx), the biggest move in one frame, and whether the drawn spot crosses a tile
# nobody can stand on (a wall; water is a place's own). Usage: swim_up.py BUILD.html OUTDIR
import sys, os, json
G = os.path.abspath(sys.argv[1]); OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
exec(open(os.path.join(os.path.dirname(G), 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
W = """(() => DECK_CREW.filter(a => a.p && a.settled && a.spot && a.spot.mv).map(a => a.p.id + ':' + a.spot.id + ':' + a.spot.mv.kind))()"""
F = """(ids => { const out = {}; for (const a of DECK_CREW) if (a.p && ids.includes(a.p.id)) { const dx = a.x + (a.hx || 0), dz = a.z + (a.hz || 0); let wall = false; try { const c = cellAt(dx, dz); wall = !free(...c) && !(ROOMS[roomAt(...c)] || {}).name; } catch (e) {}
  out[a.p.id] = [+dx.toFixed(3), +dz.toFixed(3), a.settled ? 1 : 0, a.spot && a.spot.mv ? 1 : 0, wall ? 1 : 0, a.rdx != null ? 1 : 0, +(a.hx || 0).toFixed(2), +(a.hz || 0).toFixed(2), (ROOMS[roomAt(...cellAt(dx, dz))] || {}).name || roomAt(...cellAt(dx, dz))]; } return out; })"""
with sync_playwright() as pw:
    g = Game(pw, G); g.page.set_viewport_size({'width': 390, 'height': 844})
    for when in ((5 * 1440 + 14 * 60, 'd6'), (5 * 1440 + 16 * 60, 'd6b'), (6 * 1440 + 10 * 60, 'd7')):
        g.ev(f"skipTo({when[0]}); goToDeck(7)"); g.step(30)
        movers = g.ev(W); print(when[1], 'on places with moves:', movers); ids = [m.split(':')[0] for m in movers]
        if not ids: continue
        prev = g.ev(f"({F})({json.dumps(ids)})"); seen = {}; frames = 0
        while frames < 3600 and len([k for k in seen if seen[k]['done']]) < 3:
            g.step(1, 1000 / 30); frames += 1
            cur = g.ev(f"({F})({json.dumps(ids)})")
            for k, v in cur.items():
                p = prev.get(k)
                if p and p[2] == 1 and p[3] == 1 and v[2] == 0 and k not in seen:
                    seen[k] = {'from': p, 'max': 0, 'walls': [], 'n': 0, 'done': False, 'path': []}; print('  up:', k, 'from', p, 'frame', frames, flush=True)
                    pass
                if k in seen and not seen[k]['done']:
                    S = seen[k]; step = ((v[0] - p[0]) ** 2 + (v[1] - p[1]) ** 2) ** .5 if p else 0; S['max'] = max(S['max'], step); S['n'] += 1
                    if v[4]: S['walls'].append(v[8])
                    pass
                    if S['n'] % 10 == 0: S['path'].append(v[:2] + [v[8]])
                    if abs(v[6]) < .02 and abs(v[7]) < .02 and S['n'] > 3 or S['n'] > 240: S['done'] = True; print('  done:', k, 'frames', S['n'], 'biggest step', round(S['max'], 3), 'over walls', sorted(set(S['walls'])), 'path', S['path'], flush=True)
            prev = cur
        print(when[1], 'frames watched', frames)
    print('errors', g.errors if hasattr(g, 'errors') else None); g.close()
