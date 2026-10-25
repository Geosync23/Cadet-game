# Handover: FX16 (the weekend traditions' last turns, 0.92.5 item 16, after DS1) → next builder

**Role:** builder under lead 35 (session_01VQkkt8RXcvvGs1Dmzn2emM). Reviewer RV14 (session_01RwUYVcYt2PP7B7g3ogduFZ),
build master BM16 (session_01MB7n4yvCAeGyWN4WZCAGPh), words SW1 (session_01Mjn7ezXqrDgXBrdCtddHHJ), voice CS1
(session_01QcPAXHjQZ2HfZKMCTbaW9v). Read first: plans/handover-ds1.md (and through it fx9, fx14, fx11), then this.

## Branch and builds

**claude/p925-weekend**, tip **3307ded** (pushed; check_fast OK). Game sha256 49ba25a4... (see the build-table T6 row).
- 9a249f75 T5 (decor, weekend_check lines, perf scenes, records); 3b6e48bb merge of DS1's b413cde7 (`spare: 1` on the story
  and cocoa: a seat kept for you) and DV1's arrows_check fix; c7982f2b **WEEKEND_ON = true for good** (the user, 2026-10-25).

## Built

- **Decor:** `cocoaPot` (bow lounge coffee table, L 8.4,11, top .405; +2 draw calls) and `picnicBasket` (grass by the pond's west
  bench, G 1.7,12.25; +3), in the weekend block's DECK_DRESS, `ties: decor` in the two .trad files. Every song: none.
- **weekend_check:** RV14's q_seat (a seated join seats you when a seat is free; the full-room fallback is printed; and the
  seat-first rule with every place freed: crew goalIds cleared and BUSY emptied for one tradSpot call, put back). A planted
  fault (`seat = false` in tradSpot) fails all five rule lines. Decor only in its window; birthdays (Days 1-364, none within
  EV_BDAY.gap of a weekend one); the deck head-count table (planner slot's `deck`; last column = 'away' guests/rotation crew
  or the lift). It now takes the shipped build (WEEKEND_ON = true) and makes a false copy as the base.
- **perf_check:** six `weekend:` scenes, no `needs` (0.92.4 measures the same room). In the round via CR2's perf run.
- **Records:** design-doc (the eight, rotation, times/hosts, old ones first, new give way, Cook-along in the galley, Mend-it
  morning cut, on from 0.92.5), DEV_NOTES "The weekend traditions", build-table rows (DS1's turn 1 + rotation, T5, T6),
  testing guide (weekend_check row, CR3's share), tools/affected.py (CHECKS 'weekend', section 18's rule).

## Loose ends

1. (done) RV14 FINAL PASS at 3307ded5 (2026-10-25 ~04:20 UTC), Bread day's js accepted (RV14, lead 35). Waits on the full round, then BM16's merge.
2. (done) The decor tap texts: cocoa as written, the picnic basket's final words in 3307ded (SW1, CS1 PASS).
3. The full six-runner round on the shipped build: the lead calls it.
4. (done by SW1) The pitch page has a "Since your answers" box (claude/weekend-pitch cbaac1db).
5. **Every song, Day 69:** the music room was full (six seats and both standing places by the piano taken), so joining stood you
   beside the leader with the game's own words ("Every spot's taken just now..."). The picnic on Day 20 did the same (garden benches
   full). weekend_check prints these, not fails. If the user wants a seat always there, add `spare: 1` to every-song.trad and
   garden-picnic.trad as DS1 did for the story and the cocoa (garden: the user's no-new-meal-seats rule, so only an existing bench).

## How to test

- Setup: `pip install playwright numpy pillow`; three r128 and acorn 8.12.1 into /tmp/cadet-work (testing guide 2.0);
  `CADET_CHROME=/opt/pw-browsers/chromium`; each parallel run its own CADET_WORK.
- `python3 weekend_check.py starship-cadet.html` (~12 min; WEEKEND CHECK OK). Also on the shipped file: events_check, join_check,
  day_check 6 and 7, food_check 1 7, check_fast. Perf: `PERF_SCENES=weekend python3 perf_check.py NEW OLD`, run alone.
- Proving the seat line: copy with tradSpot's `seat = !stand && WEEKEND_ON && WEEKEND_TRADS.has(e.id)` made `seat = false`:
  weekend_check must FAIL the five "RV14's q_seat" lines.
- After a .trad edit: `python3 content_gen.py starship-cadet.html`.

## Gotchas

- Two browser checks at a time at most; check_fast alone. Make log folders before starting background checks that write there.
- `heldBy` is a const: to free places in a check, clear crew `goalId`s and restore them.
- The planner's 'away' slots are guests and rotation crew not aboard (deck 0).

## Open questions for the user

None new.
