# OP1: what the draws are, in a busy scene: the picture's render list and the shadow pass, by the game's own groups.
#   python3 draw_mix.py BUILD.html [SCENE_REGEX] [VIEW]
import sys, os, re, json
pc = open('/home/user/Cadet-game/perf_check.py').read(); __file__ = '/home/user/Cadet-game/perf_check.py'
exec(pc.split("SCENE_JS = r")[0])
SCENE_JS = re.search(r'SCENE_JS = r"""(.*?)"""', pc, re.S)[1]
V = {'portrait': (390, 844, 1.5), 'wide': (390, 844, .7), 'land': (844, 390, 1.15), 'fold': (412, 960, 1.5)}
vw, vh, zoom = V[sys.argv[3] if len(sys.argv) > 3 else 'wide']
J = r"""(() => {
  const tag = new Map(), mark = (o, t) => o && o.traverse && o.traverse(x => { if (!tag.has(x)) tag.set(x, t); });
  for (const c of crowd.chunks) tag.set(c.mesh, 'crowd chunk (skinned)');
  for (const w of walkers) if (w.obj) mark(w.obj, w.isPlayer ? 'you' : 'walker (own rig)');
  mark(staticRoot, 'static furniture (merged)'); for (const t of TALL) mark(t.g, 'tall furniture');
  for (const d of WALL_DECOR) mark(d.g, 'wall decor'); for (const h of HULL_RUNS) { mark(h.g, 'hull'); mark(h.decor, 'hull decor'); }
  for (const d of DOOR_OBJS) mark(d.g, 'doors'); for (const c of CURVES) mark(c.g, 'curved walls'); for (const v of VOID_BLOCKS) mark(v.m, 'void blocks');
  for (const p of SHADOW_PROXY) tag.set(p.mesh, 'shadow stand-in');
  const why = o => { if (tag.has(o)) return tag.get(o); if (o.userData && o.userData.walker) return o.userData.walker.isPlayer ? 'you' : 'walker'; if (o.isInstancedMesh) return 'instanced (' + (o.name || o.geometry.type) + ')'; let p = o; while (p && !tag.has(p)) p = p.parent; return p ? tag.get(p) : (o.parent === scene ? 'scene: ' + (o.name || o.type) : 'deck other: ' + (o.parent && o.parent.name || '') + '/' + (o.material && o.material.type)); };
  const main = {}, shad = {}; let inShadow = false;
  const sm = renderer.shadowMap, sr = sm.render; sm.render = (...a) => { inShadow = true; try { return sr.apply(sm, a); } finally { inShadow = false; } };
  const rbd = renderer.renderBufferDirect.bind(renderer);
  renderer.renderBufferDirect = (cam, sc, geo, mat, obj, grp) => { const m = inShadow ? shad : main, k = why(obj); if (k.startsWith('deck other') && !inShadow) { let p = obj, ch = []; while (p && p !== deckRoot && p !== scene) { ch.push((p.name || p.type) + (p.userData && Object.keys(p.userData).length ? '{' + Object.keys(p.userData).slice(0, 3).join(',') + '}' : '')); p = p.parent; } const key = ch.reverse().join('>') + ' | ' + geo.type + ' v' + (geo.attributes.position ? geo.attributes.position.count : 0) + (Array.isArray(obj.material) ? ' groups' + geo.groups.length : ''); window.__oth.set(key, (window.__oth.get(key) || 0) + 1); } m[k] = (m[k] || 0) + 1; return rbd(cam, sc, geo, mat, obj, grp); };
  const oth = new Map(); const rbd0 = rbd;
  window.__oth = oth;
  window.__step(1, 33); sm.render = sr; renderer.renderBufferDirect = rbd;
  const srt = o => Object.entries(o).sort((a, b) => b[1] - a[1]);
  return { other: [...window.__oth.entries()].sort((a, b) => b[1] - a[1]).slice(0, 40), main: srt(main), shadow: srt(shad), calls: renderer.info.render.calls };
})()"""
with sync_playwright() as pw:
    for sc in SCENES:
        if not re.search(sys.argv[2] if len(sys.argv) > 2 else 'Sunday dinner', sc['name']): continue
        g = Game(pw, sys.argv[1], vw, vh)
        g.page.evaluate(f"s => window.__sc(s)({json.dumps(sc)})", SCENE_JS)
        g.ev(f"camera.zoom = {zoom}; camera.updateProjectionMatrix()"); g.step(90)
        r = g.ev(J)
        print(f"== {sc['name']} {vw}x{vh} {zoom}: calls {r['calls']}; picture {sum(v for _, v in r['main'])}, shadow pass {sum(v for _, v in r['shadow'])}")
        print('  picture:', ', '.join(f'{k} {v}' for k, v in r['main']))
        print('  shadow: ', ', '.join(f'{k} {v}' for k, v in r['shadow']))
        print('  other:', '\n    '.join(f'{v} x {k}' for k, v in r['other']))
        g.close()
