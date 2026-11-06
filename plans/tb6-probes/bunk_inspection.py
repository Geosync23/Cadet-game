# TB6 probe (0.99.7 note 18): Thursday's bunk inspection on a switched-on copy, you in your bunk room from 06:20. Two
# mornings: all three right (a pass), then the bed not made (not a pass). Checks: the walker held at your bunk's spot for
# the moment, the three checks one at a time, the verdict naming a pass or not, the notice, the walker moving on after.
# Then away from your bunk room: the Mail says passed or not. Phone size.   python3 plans/tb6-probes/bunk_inspection.py BUILD [day]
import sys, json, os, pathlib
sys.argv[0] = str(pathlib.Path(__file__).resolve().parents[2] / 'cadet_test.py')
exec(open(sys.argv[0]).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
build = sys.argv[1]; D = int(sys.argv[2]) if len(sys.argv) > 2 else 4
src = pathlib.Path(build).read_text(); on = src.replace("const TRAD997_ON = false ||", "const TRAD997_ON = true ||", 1); assert on != src
won = WORK / 'test' / ('_insp_%d.html' % os.getpid()); won.write_text(on)
FAILS = []
def check(c, m):
    print(('ok   ' if c else 'FAIL ') + m)
    if not c: FAILS.append(m)
    return c
HOOK2 = """(() => { window.__said = []; window.__toasts = [];
  const bs = bubbleSay; bubbleSay = function (who, text, secs) { const p = who && (who.p || (DECK_CREW.find(a => a.h === who) || {}).p); window.__said.push([Math.round(SHIP.time.min * 10) / 10, p ? p.id : '?', text]); return bs.apply(this, arguments); };
  const ts = toast; toast = function (a, b) { window.__toasts.push([Math.round(SHIP.time.min), a, b]); return ts.apply(this, arguments); }; })()"""
INROOM = """(() => { const c = cellPos(9, 2); player.obj.position.set(c.x, 0, c.z); player.stop(); return roomAt(...player.here()); })()"""
def morning(pw, d, bed, away=False, shot=None):
    g = Game(pw, str(won), 390, 844)
    g.ev("(() => { skipTo(%d * 1440 + 370); SHIP.device.settings.tips = false; for (const k of NEED_KEYS) SHIP.player.needs[k] = 80; })()" % (d - 1))
    g.ev("goToDeck(%d, null)" % (3 if away else 4)); g.step(10); g.ev(HOOK2)
    if not away: print('  room', g.ev(INROOM))
    g.ev("(() => { if (SHIP.clothes) SHIP.clothes.changed = %d; SHIP.player.bedMade = %s; })()" % (d, d if bed else 'null'))
    print('  due', g.ev("inspectDue(%d)" % d), 'walker', g.ev("inspectOfficer(%d)" % d), 'items', g.ev("JSON.stringify(inspectItems(%d))" % d))
    held = []; shotDone = False
    for i in range(900):
        g.step(6)
        x = json.loads(g.ev("JSON.stringify([Math.round(SHIP.time.min * 10) / 10, (DECK_CREW.find(a => a.p.id === inspectOfficer(%d)) || {}).spot ? DECK_CREW.find(a => a.p.id === inspectOfficer(%d)).spot.id : null, CREW_HELD.get(inspectOfficer(%d)) || null])" % (d, d, d)))
        if x[2]: held.append(x)
        if shot and not shotDone and g.ev("window.__said.some(s => /^(That's a pass|Not a pass)/.test(s[2]))"):
            g.page.screenshot(path=shot); shotDone = True
        if x[0] >= 440: break
    r = json.loads(g.ev("JSON.stringify({ said: window.__said, toasts: window.__toasts, mail: SHIP.mail.filter(m => /inspection/i.test(m.subject || '')).map(m => m.body) })"))
    for s in r['said']: print('  said', s)
    for t in r['toasts']: print('  toast', t)
    print('  held', held[:1], '...', held[-1:], 'mail', r['mail'])
    g.close(); return r, held
with sync_playwright() as pw:
    print('--- pass, Day', D)
    r, held = morning(pw, D, True, shot=str(pathlib.Path(build).resolve().parent / 'plans/tb6-probes/inspect-pass.png') if os.environ.get('SHOT') else None)
    by = [s for s in r['said'] if s[2].startswith(('Uniform:', 'Bed:', 'Locker:'))]
    check(len(by) == 3 and [s[2].split(':')[0] for s in by] == ['Uniform', 'Bed', 'Locker'], 'pass: three checks in order (%s)' % [s[2] for s in by])
    check(any(s[2].startswith("That's a pass") for s in r['said']), 'pass: the verdict says a pass')
    check(any(t[1] == 'Bunk inspection' and t[2].startswith('Passed.') for t in r['toasts']), 'pass: the notice')
    check(bool(held) and all(h[2] and h[2].startswith('4-inspect-a') for h in held), 'pass: the walker held at your bunk (%d frames)' % len(held))
    print('--- not a pass (bed), Day', D)
    r, held = morning(pw, D, False)
    by = [s for s in r['said'] if s[2].startswith(('Uniform:', 'Bed:', 'Locker:'))]
    check(len(by) == 3 and by[1][2] == 'Bed: not made.', 'fail: three checks, the bed not made (%s)' % [s[2] for s in by])
    check(any(s[2].startswith('Not a pass this week') for s in r['said']), 'fail: the verdict says not a pass')
    check(any(t[1] == 'Bunk inspection' and t[2].startswith('Not passed this week') for t in r['toasts']), 'fail: the notice')
    print('--- away, Day', D)
    r, held = morning(pw, D, True, away=True)
    check(any(m.startswith('Passed.') for m in r['mail']), 'away: the Mail says passed (%s)' % r['mail'])
won.unlink(missing_ok=True)
print('INSPECT PROBE ' + ('OK' if not FAILS else 'FAILED (%d)' % len(FAILS)))
