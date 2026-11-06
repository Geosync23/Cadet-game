# RV32 probe (0.99.7, TP1 note 33): Pockets in a page that really saves (no ?nosave). Buys through the store menu's own
# handler (shopMenuBuy: the basket, then the counter's pay step), 4 snacks + 1 drink (the 5th eaten at the till: full),
# a gift-able one (chocolate: into your hands, as before), saveGame, reload, the pocket kept; Pockets' Eat by a real tap.
# Usage (repo root): tp1_pockets.py BUILD_ON.html
import sys, json, pathlib, re, os
sys.argv, BUILD = [sys.argv[0]], sys.argv[1]
exec(open('cadet_test.py').read().split('\ndef run(')[0])
tmp = WORK / 'test' / '_rv32_pockets.html'; tmp.write_text(instrument(pathlib.Path(BUILD).read_text()))
BUY = r"""((name) => { const all = [...STORE.snack.map(r => ['snack', r]), ...STORE.drink.map(r => ['drink', r])], f = all.find(x => x[1][0] === name);
  const item = { kind: f[0], name: f[1][0], price: f[1][1], gain: f[1][2], gift: f[1][3] || null };
  const p = (typeof CREW !== 'undefined' ? CREW : []).find(c => /store/i.test(c.job || '')) || null; shopMenuBuy(p, item); return [item, !!ACT, ACT && ACT.kind]; })"""
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    page = b.new_page(viewport={'width': 390, 'height': 844}); errs = []
    page.on('pageerror', lambda e: errs.append(str(e)))
    page.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    page.add_init_script(INIT)
    def load():
        page.goto('file://' + str(tmp)); page.wait_for_function('window.__sc !== undefined', timeout=90000); page.evaluate('s => window.__sc(s)', SKIP_SWITCH)
        return lambda s: page.evaluate('s => window.__sc(s)', s)
    def step(n): page.evaluate(f'window.__skip = true; window.__step({n - 1}, 1000 / 30); window.__skip = false; window.__step(1, 1000 / 30)')
    ev = load(); ev('localStorage.clear()'); ev = load(); step(5)
    print('start', ev('clockText()'), ev('deckDef.num'), 'intro', ev("typeof introOn === 'function' && introOn()"), 'pack', ev('SHIP.player.pack'))
    ev("(() => { if (DIALOGUE) dialogueEnd(true); introSkip(); })()"); step(5); ev("skipTo(2 * 1440 + 17 * 60 + 40)"); step(10)
    ev("(() => { if (DIALOGUE) dialogueEnd(true); goToDeck(3); const s = placeSpot('3-store-1'); player.obj.position.set(s.x, 0, s.z); player.stop(); SHIP.player.credits = 60; SHIP.player.needs.hunger = 30; })()"); step(10)
    out = []
    for name in ['a honey flapjack', 'a bag of dried apple', 'a cold fizzy lime', 'a pot of spiced nuts', 'a bottle of cold tea', 'a bar of ship-made chocolate']:
        r = ev(BUY + '(' + json.dumps(name) + ')'); print('buy', r, ev('clockText()'), ev('deckDef.num'))
        for k in range(200):
            step(10)
            if not ev('!!basket') and not ev('!!ACT'): break
        out.append([name, ev('SHIP.player.pack.slice()'), ev('SHIP.player.carry.slice()'), round(ev('SHIP.player.needs.hunger')), ev('SHIP.player.credits'), ev("document.getElementById('tx') ? document.getElementById('tx').textContent : ''")[:150]])
        print(out[-1])
    ev('saveGame()'); saved = json.loads(ev('localStorage.getItem(SAVE_KEY)')).get('player', {}).get('pack'); print('saved pack', saved)
    ev = load(); step(5); print('after reload', ev('SHIP.player.pack'), 'carry', ev('SHIP.player.carry'))
    ev("deviceShow('pockets')"); step(3); page.screenshot(path='/tmp/rv32/pockets.png')
    body = ev("document.getElementById('devBody').textContent"); print('Pockets:', body[:400])
    h0 = ev('SHIP.player.needs.hunger')
    page.locator('#devBody button', has_text='Drink').first.click(); step(3)
    print('drink tap:', ev('SHIP.player.pack'), round(h0), '->', round(ev('SHIP.player.needs.hunger')), ev("document.getElementById('tx').textContent")[:120])
    e = page.locator('#devBody button', has_text='Eat'); print('Eat buttons now', e.count())
    page.screenshot(path='/tmp/rv32/pockets2.png')
    # the device app list: Pockets listed
    print('apps', ev("[...DEVICE_APPS.keys()]"))
    print('errors', errs[:5])
