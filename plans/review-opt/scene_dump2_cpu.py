# OR2: scene_dump2 with --disable-accelerated-2d-canvas
# OR2: Deck 7 per lap: shot, every texture's canvas hash and version, every light
import sys, json
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0].replace("'--ignore-gpu-blocklist'", "'--ignore-gpu-blocklist', '--disable-accelerated-2d-canvas'"))
from playwright.sync_api import sync_playwright
DECKS = (3, 5, 2, 1, 6, 7, 4)
DUMP = r"""(() => { const out = [], seen = new Set(); const h = s => { let x = 0; for (let i = 0; i < s.length; i += 7) x = (x * 31 + s.charCodeAt(i)) | 0; return x; };
  scene.traverse(o => { if (o.isLight) out.push(['L', o.type, o.color.getHexString(), +o.intensity.toFixed(5), o.castShadow, o.id].join(' '));
    const ms = Array.isArray(o.material) ? o.material : o.material ? [o.material] : [];
    for (const m of ms) { for (const k of ['map', 'emissiveMap', 'alphaMap', 'lightMap']) { const t = m[k]; if (!t || seen.has(t)) continue; seen.add(t);
      let hs = ''; try { const im = t.image; if (im && im.toDataURL) hs = im.width + 'x' + im.height + ':' + h(im.toDataURL()); else if (im && im.data) hs = 'data' + im.data.length; } catch (e) { hs = 'err'; }
      out.push(['T', o.name, k, t.version, hs, t.id].join(' ')); }
      out.push(['M', o.id, m.id, m.version, m.needsUpdate, m.toneMapped, m.blending, m.depthWrite, m.side, m.alphaTest, m.fog].join(' ')); } });
  out.push('R ' + JSON.stringify([renderer.toneMappingExposure, renderer.shadowMap.enabled, renderer.shadowMap.needsUpdate, renderer.shadowMap.autoUpdate, scene.fog && scene.fog.color.getHexString()]));
  return out; })()"""
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.ev("window.__realTick = tickShip; tickShip = () => {}"); g.ev("setShipNow(18 * 60 + 15)")
    for lap in (1, 2, 3):
        for n in DECKS:
            g.ev(f"goToDeck({n}); updateDeckCrew(0.05)"); g.step(3)
            if n == 7: g.shot(f'{sys.argv[2]}_lap{lap}.png'); open(f'{sys.argv[2]}_lap{lap}.txt', 'w').write('\n'.join(g.ev(DUMP)))
    g.close()
