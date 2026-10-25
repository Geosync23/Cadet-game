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

## ~01:10 UTC
- **8c crewDetail line (80dff612): PASS.** Off: cadet_test vs 0.92.4 ALL IDENTICAL; day 7 off OK; day 7 on OK; plant r_swap
  (line reverted) day 7 on FAIL (pell 0.77 hop, 08:21 3-mess-31).
- food_check 7 'garden, good' FAIL is OLD: same numbers on ba836359 and 80dff612 (told lead 35).
- weekend_check (fixed f-string, local): Sunday story FAILs on the fix: the check put you in the corridor (Holt not yet
  settled at 22:18) AND Holt settles ~22:27, so the chapter's line 0 is never read (index by clock). To DS1. FX9 says it
  fixed the check (room tile + host lines + >=5) but its push isn't on origin (DS1's e462655f is the tip): asked FX9.
- Plants with the fixed check: q_tobed -> sunday-story join FAIL (ok). q_chap, q_seat: not judgeable until the story
  lines pass on the fix. Rerun on the next sha.
- Lead 35's rule for the old traditions (same days/times/places/hosts; lose <= 2; not below minimum): my script
  plans/rv14-old_trads.py (c5ea9ebf). 80dff612 on: 5 FAILs (rec-wso -5/-3/-3/-6 Days 14/21/42/49; lineCeremony -4 Day 7).
  Off: OK, 0 shifts. DS1 to fold it into weekend_check.
- User (00:40): a 4-week rotation (W1 run/bread, W2 song/Gerald, W3 picnic/jigsaw, W4 cocoa/story); ships switched ON.
- eebed514 (game = e462655f, 80a82f67...): weekend_check OK. Plants: s_host (weekendTag clause) -> picnic host FAIL;
  s_tobed -> >=5 lines + Holt FAIL; s_chap -> Day 14 chapter FAIL; s_seat (seat-first off) -> NOT caught (asked DS1 for a
  line). Chapter line 0 point still open (DS1).

## ~01:55 UTC: 3e323170 (game 23eb60a5...): PASS for its stage (DS1 turn 1 + rotation; switch still off)
- Off: cadet_test vs FX12's 91b97ee9 (84ece11c...) ALL IDENTICAL. On: weekend_check OK (old-trads rule folded in, hosts,
  >=5, story read in full from line 1), events_check OK, day_check 7 OK.
- rv14-old_trads.py same build off vs on, Days 1-84: OK, 5 one-person shifts. vs 0.92.4: 71 "differ" = FX12's late piano and
  birthdays (intended) + Day 62 observatory-night -4 (with FX12, also with the switch off; flagged to lead 35).
- Rotation code all gated (evNewWk 0 when off). sundayStoryTick: SUN_GO starts the chapter at line 0 once Holt settled.
- Builders: DS1 handed over -> FX16 (session_01MbKpntrDkcWAKrTj1HRUMm): seat line, T5, T6, switch-on.
- 3b6e48bb (game 44d07c49..., FX16 T5 + DS1 seats; switch off): weekend_check OK; plant u_seat (tradSpot seat=false) FAILs
  all five q_seat rule lines. Decor cocoaPot/picnicBasket read OK. Perf noted (Bread day js 2.79 ms within Sunday dinner peak).

## ~04:30 UTC: FINAL, item 16 switched ON: PASS at 3307ded5 (game 49ba25a4...; = c7982f2c + one decor tap text)
- cadet_test vs 0.92.4: ALL IDENTICAL (c7982f2c and 3307ded5). weekend, events, food 1 7, day 6/7/14/28, deck OK (c7982f2c);
  join OK alone on 3307ded5 (two earlier runs timed out at the save-reload goto under load; load/skip times equal to 0.92.4);
  check_fast OK 234 s (3307ded5). old_trads shipped vs WEEKEND_ON=false copy, Days 1-84: OK, 5 one-person shifts.
- perf weekend scenes vs 0.92.4: 7 PROBLEM flags, all from more people (jigsaw 119->174 calls, story 200->235, Bread day
  landscape js 1.36->2.39 ms); under budget 450 (max 342). Told BM16 to record them as expected for CR2.
- Verdicts sent to lead 35, BM16, FX16.
