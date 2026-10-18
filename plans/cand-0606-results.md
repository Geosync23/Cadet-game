# 0.60.6 candidate: intro_check results

- **Commit:** claude/cand-0606 96582c4
- **Check:** `CADET_CHROME=/opt/pw-browsers/chromium python3 intro_check.py starship-cadet.html` (full, no flags), run alone on check runner R4
- **Result:** OK (exit 0), no FAIL lines, all parts 0-12
- **Time:** 2026-10-18 00:48 to 02:45 UTC (~1h57m; part 12 took ~8-10 min per beat in the full run, against seconds in a --week-only run)
- **Warm-up:** `--week` on 890a1f3 was OK (3m49s)

## Full log

```
0. Test URLs start with the intro off
  intro off, Day 1 06:00, escort plan None, beats 0
1. The data
  15 steps on the arrival evening, 27 beats in the week, 15 Settling-in items
  torres-zeke off days 3,4
  calder off days 5,6
  halloran-emeka off days 5,6
2. The happy path, on paper (Day 0 17:30 to Day 8 00:00)
  order: manifest > ramp > hello > haulway > works > lift > wing > bunk > toMess > servery > table > chief > free > tomas > night
  points: {'torres-zeke': 10, 'tomas': 10, 'pell': 5, 'calder': 3, 'brennan': 3}
  flags: week1.d2 Day 2 06:00, week1.d3 Day 3 06:00, week1.d4 Day 4 06:00, week1.d5 Day 5 06:00, week1.d6 Day 6 06:00, week1.d7 Day 7 06:00, week1.done Day 8 00:00
  mail: Day 4 07:00 Zeke Torres: On your own; Day 7 18:00 I. Calder: One week
3. The wanderer and the idler
  wander: by Day 0 20:01 step None, missed 5 (ramp, haulway, lift, bunk, servery); mail: Your bunk
  idle: by Day 0 20:01 step None, missed 11 (ramp, hello, haulway, works, lift, wing, bunk, toMess, servery, table, chief); mail: Your bunk, Tomorrow
  slow (10 ship minutes behind at every step): missed 0 []
  one slow step then steady {'haulway': 25, 'rest': 7}: missed []
  one slow step then steady {'lift': 25, 'rest': 6}: missed []
  one slow step then steady {'bunk': 35, 'rest': 7}: missed []
  idle, then "I know my way around" on Monday 07:00: mug, seedling unset
4. Save and reload at every step
  14 reloads; the same as without: True
5. Skip-intro
  points {'torres-zeke': 10, 'tomas': 10, 'pell': 5, 'calder': 3, 'brennan': 3} (the evening's: True); every gate open: True; the week off: True
6. Determinism
  the same twice: True
7. The Settling-in list, and the job notes
  slot 1 turned in -> ['d1-shadow:job']
  every item ticks from its own note: True | all done sends the note: True
  Torres's tour (lines per place): shuttle 5 (writers), up 8 (writers), works 2 (writers), lift 5 (writers), officers 6 (writers), wing 6 (writers), deck3 8 (writers), servery 6 (writers)
8. The evening in the real game (New game arriving, a player who follows Torres and taps through meetings)
  the Tern: you start at [5, 7] (start [5, 7], INTRO_START [5, 7]), ramp 0
  the ramp right after signing 0, 5 s later 1; the pilot (the writers' line): Dev Raman, the pilotDown gently. Ramp's opening. Welcome to the Wren.
  tapping Torres on the ramp: introAsk (tapping someone else: False)
  tour lines with the week under way (place, played, written): [['shuttle', 5, 5], ['up', 8, 8], ['works', 2, 2], ['lift', 5, 5], ['officers', 6, 6], ['wing', 6, 6], ['deck3', 8, 8], ['servery', 6, 6]]
  Day 0, Sunday 17:33  ramp  (you: Deck 5 [5, 7]; Torres [5, 11])
  Day 0, Sunday 17:40  haulway  (you: Deck 5 [5, 11]; Torres [5, 11])
  Day 0, Sunday 17:40  the ramp closes behind you (you at [6, 11], ramp 0.79)
  Day 0, Sunday 17:47  works  (you: Deck 5 [11, 8]; Torres [10, 8])
  Day 0, Sunday 17:52  lift  (you: Deck 5 [15, 9]; Torres [15, 7])
  Day 0, Sunday 17:53  wing  (you: Deck 5 [15, 9]; Torres [15, 7])
  Day 0, Sunday 18:15  bunk  (you: Deck 4 [14, 5]; Torres [14, 5])
  Day 0, Sunday 18:18  toMess  (you: Deck 4 [8, 3]; Torres [9, 4])
  Day 0, Sunday 18:26  servery  (you: Deck 3 [21, 9]; Torres [21, 9])
  Day 0, Sunday 18:34  table  (you: Deck 3 [32, 4]; Torres [31, 5]; his seat 3-mess-12)
  at the table Day 0, Sunday 18:34: servery 22 portions of tacos (dinner), 46 crew in the mess, seats you 3-mess-10, Torres 3-mess-12
  Day 0, Sunday 18:37  free  (you: Deck 3 [28, 1]; Torres [28, 2]; his seat 3-mess-12)
  the dinner seats at Day 0, Sunday 18:38: yours ['3-mess-10', None, '3-mess-10'], Torres ['3-mess-12', 'torres-zeke'], Calder ['3-mess-9', 'calder']
  Day 0, Sunday 18:49  tomas  (you: Deck 3 [28, 1]; Torres [29, 1])
  Day 0, Sunday 18:49  the arrow points to your bunk
  Day 0, Sunday 19:30  night  (you: Deck 3 [28, 1]; Torres [28, 2])
  Day 0, Sunday 20:00  None  (you: Deck 3 [28, 1]; Torres [6, 1])
  the Chief's welcome (introChief): shown -317, ended -313 (None: cut short), goodnight -311
  his goodnight at -311 (ship minute; None: not with you), last lines said: ["Day 0, Sunday 19:38 Cheerful star names. Gerald's top.", "Day 0, Sunday 19:49 My lantern's square. It's tidier.", 'Day 0, Sunday 19:58 Nobody takes the green ones.']
  draw-call peaks by deck {5: 193, 4: 208, 3: 259}; Torres led you for 186 looks
  after each ride (from, to, time, you, Torres, tiles apart): [[5, 4, 'Day 0, Sunday 18:02', [20, 10], [20, 10], 0], [4, 3, 'Day 0, Sunday 18:22', [19, 9], [19, 9], 0]]
  the walk to the lift: 12 s with him on Deck 5 (18 looks), paused 0.0 s, longest standing still 0.0 s
  said up to the lift: ['17:35 Cadet? There you are. Zeke T', "17:37 Welcome to the Wren. She's g", "17:39 That's the Tern behind you. ", '17:41 Long trip? I bet. Tell me al', '17:43 Bag all right? Right, onward', "17:45 Don't learn it all tonight. ", "17:48 Honestly? We've all been wai", '17:50 Lost? Ask anyone. I got lost', "17:52 And that's us. Works. You an", "17:54 This is where we'll be most ", '17:56 The lift. Runs right up the ']
  the tour, following: core lines heard 18/18, all lines 28/46; per place shuttle 3/3+2, up 3/8+0, works 2/2+0, lift 3/3+0, officers 3/3+1, wing 2/2+2, deck3 2/2+2, servery 3/3+0
  the ramp: closed behind you at ('Day 0, Sunday 17:40', 'haulway', [6, 11]), open again at ('Day 0, Sunday 18:37', 'free') (target 1)
9. A first launch arrives (no save, never arrived, not a test URL), and its Day 0 save loads at the same step
  Day 0, Sunday 17:30, Deck 5, intro on at manifest, manifest up
  saved at {'step': 'ramp', 'day': 0}, loaded at step ramp on Day 0, manifest gone, name Sam
11. Reload mid-walk: follow Torres to the lift (or the wing), save and reload short of it, then on to your bunk
  saved at step wing (Day 0, Sunday 17:48); after the reload: step wing, Deck 5, Torres 2 tiles away (lead)
  on to the bunk after the reload: reached True, missed [], device True
10. Monday in the real game: the three jobs held at 05:00, the briefing at 07:50, the shadow shift with Torres
  New game again: the evening's state before {'calder': None, 'tour': 1}, after {'calder': False, 'tour': 0, 'step': True, 'meet': 0}
  held for you: ['4-junction-1', '4-washer-1', '4-junction-2']
  07:50 in the Works bay: introBriefing
  its speakers: {'lines': ['calder', 'calder', 'calder', 'tech1', 'tech2', 'calder', 'torres-zeke', 'calder', 'torres-zeke', 'calder', 'calder', 'calder', 'tech2', 'calder', 'calder', 'calder', 'calder', 'calder'], 'cal': 'Works bay'}
  the briefing at a reader's pace: 19 lines, 20 taps, 07:58 to 08:36; Torres on the shadow shift from after it
  took it: True; Torres follow, 2 tiles from you; turned in: True; 'Shadow a job' ticked: True; d1-shadow note: True
  the health check missed on Tuesday: {'appts': [['14:00', 1, 'missed', 'checkup'], ['14:00', 2, 'yes', 'checkup']], 'again': True, 'mail': True}
  Pell's Wednesday ask (you were away): {'done': False, 'mail': 'Quiz tomorrow', 'seek': -1}
12. The week in the real game: each beat's teacher says their lines in its room in its window (the writers' beat.<id>.<n>); Tomas comes to Sowing
  d1-wash (Day 1, Monday 06:01, plan [4, 'intro', None]): heard 4/4
  d1-dinner (Day 1, Monday 18:01, plan [3, 'intro', '3-grab-1']): heard 5/5
  d2-booths (Day 2, Tuesday 18:01, plan [3, 'intro', '3-bench-17']): heard 4/4
  d3-pick (Day 3, Wednesday 08:01, plan [5, 'intro', '5-stool-1']): heard 5/5
  d3-store (Day 3, Wednesday 16:31, plan [3, 'intro', '3-shop-1']): heard 5/5
  d4-quiz (Day 4, Thursday 20:01, plan [3, 'intro', '3-bow-lounge-crowd-1']): heard 5/5
  d5-invite (Day 5, Friday 18:01, plan [2, 'commute', None]): heard 4/4
  d6-sowing (Day 6, Saturday 11:46, plan [3, 'intro', '3-crates-1']): heard 5/5
  Sowing: Tomas brought to the garden {'sow': True, 'at': '3-tend-3'}
OK
```
