# RV29: PL2 note 3: the no-tray Take a seat button by every public seat on every deck (SEAT_BTN_ALL set on, as a real
# game has it): stand on the nearest free cell to the seat, ask seatBtnSeat, press seatBtnGo, check you sit there. Also:
# never a private seat, never a rec deck seat, hidden with SEAT_BTN_ALL off, and the tray path in the mess hall.
import sys, json, types
from playwright.sync_api import sync_playwright
src = open(sys.argv[1] + '/cadet_test.py').read(); src = src[:src.index('import sys, json, hashlib')]
ct = types.ModuleType('ct'); exec(src, ct.__dict__)
JS = r"""((n) => { if (deckDef.num !== n) goToDeck(n); SEAT_BTN_ALL = true; DECK_CREW.length = 0;
  const all = [...PLACE_OF.values()].filter(pl => pl.deck === n && pl.pose === 'sit'), types = {};
  const pub = all.filter(pl => SIT_TYPES.has(pl.type) && !privatePlace(pl)), out = { n, sitPlaces: all.length, pub: pub.length, ok: 0, offeredOther: 0, noCell: 0, none: [], notSat: [], privOffered: [], typesOut: {} };
  for (const pl of all) if (!pub.includes(pl)) out.typesOut[pl.type + (privatePlace(pl) ? '(private)' : '')] = (out.typesOut[pl.type + (privatePlace(pl) ? '(private)' : '')] || 0) + 1;
  for (const pl of pub) { const sp = placeSpot(pl.id); if (!sp) { out.none.push(pl.id + ':nospot'); continue; }
    const rm = pl.room || roomAt(...pl.at); let best = null;
    for (let a = 0; a < W; a++) for (let b = 0; b < D; b++) { if (!free(a, b) || roomAt(a, b) !== rm) continue; const c = cellPos(a, b), d = Math.hypot(c.x - sp.x, c.z - sp.z); if (!best || d < best[1]) best = [[a, b], d, c]; }
    if (!best || best[1] > 2.1) { out.noCell++; continue; }
    if (ACT) actEnd(true); player.obj.position.set(best[2].x, 0, best[2].z);
    const s = seatBtnSeat(); if (!s) { out.none.push(pl.id); continue; }
    if (s[0].id !== pl.id) out.offeredOther++;
    if (privatePlace(s[0])) out.privOffered.push(s[0].id);
    const go = seatBtnGo(); if (go && ACT && ACT.kind === 'sit' && ACT.placeId === s[0].id) out.ok++; else out.notSat.push([pl.id, go, ACT && ACT.kind]);
    if (ACT) actEnd(true); }
  for (const pl of all.filter(q => privatePlace(q)).slice(0, 30)) { const sp = placeSpot(pl.id); if (!sp) continue; player.obj.position.set(sp.x, 0, sp.z); const s = seatBtnSeat(); if (s && privatePlace(s[0])) out.privOffered.push(s[0].id); }
  SEAT_BTN_ALL = false; const p1 = pub[0] && placeSpot(pub[0].id); if (p1) { player.obj.position.set(p1.x, 0, p1.z); out.offWhenSwitchOff = seatBtnSeat(); }
  out.none = out.none.slice(0, 12); out.notSat = out.notSat.slice(0, 6); return out; })"""
with sync_playwright() as pw:
    g = ct.Game(pw, sys.argv[2])
    print('SIT_TYPES', g.ev("[...SIT_TYPES].join(' ')"))
    for n in [1, 2, 3, 4, 5, 6, 7]:
        try: print(json.dumps(g.ev(JS + f"({n})"))[:1500])
        except Exception as e: print('deck', n, 'err', str(e)[:300])
    print('errors', g.errors[:3]); g.close()
