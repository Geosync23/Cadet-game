# TB6 probe (0.99.7 notes 50, 51): a hosted tradition on a switched-on copy: from FROM on day D on DECK, you in ROOM; a
# tap on HOST at TAP; the card (lines, question) answered at PACE real seconds a line; then your activity, the bubbles,
# the toasts, Sato/Brennan held at their spot, to END. Prints what it saw; checks: the card opened with >= 4 lines, you
# joined, your activity started in ROOM, the host spoke at least once after the card, no page errors.
#   python3 plans/tb6-probes/hosted.py BUILD id day deck room host from tap end [pace]
import sys, json, os, pathlib, re
sys.argv[0] = str(pathlib.Path(__file__).resolve().parents[2] / 'cadet_test.py')
exec(open(sys.argv[0]).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
build, TID, D, DECK, ROOM, HOST, FROM, TAP, END = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], sys.argv[6], int(sys.argv[7]), int(sys.argv[8]), int(sys.argv[9])
PACE = float(sys.argv[10]) if len(sys.argv) > 10 else 1.0
src = pathlib.Path(build).read_text(); on = src.replace("const TRAD997_ON = false ||", "const TRAD997_ON = true ||", 1); assert on != src, 'no TRAD997_ON switch'
won = WORK / 'test' / ('_hosted_%d.html' % os.getpid()); won.write_text(on)
FAILS = []
def check(c, m):
    print(('ok   ' if c else 'FAIL ') + m)
    if not c: FAILS.append(m)
HOOK2 = """(() => { window.__said = []; window.__toasts = []; window.__cards = [];
  const bs = bubbleSay; bubbleSay = function (who, text, secs) { if (who && who.p) window.__said.push([Math.round(SHIP.time.min), who.p.id, text]); return bs.apply(this, arguments); };
  const ds = dialogueShow; dialogueShow = function (id, m) { const r = ds.apply(this, arguments); window.__cards.push([id, Math.round(SHIP.time.min), (MEETING_SCRIPTS[id] || {lines: []}).lines.map(l => l.choice ? '[choice] ' + l.choice.map(c => c.text).join(' / ') : l.who + ': ' + l.text)]); return r; };
  const ts = toast; toast = function (a, b) { window.__toasts.push([Math.round(SHIP.time.min), a, b]); return ts.apply(this, arguments); }; })()"""
INROOM = """(() => { const tl = ROOM_TILES['%s'], c = cellPos(...tl[Math.floor(tl.length / 2)]); player.obj.position.copy(cellPos(...nearestOpen(c.x, c.z, player))); player.stop(); return 1; })()""" % ROOM
with sync_playwright() as pw:
    g = Game(pw, str(won), 390, 844)
    print('event', g.ev("JSON.stringify(eventsOn(%d).filter(x => x.id === '%s').map(x => [x.id, x.from, x.to]))" % (D, TID)))
    g.ev("(() => { skipTo(%d * 1440 + %d); goToDeck(%d, null); for (const k of NEED_KEYS) SHIP.player.needs[k] = 80; })()" % (D - 1, FROM, DECK)); g.ev(HOOK2); g.step(5); g.ev(INROOM)
    last = None; tapped = False; joined = False; acts = []
    for i in range(3000):
        g.step(10)
        x = json.loads(g.ev("""JSON.stringify((() => { const b = DECK_CREW.find(a => a.p.id === '%s');
          return [Math.round(SHIP.time.min), b ? (b.spot ? b.spot.id : 'walking') : 'off-deck', TJ_NOW ? TJ_NOW.e.id + ':' + TJ_NOW.lead : null, ACT ? ACT.kind + ':' + ACT.phase + ':' + (ACT.placeId || '-') + ':' + (ACT.o.pose || '') : null, !!DIALOGUE && DIALOGUE.id, roomAt(...player.here())]; })())""" % HOST))
        if x[1:] != last: print(' ', x); last = x[1:]
        if x[3]: acts.append((x[0], x[3], x[5]))
        if not tapped and x[0] >= TAP:
            tapped = True; print('TAP', g.ev("(() => { const a = DECK_CREW.find(a => a.p.id === '%s'); return a ? tradJoinTap(a) : 'no host'; })()" % HOST))
        if x[4]:
            n = 0
            while g.ev("!!DIALOGUE") and n < 20:
                g.step(max(1, int(PACE * 30))); g.ev("(() => { const v = dialogueView(); dialogueStep(v && v.choices ? 1 : undefined); })()"); n += 1
        if x[0] >= END: break
    r = json.loads(g.ev("JSON.stringify({ said: window.__said, toasts: window.__toasts, cards: window.__cards, joined: SHIP.events.joined.filter(k => k.startsWith('%s@')) })" % TID))
    for c in r['cards']:
        print('  card', c[0], c[1]); [print('     ', l) for l in c[2]]
    for s in r['said']: print('  said', s)
    for t in r['toasts']: print('  toast', t)
    check(any(len(c[2]) >= 4 for c in r['cards']), 'the host\'s card with at least 4 lines')
    check(bool(r['joined']), 'joined (%s)' % r['joined'])
    check(any(a[2] == ROOM and ':do:' in a[1] for a in acts), 'your activity in room %s (%s)' % (ROOM, acts[-1:] if acts else None))
    cardAt = min([c[1] for c in r['cards']] or [9999])
    check(any(s[1] == HOST and s[0] >= cardAt for s in r['said']), 'the host spoke after the card')
    check(not g.errors, 'no errors %s' % g.errors[:3])
    g.close()
won.unlink(missing_ok=True)
print('HOSTED PROBE ' + ('OK' if not FAILS else 'FAILED (%d)' % len(FAILS)))
