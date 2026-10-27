# RV24: DA6 abf496f3: the framed keepsakes (menu, Line certificate, Taavek's sketch) in Deck 2's room B once it's yours, at 390x844; G = a Step 6 ON copy
# from RV23's mt_play.py (RV22 vb1_play.py)
import sys, os, json, re
G = sys.argv[1]; OUT = sys.argv[2]; PART = sys.argv[3] if len(sys.argv) > 3 else 'main'; os.makedirs(OUT, exist_ok=True)
exec(open(os.path.join(os.path.dirname(G), 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
src = open(G).read().replace("const EV_VESSEL_ON = URL_FLAGS.has('evvessel');", "const EV_VESSEL_ON = true;", 1)
vp = WORK / 'test' / f'_rv24_d2b_{PART}.html'; vp.write_text(src)
RVHOOK = """(() => { window.__t = []; window.__b = [];
  const T = toast; toast = (a, b) => { window.__t.push(clockText() + ' ' + a + ': ' + b); return T(a, b); };
  const B = bubbleSay; bubbleSay = (w, t, s) => { try { window.__b.push(clockText() + ' ' + ((w && ((w.p && w.p.id) || w.id || w.name)) || w) + ': ' + t); } catch (e) {} return B(w, t, s); }; })()"""
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
    g.page.add_init_script(INIT); html = vp.read_text(); i = html.rfind('})();'); tmp = WORK / 'test' / ('_rv24k_' + vp.name); tmp.write_text(html[:i] + "window.__sc = src => eval(src);\n" + html[i:])
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
    out = g.ev("""(() => { const W = worksInit(); W.tier = 4; W.rank = 'specialist'; W.home = '2-B'; goToDeck(2);
      const ids = ['framedMenu', 'lineCertificate', 'vesselSketchShelf']; dressShow(ids);
      const t = ROOM_TILES['B']; const c = t[Math.floor(t.length / 2)]; player.obj.position.copy(cellPos(...c)); player.stop();
      return { mine: deck2Mine(), decks: ids.map(i => [i, DECK_DRESS[i] && DECK_DRESS[i].deck, DECK_DRESS[i] && (!DECK_DRESS[i].on || DECK_DRESS[i].on())]), on: [...DRESS.on.keys()], items: ITEMS.filter(i => /Framed menu|Line certificate|sketch/i.test(i.t)).map(i => i.t), calls: renderer.info.render.calls }; })()""")
    g.step(30); print('room B', json.dumps(out)); g.shot(f'{OUT}/d2b_room.png')
    g.ev("(() => { const t = ROOM_TILES['B']; const c = t.slice().sort((a, b) => a[0] - b[0])[0]; player.obj.position.copy(cellPos(c[0] + 1, c[1])); player.stop(); })()"); g.step(30); g.shot(f'{OUT}/d2b_west.png')
    print('errors', g.errors[:5]); g.close()
