import sys, os, json, time, re
sys.argv=[sys.argv[0]]+sys.argv[1:]
_src=open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0]
_src=_src.replace("__file__", "'/home/user/Cadet-game/cadet_test.py'")
exec(_src)
os.environ.setdefault('CADET_CHROME','/opt/pw-browsers/chromium')
NAMES=json.load(open('/tmp/pf/names.json'))
REALNOW="window.__realNow = (() => { const f = Object.getPrototypeOf(performance).now.bind(performance); return () => f(); })()"
SIZES_JS=r"""(names => { const out = {};
  for (const n of names) { let v; try { v = eval(n); } catch (e) { continue; }
    if (v === null || typeof v !== 'object') continue;
    let c = null, j = null;
    if (Array.isArray(v)) c = v.length; else if (v instanceof Map || v instanceof Set) c = v.size; else if (v.isObject3D || v.isMaterial || v.isBufferGeometry) continue; else { try { c = Object.keys(v).length; } catch (e) {} }
    try { const s = JSON.stringify(v instanceof Map ? [...v] : v instanceof Set ? [...v] : v); j = s ? s.length : 0; } catch (e) { j = -1; }
    out[n] = [c, j];
  } return out; })"""
SHIPSIZE_JS=r"""(() => { const o = {}; for (const k in SHIP) { try { const s = JSON.stringify(SHIP[k], (kk, v) => v instanceof Set ? [...v] : v instanceof Map ? [...v] : v); o[k] = s ? s.length : 0; } catch (e) { o[k] = -1; } } return o; })()"""
SAVE_JS=r"""(() => {   // saveGame's own body, without its NOSAVE guard: the save string and how long making it takes
  const a = window.__realNow();
  const decks = {};
  for (const n in SHIP.decks) if (SHIP.decks[n].open.size) decks[n] = { open: [...SHIP.decks[n].open] };
  const save = { v: SAVE_V, build: GAME_BUILD, time: { day: SHIP.time.day, min: SHIP.time.min },
    player: { deck: player.deck, tile: player.here(), facing: player.face }, ship: { decks }, crew: {}, flags: SHIP.flags || {}, notes: SHIP.notes || [] };
  if (typeof crewState === 'function') save.crew = crewState(SHIP.time.day);
  const b = window.__realNow(); for (const f of SAVE_EXTRA) f(save); const c = window.__realNow();
  const s = JSON.stringify(save); const d = window.__realNow();
  const parts = {}; for (const k in save) parts[k] = JSON.stringify(save[k]).length;
  window.__lastSave = s;
  return { len: s.length, msBase: +(b - a).toFixed(2), msExtra: +(c - b).toFixed(2), msJson: +(d - c).toFixed(2), parts };
})()"""
STATS_JS=r"""(() => { let objs = 0; scene.traverse(() => objs++); const m = renderer.info.memory;
  return { objs, geo: m.geometries, tex: m.textures, dom: document.getElementsByTagName('*').length, timers: SIM_TIMERS.length,
    heap: performance.memory ? Math.round(performance.memory.usedJSHeapSize / 1048576 * 10) / 10 : null, crew: crowd.stats().people,
    day: SHIP.time.day, min: Math.round(SHIP.time.min), deck: deckDef.num, simOn: SIM_ON ? [...SIM_ON.values()].reduce((a, l) => a + l.length, 0) : 0, walkers: walkers.length,
    progs: renderer.info.programs ? renderer.info.programs.length : null };
})()"""
MEASURE_JS = r"""(n => {
  window.__skip = false; window.__step(1, 1000 / 30);
  const r = { calls: renderer.info.render.calls, tris: Math.round(renderer.info.render.triangles / 1000) };
  window.__skip = true; let js = 1e9, all = [];
  for (let k = 0; k < 3; k++) { const a = window.__realNow(); window.__step(n, 1000 / 30); const v = (window.__realNow() - a) / n; all.push(+v.toFixed(2)); js = Math.min(js, v); }
  window.__skip = false; r.js = +js.toFixed(2); r.jsAll = all; return r;
})"""
def gc(g):
    c=g.page.context.new_cdp_session(g.page); c.send('HeapProfiler.collectGarbage'); u=c.send('Runtime.getHeapUsage'); c.detach(); g.heapMB=round(u['usedSize']/1048576,1); return g.heapMB
HOOKS = r"""
(() => { const L = window.__L = { add: 0, rem: 0, live: new Map(), to: 0, toLive: 0, iv: 0, raf: 0 };
  const A = EventTarget.prototype.addEventListener, Rm = EventTarget.prototype.removeEventListener;
  EventTarget.prototype.addEventListener = function (t, f, o) { L.add++; const k = (this === window ? 'window' : this === document ? 'document' : (this.nodeName || this.constructor.name)) + ':' + t; L.live.set(k, (L.live.get(k) || 0) + 1); return A.call(this, t, f, o); };
  EventTarget.prototype.removeEventListener = function (t, f, o) { L.rem++; const k = (this === window ? 'window' : this === document ? 'document' : (this.nodeName || this.constructor.name)) + ':' + t; L.live.set(k, (L.live.get(k) || 0) - 1); return Rm.call(this, t, f, o); };
  const st = window.setTimeout, ct = window.clearTimeout, live = new Set();
  window.setTimeout = function (f, ms, ...a) { L.to++; const id = st.call(window, (...b) => { live.delete(id); if (typeof f === 'function') f(...b); }, ms, ...a); live.add(id); return id; };
  window.clearTimeout = function (id) { live.delete(id); return ct.call(window, id); };
  const si = window.setInterval; window.setInterval = function (...a) { L.iv++; return si.apply(window, a); };
  L.liveTO = () => live.size;
})();
"""
INIT = INIT + HOOKS
LIS_JS = "(() => { const L = window.__L; const top = [...L.live].filter(x => x[1] > 0).sort((a, b) => b[1] - a[1]).slice(0, 12); return { add: L.add, rem: L.rem, liveTO: L.liveTO(), to: L.to, iv: L.iv, top }; })()"
def heapsnap(g, path):
    """take a heap snapshot after GC, return {constructor/type name: [count, self bytes]}"""
    c=g.page.context.new_cdp_session(g.page); chunks=[]
    c.on('HeapProfiler.addHeapSnapshotChunk', lambda e: chunks.append(e['chunk']))
    c.send('HeapProfiler.collectGarbage'); c.send('HeapProfiler.takeHeapSnapshot', {'reportProgress': False}); c.detach()
    s=json.loads(''.join(chunks)); chunks=None
    m=s['snapshot']['meta']; nf=m['node_fields']; N=len(nf); types=m['node_types'][0]
    it,iname,iself=nf.index('type'),nf.index('name'),nf.index('self_size'); strs=s['strings']; nodes=s['nodes']; agg={}
    for i in range(0,len(nodes),N):
        t=types[nodes[i+it]]; nm=strs[nodes[i+iname]] if t in ('object','closure','native','hidden') else '('+t+')'
        if t=='closure': nm='closure '+nm
        if len(nm)>60: nm=nm[:60]
        a=agg.setdefault(nm,[0,0]); a[0]+=1; a[1]+=nodes[i+iself]
    json.dump(agg,open(path,'w')); return agg
_gs=_src.split('class Game:')[1].split('\nimport sys, json, hashlib')[0]
_gs='class GameQ:'+_gs.replace("device_scale_factor=1","device_scale_factor=DSF").replace("'?nosave&debug')","'?nosave&debug' + EXTRA_Q)")
DSF=1; EXTRA_Q=''
exec(_gs)
