# PR6 tomas_probe: EV5's L4 (0032351) story A's Saturday moment, Day 6 from 19:10 on a copy with EVENTS_ON and EV_LINE_ON:
# follow Tomas until 'moment:lineTomasSat' opens; save and reload with the panel open (no reply given): is it offered
# again, and does his 22:50 Mail still come? (the storm's moments set their story flag when the panel ends: ER2's fix 4)
# was PR4: EV4's props (96bb2c6): the lantern supper only (part b of s37_probe), with the lanterns and the low light;
# was: EV3's storm S3/S5/S7 (d3bf237), live, switched on, at 390x844:
#  a. S7 Friday Day 12 17:05 in the mess near Lukas: his moment opens ("Sixty"), reply 0 holds the lantern job; no
#     Lukas Mail at 20:50; the lantern job yours when it posts Saturday 14:00;
#  b. S5 the lantern supper, Saturday Day 13: from 17:40 frames played in the mess to 18:40: crew in the mess hall,
#     Brennan there and Lukas not, staying in off, draw calls (phones: under 450), a shot;
#  c. S3 Day 12 15:00 on Deck 7: a rec tap refused with the storm words.
import os, sys, json, re, pathlib
os.environ.setdefault('CADET_WORK', '/tmp/cadet-work')
exec(open('/home/user/cadet-game/plans/review-6/pp.py').read())
path = sys.argv[1]; OUT = pathlib.Path('/home/user/cadet-game/plans/review-6/shots'); OUT.mkdir(exist_ok=True)
save = {'v': 2, 'build': 'x', 'time': {'day': 6, 'min': 1150}, 'player': {'deck': 3, 'tile': [20, 10], 'facing': 0}, 'ship': {'decks': {}, 'eventLog': [], 'evFrom': 0}, 'crew': {}}
pw = sync_playwright().start()
b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
ctx = b.new_context(viewport={'width': 390, 'height': 844}, has_touch=True); pg = ctx.new_page(); errs = []
pg.on('pageerror', lambda e: errs.append(str(e)))
pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
pg.add_init_script(INIT + "try { if (!sessionStorage.getItem('seeded')) { sessionStorage.setItem('seeded', '1'); localStorage.clear(); localStorage.setItem('starship-cadet-save', " + json.dumps(json.dumps(save)) + "); localStorage.setItem('starship-cadet-arrived', '1'); } } catch (e) {}")
(WORK / 'test').mkdir(parents=True, exist_ok=True)
tmp = WORK / 'test' / '_tomas_on.html'; tmp.write_text(instrument(pathlib.Path(path).read_text()))
pg.goto('file://' + str(tmp) + '?debug'); pg.wait_for_function('window.__sc !== undefined || window.__err', timeout=90000)
pg.add_style_tag(content='.bub{animation:none!important}')
ev = lambda s: pg.evaluate('s => window.__sc(s)', s)
step = lambda n: pg.evaluate(f'window.__step({n}, 1000/30)')
step(20); res = {}
PUT = """((deck, rx) => { if (deckDef.num !== deck) goToDeck(deck); const R = DECKS[deck].rooms, key = Object.keys(R).find(k => rx.test(R[k].name || ''));
  const pl = DECKS[deck].places.find(p => p.room === key && p.type !== 'callhome') || DECKS[deck].places.find(p => p.room === key); const c = pl.at, P = cellPos(...c), o = nearestOpen(P.x, P.z, player) || c;
  player.obj.position.copy(cellPos(...o)); player.path.length = 0; target.copy(player.obj.position).setY(.7); return [key, R[key].name]; })"""
FOLLOW = """(() => { const p = schedPeople().find(x => x.id === 'tomas'), w = whereIs(p, shipNow()); if (!w) return null;
  if (w.deck && deckDef.num !== w.deck && w.deck !== 7) goToDeck(w.deck);
  const a = DECK_CREW.find(x => x.p && x.p.id === 'tomas' && x.h); if (!a) return [clockText(), w.deck, w.placeId || w.act, 'not on deck'];
  const c = [Math.round(a.x + OX), Math.round(a.z + OZ)], P = cellPos(...c), o = nearestOpen(P.x + 1, P.z, player) || c;
  player.obj.position.copy(cellPos(...o)); player.path.length = 0; target.copy(player.obj.position).setY(.7);
  return [clockText(), w.deck, w.placeId || w.act, DIALOGUE ? DIALOGUE.id : null]; })()"""
ev("skipTo(5 * 1440 + 19 * 60 + 10)"); step(10)
got = None
for k in range(40):
    r = ev(FOLLOW); step(60)
    d = ev("DIALOGUE ? DIALOGUE.id : null")
    if k % 4 == 0: print('  ', r, d, flush=True)
    if d: got = [r, d]; break
res['opened'] = got; print('opened', got, flush=True)
res['mineBefore'] = ev("SHIP.event ? Object.keys(SHIP.event.mine).filter(k => /story|moment|met/.test(k)) : null")
pg.screenshot(path=str(OUT / 'line_tomas_sat_390.png'), timeout=180000)
ev("saveGame()"); pg.reload(); pg.wait_for_function('window.__sc !== undefined || window.__err', timeout=90000); step(30)
res['afterReload'] = ev("[clockText(), DIALOGUE ? DIALOGUE.id : null, SHIP.event ? Object.keys(SHIP.event.mine).filter(k => /story|moment|met/.test(k)) : null, typeof flag === 'function' ? flag('line.promised') : null]")
print('after reload', res['afterReload'], flush=True)
again = None
for k in range(16):
    ev(FOLLOW); step(60); d = ev("DIALOGUE ? DIALOGUE.id : null")
    if d: again = d; break
res['offeredAgain'] = again; print('offered again', again, flush=True)
ev("(() => { if (DIALOGUE) dialogueEnd(true); })()")
ev("skipTo(5 * 1440 + 22 * 60 + 55)"); step(20)
res['tomasMail'] = ev("(SHIP.mail || SHIP.inbox || []).filter(m => /Tomas/.test(m.from || '') ).map(m => m.subject || m.title).slice(-3)")
print('Tomas mail by 22:55', res['tomasMail'], flush=True)
print('RESULT', json.dumps(res)[:2000]); print('errors', errs[:5])
print('TOMAS', 'LOST' if got and not again and not res['tomasMail'] else 'OK')
b.close(); pw.stop()
