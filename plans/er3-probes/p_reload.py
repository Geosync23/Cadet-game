exec(open('/tmp/claude-0/-home-user-Cadet-game/1a3acdee-25ba-54ef-8a48-f94140cf1be8/scratchpad/common.py').read())
RELOAD = "(() => { const keep = JSON.parse(JSON.stringify(SHIP.event.mine)); DIALOGUE = null; for (const k in MEETING_SCRIPTS) if (k.startsWith('moment:')) delete MEETING_SCRIPTS[k]; SHIP.event.mine = keep; return JSON.stringify(keep); })()"
with sync_playwright() as pw:
    g = mk(pw, sys.argv[1])
    g.ev("skipTo(__at(6, 1141))"); g.ev("goToDeck(3)"); g.step(5)
    print('walk:', near_walk(g, 'tomas'))
    print('opened:', run(g, 4, "!!DIALOGUE"), g.ev("DIALOGUE && DIALOGUE.m.id"))
    g.ev("dialogueStep()"); g.step(3)
    print('reload mid-panel (the save keeps e.mine as it is):', g.ev(RELOAD))
    g.step(5); print('walk again:', near_walk(g, 'tomas', 4))
    print('offered again:', run(g, 4, "!!DIALOGUE"), g.ev("DIALOGUE && DIALOGUE.m.id"))
    g.ev("skipTo(__at(6, 1385))")
    print('Tomas Mail?', g.ev("SHIP.mail.filter(m => /Tomas/.test(m.from)).map(m => hhmm(m.at % 1440) + ' ' + m.subject)"), 'promised', g.ev("flag('line.promised')"))
    print('errors', g.errors[:5]); g.close()
