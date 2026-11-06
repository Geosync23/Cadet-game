# TB6 probe (0.99.7 note 51): the Spice shelf supper from a fresh game, as a player meets it. Day D from 17:00 in the mess.
# ON=1: a switched-on copy; END=minute to stop; INTRO=1: a fresh save with the intro on (newGameStart(true)), then the day.
#   ON=1 INTRO=1 END=1215 python3 plans/tb6-probes/spice_fresh.py BUILD [day] [tapAt]
import sys, json, os, pathlib
sys.argv[0] = str(pathlib.Path(__file__).resolve().parents[2] / 'cadet_test.py')
exec(open(sys.argv[0]).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
END = int(os.environ.get('END', '1170')); ON = os.environ.get('ON'); build = sys.argv[1]; D = int(sys.argv[2]) if len(sys.argv) > 2 else 2; TAP = int(sys.argv[3]) if len(sys.argv) > 3 else 1100
HOOK2 = """(() => { window.__said = []; window.__toasts = [];
  const bs = bubbleSay; bubbleSay = function (who, text, secs) { if (who && who.p) window.__said.push([SHIP.time.min, who.p.id, text]); return bs.apply(this, arguments); };
  const ts = toast; toast = function (a, b) { window.__toasts.push([SHIP.time.min, a, b]); return ts.apply(this, arguments); }; })()"""
INROOM = """(() => { const tl = ROOM_TILES['M'], c = cellPos(...tl[Math.floor(tl.length / 2)]); player.obj.position.copy(cellPos(...nearestOpen(c.x, c.z, player))); player.stop(); return 'M'; })()"""
if ON:
    src = pathlib.Path(build).read_text(); on = src.replace("const TRAD997_ON = false ||", "const TRAD997_ON = true ||", 1); assert on != src
    build = str(WORK / 'test' / ('_t997_%d.html' % os.getpid())); pathlib.Path(build).write_text(on)
with sync_playwright() as pw:
    g = Game(pw, build, 390, 844)
    if os.environ.get('INTRO'):   # (lead 49) a fresh save with the intro on: the arrival, then on to the day
        g.ev('localStorage.clear()'); g.ev('newGameStart(true)'); g.step(5)
        print('intro', g.ev("JSON.stringify([introOn(), SHIP.intro.step, SHIP.time.day, Math.round(SHIP.time.min)])"))
    print('day', g.ev("[SHIP.time.day, SHIP.time.min]"), 'weekday', g.ev("weekday(%d)" % D))
    print('event', g.ev("JSON.stringify(eventsOn(%d).filter(x => /spice|dinner|supper/.test(x.id)).map(x => [x.id, x.from, x.to]))" % D))
    g.ev("(() => { skipTo(%d * 1440 + 1020); goToDeck(3, null); for (const k of NEED_KEYS) SHIP.player.needs[k] = 80; })()" % (D - 1)); g.ev(HOOK2); g.step(5); g.ev(INROOM)
    last = None; tapped = False
    for i in range(1200):
        g.step(10)
        x = json.loads(g.ev("""JSON.stringify((() => { const b = DECK_CREW.find(a => a.p.id === 'brennan');
          return [SHIP.time.min, b ? (b.spot ? b.spot.id : b.goalId || 'walking') : 'off-deck', TJ_NOW ? TJ_NOW.e.id + ':' + TJ_NOW.lead : null, ACT ? ACT.kind + ':' + ACT.phase : null, SPICE995.step, SPICE995.t0, roomAt(...player.here()), !!DIALOGUE && DIALOGUE.id, (DECK_CREW.filter(a => evTagId(a.tag || '') === 'spice-shelf-supper')).length]; })())"""))
        k = x[1:]
        if k != last: print(' ', x); last = k
        if not tapped and x[0] >= TAP:
            tapped = True; print('TAP', g.ev("(() => { const a = DECK_CREW.find(a => a.p.id === 'brennan'); return a ? tradJoinTap(a) : 'no brennan'; })()"))
        if x[7] and ('spice' in str(x[7]) or 't932.join' in str(x[7])): g.ev("(() => { let n = 0; while (DIALOGUE && n++ < 10) { const v = dialogueView(); dialogueStep(v && v.choices ? 0 : undefined); } })()")
        if x[0] >= END: break
    if os.environ.get('INTRO'): print('intro after', g.ev("JSON.stringify([introOn(), SHIP.intro.step, Object.keys(SHIP.intro.done).filter(k => /^d2/.test(k)), SHIP.events.joined.filter(k => /spice/.test(k))])"))
    r = json.loads(g.ev("JSON.stringify({ said: window.__said.filter(s => s[1] === 'brennan' || /spice|jar|guess/i.test(s[2])), toasts: window.__toasts })"))
    for s in r['said']: print('  said', s)
    for t in r['toasts']: print('  toast', t)
    print('errors', g.errors[:5]); g.close()
