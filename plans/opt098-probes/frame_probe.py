# OP1 (0.98 plan): a busy scene's frame, split three ways, with spread, on one quiet browser.
#   python3 frame_probe.py BUILD.html [SCENE_REGEX] [VIEW]     VIEW: portrait | wide | land | fold | foldturn | open
# For each matching perf_check scene: stand in the room, settle 90 frames, then
#   sim    game code only (drawing skipped), 15 batches of 30 frames: median and the 10th-90th percentile
#   drawn  40 drawn frames one at a time: game code, renderer.render's own JavaScript (three.js: culling, sorting,
#          uniforms, the GL calls), and the wait for the graphics process to finish (gl.readPixels of one pixel)
#   prof   a CPU profile of 300 drawn frames: self time by section and three.js by game caller
import sys, os, re, json, time, collections, subprocess, statistics as st
sys.path.insert(0, '/home/user/Cadet-game')
pc = open('/home/user/Cadet-game/perf_check.py').read()
__file__ = "/home/user/Cadet-game/perf_check.py"; exec(pc.split("SCENE_JS = r")[0])
SCENE_JS = re.search(r'SCENE_JS = r"""(.*?)"""', pc, re.S)[1]
GAME = sys.argv[1]; RX = sys.argv[2] if len(sys.argv) > 2 else 'Sunday dinner'
V = {'portrait': (390, 844, 1.5), 'wide': (390, 844, .7), 'land': (844, 390, 1.15), 'fold': (412, 960, 1.5), 'foldturn': (960, 412, 1.15), 'open': (792, 1080, 1.5)}
vw, vh, zoom = V[sys.argv[3] if len(sys.argv) > 3 else 'wide']
PROF = os.environ.get('PROF', '1') == '1'
sec = subprocess.run(['python3', '/home/user/Cadet-game/tools/section.py'], capture_output=True, text=True, cwd='/home/user/Cadet-game').stdout
SECS = [(int(m[2]), int(m[3]), m[1]) for m in (re.match(r'\s*(\S+)\s+(\d+)-(\d+)', l) for l in sec.splitlines()) if m]
def secOf(line):
    for a, b, n in SECS:
        if a <= line <= b: return n
    return '?'
SETUP = r"""(() => {
  const f = Object.getPrototypeOf(performance).now.bind(performance); window.__rn = f; window.__rt = 0;
  const rr = renderer.render.bind(renderer); renderer.render = (s, c) => { if (window.__skip) return; const a = f(); rr(s, c); window.__rt += f() - a; };
  const gl = renderer.getContext(); window.__px = new Uint8Array(4); window.__sync = () => gl.readPixels(0, 0, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, window.__px);
})()"""
SIM = r"""(n => { window.__skip = true; const a = window.__rn(); window.__step(n, 1000 / 30); window.__skip = false; return (window.__rn() - a) / n; })"""
DRAWN = r"""(n => { const out = []; for (let k = 0; k < n; k++) { window.__rt = 0; const a = window.__rn(); window.__step(1, 1000 / 30); const b = window.__rn(); window.__sync(); const c = window.__rn();
  out.push([b - a - window.__rt, window.__rt, c - b]); } return out; })"""
def q(xs, p): xs = sorted(xs); return xs[min(len(xs) - 1, int(p * len(xs)))]
def report(prof, n):
    nodes = {x['id']: x for x in prof['nodes']}; parent = {}
    for x in prof['nodes']:
        for c in x.get('children', []): parent[c] = x['id']
    dt = collections.Counter()
    for sid, d in zip(prof['samples'], prof['timeDeltas']): dt[sid] += d
    tot = sum(dt.values()); selfsec = collections.Counter(); fn = collections.Counter(); th = collections.Counter()
    for nid, us in dt.items():
        cf = nodes[nid]['callFrame']
        if '_run_' in cf['url']: s = secOf(cf['lineNumber'] + 1); selfsec[s] += us; fn[f"{cf['functionName'] or '(anon)'}@{cf['lineNumber']+1} [{s}]"] += us
        elif 'three' in cf['url']:
            selfsec['three.js'] += us; x = parent.get(nid); caller = '?'
            while x in nodes:
                f = nodes[x]['callFrame']
                if '_run_' in f['url']: caller = f"{f['functionName'] or '(anon)'}@{f['lineNumber']+1} [{secOf(f['lineNumber']+1)}]"; break
                x = parent.get(x)
            th[caller] += us
        else: selfsec[cf['functionName'] or '?'] += us
    print(f'  profile {n} drawn frames: {tot/1e3/n:.2f} ms a frame in all (profiler on)')
    print('  self by section: ' + ', '.join(f'{k} {v/1e3/n:.2f}' for k, v in selfsec.most_common(14)))
    print('  three.js self, by game caller: ' + ', '.join(f'{k} {v/1e3/n:.2f}' for k, v in th.most_common(6)))
    print('  top functions: ' + ', '.join(f'{k} {v/1e3/n:.3f}' for k, v in fn.most_common(14)))
with sync_playwright() as pw:
    for sc in SCENES:
        if not re.search(RX, sc['name']): continue
        g = Game(pw, GAME, vw, vh)
        r = g.page.evaluate(f"s => window.__sc(s)({json.dumps(sc)})", SCENE_JS)
        g.ev(f"camera.zoom = {zoom}; camera.updateProjectionMatrix()"); g.step(90); g.ev(SETUP)
        g.step(1)
        info = g.ev("({calls: renderer.info.render.calls, tris: renderer.info.render.triangles, people: crowd.stats().people, progs: renderer.info.programs.length, geo: renderer.info.memory.geometries, tex: renderer.info.memory.textures, stood: (r => r && ROOMS[r] ? ROOMS[r].name : null)(roomAt(...player.here()))})")
        sims = [g.page.evaluate(f"s => window.__sc(s)(30)", SIM) for _ in range(15)]
        drawn = g.page.evaluate(f"s => window.__sc(s)(40)", DRAWN)
        print(f"== {sc['name']} [{info['stood']}] {vw}x{vh} zoom {zoom}: {info['calls']} calls, {info['tris']/1e3:.0f}k tris, {info['people']} people, {info['progs']} programs, {info['geo']} geometries, {info['tex']} textures")
        print(f"  sim only: median {st.median(sims):.2f} ms a frame (10-90%: {q(sims,.1):.2f}-{q(sims,.9):.2f})")
        for i, nm in enumerate(['game code', 'render() JS', 'graphics wait']):
            xs = [d[i] for d in drawn]; print(f"  drawn, {nm}: median {st.median(xs):.2f} ms (10-90%: {q(xs,.1):.2f}-{q(xs,.9):.2f})")
        if PROF:
            cdp = g.page.context.new_cdp_session(g.page); cdp.send('Profiler.enable'); cdp.send('Profiler.setSamplingInterval', {'interval': 200})
            cdp.send('Profiler.start'); g.page.evaluate("() => { for (let k = 0; k < 300; k++) window.__step(1, 1000 / 30); }"); report(cdp.send('Profiler.stop')['profile'], 300)
        g.close()
