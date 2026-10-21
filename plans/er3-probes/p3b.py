exec(open('/tmp/claude-0/-home-user-Cadet-game/1a3acdee-25ba-54ef-8a48-f94140cf1be8/scratchpad/common.py').read())
ANS = int(sys.argv[2]) if len(sys.argv) > 2 else 1
MUG = sys.argv[3] if len(sys.argv) > 3 else 'mug'      # 'mug' take Tomas the mug; 'nomug' don't; 'miss' miss the ceremony
def T(g): return g.ev("hhmm(shipNow() % 1440)")
with sync_playwright() as pw:
    g = mk(pw, sys.argv[1])
    g.ev("skipTo(__at(6, 1141))"); g.ev("goToDeck(3)"); g.step(5); near_walk(g, 'tomas'); run(g, 4, "!!DIALOGUE"); g.ev("__dlg(0)")
    print('schedule Day 7:', g.ev("devDay(7).filter(x => x.kind !== 'meal').map(x => hhmm(x.from) + ' ' + x.title + ' (' + x.kind + ')')"))
    g.ev("skipTo(__at(7, 770))"); pid = g.ev("(jobsBoard().find(j => /linePunch/.test(j.id)) || {}).id"); g.ev(f"claimJob('{pid}')")
    g.ev("goToDeck(3)"); g.ev("__put(37, 6)"); g.step(20); g.ev(f"finishJob('{pid}'); turnInJob('{pid}')")
    if MUG != 'miss':
        g.ev("skipTo(__at(7, 875))"); g.ev("goToDeck(3)"); g.ev("__put(48, 10)"); g.step(5); run(g, 7, "!!DIALOGUE"); g.ev(f"__dlg({ANS})")
    g.ev("skipTo(__at(7, 916))"); g.step(5)
    if MUG == 'mug':
        g.ev("skipTo(__at(7, 940))"); g.ev("goToDeck(2)"); g.step(5); near_walk(g, 'tomas', 8); run(g, 3, "!!DIALOGUE"); g.ev("__dlg(0)")
    print('before supper mine', g.ev("JSON.stringify(SHIP.event.mine)"))
    # the Line supper: walk in from the plaza at 18:20 and queue at the servery
    g.ev("skipTo(__at(7, 1100))"); g.ev("goToDeck(3)"); g.ev("__put(24, 7)"); g.step(10)
    g.ev("__toasts.splice(0)")
    xy = g.ev("(() => { const it = ITEMS.find(i => i.t === 'Servery'), v = new THREE.Vector3(); it.hit.getWorldPosition(v); v.project(camera); return [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight]; })()")
    o = g.ev('(() => { const c = cellPos(30, 6); return nearestOpen(c.x, c.z, player); })()'); print('walk to', o, walk(g, o[0], o[1])); xy = g.ev("(() => { const it = ITEMS.find(i => i.t === 'Servery'), v = new THREE.Vector3(); it.hit.getWorldPosition(v); v.project(camera); return [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight]; })()"); g.page.mouse.click(xy[0], xy[1]); g.step(3); print('stand in the line at 33,4:', g.ev('__put(33, 4)'))
    print(T(g), 'tapped the servery:', g.ev("JSON.stringify({ act: typeof ACT !== 'undefined' && ACT ? ACT.kind + ':' + ACT.phase : null })"))
    seen = []
    for k in range(60):
        g.step(25)
        r = g.ev("({ t: hhmm(shipNow() % 1440), room: __room(), tile: __tile(), dlg: DIALOGUE ? DIALOGUE.m.id : null, pell: __dist('pell'), bren: __dist('brennan'), act: typeof ACT !== 'undefined' && ACT ? ACT.kind + ':' + ACT.phase : null, mine: Object.keys(SHIP.event.mine).filter(k => /story:(guess|saved)/.test(k)) })")
        if r['dlg']: print(r); print('\n'.join(g.ev("__dlg(1)"))); 
        if k % 12 == 0: print(r)
        bt = g.ev("__toasts.splice(0)")
        if bt: print(bt)
        b = g.ev("(() => { const out = []; for (const a of DECK_CREW) if (a.h && a.h.bubble && a.h.bubble.text) out.push(a.p.id + ': ' + a.h.bubble.text); return out; })()") if False else None
    print('supper story:', g.ev("JSON.stringify(SHIP.event.mine)"), 'toasts', g.ev("__toasts.splice(0)"))
    print('supper on deck:', g.ev("(() => { const t = shipNow(); let s = 0, st = 0, tr = 0; for (const a of DECK_CREW) { if (/sunday-table/.test(a.tag || '')) { s++; if (a.goalId && !/^3-mess-/.test(a.goalId)) st++; } if (a.tray) tr++; } return { lineSupper: s, notAtMessSeat: st, trays: tr, crew: DECK_CREW.length }; })()"), 'calls', g.ev("renderer.info.render.calls"))
    g.shot(S + '/shots/d7-supper.png')
    print('errors', g.errors[:5]); g.close()
