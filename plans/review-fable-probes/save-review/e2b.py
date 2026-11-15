import sys, time, json, copy
from h import *
serve(8761)
good = open(S / 'save_d10.json').read(); base = json.loads(good)
PLANT = 't => { localStorage.clear(); localStorage.setItem("starship-cadet-arrived", "1"); localStorage.setItem("starship-cadet-save", t); }'
UI = "(() => ({ toast: toastEl.classList.contains('show') ? toastEl.textContent.slice(0, 160) : null, day: SHIP.time.day, min: Math.round(SHIP.time.min), deck: deckDef.num, saved: !!SAVED, here: player.here(), free: free(...player.here()) }))()"
def ls(g): return g.page.evaluate('Object.keys(localStorage).map(k => [k, localStorage.getItem(k).length, localStorage.getItem(k).slice(0, 60)])')
with sync_playwright() as pw:
    g = G(pw, 8761); g.load()
    def run(name, text, steps=60, arrived=True):
        g.page.evaluate(PLANT, text)
        if not arrived: g.page.evaluate('localStorage.removeItem("starship-cadet-arrived")')
        ok = g.load(); r = {'started': ok}
        if ok:
            r['afterLoad'] = ls(g); g.step(steps); r['ui'] = g.ev(UI); r['pending'] = g.page.evaluate('__pending()')
            g.ev('saveGame()'); r['afterSave'] = ls(g)
        r['errs'] = g.errs()[:4]; print('\n##', name, json.dumps(r)[:1500], flush=True); return r
    for name, f in [('E3 day 0 min 0', lambda s: s['time'].update(day=0, min=0)), ('E5 only the saveOk fields', None)]:
        s = copy.deepcopy(base)
        if f: f(s)
        else: s = {'v': 2, 'time': base['time'], 'player': {k: base['player'][k] for k in ('deck', 'tile', 'facing')}}
        run(name, json.dumps(s), 90)
    # D: a throw in one per-frame function
    g.page.evaluate(PLANT, good); g.load(); g.step(30)
    g.ev('window.__n = 0; const __g = galleyTick; galleyTick = () => { if (++window.__n === 5) throw new Error("planted: one bad frame"); return __g(); }')
    g.step(30); m0 = g.ev('SHIP.time.min'); g.step(60)
    print('\n## D one throw in galleyTick:', json.dumps({'pending_rAF': g.page.evaluate('__pending()'), 'minBefore': m0, 'minAfter': g.ev('SHIP.time.min'), 'ui': g.ev(UI), 'errs': g.errs()[:2],
        'visibleMessage': g.page.evaluate("[...document.querySelectorAll('body *')].filter(e => e.children.length === 0 && /error|wrong|reload|crash|problem/i.test(e.textContent) && e.offsetParent !== null && !/script|style/i.test(e.tagName)).map(e => e.textContent.slice(0, 80)).slice(0, 5)")})[:1500])
    # F: a throw in a time jump while asleep
    g.page.evaluate(PLANT, good); g.load(); g.step(30)
    g.page.evaluate('window.__st = window.setTimeout')
    g.ev('SIM_ADVANCE.push(() => { throw new Error("planted: bad time jump"); }); setShipNow(Math.floor(shipNow() / 1440) * 1440 + 22 * 60); sleepGo(360)')
    g.page.wait_for_timeout(2500); g.step(30)
    print('\n## F throw during sleep skip:', json.dumps({'fadeOpacity': g.ev('fadeEl.style.opacity'), 'sleeping': g.ev('sleeping'), 'errs': g.errs()[:2]})[:600])
    g.b.close()
    # B: storage full
    g = G(pw, 8761, pre="const __set = Storage.prototype.setItem; window.__quota = false; window.__tries = 0; Storage.prototype.setItem = function (k, v) { if (window.__quota) { window.__tries++; throw new DOMException('quota', 'QuotaExceededError'); } return __set.call(this, k, v); };")
    g.load(); g.page.evaluate(PLANT, good); g.load(); g.step(30)
    before = ls(g); g.page.evaluate('window.__quota = true')
    g.ev('skipTo(shipNow() + 600)'); g.step(60); g.ev('saveGame()')
    g.page.evaluate("document.dispatchEvent(new Event('visibilitychange'))")
    txt = g.ev('(() => { saveGame(); const t = slotText(); return t ? JSON.parse(t).time : null; })()')
    print('\n## B quota:', json.dumps({'tries': g.page.evaluate('__tries'), 'gameNow': g.ev('[SHIP.time.day, Math.round(SHIP.time.min)]'), 'storedTime (what Download my save would hand over)': txt, 'ui': g.ev(UI), 'errs': g.errs()[:3]})[:900])
    g.b.close()
    # C: storage unavailable (touching localStorage throws)
    g = G(pw, 8761, pre="Object.defineProperty(window, 'localStorage', { get() { throw new DOMException('denied', 'SecurityError'); } });")
    ok = g.load(); r = {'started': ok}
    if ok: g.step(60); r['ui'] = g.ev(UI); r['pending'] = g.page.evaluate('__pending()'); g.ev('saveGame()')
    r['errs'] = g.errs()[:4]; print('\n## C localStorage throws on access:', json.dumps(r)[:900])
    ok = g.load('#dev'); r = {'started': ok}
    if ok: g.step(60); r['pending'] = g.page.evaluate('__pending()')
    r['errs'] = g.errs()[:4]; print('\n## C2 same with #dev:', json.dumps(r)[:900])
