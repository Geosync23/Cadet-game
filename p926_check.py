# Starship Cadet: the 0.92.6 traditions check (FX17; plans/patch-0.92.6.md items 2-5, 7, 8, 13, 15; keep in the repo)
# Runs on a copy of the build with P926_TRADS on (a URL flag in the game until it's switched on; then `true`), and a copy with it
# off as the base. Each part is one of the user's playtest notes; each fails on 0.92.5 and passes with the switch on:
#   13  the Day 8 talk is spoken: Dr. Sato on the stool says talk.sato line by line in her bubble, every line in order once, while
#       you're in the auditorium; joined, the question card (talk.sato.ask) opens after the last line, not before. Off: nothing said
#   8   a tradition can be joined to its end: 5 minutes before the end of Tiles night (Day 2), quiz night (Day 4) and the jam (Day 5),
#       in its room, the join is offered (TJ_NOW, its leader on the deck) and a tap on the leader joins you; the device's Calendar and
#       Home still list it ("on now, until"). Off: at least one of them not offered or not listed
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
won = str(WORK / 'test' / ('_p926_' + pathlib.Path(build).name)); pathlib.Path(won).write_text(on)
woff = str(WORK / 'test' / ('_p926_off_' + pathlib.Path(build).name)); pathlib.Path(woff).write_text(off)

# what was said in bubbles (bubbleSay, hooked once) and which dialogue cards opened (dialogueShow)
HOOK = """(() => { window.__said = []; window.__cards = []; if (window.__hook) return; window.__hook = 1;
  const bs = bubbleSay; bubbleSay = function (who, text, secs) { if (who && who.p) window.__said.push([who.p.id, text, SHIP.time.min]); return bs.apply(this, arguments); };
  const ds = dialogueShow; dialogueShow = function (id, m) { window.__cards.push([id, SHIP.time.min]); return ds.apply(this, arguments); }; })()"""
# put you in the middle of one of a tradition's rooms on this deck (day d, id)
INROOM = """(() => { const e = eventsOn(%d).find(x => x.id === '%s'); if (!e) return 'not on'; const rk = [...eventRooms(e.ev)].map(r => r.split('|')).filter(r => +r[0] === deckDef.num).map(r => r[1]);
  const k = rk.find(r => ROOM_TILES[r] && ROOM_TILES[r].length > 12) || rk[0], tl = ROOM_TILES[k], c = cellPos(...tl[Math.floor(tl.length / 2)]); player.obj.position.set(c.x, 0, c.z); player.stop(); return k; })()"""

def talk13(path, label):
    g = Game(pw, path, 900, 760)
    g.ev("(() => { skipTo(7 * 1440 + 1135); goToDeck(7, null); SHIP.device.settings.tips = false; })()"); g.ev(HOOK); g.step(10)
    room = g.ev(INROOM % (8, 'rec-chiefs-talk'))
    for _ in range(120):
        g.step(30)
        if g.ev('SHIP.time.min') >= 1180: break
    r = json.loads(g.ev("""JSON.stringify({ t: recTalk(8), sato: DECK_CREW.some(x => x.p.id === 'sato'), stool: (DECK_CREW.find(x => x.p.id === 'sato') || {}).spot ? DECK_CREW.find(x => x.p.id === 'sato').spot.type : null,
      said: window.__said.filter(x => x[0] === 'sato'), want: (MEETING_SCRIPTS['talk.sato'] || { lines: [] }).lines.filter(x => x.text && !x.choice).map(x => x.text),
      cards: window.__cards, joined: SHIP.events.joined.includes('rec-chiefs-talk@8') })"""))
    g.close()
    said = [x[1] for x in r['said']]
    print('  13 (%s): in %s; the talk %s; Sato here %s (at %s); said %d of %d lines; cards %s; joined %s' % (label, room, r['t'], r['sato'], r['stool'], len(said), len(r['want']), r['cards'], r['joined']))
    return r, said, g.errors

with sync_playwright() as pw:
    if want('13'):
        r, said, err = talk13(woff, 'off')
        check(not said, '13 off: as 0.92.5, Sato says nothing from the stool (%d lines)' % len(said))
        r, said, err = talk13(won, 'on')
        check(r['sato'] and r['stool'] == 'rec:stool', '13: Dr. Sato is on the stool for her Day 8 talk (%s)' % r['stool'])
        check(len(r['want']) >= 4 and said == r['want'], '13: she says the whole of talk.sato, from its first line, every line in order once (%s)' % said[:2])
        last = r['said'][-1][2] if r['said'] else None
        asks = [c for c in r['cards'] if c[0].startswith('talk.sato')]
        check(r['joined'] and len(asks) == 1 and asks[0][0] == 'talk.sato.ask' and last is not None and asks[0][1] >= last,
              '13: joined, the question card opens once, after her last line (%s; last line at %s)' % (asks, last))
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
print('P926 CHECK OK' if ok else 'P926 CHECK FAILED')
sys.exit(0 if ok else 1)
