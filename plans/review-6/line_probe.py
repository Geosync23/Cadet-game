# PR6 line_probe: EV5's Crossing the Line L1-L3 (9188428), a copy with EVENTS_ON and EV_LINE_ON on, a real save Day 7 14:10 (evFrom 0):
#  1. on paper: who's in the bow lounge 14:35-15:10 that isn't the ceremony (the lounge is the ceremony's alone; PB's
#     evClosed find), Saruth's plan, the first-timers at the front, the cast at the lead spots;
#  2. live in the bow lounge 14:25-15:20: the horn's notice, the crowd, Marrow at the glass, ribbons, draw calls; a reload mid-oath;
#  3. 16:05 ribbons gone; 18:30 the Line supper in the mess (crowd, standing, calls); 19:30 the plaque on the promenade;
#     the certificate on Deck 4. Shots at 390x844 (and the ceremony at 360x780).
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
save = {'v': 2, 'build': 'x', 'time': {'day': 7, 'min': 850}, 'player': {'deck': 3, 'tile': [20, 10], 'facing': 0}, 'ship': {'decks': {}, 'eventLog': [], 'evFrom': 0}, 'crew': {}}
pw = sync_playwright().start()
b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
W0 = int(sys.argv[2]) if len(sys.argv) > 2 else 390; H0 = 844 if W0 == 390 else 780
ctx = b.new_context(viewport={'width': W0, 'height': H0}, has_touch=True); pg = ctx.new_page(); errs = []
pg.on('pageerror', lambda e: errs.append(str(e)))
pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
pg.add_init_script(INIT + "try { if (!sessionStorage.getItem('seeded')) { sessionStorage.setItem('seeded', '1'); localStorage.clear(); localStorage.setItem('starship-cadet-save', " + json.dumps(json.dumps(save)) + "); localStorage.setItem('starship-cadet-arrived', '1'); } } catch (e) {}")
(WORK / 'test').mkdir(parents=True, exist_ok=True)
tmp = WORK / 'test' / '_line_on.html'; tmp.write_text(instrument(pathlib.Path(path).read_text()))
pg.goto('file://' + str(tmp) + '?debug'); pg.wait_for_function('window.__sc !== undefined || window.__err', timeout=90000)
pg.add_style_tag(content='.bub{animation:none!important}')
ev = lambda s: pg.evaluate('s => window.__sc(s)', s)
step = lambda n: pg.evaluate(f'window.__step({n}, 1000/30)')
step(20); res = {}
PUT = """((deck, rx) => { if (deckDef.num !== deck) goToDeck(deck); const R = DECKS[deck].rooms, key = Object.keys(R).find(k => rx.test(R[k].name || ''));
  const pl = DECKS[deck].places.find(p => p.room === key && p.type !== 'callhome') || DECKS[deck].places.find(p => p.room === key); const c = pl.at, P = cellPos(...c), o = nearestOpen(P.x, P.z, player) || c;
  player.obj.position.copy(cellPos(...o)); player.path.length = 0; target.copy(player.obj.position).setY(.7); return [key, R[key].name]; })"""
IN = lambda rx, deck=3: """(() => { const R = DECKS[%d].rooms; return DECK_CREW.filter(a => a.p && a.h && (() => { const c = [Math.round(a.x + OX), Math.round(a.z + OZ)]; const k = roomAt(...c); return k && R[k] && %s.test(R[k].name || ''); })()); })()""" % (deck, rx)
PAPER = """(() => { const out = { stray: [], saruth: [], front: [], lead: [] }, F = lineFirst();
  for (let m = 875; m <= 910; m += 5) for (const p of schedPeople()) { const w = whereIs(p, 6 * 1440 + m); if (!w || w.deck !== 3 || !w.placeId) continue;
    const pl = (DECKS[3].places || []).find(x => x.id === w.placeId); if (!pl || pl.room !== 'L') continue;
    if (!/^ev-(lineCeremony|crossingLine)/.test(w.tag || '')) out.stray.push(hhmm(m) + ' ' + p.id + ' ' + w.placeId + ' ' + (w.tag || w.act));
    if (p.id === 'saruth') out.saruth.push(hhmm(m) + ' ' + w.placeId); }
  for (const p of schedPeople()) { const w = whereIs(p, 6 * 1440 + 890); if (!w || !w.placeId) continue;
    if (/-front|crowd-([1-9]|10)$/.test(w.placeId)) out.front.push(p.id + (F.has(p.id) ? '' : '(NOT first)'));
    if (/-lead-/.test(w.placeId)) out.lead.push(p.id + ' ' + w.placeId); }
  const sw = (() => { const q = schedPeople().find(p => p.id === "saruth"); return q ? whereIs(q, 6 * 1440 + 890) : null; })(); out.saruthAt = sw ? sw.deck + ':' + (sw.placeId || sw.act) : null;
  out.goers = schedPeople().filter(p => { const w = whereIs(p, 6 * 1440 + 890); return w && /^ev-lineCeremony/.test(w.tag || ''); }).length;
  return out; })()"""
