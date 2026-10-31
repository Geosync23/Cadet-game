# SD5 probe (note 4): who the mess hall sound counts across a ship day
import sys, os, json
sys.argv = [sys.argv[0]] + sys.argv[1:]
exec(open('/home/user/cadet-game/cadet_test.py').read().split('a, shots = run(')[0])
R3_AT = r"""(([t, deck, room]) => { skipTo(t); goToDeck(deck); const R = DECKS[deck].rooms, k = R[room] ? room : Object.keys(R).find(x => R[x].name === room);
  const tl = ROOM_TILES[k]; if (!tl || !tl.length) return 'no tiles for ' + room; player.obj.position.copy(cellPos(...tl[(tl.length / 2) | 0])); return k; })"""
path = sys.argv[1]
with sync_playwright() as pw:
    g = Game(pw, path)
    g.page.goto('file://' + str(g.tmp) + '?nosave&debug&sound&soundlog'); g.page.wait_for_function('window.__sc !== undefined', timeout=60000)
    g.step(30); g.page.mouse.click(450, 380); g.step(3)
    g.page.wait_for_function("window.__sc('SND._.state()') === 'running'", timeout=10000)
    print('full', g.ev("(() => { const k='M'; return (DECKS[3].places||[]).filter(p => p.room === k && p.pose === 'sit').length; })()"))
    for m in range(6*60, 23*60, 20):
        g.ev(f"({R3_AT})({json.dumps([2*1440 + m, 3, 'Mess hall'])})"); g.step(60)
        g.page.wait_for_timeout(1100); g.step(2)
        r = g.ev("""(() => { const k = 'M'; const inM = DECK_CREW.filter(a => a && isFinite(a.x) && roomAt(...cellAt(a.x, a.z)) === k);
          return { n: SND.r3Mess.n, full: SND.r3Mess.full, voices: SND.r3Mess.at(SND.r3Mess.n).voices,
            sat: inM.filter(a => a.settled && a.spot && a.spot.pose === 'sit').length, stand: inM.filter(a => a.settled && !(a.spot && a.spot.pose === 'sit')).length, walking: inM.filter(a => !a.settled).length,
            spots: inM.filter(a => a.settled && a.spot).map(a => a.spot.id).slice(0, 4) }; })()""")
        print(f"{m//60:02d}:{m%60:02d}", r)
    g.close()
