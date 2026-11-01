# RV31: which small repairs and odd jobs (FIX_ROWS, ODD_ROWS) FIXTAP_ON reaches, and what a tap there does.
# For each row whose stop place has an ixKind (a place with its own use), on its deck: every tappable thing in the stop's
# room within IX_NEAR of the stop's spot (fixThingTap's test), and, with the job yours on a FIXTAP_ON copy, what
# fixThingTap does on a tap on it (direct call). Run from the repo root: python3 plans/rv31-probes/fixtap_reach.py ON.html
import sys, json
exec(open('cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
ROWS = r"""(() => [...FIX_ROWS, ...ODD_ROWS].map(s => { const id = s.split('|')[0], x = fixRow(id), pl = x && placeById(x.place); return pl ? [id, x.place, pl.deck, pl.type] : [id, x && x.place, null, null]; }))()"""
ONE = r"""((rid) => { actEnd(true); SHIP.jobs = SHIP.jobs.filter(j => !String(j.id).startsWith('rvtap-')); SHIP.player.work = null;
  const r = fixRow(rid), pid = r.place, pl = PLACE_OF.get(pid); if (!pl) return { rid, err: 'no place on this deck' };
  const kind = ixKind(pl, null), sp = placeSpot(pid), t = shipNow();
  const j = { id: 'rvtap-' + r.id, machine: null, deck: placeById(pid).deck, room: pl.room, kind: 'chore', chore: 'fix', target: r.id, title: r.title, tier: 1, stops: [{ deck: placeById(pid).deck, placeId: pid, mins: r.mins, tag: 'fix' }],
    urgency: 0, posted: t, found: t, claimedBy: 'you', status: 'claimed', start: t, parts: [], fix: r.id, fixS: 'o', tool: r.tool };
  SHIP.jobs.push(j); MACH_REV++;
  const b = new THREE.Box3(), c = new THREE.Vector3(), out = [];
  for (const it of ITEMS.filter(i => i.hit)) { b.setFromObject(it.hit); b.getCenter(c);
    if (roomAt(...cellAt(c.x, c.z)) !== pl.room) continue; const d = ixDist(it, sp); if (d >= IX_NEAR) continue;
    actEnd(true); jobStops(j).forEach(s => { s.done = false; });
    const took = fixThingTap(it, c); out.push([it.t, Math.round(d * 100) / 100, took, ACT ? ACT.kind : null]); }
  actEnd(true); SHIP.jobs = SHIP.jobs.filter(x => x !== j); MACH_REV++;
  return { rid, pid, type: pl.type, kind, items: out }; })"""
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.step(3); g.ev("setShipNow(1440 * 6 + 10 * 60); machinesNow()")
    rows = g.ev(ROWS); print(len(rows), 'rows')
    for d in sorted({r[2] for r in rows if r[2]}):
        g.ev(f"goToDeck({d})"); g.step(5)
        for rid, pid, deck, typ in rows:
            if deck != d: continue
            o = g.ev(f"({ONE})({json.dumps(rid)})")
            if o.get('kind') or o.get('items') and any(x[2] for x in o['items']): print(json.dumps(o))
    for r in rows:
        if not r[2]: print('no place:', r)
    pe = [e for e in g.errors if e.startswith('pageerror')]; print('page errors', pe[:3])
