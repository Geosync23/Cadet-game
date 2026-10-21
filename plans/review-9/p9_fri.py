# PR9 (from PR8): turn 10's live probe on a real save (localStorage), phone 390x844 (PR5's fr6_speech.py harness).
#  d5:  Day 5 from 15:12 at work: the 15:20 heads-up, the clock words, the auditorium 15:58-16:10 (Marrow, Vance, lines,
#       shots), then 16:50 (heard, no dip, no Mail), then the mess 17:00-17:50 (diners over time, a shot at 17:20)
#  up:  an old save (no fri part, as the published game writes it) loaded on a Friday evening after the address
#  d12: Day 12 (the storm Friday) in the auditorium: which lines are said, who's at the lectern
# usage: p8_fri.py BUILD TAG SCENARIO [DAY MIN]
import os, sys, json, re, pathlib
H = '/tmp/claude-0/-home-user-Cadet-game/c90be8f5-63df-55cd-b247-474233586f38/scratchpad/wt_comb'
exec(open(H + '/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
path, tag, sc = sys.argv[1], sys.argv[2], sys.argv[3]
OUT = pathlib.Path('/home/user/Cadet-game/plans/review-9/shots'); OUT.mkdir(parents=True, exist_ok=True)
day0 = int(sys.argv[4]) if len(sys.argv) > 4 else {'d5': 5, 'up': 5, 'd12': 12, 'skip': 19}[sc]
min0 = int(sys.argv[5]) if len(sys.argv) > 5 else {'d5': 15 * 60 + 12, 'up': 18 * 60, 'd12': 15 * 60 + 56, 'skip': 15 * 60}[sc]
save = {'v': 2, 'build': 'x', 'time': {'day': day0, 'min': min0}, 'player': {'deck': 4, 'tile': [20, 4], 'facing': 0}, 'ship': {'decks': {}, 'eventLog': []}, 'crew': {}}
pw = sync_playwright().start()
b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
ctx = b.new_context(viewport={'width': 390, 'height': 844}, has_touch=True); pg = ctx.new_page(); errs = []
pg.on('pageerror', lambda e: errs.append(str(e)))
pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
pg.add_init_script(INIT + "try { if (!sessionStorage.getItem('seeded')) { sessionStorage.setItem('seeded', '1'); localStorage.clear(); localStorage.setItem('starship-cadet-save', " + json.dumps(json.dumps(save)) + "); localStorage.setItem('starship-cadet-arrived', '1'); } } catch (e) {}")
(WORK / 'test').mkdir(parents=True, exist_ok=True)
tmp = WORK / 'test' / ('_r8_' + tag + '.html'); tmp.write_text(instrument(pathlib.Path(path).read_text()))
def load():
    pg.goto('file://' + str(tmp) + '?debug', timeout=240000); pg.wait_for_function('window.__sc !== undefined || window.__err', timeout=240000)
    pg.add_style_tag(content='.bub{animation:none!important}')
ev = lambda s: pg.evaluate('s => window.__sc(s)', s)
step = lambda n: pg.evaluate(f'window.__step({n}, 1000/30)')
mm = lambda: ev("Math.floor(shipNow() % 1440)")
TOASTS = "window.__toasts = []; { const t0 = toast; toast = (t, x) => { window.__toasts.push([t, x, clockText()]); return t0(t, x); }; }"
SEAT = """(() => { if (deckDef.num !== 7) goToDeck(7); const M = DECKS[7].map, c = []; for (let j = 0; j < M.length; j++) for (let i = 0; i < M[j].length; i++) if (M[j][i] === 'A') c.push([i, j]);
  const t = cellPos(...c[Math.floor(c.length / 2)]); player.obj.position.set(t.x, 0, t.z); player.path.length = 0; target.copy(player.obj.position).setY(.7); return c[Math.floor(c.length / 2)]; })()"""
BUB = """(() => bubbles.list.map(b => { const r = b.card.getBoundingClientRect(), w = b.who; return { who: (bubblePerson(w) || {}).id, stand: !!(w.H), shown: b.el.style.display !== 'none',
  top: Math.round(r.top), bot: Math.round(r.bottom), left: Math.round(r.left), right: Math.round(r.right), t: b.text.slice(0, 60) }; }))()"""
CNT = "(() => { const l = DECKS[7].places.find(p => p.type === 'rec:lectern'), L = cellPos(...l.at); let s = 0, lec = []; for (const a of DECK_CREW) { const dd = Math.hypot(a.x - L.x, a.z - L.z); if (dd < 12 && /sit/.test(a.pose || '')) s++; if (dd < 2.5 && a.p) lec.push(a.p.id); } return [clockText(), s, lec.sort(), FRI_SAID && FRI_SAID[1]]; })()"
REP = "(() => { const R = SHIP.rep; return R ? { work: R.ship.work, address: R.cnt.address || 0 } : null; })()"
MESS = "(() => { if (deckDef.num !== 3) return null; let inM = 0, sit = 0; for (const a of DECK_CREW) { if (!a.p) continue; const t = [Math.round(a.x), Math.round(a.z)]; let r = null; try { r = roomAt(...t); } catch (e) {} if (r === 'M') { inM++; if (/sit/.test(a.pose || '')) sit++; } } return [clockText(), inM, sit]; })()"
res = {'sc': sc, 'build': path}
load(); step(20); print('loaded', ev("clockText()"), 'SHORT_FRIDAY', ev("SHORT_FRIDAY"), 'EVENTS_ON', ev("EVENTS_ON"), flush=True)
ev(TOASTS)
if sc == 'd5':
    res['rep0'] = ev(REP)
    while mm() < 15 * 60 + 24: step(20)
    res['headsup'] = ev("window.__toasts.slice()"); res['hu'] = ev("FRI.hu"); print('heads-up', res['headsup'], flush=True)
    pg.screenshot(path=str(OUT / (tag + '_d5_1524.png')))
    res['clock'] = ev("[typeof friClock === 'function' && friClock('onshift', dayShiftEnd(5)), typeof friClock === 'function' && friClock('didout', dayShiftEnd(5)), dayShiftEnd(5)]"); print('clock words', res['clock'], flush=True)
    ev("skipTo(4 * 1440 + 15 * 60 + 56)"); step(5); print('seat', ev(SEAT)); step(10)
    log = []; shot = {}
    while True:
        step(20); c = ev(CNT); m = mm(); log.append(c)
        if m >= 965 and 'a' not in shot: shot['a'] = 1; pg.screenshot(path=str(OUT / (tag + '_d5_1605.png'))); res['A_1605'] = [c, ev(BUB)]
        if m >= 970: break
    res['fill'] = log[::8]; print('fill', res['fill'], flush=True); print('16:05', json.dumps(res.get('A_1605')), flush=True)
    res['speech'] = ev("friSpeech(5).map(l => l.who + ': ' + l.text)")
    ev("skipTo(4 * 1440 + 16 * 60 + 47)"); step(5)
    while mm() < 16 * 60 + 53: step(20)
    res['after'] = [ev("[FRI.heard, FRI.mailed]"), ev(REP), ev("window.__toasts.slice()"), ev("SHIP.mail.filter(m => m.at > 4 * 1440 + 900).map(m => [m.at % 1440, m.from, m.subject])")]
    print('after 16:50 [heard, mailed], rep, toasts, mail', json.dumps(res['after']), flush=True)
    ev("goToDeck(3)"); ev("skipTo(4 * 1440 + 16 * 60 + 58)"); step(5); ml = []
    while mm() < 17 * 60 + 52:
        step(20); x = ev(MESS); m = mm()
        if len(ml) == 0 or m - ml[-1][0] >= 4: ml.append([m, x]); print('mess', x, flush=True)
        if m >= 1040 and 'm' not in shot: shot['m'] = 1; pg.screenshot(path=str(OUT / (tag + '_d5_1720.png')))
    res['mess'] = ml
    res['diners'] = ev("(() => { const S = schedData(), o = []; for (const p of ROSTER) { const pl = planDay(p, 5); const dn = pl.find(s => s.act === 'meal' && s.from >= 990 && s.from < 1200); if (dn) o.push(dn.from); } o.sort((a, b) => a - b); const h = {}; for (const x of o) { const k = Math.floor(x / 10) * 10; h[hhmm(k)] = (h[hhmm(k)] || 0) + 1; } return h; })()")
    print('dinner starts by 10 min', res['diners'], flush=True)
elif sc == 'up':
    step(30)
    for k in range(30): step(20)
    res['after'] = [ev("clockText()"), ev("[FRI.heard, FRI.mailed]"), ev(REP), ev("window.__toasts.slice()"), ev("(SHIP.mail || []).filter(m => m.at > (SHIP.time.day - 1) * 1440 + 900).map(m => [m.at % 1440, m.from, m.subject])")]
    print('old save loaded on a Friday evening: clock, [heard, mailed], rep, toasts, mail', json.dumps(res['after']), flush=True)
    pg.screenshot(path=str(OUT / (tag + '_up.png')))
elif sc == 'd12':
    print('seat', ev(SEAT)); step(10); log = []
    while mm() < 16 * 60 + 30:
        step(20); c = ev(CNT); log.append(c)
    res['fill'] = log[::10]; print('fill', res['fill'], flush=True)
    res['speech'] = ev("(friSpeech(%d) || []).map(l => l.who + ': ' + l.text)" % day0)
    res['said'] = ev("FRI_SAID"); res['bub'] = ev(BUB); pg.screenshot(path=str(OUT / (tag + '_d%d_1630.png' % day0)))
    res['storm'] = ev("[typeof eventBandOf === 'function', typeof eventOn === 'function' ? eventOn('ionStorm') : null, eventsOn(%d).map(e => e.id + ' ' + hhmm(e.from %% 1440) + '-' + hhmm(e.to %% 1440))]" % day0)
    print('speech', json.dumps(res['speech'], indent=0), flush=True); print('said', res['said'], 'bubbles', res['bub'], 'storm', res['storm'], flush=True)
elif sc == 'skip':
    # PR5's C2 with the game's own sleep (sleepUntil), then one jump across two Fridays (as Dev's clock could)
    MAILS = "(a, b) => (SHIP.mail || []).filter(m => m.at >= a && m.at < b && /Captain/.test(m.from || '')).map(m => [Math.floor(m.at / 1440) + 1, hhmm(m.at % 1440), m.subject])"
    w0 = ev(REP); ev("sleepUntil(7 * 60)"); step(10)
    res['sleep'] = [w0, ev("clockText()"), ev("[FRI.heard, FRI.mailed]"), ev(REP), ev("window.__toasts.filter(x => /missed/i.test(x[1] || ''))"), ev("(" + MAILS + ")(%d, %d)" % ((day0 - 1) * 1440, (day0 + 1) * 1440))]
    print('sleep from Friday %d %s: rep0, clock, [heard, mailed], rep, banners, Mails' % (day0, min0), json.dumps(res['sleep']), flush=True)
    ev("window.__toasts = []"); w1 = ev(REP); ev("skipTo((%d - 1) * 1440 + 900)" % (day0 + 7)); step(3); ev("skipTo((%d - 1) * 1440 + 420)" % (day0 + 15)); step(10)
    res['two'] = [w1, ev("clockText()"), ev("[FRI.heard, FRI.mailed]"), ev(REP), ev("window.__toasts.filter(x => /missed/i.test(x[1] || '')).length"), ev("(" + MAILS + ")(%d, %d)" % ((day0 + 6) * 1440, (day0 + 15) * 1440))]
    print('one jump across Fridays %d and %d: rep0, clock, [heard, mailed], rep, banners, Mails' % (day0 + 7, day0 + 14), json.dumps(res['two']), flush=True)
res['errors'] = errs[:5]; print('errors', errs[:5])
json.dump(res, open(OUT / (tag + '_res.json'), 'w'), indent=1)
