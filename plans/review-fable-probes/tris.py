import sys; sys.path.insert(0, '' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + ''); from g import *
JS = r"""(() => { const rows = []; let tot = 0, hid = 0, hidTri = 0, shadowTri = 0;
  scene.traverse(o => { if (!o.geometry || !o.geometry.attributes.position) return; const g = o.geometry; let t = (g.index ? g.index.count : g.attributes.position.count) / 3; if (o.isInstancedMesh) t *= o.count;
    let vis = true; for (let p = o; p; p = p.parent) if (!p.visible) vis = false;
    if (!vis) { hid++; hidTri += t; return; } tot += t; if (o.castShadow) shadowTri += t;
    const wp = new THREE.Vector3(); o.getWorldPosition(wp); let room = null; try { const c = [Math.floor(wp.x + OX), Math.floor(wp.z + OZ)]; const r = roomAt(...c); room = r && ROOMS[r] ? ROOMS[r].name : null; } catch (e) {}
    rows.push({ t: Math.round(t), name: o.name || '', ud: Object.keys(o.userData || {}).join(','), kind: o.isInstancedMesh ? 'inst x' + o.count : o.isSkinnedMesh ? 'skinned' : o.type, mat: Array.isArray(o.material) ? 'multi' : (o.material.type || '').replace('Mesh', '').replace('Material', ''), room, sh: o.castShadow, par: o.parent && o.parent.name || '' }); });
  rows.sort((a, b) => b.t - a.t); const n = rows.length; let acc = 0, k50 = 0; for (const r of rows) { acc += r.t; k50++; if (acc > tot / 2) break; }
  const hist = {}; for (const r of rows) { const b = r.t >= 5000 ? '5000+' : r.t >= 1000 ? '1000-5000' : r.t >= 200 ? '200-1000' : '<200'; hist[b] = hist[b] || [0, 0]; hist[b][0]++; hist[b][1] += r.t; }
  return { deck: deckDef.num, visibleMeshes: n, tris: Math.round(tot), shadowCasterTris: Math.round(shadowTri), hiddenMeshes: hid, hiddenTris: Math.round(hidTri), meshesForHalf: k50, hist, top: rows.slice(0, 22) }; })()"""
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1]); g.ev("skipTo(1440 + 760)")
    for d in [3, 4, 2]:
        g.ev(f"if (deckDef.num !== {d}) goToDeck({d})"); g.step(60); g.step(1, draw=True); r = g.ev(JS); top = r.pop('top'); print(json.dumps(r)); [print('   ', json.dumps(x)) for x in top]
    g.close()
