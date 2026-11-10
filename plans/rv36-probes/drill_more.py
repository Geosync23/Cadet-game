# RV36: piece C cases beyond TB7's probe. usage: drill_more.py C_ON.html OUTDIR [case ...]
# early (tap Calder at 14:52), halloran (join by tapping Halloran), close (close her card with X on line 1),
# save (save with her card open, reload with real saving), offdeck (be on Deck 3 at 15:00-15:16),
# after (where Zeke and Halloran are before, during and after: brought to the line, then back to their plan)
import sys, json
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
build, out = sys.argv[1], sys.argv[2]; D = 3; T0 = (D - 1) * 1440
CASES = sys.argv[3:] or ['early', 'halloran', 'close', 'save', 'offdeck', 'after']
SHOOK = "window.__s = []; { const ts = toast; toast = function (a, b) { window.__s.push([hhmm(SHIP.time.min % 1440), 't', a, String(b || '')]); return ts.apply(this, arguments); }; const ws = worksSay; worksSay = function (id, x) { window.__s.push([hhmm(SHIP.time.min % 1440), 'say', id, x]); return ws.apply(this, arguments); }; }"
ST = "JSON.stringify({ t: hhmm(SHIP.time.min %% 1440), deck: deckDef.num, dlg: DIALOGUE ? DIALOGUE.id : null, notes: simNotes('drill', %d).map(n => [n.mins, n.you, n.day]), use: SHIP.works && SHIP.works.use.m3d || 0, star: DRILL9991.el ? DRILL9991.el.style.display : null, held: ['calder','halloran-emeka','torres-zeke'].map(id => CREW_HELD.get(id) || '-'), act: ACT && ACT.kind, moving: !!(player.path && player.path.length) })" % T0
def until(g, t):
    for _ in range(600):
        if g.ev("shipNow()") >= t: return
        g.step(25)
def reopen(g):
    g.page.goto('file://' + str(g.tmp) + '?debug'); g.page.wait_for_function('window.__sc !== undefined || window.__err', timeout=60000); g.step(3)
with sync_playwright() as pw:
    for case in CASES:
        g = Game(pw, build, 390, 844); g.step(3)
        if case == 'save': reopen(g); g.ev("localStorage.clear(); newGameStart(false)"); g.step(5)
        g.ev("(() => { skipTo(%d + 880); goToDeck(%d, null); SHIP.device.settings.tips = false; for (const k of NEED_KEYS) SHIP.player.needs[k] = 80; })()" % (T0, 3 if case == 'offdeck' else 5)); g.step(5); g.ev(SHOOK)
        if case != 'offdeck': g.ev("(() => { const s = placeSpot('5-muster-6'); player.obj.position.copy(cellPos(...nearestOpen(s.x, s.z + 1.5, player))); player.stop(); })()")
        if case == 'early':
            until(g, T0 + 892); print(case, 'tap', g.ev("tradJoinTap(DECK_CREW.find(x => x.p.id === 'calder'))")); g.step(5); print(case, g.ev(ST))
            until(g, T0 + 902); print(case, 'tap', g.ev("tradJoinTap(DECK_CREW.find(x => x.p.id === 'calder'))")); g.step(5); print(case, g.ev(ST))
        elif case == 'halloran':
            until(g, T0 + 902); print(case, 'tap', g.ev("(() => { const a = DECK_CREW.find(x => x.p.id === 'halloran-emeka'); return a ? tradJoinTap(a) : 'no halloran'; })()")); g.step(5); print(case, g.ev(ST))
        elif case == 'close':
            until(g, T0 + 902); g.ev("tradJoinTap(DECK_CREW.find(x => x.p.id === 'calder'))"); g.step(5)
            print(case, 'card', g.ev(ST)); g.ev("(() => { const x = [...document.querySelectorAll('button,div,span')].find(e => e.offsetWidth && e.textContent.trim() === '×'); if (x) x.click(); else if (typeof dialogueClose === 'function') dialogueClose(); })()"); g.step(30*2)
            print(case, 'closed', g.ev(ST)); print(case, 'tap again', g.ev("tradJoinTap(DECK_CREW.find(x => x.p.id === 'calder'))")); g.step(5); print(case, g.ev(ST))
        elif case == 'save':
            until(g, T0 + 902); g.ev("tradJoinTap(DECK_CREW.find(x => x.p.id === 'calder'))"); g.step(5); print(case, 'card', g.ev(ST))
            g.ev("saveGame()"); reopen(g); g.ev(SHOOK); g.step(30*3); print(case, 'reloaded', g.ev(ST))
            print(case, 'tap again', g.ev("(() => { const a = DECK_CREW.find(x => x.p.id === 'calder'); return a ? tradJoinTap(a) : 'no calder'; })()")); g.step(5); print(case, g.ev(ST))
            if g.ev("!!DIALOGUE"): g.ev("(() => { let n = 0; while (DIALOGUE && n++ < 20) dialogueStep(); })()")
        elif case == 'after':
            W2 = "JSON.stringify(['torres-zeke','halloran-emeka'].map(id => { const p = schedPeople().find(q => q.id === id), w = whereIs(p, shipNow()), a = DECK_CREW.find(c => c.p && c.p.id === id); return [id, w && w.deck, w && (w.placeId || w.type), a ? [+a.x.toFixed(1), +a.z.toFixed(1), a.goalId || ''] : 'off-deck']; }))"
            for m in (880, 896, 904, 912):
                until(g, T0 + m); print(case, hhmm_ := m, g.ev(W2))
            g.ev("tradJoinTap(DECK_CREW.find(x => x.p.id === 'calder'))"); g.step(5); g.ev("(() => { let n = 0; while (DIALOGUE && n++ < 20) dialogueStep(); })()")
            for m in (918, 925, 935, 950):
                until(g, T0 + m); print(case, m, g.ev(W2))
        until(g, T0 + 917); print(case, 'end', g.ev(ST))
        for s in g.ev("window.__s"): 
            if s[0] >= '14:45': print('  ', s)
        print(case, 'errors', g.errors[:3]); g.page.screenshot(path=f'{out}/c-{case}.png'); g.close()
