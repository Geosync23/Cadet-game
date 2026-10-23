# RV8 probe: on every deck, the places within 2 m (floor distance) of a lift door or lift panel: what a lift tap could now
# hand to jobSpotTap (FB1 191bee5). p_liftnear.py GAME CT_DIR
import sys, json
exec(open(sys.argv[2] + '/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 900, 760); g.step(3)
    decks = g.ev("(typeof DECKS !== 'undefined' ? Object.keys(DECKS) : [1,2,3,4,5,6,7]).map(Number).filter(n => n)")
    for d in decks:
        try: g.ev(f"goToDeck({d})"); g.step(3)
        except Exception as e: print('deck', d, 'skip', str(e)[:60]); continue
        r = g.ev("""(() => { const out = [], lifts = [], q = new THREE.Vector3();
          scene.traverse(o => { const u = o.userData || {}; if (u.liftDoor || (u.item && u.item.lift)) { o.getWorldPosition(q); lifts.push([u.liftDoor ? 'door' : u.item.t, q.x, q.z]); } });
          const panels = new Set((typeof MACHINES !== 'undefined' ? MACHINES : []).filter(m => m.deck === deckDef.num).map(m => typeof panelPlace === 'function' ? panelPlace(m.id) : null).filter(Boolean));
          for (const pl of PLACE_OF.values()) { const s = placeSpot(pl.id); if (!s) continue;
            let best = Infinity, by = null; for (const [t, x, z] of lifts) { const dd = Math.hypot(s.x - x, s.z - z); if (dd < best) { best = dd; by = t; } }
            if (best < 2) out.push([pl.id, pl.type, panels.has(pl.id) ? 'PANEL' : '', Math.round(best * 100) / 100, by]); }
          return [deckDef.num, lifts.length, out.sort((a, b) => a[3] - b[3])]; })()""")
        print('deck', r[0], 'lift parts', r[1]); [print('   ', x) for x in r[2]]
    print('errors', g.errors[:3]); g.close()
