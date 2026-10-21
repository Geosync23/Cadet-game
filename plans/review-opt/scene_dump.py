# OR2: the scene on Deck 7 after keep_shots' three laps, every object's state, old vs new
import sys, json
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0])
from playwright.sync_api import sync_playwright
DECKS = (3, 5, 2, 1, 6, 7, 4)
DUMP = r"""(() => { const out = []; scene.updateMatrixWorld(true); scene.traverse(o => {
  const m = o.material, mm = Array.isArray(m) ? m[0] : m;
  let u = ''; if (mm && mm.uniforms) u = Object.entries(mm.uniforms).map(([k, v]) => k + '=' + JSON.stringify(v.value && v.value.toArray ? v.value.toArray().map(x => +x.toFixed(4)) : (typeof v.value === 'number' ? +v.value.toFixed(5) : (v.value && v.value.isTexture ? 'tex' : v.value)))).join(';');
  out.push([o.type, o.name, o.visible, o.renderOrder, o.matrixWorld.elements.map(x => +x.toFixed(4)).join(','), mm ? [mm.type, mm.color && mm.color.getHexString(), mm.emissive && mm.emissive.getHexString(), mm.emissiveIntensity, +(mm.opacity||0).toFixed(4), mm.transparent, u].join('|') : '', o.isInstancedMesh ? o.count : '', o.geometry ? (o.geometry.attributes.position || {}).count : '', o.id].join(' ')); }); return out; })()"""
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.ev("window.__realTick = tickShip; tickShip = () => {}"); g.ev("setShipNow(18 * 60 + 15)")
    for lap in (1, 2, 3):
        for n in DECKS:
            g.ev(f"goToDeck({n}); updateDeckCrew(0.05)"); g.step(3)
            if lap == 3 and n == 7: open(sys.argv[2], 'w').write('\n'.join(g.ev(DUMP)))
    g.close()
