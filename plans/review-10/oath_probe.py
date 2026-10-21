# PR10 oath_probe: who is planned in the bow lounge at 14:40 on Day 7 but not there live. arg2: start minute (skipTo), e.g. 865 or 810
import os, sys, json, re, pathlib
os.environ.setdefault('CADET_WORK', '/tmp/cadet-work')
exec(open('/home/user/cadet-game/plans/review-6/pp.py').read())
path = sys.argv[1]; START = int(sys.argv[2])
save = {'v': 2, 'build': 'x', 'time': {'day': 7, 'min': 790}, 'player': {'deck': 3, 'tile': [20, 10], 'facing': 0}, 'ship': {'decks': {}, 'eventLog': [], 'evFrom': 0}, 'crew': {}}
pw = sync_playwright().start()
b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
ctx = b.new_context(viewport={'width': 390, 'height': 844}, has_touch=True); pg = ctx.new_page(); errs = []
pg.on('pageerror', lambda e: errs.append(str(e)))
pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
pg.add_init_script(INIT + "try { if (!sessionStorage.getItem('seeded')) { sessionStorage.setItem('seeded', '1'); localStorage.clear(); localStorage.setItem('starship-cadet-save', " + json.dumps(json.dumps(save)) + "); localStorage.setItem('starship-cadet-arrived', '1'); } } catch (e) {}")
(WORK / 'test').mkdir(parents=True, exist_ok=True)
tmp = WORK / 'test' / '_oath_on.html'; tmp.write_text(instrument(pathlib.Path(path).read_text()))
pg.goto('file://' + str(tmp) + '?debug'); pg.wait_for_function('window.__sc !== undefined || window.__err', timeout=90000)
ev = lambda s: pg.evaluate('s => window.__sc(s)', s)
step = lambda n: pg.evaluate(f'window.__step({n}, 1000/30)')
step(20)
ev("(() => { goToDeck(3); const R = DECKS[3].rooms, key = Object.keys(R).find(k => /^Bow lounge$/.test(R[k].name || '')); const pl = DECKS[3].places.find(p => p.room === key); player.obj.position.copy(cellPos(...pl.at)); player.path.length = 0; target.copy(player.obj.position).setY(.7); })()")
ev(f"skipTo(6 * 1440 + {START})"); step(5)
LIVE = """(() => { const R = DECKS[3].rooms, inL = new Set(DECK_CREW.filter(a => a.p && a.h && (() => { const k = roomAt(Math.round(a.x + OX), Math.round(a.z + OZ)); return k && R[k] && /^Bow lounge$/.test(R[k].name || ''); })()).map(a => a.p.id));
  const T = 6 * 1440 + %d, out = { clock: clockText(), inL: inL.size, miss: [] };
  for (const p of schedPeople()) { const w = whereIs(p, T); if (!w || !/^ev-lineCeremony|^ev-crossingCeremony/.test(w.tag || '')) continue; if (inL.has(p.id)) continue;
    const seg = planDay(p, 7).find(s => s.tag === w.tag && s.from <= T && T < s.to), prev = planDay(p, 7).filter(s => s.to <= (seg ? seg.from : T)).slice(-1)[0];
    const a = DECK_CREW.find(x => x.p && x.p.id === p.id);
    out.miss.push([p.id, w.placeId, seg ? hhmm(seg.from - 6 * 1440) : null, prev ? [prev.deck, prev.placeId || prev.act, hhmm(prev.to - 6 * 1440)] : null, a ? [+(a.x + OX).toFixed(1), +(a.z + OZ).toFixed(1), a.h ? 'shown' : 'hidden'] : 'not on deck']); }
  return out; })()"""
while True:
    step(40); m = ev("shipNow() % 1440")
    if m >= 880: break
print('at 14:40', json.dumps(ev(LIVE % 880)))
while True:
    step(40); m = ev("shipNow() % 1440")
    if m >= 892: break
print('at 14:52', json.dumps(ev(LIVE % 892)))
print('errors', errs[:3])
