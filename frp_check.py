# Starship Cadet: the Fable review's fixes (FR2, plans/review-fable-play.md), each with its switch off and on.
#   python3 frp_check.py [BUILD.html] [part ...]      (parts: line food tray pin lead thanks words say panels label blink tips; no part = all)
# Each part makes two copies of the build, that fix's `var FRP_..._ON = ...;` line set to false and to true, whichever
# way the build has it (so a candidate with the switches on is checked as it is). Dev mode's own save (the
# real save is never touched). Setup as cadet_test.py (three r128 under $CADET_WORK); CADET_CHROME names the browser.
import sys, os, json, pathlib, math, re
args = [a for a in sys.argv[1:]]; BUILD = args[0] if args and args[0].endswith('.html') else 'starship-cadet.html'
FRP_PARTS = [a for a in args if not a.endswith('.html')]
sys.argv = [sys.argv[0], BUILD]
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'arrows_check.py')).read().split('\nwith sync_playwright() as pw:')[0])
FAILS = []
def ok(cond, msg):
    print(('  ok   ' if cond else '  FAIL ') + msg, flush=True)
    if not cond: FAILS.append(msg)
def switched(src, *names, on=True):                     # the build with these switches on (or off), whichever way the file has them
    for n in names:
        hits = re.findall(r'var ' + n + r' = (?:false|true);', src); assert len(hits) == 1, n
        src = src.replace(hits[0], f'var {n} = {"true" if on else "false"};')
    return src
def page(ctx, src, tag):
    p = WORK / 'test' / f'_frp_{os.getpid()}_{tag}.html'; p.write_text(src); return Page(ctx, str(p))
def jump(pg, day, hm):                                  # the career as at that day, then the clock to hm
    pg.ev(f"devmodeRun('Set career to Day {day}', () => devmodeSetCareerTo({day}))"); pg.step(20)
    pg.ev(f"devmodeRun('skip', () => devmodeSkipTo({(day - 1) * 1440 + hm}))"); pg.step(30)
ARROW = "(() => { const g = goalNow(); return g ? g.label : null; })()"

def part_line(ctx, src):                                # F1: the Line oath's arrow, the honest Mail, the invitation's name
    for on in (False, True):
        pg = page(ctx, switched(src, 'FRP_LINE_ON', on=on), 'line' + str(int(on))); tag = 'on: ' if on else 'off: '
        jump(pg, 7, 14 * 60 + 20); pg.step(120)
        a = pg.ev(ARROW)
        ok((a is not None and 'Line oath' in a) == on, tag + f'the arrow at 14:2x {"is" if on else "is not"} the oath ({a!r})')
        if on: ok(pg.ev("(() => { const g = goalNow(); return g.deck === 3 && g.room === 'L'; })()"), tag + 'it points at the bow lounge, Deck 3')
        shot(pg, 'f1-line-' + ('after' if on else 'before'))
        ok(pg.ev("frpInviteWhat({ trad: TRADITIONS[0].id })") == ((': ' + pg.ev('TRADITIONS[0].name')) if on else ''), tag + 'an invitation heads-up ' + ('names its tradition' if on else 'is as before'))
        for k in range(80):                              # stay in the bunk room through the oath (14:40-14:55; its notes come at 15:15)
            pg.step(60, 50)
            if pg.ev('shipNow()') >= 6 * 1440 + 15 * 60 + 22: break
        m = pg.ev("(SHIP.mail || []).filter(m => /Line oath/.test(m.subject)).map(m => m.body)")
        ok(len(m) == 1, tag + f'one Line oath Mail after missing it ({len(m)})')
        ok(bool(m) and ('without you' in m[0]) == on and ('you answered' in m[0]) == (not on), tag + ('the Mail says you were not there' if on else 'the Mail is the old gist'))
        a = pg.ev(ARROW); ok(not (a and 'Line oath' in a), tag + f'no oath arrow after it ends ({a!r})')
        if on:                                           # going: the arrow goes once you are in the oath
            pg2 = page(ctx, switched(src, 'FRP_LINE_ON'), 'line2'); jump(pg2, 7, 14 * 60 + 36)
            pg2.ev("(() => { goToDeck(3); const w = ixGoalWorld(goalNow()); const gl = nearestOpen(w.x, w.z, player); player.obj.position.copy(cellPos(...gl)); player.stop(); })()")
            for k in range(30):
                pg2.step(40, 50)
                if pg2.ev('!!DIALOGUE'): break
            ok(pg2.ev("!!DIALOGUE && DIALOGUE.id === 'crossingCeremony'"), 'on: in the lounge at 14:40 the oath opens')
            pg2.step(5); a = pg2.ev(ARROW); ok(not (a and 'Line oath' in a), f'on: the arrow goes once you are in it ({a!r})')
            pg2.ev('dialogueEnd(true)'); pg2.step(400, 50)
            m = pg2.ev("(SHIP.mail || []).filter(m => /Line oath/.test(m.subject)).map(m => m.body)")
            ok(not any('without you' in x for x in m), 'on: no "without you" Mail when you went')
            ok(not pg2.errors, f'on: no page errors {pg2.errors[:2]}')
        ok(not pg.errors, tag + f'no page errors {pg.errors[:2]}')

