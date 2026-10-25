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
    elif x['seg']: check(x['seg'][0][0] <= b['from'] + 5, f'{label}: the host planned there from {x["seg"][0][0]} ({x["seg"][0][2]})')
    else: check(all(a == 'work' for a in x['work']), f'{label}: the host at work for it ({x["work"]})')
    g.ev(f"skipTo(({b['day']} - 1) * 1440 + {b['from']} - 20)"); g.step(5)
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
        scene(g, label)
    g.step(20)
    r = json.loads(g.ev(f"JSON.stringify({{ b: SHIP.apptx.book.find(x => x.id === {b['id']}), rec: JSON.stringify(apptRecord()) }})"))
    check(bool(r['b']['done']), f'{label}: kept')
    check(APPT_TITLE[kind] in r['rec'] or 'Appointments kept' in r['rec'], f'{label}: in the Record')
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
    print('APPT CHECK ' + ('OK' if ok else 'FAILED'))
sys.exit(0 if ok else 1)
