import sys, json
src = open('perf_check.py').read()
exec(src.split("def run(path)")[0])
with sync_playwright() as pw:
    for path in sys.argv[1:]:
        rows = []
        for rep in range(2):
            g = Game(pw, path, 844, 390, [])
            g.page.evaluate("window.__realNow = (() => { const f = Object.getPrototypeOf(performance).now.bind(performance); return () => f(); })()")
            g.page.evaluate(f"s => window.__sc(s)({json.dumps(SCENES[2])})", SCENE_JS)
            g.ev("camera.zoom = 1.15; camera.updateProjectionMatrix()"); g.step(90)
            r = g.page.evaluate("s => window.__sc(s)(20)", MEASURE_JS)
            rows.append([r['calls'], r['js'], mem(g)['heap'], g.ev("crowd.stats().people")])
            g.close()
        print(path, '[calls, js ms, heap MB, crew] x2:', rows, flush=True)
