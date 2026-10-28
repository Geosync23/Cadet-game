# RV25: where PAD_ON costs game-code time with no controller: CPU profile of Sunday dinner (Day 7 18:30, the mess) on a
# build and a copy with only PAD_ON false; self time by function. Usage: pad_prof.py BUILD.html
import sys, os, re, json, collections
G = os.path.abspath(sys.argv[1])
exec(open(os.path.join(os.path.dirname(G), 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
src = open(G).read(); off = src.replace('const PAD_ON = true;', 'const PAD_ON = false;', 1); assert off != src
pon = WORK / 'test' / '_rv25_padon.html'; pon.write_text(src); poff = WORK / 'test' / '_rv25_padoff.html'; poff.write_text(off)
def prof(pw, path):
    g = Game(pw, str(path)); g.page.set_viewport_size({'width': 390, 'height': 844})
    g.ev("skipTo(6 * 1440 + 18 * 60 + 30); if (deckDef.num !== 3) goToDeck(3)"); g.step(30)
    g.ev("(() => { const k = Object.keys(ROOM_BOX).find(k => ROOMS[k] && /^Mess/i.test(ROOMS[k].name)), b = ROOM_BOX[k]; const at = nearestOpen(...Object.values(cellPos(Math.floor((b.i0 + b.i1) / 2), Math.floor((b.j0 + b.j1) / 2))).slice(0, 0).concat([cellPos(Math.floor((b.i0 + b.i1) / 2), Math.floor((b.j0 + b.j1) / 2)).x, cellPos(Math.floor((b.i0 + b.i1) / 2), Math.floor((b.j0 + b.j1) / 2)).z]), player); player.obj.position.copy(cellPos(...at)); })()"); g.step(30)
    info = g.ev("({ live: typeof PAD !== 'undefined' ? PAD.live : null, used: typeof PAD !== 'undefined' ? PAD.used : null, crew: crowd.stats().people })")
    cdp = g.page.context.new_cdp_session(g.page); cdp.send('Profiler.enable'); cdp.send('Profiler.setSamplingInterval', {'interval': 100})
    g.page.evaluate('window.__skip = true'); cdp.send('Profiler.start')
    a = g.page.evaluate('window.__realNow ? window.__realNow() : performance.now()')
    g.page.evaluate('window.__step(120, 1000 / 30)')
    p = cdp.send('Profiler.stop')['profile']; g.page.evaluate('window.__skip = false')
    nodes = {n['id']: n for n in p['nodes']}; dts = p['timeDeltas']; samples = p['samples']; self_t = collections.Counter()
    for s, dt in zip(samples, dts): n = nodes[s]; cf = n['callFrame']; self_t[(cf['functionName'] or '(anon)') + ':' + str(cf['lineNumber'] + 1)] += dt
    total = sum(dts); g.close(); return info, total, self_t
with sync_playwright() as pw:
    R = {}
    for tag, path in (('on', pon), ('off', poff)):
        info, total, st = prof(pw, path); R[tag] = st; print(tag, info, 'total ms', round(total / 1000, 1))
        for k, v in st.most_common(18): print('   ', round(v / 1000, 1), k)
    print('functions much slower with PAD_ON (on - off, ms):')
    names = set(R['on']) | set(R['off']); diff = sorted(((R['on'][n] - R['off'][n]) / 1000, n) for n in names)[::-1]
    for d, n in diff[:15]: print('   ', round(d, 1), n)
