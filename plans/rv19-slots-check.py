# RV19: independent save-slot checks: a real 0.93.1 save (Playtest and Dev) opened by the new build; bad files; odd slot keys
# Run: python3 plans/rv19-slots-check.py OLD_0.93.1.html NEW.html SERVE_DIR   (own CADET_WORK; serves both on 127.0.0.1:8791, one origin)
import sys, os, re, json, pathlib, subprocess, time
BASE_HTML, NEW_HTML, SRV = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3])
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
(SRV / 'old.html').write_text(instrument(pathlib.Path(BASE_HTML).read_text()))
(SRV / 'new.html').write_text(instrument(pathlib.Path(NEW_HTML).read_text()))
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8791', '--bind', '127.0.0.1', '-d', str(SRV)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
U = 'http://127.0.0.1:8791/'
res = []
def say(ok, msg): res.append(ok); print(('ok   ' if ok else 'FAIL ') + msg)
class Page:
    def __init__(self, ctx, url):
        self.errors = []; self.page = ctx.new_page()
        self.page.on('pageerror', lambda e: self.errors.append(f'pageerror: {e}'))
        self.page.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
        self.page.add_init_script(INIT); self.page.goto(url); self.ready()
    def ready(self):
        self.page.wait_for_function('window.__sc !== undefined || window.__err', timeout=90000)
        self.ev("(() => { const rr = renderer.render.bind(renderer); window.__draw = false; renderer.render = (s, c) => { if (window.__draw) rr(s, c); }; })()")
        self.step(20)
    def ev(self, s): return self.page.evaluate('s => window.__sc(s)', s)
    def step(self, n): self.page.evaluate(f'window.__step({n}, {1000/30})')
    def sign(self):
        if self.page.locator('text=Sign and go aboard').count():
            self.page.fill('form input', 'Ada'); self.page.click('text=Sign and go aboard'); self.step(30)
    def store(self): return self.page.evaluate('() => Object.fromEntries(Object.keys(localStorage).map(k => [k, localStorage.getItem(k)]))')
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844})
    # 1. the real 0.93.1 writes a Playtest save (Day 6 13:10) and a Dev save (Day 15 08:20)
    p = Page(ctx, U + 'old.html'); p.sign(); p.ev('introSkip(); setShipNow(5 * 1440 + 790); updateClock(); saveGame()'); p.step(5)
    p.page.goto('about:blank')
    p = Page(ctx, U + 'old.html#dev'); p.sign(); p.ev('introSkip(); setShipNow(14 * 1440 + 500); updateClock(); saveGame()'); p.step(5)
    p.page.goto('about:blank'); q0 = ctx.new_page(); q0.goto(U); old = q0.evaluate('() => Object.fromEntries(Object.keys(localStorage).map(k => [k, localStorage.getItem(k)]))'); q0.close()
    print('keys after 0.93.1:', sorted(old))
    oP, oD = old.get('starship-cadet-save'), old.get('starship-cadet-save-dev')
    say(bool(oP) and bool(oD), 'the old build left a Playtest and a Dev save')
    # 2. the new build, Playtest link
    n = Page(ctx, U + 'new.html'); st = n.store()
    say(n.ev('SAVE_SLOT') == 1 and n.ev('SAVE_KEY') == 'starship-cadet-save', 'Playtest: the old save is Slot 1 (same key)')
    say(n.ev('SHIP.time.day') == 6 and abs(n.ev('SHIP.time.min') - 790) < 5, f"Playtest: the old game loaded ({n.ev('clockText()')})")
    say(st.get('starship-cadet-save-dev') == oD, 'Playtest link: the Dev save byte for byte')
    say(not any(k in st for k in ['starship-cadet-save-2', 'starship-cadet-save-3', 'starship-cadet-save-slot', 'starship-cadet-save-new']), f'Playtest: no slot keys made by loading ({sorted(st)})')
    sv = n.store().get('starship-cadet-save'); d = json.loads(sv); o = json.loads(oP)
    same = {k: (o.get(k) == d.get(k)) for k in o}; diff = [k for k, v in same.items() if not v]
    print('  keys of the save that differ after the new build saved it:', diff[:20], '| new keys:', [k for k in d if k not in o])
    say(n.ev('slotsView().blocks.filter(x => x.kind === "list").map(x => x.rows[0].text).join("|")') == 'Slot 1 (playing)|Slot 2|Slot 3', 'Playtest: the Saves app lists Slot 1 playing, 2 and 3')
    print('  errors', n.errors[:3]); n.page.goto('about:blank')
    # 3. the new build, Dev link
    n = Page(ctx, U + 'new.html#dev'); st = n.store()
    say(n.ev('SAVE_KEY') == 'starship-cadet-save-dev' and n.ev('SAVE_SLOT') == 1, 'Dev: the old Dev save is Dev Slot 1')
    say(n.ev('SHIP.time.day') == 15 and abs(n.ev('SHIP.time.min') - 500) < 5, f"Dev: the old Dev game loaded ({n.ev('clockText()')})")
    n.step(200); n.ev('saveGame()'); st = n.store()
    say(json.loads(st['starship-cadet-save'])['time']['day'] == 6, 'Dev play leaves the Playtest save alone')
    print('  errors', n.errors[:3]); n.page.goto('about:blank')
    # 4. odd slot keys: garbage, out of range -> Slot 1; an empty slot pointed at -> Slot 1 still there
    q = ctx.new_page()
    for v in ['abc', '7', '0', '2.5', '-1']:
        q.goto(U); q.evaluate(f"() => localStorage.setItem('starship-cadet-save-slot', '{v}')")
        n = Page(ctx, U + 'new.html')
        say(n.ev('SAVE_SLOT') == 1 and n.ev('SHIP.time.day') == 6, f"a broken -slot key '{v}' plays Slot 1 ({n.ev('SAVE_SLOT')})")
        n.page.close()
    q.goto(U); q.evaluate("() => localStorage.removeItem('starship-cadet-save-slot')")
    n = Page(ctx, U + 'new.html')
    # 5. bad files: nothing changes
    before = n.store()
    for name, txt in [('not JSON', 'hello'), ('empty', ''), ('JSON array', '[1,2]'), ('v 3', json.dumps({**o, 'v': 3})), ('no player', json.dumps({k: v for k, v in o.items() if k != 'player'})),
                      ('bad deck', json.dumps({**o, 'player': {**o['player'], 'deck': 99}})), ('a 0.93.1 talk prefs file', '{"vol":0.5}')]:
        n.ev('SLOT_UI.msg = ""'); r = n.ev(f'slotLoadText({json.dumps(txt)})'); msg = n.ev('SLOT_UI.msg')
        say(r is False and 'nothing changed' in msg and n.store() == before and not n.ev('typeof DIALOGUE !== "undefined" && !!DIALOGUE'), f'bad file refused, nothing changed: {name} ({msg[:50]})')
    # 6. a file that passes saveOk but holds almost nothing: into Slot 2, then played: does the game start?
    mini = {'v': 2, 'time': {'day': 3, 'min': 600}, 'player': {'deck': 4, 'tile': [5, 5], 'facing': 0}}
    n.ev(f'slotPut(2, {json.dumps(mini)})') if False else None
    n.page.evaluate("s => localStorage.setItem('starship-cadet-save-2', s)", json.dumps(mini))
    n.page.evaluate("() => localStorage.setItem('starship-cadet-save-slot', '2')"); n.page.goto('about:blank')
    try:
        m = Page(ctx, U + 'new.html'); print('  minimal save: started', m.ev('clockText()'), 'deck', m.ev('deckDef.num'), 'errors', m.errors[:3])
        say(not m.errors, 'a minimal save that passes saveOk starts without page errors')
        say(m.ev('!!document.querySelector("#devBtn")') , 'the device button is there (the Saves app reachable)')
        m.page.evaluate("() => localStorage.setItem('starship-cadet-save-slot', '1')"); m.page.goto('about:blank')
    except Exception as e:
        say(False, f'a minimal save that passes saveOk: the game did not start ({str(e)[:200]})')
    st = Page(ctx, U + 'new.html').store()
    say(json.loads(st['starship-cadet-save'])['time']['day'] == 6, 'Slot 1 still the old game after all that')
    b.close()
srv.terminate()
print('RV19 SLOTS', 'OK' if all(res) else 'FAILED')
