import sys; sys.path.insert(0, '' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + ''); from g import *
MS = "(() => { let b = 1e9; for (let k = 0; k < 5; k++) { window.__skip = true; const a = window.__realNow(); window.__step(60, 1000/30); window.__skip = false; b = Math.min(b, (window.__realNow() - a) / 60); } return b; })()"
WANT = ['loop', 'updateDeckCrew', 'update', 'whereIs', 'planWhere', 'shipDay', 'worksEscort', 'p5Escort', 'p5TeacherWait', 'promoEscort', 'crewWayOn', 'animateActivity', 'animateRig', 'eventsTick', 'eventsOn', 'socialTick', 'playerUpdate', 'galleyTick', 'worksTick', 'worksCareerTick', 'writeWalls', 'place', 'crewNearDoor', 'machinesNow', 'flag', 'evChanged', 'popupWatch', 'stripTick', 'drawScreen', 'applyLight', 'padTick', 'frame', 'discFrame', 'tallSync', 'doorLeavesSync', 'shadowStep', '(garbage collector)', 'updateMatrixWorld', 'introTick', 'tickShip']
with sync_playwright() as pw:
    for day, tm, deck, room in [(1, '18:30', 3, 'Mess'), (2, '10:00', 5, 'Works bay'), (2, '21:00', 4, 'common room')]:
        g = Game(pw, sys.argv[1]); h, m = map(int, tm.split(':')); g.ev(f"skipTo({(day - 1) * 1440 + h * 60 + m}); if (deckDef.num !== {deck}) goToDeck({deck})"); g.step(150)
        ms = g.page.evaluate(MS); tot, top = g.profile(lambda: g.step(900), interval=150); lp = g.inc.get('loop', 1)
        g.gc(); ab, atop = g.alloc(lambda: g.step(300))
        print(f"\n== Day {day} {tm} deck {deck}: {g.ev('crowd.stats().people')} people, js {ms:.2f} ms/frame, loop total {lp:.0f} ms over 900 frames ({lp / 900:.2f} ms/frame), alloc {ab / 300 / 1024:.0f} KB/frame")
        print('  share of the loop (inclusive):', '  '.join(f"{k} {100 * g.inc[k] / lp:.0f}%" for k in sorted(WANT, key=lambda k: -g.inc.get(k, 0)) if g.inc.get(k, 0) / lp > .01))
        print('  self top:', '; '.join(f"{k} {v:.0f}" for v, k in top[:14]))
        print('  alloc top (KB/frame):', '; '.join(f"{k} {v / 1024 / 300:.1f}" for v, k in atop[:14]))
        g.close()
