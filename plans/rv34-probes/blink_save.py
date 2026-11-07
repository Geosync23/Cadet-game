# RV34: save and reload around the Last Light's blink, with real saving (no ?nosave), and phone shots of the notice.
# usage: blink_save.py BUILD.html OUTDIR
import sys, json, time
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
build, out = sys.argv[1], sys.argv[2]
ST = "JSON.stringify([SHIP.time.day, +SHIP.time.min.toFixed(2), FEEL_S.kinds.join(), +(simNow()/1000 - FEEL_S.t0).toFixed(2), SHIP.event && SHIP.event.id, SHIP.event && SHIP.event.mine && SHIP.event.mine['felt:lastLightBlink'], +hemi.intensity.toFixed(4), hemi.color.getHexString(), (window.__toasts||[]).filter(t => /pale light/.test(t[2])).length])"
HOOKT = "window.__toasts = window.__toasts || []; { const ts = toast; toast = function (a, b) { window.__toasts.push([+SHIP.time.min.toFixed(2), a, String(b||'')]); return ts.apply(this, arguments); }; }"
def reopen(g):
    g.page.goto('file://' + str(g.tmp) + '?debug'); g.page.add_style_tag(content='*,*::before,*::after{transition:none!important;animation:none!important}')
    g.page.wait_for_function('window.__sc !== undefined || window.__err', timeout=60000); g.step(3); g.ev(HOOKT)
def show_toast(g): g.ev("document.getElementById('toast').style.setProperty('opacity', '1', 'important')")
with sync_playwright() as pw:
    for case in (sys.argv[3:] or ['mid', 'before']):
        g = Game(pw, build, 390, 844); reopen(g)
        g.ev("localStorage.clear(); newGameStart(false)"); g.step(5)
        g.ev("(() => { skipTo(3 * 1440 + 14 * 60 + 7); goToDeck(3, null); const b = ROOM_BOX.L; if (b) { player.obj.position.copy(cellPos(Math.floor((b.i0 + b.i1) / 2), Math.floor((b.j0 + b.j1) / 2))); target.copy(player.obj.position).setY(.7); } if (typeof GUIDE !== 'undefined') GUIDE.tq.length = 0; })()"); g.step(10)
        if case == 'before':
            while g.ev("SHIP.time.min") < 847.85: g.step(1)
            print(case, 'saved at', g.ev(ST)); g.ev("saveGame()")
        else:
            while 'beacon' not in g.ev("FEEL_S.kinds.join()"): g.step(1)
            g.step(12); print(case, 'mid-blink', g.ev(ST))
            if case == 'mid': show_toast(g); g.page.screenshot(path=out + '/phone_peak.png')
            g.ev("saveGame()")
        reopen(g); print(case, 'after reload', g.ev(ST))
        seen = []
        for i in range(150):
            g.step(1); s = json.loads(g.ev(ST))
            if 'beacon' in s[2] and s[3] < 3: seen.append(s[3])
            if case == 'before' and i == 40: show_toast(g); g.page.screenshot(path=out + '/phone_after_reload.png')
        print(case, 'end', g.ev(ST), 'beacon frames after reload', len(seen), 'errors', [e for e in g.errors if 'pageerror' in e][:3])
        print(case, 'toast now', g.ev("document.getElementById('toast').textContent"), g.ev("JSON.stringify(document.getElementById('toast').getBoundingClientRect())"))
        g.close()
