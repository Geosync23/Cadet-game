# OP1: where renderer.render's own JavaScript goes, with the unminified three.js r128 (same code, readable names).
#   python3 render_prof.py BUILD.html [SCENE_REGEX] [VIEW]
import sys, os, re, json, collections
pc = open('/home/user/Cadet-game/perf_check.py').read(); __file__ = '/home/user/Cadet-game/perf_check.py'
exec(pc.split("SCENE_JS = r")[0])
THREE = (WORK / 'three/package/build/three.js').read_text()     # Game routes three.min.js to this text
SCENE_JS = re.search(r'SCENE_JS = r"""(.*?)"""', pc, re.S)[1]
V = {'portrait': (390, 844, 1.5), 'wide': (390, 844, .7), 'land': (844, 390, 1.15)}
vw, vh, zoom = V[sys.argv[3] if len(sys.argv) > 3 else 'wide']
with sync_playwright() as pw:
    for sc in SCENES:
        if not re.search(sys.argv[2] if len(sys.argv) > 2 else 'Sunday dinner', sc['name']): continue
        g = Game(pw, sys.argv[1], vw, vh)
        g.page.evaluate(f"s => window.__sc(s)({json.dumps(sc)})", SCENE_JS)
        g.ev(f"camera.zoom = {zoom}; camera.updateProjectionMatrix()"); g.step(90)
        st = g.ev("""(() => { let objs = 0, meshes = 0, vis = 0, auto = 0, cast = 0, skinned = 0, inst = 0, bones = 0; scene.traverse(o => { objs++; if (o.matrixAutoUpdate) auto++; if (o.isBone) bones++; if (o.isMesh) { meshes++; if (o.visible) vis++; if (o.castShadow) cast++; if (o.isSkinnedMesh) skinned++; if (o.isInstancedMesh) inst++; } });
          return { objs, auto, bones, meshes, visibleMeshes: vis, castShadow: cast, skinned, instanced: inst, calls: renderer.info.render.calls }; })()""")
        print('==', sc['name'], st)
        cdp = g.page.context.new_cdp_session(g.page); cdp.send('Profiler.enable'); cdp.send('Profiler.setSamplingInterval', {'interval': 100})
        cdp.send('Profiler.start'); g.page.evaluate("() => { for (let k = 0; k < 200; k++) window.__step(1, 1000 / 30); }"); prof = cdp.send('Profiler.stop')['profile']
        nodes = {x['id']: x for x in prof['nodes']}; parent = {}
        for x in prof['nodes']:
            for c in x.get('children', []): parent[c] = x['id']
        dt = collections.Counter()
        for sid, d in zip(prof['samples'], prof['timeDeltas']): dt[sid] += d
        selfF = collections.Counter(); incl = collections.Counter()
        for nid, us in dt.items():
            cf = nodes[nid]['callFrame']
            if 'three' in cf['url'] or cf['url'] == '': selfF[(cf['functionName'] or '(anon)') + ('' if 'three' in cf['url'] else ' [native]')] += us
            seen = set(); x = nid
            while x in nodes:
                f = nodes[x]['callFrame']
                if 'three' in f['url'] and f['functionName'] not in seen: seen.add(f['functionName']); incl[f['functionName']] += us
                x = parent.get(x)
        N = 200
        print('  inclusive (three.js functions), ms a frame: ' + ', '.join(f'{k} {v/1e3/N:.2f}' for k, v in incl.most_common(26)))
        print('  self, ms a frame: ' + ', '.join(f'{k} {v/1e3/N:.3f}' for k, v in selfF.most_common(24)))
        g.close()
