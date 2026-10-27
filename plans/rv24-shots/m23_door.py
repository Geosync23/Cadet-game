# RV24: DA6 S6-5 night 2 (88377cfa/31ad2f0e): the reactor's shielded door and the arrows at 390x844, step by step; G = a Step 6 ON copy
# from RV23's mt_play.py (RV22 vb1_play.py)
import sys, os, json, re
G = sys.argv[1]; OUT = sys.argv[2]; PART = sys.argv[3] if len(sys.argv) > 3 else 'main'; os.makedirs(OUT, exist_ok=True)
exec(open(os.path.join(os.path.dirname(G), 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
src = open(G).read().replace("const EV_VESSEL_ON = URL_FLAGS.has('evvessel');", "const EV_VESSEL_ON = true;", 1)
vp = WORK / 'test' / f'_rv24_m23_{PART}.html'; vp.write_text(src)
RVHOOK = """(() => { window.__t = []; window.__b = [];
  const T = toast; toast = (a, b) => { window.__t.push(clockText() + ' ' + a + ': ' + b); return T(a, b); };
  const B = bubbleSay; bubbleSay = (w, t, s) => { try { window.__b.push(clockText() + ' ' + ((w && ((w.p && w.p.id) || w.id || w.name)) || w) + ': ' + t); } catch (e) {} return B(w, t, s); }; })()"""
P6 = r"""((d, at, deck) => { skipTo((d - 1) * 1440 + at); machinesNow(); if (DIALOGUE) dialogueEnd(true); const W = worksInit(); W.tier = 4; W.rank = 'specialist';
  for (const r of CAREER_LADDER) if (r.id !== 'm23') { W.tr[r.id] = 1; W.use[r.id] = 9; }
  for (const k of NEED_KEYS) SHIP.player.needs[k] = 90; worksCareerTick(shipNow()); goToDeck(deck); player.stop(); return true; })"""   # controller_check's P6_M23
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
    g.page.add_init_script(INIT); html = vp.read_text(); i = html.rfind('})();'); tmp = WORK / 'test' / ('_rv24m_' + vp.name); tmp.write_text(html[:i] + "window.__sc = src => eval(src);\n" + html[i:])
    g.page.goto('file://' + str(tmp) + '#dev'); g.page.wait_for_function('window.__sc !== undefined', timeout=120000)
    g.page.add_style_tag(content='*,*::before,*::after{transition:none!important;animation:none!important}')
    g.ev = lambda src: g.page.evaluate('s => window.__sc(s)', src)
    g.step = lambda n, dt=1000/30: g.page.evaluate(f'window.__step({n}, {dt})')
    g.shot = lambda path: g.page.screenshot(path=path)
    g.close = lambda: br.close()
    g.step(20)
    if g.page.locator('text=Sign and go aboard').count(): g.page.fill('form input', 'Ada'); g.page.click('text=Sign and go aboard'); g.step(30)
    g.step(20)
    if g.page.locator('text=Sign and go aboard').count(): g.page.fill('form input', 'Ada'); g.page.click('text=Sign and go aboard'); g.step(30)
    g.ev(RVHOOK); g.ev("SHIP.device && SHIP.device.settings && (SHIP.device.settings.tips = false)")
    g.ev(P6 + "(23, 1262, 6)"); g.step(30)
    PROBE = """(() => { const pp = placeById(panelPlace('6-reactor-1')), w = pp.walk || pp.at, t = shipNow();
      const path = findPath([23, 6], w, null, 'player'); const gl = goalNow();
      return { clock: clockText(), step: m23Night2Step(m23State()), door: doorOpenFor('R', 'player', t, 6), path: path ? path.length : null, goal: gl && [gl.label, gl.deck, gl.room || null, gl.place || null], card: DEV.choose ? (DEV.choose.title || true) : null, badge: dosiOut() }; })()"""
    def st(tag): r = g.ev(PROBE); print(tag, json.dumps(r)); [print('   toast', x) for x in g.ev("window.__t.splice(0)")]; return r
    def card():
        for q in range(30):
            if g.ev("!!DEV.choose"): break
            g.step(10)
        return g.ev("DEV.choose ? (devChosen(0), true) : false")
    r0 = st('start (deck 6, nothing yet)')
    g.ev("(() => { goToDeck(1); const t = []; DECKS[1].map.forEach((row, j) => { for (let i = 0; i < row.length; i++) if (row[i] === 'B') t.push([i, j]); }); player.obj.position.copy(cellPos(...t[Math.floor(t.length / 2)])); player.stop(); })()"); g.step(30)
    g.shot(f'{OUT}/m23_permit_card.png'); print('permit card', card()); g.step(10); r1 = st('permit signed')
    g.ev("(() => { goToDeck(6); player.obj.position.copy(cellPos(23, 6)); player.stop(); })()"); g.step(30); g.shot(f'{OUT}/m23_badge_arrow.png'); r1b = st('on deck 6, before the badge')
    g.ev("dosiUse()"); g.step(10); r2 = st('badge taken'); g.shot(f'{OUT}/m23_tell_card.png'); print('tell card', card()); g.step(10)
    r3 = st('the Watch told'); g.shot(f'{OUT}/m23_reactor_arrow.png')
    g.ev("(() => { const S = m23State(), j = SHIP.jobs.find(x => x.id === S.j2); j.workDone = true; })()"); g.step(10)
    g.ev("(() => { const pp = placeById(panelPlace('6-reactor-1')), w = pp.walk || pp.at; player.obj.position.copy(cellPos(...w)); player.stop(); })()"); g.step(10)
    print('out card', card()); g.step(10); r4 = st('out, still inside'); g.shot(f'{OUT}/m23_out_inside.png')
    g.ev("(() => { player.obj.position.copy(cellPos(23, 6)); player.stop(); })()"); g.step(10); r5 = st('out, outside (badge still on)')
    g.ev("setShipNow(m23State().out + 31)"); g.step(20); r6 = st('31 min later, badge not back')
    g.ev("dosiUse()"); g.step(20); r7 = st('badge back'); print('done', g.ev("[m23State().d2 > 0, SHIP.works.tr.m23]"))
    ok = [r0['door'] is False and r0['path'] is None, r1['step'] == 'badge', r2['door'] is False, r3['door'] is True and r3['path'], r4['door'] is True, r5['door'] is False and r5['path'] is None]
    print('door gate', ok); print('errors', g.errors[:5]); g.close()
