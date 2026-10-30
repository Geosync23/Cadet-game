# opt #10: CPU profile of goToDeck(n) (the build only, no drawing), 3 builds of each deck; self and inclusive time by function
import sys, os, re, json, collections
src = open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0]
exec(src)
from playwright.sync_api import sync_playwright
DECKS = [int(x) for x in (sys.argv[2] if len(sys.argv) > 2 else '3,2,4').split(',')]
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844)
    g.ev("window.__realTick = tickShip; tickShip = () => {}")
    cdp = g.page.context.new_cdp_session(g.page)
    for n in DECKS:
        g.ev(f"goToDeck({n})"); g.ev("goToDeck(" + str(5 if n != 5 else 6) + ")")   # warm (kit made on first visit)
        cdp.send('Profiler.enable'); cdp.send('Profiler.setSamplingInterval', {'interval': 100}); cdp.send('Profiler.start')
        ms = g.page.evaluate("n => { const T = () => new Event('x').timeStamp; const out = []; for (let k = 0; k < 3; k++) { const a = T(); __sc('goToDeck(' + n + ')'); out.push(Math.round(T() - a)); __sc('goToDeck(' + (n === 5 ? 6 : 5) + ')'); } return out; }", n)
        prof = cdp.send('Profiler.stop')['profile']
        nodes = {x['id']: x for x in prof['nodes']}; par = {}
        for x in prof['nodes']:
            for c in x.get('children', []): par[c] = x['id']
        selfc = collections.Counter(); incl = collections.Counter()
        for sid, d in zip(prof['samples'], prof['timeDeltas']):
            fr = nodes[sid]['callFrame']; selfc[(fr['functionName'] or '(anon)', fr['lineNumber'])] += d
            seen = set(); k = sid
            while k is not None:
                f = nodes[k]['callFrame']; key = (f['functionName'] or '(anon)', f['lineNumber'])
                if key not in seen: incl[key] += d; seen.add(key)
                k = par.get(k)
        tot = sum(prof['timeDeltas'])
        print(f'== Deck {n}: goToDeck ms {ms} (and the build of 5/6 between); profile total {tot/1000:.0f} ms')
        print('  self:', ', '.join(f'{f}@{l} {t/1000:.0f}' for (f, l), t in selfc.most_common(14)))
        print('  incl:', ', '.join(f'{f}@{l} {t/1000:.0f}' for (f, l), t in incl.most_common(30) if f not in ('(root)', '(program)')))
    g.close()
