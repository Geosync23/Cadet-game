# TB4 probe: the 0.92.6 eight in the real game on their days. Usage: python3 plans/tb4-probes/t926_probe.py BUILD.html [id ...]
# (a build with TRAD926_JOIN_ON off is switched on in a copy first; about 6-10 minutes a tradition)
# Per tradition: skip to 6 minutes before its start, go to its deck, stand in its room, run frames: the leader (TJ_NOW),
# the marker and the arrow from its start; at +6 a tap on the leader: the card (its lines, the question), pick an answer,
# then the activity (ACT or the walk); frames to +16 (bubbles); then a real save and reload (joined kept, no marker,
# no errors); then frames past its end: the activity ended, no marker, no arrow. Prints one block each and SUMMARY lines.
import sys, json, pathlib
sys.argv, ARGS = sys.argv[:1], sys.argv[1:]
exec(open('/home/user/cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
build = ARGS[0]
_src = pathlib.Path(build).read_text()
if "const TRAD926_JOIN_ON = URL_FLAGS.has('trad926');" in _src:
    build = str(WORK / 'test' / 't926-on.html'); pathlib.Path(build).write_text(_src.replace("const TRAD926_JOIN_ON = URL_FLAGS.has('trad926');", 'const TRAD926_JOIN_ON = true;'))
DAYS = {'tool-night': 29, 'route-night': 38, 'card-night': 73, 'garden-walk': 63, 'window-sketch': 48, 'window-sketch-2': 104, 'open-house': 53, 'spoon-band': 64, 'worst-joke': 81}
ids = ARGS[1:] or list(DAYS)
SAVEJS = """(() => { const decks = {}; for (const n in SHIP.decks) if (SHIP.decks[n].open.size) decks[n] = { open: [...SHIP.decks[n].open] };
  const save = { v: SAVE_V, build: GAME_BUILD, time: { day: SHIP.time.day, min: SHIP.time.min }, player: { deck: player.deck, tile: player.here(), facing: player.face }, ship: { decks }, crew: {}, flags: SHIP.flags || {}, notes: SHIP.notes || [] };
  if (typeof crewState === 'function') save.crew = crewState(SHIP.time.day); for (const f of SAVE_EXTRA) f(save); return JSON.stringify(save); })()"""
SPY = """(() => { window.__said = []; window.__cards = []; window.__toasts = []; if (window.__hook) return; window.__hook = 1;
  const bs = bubbleSay; bubbleSay = function (who, text) { if (who && who.p) window.__said.push([SHIP.time.min, who.p.id, text]); return bs.apply(this, arguments); };
  const ts = toast; toast = function (a, b) { window.__toasts.push([SHIP.time.min, a, String(b).slice(0, 140)]); return ts.apply(this, arguments); }; })()"""
FIND = """JSON.stringify((id => { let d = %d; let e = eventsOn(d).find(x => x.id === id);
  if (!e) for (d = 1; d < 400; d++) { e = eventsOn(d).find(x => x.id === id); if (e) break; }
  return e ? { d, from: e.from, to: e.to, deck: e.ev.where[0].deck, rooms: [...(e.rooms || (e.rooms = eventRooms(e.ev)))] } : null; })('%s'))"""
IN = """((rk) => { const tl = ROOM_TILES[rk], c = cellPos(...tl[Math.floor(tl.length / 2)]); player.obj.position.copy(cellPos(...nearestOpen(c.x, c.z, player))); player.stop(); return rk; })('%s')"""
LOOK = """JSON.stringify((() => { const id = '%s', d = %d, key = id + '@' + d;
  return { m: Math.floor(SHIP.time.min), day: SHIP.time.day, tj: TJ_NOW && TJ_NOW.key === key ? TJ_NOW.lead : (TJ_NOW ? 'other:' + TJ_NOW.key : null), mark: !!(TJ_MARK && TJ_MARK.style.display === 'block' && /★/.test(TJ_MARK.textContent)),
    markTxt: TJ_MARK ? TJ_MARK.textContent : null, goal: typeof IX_GOAL !== 'undefined' && IX_GOAL ? [IX_GOAL.tj || null, IX_GOAL.label] : null,
    joined: SHIP.events.joined.includes(key), act: typeof ACT !== 'undefined' && ACT ? [ACT.kind, ACT.placeId, ACT.phase, ACT.o && ACT.o.pose, ACT.o && ACT.o.tj] : null,
    walk: TJ_WALK ? [TJ_WALK.e.id, TJ_WALK.n, TJ_WALK.path.length] : null, dlg: DIALOGUE ? DIALOGUE.id : null, here: roomAt(...player.here()), deck: deckDef.num }; })())"""
def run_one(pw, i):
    out = {'id': i}
    g = Game(pw, build, 900, 760)
    g.ev("if (typeof GUIDE_ON !== 'undefined' && GUIDE_ON) { GUIDE.tq.length = 0; }")
    f = json.loads(g.ev(FIND % (DAYS.get(i, 1), i)))
    if not f: print(i, 'NOT ON'); g.close(); return {'id': i, 'err': 'not on'}
    d, fr, to = f['d'], f['from'], f['to']; rk = [r.split('|')[1] for r in f['rooms'] if int(r.split('|')[0]) == f['deck']][0]
    print(f'== {i}: day {d} {fr // 60:02d}:{fr % 60:02d}-{to // 60:02d}:{to % 60:02d} deck {f["deck"]} rooms {f["rooms"]}')
    g.ev(f"(() => {{ skipTo({(d - 1) * 1440 + fr - 6}); goToDeck({f['deck']}, null); }})()"); g.step(5); g.ev(SPY); g.ev(IN % rk)
    first = {}; last = None; tapped = False; card = None
    def look(): return json.loads(g.ev(LOOK % (i, d)))
    for k in range(3000):
        g.step(10); x = look()
        sig = (x['tj'], x['mark'], x['goal'] and x['goal'][0], x['joined'], x['act'] and x['act'][0], x['walk'] and x['walk'][1], x['dlg'])
        if sig != last: print('  ', f"{x['m'] // 60:02d}:{x['m'] % 60:02d}", 'tj', x['tj'], 'mark', x['mark'], x['markTxt'], 'goal', x['goal'], 'joined', x['joined'], 'act', x['act'], 'walk', x['walk'], 'dlg', x['dlg'], 'here', x['here']); last = sig
        mm = x['m'] - fr
        if x['tj'] and not x['tj'].startswith('other') and 'tj' not in first: first['tj'] = mm
        if x['mark'] and 'mark' not in first: first['mark'] = mm
        if x['goal'] and x['goal'][0] == i + '@' + str(d) and 'goal' not in first: first['goal'] = mm; out['tip'] = x['goal'][1]
        if not tapped and mm >= 6 and x['tj'] and not x['tj'].startswith('other'):
            tapped = True
            r = g.ev("(() => { const ok = tradJoinTap(TJ_NOW.agent); const L = []; let n = 0; while (DIALOGUE && n++ < 20) { const v = dialogueView(); if (!v) break; L.push([v.who, v.text || '', v.choices]); dialogueStep(v.choices ? 1 : undefined); } return { ok, L }; })()")
            card = r; print('   TAP ->', r['ok']); [print('     card:', l) for l in r['L']]
            g.step(3); x = look(); out['after_tap'] = {'joined': x['joined'], 'act': x['act'], 'walk': x['walk'], 'goal': x['goal'], 'mark': x['mark']}
            print('   after tap:', out['after_tap'])
        if tapped and mm >= 16: break
    out['first'] = first; out['card'] = card
    r = json.loads(g.ev("JSON.stringify({ said: window.__said, toasts: window.__toasts })"))
    out['bubbles'] = len([s for s in r['said'] if s[0] >= fr]); print('   bubbles since start', out['bubbles'], r['said'][-5:]); print('   toasts', r['toasts'][-4:])
    # reload mid-way: a real save, then the page again
    txt = g.ev(SAVEJS); key = g.ev("SAVE_KEY"); url = g.page.url.split('?')[0]
    g.page.add_init_script("try { if (!sessionStorage.getItem('t926') ) { localStorage.clear(); localStorage.setItem(" + json.dumps(key) + ", " + json.dumps(txt) + "); sessionStorage.setItem('t926', '1'); } } catch (e) {}")
    g.page.goto(url + '?debug', timeout=120000); g.page.wait_for_function('window.__sc !== undefined', timeout=120000)
    print('   loaded the save:', g.ev("JSON.stringify([SHIP.time.day, Math.floor(SHIP.time.min), typeof TITLE !== 'undefined' && TITLE.on])"))
    g.ev("if (typeof TITLE !== 'undefined' && TITLE.on) titleClose('go')"); g.step(20); g.ev("if (typeof TITLE !== 'undefined' && TITLE.on) { TITLE.on = false; document.getElementById('title').hidden = true; }"); g.step(20)
    x = look(); out['reload'] = {'m': x['m'], 'joined': x['joined'], 'mark': x['mark'], 'tj': x['tj'], 'act': x['act'], 'walk': x['walk']}
    print('   after reload:', out['reload'])
    g.ev(SPY)
    g.step(300); x = look(); out['reload_later'] = {'m': x['m'], 'act': x['act'], 'walk': x['walk']}; print('   a little after the reload:', out['reload_later'])
    g.ev(f"skipTo({(d - 1) * 1440 + to - 2})"); g.step(30)
    for k in range(400):
        g.step(10); x = look()
        if x['m'] >= to + 2 or x['day'] > d: break
    out['end'] = {'m': x['m'], 'act': x['act'], 'walk': x['walk'], 'mark': x['mark'], 'tj': x['tj'], 'goal': x['goal']}
    print('   after the end:', out['end'])
    out['errors'] = g.errors[:6]; print('   errors', g.errors[:6])
    g.ev("localStorage.clear()"); g.close()
    return out
with sync_playwright() as pw:
    res = [run_one(pw, i) for i in ids]
for o in res:
    if o.get('err'): print('SUMMARY', o['id'], 'ERR', o['err']); continue
    a = o.get('after_tap') or {}
    ok = (o['first'].get('tj') is not None and o['first'].get('mark') is not None and o['first'].get('goal') is not None and a.get('joined') and (a.get('act') or a.get('walk'))
          and o['card'] and len(o['card']['L']) >= 3 and o['reload']['joined'] and not o['reload']['mark'] and not o['end']['mark'] and not (o['end']['act'] and o['end']['act'][4]) and not o['end']['walk'] and not o['errors'])
    print('SUMMARY', o['id'], 'OK' if ok else 'PROBLEM', 'first', o['first'], 'act', a.get('act') or a.get('walk'), 'bubbles', o['bubbles'], 'reload', o['reload'], 'end', o['end'], 'errors', len(o['errors']))
