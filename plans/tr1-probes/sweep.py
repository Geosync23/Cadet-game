# TR1 real-game sweep: one short visit per tradition / event. Usage: python3 sweep.py BUILD.html SHARD NSHARDS [id ...]
# For each: the day it's on (first in Days 2-35, Day 1 if only then); you stand in its biggest room on its deck from 6 min
# before; at +12 min: who's there (tagged, settled at its places), the join (TJ_NOW lead, marker on screen, arrow/tip), a tap
# on the leader (else the host, else anyone there): the result, your activity, a card; then a jump to 5 min before its end
# and on to +8 after: still joined, still there, your activity ended. One JSON line per tradition.
import sys, json
sys.argv, ARGS = sys.argv[:1], sys.argv[1:]
exec(open("/home/user/cadet-game/cadet_test.py").read().split("a, shots = run(")[0].replace("timeout=60000", "timeout=240000"))
build, shard, nsh = ARGS[0], int(ARGS[1]), int(ARGS[2]); ONLY = ARGS[3:]
LO, HI = [int(x) for x in os.environ.get('TR1_DAYS', '1-35').split('-')]   # the days to look in (first showing of each)
SAYH = """(() => { window.__said = []; window.__cards = []; window.__toasts = []; if (window.__hook) return; window.__hook = 1;
  const bs = bubbleSay; bubbleSay = function (who, text) { window.__said.push([Math.round(SHIP.time.min), who && (who.p ? who.p.id : who.id || (who.a && who.a.p && who.a.p.id)) || '?', String(text).slice(0, 90)]); return bs.apply(this, arguments); };
  const ds = dialogueShow; dialogueShow = function (id) { window.__cards.push([Math.round(SHIP.time.min), id]); return ds.apply(this, arguments); };
  const ts = toast; toast = function (a, b) { window.__toasts.push([Math.round(SHIP.time.min), a, String(b).slice(0, 100)]); return ts.apply(this, arguments); }; SHIP.device.settings.tips = true; })()"""
PLAN = """JSON.stringify((() => { const out = [];
  const seen = {}; for (let d = %d; d <= %d; d++) for (const e of eventsOn(d)) { if (!seen[e.id] || (seen[e.id].d === 1 && d > 1)) seen[e.id] = { d, from: e.from, to: e.to }; }
  for (const [id, o] of Object.entries(seen)) out.push([id, o.d, o.from, o.to]); return out.sort(); })())"""
LOOK = """JSON.stringify((() => { const d = %d, e = eventsOn(d).find(x => x.id === '%s'); if (!e) return { gone: 1, m: SHIP.time.min };
  if (!e.rooms) e.rooms = eventRooms(e.ev); const ids = tradSpotIds(e);
  const tag = DECK_CREW.filter(a => a.p && evTagId(a.tag || '') === e.id), at = tag.filter(a => a.settled && a.spot);
  const A = TJ_NOW && TJ_NOW.e.id === e.id ? TJ_NOW : null;
  return { m: Math.round(SHIP.time.min), tagged: tag.length, at: at.length, atIts: at.filter(a => ids.has(a.spot.id)).length, rooms: [...e.rooms],
    here: deckDef.num + '|' + roomAt(...player.here()), tj: A ? A.lead : null, mark: !!(TJ_MARK && TJ_MARK.style.display === 'block'),
    goal: typeof IX_GOAL !== 'undefined' && IX_GOAL ? IX_GOAL.label : null, joined: SHIP.events.joined.includes(e.id + '@' + d),
    act: typeof ACT !== 'undefined' && ACT ? ACT.kind + ':' + (ACT.placeId || '-') + ':' + ACT.phase : null, dlg: !!DIALOGUE && DIALOGUE.id,
    host: e.ev.host || (TRAD_JOIN[e.id] || {}).host || null, hostHere: (() => { const h = e.ev.host || (TRAD_JOIN[e.id] || {}).host; const a = h && DECK_CREW.find(c => c.p.id === h); return a ? (a.spot ? a.spot.id : 'walking') + (a.spot && e.rooms.has(deckDef.num + '|' + a.spot.room) ? '' : ' (not in its rooms)') : null; })() }; })())"""
