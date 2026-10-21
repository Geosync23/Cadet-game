exec(open('/tmp/claude-0/-home-user-Cadet-game/1a3acdee-25ba-54ef-8a48-f94140cf1be8/scratchpad/common.py').read())
pick = int(sys.argv[2]) if len(sys.argv) > 2 else 0
with sync_playwright() as pw:
    g = mk(pw, sys.argv[1])
    g.ev("skipTo(__at(6, 1141))"); 
    print('mail (newest first):', g.ev("SHIP.mail.slice(0, 4).map(m => hhmm(m.at % 1440) + ' Day ' + (Math.floor(m.at / 1440) + 1) + ' ' + m.from + ': ' + m.subject)"))
    print('event:', g.ev("JSON.stringify(SHIP.event && { id: SHIP.event.id, phase: SHIP.event.phase })"), 'status:', g.ev("typeof eventStatus === 'function' ? eventStatus() : null"))
    w = g.ev("__w('tomas')"); print('tomas 18:55', w)
    for tries in range(12):
        w = g.ev("__w('tomas')")
        if w and not w['moving'] and w['place']: break
        g.ev("skipTo(shipNow() + 5)")
    print('tomas at', g.ev("hhmm(shipNow() % 1440)"), w)
    g.ev(f"goToDeck({w['deck']})"); g.step(5)
    print('walk:', near_walk(g, 'tomas'), g.ev('JSON.stringify(__cs)'))
    ok = run(g, 6, "!!DIALOGUE")
    print('moment opened:', ok, g.ev("DIALOGUE && DIALOGUE.m && DIALOGUE.m.id"), 'mine', g.ev("JSON.stringify(SHIP.event.mine)"))
    g.shot(S + '/shots/sat-tomas.png')
    if ok:
        print('\n'.join(g.ev(f"__dlg({pick})")))
    print('promised:', g.ev("flag('line.promised')"), 'mine', g.ev("JSON.stringify(SHIP.event.mine)"))
    g.ev("skipTo(__at(6, 1380))")
    print('mail after 23:00:', g.ev("SHIP.mail.slice(0, 3).map(m => hhmm(m.at % 1440) + ' ' + m.from + ': ' + m.subject)"))
    print('errors', g.errors[:5])
    g.close()
