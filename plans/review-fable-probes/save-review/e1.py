import sys, time, json
from h import *
build(); serve(8731)
with sync_playwright() as pw:
    g = G(pw, 8731)
    t = time.time(); ok = g.load(); print('load', ok, round(time.time() - t, 1), g.errs()[:3])
    g.step(60); print('pending', g.page.evaluate('__pending()'), g.errs()[:3])
    print('keys', g.page.evaluate('Object.keys(localStorage).map(k => [k, localStorage.getItem(k).length])'))
    print(g.ev('[SHIP.time.day, SHIP.time.min, typeof INTRO_BOOT, SAVE_KEY, INTRO_KEY]'))
    # skip arrival: mark arrived, reload -> ?
    g.ev('saveGame()'); print('keys', g.page.evaluate('Object.keys(localStorage).map(k => [k, localStorage.getItem(k).length])'))
    g.ev('introMarkArrived(); newGameStart(false); typeof introSkip === "function" && introSkip()'); g.step(30)
    t = time.time(); g.ev('skipTo(shipNow() + 1440 * 9 + 300)'); print('skip 9 days', round(time.time() - t, 1))
    g.step(120); g.ev('saveGame()')
    s = g.page.evaluate('localStorage.getItem("starship-cadet-save")'); print('size', len(s), g.errs()[:5])
    open(S / 'save_d10.json', 'w').write(s)
    d = json.loads(s); print({k: len(json.dumps(v)) for k, v in d.items()})
    t = time.time(); g.ev('for (let i = 0; i < 20; i++) saveGame()'); print('20 saves ms', round((time.time() - t) * 1000))
    t = time.time(); g.ev('skipTo(shipNow() + 1440 * 25)'); print('skip 25 days', round(time.time() - t, 1)); g.step(60); g.ev('saveGame()')
    s = g.page.evaluate('localStorage.getItem("starship-cadet-save")'); print('size d35', len(s), g.errs()[:5]); open(S / 'save_d35.json', 'w').write(s)
    d = json.loads(s); print({k: len(json.dumps(v)) for k, v in d.items()})
