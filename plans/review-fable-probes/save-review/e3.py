import sys, time, json, copy
from h import *
html = pathlib.Path('/home/user/Cadet-game/archive/starship-cadet-0.64.2-whole.html').read_text(); i = html.rfind('})();')
(S / 'www' / 'old.html').write_text(html[:i] + "window.__sc = src => eval(src);\n" + html[i:])
serve(8770)
with sync_playwright() as pw:
    g = G(pw, 8770); g.url = 'http://127.0.0.1:8770/old.html'; g.load(); g.page.evaluate('localStorage.clear()'); g.load(); g.step(30)
    g.ev('introMarkArrived(); newGameStart(false); typeof introSkip === "function" && introSkip()'); g.step(30)
    saves = {}
    for d in (3, 12, 26, 34):
        g.ev(f'skipTo({(d - 1) * 1440 + 600})'); g.step(60); g.ev('saveGame()'); saves[d] = g.page.evaluate('localStorage.getItem("starship-cadet-save")')
        print('old build day', d, 'save bytes', len(saves[d]), g.errs()[:2], flush=True)
        open(S / f'old_save_d{d}.json', 'w').write(saves[d])
    g.url = 'http://127.0.0.1:8770/g.html'
    for d, t in saves.items():
        g.page.evaluate('t => { localStorage.setItem("starship-cadet-save", t); }', t)
        ok = g.load(); r = {'started': ok}
        if ok:
            r['loaded'] = g.ev('!!SAVED'); g.step(120); r['pending'] = g.page.evaluate('__pending()')
            try: g.ev('skipTo(shipNow() + 1500)'); g.step(90); g.ev('skipTo(shipNow() + 1440 * 8)'); g.step(90)
            except Exception as e: r['skipErr'] = str(e)[:400]
            r['pending2'] = g.page.evaluate('__pending()'); r['day'] = g.ev('SHIP.time.day')
            r['ex'] = g.ev("(() => { const ex = []; for (const f of SAVE_EXTRA) { try { f({ player: {}, ship: {}, flags: {} }); } catch (e) { ex.push(String(e).slice(0, 160) + ' :: ' + f.toString().slice(0, 120)); } } localStorage.removeItem(SAVE_KEY); saveGame(); return [ex, localStorage.getItem(SAVE_KEY) !== null]; })()")
        r['errs'] = g.errs()[:5]; print('\n## 0.64.2 save, day', d, '-> current build:', json.dumps(r)[:1500], flush=True)
