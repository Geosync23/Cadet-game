# RV23 (from RV22's): VB1 705c6fc5, the fetch now 12:30
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
    if PART == 'main':
        g.ev("devmodeRun('Set career', () => devmodeSetCareerTo(26))"); g.step(20)
        jump(g, D(27, 9, 50)); deck(g, 3, "'3-lounge-24'"); log(g, 'sat0950 deck3')
        run(g, D(27, 10, 14), tag='sat1014 (Calder fetch 1?)'); g.shot(f'{OUT}/a1_sat1014_calder_finds_you.png')
        jump(g, D(27, 11, 25)); deck(g, 3, "'3-lounge-24'"); run(g, D(27, 11, 44), tag='sat1144 (Calder fetch 2?)'); g.shot(f'{OUT}/a2_sat1144_calder_again.png')
        # sign: go to Calder in the Works bay
        g.ev("goToDeck(5)"); g.step(10)
        g.ev("(() => { const a = DECK_CREW.find(c => c.p && c.p.id === 'calder'); if (a) { player.obj.position.set(a.x + 1, player.obj.position.y, a.z); player.stop(); } })()")
        run(g, D(27, 11, 50), every=3, stop="!!DIALOGUE", tag='sat sign scene'); g.shot(f'{OUT}/a3_sat_sheet_scene.png'); play(g); log(g, 'after sheet')
        # Sunday: at the ramp's foot from 09:15
        jump(g, D(28, 9, 15)); deck(g, 5, 'ROT_TERN_FOOT'); log(g, 'sun0915 foot')
        for m in (20, 25, 30, 33):
            run(g, D(28, 9, m), every=6, tag=f'sun09{m}')
            if m == 30: g.shot(f'{OUT}/b1_sun0930_crowd.png')
        run(g, D(28, 9, 45), every=3, stop="!!DIALOGUE", tag='ramp scene?'); g.shot(f'{OUT}/b2_sun_ramp_scene.png'); play(g); log(g, 'after ramp')
        # away from the bench until Taavek comes to find you at 12:45
        jump(g, D(28, 12, 20)); deck(g, 3, "'3-lounge-24'"); log(g, 'sun1220 deck3 (arrow: the round one, not the sheet)')
        run(g, D(28, 12, 29), tag='sun1229'); g.shot(f'{OUT}/b3a_sun1229_arrow.png')
        run(g, D(28, 12, 59), every=6, stop="!!DIALOGUE", tag='sun round-one fetch'); g.shot(f'{OUT}/b3_sun_taavek_finds_you.png')
        if g.ev("!!DIALOGUE"): play(g)
        run(g, D(28, 13, 3), tag='sun1303')
        # Monday: away at 14:25, the notice and arrow at 14:30, Calder at 15:00
        jump(g, D(29, 14, 25)); deck(g, 3, "'3-lounge-24'"); log(g, 'mon1425')
        run(g, D(29, 14, 32), tag='mon1432 (notice + arrow at the ramp foot?)'); g.shot(f'{OUT}/c1_mon1432_home_arrow.png')
        run(g, D(29, 15, 6), tag='mon1506 (Calder fetch?)'); g.shot(f'{OUT}/c2_mon1506_calder_finds_you.png')
        deck(g, 5, 'ROT_TERN_FOOT'); run(g, D(29, 15, 20), every=3, stop="!!DIALOGUE", tag='home scene?'); g.shot(f'{OUT}/c3_mon_home_scene.png'); play(g)
        for m in (5, 10, 15): run(g, g.ev('shipNow()') + m, tag=f'after home +{m}')
        g.shot(f'{OUT}/c4_mon_tern_leaves.png')
    else:   # the misses: Monday, never going to the ramp
        g.ev("devmodeRun('Set career', () => devmodeSetCareerTo(28))"); g.step(20); g.ev(RVHOOK)
        jump(g, D(29, 14, 20)); deck(g, 1); log(g, 'mon1420 deck1')
        run(g, D(29, 15, 35), every=10, tag='mon1535 (missed?)')
        run(g, D(29, 16, 5), tag='mon1605'); g.shot(f'{OUT}/d1_mon_missed.png')
    print('errors', g.errors[:5]); g.close()
