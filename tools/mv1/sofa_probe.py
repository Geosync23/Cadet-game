# EV1-1: you sit on a sofa seat whose walk tile a neighbour's seat shares: does the neighbour stay seated?
import sys, json, os
os.chdir('/home/user/Cadet-game')
exec(open('cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    g.ev("setShipNow(1440 + 20 * 60); goToDeck(3)"); g.step(10)
    print(g.ev("JSON.stringify(['3-lounge-25', '3-lounge-26'].map(id => { const s = placeSpot(id); return [id, s.walk, s.onTile, s.pose]; }))"))
    who = g.ev("(() => { const a = DECK_CREW.find(a => !a.settled || a.spot && /lounge/.test(a.spot.id)) || DECK_CREW[0]; CREW_HELD.set(a.p.id, '3-lounge-25'); return a.p.id; })()")
    for i in range(120):
        g.step(30)
        if g.ev(f"(a => !!a && a.settled && a.spot && a.spot.id === '3-lounge-25')(DECK_CREW.find(a => a.p.id === '{who}'))"): break
    print('held', who, 'settled on 3-lounge-25:', g.ev(f"(a => !!a && a.settled && a.spot && a.spot.id)(DECK_CREW.find(a => a.p.id === '{who}'))"))
    g.ev("actStart('sit', '3-lounge-26', { title: 'Sofa' })")
    st = []
    for i in range(90):
        g.step(30); st.append(g.ev(f"(a => (a.settled ? 'sat ' : 'up ') + (a.goalId || '') + ' | you ' + (ACT && ACT.phase) + ' ' + PLAYER_PLACE + ' path ' + player.path.length + ' at ' + player.here())(DECK_CREW.find(a => a.p.id === '{who}'))"))
    for s in st[::10]: print('  ', s)
    print('errors', g.errors[:3])
