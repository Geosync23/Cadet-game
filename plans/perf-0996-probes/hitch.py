# whole ship days in real time (every frame stepped, drawing skipped), on deck 3: every frame over LIM ms, with the wrapped
# functions' times in it. ARGS: build firstDay days out.json
exec(open('/tmp/pf/scripts/common.py').read())
from playwright.sync_api import sync_playwright
path=sys.argv[1]; D0=int(sys.argv[2]); ND=int(sys.argv[3]); OUT=sys.argv[4]; LIM=float(os.environ.get('LIM','25'))
NAMES='tickShip,saveGame,galleyTick,worksTick,eventsTick,socialTick,introTick,worksCareerTick,updateDeckCrew,playerUpdate,apptTick,shiftTick,careerTick,pausePlace,machinesNow,shipDay,schedBuild,eventsOn,habitsOn,goToDeck,simTimers'.split(',')
WRAP=open('/tmp/pf/scripts/spike2.py').read().split('WRAP="')[1].split('"\nFR=')[0]
FR=r"""(([n, lim]) => { window.__skip = true; const out = []; let tot = 0; for (let k = 0; k < n; k++) { window.__W = {}; const t0 = shipNow(), a = window.__realNow(); window.__step(1, 1000 / 30); const v = window.__realNow() - a; tot += v; if (v > lim) out.push([SHIP.time.day, hhmm(t0 % 1440), deckDef.num, +v.toFixed(1), Object.entries(window.__W).filter(x => x[1] > 3).map(x => [x[0], +x[1].toFixed(1)]).sort((a, b) => b[1] - a[1])]); } window.__skip = false; return { out, mean: tot / n }; })"""
PUT=open('/tmp/pf/scripts/realtime.py').read().split('PUT=r"""')[1].split('"""')[0]
rows=[]
with sync_playwright() as pw:
    g=Game(pw,path,390,844); g.page.evaluate(REALNOW)
    g.ev(f"skipTo({(D0-1)*1440+6*60})"); g.ev(PUT); g.step(30)
    print('wrapped', len(g.page.evaluate("([s, n]) => window.__sc(s)(n)", [WRAP, NAMES])), flush=True)
    per=6000  # 2 ship hours a batch
    for b in range(ND*12):
        r=g.page.evaluate("([s, a]) => window.__sc(s)(a)", [FR, [per, LIM]])
        if g.ev("deckDef.num") != 3: g.ev(PUT)
        for x in r['out']: print(x, flush=True); rows.append(x)
        json.dump(rows,open(OUT,'w'))
    print('end', g.ev("clockText()"), flush=True)
