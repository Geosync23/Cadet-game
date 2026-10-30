# Starship Cadet: the appointments check (FX22; plans/patch-0.92.6.md item 9; keep in the repo)
# Runs on a copy of the build with P926_APPT on (a URL flag in the game until it's switched on; then `true`), and a copy with it
# off. Parts (each in its own page; a part name on the command line runs only those):
#   talk     the cheap fix: a kept appointment with someone (Day 3, 20:00, the bow lounge) opens their chat with an appt.*
#            greeting, then their Talk a while talk
#   ask      asked for in the Appointments app ("What for?"): the big scope (Sato), teach me (Zeke), an hour in another
#            department (Holt; Lukas at breakfast), the midnight feast (your bunkmates): each booked for a later day, its
#            host planned there (or at work there for it), the one-off on the calendar, the join offered with the host
#            leading it, a tap joins, the scene's lines in order and filled, a choice, kept, the Record line, the Mail
#   invite   offered by the host and accepted: Brennan's book (her galley shift), a bed of your own (Cruz, a Saturday,
#            then the first visit booked a week on, and the bed's sign up), as above
#   overlay  show and tell (Raman's cabin, tomorrow evening) and help me rehearse (Tomas, tonight, the evening before quiz
#            night): kept as appointments, then the scene with the host there
#   round    the night round: Mensah at the Deck 3 lift plaza by 22:30, a tap joins, he follows you deck by deck and says
#            each stop line once, on its deck, in order; then the scene; kept, the flag set
#   rules    on paper: the scope is once a week (not again that week, again the next), a stranger can't ask Sato, Brennan's
#            book once a game, the after line said once on a later day by the host near you
#   off      the switch off: no appointment one-offs on Days 1-21, no SHIP.apptx, no "What for?" in the app, no appt joins
#   planted  faults planted in copies must fail their part: the scope's scene removed (ask), teach me's room gone (ask)
#   fixes    RV17's findings (FX22b): a reload mid-scene, then a tap on the host opens it again and it's kept, not missed;
#            a booked appointment's heads-up with heads-ups off and on your shift; the host planned there all the slot;
#            the Record one row each, the garden's at the harvest; Mensah's chatter hushed on the round; a reload keeps
#            the round's stops (four walked: kept), lets Mensah wait again, and an invitation answered by its key
#   no page errors
# Setup and environment as for cadet_test.py.  Run:  python3 appt_check.py BUILD.html [part ...]   (about 15 minutes)
import sys, json, re
exec(open(__file__.replace('appt_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

ok = True
def check(cond, msg, quiet=False):
    global ok
    if not quiet: print(('ok   ' if cond else 'FAIL ') + msg)
    if not cond: ok = False
    return cond

GAME_PATH = sys.argv[1]; GAME_SRC = pathlib.Path(GAME_PATH).read_text(); PARTS = set(sys.argv[2:])
want = lambda p: not PARTS or p in PARTS
SW = r"^const P926_APPT = (?:URL_FLAGS\.has\('appt'\)|true)"
check(bool(re.search(SW, GAME_SRC, flags=re.M)), 'the build has the P926_APPT switch')
def copy(text, tag):
    w = str(WORK / 'test' / ('_appt_' + tag + '_' + pathlib.Path(GAME_PATH).name)); pathlib.Path(w).write_text(text); return w
ON = re.sub(SW, "const P926_APPT = true", GAME_SRC, count=1, flags=re.M)
won, woff = copy(ON, 'on'), copy(re.sub(SW, "const P926_APPT = false", GAME_SRC, count=1, flags=re.M), 'off')

SAYHOOK = """(() => { window.__said = []; window.__mail = []; if (window.__hook) return; window.__hook = 1;
  const bs = bubbleSay; bubbleSay = function (who, text) { if (who && who.p) window.__said.push([who.p.id, text, deckDef.num, Math.round(SHIP.time.min)]); return bs.apply(this, arguments); };
  const ms = mailSend; mailSend = function (m) { window.__mail.push(m && m.subject); return ms.apply(this, arguments); }; })()"""
# a tier with someone (and the tips off), at a minute
SETUP = """(() => { skipTo(%d); SHIP.device.settings.tips = false; socInit(); for (const id of %s) { const r = relGet(id); r.pts = 65; r.tier = 3; } return 1; })()"""
# accept an invitation of this kind (the hourly offers, stepped through the day's hours until one comes)
INVITE = """(() => { const d = SHIP.time.day; for (let k = 0; k < 600 && !SHIP.apptx.offers.some(o => o.kind === '%s' && o.status === 'asked'); k++) { SHIP.apptx.offerDay = 0; apptHour((d - 1) * 1440 + 480 + (k %% 12) * 60 + Math.floor(k / 12)); }
  const i = SHIP.apptx.offers.findIndex(o => o.kind === '%s' && o.status === 'asked'); if (i < 0) return null; apptAnswer(i, true); return SHIP.apptx.book.slice(-1)[0] || null; })()"""
# the booking's day as planned: the host's segment, the one-off, its rooms
BOOKED = """(b => { const p = evPerson(b.host), id = 'appt-' + b.kind, e = eventsOn(b.day).find(x => x.id === id);
  return JSON.stringify({ seg: planDay(p, b.day).filter(s => evTagId(s.tag) === id).map(s => [s.from %% 1440, s.to %% 1440, s.placeId]), on: !!e, rooms: e ? [...eventRooms(e.ev)] : [],
    guests: (b.guests || []).map(g => planDay(evPerson(g), b.day).some(s => evTagId(s.tag) === id)), work: [b.from, b.to - 5].map(t => (planWhere(p, (b.day - 1) * 1440 + t) || {}).act),
    cal: devDay(b.day).some(x => x.kind === 'tradition' && x.title === APPT_WORDS[b.kind].title) }); })(%s)"""
def scene(g, label, want_choice=True):
    """reads the open scene card to its end (the first reply each time); checks every line filled and the script's lines all shown"""
    exp = json.loads(g.ev("JSON.stringify(DIALOGUE ? MEETING_SCRIPTS[DIALOGUE.id].lines.filter(l => l.text).map(l => l.text) : null)") or 'null')
    shown, choice = [], False
    for _ in range(30):
        v = json.loads(g.ev("JSON.stringify(DIALOGUE ? dialogueView() : null)"))
        if not v: break
        if v.get('choices'): choice = True
        else: shown.append(v.get('text') or '')
        g.ev("dialogueStep(0)"); g.step(2)
    check(bool(exp) and all(t in shown for t in exp), f'{label}: the scene\'s {len(exp or [])} lines all said, in a card ({len(shown)} shown)')
    check(not any(re.search(r'[{}]', t) for t in shown), f'{label}: every line filled')
    if want_choice: check(choice, f'{label}: a choice for you')
    return shown

def to_room(g, b):
    """onto the one-off's deck, in the middle of its room"""
    r = g.ev(f"[...eventRooms(eventsOn({b['day']}).find(x => x.id === 'appt-{b['kind']}').ev)][0]")
    n = int(r.split('|')[0]); g.ev(f"goToDeck({n}, null)"); g.step(10)
    g.ev(f"""(() => {{ const tl = ROOM_TILES['{r.split('|')[1]}'], c = cellPos(...tl[Math.floor(tl.length / 2)]); player.obj.position.set(c.x, 0, c.z); player.stop(); }})()""")

def one_off(path, kind, host, day0, how='ask', min0=600, label=None, quiet=False):
    """book (asked, or an invitation accepted), then the day: the host there, a tap joins, the scene, kept. -> list of what failed"""
    global ok
    saved, ok = ok, True
    label = label or kind + ' (' + host + ')'
    g = Game(pw, path, 900, 760); g.ev(SAYHOOK)
    tiers = "['" + (host if host != 'bunk' else 'tomas') + "']"
    g.ev(SETUP % ((day0 - 1) * 1440 + min0, tiers))
    if how == 'ask':
        askable = json.loads(g.ev("JSON.stringify(apptAskable().map(x => x.kind + '|' + x.host))"))
        check(f'{kind}|{host}' in askable, f'{label}: in "What for?"')
        g.ev(f"DEVICE_APPS.get('appointments').act('x:ask', '{kind}|{host}')")
        b = json.loads(g.ev("JSON.stringify(SHIP.apptx.book.slice(-1)[0] || null)"))
    else:
        b = json.loads(g.ev("JSON.stringify(" + (INVITE % (kind, kind)) + ")"))
    if not check(bool(b) and b['kind'] == kind, f'{label}: booked ({g.ev("APPT_SAY")})'):
        g.close(); res, ok = ok, saved and ok; return False
    check(b['day'] > day0, f'{label}: on a later day (Day {b["day"]} {b["from"] // 60:02d}:{b["from"] % 60:02d})')
    x = json.loads(g.ev(BOOKED % json.dumps(b)))
    check(x['on'] and x['cal'], f'{label}: the one-off on Day {b["day"]} and in the Schedule')
    if kind == 'midnight-feast': check(len(x['guests']) + 1 >= 2 and all(x['guests']), f'{label}: {len(x["guests"]) + 1} bunkmates planned there')
    elif x['seg']: check(x['seg'][0][0] <= b['from'] + 5 and x['seg'][-1][1] >= b['to'] - 10, f'{label}: the host planned there {x["seg"][0][0]}-{x["seg"][-1][1]} for {b["from"]}-{b["to"]} ({x["seg"][0][2]})')
    else: check(all(a == 'work' for a in x['work']), f'{label}: the host at work for it ({x["work"]})')
    g.ev(f"skipTo(({b['day']} - 1) * 1440 + {b['from']} - 20)"); g.step(5)
    hu = g.ev(f"""(() => {{ SHIP.device.calendarRemind.on = false; HU_Q.length = 0; devHeadsTick(({b['day']} - 1) * 1440 + {b['from']} - 4); const q = HU_Q.slice(); SHIP.device.calendarRemind.on = true;
      return q.some(x => /{APPT_TITLE[kind]}/.test(x.title || '')) || !!(DEV.hu && /{APPT_TITLE[kind]}/.test(DEV.hu.title || '')); }})()""")
    check(hu, f'{label}: a heads-up before it, even with heads-ups off (RV17 3)')
    mail = json.loads(g.ev("JSON.stringify(window.__mail)"))
    check(any(m and APPT_TITLE[kind] in m for m in mail), f'{label}: its Mail the evening before (or that day)')
    to_room(g, b)
    lead = None
    for _ in range(40):
        g.step(45)
        lead = g.ev(f"TJ_NOW && TJ_NOW.e.id === 'appt-{kind}' ? TJ_NOW.lead : null")
        if lead and g.ev(f"(() => {{ const a = DECK_CREW.find(c => c.p.id === '{lead}'); return !!a && a.settled; }})()"): break
    check(bool(lead) and (lead == b['host'] or kind == 'midnight-feast'), f'{label}: the join offered, {lead} leading it')
    tap = g.ev(f"(() => {{ const a = DECK_CREW.find(c => c.p.id === '{lead}'); return !!a && tradJoinTap(a) && !!DIALOGUE && DIALOGUE.id.startsWith('appt:{kind}'); }})()") if lead else False
    check(tap, f'{label}: a tap on {lead} joins you and opens the scene')
    if tap:
        g.step(60)                                        # a ship minute or more with the card open: it stays (meetingsTick)
        check(g.ev("!!DIALOGUE"), f'{label}: the card stays open across a ship minute')
        if kind == 'scope':                               # RV17 2: a reload mid-scene (the card gone, joined, not kept): a tap opens it again
            g.ev("DIALOGUE = null; if (typeof deviceDialogue === 'function') deviceDialogue(null)"); g.step(5)
            check(g.ev(f"(() => {{ const a = DECK_CREW.find(c => c.p.id === '{lead}'); return !!a && tradJoinTap(a) && !!DIALOGUE && DIALOGUE.id.startsWith('appt:scope'); }})()"), f'{label}: after a reload mid-scene, a tap opens it again')
        scene(g, label)
    g.step(20)
    r = json.loads(g.ev(f"JSON.stringify({{ b: SHIP.apptx.book.find(x => x.id === {b['id']}), rec: JSON.stringify(apptRecord()) }})"))
    check(bool(r['b']['done']), f'{label}: kept')
    if kind == 'garden-bed': check('lettuce' not in r['rec'], f'{label}: not in the Record till the harvest (RV17 #5)')
    else: check(APPT_TITLE[kind] in r['rec'] or 'Appointments kept' in r['rec'], f'{label}: in the Record')
    errs = [e for e in g.errors if 'pageerror' in e]
    check(not errs, f'{label}: no page errors {errs[:2]}')
    res = ok; ok = saved and res
    if quiet == 'keep': return (g, b)
    g.close(); return res

APPT_TITLE = {'scope': 'big scope', 'teach-me': 'Teach me', 'shadow': 'another department', 'midnight-feast': 'Midnight feast', 'brennan-book': 'Brennan', 'garden-bed': 'bed of your own',
  'show-tell': 'Show and tell', 'rehearse': 'rehearse', 'night-round': 'night round'}

with sync_playwright() as pw:
    if want('talk'):
        g = Game(pw, won, 900, 760); g.ev(SAYHOOK)
        who = g.ev("""(() => { skipTo(2 * 1440 + 1170); SHIP.device.settings.tips = false; socInit(); const pl = apptPlaces().find(x => x.deck === 3 && /lounge/i.test(x.name));
          for (const p of apptPeople()) { const a = { id: 900, with: [p.id], at: 2 * 1440 + 1200, len: 30, where: apptSpot(pl.id, 2 * 1440 + 1200, 30), kind: 'social', status: 'asked', by: null };
            if (apptReply(p, a).answer === 'yes') { a.status = 'yes'; SHIP.device.appts.push(a); goToDeck(3, null); return p.id; } } return null; })()""")
        g.step(10); g.ev("(() => { const a = SHIP.device.appts.find(x => x.id === 900), c = cellPos(...PLACE_OF.get(a.where).at); player.obj.position.set(c.x + .8, 0, c.z); player.stop(); })()")
        first, talked = None, False
        for _ in range(60):
            g.step(60)
            r = json.loads(g.ev("JSON.stringify((() => { const a = SHIP.device.appts.find(x => x.id === 900); return { st: a.status, talk: a.talk || 0, line: CHAT && CHAT.line ? CHAT.line.text : null, kind: CHAT && CHAT.line ? CHAT.line.kind : null, who: CHAT ? CHAT.p.id : null, talking: !!(CHAT && CHAT.talk) }; })())"))
            if r['talk'] and not first: first = r
            if r['talking']: talked = True; break
        check(bool(first) and first['who'] == who and first['kind'] == 'appt' and bool(first['line']), f'talk: kept with {who}, their chat opens with an appointment greeting ({first and first["line"]})')
        check(talked, f'talk: then their Talk a while talk')
        check(not [e for e in g.errors if 'pageerror' in e], 'talk: no page errors')
        g.close()
    if want('ask'):
        for kind, host, day0 in [('scope', 'sato', 3), ('teach-me', 'torres-zeke', 3), ('shadow', 'holt', 3), ('shadow', 'dlamini-lukas', 3), ('midnight-feast', 'bunk', 4)]:
            one_off(won, kind, host, day0)
    if want('invite'):
        one_off(won, 'brennan-book', 'brennan', 3, how='invite')
        k = one_off(won, 'garden-bed', 'cruz-tove', 17, how='invite', quiet='keep')
        if isinstance(k, tuple):
            g, b = k
            g.step(30)
            x = json.loads(g.ev(f"""(() => {{ skipTo(({b['day']} + 6) * 1440 + 480); apptMinute(shipNow()); const n = SHIP.apptx.book.slice(-1)[0];
              return JSON.stringify({{ traced: traceOn('gardenBedYours'), g: SHIP.apptx.garden, n }}); }})()"""))
            check(x['traced'], 'garden-bed: your bed\'s sign is up (the trace gardenBedYours)')
            check(bool(x['n']) and x['n']['key'] == 'tend:0' and x['n']['day'] >= b['day'] + 7, f'garden-bed: Cruz books the first visit a week on ({x["n"] and (x["n"]["key"], x["n"]["day"])})')
            g.ev("goToDeck(3, null)"); g.step(10)
            check(g.ev("dressingOn().includes('gardenBedYours')"), 'garden-bed: the sign drawn on Deck 3')
            g.close()
    if want('overlay'):
        for kind, host, day0, min0 in [('show-tell', 'raman', 3, 600), ('rehearse', 'tomas', 3, 600)]:
            label = kind + ' (' + host + ')'
            g = Game(pw, won, 900, 760); g.ev(SAYHOOK); g.ev(SETUP % ((day0 - 1) * 1440 + min0, "['" + host + "']"))
            b = json.loads(g.ev("JSON.stringify(" + (INVITE % (kind, kind)) + ")"))
            if not check(bool(b) and b.get('aid'), f'{label}: invited, accepted, booked as an appointment ({g.ev("APPT_SAY")})'): g.close(); continue
            a = json.loads(g.ev(f"JSON.stringify(SHIP.device.appts.find(x => x.id === {b['aid']}))"))
            check(a['status'] == 'yes' and a.get('appt') == kind, f'{label}: in the Appointments app, {a["at"] // 1440 + 1} {a["at"] % 1440}')
            g.ev(f"skipTo({a['at']} - 15)"); g.step(5); g.ev(f"goToDeck(deckOf('{a['where']}'), null)"); g.step(10)
            g.ev(f"(() => {{ const c = cellPos(...PLACE_OF.get('{a['where']}').at); player.obj.position.set(c.x + .3, 0, c.z + .3); player.stop(); }})()")
            for _ in range(50):
                g.step(45)
                if g.ev("!!DIALOGUE"): break
            check(g.ev(f"!!DIALOGUE && DIALOGUE.id === 'appt:{kind}:{host}'"), f'{label}: kept, and the scene once {host} is there')
            if g.ev("!!DIALOGUE"): scene(g, label)
            g.step(20)
            check(bool(json.loads(g.ev(f"JSON.stringify(SHIP.apptx.book.find(x => x.id === {b['id']}).done)"))), f'{label}: kept')
            if kind == 'rehearse':
                g.ev(f"skipTo({b['day']} * 1440 + 1210)"); g.step(5); g.ev("goToDeck(3, null)"); g.step(20)
                tl = g.ev("""(() => { const e = eventsOn(SHIP.time.day).find(x => x.id === 'quiz'); if (!e) return 'no quiz'; const a = DECK_CREW.find(c => c.p.id === 'tomas'); if (!a) return 'no tomas'; player.obj.position.set(a.x + .9, 0, a.z); player.stop(); return 'ok'; })()""")
                for _ in range(20):
                    g.step(45)
                    if g.ev("window.__said.some(x => x[0] === 'tomas' && /heard them first/.test(x[1]))"): break
                check(g.ev("window.__said.some(x => x[0] === 'tomas' && /heard them first/.test(x[1]))"), f'rehearse: at quiz night Tomas says "You heard them first" ({tl})')
            check(not [e for e in g.errors if 'pageerror' in e], f'{label}: no page errors')
            g.close()
    if want('round'):
        g = Game(pw, won, 900, 760); g.ev(SAYHOOK); g.ev(SETUP % (3 * 1440 + 600, "['mensah']"))
        b = json.loads(g.ev("JSON.stringify(" + (INVITE % ('night-round', 'night-round')) + ")"))
        if check(bool(b), f'round: invited, accepted (Day {b and b["day"]}, the night before your day off: {b and g.ev("!devShiftOn(" + str(b["day"] + 1) + ")")})'):
            g.ev(f"skipTo(({b['day']} - 1) * 1440 + {b['from']} - 12)"); g.step(5); g.ev("goToDeck(3, null)"); g.step(10)
            g.ev("(() => { const pl = DECKS[3].places.find(q => q.room === '+' && q.type === 'bench'), c = cellPos(...pl.at); player.obj.position.set(c.x + .8, 0, c.z + .8); player.stop(); })()")
            for _ in range(30):
                g.step(45)
                if g.ev("(() => { const a = DECK_CREW.find(c => c.p.id === 'mensah'); return !!a && a.settled && SHIP.time.min >= 1350; })()"): break
            check(g.ev("(() => { const a = DECK_CREW.find(c => c.p.id === 'mensah'); return !!a && roomAt(...cellAt(a.x, a.z)) === '+'; })()"), 'round: Mensah at the Deck 3 lift plaza at 22:30')
            check(g.ev("(() => { const a = DECK_CREW.find(c => c.p.id === 'mensah'); return !!a && tradJoinTap(a) && !!APPT_ROUND_NOW; })()"), 'round: a tap joins, the round begins')
            OUT = """(() => { const [c0, r0] = DECKS[deckDef.num].lift; let best = null; for (let dc = -3; dc <= 3; dc++) for (let dr = -3; dr <= 3; dr++) { const c = c0 + dc, r = r0 + dr, k = roomAt(c, r); if (!k || k === '@' || BLOCKED.has(c + ',' + r)) continue; const d = Math.abs(dc) + Math.abs(dr); if (!best || d < best[0]) best = [d, c, r]; }
              const p = cellPos(best[1], best[2]); player.obj.position.set(p.x, 0, p.z); player.stop(); return 1; })()"""
            for n, upto in [(6, 1), (5, 2), (4, 4), (3, 5), (2, 6), (1, 7)]:
                g.ev(f"goToDeck({n}, null)"); g.step(20); g.ev(OUT)
                for _ in range(40):
                    g.step(30)
                    if (g.ev("APPT_ROUND_NOW ? APPT_ROUND_NOW.i : 99") or 0) >= upto: break
            for _ in range(20):
                g.step(30)
                if g.ev("!!DIALOGUE"): break
            said = json.loads(g.ev("JSON.stringify(window.__said.filter(x => x[0] === 'mensah').map(x => [x[1], x[2]]))"))
            stops = json.loads(g.ev("JSON.stringify(APPT_WORDS['night-round'].stops.map(l => l.text))"))
            check([t for t, _ in said if t in stops] == stops, f'round: all {len(stops)} stop lines, once each, in order ({len(said)} said)')
            check([d for t, d in said if t in stops] == [6, 5, 4, 4, 3, 2, 1], f'round: each on its deck (the rec deck\'s from Deck 4) ({[d for t, d in said if t in stops]})')
            check(g.ev("!!DIALOGUE && DIALOGUE.id.startsWith('appt:night-round')"), 'round: then the scene')
            if g.ev("!!DIALOGUE"): scene(g, 'round')
            g.step(20)
            check(g.ev(f"!!SHIP.apptx.book.find(x => x.id === {b['id']}).done && flag('night.round.walked') === true"), 'round: kept, night.round.walked set')
        check(not [e for e in g.errors if 'pageerror' in e], 'round: no page errors')
        g.close()
    if want('rules'):
        k = one_off(won, 'scope', 'sato', 3, quiet='keep')
        if isinstance(k, tuple):
            g, b = k
            check(not g.ev(f"apptCan('scope', 'sato', {b['day']})"), 'rules: the scope not again that week')
            check(g.ev(f"apptCan('scope', 'sato', {b['day']} + 7)"), 'rules: the scope again the next week')
            check(not g.ev("(() => { const r = relGet('sato'); const t = r.tier; r.tier = 0; const c = apptCan('scope', 'sato', 30); r.tier = t; return c; })()"), 'rules: a stranger can\'t ask Sato')
            g.ev(f"skipTo({b['day']} * 1440 + 1170)"); g.step(5); g.ev("goToDeck(2, null)"); g.step(20)
            for _ in range(30):
                where = g.ev("(() => { const a = DECK_CREW.find(c => c.p.id === 'sato'); if (!a || !a.settled) return null; player.obj.position.set(a.x + .9, 0, a.z); player.stop(); return 1; })()")
                g.step(45)
                if g.ev("window.__said.some(x => x[0] === 'sato' || /Sato/.test(x[1]))"): break
            said = json.loads(g.ev("JSON.stringify(window.__said.map(x => x[1]))"))
            after = json.loads(g.ev("JSON.stringify(APPT_WORDS.scope.after.map(l => l.text))"))
            check(sum(1 for t in said if t in after) == 1, f'rules: the scope\'s after line said once the next day ({[t for t in said if t in after]})')
            g.close()
        g = Game(pw, won, 900, 760); g.ev(SETUP % (2 * 1440 + 600, "['brennan']"))
        b = json.loads(g.ev("JSON.stringify(" + (INVITE % ('brennan-book', 'brennan-book')) + ")"))
        if b:
            g.ev(f"apptKeep(SHIP.apptx.book.find(x => x.id === {b['id']}))")
            check(not g.ev("apptCan('brennan-book', 'brennan', SHIP.time.day + 10)"), 'rules: Brennan\'s book once a game')
            n = g.ev("""(() => { const X = SHIP.apptx; X.book.push({ id: 90, kind: 'scope', key: 'tavessa', host: 'sato', guests: [], day: 3, from: 1170, to: 1200, done: 3 }, { id: 91, kind: 'scope', key: 'shoals', host: 'sato', guests: [], day: 10, from: 1170, to: 1200, done: 10 },
              { id: 92, kind: 'garden-bed', key: '', host: 'cruz-tove', guests: [], day: 6, from: 600, to: 630, done: 6 }, { id: 93, kind: 'garden-bed', key: 'tend:0', host: 'cruz-tove', guests: [], day: 13, from: 600, to: 615, done: 13 });
              const r = apptRecord(); const rows = r.length ? r[1].rows.map(x => x.text) : []; return JSON.stringify(rows); })()""")
            rows = json.loads(n)
            check(sum('scope' in t for t in rows) == 1 and not any('lettuce' in t for t in rows), f'rules: the Record has one row for the scope and no garden line before the harvest (RV17 5) {rows}')
        else: check(False, 'rules: Brennan\'s book offered')
        g.close()
    if want('off'):
        g = Game(pw, woff, 900, 760)
        r = json.loads(g.ev("""(() => { skipTo(2 * 1440 + 600); socInit(); for (const id of ['sato', 'brennan', 'mensah']) { const r = relGet(id); r.tier = 3; r.pts = 65; }
          const ids = []; for (let d = 1; d <= 21; d++) for (const e of eventsOn(d)) if (/^appt-/.test(e.id)) ids.push(e.id + '@' + d);
          const v = DEVICE_APPS.get('appointments').view(); return JSON.stringify({ ids, x: typeof SHIP.apptx, what: JSON.stringify(v).includes('What for?'), joins: Object.keys(TRAD_JOIN).filter(k => /^appt-/.test(k)), places: DECKS[4].places.filter(q => /^4-feast-/.test(q.id)).length }); })()"""))
        g.step(600)
        check(not r['ids'] and r['x'] == 'undefined' and not r['what'] and not r['joins'] and not r['places'], f'off: nothing ({r})')
        check(not [e for e in g.errors if 'pageerror' in e], 'off: no page errors')
        g.close()
    if want('planted'):
        for name, a, b2 in [("the scope's scene removed", None, None),
                            ("teach me's room gone", "where: h => [{ deck: APPT_TEACH[h][0], pool: APPT_TEACH[h][1] }]", "where: h => [{ deck: APPT_TEACH[h][0], pool: 'nowhere' }]")]:
            t = ON
            if name.startswith('the scope'):
                check("const apptWord = (kind," in t, 'planted: the line to change is there', quiet=True)
                t = t.replace("const apptWord = (kind,", "APPT_WORDS.scope = { ...APPT_WORDS.scope, scene: {} };\nconst apptWord = (kind,", 1)
            else:
                check(a in t, 'planted: the line to change is there', quiet=True); t = t.replace(a, b2, 1)
            p = copy(t, 'planted')
            print('  planted:', name)
            kind, host = ('scope', 'sato') if name.startswith('the scope') else ('teach-me', 'torres-zeke')
            ok_before = ok
            res = one_off(p, kind, host, 3, label='planted ' + kind)
            ok = ok_before
            check(res is False, f'planted: {name}: its part fails')
    if want('fixes'):
        # RV17 #2: save and reload in the middle of the scope's scene
        k = None
        g = Game(pw, won, 900, 760); g.ev(SAYHOOK); g.ev(SETUP % (2 * 1440 + 600, "['sato']"))
        g.ev("DEVICE_APPS.get('appointments').act('x:ask', 'scope|sato')")
        b = json.loads(g.ev("JSON.stringify(SHIP.apptx.book.slice(-1)[0] || null)"))
        if check(bool(b), 'fixes: the scope booked for the reload'):
            g.ev(f"skipTo(({b['day']} - 1) * 1440 + {b['from']} - 20)"); g.step(5); to_room(g, b)
            for _ in range(40):
                g.step(45)
                if g.ev("TJ_NOW && TJ_NOW.e.id === 'appt-scope' && (() => { const a = DECK_CREW.find(c => c.p.id === 'sato'); return !!a && a.settled; })()"): break
            tap = "(() => { const a = DECK_CREW.find(c => c.p.id === 'sato'); return !!a && tradJoinTap(a) && !!DIALOGUE && DIALOGUE.id.startsWith('appt:scope'); })()"
            check(g.ev(tap), 'fixes: a tap on Sato opens the scene')
            g.ev("dialogueStep(0)"); g.step(2)
            g.ev("eval('(' + saveGame.toString().replace('if (NOSAVE ||', 'if (false &&') + ')')()")   # the save as the game writes it (the page is ?nosave)
            g.page.goto(g.page.url.replace('?nosave&debug', '?debug'), wait_until='commit', timeout=180000); g.page.wait_for_function('window.__sc !== undefined || window.__err', timeout=180000, polling=500); g.step(5)
            r = json.loads(g.ev(f"JSON.stringify({{ open: !!DIALOGUE, joined: SHIP.events.joined.includes('appt-scope@{b['day']}'), deck: deckDef.num, b: SHIP.apptx.book.find(x => x.id === {b['id']}) }})"))
            check(r['joined'] and not r['open'] and r['deck'] == 2, f'fixes: reloaded mid-scene, the card closed, still joined ({r["deck"]}, {r["open"]}, {r["joined"]})')
            for _ in range(20):
                if g.ev("(() => { const a = DECK_CREW.find(c => c.p.id === 'sato'); if (!a || !a.settled) return false; player.obj.position.set(a.x + .9, 0, a.z); player.stop(); return true; })()"): break
                g.step(45)
            if check(g.ev(tap), 'fixes: after the reload a tap on Sato opens the scene again (RV17 #2)'): scene(g, 'fixes: the scope again')
            g.step(20)
            r = json.loads(g.ev(f"JSON.stringify(SHIP.apptx.book.find(x => x.id === {b['id']}))"))
            check(bool(r['done']) and not r.get('gone'), f'fixes: kept after the reload, not missed ({r.get("done")}, {r.get("gone")})')
            # a reload with the card closed and no tap: at its end still kept (you were there)
            g.ev(f"(() => {{ const b = SHIP.apptx.book.find(x => x.id === {b['id']}); b.done = 0; b.gone = 0; apptMinute(({b['day']} - 1) * 1440 + {b['to']} + 31); }})()")
            r = json.loads(g.ev(f"JSON.stringify(SHIP.apptx.book.find(x => x.id === {b['id']}))"))
            check(bool(r['done']) and not r.get('gone'), f'fixes: joined, the card closed by a reload: kept at its end ({r.get("done")}, {r.get("gone")})')
        g.ev("localStorage.clear()")
        check(not [e for e in g.errors if 'pageerror' in e], 'fixes: reload: no page errors')
        g.close()
        # RV17 R1: the rejoin after a reload when the host is at work for it (not planned there): Brennan, and Mensah's round
        def reload(g):
            g.ev("eval('(' + saveGame.toString().replace('if (NOSAVE ||', 'if (false &&') + ')')()")
            g.page.goto(g.page.url.replace('?nosave&debug', '?debug'), wait_until='commit', timeout=180000); g.page.wait_for_function('window.__sc !== undefined || window.__err', timeout=180000, polling=500); g.step(5)
        g = Game(pw, won, 900, 760); g.ev(SETUP % (2 * 1440 + 600, "['brennan']"))
        b = json.loads(g.ev("JSON.stringify(" + (INVITE % ('brennan-book', 'brennan-book')) + ")"))
        if check(bool(b), 'fixes: Brennan\'s book booked for the reload'):
            g.ev(f"skipTo(({b['day']} - 1) * 1440 + {b['from']} - 20)"); g.step(5); to_room(g, b)
            for _ in range(40):
                g.step(45)
                if g.ev("TJ_NOW && TJ_NOW.e.id === 'appt-brennan-book' && (() => { const a = DECK_CREW.find(c => c.p.id === TJ_NOW.lead); return !!a && a.settled; })()"): break
            tapB = "(() => { const a = DECK_CREW.find(c => c.p.id === 'brennan'); if (!a) return false; player.obj.position.set(a.x + .9, 0, a.z); player.stop(); return tradJoinTap(a) && !!DIALOGUE && DIALOGUE.id.startsWith('appt:brennan-book'); })()"
            check(g.ev(tapB), 'fixes: a tap on Brennan opens her scene')
            g.ev("dialogueStep(0)"); g.step(2); reload(g)
            if check(g.ev(tapB), 'fixes: after a reload a tap on Brennan (at work for it) opens the scene again (RV17 R1)'): scene(g, 'fixes: Brennan again')
            g.step(20)
            r = json.loads(g.ev(f"JSON.stringify(SHIP.apptx.book.find(x => x.id === {b['id']}))"))
            check(bool(r['done']) and not r.get('gone'), f'fixes: Brennan\'s book kept after the reload ({r.get("done")}, {r.get("gone")})')
        g.ev("localStorage.clear()"); check(not [e for e in g.errors if 'pageerror' in e], 'fixes: Brennan reload: no page errors'); g.close()
        g = Game(pw, won, 900, 760); g.ev(SAYHOOK); g.ev(SETUP % (3 * 1440 + 600, "['mensah']"))
        b = json.loads(g.ev("JSON.stringify(" + (INVITE % ('night-round', 'night-round')) + ")"))
        if check(bool(b), 'fixes: the night round booked for the reload'):
            BENCH = "(() => { const pl = DECKS[3].places.find(q => q.room === '+' && q.type === 'bench'), c = cellPos(...pl.at); player.obj.position.set(c.x + .8, 0, c.z + .8); player.stop(); })()"
            MENSAH = "(() => { const a = DECK_CREW.find(c => c.p.id === 'mensah'); return !!a && a.settled && SHIP.time.min >= %d; })()"
            tapM = "(() => { const a = DECK_CREW.find(c => c.p.id === 'mensah'); return !!a && tradJoinTap(a) && !!APPT_ROUND_NOW; })()"
            g.ev(f"skipTo(({b['day']} - 1) * 1440 + {b['from']} - 12)"); g.step(5); g.ev("goToDeck(3, null)"); g.step(10); g.ev(BENCH)
            for _ in range(30):
                g.step(45)
                if g.ev(MENSAH % 1350): break
            check(g.ev(tapM), 'fixes: a tap on Mensah starts the round')
            OUT = """(() => { const [c0, r0] = DECKS[deckDef.num].lift; let best = null; for (let dc = -3; dc <= 3; dc++) for (let dr = -3; dr <= 3; dr++) { const c = c0 + dc, r = r0 + dr, k = roomAt(c, r); if (!k || k === '@' || BLOCKED.has(c + ',' + r)) continue; const d = Math.abs(dc) + Math.abs(dr); if (!best || d < best[0]) best = [d, c, r]; }
              const p = cellPos(best[1], best[2]); player.obj.position.set(p.x, 0, p.z); player.stop(); return 1; })()"""
            g.ev("goToDeck(6, null)"); g.step(20); g.ev(OUT)
            for _ in range(40):
                g.step(30)
                if (g.ev("APPT_ROUND_NOW ? APPT_ROUND_NOW.i : 0") or 0) >= 1: break
            ri = g.ev(f"SHIP.apptx.book.find(x => x.id === {b['id']}).ri || 0")
            check(ri == 1, f'fixes: one stop walked, saved on the booking (ri {ri})')
            now = g.ev("Math.round(SHIP.time.min)"); reload(g)
            g.ev("goToDeck(3, null)"); g.step(10); g.ev(BENCH)
            for _ in range(30):
                g.step(45)
                if g.ev(MENSAH % 0): break
            r = g.ev("(() => { const a = DECK_CREW.find(c => c.p.id === 'mensah'); return !!a && tradJoinTap(a) && !!APPT_ROUND_NOW ? APPT_ROUND_NOW.i : -1; })()")
            check(r == 1, f'fixes: after a reload (at {now}) Mensah waits at the bench again, and a tap picks the round up at stop 2 (RV17 R1: {r})')
        g.ev("localStorage.clear()"); check(not [e for e in g.errors if 'pageerror' in e], 'fixes: round reload: no page errors'); g.close()
        # RV17 #3: Brennan's book (14:30, a weekday) on your shift, and with heads-ups off
        g = Game(pw, won, 900, 760); g.ev(SETUP % (2 * 1440 + 600, "['brennan']"))
        b = json.loads(g.ev("JSON.stringify(" + (INVITE % ('brennan-book', 'brennan-book')) + ")"))
        if check(bool(b), 'fixes: Brennan\'s book booked for the heads-ups'):
            at = (b['day'] - 1) * 1440 + b['from']
            HU = "(() => { HU_Q.length = 0; DEV.notes.calendar = 0; SHIP.device.calendarRemind.heard.length = 0; devHeadsTick(shipNow()); return JSON.stringify({ q: HU_Q.map(h => h.title), badge: DEV.notes.calendar || 0, shift: devOnShift() }); })()"
            g.ev(f"skipTo({at} - SHIP.device.calendarRemind.ahead + 1); SHIP.device.calendarRemind.on = true"); r = json.loads(g.ev(HU))
            check(r['shift'] and any('Brennan' in x for x in r['q']), f'fixes: on your shift, a heads-up strip, not just a badge (RV17 #3: {r})')
            g.ev(f"skipTo({at}); SHIP.device.calendarRemind.on = false"); r = json.loads(g.ev(HU))
            check(any('Brennan' in x for x in r['q']), f'fixes: with heads-ups off, the booked appointment still reminds you (RV17 #3: {r})')
        g.close()
        # RV17 #4: the host planned there for all of the slot (RV17's days: Sato Day 48, Cruz Day 41, Zeke Day 34)
        g = Game(pw, won, 900, 760)
        for kind, host, d0 in [('scope', 'sato', 5), ('teach-me', 'rina', 10), ('teach-me', 'torres-zeke', 33), ('garden-bed', 'cruz-tove', 40), ('scope', 'sato', 47)]:
            r = json.loads(g.ev(f"""(() => {{ skipTo(({d0} - 1) * 1440 + 600); const R = APPT_RULES['{kind}'], b = apptTry('{kind}', '{host}', apptSlots('{kind}', '{host}')); if (!b) return 'null';
              const B = (b.day - 1) * 1440, S = planDay(evPerson(b.host), b.day).filter(s => evTagId(s.tag) === 'appt-{kind}').map(s => [s.from - B, s.to - B]), sh = R.onShift('{host}', b.day);
              let all = true; for (let t = b.from + 5; t < b.to - 10; t += 5) if (!S.some(([a, c]) => a <= t && t < c)) all = false;
              const out = {{ day: b.day, from: b.from, to: b.to, S, sh, all: sh || all }}; apptUnbook('appt-{kind}', b.day); SHIP.apptx.book.pop(); return JSON.stringify(out); }})()"""))
            check(r != 'null' and r['all'], f'fixes: {kind} with {host} from Day {d0}: the host there all the slot (RV17 #4: {r})')
        check(not [e for e in g.errors if 'pageerror' in e], 'fixes: slots: no page errors')
        g.close()
        # RV17 #5, #6 and the nits, on paper
        g = Game(pw, won, 900, 760); g.ev(SAYHOOK); g.ev(SETUP % (9 * 1440 + 600, "['sato', 'cruz-tove']"))
        r = json.loads(g.ev("""(() => { const X = SHIP.apptx, mk = (id, kind, host, day, key) => ({ id, kind, key, host, guests: [], day, from: 1140, to: 1170, done: day });
          X.book.push(mk(1, 'garden-bed', 'cruz-tove', 3, ''), mk(2, 'scope', 'sato', 4, 'tavessa'), mk(3, 'garden-bed', 'cruz-tove', 10, 'tend:0'), mk(4, 'scope', 'sato', 11, 'shoals'));
          const before = apptRecord(); X.book.push(mk(5, 'garden-bed', 'cruz-tove', 31, 'harvest')); const after = apptRecord();
          const rows = B => (B[1] || { rows: [] }).rows.map(x => x.text); return JSON.stringify({ before: rows(before), after: rows(after) }); })()"""))
        lettuce = lambda L: sum(1 for x in L if 'lettuce' in x)
        check(lettuce(r['before']) == 0 and sum(1 for x in r['before'] if 'scope' in x) == 1, f'fixes: the Record: one scope row, no lettuce before the harvest (RV17 #5: {r["before"]})')
        check(lettuce(r['after']) == 1, f'fixes: the Record: the lettuce once, at the harvest ({r["after"]})')
        # Mensah's chatter while the round runs (RV17 #6): only him near you, his chatter tried over many ship minutes
        CH = """(() => { const keep = DECK_CREW.slice(), m = keep.find(c => c.p.id === 'mensah'); if (!m) return -1; DECK_CREW.splice(0, DECK_CREW.length, m);
          player.obj.position.set(m.x + 1.2, 0, m.z); let n = 0; const bs = bubbleSay; bubbleSay = function (w) { if (w === m.h || w && w.p && w.p.id === 'mensah') n++; return bs.apply(this, arguments); };
          try { for (let k = 0; k < 400; k++) { CHATTER_AT = -1e9; CHATTER_LAST.length = 0; socialChatter(20000 + k); } } finally { DECK_CREW.splice(0, DECK_CREW.length, ...keep); bubbleSay = bs; }
          return n; })()"""
        d = g.ev("""(() => { for (let d = SHIP.time.day + 1; d < SHIP.time.day + 8; d++) { const w = planWhere(evPerson('mensah'), (d - 1) * 1440 + 1380); if (w && w.act === 'work' && w.deck) return [d, w.deck]; } return null; })()""")
        if check(bool(d), f'fixes: Mensah on watch at 23:00 ({d})'):
            g.ev(f"skipTo(({d[0]} - 1) * 1440 + 1380)"); g.step(5); g.ev(f"goToDeck({d[0] and d[1]}, null)"); g.step(30)
            g.ev("(() => { const m = DECK_CREW.find(c => c.p.id === 'mensah'); if (m) { player.obj.position.set(m.x + 1.2, 0, m.z); player.stop(); } })()"); g.step(10)
            free = g.ev(CH)
            g.ev(f"APPT_ROUND_NOW = {{ b: {{ host: 'mensah', kind: 'night-round', day: {d[0]}, to: 1439, done: 0 }}, i: 0, L: [], decks: [], at: 1e12 }}")
            hushed = g.ev(CH); g.ev("APPT_ROUND_NOW = null")
            check(free > 0 and hushed == 0, f'fixes: Mensah chatters ({free} bubbles), but not while the round runs ({hushed}) (RV17 #6)')
        r = json.loads(g.ev("""(() => { const s = { ship: { apptx: { book: [{ id: 9, kind: 'night-round', key: '', host: 'mensah', guests: [], day: 12, from: 1350, to: 1395, done: 0, waits: 1, ri: 4 }, { id: 10, kind: 'show-tell', key: 'raman', host: 'raman', day: 12, from: 1150, to: 1180, done: 0, aid: 5, shown: 1 }], offers: [] } } };
          const L = apptxLoad(s); return JSON.stringify(L.book); })()"""))
        check(not any('waits' in x or 'shown' in x for x in r) and r[0].get('ri') == 4, f'fixes: a reload: Mensah waits again, an overlay scene can show again, the round\'s stops kept (RV17 7a: {r})')
        r = g.ev("""(() => { const X = SHIP.apptx; X.book.push({ id: 11, kind: 'night-round', key: '', host: 'mensah', guests: [], day: 12, from: 1350, to: 1395, done: 0, ri: 4 }); SHIP.events.joined.push('appt-night-round@12');
          APPT_ROUND_NOW = null; apptMinute(11 * 1440 + 1395 + 31); const b = X.book.find(x => x.id === 11); return JSON.stringify([b.done, b.gone || 0]); })()""")
        check(json.loads(r)[0] and not json.loads(r)[1], f'fixes: a reload mid-round with four stops walked: kept at its end (RV17 7b: {r})')
        r = json.loads(g.ev("""(() => { const X = SHIP.apptx; X.offers = [{ kind: 'scope', host: 'sato', day: 30, from: 1140, to: 1170, made: 10, status: 'asked', said: 0 }, { kind: 'teach-me', host: 'rina', day: 31, from: 1140, to: 1180, made: 10, status: 'asked', said: 0 }];
          const v = apptViewX(), btn = v.filter(x => x.kind === 'buttons')[1].items[1].action; X.offers.shift(); apptActX(btn.do, btn.arg); return JSON.stringify(X.offers.map(o => o.status)); })()"""))
        check(r == ['no'], f'fixes: Decline answers its own invitation after the list moved (RV17 7c: {r})')
        check(not [e for e in g.errors if 'pageerror' in e], 'fixes: on paper: no page errors')
        g.close()
    print('APPT CHECK ' + ('OK' if ok else 'FAILED'))
sys.exit(0 if ok else 1)
