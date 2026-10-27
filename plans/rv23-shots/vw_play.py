# RV23: W6's vessel-words 0f8a2406 (everything ON): the four shortened lines where they show, at 390x844
# RV22: VB1 5578c78d at phone size, vessel switched on: the new V-2 beats in real-time play
import sys, os, json, re
G = sys.argv[1]; OUT = sys.argv[2]; PART = sys.argv[3] if len(sys.argv) > 3 else 'main'; os.makedirs(OUT, exist_ok=True)
exec(open(os.path.join(os.path.dirname(G), 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
src = open(G).read().replace("const EV_VESSEL_ON = URL_FLAGS.has('evvessel');", "const EV_VESSEL_ON = true;", 1)
vp = WORK / 'test' / f'_rv22_vb1_{PART}.html'; vp.write_text(src)
RVHOOK = """(() => { window.__t = []; window.__b = [];
  const T = toast; toast = (a, b) => { window.__t.push(clockText() + ' ' + a + ': ' + b); return T(a, b); };
  const B = bubbleSay; bubbleSay = (w, t, s) => { try { window.__b.push(clockText() + ' ' + ((w && ((w.p && w.p.id) || w.id || w.name)) || w) + ': ' + t); } catch (e) {} return B(w, t, s); }; })()"""
ST = """(() => { const g = goalNow(), e = SHIP.event; const crowd = deckDef && deckDef.num === 5 ? DECK_CREW.filter(a => roomAt(...cellAt(a.x, a.z)) === 'S').length : null;
  const near = id => { const a = DECK_CREW.find(c => c.p && c.p.id === id); return a ? Math.round(Math.hypot(a.x - player.obj.position.x, a.z - player.obj.position.z) * 10) / 10 : null; };
  return { clock: clockText(), deck: deckDef && deckDef.num, room: roomAt(...player.here()), goal: g && [g.label, g.deck, g.place || g.crew || null, g.guide || null], dlg: DIALOGUE && DIALOGUE.id,
    crowd, calder: near('calder'), taavek: near('taavek'), tern: typeof TERN !== 'undefined' ? TERN.target : null,
    mine: e && e.id === 'veyliVessel' ? Object.fromEntries(Object.entries(e.mine).filter(([k]) => /^vessel:(told|met|roundOne|home|sketch|fetch|found)|notice:ternIn/.test(k))) : null }; })()"""
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
    g.page.add_init_script(INIT); html = vp.read_text(); i = html.rfind('})();'); tmp = WORK / 'test' / ('_rv22p_' + vp.name); tmp.write_text(html[:i] + "window.__sc = src => eval(src);\n" + html[i:])
    g.page.goto('file://' + str(tmp) + '#dev'); g.page.wait_for_function('window.__sc !== undefined', timeout=120000)
    g.page.add_style_tag(content='*,*::before,*::after{transition:none!important;animation:none!important}')
    g.ev = lambda src: g.page.evaluate('s => window.__sc(s)', src)
    g.step = lambda n, dt=1000/30: g.page.evaluate(f'window.__step({n}, {dt})')
    g.shot = lambda path: g.page.screenshot(path=path)
    g.close = lambda: br.close()
    g.step(20)
    if g.page.locator('text=Sign and go aboard').count(): g.page.fill('form input', 'Ada'); g.page.click('text=Sign and go aboard'); g.step(30)
    print('dev', g.ev("typeof devmodeState === 'function' && !!devmodeState()")); g.ev(RVHOOK)
    def item_tap(js):   # a real tap on the item js finds
        xy = g.ev(f"(() => {{ const i = {js}; if (!i) return null; const v = new THREE.Vector3(); i.hit.getWorldPosition(v); v.project(camera); return [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight, i.t]; }})()")
        print('   item', xy)
        if xy and 0 < xy[0] < 390 and 0 < xy[1] < 844: g.page.mouse.click(xy[0], xy[1]); g.step(2)
        return xy
    def until_toast(rx, limit, tag, shot):   # step until a toast matching rx shows, then the screenshot at once
        g.ev("window.__t = []")
        for k in range(limit):
            g.step(2, 50)
            if g.ev(f"window.__t.some(x => {rx}.test(x))"): break
        g.step(3); g.shot(f'{OUT}/{shot}'); log(g, tag)
        print('   toast on screen', g.ev("(() => { const e = typeof toastEl !== 'undefined' ? toastEl : null; if (!e) return null; const r = e.getBoundingClientRect(); return { show: e.classList.contains('show'), text: e.textContent.slice(0, 120), box: [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)], hu: (() => { const h = document.getElementById('devHu'); return h && !h.hidden ? h.textContent.slice(0, 80) : null; })() }; })()"))
    SHEET = "ITEMS.find(i => i.vesselSheet && i.hit)"; SKETCH = "ITEMS.find(i => i.hit && /sketch/i.test(i.t || ''))"
    def stand_at(js):
        g.ev(f"(() => {{ const i = {js}; const v = new THREE.Vector3(); i.hit.getWorldPosition(v); const s = cellPos(...nearestOpen(v.x, v.z, player)); player.obj.position.set(s.x, player.obj.position.y, s.z); target.copy(player.obj.position).setY(.7); player.stop(); }})()"); g.step(15)
    g.ev("devmodeRun('Set career', () => devmodeSetCareerTo(26))"); g.step(20); g.ev(RVHOOK); g.ev("SHIP.device && SHIP.device.settings && (SHIP.device.settings.tips = false)")
    ONLY = os.environ.get('VW_ONLY') == 'shelf'
    if ONLY: jump(g, D(29, 15, 20)); deck(g, 1); until_toast('/went home on the Tern/', 600, 'home missed', 'w3_home_missed.png')
    # 1) Saturday 11:00, told: tap the sheet on the Works bay wall
    if not ONLY:
        jump(g, D(27, 11, 0)); g.ev("SHIP.event.mine['vessel:told'] = 1"); deck(g, 5); g.step(90)
        print('   sheet item', g.ev(f"!!({SHEET})"))
        if g.ev(f"!!({SHEET})"):
            stand_at(SHEET); g.ev("window.__t = []"); item_tap(SHEET); until_toast('/sign the sheet/i', 200, 'signed', 'w1_signed.png')
        # 2) Sunday: met, the round one never seen (Taavek's fetch used), on Deck 1 past 13:00
        jump(g, D(28, 12, 50)); g.ev("SHIP.event.mine['vessel:met'] = 1; SHIP.event.mine['vessel:metBy'] = 'ramp'; SHIP.event.mine['vessel:fetch:roundOne'] = 1"); deck(g, 1)
        until_toast('/round one:/', 400, 'round one missed', 'w2_roundone_missed.png')
        # 3) Monday: never at the ramp
        jump(g, D(29, 15, 20)); deck(g, 1); until_toast('/went home on the Tern/', 600, 'home missed', 'w3_home_missed.png')
    # 4) Tuesday 12:00: your bunk; the sketch onto the shelf, then tap it there
    jump(g, D(30, 11, 58)); g.ev("goToDeck(4)"); g.step(10)
    g.ev("(() => { const s = placeSpot(playerBed()); player.obj.position.set(s.x, player.obj.position.y, s.z); target.copy(player.obj.position).setY(.7); player.stop(); })()")
    until_toast('/sketch:/', 400, 'shelved', 'w4_shelved.png')
    g.step(240); g.ev("window.__t = []"); print('   sketch item', g.ev(f"(() => {{ const i = {SKETCH}; return i ? i.t : null; }})()"))
    if g.ev(f"!!({SKETCH})"): item_tap(SKETCH); until_toast('/sketch:/', 100, 'shelf tap', 'w5_shelf_tap.png')
    print('errors', g.errors[:5]); g.close()
