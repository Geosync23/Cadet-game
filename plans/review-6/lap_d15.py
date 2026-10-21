# PR4: is Lap of the Wren on Day 15 at 20:30 (S6's EV_DAY_DRESS add) in a switched-on copy? eventsOn(14/15/21), the dress table
import os, sys, json, re, pathlib
os.environ.setdefault('CADET_WORK', '/tmp/cadet-workb')
exec(open('/home/user/cadet-game/plans/review-6/pp.py').read())
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1]); g.step(10)
    print(g.ev("[EV_CAL_ON, EV_DAY_DRESS.size, [...EV_DAY_DRESS.keys()], [14, 15, 21].map(d => d + ': ' + eventsOn(d).map(e => e.id + '@' + (e.from != null ? e.from : '')).join(' '))]"))
    print(g.ev("(() => { const ev = evTable().find(e => e.id === 'lap-of-the-wren'); return ev ? { when: ev.when, at: ev.at, flag: ev.flag || null, unflag: ev.unflag || null, skip: !!ev.skip } : null; })()"))
    g.close()
# the dressed copy is a new object: section 18's identity tests (tradJoinable, evBudget's rank, the week's Mail, the note's src)
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1]); g.step(10)
    print(g.ev("[15, 21].map(d => eventsOn(d).filter(e => /lap-of-the-wren|rec-talent-night/.test(e.id)).map(e => [d, e.id, 'TRAD_JOIN:' + !!TRAD_JOIN[e.id], 'joinable:' + tradJoinable(e), 'inTraditions:' + SHIP_TRADITIONS.includes(e.ev)]))"))
    g.close()
