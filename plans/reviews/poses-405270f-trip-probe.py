import sys, json
src = open('perf_check.py').read()
exec(src.split("def run(path)")[0])
with sync_playwright() as pw:
    for path in sys.argv[1:]:
        g = Game(pw, path, 390, 844, [])
        laps = []
        for lap in range(2):
            for n in g.ev("Object.keys(DECKS).map(Number)") + [4]:
                g.ev(f"goToDeck({n})"); g.step(3)
            g.step(10); laps.append(mem(g))
        extra = g.ev("typeof SEAT_RC === 'undefined' ? null : [SEAT_RC.list.length, SEAT_RC.root === deckRoot]")
        g.ev("if (typeof SEAT_RC !== 'undefined') { SEAT_RC.list = []; SEAT_RC.root = null; for (const a of DECK_CREW) if (a.h && a.h.cush) a.h.cush = null; }")
        after = mem(g)
        print(path, 'laps', laps, 'SEAT_RC', extra, 'after clearing SEAT_RC', after, flush=True)
        g.close()
