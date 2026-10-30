# patch #5: Deck 5's paths are the same with the ladder on (400 fixed tile pairs, as the player and as crew), and the lift still answers
import sys, os, json; sys.path.insert(0, '/home/user/Cadet-game/plans/patch-plan-probes')
from pp import *
g = start('?nosave&debug' + os.environ.get('Q', '')); g.step(5)
g.ev("goToDeck(5)"); g.step(3)
r = g.ev(r"""(() => { const tiles = []; for (let j = 0; j < D; j++) for (let i = 0; i < W; i++) if (free(i, j)) tiles.push([i, j]);
  let s = 12345; const rnd = () => (s = (s * 1103515245 + 12345) % 2147483648) / 2147483648; const out = [];
  for (let k = 0; k < 400; k++) { const a = tiles[Math.floor(rnd() * tiles.length)], b = tiles[Math.floor(rnd() * tiles.length)];
    const p = findPath(a, b, null, player), c = findPath(a, b, null, null); out.push([(p || []).map(String).join(';'), (c || []).map(String).join(';')]); }
  return { n: tiles.length, h: out }; })()""")
lift = g.ev("(() => { player.obj.position.copy(cellPos(19, 9)); target.copy(player.obj.position).setY(.7); enterLift(); return 1; })()"); g.secs(4)
print(json.dumps({ 'tiles': r['n'], 'hash': __import__('hashlib').md5(json.dumps(r['h']).encode()).hexdigest(), 'liftPanel': g.ev("!document.getElementById('lift').hidden"),
  'callPanels': g.ev("WALL_DECOR.filter(d => d.e && ['v,17,9','v,19,9'].includes(d.e.key)).map(d => d.e.key + ':' + d.e.type)") }))
g.close()