TOASTS = "(() => { window.__t = []; const ts = toast; toast = function (a, b) { window.__t.push(String(a)); return ts.apply(this, arguments); }; })()"
def part_food(ctx, src):                                # F2: Food under 10 and staying there
    res = {}
    for on in (False, True):
        pg = page(ctx, switched(src, 'FRP_FOOD_ON', on=on), 'food' + str(int(on))); tag = 'on: ' if on else 'off: '
        jump(pg, 2, 6 * 60 + 5); pg.ev(TOASTS)
        pin = "SHIP.player.needs.hunger = 5; for (const k of NEED_KEYS) if (k !== 'hunger') SHIP.player.needs[k] = 90;"
        def run(until):
            while pg.ev('shipNow()') < 1440 + until: pg.ev(pin); pg.step(40, 50)
        run(6 * 60 + 40); n1 = pg.ev("window.__t.filter(x => x === 'Very hungry').length")
        ok(n1 == 1, tag + f'the firm warning once by 06:40 ({n1})')
        a = pg.ev(ARROW); ok(a is not None and a.startswith('Food'), tag + f'its marker is up ({a!r})')
        ok(pg.ev("(() => { needGoalClear(); clearGoal(); return goalNow(); })()") is None, tag + 'marker cleared (as if another arrow had held it off)')
        run(6 * 60 + 52); a = pg.ev(ARROW)
        ok((a is not None and a.startswith('Food')) == on, tag + f'with no other arrow the Food marker {"comes back" if on else "stays away"} ({a!r})')
        run(7 * 60 + 20); n2 = pg.ev("window.__t.filter(x => x === 'Very hungry').length")
        ok(n2 == (2 if on else 1), tag + f'as breakfast opens the warning is {"said again" if on else "not said again"} ({n2})')
        run(7 * 60 + 50); n3 = pg.ev("window.__t.filter(x => x === 'Very hungry').length"); ok(n3 == n2, tag + f'and not again within the same meal ({n3})')
        if on:
            pg.ev("SHIP.player.needs.hunger = 80; needGoalClear(); clearGoal()"); pin = "SHIP.player.needs.hunger = 80;"
            run(8 * 60 + 0); a = pg.ev(ARROW); ok(not (a and a.startswith('Food')), f'on: fed, no Food marker ({a!r})')
        ok(not pg.errors, tag + f'no page errors {pg.errors[:2]}')

SHOTS = os.environ.get('FRP_SHOTS')                     # a folder: before/after pictures land there
def shot(pg, name):
    if not SHOTS: return
    pg.ev('window.__draw = true'); pg.step(1, 20); pg.page.screenshot(path=os.path.join(SHOTS, name + '.png')); pg.ev('window.__draw = false')
