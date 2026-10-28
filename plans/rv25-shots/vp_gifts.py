# RV25: visit-pointer, Day 19 08:30-09:25 (Dev career Day 19): the gift exchange's heads-up queue, Calder's Tier 4 offer, and
# what becomes of the gift exchange when she finds you in the observation room. Usage: vp_gifts.py BUILD.html [stay|away]
import sys, os, re, json
G = os.path.abspath(sys.argv[1]); WHERE = sys.argv[2] if len(sys.argv) > 2 else 'stay'
cc = os.path.join(os.path.dirname(G), 'controller_check.py')
sys.argv = [cc, G, 'idle']; src = open(cc).read().split('# ---- run ----')[0]; __file__ = cc; exec(src)
from playwright.sync_api import sync_playwright
RV_D = lambda d, h, m: (d - 1) * 1440 + h * 60 + m
RV_S = """(() => ({ clock: clockText(), room: (ROOMS[roomAt(...player.here())] || {}).name, dlg: DIALOGUE && DIALOGUE.id, hu: DEV.hu ? DEV.hu.title : null, q: HU_Q.map(h => h.title + ' ' + h.stage).slice(0, 4), busy: devHuBusy(), tips: TIP_Q.length, addr: !!(document.getElementById('devAddr') && !document.getElementById('devAddr').hidden), dlgon: document.body.classList.contains('dlgon'),
  calder: (() => { const a = DECK_CREW.find(c => c.p && c.p.id === 'calder'); return a ? Math.round(Math.hypot(a.x - player.obj.position.x, a.z - player.obj.position.z) * 10) / 10 : null; })(),
  seek: PU4_LIVE.seek ? true : false, t4: JSON.stringify(puT4()) }))()"""
with sync_playwright() as pw:
    r = Run(pw, open(G).read(), 'rv25_vg', mode='pad', plug={}, w=390, h=844, query='?debug#dev', quiet=QUIET.replace('#devHu{display:none!important}', '').replace('#needStrip{display:none!important}', ''))
    r.step(20)
    if r.page.locator('text=Sign and go aboard').count(): r.page.fill('form input', 'Ada'); r.page.click('text=Sign and go aboard'); r.step(30); r.press('B'); r.step(2)
    print('set', r.ev("devmodeRun('Set career', () => devmodeSetCareerTo(19))")); r.step(20)
    print('mtg', r.ev("JSON.stringify(MEETINGS.filter(m => m.id === 'veyliGifts').map(m => ({ at: m.at, len: m.len, notify: m.notify, invited: evInvited(m) })))"))
    r.ev(f"devmodeSkipTo({RV_D(19, 8, 30)})"); r.step(5)
    last = None
    while r.ev("shipNow()") < RV_D(19, 9, 25):
        if WHERE == 'stay' and r.ev("shipNow()") >= RV_D(19, 8, 55) and r.ev("deckDef.num") != 1:
            r.ev("(() => { goToDeck(1); })()"); r.step(10)
            r.ev("""(() => { const k = Object.keys(ROOM_TILES).find(k => /^Observation room$/.test((ROOMS[k] || {}).name || '')); const t = ROOM_TILES[k]; const c = cellPos(...t[Math.floor(t.length / 2)]); player.obj.position.set(c.x, player.obj.position.y, c.z); player.stop(); })()"""); r.step(3)
        r.step(10, 100); s = r.ev(RV_S); k = json.dumps(s, sort_keys=True)[30:]
        if k != last: print(json.dumps(s)); last = k
        if s['hu'] == 'The gift exchange' and not os.path.exists('/tmp/rv25/vp/gifts_hu_' + str(s['clock'][-5:]).replace(':', '') + '.png'): r.page.screenshot(path='/tmp/rv25/vp/gifts_hu_' + s['clock'][-5:].replace(':', '') + '.png')
        if s['dlg']:
            v = r.ev("(() => { const v = dialogueView(); return v ? (v.who || '') + ': ' + (v.text || '[choice]') : null; })()"); print('   |', v)
            r.ev("(() => { const v = dialogueView(); if (v && v.choices) dialogueChoose(0); else dialogueNext(); })()")
    print('mail', r.ev("SHIP.mail.slice(-8).map(m => (m.from || '') + ': ' + (m.subject || m.title || ''))"))
    print('errors', r.errors[:6]); r.close()
