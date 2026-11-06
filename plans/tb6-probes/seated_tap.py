# TB6 probe (lead 49's ask, backlog EV1-1): tap a seated host at a tradition to join; do they stay seated? Prints the host's
# pose, settled and spot for a few ship minutes after the tap.   python3 plans/tb6-probes/seated_tap.py BUILD id host deck room [on]
import sys, json, os, pathlib
sys.argv[0] = str(pathlib.Path(__file__).resolve().parents[2] / 'cadet_test.py')
exec(open(sys.argv[0]).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
build, TID, HOST, DECK, ROOM = sys.argv[1:6]; ON = len(sys.argv) > 6
src = pathlib.Path(build).read_text()
if ON: src = src.replace("const TRAD997_ON = false ||", "const TRAD997_ON = true ||", 1)
won = WORK / 'test' / ('_seat_%d.html' % os.getpid()); won.write_text(src)
with sync_playwright() as pw:
    g = Game(pw, str(won), 390, 844)
    D, F = g.ev("(() => { for (let d = 1; d < 60; d++) { const e = eventsOn(d).find(x => x.id === '%s'); if (e) return [d, e.from]; } return [0, 0]; })()" % TID)
    print('day', D, 'from', F)
    g.ev("(() => { skipTo(%d * 1440 + %d + 8); goToDeck(%s, null); SHIP.device.settings.tips = false; })()" % (D - 1, F, DECK)); g.step(60)
    g.ev("(() => { const a = DECK_CREW.find(c => c.p.id === '%s'); const w = nearestOpen(a.x + 1, a.z + 1, player); player.obj.position.copy(cellPos(...w)); player.stop(); })()" % HOST); g.step(5)
    st = lambda: g.ev("(() => { const a = DECK_CREW.find(c => c.p.id === '%s'); return a ? [Math.round(SHIP.time.min), a.pose, a.settled, a.spot && a.spot.id, Math.round(a.talking * 10) / 10, a.goalId || null] : null; })()" % HOST)
    print('before', st())
    print('tap', g.ev("(() => { const a = DECK_CREW.find(c => c.p.id === '%s'); return tradJoinTap(a); })()" % HOST))
    for i in range(40):
        g.step(15)
        if g.ev("!!DIALOGUE"): g.ev("(() => { const v = dialogueView(); dialogueStep(v && v.choices ? 0 : undefined); })()")
        if i % 4 == 0: print("  ", st(), g.ev("ACT ? [ACT.kind, ACT.phase, ACT.placeId, !!ACT.release, ACT.spot && ACT.spot.pose, [...CREW_WAY.entries()], PLAYER_PLACE, BUSY.has('3-lounge-26'), (whereIs(DECK_CREW.find(c => c.p.id === 'walsh-esme').p, shipNow()) || {}).placeId, CREW_HELD.get('walsh-esme')] : null"))
    g.close()
won.unlink(missing_ok=True)
