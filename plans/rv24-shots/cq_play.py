# RV24: W8 S6-9 (bd138090): Calder's question live at 390x844 from Dev mode's Day 26 cq preset (Four weeks aboard tea); G = a Step 6 ON copy
# from RV23's mt_play.py (RV22 vb1_play.py)
import sys, os, json, re
G = sys.argv[1]; OUT = sys.argv[2]; PART = sys.argv[3] if len(sys.argv) > 3 else 'main'; os.makedirs(OUT, exist_ok=True)
exec(open(os.path.join(os.path.dirname(G), 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
src = open(G).read().replace("const EV_VESSEL_ON = URL_FLAGS.has('evvessel');", "const EV_VESSEL_ON = true;", 1)
vp = WORK / 'test' / f'_rv24_cq_{PART}.html'; vp.write_text(src)
RVHOOK = """(() => { window.__t = []; window.__b = [];
  const T = toast; toast = (a, b) => { window.__t.push(clockText() + ' ' + a + ': ' + b); return T(a, b); };
  const B = bubbleSay; bubbleSay = (w, t, s) => { try { window.__b.push(clockText() + ' ' + ((w && ((w.p && w.p.id) || w.id || w.name)) || w) + ': ' + t); } catch (e) {} return B(w, t, s); }; })()"""
ST = """(() => { const g = goalNow(); const pos = id => { const a = DECK_CREW.find(c => c.p && c.p.id === id); return a ? Math.round(Math.hypot(a.x - player.obj.position.x, a.z - player.obj.position.z) * 10) / 10 : null; };
  const seat = id => { const pl = placeById(id); if (!pl) return null; const c = placeSpot(id); const on = DECK_CREW.filter(a => a.p && Math.hypot(a.x - c.x, a.z - c.z) < 0.5).map(a => a.p.id); return (BUSY.has(id) ? 'B ' : '') + (PLAYER_PLACE === id ? 'YOU ' : '') + on.join(','); };
  const tea = DECK_CREW.filter(a => a.p && deckDef.num === 5 && roomAt(...cellAt(a.x, a.z)) === 't').map(a => a.p.id);
  return { clock: clockText(), deck: deckDef && deckDef.num, room: roomAt(...player.here()), place: PLAYER_PLACE, goal: g && [g.label, g.place || g.crew || null], dlg: DIALOGUE && DIALOGUE.id,
    calder: pos('calder'), s1: seat('5-tea-1'), s2: seat('5-tea-2'), s3: seat('5-tea-3'), tea, cq: (typeof cqOf === 'function' && JSON.stringify(cqOf())), come: COME_TO.has('calder') ? COME_TO.get('calder').placeId : null, ev: SHIP.event && SHIP.event.id }; })()"""
def log(g, tag):
    s = g.ev(ST); t = g.ev("window.__t.splice(0)"); b = g.ev("window.__b.splice(0)")
    print(tag, json.dumps(s)); [print('   toast', x) for x in t]; [print('   say', x) for x in b]; return s
def run(g, until, every=10, tag=None, stop=None):
    while g.ev('shipNow()') < until:
        g.step(every, 50)
        if stop and g.ev(stop): break
    if tag: log(g, tag)
def jump(g, abs): g.ev(f"devmodeSkipTo({abs}); for (const k of NEED_KEYS) SHIP.player.needs[k] = Math.max(SHIP.player.needs[k], 85)"); g.step(10)
def deck(g, n, place=None):
    g.ev(f"goToDeck({n})"); g.step(10)
    if place: g.ev(f"(() => {{ const s = placeSpot({place}); player.obj.position.set(s.x, player.obj.position.y, s.z); player.stop(); }})()"); g.step(5)
def play(g, pick=1):
    n = 0; lines = []
    while g.ev("!!DIALOGUE") and n < 60:
        v = g.ev("(() => { const v = dialogueView(); return v ? { who: v.who || v.name || null, text: v.text || null, ch: !!v.choices } : null; })()")
        if v: lines.append(v)
        g.ev(f"(() => {{ const v = dialogueView(); if (v && v.choices) dialogueChoose({pick}); else dialogueNext(); }})()"); g.step(2); n += 1
    print('   dialogue', len(lines), 'panels'); return lines
D = lambda d, h, m: (d - 1) * 1440 + h * 60 + m
with sync_playwright() as pw:
    class P: pass
    g = P(); br = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    g.page = br.new_page(viewport={'width': 390, 'height': 844}); g.errors = []
    g.page.on('pageerror', lambda e: g.errors.append(str(e)))
    g.page.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    g.page.add_init_script(INIT); html = vp.read_text(); i = html.rfind('})();'); tmp = WORK / 'test' / ('_rv24p_' + vp.name); tmp.write_text(html[:i] + "window.__sc = src => eval(src);\n" + html[i:])
    g.page.goto('file://' + str(tmp) + '#dev'); g.page.wait_for_function('window.__sc !== undefined', timeout=120000)
    g.page.add_style_tag(content='*,*::before,*::after{transition:none!important;animation:none!important}')
    g.ev = lambda src: g.page.evaluate('s => window.__sc(s)', src)
    g.step = lambda n, dt=1000/30: g.page.evaluate(f'window.__step({n}, {dt})')
    g.shot = lambda path: g.page.screenshot(path=path)
    g.close = lambda: br.close()
    g.step(20)
    if g.page.locator('text=Sign and go aboard').count(): g.page.fill('form input', 'Ada'); g.page.click('text=Sign and go aboard'); g.step(30)
    print('dev', g.ev("typeof devmodeState === 'function' && !!devmodeState()")); g.ev(RVHOOK)
    g.ev("SHIP.device && SHIP.device.settings && (SHIP.device.settings.tips = false)")
    g.ev("devmodeRun('Set career', () => devmodeSetCareer(26, DM_BEATS.find(b => b.id === 'cq')))"); g.step(30); g.ev(RVHOOK)
    log(g, 'start'); g.shot(f'{OUT}/cq0_start.png')
    print('works', g.ev("JSON.stringify({ tier: SHIP.works.tier, rank: SHIP.works.rank, end: SHIP.works.end })"))
    print('rows', g.ev("JSON.stringify(typeof cqItems === 'function' ? cqItems(26) : null)"))
    if PART == 'sit': SIT = True
    else: SIT = False
    if PART != 'miss':   # walk into the tea corner (from the Works bay side) at 18:38
        run(g, D(26, 18, 38), 10)
        g.ev("(() => { if (deckDef.num !== 5) goToDeck(5); player.obj.position.copy(cellPos(...ROOM_TILES['t'][0])); player.stop(); })()"); g.step(10)
    if PART == 'miss': deck(g, 3, "'3-lounge-24'")
    k = 0; last = None
    while g.ev('shipNow()') < D(26, 20, 0) and k < 8:
        g.step(15, 100)
        if g.ev("!!DIALOGUE"):
            k += 1; log(g, f'scene {k}'); g.shot(f'{OUT}/cq{k}_scene_{PART}.png'); play(g, 0); g.step(5); log(g, f'after scene {k}')
        if SIT and g.ev("(() => { const x = goalNow(); return !!(x && /Sit with Calder/.test(x.label)); })()") and not g.ev("!!ACT"):
            seat = g.ev("goalNow().place"); print('sitting at', seat, g.ev("clockText()")); g.ev(f"actStart('sit', '{seat}', {{ title: 'Tea corner seat' }})")
        mn = g.ev("Math.floor(shipNow() % 1440)")
        if mn != last and mn % 3 == 0: last = mn; log(g, ' ')
        if mn in (1146, 1150) and not g.ev("!!DIALOGUE"): g.shot(f'{OUT}/cq_seat_{mn}_{PART}.png')
        if g.ev("!!(cqOf() && cqOf().answer)"): break
    log(g, 'end'); g.shot(f'{OUT}/cq_end_{PART}.png')
    print('record', g.ev("worksRecordHead().text.slice(-200)"))
    print('mail', g.ev("SHIP.mail.filter(m => /What you said|Four weeks/.test(m.subject)).map(m => m.from + ': ' + m.subject)"))
    print('errors', g.errors[:5]); g.close()