def part_tray(ctx, src):                                # F3: a tray in hand: the arrow at a free seat
    for on in (False, True):
        pg = page(ctx, switched(src, 'FRP_TRAY_ON', on=on), 'tray' + str(int(on))); tag = 'on: ' if on else 'off: '
        jump(pg, 2, 17 * 60 + 40)
        pg.ev("(() => { for (const k of NEED_KEYS) SHIP.player.needs[k] = 90; needGoalClear(); clearGoal(); goToDeck(3); })()"); pg.step(10)
        pg.ev("(() => { const it = ITEMS.find(i => /^servery$/i.test(i.t)); it.hit.getWorldPosition(_wp); const gl = nearestOpen(_wp.x, _wp.z, player); player.obj.position.copy(cellPos(...gl)); player.stop(); SHIP.player.tray = 'curry'; SHIP.player.trayLeft = 0; })()")
        pg.step(60, 50); a = pg.ev(ARROW)
        ok((a == 'A seat for your tray') == on, tag + f'tray in hand, Food 90: the arrow {"points at a seat" if on else "is as before"} ({a!r})')
        shot(pg, 'f3-tray-' + ('after' if on else 'before'))
        if on:
            ok(pg.ev("(() => { const pl = placeById(IX_GOAL.place); return pl.type === 'mess-seat' && !heldBy(pl.id); })()"), 'on: a free mess seat')
            s0 = pg.ev('IX_GOAL.place')
            pg.ev("(() => { const far = DECKS[3].places.filter(p => p.type === 'mess-seat' && !heldBy(p.id)).map(p => { const c = cellPos(...p.at), q = player.obj.position; return [Math.hypot(c.x - q.x, c.z - q.z), p]; }).sort((a, b) => b[0] - a[0])[0][1]; const c = cellPos(...far.at), gl = nearestOpen(c.x, c.z, player); player.obj.position.copy(cellPos(...gl)); player.stop(); })()")
            pg.step(60, 50); ok(pg.ev('IX_GOAL && IX_GOAL.place') != s0, 'on: walk across the mess and it points at the seat nearest you now')
            r = pg.ev("(() => { const pl = placeById(IX_GOAL.place), c = cellPos(...pl.at), its = ITEMS.map(i => { i.hit.getWorldPosition(_wp); return [Math.hypot(_wp.x - c.x, _wp.z - c.z), i]; }).sort((a, b) => a[0] - b[0]); return playerTap(its[0][1], new THREE.Vector3(c.x, .5, c.z), new THREE.Vector3(c.x, .5, c.z)); })()")   # the bench or chair at the seat, tapped at the seat
            pg.step(90, 50); ok(pg.ev("!!ACT") and pg.ev(ARROW) != 'A seat for your tray', f'on: tap the seat: you sit to eat and the arrow goes (tap {r!r}, act {pg.ev("ACT && ACT.kind")!r})')
            pg.ev("actEnd(true); SHIP.player.tray = null"); pg.step(60, 50); ok(pg.ev(ARROW) != 'A seat for your tray', 'on: no tray, no seat arrow')
            pg.ev("SHIP.player.tray = 'curry'; setGoal({ deck: 5, room: 'w', label: 'someone else' })"); pg.step(60, 50); ok(pg.ev(ARROW) == 'someone else', 'on: never over another arrow')
        ok(not pg.errors, tag + f'no page errors {pg.errors[:2]}')

HOOKS = "(() => { window.__h = []; const co = chatOpen; chatOpen = function (p) { window.__h.push('chat:' + (p && p.id)); return co.apply(this, arguments); }; const pt = playerTap; playerTap = function (it) { window.__h.push('thing:' + (it && it.t)); return pt.apply(this, arguments); }; })()"
# a settled person with a place (and a thing at it) right beside them, where a tap on the pin's label would be theirs
FIND_SPOT = r"""(() => { const out = []; for (const a of DECK_CREW) { if (!a.p || !a.settled) continue;
  for (const pl of DECKS[deckDef.num].places || []) { const c = cellPos(...pl.at), d = Math.hypot(c.x - a.x, c.z - a.z); if (d > 1.1 || d < .2 || privatePlace(pl)) continue;
    let it = null, bd = 1.6; for (const i of ITEMS) { if (!i.hit || i.lift) continue; i.hit.getWorldPosition(_wp); const q = Math.hypot(_wp.x - c.x, _wp.z - c.z); if (q < bd) { bd = q; it = i; } }
    if (it) out.push([a.p.id, pl.id, it.t, c.x, c.z]); } } return out.slice(0, 12); })()"""
