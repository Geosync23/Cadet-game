# RV36 (usage: drill_zeke.py ON.html [START_MIN STOP_HHMM]): how Zeke arrives at the muster line (Day 3 14:54-15:00, switched-on copy): walks in, or appears on his spot?
import sys
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
START = int(sys.argv[2]) if len(sys.argv) > 2 else 893; STOP = sys.argv[3] if len(sys.argv) > 3 else '15:01'
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.step(3)
    g.ev("(() => { skipTo(2 * 1440 + %d)" % START + "; goToDeck(5, null); SHIP.device.settings.tips = false; })()"); g.step(5)
    last = None
    for i in range(300):
        g.step(4)
        r = g.ev("(() => { const a = DECK_CREW.find(c => c.p && c.p.id === 'torres-zeke'); return [hhmm(SHIP.time.min % 1440), a ? [+a.x.toFixed(2), +a.z.toFixed(2), a.goalId || '', !!(a.path && a.path.length)] : 'off-deck']; })()")
        if str(r[1]) != str(last): print(r); last = r[1]
        if r[0] >= STOP: break
    print(g.errors[:3]); g.close()
