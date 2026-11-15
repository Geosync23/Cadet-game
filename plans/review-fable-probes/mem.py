import sys; sys.path.insert(0, '' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + ''); from g import *
JS = r"""(() => { const bufs = new Set(), geos = new Set(), texs = new Set(), mats = new Set(); let meshes = 0, objs = 0, vis = 0, tris = 0, inst = 0, skinned = 0;
  scene.traverse(o => { objs++; if (o.visible) vis++; if (o.geometry) { meshes++; geos.add(o.geometry); if (o.isInstancedMesh) inst++; if (o.isSkinnedMesh) skinned++; const ms = Array.isArray(o.material) ? o.material : [o.material]; for (const m of ms) if (m) { mats.add(m); for (const k of ['map', 'emissiveMap', 'normalMap', 'roughnessMap', 'alphaMap']) if (m[k]) texs.add(m[k]); } } });
  let gb = 0, verts = 0, idx = 0; for (const g of geos) { for (const k in g.attributes) { const a = g.attributes[k], arr = a.array || (a.data && a.data.array); if (arr && !bufs.has(arr.buffer)) { bufs.add(arr.buffer); gb += arr.buffer.byteLength; } } if (g.index && !bufs.has(g.index.array.buffer)) { bufs.add(g.index.array.buffer); gb += g.index.array.buffer.byteLength; } if (g.attributes.position) verts += g.attributes.position.count; idx += g.index ? g.index.count : 0; }
  let tb = 0; const sizes = {}; for (const t of texs) { const im = t.image; if (im && im.width) { tb += im.width * im.height * 4; const k = im.width + 'x' + im.height; sizes[k] = (sizes[k] || 0) + 1; } }
  const cv = document.querySelectorAll('canvas').length;
  return { deck: deckDef.num, objs, vis, meshes, inst, skinned, geos: geos.size, mats: mats.size, texs: texs.size, geoMB: +(gb / 1e6).toFixed(1), verts, texMB_cpu: +(tb / 1e6).toFixed(1), texSizes: sizes, info: renderer.info.memory, programs: renderer.info.programs.length, calls: renderer.info.render.calls, tris: renderer.info.render.triangles, shadowMap: sun.shadow.mapSize.x, dom: document.querySelectorAll('*').length }; })()"""
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1]); g.ev("skipTo(1440 + 600)")
    for d in [4, 1, 2, 3, 5, 6, 7, 4]:
        g.ev(f"if (deckDef.num !== {d}) goToDeck({d})"); g.step(60); g.step(1, draw=True)
        r = g.ev(JS); r['heapMB'] = round(g.heap() / 1e6); r['backing'] = round(g.cdp.send('Runtime.getHeapUsage')['backingStorageSize'] / 1e6); print(json.dumps(r))
    g.close()