GO = """(() => { const d = %d, e = eventsOn(d).find(x => x.id === '%s'); if (!e) return 'not on';
  if (!e.rooms) e.rooms = eventRooms(e.ev); const rs = [...e.rooms].map(r => r.split('|'));
  const deck = +(rs[0] || [3])[0]; skipTo((d - 1) * 1440 + e.from - 6); goToDeck(deck, null);
  const rk = rs.filter(r => +r[0] === deck).map(r => r[1]).sort((a, b) => (ROOM_TILES[b] || []).length - (ROOM_TILES[a] || []).length)[0];
  const tl = ROOM_TILES[rk]; if (tl) { const free = tl.filter(t => typeof walkable !== 'function' || walkable(...t)); const t = (free.length ? free : tl)[Math.floor((free.length ? free : tl).length / 2)], c = cellPos(...t); player.obj.position.set(c.x, 0, c.z); player.stop(); }
  return deck + '|' + rk; })()"""
TAP = """JSON.stringify((() => { const d = %d, e = eventsOn(d).find(x => x.id === '%s'); if (!e) return 'not on';
  const id = (TJ_NOW && TJ_NOW.e.id === e.id && TJ_NOW.lead) || e.ev.host || (TRAD_JOIN[e.id] || {}).host;
  let a = id && DECK_CREW.find(c => c.p.id === id); if (!a) a = DECK_CREW.find(c => c.p && evTagId(c.tag || '') === e.id && c.settled);
  if (!a) return { who: null };
  const r = tradJoinTap(a); let alt = null;
  if (!r) { alt = 'chat'; if (typeof chatOpen === 'function') { } }
  return { who: a.p.id, tapJoin: r, act: typeof ACT !== 'undefined' && ACT ? ACT.kind + ':' + (ACT.placeId || '-') : null, dlg: !!DIALOGUE && DIALOGUE.id, joined: SHIP.events.joined.includes(e.id + '@' + d) }; })())"""
def mins(g, until, every=30, cap=900):
    out = []
    for _ in range(cap):
        g.step(every); x = json.loads(g.ev("JSON.stringify(SHIP.time.min)"))
        if x >= until: break
with sync_playwright() as pw:
    g = Game(pw, build, 600, 500); plan = json.loads(g.ev(PLAN % (LO, HI))); g.close()
    plan = [p for p in plan if (not ONLY or p[0] in ONLY)]
    plan = [p for k, p in enumerate(plan) if k % nsh == shard]
    for tid, d, fr, to in plan:
        try:
            g = Game(pw, build, 900, 760); R = { 'id': tid, 'day': d, 'from': fr, 'to': to }
            R['where'] = g.ev(GO % (d, tid)); g.ev(SAYH); g.step(5)
            R['dayStart'] = (d - 1) * 1440
            base = (d - 1) * 1440
            peak = { 'tagged': 0, 'atIts': 0 }; firstTj = None; firstMark = None; S = []
            while True:
                g.step(30); x = json.loads(g.ev(LOOK % (d, tid)))
                if x.get('gone'): break
                m = x['m'] % 1440 if x['m'] > 1440 else x['m']
                mm = x['m'] - 0
                for k in peak: peak[k] = max(peak[k], x[k])
                if x['tj'] and firstTj is None: firstTj = [x['m'] - fr, x['tj']]
                if x['mark'] and firstMark is None: firstMark = x['m'] - fr
                if x['m'] >= fr + 12 or x['m'] >= to - 1: break
            R['at12'] = x; R['peak'] = peak; R['firstTj'] = firstTj; R['firstMark'] = firstMark
            R['tap'] = json.loads(g.ev(TAP % (d, tid)))
            g.step(60); R['afterTap'] = json.loads(g.ev(LOOK % (d, tid)))
            g.ev("for (let k = 0; k < 8 && DIALOGUE; k++) try { dialogueStep(0); } catch (x) { break; }")
            if to - 5 > fr + 14:
                g.ev("skipTo(%d)" % (base + to - 5)); g.step(10)
            R['nearEnd'] = json.loads(g.ev(LOOK % (d, tid)))
            while True:
                g.step(30); m = g.ev("SHIP.time.min")
                if m >= to + 8 or m < fr: break
            R['after'] = json.loads(g.ev(LOOK % (d, tid))) if True else None
            r = json.loads(g.ev("JSON.stringify({ said: window.__said.length, saidBy: [...new Set(window.__said.map(x => x[1]))].slice(0, 8), cards: window.__cards, toasts: window.__toasts.filter(t => !/hungry|Exhausted|shower|toilet|Bursting|Starving|new messages|New mail/i.test(t[1] + t[2])).slice(0, 5) })"))
            R.update(r); R['errors'] = g.errors[:3]; g.close()
        except Exception as ex:
            R['crash'] = str(ex)[:300]
            try: g.close()
            except Exception: pass
        print(json.dumps(R), flush=True)
