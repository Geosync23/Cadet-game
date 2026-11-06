import sys
exec(open("/home/user/Cadet-game/cadet_test.py").read().split("a, shots = run(")[0])
path = sys.argv[1]
with sync_playwright() as pw:
    g = Game(pw, path, 390, 844); g.step(3)
    g.ev("window.__B = []; const bs = bubbleSay; bubbleSay = (w, t, s) => { window.__B.push([(w && w.p ? w.p.id : String(w)), t, SHIP.time.min|0]); return bs(w, t, s); }")
    g.ev("window.__A = []; const ca = captainAddress; captainAddress = o => { window.__A.push(JSON.stringify(o).slice(0, 400)); return ca(o); }")
    print('paper', g.ev("""(() => ({ eventDay3: eventDay(3), eventDay4: eventDay(4), plan: evCalPlan().map(r => r.id + '@' + r.day), cases: typeof eventDay === 'function' }))()"""))
    g.ev("skipTo(2 * 1440 + 17 * 60 + 55)"); g.step(30*8)
    print('wed 18:0x mail', g.ev("(SHIP.mail || []).slice(-4).map(m => [m.from, m.subject, (typeof m.body === 'string' ? m.body : '').slice(0, 80)])"), g.ev("SHIP.event && [SHIP.event.id, SHIP.event.phase]"))
    g.ev("skipTo(3 * 1440 + 13 * 60 + 40); goToDeck(3); const b = ROOM_BOX.L; player.obj.position.copy(cellPos(Math.floor((b.i0 + b.i1) / 2), Math.floor((b.j0 + b.j1) / 2))); target.copy(player.obj.position).setY(.7)")
    g.step(30)
    goers = g.ev("""(() => { const e = eventsOn(4).find(x => x.id === 'lastLightGlass'); const s = evGoers(e, 4); const ppl = schedPeople().filter(p => s.has(p.id));
       const easy = ppl.filter(p => lineEasy(p, 4, e)).length; return [s.size, easy, ppl.map(p => p.dept).reduce((o, x) => (o[x] = (o[x] || 0) + 1, o), {})]; })()""")
    print('goers', goers)
    g.ev("window.__B.length = 0")
    for k in range(14):
        g.step(30*5)
        r = g.ev("""(() => { const n = DECK_CREW.filter(c => c.p && evTagId(c.tag || '') === 'lastLightGlass'); const s = DECK_CREW.find(c => c.p && c.p.id === 'sato');
          return [SHIP.time.min|0, n.length, n.filter(c => c.settled).length, s ? [s.tag, s.settled, s.spot && s.spot.id] : null, SHIP.event && SHIP.event.phase, roomAt(...player.here())]; })()""")
        print(r)
    print('addr', g.ev("window.__A"))
    for b in g.ev("window.__B"): print('  ', b[2]//60, b[2]%60, b[0], '|', b[1])
    print('joined', g.ev("SHIP.events.joined.filter(k => /lastLight/.test(k))"), 'toasts', g.ev("document.getElementById('toast') && document.getElementById('toast').textContent.slice(0,200)"))
    g.ev("skipTo(4 * 1440 + 9 * 60)"); g.step(30)
    print('day5 log', g.ev("SHIP.eventLog.map(l => l.id + ' ' + l.startDay + '-' + l.endDay)"), g.ev("SHIP.event && SHIP.event.id"))
    print('errors', g.errors[:5])
    g.close()
