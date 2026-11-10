# RV36: the toasts and the tip box when you join on Day 3 (both pods taken: the give). usage: sim_toasts.py ON.html
import sys
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.step(3)
    g.ev("window.__t = []; { const ts = toast; toast = function (a, b, o) { window.__t.push([hhmm(SHIP.time.min % 1440), a, String(b || '')]); return ts.apply(this, arguments); }; }")
    g.ev("skipTo(2 * 1440 + 19 * 60 + 40); goToDeck(7); const b = ROOM_BOX.S; player.obj.position.copy(cellPos(Math.floor((b.i0 + b.i1) / 2), Math.floor((b.j0 + b.j1) / 2))); target.copy(player.obj.position).setY(.7)")
    g.step(30*8); g.ev("tradJoinTap(DECK_CREW.find(c => c.p && c.p.id === 'raman'))"); g.step(10)
    for i in range(4):
        if g.ev("!!DIALOGUE"): g.ev("dialogueNext()"); g.step(3)
    for i in range(8):
        g.step(30*3); print(g.ev("[hhmm(SHIP.time.min % 1440), document.getElementById('toast').textContent.slice(0, 160), [...document.querySelectorAll('div')].filter(d => d.offsetWidth && /^TIP/.test(d.textContent) && d.children.length < 4).map(d => d.textContent.slice(0, 60)).slice(0, 1)]"))
    for t in g.ev("window.__t"): print(t)
    print(g.errors[:3]); g.close()
