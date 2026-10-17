# reviewer 1f: which tappable things sit within JOB_REACH (1.5 m) of a job stop (machine panels, chore stops)? A tap on them goes to the job while it's yours (0.28.52)
import sys, json
src = open('cadet_test.py').read().split('import sys, json, hashlib')[0]
exec(src)
from playwright.sync_api import sync_playwright
JS = r"""(() => {
  const out = [], v = new THREE.Vector3();
  const spots = [];
  for (const m of machineList()) if (m.deck === deckDef.num) { const pid = panelPlace(m.id); if (pid && PLACE_OF.has(pid)) spots.push(['panel:' + m.id, placeSpot(pid)]); }
  for (const it of ITEMS) { if (!it.hit) continue; it.hit.getWorldPosition(v);
    for (const [k, s] of spots) { const d = Math.hypot(v.x - s.x, v.z - s.z); if (d < JOB_REACH && !/job board|ship health/i.test(it.t)) out.push([k, it.t, Math.round(d * 100) / 100]); } }
  return JSON.stringify({ n: spots.length, out });
})()"""
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    for n in (1, 2, 3, 4, 5, 6):
        g.ev(f"goToDeck({n})"); g.step(3)
        r = json.loads(g.ev(JS))
        seen = {}
        for k, t, d in r['out']: seen.setdefault(t, []).append((k, d))
        print('deck', n, 'panels', r['n'], 'things near a panel:', len(seen))
        for t, ks in sorted(seen.items()): print('   ', t, '<-', ks[:3])
    g.close()
