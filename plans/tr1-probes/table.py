# TR1: the per-tradition table for plans/review-tr1-traditions.md, from results/sweep-*.jsonl and TR1's verdicts below
import json, sys
hh = lambda m: '%02d:%02d' % (int(m) % 1440 // 60, int(m) % 60)
B = 'BROKEN'; W = 'WRONG'; R = 'ROUGH'; OK = 'OK'; T = 'OK (turn up)'
V = {   # id: (status, short note)
 'spice-shelf-supper': (B, 'no Tap to join; Brennan out ~23 min late; card only at 18:53 (see 1)'),
 'new-hands-tea': (B, 'your own welcome tea, Calder hosts: no tap, no moment; replaces Works tea, which has one (see 2)'),
 'four-weeks-aboard': (B, 'your four weeks, the cake: no tap, no moment (see 2)'),
 'six-weeks-aboard': (B, "Zeke's tea for your six weeks: no tap, no card (One week aboard has both) (see 2)"),
 'twelve-weeks-aboard': (B, "Calder's toast for your twelve weeks: no tap, no moment (see 2)"),
 'open-door': (B, "Calder's weekly tea: no tap, 1 there at +12 (paper: 3 of 15 fit), the 5-tile tea corner (see 2, 10)"),
 'tool-night': (B, '0.92.6 new: the eyes-shut tool game is not built; no tap (see 3)'),
 'route-night': (B, '0.92.6 new: "a pin for everyone" not built; no tap (see 3)'),
 'card-night': (B, '0.92.6 new: no tap, nothing to make (see 3)'),
 'garden-walk': (B, '0.92.6 new: no tap; a walk with no Tap to join walk (see 3)'),
 'window-sketch': (B, '0.92.6 new: no tap (see 3)'), 'window-sketch-2': (B, '0.92.6 new: no tap (see 3)'),
 'spoon-band': (B, '0.92.6 new: no tap (see 3)'), 'worst-joke': (B, '0.92.6 new: no tap (see 3)'), 'open-house': (B, '0.92.6 new: no tap (see 3)'),
 'off-the-tern': (W, 'design says "you can tap to join"; no Tap to join (see 4)'),
 'playlist-duel': (W, 'its star and arrow hidden by Book circle on the same deck (see 5)'),
 'tiles-ladder': (W, 'Saturdays: star hidden from 15:30 by Cook-along / Jar day (see 5)'),
 'cook-along': (W, 'some Saturdays its star hidden by the coffee trials (see 5)'),
 'whodunnit-club': (W, 'its star hidden by the tasting table from 20:00 (Day 66 on) (see 5)'),
 'running': (R, 'Day 8 Rina (host) not there; Saruth leads (see 7)'),
 'sunrise-stretch': (R, 'host not going some days (8, 12, 15) on paper; "About 46 minutes" toast for a 30-minute stretch (see 8)'),
 'name-on-the-beam': (W, 'note 8: you paint 1.4 m from your name; watchers under it'),
 'name-on-the-beam-new': (T, "Basil's name: you watch"),
 'birthday': (T, 'tap the cake (not a person)'), 'captains-address': (T, 'the address'), 'film': (T, 'turn up'), 'rec-film-night': (T, 'turn up'),
 'long-breakfast': (T, 'a meal'), 'sunday-table': (T, 'a meal'), 'farewell-supper': (T, 'a meal'), 'first-fruits': (T, 'a meal'), 'harvest-supper': (T, 'a meal'),
 'lanternSupper': (T, 'a meal, the storm'), 'party': (T, 'the storm\'s party'), 'lineCeremony': (T, 'ceremony card'), 'crossingBackCeremony': (T, 'ceremony card'),
 'vesselArrival': (T, 'the Veyli ship arrives'), 'founding': (T, 'turn up'), 'quiet-watch': (T, 'turn up'), 'years-end': (T, 'turn up'), 'midtour': (R, 'Oduya: "write a letter to yourself" not offered; no tap'),
 'hull-lights': (T, 'turn up'), 'late-piano': (T, 'listen'), 'tap-night': (R, 'no host; the drink of the week not offered'),
 'rec-chiefs-talk': (T, 'spoken talk; question card after'), 'rec-wren-talk': (T, 'spoken talk; question card after'), 'rec-talent-night': (T, 'act-or-watch card'),
 'talent-night': (R, 'Dahl hosts; no tap, no act card (the rec one has one)'),
 'cometCaptain': (OK, 'Officers and up only (you were a Cadet): by design'),
 'rec-dawn-swim': (R, 'host Rina, no tap (rec deck: use the pool)'), 'rec-wall-night': (R, 'host Tomas, no tap (use the wall)'), 'rec-paddle-club': (R, 'host Holt, no tap'),
 'rec-float-hour': (R, 'host Oduya, no tap'), 'rec-slow-stretch': (R, 'host Nandakumar, no tap'), 'rec-regatta': (R, 'host Holt, no tap'), 'rec-sim-night': (R, 'host Raman, no tap'),
 'rec-wso': (R, 'Pell\'s board; no host tap (5-6 at it by 13:30)'), 'rec-cup': (R, 'Pell\'s bracket; no host tap'),
 'midnight-toast': (OK, '4 still there 8 min after (within the 25-minute linger)'),
}
rows = [json.loads(l) for f in sys.argv[1:] for l in open(f)]
rows.sort(key=lambda r: ({B: 0, W: 1, R: 2}.get(V.get(r['id'], (OK,))[0], 3), r['id']))
print('| Tradition | Day, time | Where | There at +12 (at its places) | Join offered (leader) | Tap on leader/host | What you got | Status | Note |')
print('|---|---|---|---|---|---|---|---|---|')
for r in rows:
    t = r['tap'] if isinstance(r['tap'], dict) else {}
    st, note = V.get(r['id'], (OK, ''))
    got = (t.get('act') or '').split(':')[0] or ''
    cards = ','.join(c[1] for c in r.get('cards', []) if c[1] not in ('vesselSheet',))
    got = ', '.join(x for x in [got, cards] if x) or '-'
    print('| %s | D%s %s-%s | %s | %s (%s) | %s | %s | %s | %s | %s |' % (r['id'], r['day'], hh(r['from']), hh(r['to']), 'Deck ' + r['where'].replace('|', ' room '), r['peak']['tagged'], r['peak']['atIts'],
        (r['firstTj'] or [0, 'no'])[1], (t.get('who') or '-') + (': joined' if t.get('tapJoin') else ': nothing' if t else ''), got, st, note))
