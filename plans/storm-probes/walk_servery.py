# EV4, ER2's storm fixes 3 and 4. Run: CADET_WORK=... CADET_CHROME=... python3 plans/storm-probes/walk_servery.py ON.html  (a switched-on copy)
# ER2's fix 3: a player who walks to the servery on Friday Day 12 from 17:00 and queues (a real tap) meets Lukas there
import sys, json
exec(open('/home/user/Cadet-game/cadet_test.py').read().split('a, shots = run(')[0])
src, start = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 1020
with sync_playwright() as pw:
    g = Game(pw, src, 390, 844)
    g.ev(f"skipTo(11 * 1440 + {start} - 600); SHIP.galley = null; skipTo(11 * 1440 + {start}); goToDeck(3); const c = cellPos(24, 7), at = nearestOpen(c.x, c.z, player); player.obj.position.copy(cellPos(...at)); target.copy(player.obj.position).setY(.7); clearGoal(); 1")
    g.step(30)
    g.page.add_style_tag(content='#toast,.nf{pointer-events:none!important}')
    print('walk toward the servery (playerGo, the tap-to-walk):', g.ev("playerGo([30, 6])"))
    for k in range(40):
        g.step(15)
        if g.ev("!player.goal"): break
    print('arrived at', g.ev("cellAt(player.obj.position.x, player.obj.position.z).join(',') + ' ' + hhmm(shipNow() % 1440)"))
    xy = g.ev("(() => { const it = ITEMS.find(i => i.t === 'Servery'), v = new THREE.Vector3(); it.hit.getWorldPosition(v); v.project(camera); return [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight]; })()")
    print('at the tap:', g.ev("document.elementFromPoint(%d, %d).id || document.elementFromPoint(%d, %d).tagName" % (xy[0], xy[1], xy[0], xy[1])))
    g.page.mouse.click(xy[0], xy[1]); g.step(3)
    print('after:', g.ev("JSON.stringify({ act: typeof ACT !== 'undefined' && ACT ? ACT.kind + ':' + ACT.phase : null, path: player.path ? player.path.length : null })"))
    print('tapped the servery at', [round(x) for x in xy], '| toast:', g.ev("(document.getElementById('toast') || {}).textContent || ''")[:80])
    got = None
    for k in range(200):
        g.step(30)
        r = g.ev("""(() => { const P = player.obj.position, L = DECK_CREW.find(a => a.p.id === 'dlamini-lukas'), d = L ? Math.hypot(L.x - P.x, L.z - P.z) : null;
          return { t: hhmm(shipNow() % 1440), you: cellAt(P.x, P.z).join(','), lukas: L ? (L.goalId || '') : 'not on deck', d: d == null ? null : +d.toFixed(1), dlg: DIALOGUE ? DIALOGUE.id : null, fri: !!(SHIP.event && SHIP.event.mine['story:fri']) }; })()""")
        if k % 10 == 0 or r['dlg']: print(json.dumps(r))
        if r['dlg']: got = r; break
        if r['t'] >= '20:30': break
    print('MOMENT OPENED' if got and 'stormLukasFri' in got['dlg'] else 'NO MOMENT', got)
    if got:
        # a reload mid-panel: the page goes, the open panel with it (no onEnd); the save keeps e.mine
        print('reload mid-panel:', g.ev("(() => { const keep = JSON.parse(JSON.stringify(SHIP.event.mine)); DIALOGUE = null; for (const k in MEETING_SCRIPTS) if (k.startsWith('moment:')) delete MEETING_SCRIPTS[k]; SHIP.event.mine = keep; return JSON.stringify({ fri: !!keep['story:fri'] }); })()"))
        g.step(60); print('offered again:', g.ev("DIALOGUE ? DIALOGUE.id : null"))
        n = 0
        while g.ev("!!DIALOGUE") and n < 30:
            n += 1; g.ev("(() => { const v = dialogueView(); dialogueStep(v.choices ? 0 : undefined); })()"); g.step(2)
        print('after the reply:', g.ev("JSON.stringify({ fri: SHIP.event.mine['story:fri'] || null, wants: SHIP.event.mine['wants:stormLanterns'] || null, dlg: DIALOGUE ? DIALOGUE.id : null })"))
        g.step(60); print('not offered a third time:', g.ev("DIALOGUE ? DIALOGUE.id : null"))
    g.close()
