# PR7: the first crew rotation on paper and with a real save at phone size, with reloads across it.
# python3 rot_probe.py BUILD.html [OUTDIR]   (CADET_CHROME, CADET_WORK as for the checks)
import os, sys, json, re, pathlib
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
GAME = sys.argv[1]; OUT = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else '.'); OUT.mkdir(parents=True, exist_ok=True)
TMP = WORK / 'test' / '_rot_probe.html'; TMP.write_text(instrument(pathlib.Path(GAME).read_text()))
class Page:
    def __init__(self, ctx, suffix=''):
        self.errors = []; self.page = ctx.new_page()
        self.page.on('pageerror', lambda e: self.errors.append(f'pageerror: {e}'))
        self.page.on('console', lambda m: m.type == 'error' and self.errors.append(f'error: {m.text}'))
        self.page.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
        self.page.add_init_script(INIT); self.page.goto('file://' + str(TMP) + suffix); self.ready()
    def ready(self):
        self.page.wait_for_function('window.__sc !== undefined', timeout=90000)
        self.page.add_style_tag(content='*,*::before,*::after{transition:none!important;animation:none!important}')
        self.ev("(() => { const rr = renderer.render.bind(renderer); window.__draw = false; renderer.render = (s, c) => { if (window.__draw) rr(s, c); }; })()")
        self.step(20)
    def reload(self): self.page.reload(); self.ready()
    def ev(self, src): return self.page.evaluate('s => window.__sc(s)', src)
    def step(self, n, dt=1000 / 30): self.page.evaluate(f'window.__step({n}, {dt})')
    def shot(self, p): self.page.evaluate('window.__draw = true'); self.step(1); self.page.screenshot(path=str(p)); self.page.evaluate('window.__draw = false')
BAD = []
def check(c, m):
    print(('  ok  ' if c else '  BAD ') + m)
    if not c: BAD.append(m)
PAPER = r"""(() => {
  const T = ROSTER.find(p => p.id === 'teague-theo'), B = ROSTER_RESERVE.find(p => p.id === 'bramwell-basil');
  const ev = {}; for (let d = 17; d <= 30; d++) for (const e of eventsOn(d)) if (/farewell|welcome-tea|name-on-the-beam-new|tern/i.test(e.id)) (ev[d] = ev[d] || []).push([e.id, e.from, e.to, (e.honorees || []).map(p => p.id).join(',')]);
  const st = {}; for (const d of [19, 20, 21, 22]) st[d] = [guestStay(T, d), guestStay(B, d)];
  return { ev, st, rot: ROSTER_ROTATIONS[0], out: crewLeaving(T), in: crewArriving(B) };
})()"""
SNAP = r"""(() => { const ids = ['teague-theo', 'bramwell-basil'];
  const moved = (SHIP.social && SHIP.social.moved || []).map(m => m.id);
  const cs = typeof crewState === 'function' ? crewState(SHIP.time.day) : null;
  const deck = DECK_CREW.map(a => a.p && a.p.id || a.id).filter(id => ids.includes(id));
  return { t: clockText(), day: SHIP.time.day, moved, cs: JSON.stringify(cs).slice(0, 300), theoAboard: aboard(ROSTER.find(p => p.id === 'teague-theo'), SHIP.time.day), basilAboard: aboard(ROSTER_RESERVE.find(p => p.id === 'bramwell-basil'), SHIP.time.day), onDeck: deck.join(',') };
})()"""
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    for w, h in ((390, 844), (360, 780)):
        ctx = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1)
        pg = Page(ctx, '#debug')
        if w == 390:
            p = pg.ev(PAPER); print('paper:', json.dumps(p))
            check(p['out'] == 21 and p['in'] == 21, f"aboard windows: Theo leaves {p['out']}, Basil arrives {p['in']}")
            check(p['st']['20'][1] == 'away' and p['st']['22'][0] == 'away', f"stays 19-22 (Theo, Basil): {p['st']}")
            check(any(e[0] == 'farewell-supper' and 'teague-theo' in e[3] for e in p['ev'].get('20', [])), 'farewell supper on Day 20 for Theo')
            check(any(e[0] == 'name-on-the-beam-new' and 'bramwell-basil' in e[3] for e in p['ev'].get('22', [])), 'Name on the beam on Day 22 for Basil')
            tea = [d for d, es in p['ev'].items() if any(e[0] == 'crew-welcome-tea' for e in es)]; print('  tea on days', tea)
        pg.ev('newGameStart(false); if (typeof introSkip === "function") introSkip(); saveGame()'); pg.reload()
        for label, d, m in (('D20 21:00', 20, 1260), ('D21 14:40', 21, 880), ('D21 15:20', 21, 920), ('D21 18:00', 21, 1080), ('D22 08:00', 22, 480)):
            pg.ev(f'skipTo({(d - 1) * 1440 + m}); saveGame()'); before = pg.ev(SNAP)
            s0 = pg.page.evaluate('() => localStorage.getItem("starship-cadet-save")')
            pg.reload(); after = pg.ev(SNAP)
            pg.ev('saveGame()'); s1 = pg.page.evaluate('() => localStorage.getItem("starship-cadet-save")')
            print(f'  {w} {label}: before {json.dumps(before)}')
            check({k: v for k, v in before.items() if k != 'onDeck'} == {k: v for k, v in after.items() if k != 'onDeck'}, f'{w} {label}: same state after a reload')
            a0, a1 = json.loads(s0), json.loads(s1)
            for k in ('time',): a0.pop(k, None); a1.pop(k, None)
            diff = [k for k in set(a0) | set(a1) if a0.get(k) != a1.get(k)]
            check(len(diff) <= 2, f'{w} {label}: save keys that change across the reload (time aside): {diff}')
            if label == 'D21 18:00': check(not after['theoAboard'] and after['basilAboard'] and after['moved'].count('teague-theo') == 1, f'{w} Day 21 evening: Theo gone once, Basil aboard')
            if label == 'D22 08:00': check(after['moved'].count('teague-theo') == 1, f'{w} Day 22: Theo in moved once ({after["moved"]})')
        pg.ev('goToDeck(5)'); pg.step(30); pg.shot(OUT / f'rot_{w}_d22_deck5.png')
        check(not pg.errors, f'{w}: errors {pg.errors[:3]}'); ctx.close()
    b.close()
print('ROT PROBE ' + ('OK' if not BAD else 'FAILED: ' + '; '.join(BAD)))