def part_pin(ctx, src):                                 # F4: beside the arrow's pin, the arrow's target before a bystander
    for on in (False, True):
        pg = page(ctx, switched(src, 'FRP_PINTAP_ON', on=on), 'pin' + str(int(on))); tag = 'on: ' if on else 'off: '
        jump(pg, 2, 10 * 60 + 30); pg.ev("goToDeck(5); for (const k of NEED_KEYS) SHIP.player.needs[k] = 90; needGoalClear(); clearGoal(); SHIP.player.track = null"); pg.step(40); pg.ev(HOOKS)
        done = False
        for who, place, thing, x, z in pg.ev(FIND_SPOT):
            pg.ev(f"(() => {{ const gl = nearestOpen({x} + 1.5, {z} + 1.5, player); player.obj.position.copy(cellPos(...gl)); player.stop(); setGoal({{ deck: deckDef.num, place: {json.dumps(place)}, label: 'A test stop' }}); }})()")
            pg.ev('window.__draw = true'); pg.step(12, 30); pg.ev('window.__draw = false')
            pt = pg.ev("(() => { if (performance.now() - IX_PIN.t >= 500) return null; const x = IX_PIN.x, y = IX_PIN.y + 12, a = crewAtScreen(x, y); return a ? [x, y, a.p.id] : null; })()")
            if not pt or pt[1] < 215 or pt[1] > 700: continue   # the pin must be someone's tap, and clear of the HUD
            pg.ev('window.__h.length = 0; if (typeof CHAT !== "undefined" && CHAT) chatClose()'); pg.page.mouse.click(pt[0], pt[1]); pg.step(6, 30); h = pg.ev('window.__h')
            ok(any(x.startswith('thing:') for x in h) == on and any(x.startswith('chat:') for x in h) == (not on), tag + f'a tap on the pin with {pt[2]} standing there goes to {"the thing it points at" if on else "them, as before"} ({h}; {thing})')
            # away from the pin, on the person: theirs either way
            far = pg.ev(f"(() => {{ const a = DECK_CREW.find(x => x.p && x.p.id === {json.dumps(pt[2])}); _cp.set(a.x, a.y + 1, a.z).project(camera); const x = (_cp.x + 1) / 2 * innerWidth, y = (1 - _cp.y) / 2 * innerHeight; clearGoal(); return [x, y]; }})()")
            pg.ev('if (ACT) actEnd(true); if (DEV.open) deviceClose(); if (typeof CHAT !== "undefined" && CHAT) chatClose(); window.__h.length = 0'); pg.step(8, 30)
            pg.page.mouse.click(far[0], far[1]); pg.step(6, 30); h = pg.ev('window.__h')
            ok(any(x == 'chat:' + pt[2] for x in h), tag + f'with no arrow, a tap on them is theirs ({h})')
            done = True; break
        ok(done, tag + 'found someone standing at a place to test with')
        ok(not pg.errors, tag + f'no page errors {pg.errors[:2]}')

def part_lead(ctx, src):                                # F5: the arrival: a tap on Zeke, or on his arrow, walks you to him
    for on in (False, True):
        pg = page(ctx, switched(src, 'FRP_LEAD_ON', on=on), 'lead' + str(int(on))); tag = 'on: ' if on else 'off: '
        pg.ev('localStorage.clear()'); pg.ev('newGameStart(true)'); pg.step(5)
        pg.page.fill('form input[maxlength="24"]', 'Sam'); pg.page.click('form button'); pg.step(5)
        for k in range(60):                              # Zeke comes to the ramp and waits; his arrow goes up
            pg.step(30, 40)
            if pg.ev("!!IX_GOAL && IX_GOAL.label === 'Zeke Torres' && !!DECK_CREW.find(x => x.p && x.p.id === SHIP.intro.escort)"): break
        ok(pg.ev("!!IX_GOAL && IX_GOAL.label === 'Zeke Torres'"), tag + 'the arrival: the arrow is on Zeke')
        for k in range(60):                              # the ramp comes down a ship minute or two later: till then nothing outside the Tern can be walked to
            if pg.ev("(() => { const t = nearestOpen(cellPos(...IX_GOAL.at).x, cellPos(...IX_GOAL.at).z, player); return [[0, 0], [0, -1], [1, 0], [-1, 0], [0, 1]].some(d => free(t[0] + d[0], t[1] + d[1]) && !!findPath(player.here(), [t[0] + d[0], t[1] + d[1]], null, player)); })()"): break
            pg.step(15, 40)
        ok(pg.ev("document.getElementById('ixGoal').classList.contains('lead')") == on, tag + f'his arrow {"takes" if on else "does not take"} taps')
        P = "(() => { const a = DECK_CREW.find(x => x.p && x.p.id === SHIP.intro.escort), q = player.obj.position; _cp.set(a.x, a.y + 1, a.z).project(camera); return [(_cp.x + 1) / 2 * innerWidth, (1 - _cp.y) / 2 * innerHeight, Math.hypot(a.x - q.x, a.z - q.z), q.x, q.z]; })()"
        pg.ev('window.__draw = true'); pg.step(3, 30); pg.ev('window.__draw = false')
        z = pg.ev(P); shot(pg, 'f5-lead-' + ('after' if on else 'before'))
        if not (20 < z[0] < 370 and 215 < z[1] < 700): ok(False, tag + f'Zeke is on screen to tap ({z})')
        else:
            pg.page.mouse.click(z[0], z[1]); pg.step(90, 40); z2 = pg.ev(P); moved = math.hypot(z2[3] - z[3], z2[4] - z[4])
            ok(z[2] > 3, tag + f'he is across the bay ({z[2]:.1f})')
            ok((moved > .5) == on, tag + f'a tap on him {"walks you over" if on else "is his description, no step"} (moved {moved:.2f})')
        if on:
            for k in range(30):
                pg.step(30, 40)
                if pg.ev(P)[2] <= 3: break
            pg.ev("player.stop(); window.__t = []; const ts = toast; toast = function (a) { window.__t.push(String(a)); return ts.apply(this, arguments); }")
            z = pg.ev(P)
            if z[2] <= 3 and 20 < z[0] < 370 and 215 < z[1] < 700:
                q0 = z[3:5]; pg.page.mouse.click(z[0], z[1]); pg.step(10, 40); z2 = pg.ev(P)
                ok(pg.ev("window.__t.includes('Zeke Torres')"), 'on: beside him, a tap is his usual card')
            # his arrow itself: from far away again
            pg.ev("(() => { const gl = nearestOpen(5, 7, player); player.obj.position.copy(cellPos(5, 7)); player.stop(); })()"); pg.ev('window.__draw = true'); pg.step(6, 30); pg.ev('window.__draw = false')
            r = pg.ev("(() => { const el = document.getElementById('ixGoal'), k = [...el.children].find(c => getComputedStyle(c).display !== 'none' && c.getBoundingClientRect().width > 1), b = k.getBoundingClientRect(); return [b.left + b.width / 2, b.top + b.height / 2, k.className]; })()")
            q0 = pg.ev('[player.obj.position.x, player.obj.position.z]'); pg.page.mouse.click(r[0], r[1]); pg.step(60, 40); q1 = pg.ev('[player.obj.position.x, player.obj.position.z]')
            ok(math.hypot(q1[0] - q0[0], q1[1] - q0[1]) > .5, f'on: a tap on his arrow ({r[2]}) walks you toward him')
        ok(not pg.errors, tag + f'no page errors {pg.errors[:2]}')

