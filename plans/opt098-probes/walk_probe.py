# OP1, 0.98 turn 6 (FX24-2, FX12-1, TQ1-1): the crew's planned walks against their real ones, on the drawn deck.
#   python3 walk_probe.py BUILD.html DECK DAY FROM_HH:MM TO_HH:MM [OUT.json]
# Steps the game in 1-real-second chunks (0.6 ship minutes; drawing skipped) and samples every crew member on the deck:
# when they leave a settled spot and when they settle at the next, against planWhere's segment for that place (its
# `from`, the minute the plan has them there). Prints, by kind (tradition, toilet, meal, other): how late they settle
# after their plan's minute (negative: early), how long the walk took, and how early they set off before the plan's minute.
import sys, os, re, json, statistics as st
src = open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0]; exec(src)
from playwright.sync_api import sync_playwright
G, DECK, DAY = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
hm = lambda s: int(s.split(':')[0]) * 60 + int(s.split(':')[1])
T0, T1 = (DAY - 1) * 1440 + hm(sys.argv[4]), (DAY - 1) * 1440 + hm(sys.argv[5])
SAMPLE = r"""(() => { const now = shipNow(), out = [];
  for (const a of DECK_CREW) { const w = planWhere(a.p, now); out.push([a.p.id, a.settled ? 1 : 0, a.spot ? a.spot.id : null, w && w.placeId, w && w.from, w && (w.tag || w.act), w && w.type]); }
  return [now, out]; })()"""
with sync_playwright() as pw:
    g = Game(pw, G, 390, 844)
    g.ev(f"skipTo({T0 - 20}); if (deckDef.num !== {DECK}) goToDeck({DECK}); player.steer = null; player.stop()")
    g.ev("(() => { const l = DECKS[deckDef.num].lift; if (l) { player.obj.position.copy(cellPos(l[0], l[1])); } })()")
    prev = {}; ev = []; t = 0
    while t < T1:
        g.page.evaluate("window.__skip = true; window.__step(30, 1000 / 30); window.__skip = false")
        t, rows = g.ev(SAMPLE)
        for pid, settled, spot, plan, pfrom, kind, ptype in rows:
            p = prev.get(pid)
            if p is None: prev[pid] = {'settled': settled, 'spot': spot, 'left': t if t > T0 - 19 else None, 'spawn': True}; continue
            if p['settled'] and not settled: p['left'] = t; p['spawn'] = False; p['fromSpot'] = p['spot']
            if settled and (not p['settled'] or spot != p['spot']) and t >= T0:
                ev.append({'id': pid, 'at': round(t, 1), 'spot': spot, 'plan': plan, 'from': pfrom, 'kind': kind, 'type': ptype, 'left': p.get('left'), 'spawn': p.get('spawn'), 'fromSpot': p.get('fromSpot') if not p.get('spawn') else None})
            p['settled'], p['spot'] = settled, spot
    est = g.ev("(L => L.map(([a, b]) => { const A = PLACE_OF.get(a), B = PLACE_OF.get(b); if (!A || !B) return null; return walkLead(A.xy || [A.at[0] + .5, A.at[1] + .5], B); }))(" + json.dumps([[e['fromSpot'], e['spot']] if e['fromSpot'] else [None, None] for e in ev]) + ")")
    for e, x in zip(ev, est): e['est'] = x
    g.close()
def kindOf(e):
    k = str(e['kind'] or ''); ty = str(e['type'] or '')
    return 'tradition' if k.startswith('ev-') else 'toilet' if 'toilet' in k or ty == 'toilet' else 'meal' if k in ('breakfast', 'dinner', 'lunch', 'queue') else 'other'
groups = {}
for e in ev:
    if e['plan'] != e['spot'] or e['from'] is None: continue          # settled somewhere their plan doesn't say (a queue spot, a stand-in): not a timed arrival
    e['late'] = round(e['at'] - e['from'], 1); e['walk'] = round(e['at'] - e['left'], 1) if e['left'] else None; e['early'] = round(e['from'] - e['left'], 1) if e['left'] else None
    groups.setdefault(kindOf(e), []).append(e)
q = lambda xs, p: sorted(xs)[min(len(xs) - 1, int(p * len(xs)))]
print(f"walk_probe {os.path.basename(G)} deck {DECK} day {DAY} {sys.argv[4]}-{sys.argv[5]}: {len(ev)} settlings, {sum(len(v) for v in groups.values())} at their planned place")
for k, xs in sorted(groups.items()):
    L = [e['late'] for e in xs]; W = [e['walk'] for e in xs if e['walk'] is not None and not e['spawn']]; E = [e['early'] for e in xs if e['early'] is not None and not e['spawn']]; S = [e['late'] for e in xs if e['spawn']]
    print(f"  {k:9} n={len(xs):3}  late after the plan's minute: median {st.median(L):5.1f}  p90 {q(L, .9):5.1f}  max {max(L):5.1f}" + (f" | from the lift (n={len(S)}): median {st.median(S):.1f}, max {max(S):.1f}" if S else '') + (f" | walk median {st.median(W):.1f} | set off before the plan by median {st.median(E):.1f}" if W else ''))
    R = [e['walk'] / e['est'] for e in xs if e.get('est') and e['walk'] and not e['spawn']]
    if R: print(f"  {'':9}        the real walk / the planner's walkLead estimate: median {st.median(R):.2f} (10-90%: {q(R, .1):.2f}-{q(R, .9):.2f}, n={len(R)})")
worst = sorted((e for v in groups.values() for e in v), key=lambda e: -e['late'])[:8]
for e in worst: print(f"    late {e['late']:5.1f}  {e['id']} -> {e['spot']} ({e['kind']}) planned {e['from']:.0f}, settled {e['at']}, left {e['left']}{' (came by lift)' if e['spawn'] else ''}")
if len(sys.argv) > 6: json.dump(ev, open(sys.argv[6], 'w'))
