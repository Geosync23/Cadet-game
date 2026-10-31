# Starship Cadet: the 0.92.6 traditions check (FX17; plans/patch-0.92.6.md items 2-5, 7, 8, 13, 15; keep in the repo)
# Runs on a copy of the build with P926_TRADS on (a URL flag in the game until it's switched on; then `true`), and a copy with it
# off as the base. Each part is one of the user's playtest notes; each fails on 0.92.5 and passes with the switch on:
#   13  the Day 8 talk is spoken: Dr. Sato on the stool says talk.sato line by line in her bubble, every line in order once, while
#       you're in the auditorium; joined, the question card (talk.sato.ask) opens after the last line, not before. Off: nothing said
#   8   a tradition can be joined to its end: 5 minutes before the end of Tiles night (Day 2), quiz night (Day 4) and the jam (Day 5),
#       in its room, the join is offered (TJ_NOW, its leader on the deck) and a tap on the leader joins you; the device's Calendar and
#       Home still list it ("on now, until"). Off: at least one of them not offered or not listed
#   5   One week aboard (Day 7): Zeke is in the bow lounge, sitting, by 17:25; the join is his (TJ_NOW leads with him); a tap sits you
#       down and opens his card going over your week (week1.zeke), its lines filled. Off: no card
#   2   the Sunday swap meet (Day 14, 11:00): Orla Ishikawa (the host) and Dara Shah at the stalls' spots, people browsing or on the
#       benches, the join is Orla's, her swap card opens on a tap, and the stalls talk (bubbles). Off: nobody at a stall, no card
#   15  Spice shelf supper (Day 16, a Tuesday): Brennan comes out to the spice shelf (3-spice-host) by 18:40, opens and names three
#       jars, the mess guesses (bubbles), she says whose, and joined you get the guess card. Off: Brennan never at the shelf, no card
#   4   Reading corner (Day 21, 16:30; fortnightly, odd-week Sundays, since 0.93.2's FX24): Esme Walsh there, everyone at it seated
#       within 4.5 m of the bow window's sofa, at least 4 bubbles about books in the room, a tap joins you with a book. Day 14 (an even
#       week): nobody there, no host alone. Off (Day 14, as before): no host
#   3   Winner stays on (Days 14 and 21): planned in the stands at 12:30, 13:30, 14:30 and 15:30: 9 or more, and 12 or more at 13:30 and
#       14:30 (of about 30 crew off duty and aboard on a Sunday afternoon). Off: thinner (3-9) at least once
#   7   the career's weeks: (b) a talk on every Monday from Day 36 to 78 and a chief's on Days 32, 46, 60, 74, each on the calendar;
#       (c) Six weeks aboard on Day 42 and Twelve weeks on Day 84; and (a) from week 5 to 12 each week has a tradition not seen in
#       any earlier week; every new one's host at each showing to Day 112, and none on a day its host is away. Off: no talk after Day 29
#       and no milestones
#   no page errors
# Setup and environment as for cadet_test.py.  Run:  python3 p926_check.py BUILD.html [part ...]   (no parts: all of them)
import sys, json, re
exec(open(__file__.replace('p926_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

ok = True
def check(cond, msg):
    global ok
    print(('ok   ' if cond else 'FAIL ') + msg)
    if not cond: ok = False
    return cond

build = sys.argv[1]; src = pathlib.Path(build).read_text(); PARTS = set(sys.argv[2:])
want = lambda p: not PARTS or p in PARTS
SW = r"^const P926_TRADS = (?:URL_FLAGS\.has\('p926'\)|true)"
has = check(bool(re.search(SW, src, flags=re.M)), 'the build has the P926_TRADS switch')
on = re.sub(SW, "const P926_TRADS = true", src, count=1, flags=re.M); off = re.sub(SW, "const P926_TRADS = false", src, count=1, flags=re.M)
won = str(WORK / 'test' / ('_p926_%d_' % os.getpid() + pathlib.Path(build).name)); pathlib.Path(won).write_text(on)   # (the pid: two runs at once don't write each other's copies)
woff = str(WORK / 'test' / ('_p926_off_%d_' % os.getpid() + pathlib.Path(build).name)); pathlib.Path(woff).write_text(off)

# what was said in bubbles (bubbleSay, hooked once) and which dialogue cards opened (dialogueShow)
SAYHOOK = """(() => { window.__said = []; window.__cards = []; if (window.__hook) return; window.__hook = 1;
  const bs = bubbleSay; bubbleSay = function (who, text, secs) { if (who && who.p) window.__said.push([who.p.id, text, SHIP.time.min]); return bs.apply(this, arguments); };
  const ds = dialogueShow; dialogueShow = function (id, m) { window.__cards.push([id, SHIP.time.min]); return ds.apply(this, arguments); }; })()"""
# put you in the middle of one of a tradition's rooms on this deck (day d, id)
INROOM = """(() => { const e = eventsOn(%d).find(x => x.id === '%s'); if (!e) return 'not on'; const rk = [...eventRooms(e.ev)].map(r => r.split('|')).filter(r => +r[0] === deckDef.num).map(r => r[1]);
  const k = rk.find(r => ROOM_TILES[r] && ROOM_TILES[r].length > 12) || rk[0], tl = ROOM_TILES[k], c = cellPos(...tl[Math.floor(tl.length / 2)]); player.obj.position.set(c.x, 0, c.z); player.stop(); return k; })()"""

def talk13(path, label):
    g = Game(pw, path, 900, 760)
    g.ev("(() => { skipTo(7 * 1440 + 1135); goToDeck(7, null); SHIP.device.settings.tips = false; })()"); g.ev(SAYHOOK); g.step(10)
    room = g.ev(INROOM % (8, 'rec-chiefs-talk'))
    for _ in range(120):
        g.step(30)
        if g.ev('SHIP.time.min') >= 1180: break
    r = json.loads(g.ev("""JSON.stringify({ t: recTalk(8), sato: DECK_CREW.some(x => x.p.id === 'sato'), stool: (() => { const a = DECK_CREW.find(x => x.p.id === 'sato'), pl = a && a.goalId && PLACE_OF.get(a.goalId); return pl ? pl.type : null; })(),
      said: window.__said.filter(x => x[0] === 'sato'), want: (MEETING_SCRIPTS['talk.sato'] || { lines: [] }).lines.filter(x => x.text && !x.choice).map(x => x.text),
      cards: window.__cards, joined: SHIP.events.joined.includes('rec-chiefs-talk@8'), open: !!DIALOGUE && DIALOGUE.id })"""))
    g.close()
    said = [x[1] for x in r['said']]
    print('  13 (%s): in %s; the talk %s; Sato here %s (at %s); said %d of %d lines; cards %s; joined %s' % (label, room, r['t'], r['sato'], r.get('stool'), len(said), len(r['want']), r['cards'], r['joined']))
    return r, said, g.errors

with sync_playwright() as pw:
    if want('13'):
        r, said, err = talk13(woff, 'off')
        check(not said, '13 off: as 0.92.5, Sato says nothing from the stool (%d lines)' % len(said))
        r, said, err = talk13(won, 'on')
        check(r['sato'] and r.get('stool') == 'rec:stool', '13: Dr. Sato is on the stool for her Day 8 talk (%s)' % r.get('stool'))
        check(len(r['want']) >= 4 and said == r['want'], '13: she says the whole of talk.sato, from its first line, every line in order once (%s)' % said[:2])
        last = r['said'][-1][2] if r['said'] else None
        asks = [c for c in r['cards'] if c[0].startswith('talk.sato')]
        check(r['joined'] and len(asks) == 1 and asks[0][0] == 'talk.sato.ask' and last is not None and asks[0][1] >= last,
              '13: joined, the question card opens once, after her last line (%s; last line at %s)' % (asks, last))
        check(r.get('open') == 'talk.sato.ask', '13: the question card is still open minutes later, at %s (FX22: no `where` closed it at the next ship minute) (%s)' % (r['t'] and 1180, r.get('open')))
        check(not err, '13: no errors: ' + ' | '.join(err[:5]))
    if want('8'):
        END = [(2, 'tiles-night', 3), (4, 'quiz', 3), (5, 'jam', 4)]
        def late8(path):
            res = []
            for d, tid, deck in END:
                g = Game(pw, path, 900, 760)
                to = g.ev("(() => { const e = eventsOn(%d).find(x => x.id === '%s'); return e ? e.to : null; })()" % (d, tid))
                if to is None: res.append((tid, 'not on')); g.close(); continue
                g.ev("(() => { skipTo((%d - 1) * 1440 + %d - 9); goToDeck(%d, null); SHIP.device.settings.tips = false; })()" % (d, to, deck)); g.step(10)
                g.ev(INROOM % (d, tid)); g.step(120)
                r = json.loads(g.ev("""(() => { const now = shipNow(), t = SHIP.time.min, cal = JSON.stringify(DEVICE_APPS.get('calendar').view()), home = JSON.stringify(DEVICE_APPS.get('home').view());
                  const e = eventsOn(%d).find(x => x.id === '%s'), n = TJ_NOW && TJ_NOW.e.id === e.id ? TJ_NOW : null;
                  let joined = false; if (n && n.agent) { tradJoinTap(n.agent); joined = SHIP.events.joined.includes(e.id + '@%d'); }
                  return JSON.stringify({ t, to: e.to, offered: !!n, lead: n && n.lead, joined, cal: cal.includes(e.name), home: home.includes(e.name) }); })()""" % (d, tid, d)))
                res.append((tid, r)); err = g.errors; g.close()
                check(not err, '8 (%s): no errors: %s' % (tid, ' | '.join(err[:3])))
            return res
        roff = late8(woff); print('  8 off:', roff)
        check(any(isinstance(r, dict) and not (r['offered'] and r['joined'] and r['cal'] and r['home']) for _, r in roff), '8 off: as 0.92.5, at least one is no longer offered or listed near its end')
        for tid, r in late8(won):
            if not check(isinstance(r, dict), '8: %s on (%s)' % (tid, r)): continue
            check(r['to'] - r['t'] <= 8 and r['offered'] and r['joined'], '8: %s at %d (ends %d): the join is offered (leader %s) and a tap joins you' % (tid, r['t'], r['to'], r['lead']))
            check(r['cal'] and r['home'], '8: %s still on the device near its end: Calendar %s, Home %s' % (tid, r['cal'], r['home']))
        # RV14: the leader really gone (Tiles night, Day 2, 5 minutes before its end: Rina taken out of DECK_CREW for one minute's
        # tradJoinMinute, put back in the same evaluate): anyone still at it leads, and a tap on them joins you
        g = Game(pw, won, 900, 760)
        to = g.ev("eventsOn(2).find(x => x.id === 'tiles-night').to")
        g.ev("(() => { skipTo(1440 + %d - 9); goToDeck(3, null); SHIP.device.settings.tips = false; })()" % to); g.step(10); g.ev(INROOM % (2, 'tiles-night')); g.step(120)
        r = json.loads(g.ev("""(() => { const e = eventsOn(2).find(x => x.id === 'tiles-night'), lead = tradLeader({ ...e, day: 2 }), k = DECK_CREW.findIndex(a => a.p && a.p.id === lead);
          if (k < 0) return JSON.stringify({ err: 'the leader ' + lead + ' not on the deck' }); const gone = DECK_CREW.splice(k, 1)[0];
          let out; try { tradJoinMinute(shipNow()); const n = TJ_NOW && TJ_NOW.e.id === 'tiles-night' ? TJ_NOW : null; out = { lead, now: n && n.lead };
            if (n && n.agent) { tradJoinTap(n.agent); out.joined = SHIP.events.joined.includes('tiles-night@2'); } } finally { DECK_CREW.splice(k, 0, gone); }
          return JSON.stringify(out); })()"""))
        err = g.errors; g.close()
        check('err' not in r and r.get('now') and r['now'] != r['lead'] and r.get('joined'), '8: the leader gone near the end, someone still at it leads and a tap joins you (RV14) (%s)' % r)
        check(not err, '8 (leader gone): no errors: ' + ' | '.join(err[:3]))
    if want('5'):
        def week5(path):
            g = Game(pw, path, 900, 760)
            g.ev("(() => { skipTo(6 * 1440 + 1028); goToDeck(3, null); SHIP.device.settings.tips = false; })()"); g.ev(SAYHOOK); g.step(10)
            room = g.ev(INROOM % (7, 'one-week-aboard'))
            for _ in range(80):
                g.step(30)
                if g.ev('SHIP.time.min') >= 1045: break
            r = json.loads(g.ev("""(() => { const z = DECK_CREW.find(x => x.p.id === 'torres-zeke'), here = z && roomAt(...cellAt(z.x, z.z));
              const n = TJ_NOW && TJ_NOW.e.id === 'one-week-aboard' ? TJ_NOW : null, out = { t: SHIP.time.min, zeke: !!z, room: here ? (deckDef.rooms[here] || {}).name : null, sit: z ? /^sit/.test(z.pose || '') || (z.spot || {}).pose === 'sit' : false, lead: n && n.lead };
              if (z) tradJoinTap(z); out.cards = window.__cards.map(c => c[0]); out.act = ACT && ACT.kind;
              const v = DIALOGUE && DIALOGUE.id === 'week1.zeke' ? MEETING_SCRIPTS['week1.zeke'].lines.filter(l => l.text).map(l => evText(l.text, {})) : [];
              out.lines = v; return JSON.stringify(out); })()"""))
            g.step(180); r['open'] = g.ev('[!!DIALOGUE && DIALOGUE.id, SHIP.time.min]')
            err = g.errors; g.close(); return r, err
        r, err = week5(woff); print('  5 off:', r)
        check('week1.zeke' not in r['cards'], '5 off: as 0.92.5, no sit-down with Zeke')
        r, err = week5(won); print('  5 on:', r)
        check(r['zeke'] and r['room'] == 'Bow lounge' and r['sit'], '5: Zeke is in the bow lounge, sitting, at %s (%s, %s)' % (r['t'], r['room'], r['sit']))
        check(r['lead'] == 'torres-zeke', '5: the join is Zeke\'s (%s)' % r['lead'])
        check('week1.zeke' in r['cards'] and len(r['lines']) >= 4 and not any('{' in l for l in r['lines']), '5: a tap opens his card going over your week, filled in (%s)' % r['lines'][:2])
        check(r.get('open', [0])[0] == 'week1.zeke' and r['open'][1] - r['t'] >= 3, '5: his card is still open 3 ship minutes later, no input (RV14, FX22) (%s, tapped at %.1f)' % (r.get('open'), r['t']))
        check(not err, '5: no errors: ' + ' | '.join(err[:5]))
        # lead 36: tapped from the doorway (on the promenade, outside the bow lounge), then walking in: the card stays open
        g = Game(pw, won, 900, 760)
        g.ev("(() => { skipTo(6 * 1440 + 1040); goToDeck(3, null); SHIP.device.settings.tips = false; })()"); g.step(150)
        r = json.loads(g.ev("""(() => { const c = cellPos(40, 10); player.obj.position.set(c.x, 0, c.z); player.stop(); const room0 = (deckDef.rooms[roomAt(...player.here())] || {}).name;
          const z = DECK_CREW.find(x => x.p.id === 'torres-zeke'); tradJoinMinute(shipNow()); if (z) tradJoinTap(z); return JSON.stringify({ room0, t: SHIP.time.min, card: !!DIALOGUE && DIALOGUE.id }); })()"""))
        g.step(240); r2 = json.loads(g.ev("JSON.stringify({ t: SHIP.time.min, card: !!DIALOGUE && DIALOGUE.id, room: (deckDef.rooms[roomAt(...player.here())] || {}).name })"))
        err = g.errors; g.close()
        check(r['room0'] != 'Bow lounge' and r['card'] == 'week1.zeke' and r2['card'] == 'week1.zeke' and r2['room'] == 'Bow lounge' and r2['t'] - r['t'] >= 3,
              '5: tapped from the doorway (%s), you walk in and his card is still open %.1f ship minutes later (lead 36) (%s -> %s)' % (r['room0'], r2['t'] - r['t'], r, r2))
        check(not err, '5 (doorway): no errors: ' + ' | '.join(err[:3]))
    if want('2'):
        def swap2(path):
            g = Game(pw, path, 900, 760)
            g.ev("(() => { skipTo(13 * 1440 + 640); goToDeck(3, null); SHIP.device.settings.tips = false; })()"); g.ev(SAYHOOK); g.step(10)
            g.ev("(() => { const c = cellPos(36, 10); player.obj.position.set(c.x, 0, c.z); player.stop(); })()")
            for _ in range(80):
                g.step(30)
                if g.ev('SHIP.time.min') >= 660: break
            r = json.loads(g.ev("""(() => { const at = DECK_CREW.filter(a => a.settled && a.spot && evTagId(a.tag || '') === 'market'), n = TJ_NOW && TJ_NOW.e.id === 'market' ? TJ_NOW : null;
              const out = { t: SHIP.time.min, stall: at.filter(a => /^3-swap-stall-/.test(a.spot.id)).map(a => a.p.id).sort(), n: at.length, lead: n && n.lead, said: window.__said.length };
              const o = DECK_CREW.find(a => a.p.id === 'ishikawa-orla'); if (o) tradJoinTap(o); out.cards = window.__cards.map(c => c[0]); return JSON.stringify(out); })()"""))
            g.step(180); r['open'] = g.ev('[!!DIALOGUE && DIALOGUE.id, SHIP.time.min]')
            err = g.errors; g.close(); return r, err
        r, err = swap2(woff); print('  2 off:', r)
        check(not r['stall'] and 'swap.meet' not in r['cards'], '2 off: as 0.92.5, nobody at the stalls and no swap')
        r, err = swap2(won); print('  2 on:', r)
        check(r['stall'] == ['ishikawa-orla', 'shah-dara'], '2: Orla and Dara at the stalls (%s)' % r['stall'])
        check(r['n'] >= 5 and r['lead'] == 'ishikawa-orla', '2: people at it (%d), the join Orla\'s (%s)' % (r['n'], r['lead']))
        check('swap.meet' in r['cards'] and r['said'] >= 3, '2: a tap opens the swap card (%s), and the stalls talk (%d bubbles)' % (r['cards'], r['said']))
        check(r.get('open', [0])[0] == 'swap.meet' and r['open'][1] - r['t'] >= 3, '2: the swap card is still open 3 ship minutes later, no input (RV14, FX22) (%s, tapped at %.1f)' % (r.get('open'), r['t']))
        check(not err, '2: no errors: ' + ' | '.join(err[:5]))
    if want('15'):
        def spice15(path):
            g = Game(pw, path, 900, 760)
            g.ev("(() => { skipTo(15 * 1440 + 1100); goToDeck(3, null); SHIP.device.settings.tips = false; })()"); g.ev(SAYHOOK); g.step(10)
            g.ev(INROOM % (16, 'spice-shelf-supper'))
            seen = None; card = None; held = None
            for _ in range(200):
                g.step(30)
                x = json.loads(g.ev("JSON.stringify([SHIP.time.min, (DECK_CREW.find(a => a.p.id === 'brennan') || {}).spot ? DECK_CREW.find(a => a.p.id === 'brennan').spot.id : null, !!DIALOGUE && DIALOGUE.id])"))
                if x[1] == '3-spice-host' and seen is None: seen = x[0]
                if x[0] >= 1101 and g.ev("typeof TRAD995_ON !== 'undefined' && TRAD995_ON && !SHIP.events.joined.includes('spice-shelf-supper@16')"): g.ev("tradJoinTap(DECK_CREW.find(a => a.p.id === 'brennan'))")   # 0.99.5 note 19 (TB3): tap to join, switched on
                if x[2] == 'spice.guess' and card is None: card = x[0]
                if card is not None and held is None and x[0] >= card + 3: held = x[2]; g.ev("(() => { let n = 0; while (DIALOGUE && /^spice\\.guess/.test(DIALOGUE.id) && n++ < 10) { const v = dialogueView(); dialogueStep(v && v.choices ? 0 : undefined); } })()")   # answered (TB5: with TRAD995_ON a card left open holds the reveal up to a minute)
                if x[0] >= 1141: break
            r = json.loads(g.ev("""JSON.stringify({ said: window.__said.map(x => x[0] + ': ' + x[1]), cards: window.__cards.map(c => c[0]), joined: SHIP.events.joined.includes('spice-shelf-supper@16') })"""))
            err = g.errors; g.close(); r['seen'] = seen; r['held'] = held; return r, err
        r, err = spice15(woff); print('  15 off:', r['seen'], r['cards'], len(r['said']))
        check(r['seen'] is None and 'spice.guess' not in r['cards'], '15 off: as 0.92.5, Brennan never at the shelf, no guessing')
        r, err = spice15(won); print('  15 on: Brennan at the shelf from', r['seen'], r['cards'], r['said'][:12])
        b = [x for x in r['said'] if x.startswith('brennan: ')]; o = [x for x in r['said'] if not x.startswith('brennan: ')]
        check(r['seen'] is not None and r['seen'] <= 1120, '15: Brennan at the spice shelf by 18:40 (%s)' % r['seen'])
        check(len(b) >= 5, '15: she opens, names three jars and says whose (%d lines)' % len(b))
        check(len(o) >= 3, '15: the mess guesses out loud (%d bubbles)' % len(o))
        check(r['joined'] and 'spice.guess' in r['cards'], '15: joined, your guess card (%s)' % r['cards'])
        check(r.get('held') == 'spice.guess', '15: the guess card is still open 3 ship minutes later, no input (RV14, FX22) (%s)' % r.get('held'))
        check(not err, '15: no errors: ' + ' | '.join(err[:5]))
    if want('4'):
        def read4(path, day):
            g = Game(pw, path, 900, 760)
            g.ev("(() => { skipTo(" + str(day - 1) + " * 1440 + 965); goToDeck(3, null); SHIP.device.settings.tips = false; })()"); g.ev(SAYHOOK); g.step(10)
            g.ev(INROOM % (day, 'reading-corner'))
            for _ in range(120):
                g.step(30)
                if g.ev('SHIP.time.min') >= 990: break
            r = json.loads(g.ev("""(() => { const at = DECK_CREW.filter(a => a.settled && a.spot && evTagId(a.tag || '') === 'reading-corner');
              const far = at.map(a => { const pl = PLACE_OF.get(a.spot.id), xy = pl && (pl.xy || pl.at); return [a.p.id, a.spot.id, xy ? +Math.hypot(xy[0] - 48.7, xy[1] - 11).toFixed(1) : 99, (a.spot.pose || '')]; });
              const host = at.find(a => a.p.id === 'walsh-esme'), out = { t: SHIP.time.min, at: far, host: !!host, said: window.__said.length };
              const a = host || at[0]; if (a) tradJoinTap(a); out.act = ACT && ACT.kind; return JSON.stringify(out); })()"""))
            err = g.errors; g.close(); return r, err
        r, err = read4(woff, 14); print('  4 off (Day 14):', r)
        check(not r['host'], '4 off: as 0.92.5, no host')
        r, err = read4(won, 14); print('  4 on, Day 14 (an even week: none):', r)
        check(not r['host'] and not r['at'] and r['act'] is None, '4: Day 14, an even week since FX24: no reading corner, no host alone (%s)' % r)
        r, err = read4(won, 21); print('  4 on (Day 21):', r)
        check(r['host'] and len(r['at']) >= 3, '4: Esme Walsh hosts, %d at it' % len(r['at']))
        check(all(x[2] <= 4.5 and x[3] == 'sit' for x in r['at']), '4: everyone at it sits within 4.5 m of the window sofa (%s)' % [x for x in r['at'] if x[2] > 4.5 or x[3] != 'sit'])
        check(r['said'] >= 4, '4: they talk about their books (%d bubbles)' % r['said'])
        check(r['act'] == 'tj:reading-corner', '4: a tap joins you (%s)' % r['act'])
        check(not err, '4: no errors: ' + ' | '.join(err[:5]))
    if want('3'):
        STANDS = """JSON.stringify((() => { const S = schedData(), seats = new Set((S.shared.get('7|rec-stand') || []).map(pl => pl.id)), out = [];
          for (const d of [14, 21]) { if (!eventsOn(d).some(e => e.id === 'rec-wso')) { out.push([d, 'not on']); continue; }
            for (const m of [750, 810, 870, 930]) { const t = (d - 1) * 1440 + m; let n = 0; for (const p of schedPeople()) { const s = planDay(p, d).find(x => x.from <= t && x.to > t); if (s && seats.has(s.placeId)) n++; } out.push([d, m, n, seats.size]); } }
          return out; })())"""
        def stands3(path):
            g = Game(pw, path, 900, 760); r = json.loads(g.ev(STANDS)); err = g.errors; g.close(); return r, err
        r, err = stands3(woff); print('  3 off (day, minute, in the stands, seats):', r)
        check(any(len(x) == 4 and (x[2] < 9 or x[1] in (810, 870) and x[2] < 12) for x in r), '3 off: as 0.92.5, the stands thin (under 9, or under 12 mid-afternoon) at least once')
        r, err = stands3(won); print('  3 on:', r)
        check(all(len(x) == 4 and x[2] >= 9 and (x[1] not in (810, 870) or x[2] >= 12) for x in r), '3: the stands fill: 9 or more all afternoon, 12 or more at 13:30 and 14:30 (nearly everyone off duty and aboard: the stands have 33 seats) (%s)' % r)
        check(not err, '3: no errors: ' + ' | '.join(err[:5]))
    if want('7'):
        WEEKS = """JSON.stringify((() => { const talks = [32, 36, 43, 46, 50, 57, 60, 64, 71, 74, 78].map(d => [d, recTalk(d), eventsOn(d).filter(e => /^rec-(wren|chiefs)-talk$/.test(e.id)).map(e => e.id)]);
          const spk = []; for (let d = 30; d <= 84; d++) { const t = recTalk(d), e = t && eventsOn(d).find(x => /^rec-(wren|chiefs)-talk$/.test(x.id)), p = t && schedPeople().find(q => q.id === t.by);
            if (e && p) spk.push([d, t.by, planDay(p, d).some(s => evTagId(s.tag) === e.id)]); }
          const ms = [42, 84].map(d => [d, eventsOn(d).map(e => e.id).filter(i => /weeks-aboard$/.test(i))]);
          const seen = new Set(), wk = []; for (let w = 0; w < 12; w++) { const ids = new Set(); for (let d = w * 7 + 1; d <= w * 7 + 7; d++) for (const e of eventsOn(d)) if (e.id !== 'birthday') ids.add(e.id);
            wk.push([w + 1, [...ids].filter(i => !seen.has(i))]); for (const i of ids) seen.add(i); }
          const hosts = []; for (let d = 1; d <= 112; d++) for (const e of eventsOn(d)) { if (!P926_NEW.has(e.id) || !e.ev.host) continue; const h = schedPeople().find(q => q.id === e.ev.host);
            hosts.push([d, e.id, e.ev.host, !!h && planDay(h, d).some(s => evTagId(s.tag) === e.id)]); }
          const away = []; for (let d = 1; d <= 112; d++) for (const ev of SHIP_TRADITIONS) if (P926_NEW.has(ev.id) && ev.host && evDue(ev.when, d)) { const h = schedPeople().find(q => q.id === ev.host); if (h && !aboard(h, d)) away.push([d, ev.id, eventsOn(d).some(e => e.id === ev.id)]); }
          const meet = []; for (let d = 1; d <= 112; d++) for (const e of eventsOn(d)) { if (!(e.ev.stay || P926_NEW.has(e.id))) continue;
            for (const p of schedPeople()) { const segs = planDay(p, d), mine = segs.filter(s => evTagId(s.tag) === e.id); if (!mine.length) continue;
              for (const g of (typeof eventMeetPlan === 'function' ? eventMeetPlan(p, d, null) : [])) if (mine.some(s => s.from < (d - 1) * 1440 + g.at + g.dur && (d - 1) * 1440 + g.at < s.to)) meet.push([d, e.id, p.id, g.tag]); } }
          return { talks, ms, wk, spk, hosts, away, meet }; })())"""
        def weeks7(path):
            g = Game(pw, path, 900, 760); r = json.loads(g.ev(WEEKS)); err = g.errors; g.close(); return r, err
        r, err = weeks7(woff); print('  7 off: talks', [(t[0], bool(t[1])) for t in r['talks']], 'milestones', r['ms'], 'new by week', r['wk'][4:])
        check(not any(t[1] for t in r['talks'] if t[0] > 29) and not any(m[1] for m in r['ms']), '7 off: as 0.92.5, no talks after Day 29, no milestones')
        r, err = weeks7(won); print('  7 on: talks', [(t[0], t[1] and t[1]['by'], t[2]) for t in r['talks']], 'milestones', r['ms'], 'new by week', r['wk'])
        check(all(t[1] and t[2] for t in r['talks']), '7 (b): a talk on each of Days 32-78\'s talk days, on the calendar (%s)' % [t[0] for t in r['talks'] if not (t[1] and t[2])])
        print('  7 new traditions, Days 1-112 (day, id, host, host there):', r['hosts'])
        check(r['hosts'] and all(x[3] for x in r['hosts']), '7: each new tradition\'s host is planned at every showing, Days 1-112 (RV14) (missing: %s)' % [x[:3] for x in r['hosts'] if not x[3]])
        check(not any(x[2] for x in r['away']), '7: a new tradition gives way when its host is away (RV14) (%s)' % r['away'])
        check(not r['meet'], '7: nobody planned at Winner stays on or a new tradition over their own ship-wide event meeting, Days 1-112 (lead 36: the Captain at the Line on Day 7) (%s)' % r['meet'][:5])
        check(r['spk'] and all(x[2] for x in r['spk']), '7 (b): every talk\'s speaker is planned at it, Days 30-84 (missing: %s)' % [x[:2] for x in r['spk'] if not x[2]])
        check([m[1] for m in r['ms']] == [['six-weeks-aboard'], ['twelve-weeks-aboard']], '7 (c): Six weeks aboard on Day 42, Twelve weeks on Day 84 (%s)' % r['ms'])
        check(all(w[1] for w in r['wk'][4:]), '7 (a): weeks 5-12 each bring a tradition not seen before (%s)' % [w[0] for w in r['wk'][4:] if not w[1]])
        check(not err, '7: no errors: ' + ' | '.join(err[:5]))
print('P926 CHECK OK' if ok else 'P926 CHECK FAILED')
sys.exit(0 if ok else 1)