def part_thanks(ctx, src):                              # F9: no form thank-you Mail after a one-off, or from the Captain
    pg = page(ctx, switched(src, 'FRP_THANKS_ON'), 'thanksF'); jump(pg, 2, 9 * 60)
    t = pg.ev("TRADITIONS.map(t => [t.id, frpThanksOk({ ev: t })])"); yes = [a for a, b in t if b]; no = [a for a, b in t if not b]
    print('   thanked:', ' '.join(yes)); print('   not thanked:', ' '.join(no))
    for i in ('name-on-the-beam', 'name-on-the-beam-new', 'captains-address', 'one-week-aboard', 'years-end', 'off-the-tern'): ok(i in no, f'on: no thank-you after {i}')
    for i in ('sunrise-stretch', 'tiles-night', 'knit-and-natter', 'late-piano', 'sunday-table'): ok(i in yes, f'on: still one after {i}')
    ok(pg.ev("frpThanksOk({ ev: { id: 'birthday', when: { birthday: true } } }) === false && frpThanksOk({ ev: { id: 'lastLightGlass' } }) === false"), 'on: none after a birthday or an event\'s gathering')
    for on in (False, True):                             # live: the Last Light with Dr. Sato
        pg = page(ctx, switched(src, 'FRP_THANKS_ON', on=on), 'thanks' + str(int(on))); tag = 'on: ' if on else 'off: '
        jump(pg, 4, 14 * 60 + 9); pg.ev("goToDeck(3)"); pg.step(20)
        for k in range(20):
            r = pg.ev("(() => { const a = DECK_CREW.find(x => x.p && /Sato/.test(x.p.name)); if (!a) return null; const gl = nearestOpen(a.x, a.z, player); player.obj.position.copy(cellPos(...gl)); player.stop(); return tradJoinTap(a); })()")
            if r: break
            pg.step(40, 50)
        ok(bool(r), tag + 'joined the Last Light by a tap on Dr. Sato')
        pg.step(20); n = pg.ev("(SHIP.mail || []).filter(m => m.subject === 'Thanks for coming' && /Last Light/i.test(m.body)).length")
        ok(n == (0 if on else 1), tag + f'"Same time next one?" Mail after it: {n}')
        ok(not pg.errors, tag + f'no page errors {pg.errors[:2]}')

