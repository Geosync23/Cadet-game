# 28b's Monday briefing (Day 22, 08:30): read at about 3 s a line; where are the Captain and Calder
import sys, json, os
os.chdir('/home/user/Cadet-game')
exec(open('cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
SET = r"""(() => { skipTo(21 * 1440 + 505); machinesNow(); if (DIALOGUE) dialogueEnd(true); const W = worksInit(); W.tier = 3; W.rank = 'senior'; W.tr.t3 = 15; worksCareerTick(shipNow());
  goToDeck(1); player.stop(); const r = m21Rec(22); return r ? [r.id, r.at % 1440, r.len] : null; })()"""
WHO = "(() => ['marrow', 'calder'].map(id => { const a = DECK_CREW.find(a => a.p.id === id); return id + ':' + (a ? (a.settled ? 'sat ' : 'up ') + (a.spot ? a.spot.id : a.goalId) : 'gone'); }).join(' ') + ' ' + hhmm(shipNow() % 1440))()"
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    g.ev("SHIP.device && SHIP.device.settings && (SHIP.device.settings.tips = false)")
    print('booked', g.ev(SET)); g.step(20)
    g.ev("(() => { const pl = placeById('1-conf-10'), w = pl.walk || pl.at; player.obj.position.copy(cellPos(w[0], w[1] - 1)); player.stop(); })()")
    for k in range(120):
        if g.ev("!!DIALOGUE"): break
        g.step(30)
    print('dialogue', g.ev("DIALOGUE && DIALOGUE.id"), g.ev(WHO), 'lines', g.ev("DIALOGUE ? DIALOGUE.queue.length : 0"))
    n = 0; rows = []
    while g.ev('!!DIALOGUE') and n < 80:
        g.ev('(() => { const l = DIALOGUE.queue[DIALOGUE.i]; if (l && l.choice) dialogueChoose(0); else dialogueNext(); })()'); n += 1
        if not g.ev('!!DIALOGUE'): break
        g.step(100); rows.append(g.ev(WHO))
    for r in rows[::2]: print('  ', r)
    print('taps', n, 'end', g.ev("hhmm(shipNow() % 1440)"), 'errors', g.errors[:3])
