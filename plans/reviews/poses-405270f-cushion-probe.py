import sys, json
exec(open('cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
# 0.27.40's seatCushion: how many rays, how long they take, and whether the same seated people cast again and again
# (their cache is keyed on pos x/z and face). Sunday dinner in the mess and the bow lounge at 20:30.
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1]); ev = g.ev
    ev("""(() => { const S = SEAT_RC, f = S.rc.intersectObjects.bind(S.rc); window.__rc = { n: 0, ms: 0, max: 0, who: new Map() };
      S.rc.intersectObjects = (l, r) => { const a = window.__realNow ? window.__realNow() : performance.now(); const out = f(l, r);
        const t = (window.__realNow ? window.__realNow() : performance.now()) - a; __rc.n++; __rc.ms += t; __rc.max = Math.max(__rc.max, t); return out; }; })()""")
    for name, day, tm, deck, room in [('Sunday dinner 18:30', 7, 18 * 60 + 30, 3, '^Mess'), ('bow lounge Tue 20:30', 2, 20 * 60 + 30, 3, '^Bow lounge$')]:
        ev(f"""(() => {{ skipTo({(day - 1) * 1440 + tm}); if (deckDef.num !== {deck}) goToDeck({deck});
          const re = new RegExp('{room}', 'i'), k = Object.keys(ROOM_BOX).find(k => ROOMS[k] && re.test(ROOMS[k].name)), b = ROOM_BOX[k];
          player.obj.position.copy(cellPos(...nearestOpen(Math.floor((b.i0 + b.i1) / 2), Math.floor((b.j0 + b.j1) / 2), player))); target.copy(player.obj.position).setY(.7);
          Object.assign(__rc, {{ n: 0, ms: 0, max: 0 }}); }})()""")
        res = []
        for k in range(6):
            g.step(60)
            res.append(json.loads(ev("JSON.stringify([__rc.n, +__rc.ms.toFixed(1), +__rc.max.toFixed(2), SEAT_RC.list.length, crowd.stats().people])")))
            ev("Object.assign(__rc, { n: 0, ms: 0, max: 0 })")
        print(name, '[rays, ms, worst ms, meshes listed, crew] per 60 frames:', res)
    for e in g.errors: print('page error', e)
    g.close()
