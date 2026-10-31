# TR1 probe: Spice shelf supper in the real game. Usage: python3 plans/tr1-probes/spice_probe.py BUILD.html [day ...]
# You stand in the mess hall from 18:15 on a Tuesday; each ~30 frames: the ship minute, the join offer (TJ_NOW), Brennan's
# spot, joined, who is there for it. At 18:40 a tap on Brennan (tradJoinTap) is tried before any auto-join could matter.
import sys, json, pathlib
sys.argv, ARGS = sys.argv[:1], sys.argv[1:]
exec(open('/home/user/cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
build = ARGS[0]; days = [int(x) for x in ARGS[1:]] or [2, 9, 16]
SAY = """(() => { window.__said = []; window.__cards = []; window.__toasts = []; if (window.__hook) return; window.__hook = 1;
  const bs = bubbleSay; bubbleSay = function (who, text) { if (who && who.p) window.__said.push([SHIP.time.min, who.p.id, text]); return bs.apply(this, arguments); };
  const ds = dialogueShow; dialogueShow = function (id) { window.__cards.push([SHIP.time.min, id]); return ds.apply(this, arguments); };
  const ts = toast; toast = function (a, b) { window.__toasts.push([SHIP.time.min, a, String(b).slice(0, 120)]); return ts.apply(this, arguments); }; })()"""
IN = """(() => { const tl = ROOM_TILES['M'], c = cellPos(...tl[Math.floor(tl.length / 2)]); player.obj.position.set(c.x, 0, c.z); player.stop(); return [c.x, c.z]; })()"""
LOOK = """JSON.stringify((() => { const d = %d, e = eventsOn(d).find(x => x.id === 'spice-shelf-supper'), b = DECK_CREW.find(a => a.p.id === 'brennan');
  const tag = DECK_CREW.filter(a => a.p && evTagId(a.tag || '') === 'spice-shelf-supper');
  return { m: SHIP.time.min, on: !!e, from: e && e.from, to: e && e.to, joinable: tradJoinable(e), tj: TJ_NOW && [TJ_NOW.key, TJ_NOW.lead], mark: !!(TJ_MARK && TJ_MARK.style.display === 'block'),
    goal: typeof IX_GOAL !== 'undefined' && IX_GOAL ? IX_GOAL.label : null, b: b ? [b.spot && b.spot.id, b.settled, b.tag || null, roomAt(...[b.x, b.z].map((v, i) => v))] : 'not on deck',
    joined: SHIP.events.joined.includes('spice-shelf-supper@' + d), here: roomAt(...player.here()), tagged: tag.length, settled: tag.filter(a => a.settled).map(a => a.p.id + '@' + (a.spot ? a.spot.id : '-')), goers: e ? tradGoers(e).map(p => p.id) : [] }; })())"""
with sync_playwright() as pw:
    for d in days:
        g = Game(pw, build, 900, 760)
        g.ev("(() => { skipTo(%d * 1440 + 18 * 60 + 10); goToDeck(3, null); SHIP.device.settings.tips = false; })()" % (d - 1)); g.ev(SAY); g.step(10)
        print('== Day', d, 'weekday', g.ev('weekday(%d)' % d), 'player at', g.ev(IN))
        last = None; tapped = None; closeAt = -1
        for k in range(400):
            g.step(30); x = json.loads(g.ev(LOOK % d))
            sig = (x['tj'] and tuple(x['tj']), x['b'] if isinstance(x['b'], str) else tuple(x['b'][:2]), x['joined'], x['mark'], x['tagged'])
            if sig != last: print(' ', x['m'], 'tj', x['tj'], 'mark', x['mark'], 'brennan', x['b'], 'joined', x['joined'], 'tagged', x['tagged'], 'goal', x['goal']); last = sig
            if k == 0: print('  on', x['on'], x['from'], x['to'], 'joinable', x['joinable'], 'goers', len(x['goers']), x['goers'])
            if tapped is None and x['m'] >= 1120:
                tapped = g.ev("(() => { const b = DECK_CREW.find(a => a.p.id === 'brennan'); return b ? [tradJoinTap(b), !!DIALOGUE && DIALOGUE.id] : 'no brennan'; })()")
                print('  18:40 tap on Brennan -> tradJoinTap', tapped, 'settled at the mess:', x['settled'])
                closeAt = k + int(os.environ.get("TR1_CARD_STEPS", "1"))
            if tapped is not None and k == closeAt:
                print('  closing the card at', x['m'], g.ev("(() => { let n = 0; while (DIALOGUE && n < 20) { try { dialogueStep(0); } catch (e) { break; } n++; } return [n, !!DIALOGUE]; })()"))
            if x['m'] >= 1155: break
        r = json.loads(g.ev("JSON.stringify({ said: window.__said, cards: window.__cards, toasts: window.__toasts })"))
        print('  cards', r['cards']); print('  toasts', r['toasts'][:8]); print('  bubbles', len(r['said']), r['said'])
        print('  errors', g.errors[:4]); g.close()