def part_words(ctx, src):                               # F12: the wording slips
    for on in (False, True):
        pg = page(ctx, switched(src, 'FRP_WORDS_ON', on=on), 'words' + str(int(on))); tag = 'on: ' if on else 'off: '
        jump(pg, 2, 9 * 60 + 5)
        ok(pg.ev("frpWords()") == on, tag + 'the switch reads ' + str(on))
        ok(pg.ev("[frpPlural('light relays'), frpPlural('grow lights 2'), frpPlural('oven'), frpPlural('compass'), frpPlural('air scrubber')].join()") == 'true,true,false,false,false', tag + 'plural machines told from singular')
        w = pg.ev("frpTitleWhere('Take medical supplies to the infirmary, Deck 3', 'Deck 3 · infirmary')")
        ok(w.endswith('Deck 3') != on, tag + f'Job taken names the deck {"once" if on else "twice, as before"} ({w!r})')
        ok(pg.ev("frpTitleWhere('Oil the sim bay door', 'Rec deck · sim bay')") == 'Oil the sim bay door', tag + 'a title with no deck is left alone')
        # the Calendar's button
        pg.ev("deviceShow('calendar')"); pg.step(10)
        bt = pg.ev("[...document.querySelectorAll('#devBody button')].map(b => b.textContent.trim())")
        ok(('No reminder' in bt) == on and ("Don't" in bt) == (not on), tag + f'the Calendar button says {"No reminder" if on else "Don" + chr(39) + "t"} ({sorted(set(bt))[:6]})')
        shot(pg, 'f12-calendar-' + ('after' if on else 'before')); pg.ev('deviceClose()')
        # a calibrate chore's title, the grab shelf's plate, and a small job's pop-up (read from the game's own makers)
        cal = pg.ev("(SHIP.jobs || []).map(j => j.title).filter(t => /^Calibrate/.test(t))")
        ok(not on or not any(re.search(r'^Calibrate the .*\d$', t) for t in cal), tag + f'no "Calibrate the oven 2" among today\'s jobs ({cal[:4]})')
        ok(not pg.errors, tag + f'no page errors {pg.errors[:2]}')

def part_say(ctx, src):                                 # F11: three messages that explained nothing
    for on in (False, True):
        pg = page(ctx, switched(src, 'FRP_SAY_ON', on=on), 'say' + str(int(on))); tag = 'on: ' if on else 'off: '
        jump(pg, 2, 9 * 60 + 30); pg.ev("goToDeck(5)"); pg.step(20)
        ok(('board' in pg.ev("frpJobGone()")) == on, tag + 'the job-gone message ' + ('says where it went' if on else 'is as before'))
        r = pg.ev("(() => { const it = ITEMS.find(i => /time clock/i.test(i.t)); it.hit.getWorldPosition(_wp); const gl = nearestOpen(_wp.x, _wp.z, player); player.obj.position.copy(cellPos(...gl)); player.stop(); return playerTap(it, _wp.clone(), _wp.clone()); })()")
        for k in range(20):
            pg.step(10, 40); t = pg.ev("(() => { const c = document.getElementById('clockScreen'); return c && !c.hidden ? c.textContent : ''; })()")
            if t: break
        ok(('began at 09:00' in t) == on and ('Shift starts at 09:00' in t) == (not on), tag + f'the time clock at 09:30 says the shift {"began" if on else "starts"} ({t[:90]!r})')
        shot(pg, 'f11-clock-' + ('after' if on else 'before'))
        ok(pg.ev("frpJobDone()") is False, tag + 'no finished job waiting: the board\'s heading is the usual one')
        ok(not pg.errors, tag + f'no page errors {pg.errors[:2]}')

