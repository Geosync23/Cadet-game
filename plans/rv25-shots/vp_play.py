# RV25: EV1 visit-pointer (a9364fd): the visit's three pointers in real play at 390x844, with a pretend pad (controller_check's Run).
# Day 17 the greeting's heads-up; Day 19 the gift exchange's heads-up (Go there), the scene, then the farewell: tap to join with
# Envoy Saruth by pad A. Usage: python3 vp_play.py BUILD.html OUTDIR
import sys, os, re, json
G = os.path.abspath(sys.argv[1]); OUT = sys.argv[2]; PART = sys.argv[3] if len(sys.argv) > 3 else 'all'; os.makedirs(OUT, exist_ok=True)
cc = os.path.join(os.path.dirname(G), 'controller_check.py')
sys.argv = [cc, G, 'idle']; src = open(cc).read().split('# ---- run ----')[0]; __file__ = cc; exec(src)
from playwright.sync_api import sync_playwright
RV_HOOK = """(() => { window.__t = []; const T = toast; toast = (a, b) => { window.__t.push(clockText() + ' ' + a + ': ' + b); return T(a, b); }; })()"""
RV_ST = """(() => { const g = goalNow(), tip = document.getElementById('tipCard') || document.getElementById('tip'); const near = ['saruth','teshavi','marrow'].map(id => { const a = DECK_CREW.find(c => c.p && c.p.id === id); return a ? id + '@' + Math.round(Math.hypot(a.x - player.obj.position.x, a.z - player.obj.position.z) * 10) / 10 : null; }).filter(Boolean);
  return { clock: clockText(), deck: deckDef && deckDef.num, room: (ROOMS[roomAt(...player.here())] || {}).name, goal: g && [g.label, g.deck || null, g.place || g.crew || g.room || null], dlg: DIALOGUE && DIALOGUE.id, act: ACT && (ACT.id || ACT.key || ACT.kind || true), tip: tip && !tip.hidden ? tip.textContent : null, ev: SHIP.event && [SHIP.event.id, SHIP.event.phase], near }; })()"""
def rv_log(r, tag):
    s = r.ev(RV_ST); t = r.ev("window.__t.splice(0)"); print(tag, json.dumps(s)); [print('   toast', x) for x in t]; sys.stdout.flush(); return s
def rv_play(r):
    n = 0
    while r.ev("!!DIALOGUE") and n < 80:
        v = r.ev("(() => { const v = dialogueView(); return v ? (v.who || v.name || '') + ': ' + (v.text || '[choice]') : null; })()"); print('     |', (v or '')[:140])
        r.ev("(() => { const v = dialogueView(); if (v && v.choices) dialogueChoose(0); else dialogueNext(); })()"); r.step(2); n += 1
RV_D = lambda d, h, m: (d - 1) * 1440 + h * 60 + m
def rv_goto(r, deck, roomre):
    r.ev(f"""(() => {{ if (deckDef.num !== {deck}) goToDeck({deck}); }})()"""); r.step(10)
    r.ev(f"""(() => {{ const k = Object.keys(ROOM_TILES).find(k => {roomre}.test((ROOMS[k] || {{}}).name || '')); const t = ROOM_TILES[k]; const c = cellPos(...t[Math.floor(t.length / 2)]); player.obj.position.set(c.x, player.obj.position.y, c.z); player.stop(); }})()"""); r.step(5)
