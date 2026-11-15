# long session: one page, saving on, skip day by day; at sample days measure frame cost, save size and time, heap, table sizes
import sys; sys.path.insert(0, '' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + ''); from g import *
GAME = sys.argv[1]; DAYS = [1, 2, 4, 7, 10, 14, 21, 28, 35, 50, 70, 100]
MS = "(() => { let b = 1e9; for (let k = 0; k < 4; k++) { window.__skip = true; const a = window.__realNow(); window.__step(60, 1000/30); window.__skip = false; b = Math.min(b, (window.__realNow() - a) / 60); } return b; })()"
with sync_playwright() as pw:
    g = Game(pw, GAME, q='?debug')
    print('intro on:', g.ev("typeof introOn === 'function' && introOn()"), 'NOSAVE', g.ev('NOSAVE'), 'day', g.ev('SHIP.time.day'))
    g.ev("if (typeof introOn === 'function' && introOn()) introSkip()"); g.step(30)
    h0 = g.heap(); last = None
    for d in DAYS:
        cur = g.ev('SHIP.time.day')
        t0 = time.time()
        for x in range(cur, d):                       # a night at a time, as sleeping does, with a little play between
            g.ev(f"skipTo({x} * 1440 + 420)"); g.step(30)
        g.ev(f"skipTo({(d - 1) * 1440 + 600}); if (deckDef.num !== 5) goToDeck(5)"); g.step(150)
        skip_s = time.time() - t0
        ms = g.page.evaluate(MS)
        sv = g.page.evaluate("(() => { const a = window.__realNow(); window.__sc('saveGame()'); const t = window.__realNow() - a; const s = localStorage.getItem(window.__sc('SAVE_KEY')) || ''; const o = s ? JSON.parse(s) : {}; const by = Object.entries(o).map(([k, v]) => [k, JSON.stringify(v).length]).sort((a, b) => b[1] - a[1]).slice(0, 9); let all = 0; for (let i = 0; i < localStorage.length; i++) all += localStorage.key(i).length + localStorage.getItem(localStorage.key(i)).length; return { ms: t, size: s.length, all, keys: localStorage.length, by }; })()")
        cnt = g.ev("({occ: SHIP.occasions.length, jobs: SHIP.jobs.length, notes: (SHIP.notes || []).length, mail: SHIP.player && SHIP.player.mail ? SHIP.player.mail.length : null, simT: SIM_TIMERS.length, shipDays: SHIP_DAYS.size, evDays: EV_DAYS.size, people: crowd.stats().people, day: SHIP.time.day})")
        heap = g.heap()
        print(f"day {d:>3}: js {ms:.2f} ms/frame  save {sv['size'] / 1024:.0f} KB in {sv['ms']:.1f} ms (all storage {sv['all'] / 1024:.0f} KB, {sv['keys']} keys)  heap {heap / 1e6:.0f} MB  skip {skip_s:.0f}s  {json.dumps(cnt)}")
        print('      save by key (chars):', sv['by'])
        if g.errors: print('      errors:', g.errors[:3]); g.errors.clear()
    # reload from the save: does a Day-100 save load, and how long does it take
    t = time.time(); g.page.goto(g.url, timeout=180000); g.page.wait_for_function('window.__sc !== undefined', timeout=180000)
    print('reload from the save:', round(time.time() - t, 1), 's; day', g.ev('SHIP.time.day'), 'errors', g.errors[:3])
    g.close()
