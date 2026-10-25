# RV14 review log (reviewer under Lead 34; took over from RV13, 2026-10-24 ~22:45 UTC)

Scope: 0.92.5 item 16 (the weekend traditions, behind WEEKEND_ON) and item 19 (Cook-along in the galley, not behind
the switch), both on claude/p925-weekend. Builder FX9 (session_01WeXGZBS3DyyLqHGpRjWZzA); BM16; Lead 34.
Base: claude/integration ba836359 (0.92.4, game 2aa6427f...).

## 357ff7ac (game d2ca64c2...): T1-T4, tjActs, weekend_check
- cadet_test 0.92.4 vs 357ff7ac (off): ALL IDENTICAL.
- weekend_check: FAILED only on night-owls-cocoa and sunday-story ("nobody at it": bedtimes; the known attendance gap).
  Everything else ok (each on its day, off = none, joins/acts, tap-join gains, Bread day spots/decor/loaf, jigsaw).
- Words: the baked jigsaw chatter says "Vance ... in her head"; Vance is "he" everywhere else. SW1's df94ab2c (not yet
  merged) rewrites it. Every song's "Sing-along at five" needs a word if it moves to 17:15.
- Hosts: Vance (offDays Wed/Thu) works Sundays; Zeke works Saturdays; Tove Cruz off Sat/Sun (picnic host refused by take()).

## 344c0dd5 + 56293048 (game bcd972f9...): item 19 Cook-along in the galley
- events_check part 13 alone on 0.92.4: FAIL (all five in the mess, talk). Good line.
- cadet_test 0.92.4 vs tip (off): ALL IDENTICAL. content_gen --check, names_check (off and on): OK.
- Probe (/tmp/rv14/scripts/probe_k.py, switch on): Day 6 15:46 and 16:06 Sato at 3-cookalong-3 (38.35,6.9) and Madsen
  at 3-galley-6 (38.5,6.8, prep) 0.18 m apart. Bread-4 has the same point (Sunday samples clear, but galley-6 is a bake
  station). -> FIXES NEEDED (sent ~23:20 UTC): move off galley stations; add a no-overlap line to part 13.
- Depends on bbcea5cb's evTagId 'cook' (tag ev-cook-along-cook): not pickable alone (told BM16).

## Later finds (~23:10-23:45 UTC)
- Full events_check on the shipped tip (off, 56293048): FAILED. (1) events_check.py's own tagId lacks 'cook': Cook-along
  "never happened"/"not on" Days 6, 20, 27. (2) Since T1: with the switch off, the content/traditions vs loaded check
  flags the eight weekend files "not loaded" (16 FAILs). Sent to FX9/BM16/lead. Log /tmp/rv14/ev_tip.txt.
- f18d18d5 (game 483625fb...): Sunday story chapters (sundayStoryTick, story.sunday.<week mod 4 + 1>, friHere room),
  Every song 17:15, jigsaw host Raman (off Sat/Sun), SW1 df94ab2c merged.
  day_check on: Day 6 OK; Day 7 FAILED (pell hops 0.77 tiles getting up from 3-mess-31 at 08:21). Off f18 and 0.92.4:
  Day 7 OK -> weekend-caused; sent to FX9. food_check on (1 7): OK.
- Plants through weekend_check (357ff7ac): skip line removed -> "switch off" FAIL; loaf not noted -> both loaf lines FAIL;
  jigsaw mins ignored -> 20-minute lines FAIL; hobbyCount removed -> hobby line FAIL. RV13: second tjActs() removed -> FAIL.
- FX9's next sha promises: events_check fixes, cookalong-3 moved + no-overlap line, Bread day on Cook-along spots,
  host-stays rule (picnic), tradToBed attendance, Mensah hosts cocoa, SW1 c5f1fc7b/faac7054, Sunday story check, Day 7 fix.

## 2026-10-25 ~00:30 UTC
- **Item 19 PASS at 7ff6a818** (game e9118344...): off: cadet_test vs 0.92.4 ALL IDENTICAL, events_check OK (FX9's tagId
  'cook' + weekend-files skip), food 1 7 OK, day 6 OK, check_fast OK (235 s). Part 13: FAIL on 0.92.4, its overlap sweep
  FAIL on f18d18d5 (Sato/Madsen .18), OK on 7ff6a818 (on, incl. Bread day). Merge note: needs bbcea5cb's evTagId 'cook'.
- weekend_check.py at 7ff6a818/80dff612 does not start (f-string SyntaxError line ~101, 8cef93c7). Testing with a local
  fix in /tmp/rv14/chk. Told FX9, then DS1.
- 80dff612 (game d4f3bc0d...): section 8c crewDetail swap sets the body at x+lx+hx / z+lz+hz (FX9's root cause of Day 7
  pell 0.77 hop). Ungated, affects everyone; its owner idle -> I review it. Plant r_swap (line reverted) prepared.
- FX9 handed over; DS1 (session_01MZBSf7MZeb9C89wpoavLko) builds T5/T6, (a)/(c), the switch-on. Lead 35
  (session_01VQkkt8RXcvvGs1Dmzn2emM) replaces lead 34. USER (00:30): 0.92.5 ships the weekend SWITCHED ON: final verdict on
  the shipped switch-on file; cadet_test diffs vs 0.92.4 only the expected weekend ones.
- Asked for check lines: host at each weekend tradition; >=5 at cocoa/story.