r1 = ev(PAPER); res['paper'] = r1; print('paper', r1, flush=True)
ev("skipTo(6 * 1440 + 14 * 60 + 25)"); step(5); print('lounge', ev(PUT + "(3, /^Bow lounge$/)"), flush=True)
toasts = []
dc = []
for k in range(40):
    step(45)
    t = ev("(() => [...document.querySelectorAll('.toast, #toast, .toasts > *')].map(e => e.textContent).join(' | '))()")
    if t and t not in toasts: toasts.append(t)
    if k % 5 == 4:
        r = ev("(() => { const inL = " + IN('/^Bow lounge$/') + "; window.__skip = false; window.__step(1, 16); const mar = DECK_CREW.find(a => a.p && a.p.id === 'marrow'); return [clockText(), inL.length, inL.some(a => a.p.id === 'marrow'), inL.some(a => a.p.id === 'saruth'), mar ? [+(mar.x + OX).toFixed(1), +(mar.z + OZ).toFixed(1)] : null, DRESS.on.has('lineRibbons'), renderer.info.render.calls, SHIP.event && SHIP.event.id, (eventNow() || {}).phase]; })()")
        dc.append(r); print('  ', r, flush=True)
        if r[0].endswith('14:45') or (k == 19): pg.screenshot(path=str(OUT / f'line_ceremony_{W0}.png'), timeout=180000)
res['toasts'] = toasts[:8]; print('toasts', toasts[:8], flush=True)
res['ceremony'] = dc
# reload mid-oath: the meeting comes back (F4) and the crowd is still there
ev("skipTo(6 * 1440 + 14 * 60 + 44)"); step(30); ev("saveGame()"); pg.reload(); pg.wait_for_function('window.__sc !== undefined || window.__err', timeout=90000); step(60)
res['reload'] = ev("(() => { const inL = " + IN('/^Bow lounge$/') + "; return [clockText(), inL.length, SHIP.event && SHIP.event.id, (eventNow() || {}).phase, typeof MEET !== 'undefined' && MEET ? MEET.id || 'meet' : (typeof meetNow === 'function' ? !!meetNow() : null)]; })()"); print('reload', res['reload'], flush=True)
if W0 == 390:
    ev("skipTo(6 * 1440 + 16 * 60 + 5)"); step(30); res['ribbons1605'] = ev("DRESS.on.has('lineRibbons')"); print('ribbons 16:05', res['ribbons1605'], flush=True)
    ev("skipTo(6 * 1440 + 18 * 60 + 20)"); step(5); print('mess', ev(PUT + "(3, /^Mess hall$/)"), flush=True)
    sup = []
    for k in range(20):
        step(60)
        if k % 5 == 4:
            r = ev("(() => { const inM = " + IN('/^Mess hall$/') + "; window.__skip = false; window.__step(1, 16); return [clockText(), inM.length, renderer.info.render.calls, (galleyMenu(7) || {}).pudding || null]; })()"); sup.append(r); print('  ', r, flush=True)
    pg.screenshot(path=str(OUT / 'line_supper_390.png'), timeout=180000); res['supper'] = sup
    ev("skipTo(6 * 1440 + 19 * 60 + 40)"); step(10); print('prom', ev(PUT + "(3, /^Promenade$/)"), flush=True); step(60)
    res['plaque'] = ev("[clockText(), DRESS.on.has('linePlaque'), FEEL_S && FEEL_S.mood, renderer.info.render.calls]"); print('plaque', res['plaque'], flush=True)
    pg.screenshot(path=str(OUT / 'line_plaque_390.png'), timeout=180000)
    ev("goToDeck(4)"); step(30); res['cert'] = ev("[DRESS.on.has('lineCertificate'), SHIP.traces.map(t => t.id || t).join(',')]"); print('cert', res['cert'], flush=True)
print('RESULT', json.dumps(res)[:3000]); print('errors', errs[:5])
b.close(); pw.stop()