def part_panels(ctx, src):                              # F6: solid panels, and a tip waits for a card or panel to close
    for on in (False, True):
        pg = page(ctx, switched(src, 'FRP_PANELS_ON', on=on), 'panels' + str(int(on))); tag = 'on: ' if on else 'off: '
        jump(pg, 2, 9 * 60 + 10); pg.ev("goToDeck(5); SHIP.device.settings.tips = true"); pg.step(20)
        pg.ev("(() => { const it = ITEMS.find(i => /^job board$/i.test(i.t)); it.hit.getWorldPosition(_wp); const gl = nearestOpen(_wp.x, _wp.z, player); player.obj.position.copy(cellPos(...gl)); player.stop(); playerTap(it, _wp.clone(), _wp.clone()); })()")
        for k in range(20):
            pg.step(10, 40)
            if pg.ev("!document.getElementById('ixBoard').hidden"): break
        bg = pg.ev("getComputedStyle(document.getElementById('ixBoard')).backgroundColor")
        ok((bg == 'rgb(13, 21, 33)') == on, tag + f'the job board\'s background is {"solid" if on else "see-through, as before"} ({bg})')
        shot(pg, 'f6-board-' + ('after' if on else 'before'))
        if TIPQ := pg.ev("TIP_Q.length"): pg.ev("while (TIP_Q.length) tipDone()")
        pg.ev("tipShow('frp:test', 'A test tip, long enough to cover a line or two of whatever is under it.')"); pg.step(3)
        vis = pg.ev("(() => { const c = document.getElementById('devTip'); return !!c && !c.hidden; })()")
        ok(vis == (not on), tag + f'a tip asked for with the board open {"waits" if on else "shows over it, as before"}')
        if on:
            pg.page.click('#ixBoardC'); pg.page.wait_for_timeout(700); pg.step(3)
            ok(pg.ev("(() => { const c = document.getElementById('devTip'); return !!c && !c.hidden && /A test tip/.test(c.textContent); })()"), 'on: it shows once the board is closed')
            pg.ev("while (TIP_Q.length) tipDone()"); pg.ev("deviceShow('mail')"); pg.step(5)
            pg.ev("while (TIP_Q.length) tipDone()"); pg.ev("tipShow('t:a-frptest', 'An app tip.')"); pg.step(3)
            d = pg.ev("(() => { const c = document.getElementById('devTip'); return [!!c && !c.hidden, DEV.open, DEV.app, TIP_Q.map(x => x.id).join(), frpTipBusy({ id: 't:a-frptest' }), ['chat', 'ixBoard', 'sleepAsk', 'clockScreen', 'ixHealth'].filter(i => { const e = document.getElementById(i); return e && !e.hidden; }).join()]; })()")
            ok(d[0], f'on: an app\'s own tip still shows over the open device ({d})')
            pg.ev("while (TIP_Q.length) tipDone(); deviceClose()")
        pg2 = page(ctx, switched(src, 'FRP_PANELS_ON', on=on), 'alarm' + str(int(on))); jump(pg2, 2, 20 * 60 + 30)
        bg = pg2.ev("getComputedStyle(document.getElementById('sleepAsk')).backgroundColor")
        ok((bg == 'rgb(13, 21, 33)') == on, tag + f'the alarm card\'s background is {"solid" if on else "as before"} ({bg})')
        ok(not pg.errors and not pg2.errors, tag + f'no page errors {(pg.errors + pg2.errors)[:2]}')

def part_label(ctx, src):                               # F7: the arrow's label wraps instead of being cut
    for on in (False, True):
        pg = page(ctx, switched(src, 'FRP_LABEL_ON', on=on), 'label' + str(int(on))); tag = 'on: ' if on else 'off: '
        jump(pg, 2, 9 * 60 + 10); pg.ev("goToDeck(5); needGoalClear(); SHIP.player.track = null"); pg.step(20)
        L = "(() => { const e = document.querySelector('#ixGoal .ixlab'), r = e.getBoundingClientRect(); return [Math.round(r.height), e.scrollWidth > e.clientWidth + 1, Math.round(r.width), e.textContent]; })()"
        pg.ev("setGoal({ deck: 5, room: 'w', label: 'Fire drill, 15:00: Chief Calder at the Works bay' })"); pg.ev('window.__draw = true'); pg.step(8, 30); pg.ev('window.__draw = false')
        a = pg.ev(L); shot(pg, 'f7-label-' + ('after' if on else 'before'))
        ok(a[1] == (not on), tag + f'a long label is {"shown whole" if on else "cut off, as before"} ({a})')
        ok((a[0] >= 34) == on and a[2] <= 262, tag + f'{"two lines" if on else "one line"}, no wider than before ({a[0]} px high, {a[2]} wide)')
        pg.ev("setGoal({ deck: 5, room: 'w', label: 'The job board' })"); pg.step(8, 30); b = pg.ev(L)
        ok(b[0] == 23 and not b[1], tag + f'a short label is one line, the height it always was ({b})')
        ok(not pg.errors, tag + f'no page errors {pg.errors[:2]}')

