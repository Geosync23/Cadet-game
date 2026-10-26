# Handover: DS1 (the weekend traditions, 0.92.5 items 16 + 19, after FX9) → next builder

**Role:** builder under lead 35 (session_01VQkkt8RXcvvGs1Dmzn2emM). Reviewer RV14 (session_01RwUYVcYt2PP7B7g3ogduFZ),
build master BM16 (session_01MB7n4yvCAeGyWN4WZCAGPh), words SW1 (session_01Mjn7ezXqrDgXBrdCtddHHJ), voice CS1
(session_01QcPAXHjQZ2HfZKMCTbaW9v). Read first: plans/handover-fx14.md, plans/handover-fx11.md, plans/handover-fx9.md, then this.

## Branch and builds

**claude/p925-weekend**, tip **b413cde7** (pushed; check_fast OK). From integration ba836359 (0.92.4) + FX12's claude/p925-fx12
91b97ee9 (late piano, birthdays) merged + SW1's final words (claude/weekend-words-sw1 8d2e66b0) baked. Everything weekend is
behind `WEEKEND_ON` (section 13); **the user (00:30 UTC 2026-10-25): 0.92.5 ships with it ON** (no preview): the last turn
flips `const WEEKEND_ON = URL_FLAGS.has('weekend')` to `true`, with design-doc/DEV_NOTES saying so, and the checks then run on
the shipped file; cadet_test vs 0.92.4 will differ on weekend days (say which differences are expected).

## Done in my turns (all behind the switch unless said)

- **FX12 merge:** one toBed hook in evArrive at FX12's place, calling FX9's `tradToBed` (so `toBed: 20` on cocoa/story holds;
  FX12's late piano `to-bed: yes` reads as its min); FX12's eventPlan clamp; events_check part 13 = Cook-along (FX9), 14 = FX12.
- **The 4-week rotation** (the user 2026-10-25: "spread the new ones across weeks, and keep some that were already there";
  lead 35's table): the eight `.trad` files `when: every 4 weeks <day> week N from day 1`: wk1 Saturday run / Bread day,
  wk2 Every song / Gerald clinic, wk3 Garden picnic / big jigsaw, wk4 Night owls' cocoa / Sunday story (old `when` kept in a
  comment line above).
- **New ones always give way** (section 18): `evNewWk(e)`; evBudget sorts them last (it kept the rarer one before); evBdaySlot
  places a birthday ignoring them and drops a new one within its hour; `evOldGoer(p, d, e)` in evArrive: a new one never draws
  someone an overlapping old tradition would have (lead 35's rule: an old one loses at most 2 people).
- **Sunday story** 22:15 → 21:15-21:55 (Holt, its host and reader, has a Sunday bedtime 22:24-23:08); SW1 re-voiced. The
  chapter (`sundayChapter`) advances a showing (28 days), and `sundayStoryTick` starts it from line 0 once Holt is settled in
  the room (`SUN_GO`), every line in order (RV14).
- **Every song:** two standing places 4-song-1/2 by the piano (type event, tagged every-song only; RV14's (c)).
- **join_check:** reports TJ_NOW's leader (the game's marker and arrow both read TJ_NOW; RV14's (a) was the check printing
  the planner's tradLeader); fails unless marker, arrow and its words name the same person.
- **weekend_check** (switch on in a copy; the same build switched off is the base): rotation days; old traditions' days, times,
  places, hosts identical Days 1-56 (RV14's old_trads folded in), none loses > 2, none under its own fewest; each weekend day
  only its own new one (gave-way days printed: Day 13 storm, Day 41 Every song for a birthday); hosts at it (or at work in its
  room: Brennan) Days 6-84; >= 5 at every cocoa/story; the story read in full on Days 28 and 56. WEEKEND CHECK OK.

- **Seats:** the Sunday story and the cocoa have `spare: 1` (a full common room had your join standing by the leader);
  weekend_check: your story join is on a sit place, and tradSpot from the kettle's spot still gives a seat (RV14's q_seat).
  Note: RV14's plant (seat-first off) is NOT caught in this setup (crew stand at the kettle then); outcome-only lines.
- **DV1's arrows_check fix** (claude/m6-day9 e823a74f, test only) merged: the week's Day 9 burst pipe.

## Results

On 3e323170: weekend_check OK; events_check OFF OK, ON OK; check_fast OK (202 s); cadet_test switch-off vs FX12's 91b97ee9 ALL
IDENTICAL. On b413cde7 (spare: 1 and the seat lines on top): weekend_check OK, check_fast OK (201 s); events_check and cadet_test
not rerun since (spare changes only the story/cocoa, both behind the switch).

## Left

1. (done) RV14's q_seat line. If RV14 wants its plant caught, free the kettle in the test first.
2. **T5:** decor on the days (Bread day and the jigsaw have theirs; consider small ones for the picnic, cocoa, Every song only
   if they fit; watch draw calls), head counts per deck at each (a printed table from the planner, Days 6-84), perf numbers
   (perf_check alone, `PERF_SCENES=regexp`: Deck 3 Sunday morning, the rec deck, Deck 1 jigsaw) vs 0.92.4.
3. **T6:** design-doc: the weekend traditions paragraph needs the rotation, the new times (story 21:15), hosts, "new ones give
   way", Cook-along in the galley, Mend-it morning parked as cut (the user's NO 2026-10-24; keep on record); DEV_NOTES entry;
   build-table rows (p925-weekend turn 1 + rotation; T5; T6); the switch flipped on; the full round on the shipped file
   (two browser checks at a time here); cadet_test vs 0.92.4 with the expected weekend-day differences named.
4. SW1's note: the pitch page and sunday-story.trad's header comment still say 22:15 "after his last round": update the
   trad comment when you touch it.

## Gotchas

- Never more than two browser checks at once here; check_fast alone counts as several.
- After a change the planner reads: `SCHED_DATA = null; SHIP_DAYS.clear(); EV_DAYS.clear()`.
- A Python check's evaluate that spans lines must be a triple-quoted f-string; double `{{ }}` inside f-strings.
- The ship clock only runs forward (skipTo to an earlier day does nothing): order a check's parts by day.
- PLACE_OF holds only the current deck's places: look a place up in `DECKS[n].places` for other decks.

## Open questions for the user

None new.
