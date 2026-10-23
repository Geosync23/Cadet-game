# AR1: a tracked shift, followed honestly: go where the arrow points (teleport = walk), tap the thing it points at
import sys, json
from harness import *
DAY = int(sys.argv[1]) if len(sys.argv) > 1 else 2
TRACK_SHIFT = (sys.argv[2] if len(sys.argv) > 2 else 'shift')
FOLLOW = r"""(() => {
  const out = {};
  if (typeof DIALOGUE !== 'undefined' && DIALOGUE) { const v = dialogueView(); if (v && v.choices) dialogueChoose(0); else dialogueNext(); return 'read a line: ' + (v && v.name); }
  if (ACT) return null;
  const cs = document.getElementById('clockScreen'); if (cs && !cs.hidden && getComputedStyle(cs).display !== 'none') { const gl = (goalNow() || {}).label || ''; const want = /clock out/i.test(gl) ? /clock out/i : /clock in/i; const b = [...cs.querySelectorAll('button')].find(b => want.test(b.textContent)); if (!b) { const c = [...cs.querySelectorAll('button')].find(b => /close/i.test(b.textContent)); if (c) c.click(); return 'clock screen closed'; } if (b) { const t = b.textContent; b.click(); return 'clock screen: ' + t; } }
  const bd = document.getElementById('ixBoard'); if (bd && !bd.hidden) { const b = [...bd.querySelectorAll('#ixBoardL button')].find(b => /turn it in|take/i.test(b.textContent)); const t = b ? b.textContent + ' (' + (b.closest('.ixjob') || b.parentNode).textContent.slice(0, 60) + ')' : 'nothing to press'; if (b) b.click(); else document.getElementById('ixBoardC').click(); return 'board: ' + t; }
  const g = goalNow(); if (!g) return null;
  if (deckDef.num !== g.deck) { goToDeck(g.deck); return 'lift to deck ' + g.deck; }
  const w = ixGoalWorld(g); if (!w) return 'arrow with no spot: ' + g.label;
  const p = player.obj.position, d = Math.hypot(w.x - p.x, w.z - p.z);
  const it = ITEMS.map(i => { i.hit.getWorldPosition(_wp); return [i, _wp.clone(), Math.hypot(_wp.x - w.x, _wp.z - w.z)]; }).sort((a, b) => a[2] - b[2])[0];
  if (d > 2.2) { const gl = nearestOpen(w.x, w.z, player); player.obj.position.copy(cellPos(...gl)); player.stop(); return 'walked to ' + g.label; }
  if (window.__lastTap === g.label + '|' + Math.floor(shipNow())) return null;
  window.__lastTap = g.label + '|' + Math.floor(shipNow());
  const sh = /the (.+) shelf/.exec(g.label || ''); if (sh) { const x = ITEMS.find(i => i.t === sh[1]); if (x) { x.hit.getWorldPosition(_wp); return 'tapped shelf ' + x.t + ' -> ' + playerTap(x, _wp.clone(), _wp.clone()); } }
  if (it && it[2] < 2.5) { const r = playerTap(it[0], it[1].clone(), it[1].clone()); return 'tapped ' + it[0].t + ' -> ' + r; }
  return 'nothing to tap at ' + g.label;
})()"""
with sync_playwright() as pw:
    g = G(pw)
    if DAY > 2: g.ev(f"devmodeRun('Set', () => devmodeSetCareerTo({DAY - 1}))"); g.step(10)
    else: g.ev("devmodeRun('Set', () => devmodeSetCareerTo(1))"); g.step(10)
    g.ev(f"devmodeRun('Clock', () => devmodeSkipTo({(DAY - 1) * 1440 + int(os.environ.get('START', 450))}))"); g.step(10)
    g.ev("SHIP.player.track = 'stale-from-yesterday'"); (os.environ.get('CLOCKIN') and g.ev('careerClock(shipNow(), true)'))   # as in a real game: the last job taken stays the tracked id
    print('start', g.ev('clockText()'), 'arrow:', g.ev('goalNow() && goalNow().label'))
    items = g.ev("trkItems().map(x => [x.sec, x.key, x.title, x.sub, x.tag, x.goal && x.goal.label])")
    for x in items: print('  tracked item:', x)
    if TRACK_SHIFT == 'shift':
        k = next((x[1] for x in items if x[1].startswith('shift:')), None)
        print('tap Tracked "Your shift":', k, g.ev(f"trkTap({json.dumps(k)})") if k else 'NO SHIFT ROW', '->', g.ev('goalNow() && goalNow().label'))
    n0 = len(g.log()); acts = []
    def hook(g):
        r = g.ev(FOLLOW)
        if r: acts.append((g.ev('clockText()'), r))
    g.run_min(int(sys.argv[3]) if len(sys.argv) > 3 else 600, hook=hook)
    L = [tuple(l) for l in g.log()[n0:]] + [(a[0], 'PLAYER', a[1]) for a in acts]
    import re as _r
    key = lambda x: _r.sub(r'.*?(\d\d:\d\d)$', r'\1', x[0])
    for l in sorted(L, key=lambda x: (x[0][:6], key(x))): print(*l)
    print('errors', g.errors[:5])
    g.close()
