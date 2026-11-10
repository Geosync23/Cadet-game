# RV36: Sim night joins beyond EV2's probe. usage: sim_more.py ON.html OUTDIR [case ...]
# cases: d3crowd (who stands where while a pilot has given you their pod), tapother (join by tapping a non-host),
#        d25 (a later sim night, no card), walkaway (leave mid-run: pod back), save (save mid-run, reload with real saving)
import sys, json
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
build, out = sys.argv[1], sys.argv[2]
CASES = sys.argv[3:] or ['d3crowd', 'tapother', 'd25', 'walkaway', 'save']
ROOM = """(() => { const o = []; for (const c of DECK_CREW) { if (!c.p) continue; const x = c.obj ? c.obj.position.x : c.x, z = c.obj ? c.obj.position.z : c.z; if (ROOM_BOX.S && x != null) o.push([c.p.id, +x.toFixed(2), +z.toFixed(2), c.spot && c.spot.id || '', c.goalId || '']); } return o; })()"""
HELD = "JSON.stringify([...PLACE_OF.values()].filter(q => /^7-sim/.test(q.id)).map(q => { const c = heldBy(q.id); return q.id + '=' + (c && c.p ? c.p.id : '-'); }))" 
ST = "JSON.stringify([hhmm(SHIP.time.min % 1440), ACT && ACT.kind, ACT && ACT.placeId, SIM_POD_IDS.map(id => { const c = heldBy(id); return c ? c.p.id : '-'; }), EV9991_GIVE && EV9991_GIVE.id, SHIP.events.joined.filter(k => /sim/.test(k))])"
def overlap(g):
    crew = g.ev(ROOM); bad = []
    for i in range(len(crew)):
        for j in range(i + 1, len(crew)):
            a, b = crew[i], crew[j]
            if ((a[1]-b[1])**2 + (a[2]-b[2])**2) ** .5 < .35: bad.append((a[0], b[0], a[1], a[2]))
    p = g.ev("[+player.obj.position.x.toFixed(2), +player.obj.position.z.toFixed(2)]")
    for c in crew:
        if ((c[1]-p[0])**2 + (c[2]-p[1])**2) ** .5 < .35: bad.append(('player', c[0], p[0], p[1]))
    return bad
def setup(g, day, hm):
    if g.ev("typeof GUIDE_ON !== 'undefined' && GUIDE_ON"): g.ev("GUIDE.tq.length = 0; guideToast = () => false")
    g.ev(f"skipTo({day-1} * 1440 + {hm}); goToDeck(7); const b = ROOM_BOX.S; player.obj.position.copy(cellPos(Math.floor((b.i0 + b.i1) / 2), Math.floor((b.j0 + b.j1) / 2))); target.copy(player.obj.position).setY(.7)")
    g.step(30*8)
def tap(g, who=None):
    return g.ev("(() => { const a = DECK_CREW.find(c => c.p && " + (f"c.p.id === '{who}'" if who else "c.p.id !== 'raman' && c.spot && /^7-sim/.test(c.spot.id || '')") + "); return a ? [a.p.id, tradJoinTap(a)] : 'none'; })()")
def through_card(g):
    for i in range(4):
        if g.ev("!!DIALOGUE"): g.ev("dialogueNext()"); g.step(3)
with sync_playwright() as pw:
    for case in CASES:
        g = Game(pw, build, 390, 844); g.step(3)
        if case == 'save':
            g.page.goto('file://' + str(g.tmp) + '?debug'); g.page.wait_for_function('window.__sc !== undefined || window.__err', timeout=60000); g.step(3)
            g.ev("localStorage.clear(); newGameStart(false)"); g.step(5)
        day = 25 if case == 'd25' else 3
        setup(g, day, 19 * 60 + 40)
        print(case, 'before', g.ev(ST), g.ev(HELD))
        print(case, 'tap', tap(g) if case == 'tapother' else tap(g, 'raman')); g.step(10); through_card(g); g.step(30*6)
        print(case, 'joined', g.ev(ST), g.ev(HELD))
        if case == 'save':
            g.ev("saveGame()"); g.page.goto('file://' + str(g.tmp) + '?debug'); g.page.wait_for_function('window.__sc !== undefined || window.__err', timeout=60000); g.step(3)
            if g.ev("typeof GUIDE_ON !== 'undefined' && GUIDE_ON"): g.ev("GUIDE.tq.length = 0; guideToast = () => false")
            g.step(30*6); print(case, 'reloaded', g.ev(ST), g.ev(HELD))
        if case == 'walkaway':
            g.ev("actEnd(true)"); g.step(30*4); print(case, 'left', g.ev(ST))
        worst = []
        for i in range(12):
            g.step(30*3); s = json.loads(g.ev(ST)); b = overlap(g)
            if b: worst.append((s[0], b[:3]))
            if i in (1, 6, 11): print(case, 't', s, g.ev(HELD))
            if i == 2: g.page.screenshot(path=f'{out}/{case}-mid.png')
        print(case, 'overlaps', worst[:6])
        print(case, 'errors', [e for e in g.errors][:3]); g.close()
