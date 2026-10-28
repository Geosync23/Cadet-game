# perf_check's scenes: which room you actually stand in, and draw calls / game code, as now and with the tile->world fix
import sys, os, re, json
pc = open('/home/user/Cadet-game/perf_check.py').read()
exec(pc.split("def mem(g)")[0].split("import sys, os, json, re, time")[1].replace("exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cadet_test.py')).read().split(\"a, shots = run(\")[0])", "exec(open('/home/user/Cadet-game/cadet_test.py').read().split('a, shots = run(')[0])"))
FIXED = SCENE_JS.replace("at = nearestOpen(Math.floor((b.i0 + b.i1) / 2), Math.floor((b.j0 + b.j1) / 2), player)", "c0 = cellPos(Math.floor((b.i0 + b.i1) / 2), Math.floor((b.j0 + b.j1) / 2)), at = nearestOpen(c0.x, c0.z, player)")
assert FIXED != SCENE_JS
with sync_playwright() as pw:
    for sc in SCENES:
        out = []
        for tag, js in (('now', SCENE_JS), ('fixed', FIXED)):
            for vname, w, h, zoom in (VIEWS[0], VIEWS[1]):
                g = Game(pw, sys.argv[1], w, h)
                g.page.evaluate("window.__realNow = (() => { const f = Object.getPrototypeOf(performance).now.bind(performance); return () => f(); })()")
                g.ev(GL_JS); g.page.evaluate(f"s => window.__sc(s)({json.dumps(sc)})", js)
                g.ev(f"camera.zoom = {zoom}; camera.updateProjectionMatrix()"); g.step(90)
                r = g.page.evaluate("s => window.__sc(s)(20)", MEASURE_JS)
                room = g.ev("(r => r ? ROOMS[r].name : '?')(roomAt(...player.here()))")
                out.append(f"{tag} {vname}: in [{room}] {r['calls']}c {r['js']}ms {r['crew']}p")
                g.close()
        print(sc['name'], '|', ' ; '.join(out), flush=True)
