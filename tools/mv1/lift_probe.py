# note 24 probe: per frame, every crew body's drawn root; flags jumps and bodies far from their agent
import sys, json, os
os.chdir('/home/user/Cadet-game')
exec(open('cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
BUILD = sys.argv[1]; DECKS_T = json.loads(sys.argv[2]) if len(sys.argv) > 2 else [[3, 1, 420], [4, 1, 450], [5, 1, 530], [7, 1, 1140]]
SRC = r"""(({ n, day, min, frames }) => {
  setShipNow((day - 1) * 1440 + min); goToDeck(n);
  const last = new Map(), out = [], born = new Map(); let f = 0;
  window.__lp = { tick() {
    f++;
    const seen = new Set();
    for (const a of DECK_CREW) {
      const r = a.h.rig && a.h.rig.root ? a.h.rig.root.position : null; if (!r) continue;
      seen.add(a);
      const want = { x: a.x + a.lx + a.hx, z: a.z + a.lz + a.hz };
      const v = _cp.set(r.x, 1, r.z).project(camera), inv = Math.abs(v.x) < 1.05 && Math.abs(v.y) < 1.05; const l = last.get(a), j = l ? Math.hypot(r.x - l.x, r.z - l.z) : 0, off = Math.hypot(r.x - want.x, r.z - want.z);
      if (!born.has(a)) born.set(a, f);
      if (inv && (j > .3 || off > .3) && out.length < 60) out.push({ f, who: a.p.id, age: f - born.get(a), jump: +j.toFixed(2), off: +off.toFixed(2), r: [+r.x.toFixed(1), +r.z.toFixed(1)], at: [+a.x.toFixed(1), +a.z.toFixed(1)], goal: a.goalId, path: a.path.length, settled: a.settled, full: !!a.h.full, vis: a.h.full ? a.h.rig.root.visible : null, t: hhmm(SHIP.time.min), lp: [+player.obj.position.x.toFixed(1), +player.obj.position.z.toFixed(1)] });
      last.set(a, { x: r.x, z: r.z });
    }
    return out.length;
  }, out };
  return DECK_CREW.length;
})"""
with sync_playwright() as pw:
    for n, day, mn in DECKS_T:
        g = Game(pw, BUILD)
        g.ev('(' + SRC + ')(' + json.dumps({'n': n, 'day': day, 'min': mn, 'frames': 0}) + ')')
        g.step(30)
        for k in range(int(sys.argv[3]) if len(sys.argv) > 3 else 1500):
            g.page.evaluate('window.__skip = true; window.__step(1, 1000/30)')
            g.ev('__lp.tick()')
        o = g.ev('__lp.out')
        print('deck', n, 'day', day, 'min', mn, 'flags', len(o))
        for x in o[:40]: print('  ', json.dumps(x))
        g.close()
