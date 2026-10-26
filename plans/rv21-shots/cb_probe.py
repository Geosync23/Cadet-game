import sys, os
G = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
exec(open(os.path.join(os.path.dirname(G), 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
src = open(G).read().replace("const EV_ENDING_ON = URL_FLAGS.has('ending');", "const EV_ENDING_ON = true;", 1)
vp = WORK / 'test' / '_rv21_cb.html'; vp.write_text(src)
GOAL = "(() => { const g = goalNow(); return { clock: clockText(), ev: SHIP.event && SHIP.event.id, goal: g && g.label, lvl: (GUIDE.list||[]).filter(x=>/^end:cb/.test(x.id)).map(x=>x.id+':'+x.level), dlg: DIALOGUE && DIALOGUE.id }; })()"
with sync_playwright() as pw:
    g = Game(pw, str(vp), 390, 844)
    g.ev("skipTo(30 * 1440 + 400)"); g.step(5)
    g.ev("(() => { for (let t = 30*1440+400; t <= 34*1440 + 845; t += 5) { setShipNow(t); EV_MIN = -1; eventsTick(); } })()"); g.step(30)
    print('sun 14:05', g.ev(GOAL)); g.shot(f'{OUT}/c1_sun1405_oath_arrow.png')
    g.ev("(() => { goToDeck(3); const t = ROOM_TILES['L'].slice().sort((a,b)=>b[0]-a[0])[5]; player.obj.position.copy(cellPos(...t)); player.stop(); for (let t = 34*1440+846; t <= 34*1440 + 878; t++) { setShipNow(t); EV_MIN = -1; eventsTick(); } })()"); g.step(60)
    print('sun 14:38', g.ev(GOAL)); g.shot(f'{OUT}/c2_sun1438_lounge.png')
    g.ev("(() => { for (let t = 34*1440+879; t <= 34*1440 + 884; t++) { setShipNow(t); EV_MIN = -1; eventsTick(); } })()"); g.step(90)
    print('sun 14:44', g.ev(GOAL)); g.shot(f'{OUT}/c3_sun1444_oath.png')
    print('errors', g.errors[:5]); g.close()
