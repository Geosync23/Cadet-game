# Handover: FX9 (the weekend traditions and item 19, after FX14 and FX11; 0.92.5 item 16) → next builder (lead 35 plans DS1)

**Role:** builder under lead 35 (session_01VQkkt8RXcvvGs1Dmzn2emM). Reviewer RV14 (session_01RwUYVcYt2PP7B7g3ogduFZ),
build master BM16 (session_01MB7n4yvCAeGyWN4WZCAGPh), words SW1 (session_01Mjn7ezXqrDgXBrdCtddHHJ), voice CS1
(session_01QcPAXHjQZ2HfZKMCTbaW9v), FX12 (session_01DfkfrfvdT2bW2Q1Y7b2AA5: late piano's to-bed rule, the birthday hour).
Read first: plans/handover-fx14.md (how traditions, joins, places and the switch work), then plans/handover-fx11.md, then this.

## Branch and builds

**claude/p925-weekend**, tip **9f02a5ef** (pushed; check_fast OK). From integration ba836359 (0.92.4). Everything weekend is
behind `WEEKEND_ON` (section 13; a URL flag `?weekend`, off in the game): switch off = 0.92.4 plus item 19.
RV14 has the list of commits since f18d18d5 (my message of ~00:00 UTC 2026-10-25). Earlier pieces of mine on other branches,
all passed: claude/p923-fx9 (needs pace), claude/p925-fx9 (go-walk), claude/p925-fx9b (piano/lounge), claude/p925-fx9c (lift flash).

## Done (since FX11's 357ff7ac)

- **Item 19, Cook-along in the galley** (344c0dd5, NOT behind the switch; its own commit): 3-cookalong-1..6 (ids kept) on free galley
  tiles round the prep island (K: 36,6 37,7 39,7 39,6 36,3 40,6; each over .75 m from any 3-galley-* standing point; 6039daa2 moved
  #3 off 38,7, RV14's finding), anim cook; cook-along.trad `where: 3 pool @cook-along`, anim cook; "in the galley" words (SW1 OK).
  events_check part 13: everyone at it in room K, cooking; and nobody at a 3-cookalong place within .45 m of a cook (Saturday,
  and Bread day with the switch on). Fails on 0.92.4 / f18d18d5, passes now. Needs evTagId's 'cook' (bbcea5cb) if cherry-picked.
- **Bread day** uses Cook-along's six spots (`where: 3 pool @cook-along`); its own 3-bread-* are gone (one sat on 3-galley-4).
  Leaves out Nandakumar (`nandakumar 0%` first: she hosts the rec deck's Sunday 08:00 slow stretch and missed it).
- **Hosts:** Every song 17:15-18:05 (Zeke works to 17:00); the big jigsaw's host Dev Raman (Vance works Sundays; Vance drops in);
  Night owls' cocoa host Kofi Mensah (Keane, bed 22:46, stays a regular): all lead 34's calls, SW1's words, CS1 PASS.
  A weekend tradition's host stays to its end (section 14 leisureUntil, `weekendTag(tag)` beside the switch): Cruz hosts her picnic.
- **Attendance:** `tradToBed(p, d, e)` (section 18, above evArrive) for traditions with `toBed`: someone whose bedtime falls inside
  it comes from the start and leaves 20 min before bed, if that's at least n minutes (n = the number, or the tradition's min when
  `toBed === true`, FX12's `to-bed: yes`). Hooks in evArrive and eventPlan. Set to 20 for night-owls-cocoa and sunday-story in the
  weekend block. Days 6-28: cocoa 7/6/10 (was 3/1/2), story 7/9/9/3 (was 2/3/4/2). FX12 agreed: whoever merges second drops their
  own two inline hooks.
- **The Sunday story:** `sundayStoryTick()` (weekend slot, called from eventsTick when on): Holt says chapter
  story.sunday.(((week-1) mod chapters)+1) line by line in his bubble while you're in its room (as the Friday address).
- **Seated weekend joins take a seat first** (tradSpot, switch-gated: the Sunday story had put you at the kettle).
- events_check: tagId knows 'cook'; the weekend .trad files aren't expected loaded with the switch off.
- weekend_check: Bread day sampled at ~07:16; the Sunday story part (Holt reads chapter 1 on Day 7, 2 on Day 14). Not yet run
  in full on the tip (an earlier run had only the then-known attendance FAILs and a too-early Bread day sample).

## Results (switch on unless said)

events_check OFF: OK. events_check ON (before 78912de3): only rec-slow-stretch losing Nandakumar (fixed, rerun pending).
deck_check ON: OK. RV14: deck, join, food 1 7 ON OK; weekend_check's planted faults caught.
**Open:**
1. **day_check 7 ON, pell hopping .77 tiles at 08:21: FIXED** (root cause, not weekend code): section 8c's crewDetail swaps a story
   crew member between the full body and the crowd body, and set the new body at a.x/a.z without the get-up glide (hx/hz) and the
   lane (lx/lz); at 08:21:00 Pell's swap fell on the step she got up, so she was drawn .63 ahead for a frame. Now set at
   x + lx + hx, z + lz + hz like every other set. day_check 7 ON OK (biggest get-up move .19). Section 8c's owner should review it.
2. **food_check 7 'garden, good' fails with the switch OFF too** (same numbers): it's the Day 7 + 7 days window, not the weekend's;
   the round runs food_check 1 7, which passes. Not ours; backlog row if anyone wants it.
3. RV14 (a): at Bread day join_check says the marker is on the leader (Uma Vasquez) but the arrow says "Tap Chef Brennan". In the game
   both read TJ_NOW (host Brennan when she's within 6 m of the spots): check what join_check reads (tradLeader vs TJ_NOW).
4. RV14 (c): Every song is capped by the music room's 6 places; add two standing `music`-type places in room n of Deck 4 behind the switch.

## Left (T5, T6)

- **T5:** decor on the days (each tradition's ties.decor where it fits), head counts per deck at each (the user's "deck head counts"),
  perf numbers (perf_check on Deck 3 Sunday morning, the rec deck, Deck 1 jigsaw).
- **T6:** the birthday hour with FX12 (no birthday within an hour of any tradition: FX12's scheduler rule); design-doc: the eight
  weekend traditions (times/hosts above), Mend-it morning parked as cut (the user's NO, 2026-10-24: keep on record), Cook-along in the
  galley; DEV_NOTES; build-table rows (only cook-galley's is in); the full round with the switch on in a copy.

## How to test

- Setup: pip install playwright numpy pillow; three r128 and acorn@8.12.1 into /tmp/cadet-work (testing-guide 2.0);
  CADET_CHROME=/opt/pw-browsers/chromium. Never more than two browser checks at once here (they time out).
- Switch on in a copy: `sed "s/^const WEEKEND_ON = URL_FLAGS.has('weekend')/const WEEKEND_ON = true/" starship-cadet.html > on.html`.
- `python3 weekend_check.py starship-cadet.html` (it switches on itself, ~10 min). events_check on both the file and the on-copy.
- `python3 content_gen.py starship-cadet.html` after any .trad/.lines change (check_fast checks it's baked).
- After a change the planner reads: `SCHED_DATA = null; SHIP_DAYS.clear(); EV_DAYS.clear()`.
- Gotcha: `eventsOn(d)` gives from/to as minutes of the day, not absolute.
- Gotcha: a waiting loop `until ! pgrep -f X` matches its own command line; wait on an output line instead.

## Open questions for the user

None new. (The jigsaw filling week by week, the Gerald as a keepsake, more Sunday story chapters: ask before building.)
