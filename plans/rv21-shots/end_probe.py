# RV21: the ending at phone size (390x844), switch on: the offer arrow/ready room, the goodbye bay, the end page
import sys, os, re
G = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
D = os.path.dirname(G)
exec(open(os.path.join(D, 'cadet_test.py')).read().split("a, shots = run(")[0])
SETUP = open(os.path.join(D, 'ending_check.py')).read().split('SETUP = r"""')[1].split('"""')[0]
from playwright.sync_api import sync_playwright
src = open(G).read().replace("const EV_ENDING_ON = URL_FLAGS.has('ending');", "const EV_ENDING_ON = true;", 1)
vp = WORK / 'test' / '_rv21_end.html'; vp.write_text(src)
with sync_playwright() as pw:
    g = Game(pw, str(vp), 390, 844); g.step(2); g.ev(SETUP)
    # the offer day, 15:50: the arrow; then in the ready room at 16:00
    g.ev("(() => { __reset(32, 940); for (let t = 31*1440 + 350; t <= 31*1440 + 950; t += 10) { setShipNow(t); __tick(); } setShipNow(31*1440 + 950); __tick(); })()")
    g.step(40); print('offer 15:50', g.ev("({ goal: (goalNow()||{}).label, lvl: __guide('end:offer'), notes: __notes.slice(-3), mail: __mail().slice(-2) })")); g.shot(f'{OUT}/e1_offer_1550_arrow.png')
    g.ev("(() => { __to(1, 'R'); setShipNow(31*1440 + 961); __tick(); })()"); g.step(60)
    print('room 16:01', g.ev("({ dlg: DIALOGUE && DIALOGUE.id, line: DIALOGUE && dialogueView() && dialogueView().text })")); g.shot(f'{OUT}/e2_offer_room.png')
    # the goodbye: Monday 09:40 in the bay
    g.ev("""(() => { if (DIALOGUE) dialogueEnd(true); SHIP.player.name = 'Ada'; SHIP.end = endClean({ offer: { day: 32, met: true }, said: [[33, 'go']], settled: { day: 35, choice: 'go' }, f: { asks: 1, last: 1, bf: 1 } });
      setShipNow(35 * 1440 + 556); goToDeck(5); player.obj.position.copy(cellPos(10, 10)); __tick(); })()""")
    g.step(120); g.ev("__tick()"); g.step(60)
    print('bay 09:17+', g.ev("({ calls: renderer.info.render.calls, bay: DECK_CREW.filter(a => a.p && roomAt(...cellAt(a.x, a.z)) === 'S').length, goal: (goalNow()||{}).label })")); g.shot(f'{OUT}/e3_goodbye_bay.png')
    # the end page
    g.ev("(() => { if (DIALOGUE) dialogueEnd(true); endTheEnd(); })()"); g.step(5); g.shot(f'{OUT}/e4_endpage.png')
    print('endpage', g.ev("document.getElementById('endPage').innerText.slice(0, 600)"))
    print('errors', g.errors[:5]); g.close()
