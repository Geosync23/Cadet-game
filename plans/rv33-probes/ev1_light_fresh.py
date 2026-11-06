# RV33: The Last Light (EV1 notes 8, 34) from a fresh save with the intro on, as a player at work on Day 4 meets it.
import sys, json
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
build, out = sys.argv[1], sys.argv[2]
RV_HOOK = """(() => { window.__said = []; window.__toasts = [];
  const bs = bubbleSay; bubbleSay = function (who, text) { if (who && who.p) window.__said.push([Math.round(SHIP.time.min), who.p.id, text]); return bs.apply(this, arguments); };
  const ts = toast; toast = function (a, b) { window.__toasts.push([Math.round(SHIP.time.min), a, String(b || '').slice(0, 140)]); return ts.apply(this, arguments); };
  const da = deviceAddress; deviceAddress = function (o) { window.__toasts.push([Math.round(SHIP.time.min), 'ADDRESS ' + o.from, String(o.text || '').slice(0, 200)]); return da.apply(this, arguments); }; })()"""
with sync_playwright() as pw:
    g = Game(pw, build, 390, 844)
    g.ev('localStorage.clear()'); g.ev('newGameStart(true)'); g.step(5)
    g.page.fill('form input[maxlength="24"]', 'Sam'); g.page.locator('form button').first.click(); g.step(5)
    g.ev("""(() => { const t0 = introAbs(INTRO_START.day, INTRO_START.min); socInit(); SHIP.intro = introBlank(); introBegin('Sam');
      for (let t = t0; t <= 3 * 1440 + 9 * 60; t++) { setShipNow(t); const st = SHIP.intro.step && introStepById(SHIP.intro.step);
        introAdvance(t, st && st.checkpoint ? { deck: st.checkpoint.deck, tile: st.checkpoint.tile } : { deck: 4, tile: [8, 3] }); } })()""")
    print('intro', g.ev("JSON.stringify([introOn(), SHIP.intro.step, SHIP.time.day, Math.round(SHIP.time.min)])"))
    mail = g.ev("JSON.stringify(SHIP.mail.filter(m => /light|Vance/i.test((m.subject||'') + (m.from||'') + (m.body||''))).map(m => [m.at, m.from, m.subject, (m.body||'').slice(0,160)]))")
    print('mail so far (Last Light / Vance):', mail)
    g.ev("skipTo(3 * 1440 + 8 * 60 + 52)"); g.step(5)
    print('clock in at 08:52:', g.ev("(() => { const r = clockPunch(false); clockUndoSettle(); return r; })()"))
    g.ev("(() => { skipTo(3 * 1440 + 13 * 60 + 20); goToDeck(5, null); const tl = ROOM_TILES[Object.keys(DECKS[5].rooms).find(k => DECKS[5].rooms[k].name === 'Works bay')]; player.obj.position.copy(cellPos(...tl[(tl.length/2)|0])); for (const k of NEED_KEYS) SHIP.player.needs[k] = 80; })()")
    g.ev(RV_HOOK); g.step(5)
    print('mail by Day 4 13:20:', g.ev("JSON.stringify(SHIP.mail.filter(m => /light/i.test((m.subject||'') + (m.body||''))).map(m => [m.at, m.from, m.subject]))"))
    last = None; tapped = False; walked = False
    for i in range(400):
        if tapped: g.step(30)
        else: g.ev("skipTo(Math.floor(shipNow()) + 1)"); g.step(15)
        x = json.loads(g.ev("""JSON.stringify([Math.round(SHIP.time.min), player.deck, roomAt(...player.here()), typeof goalNow === 'function' && goalNow() ? (goalNow().label || goalNow().text || '') : null,
          TJ_NOW ? TJ_NOW.e.id + ':' + TJ_NOW.lead : null, ACT ? ACT.kind : null, !!DIALOGUE && DIALOGUE.id, typeof eventOn === 'function' && eventOn(4) ? eventOn(4).phase || 'on' : null])"""))
        k = x[1:]
        if k != last: print(' ', x); last = k
        if not walked and x[0] >= 13 * 60 + 55:
            walked = True; print('  following the arrow to the bow lounge')
            g.ev("(() => { goToDeck(3, null); const k = Object.keys(DECKS[3].rooms).find(k => DECKS[3].rooms[k].name === 'Bow lounge'); const tl = ROOM_TILES[k]; player.obj.position.copy(cellPos(...tl[(tl.length/2)|0])); })()"); g.step(20)
            g.page.screenshot(path=out + '/light_arrive.png')
        if walked and not tapped and x[0] >= 14 * 60 + 2:
            tapped = True; print('TAP', g.ev("(() => { const a = DECK_CREW.find(a => a.p.id === 'sato'); return a ? [tradJoinTap(a), a.spot && a.spot.id] : 'no sato on deck'; })()")); g.step(10)
            g.page.screenshot(path=out + '/light_tap.png')
        if x[6]: 
            if 'card' not in globals(): card = 1; print('  card', g.ev("JSON.stringify(dialogueView()).slice(0, 400)")); g.page.screenshot(path=out + '/light_card.png')
            g.ev("(() => { let n = 0; while (DIALOGUE && n++ < 12) { const v = dialogueView(); dialogueStep(v && v.choices ? 0 : undefined); } })()")
        if x[0] == 14 * 60 + 15 and walked: g.page.screenshot(path=out + '/light_mid.png')
        if x[0] >= 15 * 60 or (tapped and i > 250): break
    r = json.loads(g.ev("JSON.stringify({ said: window.__said.filter(s => s[0] >= 13*60+50 && s[0] <= 14*60+40), toasts: window.__toasts })"))
    print('bubbles 13:50-14:40:', len(r['said']), 'by', sorted(set(s[1] for s in r['said'])))
    for s in r['said'][:14]: print('  said', s)
    for t in r['toasts']: print('  toast', t)
    print('addresses', g.ev("JSON.stringify(ADDRESSES.slice(-3).map(a => [a.at, a.text.slice(0, 120)]))"), 'all-hands mail', g.ev("JSON.stringify(SHIP.mail.filter(m => m.subject === 'All hands').map(m => [m.at, (m.body||'').slice(0,80)]))"))
    print('career Day 4', g.ev("JSON.stringify([SHIP.player.clockLog && SHIP.player.clockLog[4], (careerInit().log || []).slice(-5)])")[:400])
    print('joined', g.ev("SHIP.events.joined.filter(k => /ight/.test(k))"), 'intro still on', g.ev("introOn()"), 'errors', [e for e in g.errors if 'pageerror' in e][:4])