with sync_playwright() as pw:
    r = Run(pw, open(G).read(), 'rv25_vp', mode='pad', plug={}, w=390, h=844, query='?debug#dev')
    r.step(20)
    if r.page.locator('text=Sign and go aboard').count(): r.page.fill('form input', 'Ada'); r.page.click('text=Sign and go aboard'); r.step(30); r.press('B'); r.step(2)
    if PART != "d19": r.ev("SHIP.device && SHIP.device.settings && (SHIP.device.settings.tips = false)")
    r.ev('0'); print('set', r.ev("devmodeRun('Set career', () => devmodeSetCareerTo(" + ('19' if PART == 'd19' else '17') + "))")); r.step(20); r.ev(RV_HOOK)
    if PART != 'd19':
        # Day 17: the greeting's heads-up
        r.ev(f"devmodeSkipTo({RV_D(17, 9, 30)})"); r.step(5); rv_log(r, 'd17 0930')
        for k in range(30):
            r.step(30, 100); s = rv_log(r, ' ') if k % 3 == 0 else None
            if r.page.locator('button:visible', has_text='Go there').count(): print('   Go there visible', r.ev("clockText()")); r.page.screenshot(path=f'{OUT}/d17_headsup.png'); break
            if r.ev("shipNow()") > RV_D(17, 10, 0): break
        if r.page.locator('button:visible', has_text='Go there').count():
            r.page.locator('button:visible', has_text='Go there').first.click(); r.step(5); rv_log(r, ' after Go there')
        rv_goto(r, 5, '/^Shuttle bay$/'); r.ev(f"devmodeSkipTo({RV_D(17, 9, 59)})"); r.step(5)
        for k in range(20):
            r.step(10, 100)
            if r.ev("!!DIALOGUE"): s = rv_log(r, ' greeting scene'); r.page.screenshot(path=f'{OUT}/d17_greeting.png'); rv_play(r); break
        rv_log(r, 'd17 after')
    # Day 19: the gift exchange's heads-up and scene
    r.ev(f"devmodeSkipTo({RV_D(19, 8, 30)})"); r.step(5); rv_log(r, 'd19 0830')
    for k in range(40):
        r.step(30, 100)
        hu = r.ev("[...document.querySelectorAll('body *')].filter(e => e.children.length === 0 && e.offsetParent && /gift exchange|Veyli/i.test(e.textContent)).map(e => e.textContent.slice(0, 120)).slice(0, 4)")
        if hu: print('   visible text', r.ev("clockText()"), hu)
        if r.page.locator('button:visible', has_text='Go there').count(): print('   Go there visible', r.ev("clockText()")); r.page.screenshot(path=f'{OUT}/d19_headsup.png'); break
        if r.ev("shipNow()") > RV_D(19, 9, 0): break
    if r.page.locator('button:visible', has_text='Go there').count():
        r.page.locator('button:visible', has_text='Go there').first.click(); r.step(5); rv_log(r, ' after Go there')
    rv_goto(r, 1, '/^Observation room$/'); r.ev(f"devmodeSkipTo(Math.max(shipNow(), {RV_D(19, 8, 59)}))"); r.step(5)
    for k in range(30):
        r.step(10, 100)
        if r.ev("!!DIALOGUE"): s = rv_log(r, ' gifts scene'); r.page.screenshot(path=f'{OUT}/d19_gifts.png'); rv_play(r); break
    rv_log(r, 'd19 after gifts')
    # the farewell, 09:30 in the shuttle bay: marker, arrow, tip; then A by pad
    r.ev(f"devmodeSkipTo({RV_D(19, 9, 31)})"); r.step(5); rv_log(r, 'd19 0927')
    rv_goto(r, 5, '/^Shuttle bay$/'); r.step(30, 100); s = rv_log(r, 'd19 bay'); r.page.screenshot(path=f'{OUT}/d19_farewell_bay.png')
    r.ev("(() => { const a = DECK_CREW.find(c => c.p && c.p.id === 'saruth'); if (a) { player.obj.position.set(a.x + 0.9, player.obj.position.y, a.z); player.stop(); } })()"); r.step(10, 100)
    rv_log(r, 'd19 by Saruth'); r.page.screenshot(path=f'{OUT}/d19_by_saruth.png')
    for k in range(4):
        print('   ring', r.ev("(() => { const s = PAD_PICK.sel; return s ? JSON.stringify({ key: s.key, d: s.d && Math.round(s.d * 10) / 10 }) : null; })()"), r.ev("JSON.stringify((PAD_PICK.list || []).slice(0, 5).map(o => o.key))"))
        r.press('A'); r.step(6); s = rv_log(r, f' after A {k + 1}')
        if s['act']: break
        if r.ev("!!DIALOGUE"): rv_play(r)
    print('   TJ_NOW', r.ev("JSON.stringify(TJ_NOW && { id: TJ_NOW.e.id, lead: TJ_NOW.lead })"))
    print('   farewell entry', r.ev("JSON.stringify(eventsOn(19).filter(e => e.id === 'farewell').map(e => ({ id: e.id, from: e.from, to: e.to, join: tradJoinable(e) })))"))
    r.page.screenshot(path=f'{OUT}/d19_after_A.png')
    for k in range(6): r.step(30, 100)
    rv_log(r, 'd19 end'); r.page.screenshot(path=f'{OUT}/d19_end.png')
    print('errors', r.errors[:8]); r.close()
