# RV23: B3's talk-close (f52e2abc) at phone size: a tap from afar shows the card with Walk over; walking over, they wait;
# up close the talk card; a near tap opens it at once; the "would like a word" chip the same. Run from the game's folder.
import sys, os, json, re
G = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
exec(open(os.path.join(os.path.dirname(G), 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
vp = WORK / 'test' / '_rv23_talk.html'; vp.write_text(open(G).read())
D = lambda d, h, m: (d - 1) * 1440 + h * 60 + m
CARD = """(() => { const el = document.getElementById('chat'); const vis = el && !el.hidden && el.offsetWidth > 0; const r = vis ? el.getBoundingClientRect() : null;
  return { chat: CHAT ? { p: CHAT.p.id, far: !!CHAT.far, walking: !!CHAT.walking, line: CHAT.line && CHAT.line.text } : null, vis, box: r && [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)],
    buttons: vis ? [...el.querySelectorAll('button')].map(b => b.textContent + (b.disabled ? '(off)' : '')) : [] }; })()"""
def dist(g, id): return g.ev(f"(() => {{ const a = DECK_CREW.find(c => c.p && c.p.id === '{id}'); return a ? +Math.hypot(a.x - player.obj.position.x, a.z - player.obj.position.z).toFixed(2) : null; }})()")
def apos(g, id): return g.ev(f"(() => {{ const a = DECK_CREW.find(c => c.p && c.p.id === '{id}'); return a ? [+a.x.toFixed(2), +a.z.toFixed(2)] : null; }})()")
def tap_on(g, id):   # a real tap at their screen position
    xy = g.ev(f"(() => {{ const a = DECK_CREW.find(c => c.p && c.p.id === '{id}'); const v = new THREE.Vector3(a.x, 1.0, a.z).project(camera); return [ (v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight ]; }})()")
    g.page.mouse.click(xy[0], xy[1]); g.step(4); return xy
with sync_playwright() as pw:
    class P: pass
    g = P(); br = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    g.page = br.new_page(viewport={'width': 390, 'height': 844}, has_touch=False); g.errors = []
    g.page.on('pageerror', lambda e: g.errors.append(str(e)))
    g.page.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    g.page.add_init_script(INIT); html = vp.read_text(); i = html.rfind('})();'); tmp = WORK / 'test' / ('_rv23p_' + vp.name); tmp.write_text(html[:i] + "window.__sc = src => eval(src);\n" + html[i:])
    g.page.goto('file://' + str(tmp) + '#dev'); g.page.wait_for_function('window.__sc !== undefined', timeout=120000)
    g.page.add_style_tag(content='*,*::before,*::after{transition:none!important;animation:none!important}')
    g.ev = lambda src: g.page.evaluate('s => window.__sc(s)', src)
    g.step = lambda n, dt=1000/30: g.page.evaluate(f'window.__step({n}, {dt})')
    g.step(20)
    if g.page.locator('text=Sign and go aboard').count(): g.page.fill('form input', 'Ada'); g.page.click('text=Sign and go aboard'); g.step(30)
    g.ev("devmodeRun('Set career', () => devmodeSetCareerTo(10))"); g.step(20)
    g.ev(f"devmodeSkipTo({D(11, 12, 20)}); for (const k of NEED_KEYS) SHIP.player.needs[k] = 85"); g.step(10)
    g.ev("goToDeck(4)"); g.step(20)
    # someone awake on the deck, 5-12 m off, in view
    pick = g.ev("""(() => { const P = player.obj.position; const out = [];
      for (const a of DECK_CREW) { if (!a.p || !a.p.id) continue; const w = whereIs(a.p, shipNow()); if (!w || w.act === 'sleep') continue;
        out.push([a.p.id, +Math.hypot(a.x - P.x, a.z - P.z).toFixed(1), w.act]); } return out.sort((x, y) => x[1] - y[1]); })()""")
    print('crew', pick)
    who = [x for x in pick if x[2] in ('leisure', 'off')][0][0]
    def place(dx, dz):   # stand dx, dz from them (an open tile), the camera on you
        g.ev(f"(() => {{ const a = DECK_CREW.find(c => c.p.id === '{who}'); const s = cellPos(...nearestOpen(a.x + {dx}, a.z + {dz}, player)); player.obj.position.set(s.x, player.obj.position.y, s.z); target.copy(player.obj.position).setY(.7); player.stop(); }})()"); g.step(15)
    for dx, dz in ((5, 0), (-5, 0), (0, 5), (0, -5), (4, 3)):
        place(dx, dz); xy = g.ev(f"(() => {{ const a = DECK_CREW.find(c => c.p.id === '{who}'); const v = new THREE.Vector3(a.x, 1.0, a.z).project(camera); return [ (v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight ]; }})()")
        if 20 < xy[0] < 370 and 250 < xy[1] < 650 and dist(g, who) > 3.5: break
    print('who', who, 'dist', dist(g, who))
    # face the camera at them: tap where they are
    xy = tap_on(g, who); c1 = g.ev(CARD); print('A far tap', xy, c1, 'dist', dist(g, who)); g.page.screenshot(timeout=90000, path=f'{OUT}/t1_far_card.png')
    p0 = apos(g, who); g.step(60); print('   card left open 2 s: they', p0, '->', apos(g, who), g.ev(CARD)['chat'])
    if c1['chat'] and c1['chat']['far']:
        g.page.click('#chat button:has-text("Walk over")'); g.step(2); print('B pressed Walk over', g.ev(CARD)); g.page.screenshot(timeout=90000, path=f'{OUT}/t2_walking.png')
        trail = []
        for k in range(40):
            g.step(15); c = g.ev(CARD); trail.append((dist(g, who), apos(g, who), c['chat'] and c['chat']['far']))
            if c['chat'] and not c['chat']['far']: break
        print('   walk', trail[:3], '...', trail[-2:])
        print('C arrived', g.ev(CARD), 'dist', dist(g, who)); g.page.screenshot(timeout=90000, path=f'{OUT}/t3_up_close.png')
    g.ev("chatClose()"); g.step(5)
    # near tap
    print('D near tap', dist(g, who)); tap_on(g, who); print('  ', g.ev(CARD)); g.page.screenshot(timeout=90000, path=f'{OUT}/t4_near_tap.png'); g.ev("chatClose()"); g.step(5)
    # the chip: "would like a word" from afar
    place(dx, dz)
    g.ev(f"seekShow(DECK_CREW.find(c => c.p.id === '{who}').p, Math.floor(shipNow()), null, null)"); g.step(3); g.page.screenshot(timeout=90000, path=f'{OUT}/t5_chip.png')
    g.page.click('#seek'); g.step(3); print('E chip from', dist(g, who), g.ev(CARD)); g.page.screenshot(timeout=90000, path=f'{OUT}/t6_chip_card.png')
    if g.ev("!!(CHAT && CHAT.far)"):
        g.ev("chatDo('walk-over')")
        for k in range(40):
            g.step(15)
            if g.ev("!!(CHAT && !CHAT.far)"): break
        print('   chip walk arrived', g.ev(CARD), dist(g, who))
    # walking off with a far card open (no Walk over): does it close or stay?
    g.ev("chatClose()"); g.step(3); tap_on(g, who) if dist(g, who) > 2.5 else None
    place(dx, dz)
    tap_on(g, who); g.step(3); print('F far card', g.ev(CARD)['chat'])
    g.ev("playerGo(cellAt(player.obj.position.x + 10, player.obj.position.z), () => {})"); g.step(200); print('   walked away', dist(g, who), g.ev(CARD)['chat'])
    print('errors', g.errors[:5]); br.close()
