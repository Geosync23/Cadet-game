# RV23: N6's nights (S6-1 turn 3, c806c78) on a Step 6 ON copy at 390x844: Calder's night.on in person, the notice, arrows and rings to the clock
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
    g.ev("SHIP.device && SHIP.device.settings && (SHIP.device.settings.tips = false)")
    g.ev("devmodeRun('Set career', () => devmodeSetCareerTo(21))"); g.step(20); g.ev(RVHOOK)
    near = lambda: g.ev("(() => { const a = DECK_CREW.find(c => c.p && c.p.id === 'calder'); return a ? +Math.hypot(a.x - player.obj.position.x, a.z - player.obj.position.z).toFixed(1) : null; })()")
    jump(g, D(22, 9, 12)); deck(g, 3, "'3-lounge-24'"); log(g, 'mon0912')
    tr = []
    while g.ev('shipNow()') < D(22, 10, 5):
        g.step(20, 100); tr.append((g.ev("hhmm(shipNow() % 1440)"), near()))
        if g.ev("!!DIALOGUE"): break
    print('trail', tr[::5], tr[-2:]); log(g, 'night.on?'); g.shot(f'{OUT}/n1_night_on.png')
    if g.ev("!!DIALOGUE"): print('scene', g.ev("DIALOGUE.m && DIALOGUE.m.id"), 'at', near()); play(g, 1); log(g, 'after')
    print('sched', g.ev("JSON.stringify((typeof devDay === 'function' ? devDay(22) : []).map(x => hhmm(x.from) + ' ' + x.title))")[:600])
    jump(g, D(22, 22, 25)); deck(g, 3, "'3-lounge-24'")
    run(g, D(22, 22, 44), every=20, tag='mon2244 (notice, arrow to the clock?)'); g.shot(f'{OUT}/n2_clock_arrow.png')
    print('ring', g.ev("(() => { const q = typeof POINT_Q !== 'undefined' ? POINT_Q.filter(x => /night|clock|p5n/i.test(x.id)).map(x => x.id + (x.force ? ' forced' : '')) : null; const e = GUIDE.list.filter(x => /p5n|night|clock/i.test(x.id)).map(x => x.id + ' L' + x.level); return { q, e }; })()"))
    # clock in at the time clock (stand there, the clock's own call), then the engine room arrow
    g.ev("goToDeck(5)"); g.step(10); g.ev("(() => { const s = placeSpot('5-timeclock-1'); player.obj.position.set(s.x, player.obj.position.y, s.z); player.stop(); })()"); g.step(10)
    print('clock', g.ev("careerClock(shipNow(), true)")); run(g, D(22, 22, 52), every=20, tag='after clock-in (engine room arrow?)'); g.shot(f'{OUT}/n3_after_in.png')
    jump(g, D(23, 5, 50)); run(g, D(23, 6, 3), every=20, tag='tue0603 (the clock again?)'); g.shot(f'{OUT}/n4_morning.png')
    print('errors', g.errors[:5]); g.close()
