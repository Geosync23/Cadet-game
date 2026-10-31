# TB3 probe for 0.99.5 note 19 (Spice shelf supper, tap to join), on a copy with TRAD995_ON switched on.
# For each Tuesday given (default 2 9 16): from 18:12 in the mess hall, the marker over Brennan and the arrow at her from
# 18:15; Brennan at the spice shelf and kept there to 19:15; a tap on her joins you, sits you at a free mess seat with your
# dinner, one join notice; her opening, the three jars, the guesses and the three reveals as bubbles (each jar's line in
# its place, the spice small mid-sentence, no guess naming its speaker); the card once the jars are named, the reveal
# after it. Then a save and reload mid-supper (saving on): the card again after the jars. No page errors.
#   python3 plans/tb3-probes/spice995.py starship-cadet.html [day ...]
import sys, json, re, os, pathlib
sys.argv[0] = str(pathlib.Path(__file__).resolve().parents[2] / 'cadet_test.py')
exec(open(sys.argv[0]).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

build = sys.argv[1]; DAYS = [int(x) for x in sys.argv[2:]] or [2, 9, 16]
src = pathlib.Path(build).read_text()
on = src.replace("const TRAD995_ON = false ||", "const TRAD995_ON = true ||", 1); assert on != src, 'no TRAD995_ON switch'
won = WORK / 'test' / ('_spice995_%d.html' % os.getpid()); won.write_text(on)
FAILS = []
def check(c, m):
    print(('ok   ' if c else 'FAIL ') + m)
    if not c: FAILS.append(m)

SAYHOOK = """(() => { window.__said = []; window.__cards = []; window.__toasts = []; if (window.__hook) return; window.__hook = 1;
  const bs = bubbleSay; bubbleSay = function (who, text, secs) { if (who && who.p) window.__said.push([who.p.id, text, SHIP.time.min]); return bs.apply(this, arguments); };
  const ds = dialogueShow; dialogueShow = function (id, m) { window.__cards.push([id, SHIP.time.min]); return ds.apply(this, arguments); };
  const ts = toast; toast = function (a, b) { window.__toasts.push([a, b, SHIP.time.min]); return ts.apply(this, arguments); };
  if (typeof GUIDE_ON !== 'undefined' && GUIDE_ON) { GUIDE.tq.length = 0; guideToast = () => false; } })()"""
INROOM = """(() => { const tl = ROOM_TILES['M'], c = cellPos(...tl[Math.floor(tl.length / 2)]); player.obj.position.copy(cellPos(...nearestOpen(c.x, c.z, player))); player.stop(); return 'M'; })()"""
STATE = """JSON.stringify((() => { const b = DECK_CREW.find(a => a.p.id === 'brennan'), mk = document.getElementById('tjMark');
  return [SHIP.time.min, b && b.spot ? b.spot.id : null, b ? !!b.settled : null, !!DIALOGUE && DIALOGUE.id, TJ_NOW ? TJ_NOW.lead : null, !!mk && mk.style.display !== 'none' && /Brennan/.test(mk.textContent),
    IX_GOAL && IX_GOAL.tj ? IX_GOAL.crew : null, ACT ? [ACT.kind, ACT.placeId, ACT.phase, !!ACT.o.fed, ACT.o.dish || null] : null, SPICE995.step]; })())"""

def supper(pw, d):
    print('--- Day %d (weekday %s)' % (d, '?'))
    g = Game(pw, str(won), 900, 760)
    wd = g.ev("weekday(%d)" % d); on_ = g.ev("eventsOn(%d).some(x => x.id === 'spice-shelf-supper')" % d)
    check(wd == 1 and on_, 'Day %d is a Tuesday with the supper (%s, %s)' % (d, wd, on_))
    if not on_: g.close(); return
    g.ev("(() => { skipTo(%d * 1440 + 1080); goToDeck(3, null); SHIP.device.settings.tips = false; for (const k of NEED_KEYS) SHIP.player.needs[k] = 95; clearGoal(); })()" % (d - 1)); g.ev(SAYHOOK); g.step(5)
    g.ev(INROOM)
    first = {}; tapped = None; spots_after = []; card_at = None; picked = False
    for i in range(400):
        g.step(20)
        x = json.loads(g.ev(STATE)); m = x[0]
        if x[4] == 'brennan' and 'lead' not in first: first['lead'] = m
        if x[5] and 'mark' not in first: first['mark'] = m
        if x[6] == 'brennan' and 'arrow' not in first: first['arrow'] = m
        if x[1] == '3-spice-host' and x[2] and 'shelf' not in first: first['shelf'] = m
        if tapped is None and m >= 1101:
            tapped = m; r = json.loads(g.ev("""JSON.stringify((() => { window.__toasts.length = 0; const a = DECK_CREW.find(a => a.p.id === 'brennan'); const ok = tradJoinTap(a);
              return [ok, SHIP.events.joined.includes('spice-shelf-supper@%d'), ACT ? [ACT.kind, ACT.placeId, !!ACT.o.fed, ACT.o.dish, (PLACE_OF.get(ACT.placeId) || {}).type] : null]; })())""" % d))
            print('  tap at %d: %s' % (m, r))
            check(r[0] and r[1], 'Day %d: the tap on Brennan joins you' % d)
            check(bool(r[2]) and r[2][0] == 'eat' and r[2][2] and r[2][4] == 'mess-seat', 'Day %d: sat at a free mess seat with your dinner (%s)' % (d, r[2]))
        if tapped is not None: spots_after.append((m, x[1]))
        if x[3] == 'spice.guess' and card_at is None: card_at = m
        if card_at is not None and not picked and m >= card_at + 2:
            picked = True; g.ev("(() => { let n = 0; while (DIALOGUE && n++ < 10) { const v = dialogueView(); dialogueStep(v && v.choices ? 0 : undefined); } })()")
        if m >= 1150: break
        if i % 10 == 0: g.ev("for (const k of NEED_KEYS) SHIP.player.needs[k] = Math.max(SHIP.player.needs[k], 70)")
    r = json.loads(g.ev("JSON.stringify({ said: window.__said, cards: window.__cards, toasts: window.__toasts, jars: spiceWeek(%d), ask: (MEETING_SCRIPTS['spice.guess'] || {lines: [{}]}).lines[0].text || null })" % d))
    print('  first:', first, ' card at', card_at)
    check(first.get('lead') is not None and first['lead'] < 1096 and first.get('mark') is not None and first['mark'] < 1096, 'Day %d: the marker over Brennan from 18:15 (%s)' % (d, first))
    check(first.get('arrow') is not None and first['arrow'] < 1096, 'Day %d: the arrow at Brennan from 18:15 (%s)' % (d, first.get('arrow')))
    check(first.get('shelf') is not None and first['shelf'] <= 1096, 'Day %d: Brennan at the spice shelf early (%s)' % (d, first.get('shelf')))
    off = [s for s in spots_after if s[1] != '3-spice-host']
    check(not off, 'Day %d: Brennan stays at the shelf after the tap to the end (%s)' % (d, off[:4]))
    joins = [t for t in r['toasts'] if t[0] == 'Spice shelf supper' and 'Social and leisure up' in (t[1] or '')]
    check(len(joins) == 1, 'Day %d: the join notice once (%s)' % (d, [t[:2] for t in r['toasts']]))
    b = [s for s in r['said'] if s[0] == 'brennan']; o = [s for s in r['said'] if s[0] != 'brennan']
    for s in r['said']: print('   %d %-14s %s' % (s[2], s[0], s[1]))
    check(len(b) == 7, 'Day %d: Brennan opens, names three jars, says whose each was (%d lines)' % (d, len(b)))
    check(len(r['said']) >= 15, 'Day %d: at least 15 bubbles (%d)' % (d, len(r['said'])))
    jl = b[1:4]
    check(len(jl) == 3 and not re.match(r'Last\b', jl[0][1]) and not re.match(r'First\b', jl[2][1]) and not re.match(r'(First|Last)\b', jl[1][1]) and len({x[1] for x in jl}) == 3, 'Day %d: each jar line in its place, three different' % d)
    sp = [j[1] for j in r['jars']]
    bad = [s[1] for s in r['said'] + [['', r['ask'] or '']] for v in sp if re.search(r'[a-z,] ' + re.escape(v[0].upper() + v[1:]), s[1]) or re.match(re.escape(v), s[1])]
    check(not bad, 'Day %d: the spice small mid-sentence, a capital at the start (%s)' % (d, bad))
    names = {p['id']: p['n'] for p in g.ev("schedPeople().map(p => ({ id: p.id, n: shortName(p) }))")}
    selfg = [s for s in o if names.get(s[0]) and re.search(r'\b' + re.escape(names[s[0]]) + r'\b', s[1])]
    check(not selfg, 'Day %d: no guess names its own speaker (%s)' % (d, selfg))
    rev = [s[2] for s in b[4:]]
    check(card_at is not None and all(t >= card_at for t in rev) and card_at >= b[3][2], 'Day %d: the card after the last jar (%s), the reveals after it (%s)' % (d, card_at, rev))
    check(not g.errors, 'Day %d: no errors %s' % (d, g.errors[:3]))
    g.close()

def reload(pw, d):
    print('--- reload, Day %d' % d)
    tmp = WORK / 'test' / ('_spice995_save_%d.html' % os.getpid()); tmp.write_text(instrument(on))
    errs = []
    br = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    page = br.new_page(viewport={'width': 900, 'height': 760}); page.on('pageerror', lambda e: errs.append(str(e)))
    page.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    page.add_init_script(INIT)
    def load():
        page.goto('file://' + str(tmp)); page.wait_for_function('window.__sc !== undefined', timeout=120000); page.evaluate('s => window.__sc(s)', SKIP_SWITCH)
    ev = lambda x: page.evaluate('s => window.__sc(s)', x)
    step = lambda n: page.evaluate(f'window.__skip = true; window.__step({n}, {1000/30}); window.__skip = false')
    load(); ev("localStorage.clear()"); load()
    ev("(() => { newGameStart(false); skipTo(%d * 1440 + 1100); goToDeck(3, null); SHIP.device.settings.tips = false; for (const k of NEED_KEYS) SHIP.player.needs[k] = 95; clearGoal(); })()" % (d - 1)); ev(INROOM); step(200)
    r0 = ev("(() => { const a = DECK_CREW.find(a => a.p.id === 'brennan'); return [tradJoinTap(a), SHIP.events.joined.includes('spice-shelf-supper@%d'), SPICE.joined, SPICE995.step]; })()" % d)
    ev("saveGame()"); sv = json.loads(ev("localStorage.getItem(SAVE_KEY)"))
    print('  joined', r0, 'saved spice', sv['ship'].get('spice'))
    load(); ev(SAYHOOK); ev("goToDeck(3, null)"); ev(INROOM)
    ld = ev("[SPICE.joined, SPICE.asked, SHIP.time.day, SHIP.time.min]")
    card = None
    for i in range(200):
        step(20); x = ev("[SHIP.time.min, !!DIALOGUE && DIALOGUE.id, deckDef.num, roomAt(...player.here()), JSON.stringify(SPICE995), (DECK_CREW.find(a => a.p.id === 'brennan') || {}).goalId || null]")
        if i % 15 == 0: print('   ', x)
        if x[1] == 'spice.guess': card = x[0]; break
        if x[0] >= 1150: break
    print('  loaded', ld, 'card at', card)
    check(sv['ship'].get('spice', {}).get('joined') == d and ld[0] == d, 'reload Day %d: joined kept through a save (%s, %s)' % (d, sv['ship'].get('spice'), ld))
    check(card is not None, 'reload Day %d: the guess card after the reload (%s)' % (d, card))
    ev("(() => { let n = 0; while (DIALOGUE && n++ < 10) { const v = dialogueView(); dialogueStep(v && v.choices ? 0 : undefined); } saveGame(); })()")
    load(); ev("goToDeck(3, null)"); ev(INROOM); ev(SAYHOOK)
    for i in range(80): step(20)
    again = ev("window.__cards.filter(c => c[0] === 'spice.guess').length")
    check(again == 0, 'reload Day %d: answered, not asked again after another reload (%s)' % (d, again))
    check(not errs, 'reload: no errors %s' % errs[:3])
    ev("localStorage.clear()"); br.close(); tmp.unlink(missing_ok=True)

with sync_playwright() as pw:
    for d in DAYS: supper(pw, d)
    reload(pw, DAYS[0])
won.unlink(missing_ok=True)
print('SPICE995 PROBE ' + ('OK' if not FAILS else 'FAILED (%d)' % len(FAILS)))
