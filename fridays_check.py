#!/usr/bin/env python3
"""fridays_check.py: Short Fridays and the Captain's address (section 18f, the Fridays builder FR1;
plans/fridays-build-brief.md), on paper, about a minute a build.

  CADET_CHROME=/opt/pw-browsers/chromium python3 fridays_check.py BUILD.html

With SHORT_FRIDAY off (the build as it is): no short Friday, no address in the traditions, the day shift ends at
17:00 every day. With it on (a test copy is made with the switch line flipped): the day shift ends at 15:30 on
Fridays; the address is on every Friday from Day 5 at 16:00-16:50 and on no other day; it sits inside the events
base's Friday hold (EV_BEATS' 'fridayAddress' row, when the build has it); no other tradition overlaps Friday
15:30-17:00; Marrow and Vance plan the lectern, nobody of the Friday skeleton comes, and the auditorium fills
(Days 5 and 12); the Thursday Mail is the first week's on Day 4 and the usual one after. Prints FRIDAYS CHECK OK.
"""
import os, sys, re, json, pathlib

GAME = sys.argv[1] if len(sys.argv) > 1 else 'starship-cadet.html'
ROOT = pathlib.Path(__file__).resolve().parent
src = open(ROOT / 'cadet_test.py').read().split("a, shots = run(")[0]
exec(src)
from playwright.sync_api import sync_playwright

fails = []
def check(ok, what):
    if not ok: fails.append(what); print('  FAIL', what)
    return ok

text = pathlib.Path(GAME).read_text()
if not re.search(r'^const SHORT_FRIDAY = (true|false);', text, re.M):
    print('FRIDAYS CHECK FAILED: no SHORT_FRIDAY switch in', GAME); sys.exit(1)
work = WORK / 'test'; work.mkdir(parents=True, exist_ok=True)
copies = {}
for on in (False, True):
    p = work / ('_fri_' + ('on' if on else 'off') + '.html')
    p.write_text(re.sub(r'^const SHORT_FRIDAY = (true|false);', 'const SHORT_FRIDAY = %s;' % ('true' if on else 'false'), text, flags=re.M))
    copies[on] = p

PAPER = r"""(() => {
  const out = {}, ppl = schedPeople(), A = 'captains-address';
  out.inTable = SHIP_TRADITIONS.some(e => e.id === A);
  out.ends = [4, 5, 6, 12].map(d => [d, dayShiftEnd(d)]);
  out.on = []; for (let d = 1; d <= 40; d++) { const e = eventsOn(d).find(x => x.id === A); if (e) out.on.push([d, e.from, e.to]); }
  let hold = null; try { const b = EV_BEATS.find(x => x.id === 'fridayAddress'); if (b) hold = { at: b.at, fromDay: b.fromDay, weekday: b.weekday }; } catch (e) { hold = 'none'; }
  out.hold = hold;
  out.clash = [];
  for (let d = 1; d <= 40; d++) if (weekday(d) === 4) for (const e of eventsOn(d)) if (e.id !== A && e.from < 1020 && e.to > 930) out.clash.push([d, e.id, e.from, e.to]);
  out.days = {};
  for (const d of [5, 12]) {
    const at = (d - 1) * 1440 + 970, here = [], lect = [];
    for (const p of ppl) { const w = planWhere(p, at); if (!w || w.deck !== 7) continue; if (w.type === 'rec:lectern') lect.push(p.id); else if (w.type === 'rec-aud' || /^ev-captains-address/.test(w.tag || '')) here.push(p.id); }
    out.days[d] = { here: here.length, lect, skel: ppl.filter(p => friSkeleton(p, d)).map(p => p.id), skelHere: ppl.filter(p => friSkeleton(p, d) && (here.includes(p.id) || lect.includes(p.id))).map(p => p.id),
      night: ppl.filter(p => p.shift === 'night' && here.includes(p.id)).length, nights: ppl.filter(p => p.shift === 'night').length,
      storm: !!eventOn(d), double: ['marrow', 'vance'].filter(id => { const p = ppl.find(q => q.id === id); return p && schedFrame(p, d).double; }) };
  }
  const e5 = eventsOn(5).find(x => x.id === A), e12 = eventsOn(12).find(x => x.id === A);
  out.mail = [e5 && e5.ev.mail ? evText(e5.ev.mail, e5) : null, e12 && e12.ev.mail ? evText(e12.ev.mail, e12) : null];
  out.week1 = friText('fri.mail.week1');
  out.errors = TRAD_ERRORS.filter(x => /captains/.test(x));
  return out;
})()"""

with sync_playwright() as pw:
    res = {}
    for on in (False, True):
        g = Game(pw, str(copies[on]), 390, 844)
        res[on] = g.ev(PAPER)
        if g.errors: check(False, ('on' if on else 'off') + ': page errors ' + str(g.errors[:3]))
        g.b.close()

off, on = res[False], res[True]
print('off:', json.dumps({k: off[k] for k in ('inTable', 'ends', 'on')}))
check(not off['inTable'] and not off['on'], 'off: the address is in the game')
check(all(e == 1020 for _, e in off['ends']), 'off: a shift ending before 17:00 %s' % off['ends'])

print('on: ends', on['ends'], '| address on', on['on'][:6], '| hold', on['hold'])
check(on['inTable'], 'on: the address is not in the traditions')
check(dict(on['ends']) == {4: 1020, 5: 930, 6: 1020, 12: 930}, 'on: shift ends %s' % on['ends'])
days = [d for d, _, _ in on['on']]
check(days == [d for d in range(5, 41) if (d - 1) % 7 == 4], 'on: the address on days %s (want every Friday from Day 5)' % days)
check(all(f == 960 and t == 1010 for _, f, t in on['on']), 'on: the address not at 16:00-16:50 %s' % on['on'])
h = on['hold']
if isinstance(h, dict):
    check(h['weekday'] == 4 and h['at'][0] <= 960 and h['at'][1] >= 1010 and h['fromDay'] <= 5, 'on: the address is outside the Friday hold %s' % h)
else:
    print('  (no EV_BEATS in this build: the hold is checked once the events base is in)')
check(not on['clash'], 'on: traditions overlapping Friday 15:30-17:00 %s' % on['clash'])
for d, x in on['days'].items():
    print('  Day %s at 16:10: %d in the seats, lectern %s, skeleton %s (here: %s), night shift %d of %d' % (d, x['here'], x['lect'], x['skel'], x['skelHere'], x['night'], x['nights']))
    if x['storm'] and x['double'] and not x['lect']:
        print('  (Day %s: %s on the storm\'s double shift: the events base\'s storm update exempts them for the address, EV1)' % (d, x['double']))
    else:
        check(sorted(x['lect']) == ['marrow', 'vance'], 'on: Day %s lectern %s' % (d, x['lect']))
    check(not x['skelHere'], 'on: Day %s skeleton at the address %s' % (d, x['skelHere']))
    check(len(x['skel']) == 3, 'on: Day %s skeleton %s' % (d, x['skel']))
    check(40 <= x['here'] <= 76, 'on: Day %s %d in the seats (want 40-76)' % (d, x['here']))
print('  Mail:', on['mail'])
check(on['mail'][0] == on['week1'] and on['week1'], 'on: Day 4 Mail is not the first week\'s')
check(on['mail'][1] and on['mail'][1] != on['week1'], 'on: Day 11 Mail is the first week\'s')
check(not on['errors'], 'on: tradition errors %s' % on['errors'])
print('FRIDAYS CHECK OK' if not fails else 'FRIDAYS CHECK FAILED (%d)' % len(fails))
sys.exit(1 if fails else 0)
