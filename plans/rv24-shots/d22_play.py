# RV24: Day 22 as an arrow-following player (RV23's item 3): the Monday briefing 08:30, Calder's night word, the Tier 4 test 09:30;
# a coarse follower: jumps to where each arrow points, plays scenes (choice 0) and cards; logs the timeline. G = a Step 6 ON copy
# from RV23's mt_play.py (RV22 vb1_play.py)
import sys, os, json, re
G = sys.argv[1]; OUT = sys.argv[2]; PART = sys.argv[3] if len(sys.argv) > 3 else 'main'; os.makedirs(OUT, exist_ok=True)
exec(open(os.path.join(os.path.dirname(G), 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
src = open(G).read().replace("const EV_VESSEL_ON = URL_FLAGS.has('evvessel');", "const EV_VESSEL_ON = true;", 1)
vp = WORK / 'test' / f'_rv24_d22_{PART}.html'; vp.write_text(src)
RVHOOK = """(() => { window.__t = []; window.__b = [];
  const T = toast; toast = (a, b) => { window.__t.push(clockText() + ' ' + a + ': ' + b); return T(a, b); };
  const B = bubbleSay; bubbleSay = (w, t, s) => { try { window.__b.push(clockText() + ' ' + ((w && ((w.p && w.p.id) || w.id || w.name)) || w) + ': ' + t); } catch (e) {} return B(w, t, s); }; })()"""
def log(g, tag): pass
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
    g.page.add_init_script(INIT); html = vp.read_text(); i = html.rfind('})();'); tmp = WORK / 'test' / ('_rv24d_' + vp.name); tmp.write_text(html[:i] + "window.__sc = src => eval(src);\n" + html[i:])
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
    g.ev("devmodeRun('Set career', () => devmodeSetCareerTo(21))"); g.step(30); g.ev(RVHOOK)
    jump(g, D(22, 7, 30)); g.ev(RVHOOK)
    GO = """((g) => { if (!g || !g.deck) return null; if (deckDef.num !== g.deck) goToDeck(g.deck);
      let c = null; if (g.place) { const pl = placeById(g.place); c = pl && (pl.walk || pl.at); }
      if (!c && g.crew) { const a = DECK_CREW.find(x => x.p && x.p.id === g.crew); c = a ? cellAt(a.x, a.z) : null; }
      if (!c && g.room && ROOM_TILES[g.room]) { const t = ROOM_TILES[g.room]; c = t[Math.floor(t.length / 2)]; }
      if (!c) return 'no tile'; const P = player.obj.position, w = cellPos(...c); if (Math.hypot(P.x - w.x, P.z - w.z) < 2.5) return 'there';
      player.obj.position.copy(w); player.stop(); return 'jumped ' + c; })(goalNow())"""
    near = lambda: g.ev("(() => { const a = DECK_CREW.find(c => c.p && c.p.id === 'calder'); return a ? +Math.hypot(a.x - player.obj.position.x, a.z - player.obj.position.z).toFixed(1) : null; })()")
    last = None; lastgo = 0; took = False
    while g.ev('shipNow()') < D(22, 10, 30):
        g.step(10, 100)
        for x in g.ev("window.__t.splice(0)"): print('   toast', x)
        for x in g.ev("window.__b.splice(0)"): print('   say', x)
        if g.ev("!!DIALOGUE"):
            print(g.ev("clockText()")[-5:], 'SCENE', g.ev("DIALOGUE.id || (DIALOGUE.m && DIALOGUE.m.id)"), 'calder', near(), 'deck', g.ev("deckDef.num")); play(g, 0); continue
        if g.ev("!!(DEV.choose)"):
            print(g.ev("clockText()")[-5:], 'CARD', g.ev("DEV.choose.title || ''")); g.ev("devChosen(0)"); continue
        gl = g.ev("(() => { const x = goalNow(); return x ? [x.label, x.deck || null, x.room || x.place || x.crew || null] : null; })()")
        if gl != last: print(g.ev("clockText()")[-5:], 'GOAL', gl, 'calder', near(), 'deck', g.ev("deckDef.num")); last = gl
        if gl and gl[0] and 'take it' in gl[0] and not took:
            r = g.ev("(() => { const c = SHIP.works.cur; return c ? claimJob(c.j) : 'no cur'; })()"); took = True; print(g.ev("clockText()")[-5:], 'TAKE test', r); continue
        t = g.ev("shipNow()")
        if gl and gl[1] and t - lastgo >= 3:
            r = g.ev(GO); lastgo = t
            if r and r != 'there': print(g.ev("clockText()")[-5:], 'GO', r)
    print('end', g.ev("JSON.stringify({ m21: m21State && m21State(), t4: puT4 && puT4(), cur: SHIP.works.cur, words: [flag('p5n.on'), flag('p5n.off')] })")[:600])
    print('errors', g.errors[:5]); g.close()