def part_blink(ctx, src):                               # F8: the Last Light blinks again while it passes, softly
    for on in (False, True):
        pg = page(ctx, switched(src, 'FRP_BLINK_ON', on=on), 'blink' + str(int(on))); tag = 'on: ' if on else 'off: '
        jump(pg, 4, 14 * 60 + 12); pg.ev("goToDeck(3)"); pg.step(10)
        pg.ev("window.__b = []; const sf = shipFeel; shipFeel = function (k) { if (k.includes('beacon')) window.__b.push(Math.floor(shipNow()) % 1440); return sf.apply(this, arguments); }")
        got = False
        while pg.ev('shipNow()') < 3 * 1440 + 14 * 60 + 29:
            pg.step(20, 50)
            if on and not got and pg.ev("FEEL_S.kinds.includes('beacon') && simNow() / 1000 - FEEL_S.t0 > .3 && simNow() / 1000 - FEEL_S.t0 < .6"):
                got = True; ok(pg.ev("FRP_BLINK.t0 === FEEL_S.t0 && FRP_BLINK.soft === .5"), 'on: a repeat is at half strength'); shot(pg, 'f8-blink-after')
        n = pg.ev('window.__b')
        ok((len(n) >= 2) == on and (on or not n), tag + f'blinks between 14:12 and 14:29: {n}')
        if on: ok(all(b - a >= 5 for a, b in zip(n, n[1:])), f'on: at least eleven seconds of play apart ({n})')
        else: shot(pg, 'f8-blink-before')
        while pg.ev('shipNow()') < 3 * 1440 + 14 * 60 + 45: pg.step(40, 50)
        n2 = pg.ev('window.__b'); ok(all(x < 14 * 60 + 31 for x in n2), tag + f'none after the gathering ends ({n2})')
        ok(not pg.errors, tag + f'no page errors {pg.errors[:2]}')

def part_tips(ctx, src):                                # F10: the view, needs and pause tips on the arrival evening
    for on in (False, True):
        pg = page(ctx, switched(src, 'FRP_TIPS_ON', on=on), 'tips' + str(int(on))); tag = 'on: ' if on else 'off: '
        pg.ev('localStorage.clear()'); pg.ev('newGameStart(true)'); pg.step(5)
        pg.page.fill('form input[maxlength="24"]', 'Sam'); pg.page.click('form button'); pg.step(5)
        pg.ev("window.__tips = []; const o = tipShow; tipShow = function (id) { const r = o.apply(this, arguments); if (r) window.__tips.push([clockText().slice(-5), id]); return r; }")
        f = Follower(pg)
        f.pre = """(() => { window.__rvDev = DEV.open && !DEV.choose && !DIALOGUE ? (window.__rvDev || 0) + 1 : 0;
          if (window.__rvDev >= 4) { window.__rvDev = 0; deviceClose(); return 'close the device'; }
          if (ACT && ACT.kind === 'sit' && ACT.phase !== 'walk' && goalNow() && !DIALOGUE) { actEnd(); return 'get up'; } return null; })()"""
        end = -1440 + 21 * 60 + 30
        while pg.ev('shipNow()') < end:
            f.run(min(end, pg.ev('shipNow()') + 10)); pg.page.wait_for_timeout(1200)   # tips close on a real-time timer: give it some
        t = pg.ev('window.__tips'); ids = [x[1] for x in t]
        print('   tips shown on the arrival evening:', t)
        ok(('t:view' in ids) == on and ('t:needs' in ids) == on, tag + f'Rotate/Walls/zoom and the needs strip {"are" if on else "are not"} taught on the arrival evening')
        if on: ok(all(x[0] >= '18:00' for x in t if x[1] in ('t:view', 't:needs', 't:pause')), 'on: only once the walk and dinner are over')
        r = pg.ev("(() => { const row = TEACH.find(r => r[0] === 't:sleep'); return [row[1]({ S: { woke: true }, min: 400 }), row[1]({ S: { woke: true }, min: 902 })]; })()")
        ok(r == [True, not on], tag + f'"Slept well?" {"only before 09:00" if on else "at any hour, as before"} ({r})')
        ok(not pg.errors, tag + f'no page errors {pg.errors[:2]}')

FRP_ALL = {'line': part_line, 'food': part_food, 'tray': part_tray, 'pin': part_pin, 'lead': part_lead, 'thanks': part_thanks, 'words': part_words, 'say': part_say, 'panels': part_panels, 'label': part_label, 'blink': part_blink, 'tips': part_tips}
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1, has_touch=True)
    src = pathlib.Path(BUILD).read_text()
    for name in (FRP_PARTS or list(FRP_ALL)):
        print('part', name, flush=True); FRP_ALL[name](ctx, src)
    b.close()
print('frp_check:', 'FAILED ' + str(len(FAILS)) if FAILS else 'OK')
sys.exit(1 if FAILS else 0)
