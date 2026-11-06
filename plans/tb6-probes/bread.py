# TB6 probe (0.99.7 note 43): Bread day's loaf on a switched-on copy, at phone size. The first Bread day: in the galley at
# 06:58, a tap on Brennan (or anyone at it) joins you; you knead to the end; then the loaf in your hand (the tray slot and
# the loaf prop), Brennan's words and the notice; you sit at a mess seat with it and eat it; the loaf on the table in front
# of you (not the tray) while you eat; afterwards no loaf, Food up. Screenshots in plans/tb6-probes/ with SHOT=1.
# Also: a short knead (walk away after 3 minutes) gives no loaf.   python3 plans/tb6-probes/bread.py BUILD
import sys, json, os, pathlib
sys.argv[0] = str(pathlib.Path(__file__).resolve().parents[2] / 'cadet_test.py')
exec(open(sys.argv[0]).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
build = sys.argv[1]; OUT = pathlib.Path(__file__).resolve().parent
src = pathlib.Path(build).read_text(); on = src.replace("const TRAD997_ON = false ||", "const TRAD997_ON = true ||", 1); assert on != src
won = WORK / 'test' / ('_bread_%d.html' % os.getpid()); won.write_text(on)
FAILS = []
def check(c, m):
    print(('ok   ' if c else 'FAIL ') + m)
    if not c: FAILS.append(m)
    return c
HOOK2 = """(() => { window.__said = []; window.__toasts = [];
  const bs = bubbleSay; bubbleSay = function (who, text, secs) { if (who && who.p) window.__said.push([Math.round(SHIP.time.min), who.p.id, text]); return bs.apply(this, arguments); };
  const ts = toast; toast = function (a, b) { window.__toasts.push([Math.round(SHIP.time.min), a, b]); return ts.apply(this, arguments); }; })()"""
def start(pw, D):
    g = Game(pw, str(won), 390, 844)
    g.ev("(() => { skipTo(%d * 1440 + 412); goToDeck(3, null); SHIP.device.settings.tips = false; for (const k of NEED_KEYS) SHIP.player.needs[k] = 70; SHIP.player.needs.hunger = 40; })()" % (D - 1)); g.step(10); g.ev(HOOK2)
    g.ev("(() => { const tl = ROOM_TILES['K'], c = cellPos(...tl[Math.floor(tl.length / 2)]); player.obj.position.copy(cellPos(...nearestOpen(c.x, c.z, player))); player.stop(); })()")
    for _ in range(60):
        g.step(20)
        if g.ev("!!TJ_NOW && TJ_NOW.e.id === 'bread-day' && !!TJ_NOW.agent && TJ_NOW.agent.settled"): break
    r = g.ev("(() => { const a = TJ_NOW && TJ_NOW.agent; return a ? [a.p.id, tradJoinTap(a)] : null; })()")
    print('  tap', r)
    n = 0
    while g.ev("!!DIALOGUE") and n < 20: g.step(30); g.ev("(() => { const v = dialogueView(); dialogueStep(v && v.choices ? 0 : undefined); })()"); n += 1
    return g, r
with sync_playwright() as pw:
    g = Game(pw, str(won), 390, 844)
    D = g.ev("(() => { for (let d = 1; d < 60; d++) if (eventsOn(d).some(x => x.id === 'bread-day')) return d; return 0; })()")
    print('first Bread day: Day', D, g.ev("JSON.stringify(eventsOn(%d).filter(x => x.id === 'bread-day').map(x => [x.from, x.to]))" % D)); g.close()
    g, r = start(pw, D)
    check(bool(r) and r[1], 'joined by a tap (%s)' % r)
    k = []
    for _ in range(400):
        g.step(20); x = g.ev("[Math.round(SHIP.time.min), ACT ? ACT.kind + ':' + ACT.phase : null, SHIP.player.tray, player.holding || null]")
        if x[1] and 'bread' in x[1]: k.append(x)
        if x[2]: break
        if x[0] > 480: break
    print('  kneaded', k[:1], '...', k[-1:], 'now', x)
    check(len(k) > 0 and k[0][1].startswith('tj:bread-day'), 'kneading at the island')
    g.step(10); x = g.ev("[Math.round(SHIP.time.min), SHIP.player.tray, player.holding || null]")
    check(x[1] == 'your loaf from bread day' and x[2] == 'loaf', 'the loaf in your hand (%s)' % x)
    r2 = json.loads(g.ev("JSON.stringify({ said: window.__said.filter(s => s[1] === 'brennan').slice(-2), toasts: window.__toasts.filter(t => /loaf/i.test(t[1] + t[2])) })"))
    print('  ', r2)
    check(any('loaf' in t[1].lower() for t in r2['toasts']), 'the notice about your loaf')
    if os.environ.get('SHOT'):
        g.ev("(() => { player.obj.position.copy(cellPos(...nearestOpen(player.obj.position.x + 1.2, player.obj.position.z, player))); })()"); g.step(30)
        g.ev('setZoom(2.4)'); g.step(15); g.page.screenshot(path=str(OUT / 'bread-held.png'))
    seat = g.ev("(() => { const pl = [...PLACE_OF.values()].filter(q => q.type === 'mess-seat' && !heldBy(q.id) && !BUSY.has(q.id)).map(q => [q, placeSpot(q.id)]).filter(([, s]) => s).sort((a, b) => Math.hypot(a[1].x - player.obj.position.x, a[1].z - player.obj.position.z) - Math.hypot(b[1].x - player.obj.position.x, b[1].z - player.obj.position.z))[0]; return pl ? pl[0].id : null; })()")
    h0 = g.ev("SHIP.player.needs.hunger")
    g.ev("actStart('sit', '%s', { title: 'A seat' })" % seat)
    seen = None
    for _ in range(300):
        g.step(10); y = g.ev("[ACT ? ACT.kind + ':' + ACT.phase : null, ACT && ACT.o.dish || null, LOAF997_ON.visible, TRAY_ON.visible, player.holding || null]")
        if y[0] == 'eat:do' and seen is None:
            seen = y; g.step(20)
            if os.environ.get('SHOT'): g.ev('setZoom(2.4)'); g.step(15); g.page.screenshot(path=str(OUT / 'bread-eating.png')); xy = g.ev("(() => { const v = LOAF997_ON.position.clone().project(camera); return [Math.round((v.x + 1) * innerWidth / 2), Math.round((1 - v.y) * innerHeight / 2)]; })()"); print('  loaf on screen at', xy); g.page.screenshot(path=str(OUT / 'bread-eating-close.png'), clip={'x': max(0, xy[0] - 80), 'y': max(0, xy[1] - 80), 'width': 160, 'height': 160})
        if seen and not y[0]: break
    print('  eating', seen, 'after', y, 'hunger', h0, '->', g.ev("SHIP.player.needs.hunger"))
    check(bool(seen) and seen[1] == 'your loaf from bread day' and seen[2] and not seen[3], 'eating it at %s: the loaf on the table, not the tray (%s)' % (seat, seen))
    check(g.ev("SHIP.player.tray") is None and g.ev("SHIP.player.needs.hunger") > h0 + 20 and not g.ev("LOAF997_ON.visible"), 'eaten: no loaf left, Food up')
    check(not [e for e in g.errors if 'pageerror' in e], 'no page errors %s' % g.errors[:2])
    g.close()
    print('--- a short knead')
    g, r = start(pw, D)
    g.step(150); g.ev("actEnd(true)"); g.step(60)
    x = g.ev("[Math.round(SHIP.time.min), SHIP.player.tray, LOAF997.given]")
    check(x[1] is None and x[2] == -1, 'walked off after a few minutes: no loaf (%s)' % x)
    g.close()
won.unlink(missing_ok=True)
print('BREAD PROBE ' + ('OK' if not FAILS else 'FAILED (%d)' % len(FAILS)))
