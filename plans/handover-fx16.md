# Handover: FX16 (the weekend traditions' last turns, 0.92.5 item 16, after DS1) → next builder

**Role:** builder under lead 35 (session_01VQkkt8RXcvvGs1Dmzn2emM). Reviewer RV14 (session_01RwUYVcYt2PP7B7g3ogduFZ),
build master BM16 (session_01MB7n4yvCAeGyWN4WZCAGPh), words SW1 (session_01Mjn7ezXqrDgXBrdCtddHHJ), voice CS1
(session_01QcPAXHjQZ2HfZKMCTbaW9v). Read first: plans/handover-ds1.md (and through it fx9, fx14, fx11), then this.

## Branch and builds

**claude/p925-weekend**, tip **c7982f2b** (pushed; check_fast OK). Game sha256 39e8b873... (see the build-table T6 row).
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

1. RV14's verdict on c7982f2b (and on Bread day's js: 1.65 -> 2.79 ms portrait, 29 -> 33 people; Sunday dinner today is
   2.37-2.79 with 66). If asked to dig: profile the galley at Day 7 07:25 (cook anim near the cooks? the cook-along spots?).
2. SW1's words for the two decor tap texts (asked; stand-ins in the code). Put them in, CS1 checks.
3. The full six-runner round on the shipped build: the lead calls it.
4. The pitch page (claude/weekend-pitch) still says the story is 22:15: SW1's file.

## Gotchas

- Two browser checks at a time at most; check_fast alone. Make log folders before starting background checks that write there.
- `heldBy` is a const: to free places in a check, clear crew `goalId`s and restore them.
- The planner's 'away' slots are guests and rotation crew not aboard (deck 0).

## Open questions for the user

None new.
