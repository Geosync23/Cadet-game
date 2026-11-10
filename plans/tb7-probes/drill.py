# TB7 probe (0.99.91 piece C, drills as traditions): the Wednesday drill on a switched-on copy at phone size. Day D (3 fire,
# 10 pressure, 17 power) from 14:40 on Deck 5: no drill side job; the 14:50 toast and arrow; 15:00 Calder, Zeke and Halloran on
# the muster line and the star over her; a tap on her opens her card (the talk); the turnout (note, reputation); you on the line;
# 15:15 the all-clear and the holds let go. MISS=1: you don't tap (the missed note, no reputation). SHOT=1: screenshots here.
#   python3 plans/tb7-probes/drill.py BUILD [day ...]
import sys, json, os, pathlib
sys.argv[0] = str(pathlib.Path(__file__).resolve().parents[2] / 'cadet_test.py')
exec(open(sys.argv[0]).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
build = sys.argv[1]; DAYS = [int(x) for x in sys.argv[2:]] or [3, 10, 17]; OUT = pathlib.Path(__file__).resolve().parent; MISS = os.environ.get('MISS')
src = pathlib.Path(build).read_text(); on = src.replace("const TB9991_DRILL_ON = false ||", "const TB9991_DRILL_ON = true ||", 1)
won = WORK / 'test' / ('_drill_%d.html' % os.getpid()); won.write_text(on)
FAILS = []
if os.environ.get('SHOT'):   # screenshots for a person: at device scale 2
    from playwright.sync_api._generated import Browser as _B
    _np = _B.new_page; _B.new_page = lambda self, **k: _np(self, **{**k, 'device_scale_factor': 2})
def check(c, m):
    print(('ok   ' if c else 'FAIL ') + m)
    if not c: FAILS.append(m)
    return c
HOOKP = """(() => { window.__said = []; window.__toasts = [];
  const bs = bubbleSay; bubbleSay = function (who, text, secs) { if (who && who.p) window.__said.push([Math.round(shipNow()), who.p.id, text]); return bs.apply(this, arguments); };
  const ts = toast; toast = function (a, b) { window.__toasts.push([Math.round(shipNow()), a, b]); return ts.apply(this, arguments); };
  const ws = worksSay; worksSay = function (id, text) { window.__said.push([Math.round(shipNow()), id, text]); return ws.apply(this, arguments); }; })()"""
LINE = """JSON.stringify((() => { const at = id => { const a = DECK_CREW.find(x => x.p.id === id); if (!a) return 'off-deck'; const s = placeSpot('5-muster-' + ({ calder: 3, 'torres-zeke': 2, 'halloran-emeka': 4 })[id]);
  return [CREW_HELD.get(id) || null, s ? +Math.hypot(s.x - a.x, s.z - a.z).toFixed(2) : null]; };
  return { t: Math.round(shipNow()), calder: at('calder'), zeke: at('torres-zeke'), hall: at('halloran-emeka'), star: DRILL9991.el ? DRILL9991.el.style.display + ':' + DRILL9991.el.textContent : null,
    goal: (() => { try { const g = goalNow(); return g ? g.label : null; } catch (e) { return 'err ' + e; } })(), jobs: SHIP.jobs.filter(j => /drill/.test(j.kind)).length, dlg: DIALOGUE ? DIALOGUE.id : null }; })())"""
def until(g, t):
    for _ in range(400):
        if g.ev("shipNow()") >= t: return
        g.step(25)
with sync_playwright() as pw:
    for D in DAYS:
        print('==== Day', D)
        g = Game(pw, str(won), 390, 844)
        g.ev("(() => { skipTo(%d * 1440 + 880); goToDeck(5, null); SHIP.device.settings.tips = false; for (const k of NEED_KEYS) SHIP.player.needs[k] = 80; })()" % (D - 1)); g.step(5); g.ev(HOOKP)
        g.ev("(() => { const s = placeSpot('5-muster-6'); player.obj.position.copy(cellPos(...nearestOpen(s.x, s.z + 1.5, player))); player.stop(); })()")
        st = g.ev("JSON.stringify([SHIP.time.day, weekday(%d), drillKind(%d), drill9991Who(%d), SHIP.works && SHIP.works.rank, SHIP.works && [...worksOpened(SHIP.works)].includes('m3d'), playerShiftOn(%d)])" % (D, D, D, D))
        print('  state', st); st = json.loads(st)
        if not check(st[3] in ('junior', 'senior'), 'Day %d: a drill of yours (%s)' % (D, st)): g.close(); continue
        until(g, (D - 1) * 1440 + 892)
        a = json.loads(g.ev(LINE)); print('  14:5x', a)
        t = json.loads(g.ev("JSON.stringify(window.__toasts)")); print('  toasts', t)
        check(any('Drill at 15:00' in (x[2] or '') for x in t), 'Day %d: the 14:50 toast' % D)
        check(a['jobs'] == 0, 'Day %d: no drill side job' % D)
        check(bool(a['goal']) and 'Calder' in a['goal'], 'Day %d: the arrow to Calder (%s)' % (D, a['goal']))
        until(g, (D - 1) * 1440 + 901)
        for _ in range(30):
            a = json.loads(g.ev(LINE))
            if a['calder'] != 'off-deck' and a['calder'][1] is not None and a['calder'][1] < .3: break
            g.step(25)
        print('  15:0x', a)
        check(a['calder'] != 'off-deck' and a['calder'][0] == '5-muster-3' and a['calder'][1] < .3, 'Day %d: Calder on the muster line (%s)' % (D, a['calder']))
        check(a['zeke'] == 'off-deck' or a['zeke'][0] == '5-muster-2', 'Day %d: Zeke held beside her (%s)' % (D, a['zeke']))
        check(a['hall'] == 'off-deck' or a['hall'][0] == '5-muster-4', 'Day %d: Halloran held beside her (%s)' % (D, a['hall']))
        check(bool(a['star']) and a['star'].startswith('block'), 'Day %d: the star over her (%s)' % (D, a['star']))
        use0 = g.ev("SHIP.works.use.m3d || 0")
        if MISS:
            pass
        else:
            r = g.ev("tradJoinTap(DECK_CREW.find(x => x.p.id === 'calder'))"); g.step(3)
            v = json.loads(g.ev("JSON.stringify(DIALOGUE && { id: DIALOGUE.id, n: DIALOGUE.queue.length, lines: DIALOGUE.queue.map(l => [l.who, l.text]) })"))
            print('  card', json.dumps(v, indent=1))
            check(r and v and v['id'] == 'drill9991.talk', 'Day %d: a tap on Calder opens her talk (%s)' % (D, r))
            check(v and 6 <= v['n'] <= 9 and not any(l[0] is None for l in v['lines']), 'Day %d: about 6 lines, no question' % D)
            if os.environ.get('SHOT'):
                g.ev('setZoom(2.4)'); g.step(10); g.page.screenshot(path=str(OUT / ('drill-%s.png' % st[2])))
            n = 0
            while g.ev("!!DIALOGUE") and n < 20:
                g.ev("dialogueStep()"); g.step(5); n += 1
            for _ in range(20): g.step(15)
            b = json.loads(g.ev("JSON.stringify({ notes: simNotes('drill', %d).map(n => [n.kind, n.mins, n.you, n.day]), pd: simNotes('pwrDrill', %d), use: SHIP.works.use.m3d || 0, tr: SHIP.works.tr.m3d, star: DRILL9991.el && DRILL9991.el.style.display, at: (() => { const [c, r] = player.here(); return [c, r, roomAt(c, r)]; })() })" % ((D - 1) * 1440, (D - 1) * 1440)))
            print('  after', b)
            if st[3] == 'junior': check([n for n in b['notes'] if n[3] == D] == [['drill', 0, True, D]] and b['use'] == use0 + 1, 'Day %d: the turnout counted (note, reputation %s -> %s)' % (D, use0, b['use']))
            check(b['star'] == 'none', 'Day %d: the star gone after you joined' % D)
            check(b['at'][1] == 4 and 14 <= b['at'][0] <= 19, 'Day %d: you on the muster line (%s)' % (D, b['at']))
        until(g, (D - 1) * 1440 + 916)
        c = json.loads(g.ev(LINE)); t = json.loads(g.ev("JSON.stringify(window.__toasts.filter(x => x[0] >= %d))" % ((D - 1) * 1440 + 914)))
        s = json.loads(g.ev("JSON.stringify(window.__said.filter(x => x[0] >= %d && x[1] === 'calder'))" % ((D - 1) * 1440 + 914)))
        nn = json.loads(g.ev("JSON.stringify([simNotes('drill', %d).map(n => [n.mins, n.you]), SHIP.works.use.m3d || 0])" % ((D - 1) * 1440)))
        print('  15:1x', c, t, s, nn)
        check(any('All clear' in (x[2] or '') for x in t), 'Day %d: the all-clear' % D)
        check(all(x == 'off-deck' or x[0] is None for x in (c['calder'], c['zeke'], c['hall'])), 'Day %d: the holds let go' % D)
        if MISS: check(nn[0][-1:] == [[None, False]] and nn[1] == use0 and any('without you' in x[2] for x in s + [[0, 0, y[2]] for y in t]), 'Day %d: missed: the note, no reputation, her word (%s)' % (D, nn))
        check(not g.errors, 'Day %d: no errors (%s)' % (D, g.errors[:3]))
        g.close()
print('DRILL PROBE', 'OK' if not FAILS else 'FAILED: ' + '; '.join(FAILS))
