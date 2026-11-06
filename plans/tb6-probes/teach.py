# TB6 probe (0.99.7 note 52): Teach me your thing with each teacher, on a switched-on copy. Book it (the Appointments
# app's ask), go to its room on the day, tap the teacher, read the scene; then your activity (its own pose per teacher),
# the coaching bubbles, the result notice and its flag. Phone size.
#   python3 plans/tb6-probes/teach.py BUILD [host ...]
import sys, json, os, pathlib
sys.argv[0] = str(pathlib.Path(__file__).resolve().parents[2] / 'cadet_test.py')
exec(open(sys.argv[0]).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
build = sys.argv[1]; HOSTS = sys.argv[2:] or ['torres-zeke', 'cruz-tove', 'rina', 'hart-ravi']
WANT = {'torres-zeke': ('sit:read', 'knit'), 'cruz-tove': ('water', 'garden'), 'rina': ('sit:play', 'games'), 'hart-ravi': ('sit:fold', 'draw')}
src = pathlib.Path(build).read_text(); on = src.replace("const TRAD997_ON = false ||", "const TRAD997_ON = true ||", 1); assert on != src
won = WORK / 'test' / ('_teach_%d.html' % os.getpid()); won.write_text(on)
FAILS = []
def check(c, m):
    print(('ok   ' if c else 'FAIL ') + m)
    if not c: FAILS.append(m)
    return c
HOOK2 = """(() => { window.__said = []; window.__toasts = [];
  const bs = bubbleSay; bubbleSay = function (who, text, secs) { if (who && who.p) window.__said.push([Math.round(SHIP.time.min), who.p.id, text]); return bs.apply(this, arguments); };
  const ts = toast; toast = function (a, b) { window.__toasts.push([Math.round(SHIP.time.min), a, b]); return ts.apply(this, arguments); }; })()"""
SETUP = """(() => { skipTo(%d); SHIP.device.settings.tips = false; socInit(); for (const id of ['%s']) { const r = relGet(id); r.pts = 65; r.tier = 3; } return 1; })()"""
with sync_playwright() as pw:
    for host in HOSTS:
        print('---', host)
        g = Game(pw, str(won), 390, 844); g.ev(HOOK2); g.ev(SETUP % (2 * 1440 + 600, host))
        g.ev(f"DEVICE_APPS.get('appointments').act('x:ask', 'teach-me|{host}')")
        b = json.loads(g.ev("JSON.stringify(SHIP.apptx.book.slice(-1)[0] || null)"))
        if not check(bool(b) and b['host'] == host, f'{host}: booked ({b})'): g.close(); continue
        g.ev(f"skipTo(({b['day']} - 1) * 1440 + {b['from']} - 5)"); g.step(5)
        r = g.ev(f"[...eventRooms(eventsOn({b['day']}).find(x => x.id === 'appt-teach-me').ev)][0]")
        g.ev(f"goToDeck({int(r.split('|')[0])}, null)"); g.step(10)
        g.ev(f"""(() => {{ const tl = ROOM_TILES['{r.split('|')[1]}'], c = cellPos(...tl[Math.floor(tl.length / 2)]); player.obj.position.set(c.x, 0, c.z); player.stop(); }})()""")
        lead = None
        for _ in range(60):
            g.step(30); lead = g.ev("TJ_NOW && TJ_NOW.e.id === 'appt-teach-me' ? TJ_NOW.lead : null")
            if lead and g.ev(f"(() => {{ const a = DECK_CREW.find(c => c.p.id === '{lead}'); return !!a && a.settled; }})()"): break
        tap = g.ev(f"(() => {{ const a = DECK_CREW.find(c => c.p.id === '{host}'); return !!a && tradJoinTap(a); }})()")
        check(tap and g.ev("!!DIALOGUE"), f'{host}: a tap opens the scene ({lead}, {g.ev("DIALOGUE && DIALOGUE.id")})')
        n = 0
        while g.ev("!!DIALOGUE") and n < 20: g.step(30); g.ev("(() => { const v = dialogueView(); dialogueStep(v && v.choices ? 0 : undefined); })()"); n += 1
        acts = []
        for _ in range(240):
            g.step(15); a = g.ev("ACT ? [ACT.kind, ACT.phase, ACT.placeId, ACT.o.pose, (PLACE_OF.get(ACT.placeId) || {}).type || null] : null")
            if a: acts.append(a)
            if g.ev("window.__toasts.some(t => /^Your first|^Your mint/.test(t[1]))"): break
        r = json.loads(g.ev("JSON.stringify({ said: window.__said.filter(s => s[1] === '%s'), toasts: window.__toasts.filter(t => !/device/.test(t[1])), flag: SHIP.flags['teach997.%s'] })" % (host, WANT[host][1])))
        for s in r['said']: print('  said', s)
        for t in r['toasts']: print('  toast', t)
        do = [a for a in acts if a[1] == 'do']
        print('  act', do[:1])
        check(bool(do) and do[0][3] == WANT[host][0], f'{host}: practising in the pose {WANT[host][0]} ({do[:1]})')
        check(len([s for s in r['said']]) >= 4, f'{host}: four coaching lines')
        check(any(t[1].startswith('Your first') or t[1].startswith('Your mint') for t in r['toasts']) and r['flag'] == b['day'], f'{host}: the result notice and its flag ({r["flag"]})')
        check(not [e for e in g.errors if 'pageerror' in e], f'{host}: no page errors {g.errors[:2]}')
        g.close()
won.unlink(missing_ok=True)
print('TEACH PROBE ' + ('OK' if not FAILS else 'FAILED (%d)' % len(FAILS)))
