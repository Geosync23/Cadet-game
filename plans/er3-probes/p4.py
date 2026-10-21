exec(open('/tmp/claude-0/-home-user-Cadet-game/1a3acdee-25ba-54ef-8a48-f94140cf1be8/scratchpad/common.py').read())
ANS = int(sys.argv[2]) if len(sys.argv) > 2 else 1
def T(g): return g.ev("hhmm(shipNow() % 1440)")
with sync_playwright() as pw:
    g = mk(pw, sys.argv[1])
    g.ev("skipTo(__at(7, 875))"); g.ev("goToDeck(3)"); g.ev("__put(48, 10)"); g.step(5); run(g, 7, "!!DIALOGUE"); g.ev(f"__dlg({ANS})")
    # draw calls: the oath crowd at the widest zoom; the supper at the widest zoom
    for (lab, t, tile) in [('oath', 885, (46, 10)), ('dunk', 900, (46, 10)), ('supper', 1110, (24, 8)), ('supper', 1125, (28, 9))]:
        g.ev(f"skipTo(__at(7, {t})); goToDeck(3); __put({tile[0]}, {tile[1]})"); g.step(40)
        a = g.ev("renderer.info.render.calls"); g.ev("setZoom(.1)"); g.step(20); b = g.ev("renderer.info.render.calls"); g.ev("setZoom(1)")
        print(lab, hhmm := g.ev("hhmm(shipNow() % 1440)"), 'calls', a, 'widest', b, 'crew', g.ev("DECK_CREW.length"))
        if lab == 'supper' and t == 1125: g.ev("setZoom(.1)"); g.step(5); g.shot(S + '/shots/d7-supper-wide.png'); g.ev("setZoom(1)")
    # the Lap: join Tomas's line at 20:30 on the plaza
    g.ev("skipTo(__at(7, 1232)); goToDeck(3); clearGoal(); actEnd(true)"); g.step(5)
    print(T(g), 'tomas', g.ev("__w('tomas')"), 'zeke', g.ev("__w('torres-zeke')"), 'pell', g.ev("__w('pell')"))
    print('near:', near_walk(g, 'tomas', 4))
    print('TJ_NOW', g.ev("TJ_NOW && TJ_NOW.lead"), 'join:', g.ev("TJ_NOW && tradJoinTap(TJ_NOW.agent)"), 'walk', g.ev("!!TJ_WALK"))
    for k in range(150):
        g.step(30)
        r = g.ev("({ t: hhmm(shipNow() % 1440), walk: !!TJ_WALK, dlg: DIALOGUE ? DIALOGUE.m.id : null, lap: SHIP.event.mine['story:lap'] || null, lead: TJ_WALK ? TJ_WALK.lead : null })")
        if r['dlg']: print(r); print('\n'.join(g.ev("__dlg(0)"))); break
        if not r['walk']: print('walk ended', r); break
    print('lap mine', g.ev("SHIP.event.mine['story:lap']"))
    # Monday: the plaque and the certificate, the Record
    g.ev("skipTo(__at(8, 600)); goToDeck(3); __put(39, 10)"); g.step(20)
    print('Monday event', g.ev("JSON.stringify(SHIP.event && { id: SHIP.event.id, phase: SHIP.event.phase })"), 'log', g.ev("JSON.stringify(SHIP.eventLog.map(l => [l.id, l.band]))"), 'traces', g.ev("JSON.stringify(SHIP.traces)"))
    print('plaque item', g.ev("(ITEMS.find(i => i.t === 'The Line plaque') || {}).x"), 'calls', g.ev("renderer.info.render.calls"))
    g.ev("player.face = 0"); g.shot(S + '/shots/d8-plaque.png')
    g.ev("goToDeck(4)"); g.step(20); print('certificate item', g.ev("(ITEMS.find(i => i.t === 'Line certificate') || {}).x"), 'calls', g.ev("renderer.info.render.calls"))
    print('record', g.ev("JSON.stringify(eventRecord())"), 'commendations', g.ev("JSON.stringify(SHIP.commendations)"))
    g.ev("skipTo(__at(9, 60))"); print('Tue: event', g.ev("JSON.stringify(SHIP.event && SHIP.event.id)"), 'log', g.ev("JSON.stringify(SHIP.eventLog.map(l => [l.id, l.startDay, l.endDay]))"))
    print('mail Sun-Mon:', g.ev("SHIP.mail.filter(m => m.at >= __at(7, 0) && m.at < __at(9, 0)).map(m => 'Day ' + (Math.floor(m.at / 1440) + 1) + ' ' + hhmm(m.at % 1440) + ' ' + m.from + ': ' + m.subject)"))
    print('errors', g.errors[:5]); g.close()
