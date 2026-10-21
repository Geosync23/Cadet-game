exec(open('/tmp/claude-0/-home-user-Cadet-game/1a3acdee-25ba-54ef-8a48-f94140cf1be8/scratchpad/common.py').read())
ANS = int(sys.argv[2]) if len(sys.argv) > 2 else 1
def T(g): return g.ev("hhmm(shipNow() % 1440)")
def toasts(g): r = g.ev("__toasts.splice(0)"); return r
with sync_playwright() as pw:
    g = mk(pw, sys.argv[1])
    # Saturday: the promise
    g.ev("skipTo(__at(6, 1141))"); g.ev("goToDeck(3)"); g.step(5); near_walk(g, 'tomas')
    run(g, 4, "!!DIALOGUE"); g.ev("__dlg(0)"); print('Sat promised:', g.ev("flag('line.promised')"))
    # Sunday morning: Brennan's offer
    g.ev("skipTo(__at(7, 640))"); w = g.ev("__w('brennan')"); print(T(g), 'brennan', w)
    g.ev(f"goToDeck({w['deck']})"); g.step(5); print('walk:', near_walk(g, 'brennan'))
    run(g, 3, "!!SHIP.event.mine['story:offer']"); print('offer:', g.ev("SHIP.event.mine['story:offer']"), toasts(g))
    # 12:45: the jobs
    g.ev("skipTo(__at(7, 770))"); 
    jobs = g.ev("jobsBoard().filter(j => j.event === 'crossingLine').map(j => ({ id: j.id, title: j.title, reserved: j.reserved, until: j.until && hhmm(j.until % 1440), status: j.status }))"); print(T(g), 'jobs:', jobs)
    pid = [j for j in jobs if 'linePunch' in j['id']][0]['id'] if jobs else None
    print('claim punch:', g.ev(f"claimJob('{pid}')"))
    print('sheet:', g.ev("(() => { const d = DECK_DRESS.signupMess; return EVENT_DRESS_ON !== undefined ? 1 : 0; })()") if False else '')
    g.ev("goToDeck(3)"); g.step(5); print('to the galley:', g.ev("__put(37, 6)"), g.ev("__room()")); run(g, 2, "!!SHIP.event.mine['story:secret']")
    print('secret:', g.ev("SHIP.event.mine['story:secret']"), toasts(g))
    print('finish punch:', g.ev(f"finishJob('{pid}')"), 'counted before turn-in:', g.ev("eventJobDone('linePunch', true)"), 'turn in:', g.ev(f"typeof turnInJob === 'function' && turnInJob('{pid}')"), g.ev("eventJobDone('linePunch', true)"))
    # 14:20: walk to the bow lounge from the plaza
    g.ev("skipTo(__at(7, 860))"); g.ev("goToDeck(3)"); g.ev("__put(30, 9)"); g.step(5)
    print(T(g), 'lounge open to me? walk to 47,10:', walk(g, 48, 10), g.ev("__room()"))
    run(g, 11, "shipNow() >= __at(7, 871)")
    print(T(g), 'horn toasts', toasts(g), 'felt', g.ev("JSON.stringify(SHIP.event.mine)"))
    g.shot(S + '/shots/d7-1431-lounge.png'); print('calls at 14:31', g.ev("renderer.info.render.calls"))
    run(g, 10, "!!DIALOGUE")
    print(T(g), 'oath open:', g.ev("DIALOGUE && DIALOGUE.m.id"), 'crowd on deck', g.ev("DECK_CREW.filter(a => /lineCeremony|crossingLine/.test(a.tag || '')).length"), 'calls', g.ev("renderer.info.render.calls"))
    g.shot(S + '/shots/d7-oath.png')
    print('\n'.join(g.ev(f"__dlg({ANS})")))
    print('answer flags', g.ev("['proud','watch','punch'].filter(a => flag('line.answer.' + a))"))
    run(g, 16, "shipNow() >= __at(7, 897)")
    print(T(g), 'dunking: mugs', g.ev("DECK_CREW.filter(a => a.pose === 'cocoa').length"), 'calls', g.ev("renderer.info.render.calls")); g.shot(S + '/shots/d7-dunk.png')
    # zoomed out
    g.ev("(() => { if (typeof camDist !== 'undefined') camDist = 1e9; })()")
    run(g, 18, "shipNow() >= __at(7, 916)")
    print(T(g), 'mug toasts', toasts(g), 'goal', g.ev("JSON.stringify(IX_GOAL)"), 'mine', g.ev("JSON.stringify(SHIP.event.mine)"))
    print('status', g.ev("eventStatus()"), 'mail', g.ev("SHIP.mail.slice(0,2).map(m => hhmm(m.at % 1440) + ' ' + m.from + ': ' + m.subject)"))
    # Tomas at his post: walk from the Deck 2 lift
    g.ev("goToDeck(2)"); g.step(5); print('tomas on deck 2:', g.ev("__w('tomas')"), near_walk(g, 'tomas', 8))
    run(g, 3, "!!DIALOGUE"); print(T(g), 'mug moment', g.ev("DIALOGUE && DIALOGUE.m.id"))
    print('\n'.join(g.ev("__dlg(0)")))
    print('after: goal', g.ev("JSON.stringify(IX_GOAL)"), 'mine', g.ev("JSON.stringify(SHIP.event.mine)"))
    g.ev("skipTo(__at(7, 960))"); g.ev("goToDeck(3)"); g.step(20); print(T(g), 'lounge at 16:00 ribbons gone?', g.ev("JSON.stringify(DRESS && DRESS.on ? [...DRESS.on.keys ? DRESS.on.keys() : Object.keys(DRESS.on)] : null)"))
    print('errors', g.errors[:5]); g.close()
