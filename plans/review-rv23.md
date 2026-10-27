# Review log: RV23 (reviewer, from RV22), 2026-10-27

Lead: lead 41 (session_01GKuymjWR1dqfbCw1MyEP9j). Notes-only branch `claude/review-rv23`. Probes: `plans/rv23-shots/`.

## Verdicts
| Branch | Verdict | Sha |
|---|---|---|
| claude/vessel (VB1): RV22's must (round-one fetch) + 2 shoulds | PASS | 03b63d95 (game 705c6fc5) |
| claude/talk-close (B3): talk only up close | PASS (1 should) | f52e2abc |
| claude/p5s6-core (W6): Step 6 first turn, all off | PASS (1 note) | 95ef6947 (game 7c13cfe7) |
| claude/talk-close-fix (W6): the far card closes | PASS | 6dfc4ec1 (game ea9e0f3c) |
| claude/vessel-words (W6): 4 lines cut to 90 chars | PASS | 0f8a2406 (game afde419d) |
| claude/check-offcopies (test only) | code read OK, not run | 00161062 |
| claude/p5s6-mech-a (MA6): M21 the Monday briefing | PASS | 27166be |
| claude/p5s6-puzzles (PZ6): S6-8 P6-P8 | PASS | fd1f27f (= aed3f73, e16be28) |
| claude/p5s6-nights (N6): S6-1 turns 1-3 | FIXES NEEDED (1 must: Calder not in person Day 22; 1 should: 2.2 m reach) | c806c78 |
| claude/p5s6-promo4 (W6/W7): S6-3 turns 1-4b | FIXES NEEDED (must: Calder stuck in the lift car, no offer in person) | 9ac35bfd |
| claude/p5s6-deck (DA6): S6-4 Deck 6 kit | PASS | 469b606b |
| claude/p5s6-mech-a (MA6): M24 leading a team | PASS | 8f943e82 |
| VB2's ending leftovers (arrows endgo teachoff, track) | PASS | staging-0.94.0 d69473b7 |

## VB1 03b63d95
- cadet_test 0340b6f9 vs 03b63d95 (off): ALL IDENTICAL.
- events_check: only known-old FX24-2. Its new fetch cases: Calder 11:30 speaks, sheet scene at 2.8 m; Taavek 12:33 speaks, round-one scene at 4 m.
- arrows_check vessel (ON copy) OK; day_check 28 (ON copy) OK.
- Phone play 390x844 (vb1_play.py, the fetch now from 12:20): Calder's Saturday fetches speak (10:14, 11:44) and open the sheet scene;
  Sunday 12:20-12:29 the arrow is "Join Taavek at the bench"; Taavek sets off 12:30, reaches the bow lounge 12:43, speaks, scene at
  5.4 m (12 panels); chain arrow after. Monday goodbye as before.
- Optional (RV22's): VESSEL_FETCH isn't saved (reload mid-fetch: 3.2 m reach, Taavek back to their plan; the arrow still leads to them).

## B3 talk-close f52e2abc (base ac810e7e)
- cadet_test ac810e7e vs f52e2abc ALL IDENTICAL; interactions OK; player_check OK; arrows week guide OK; controller pick, day OK;
  promo3 OK alone (a first run beside two browsers failed: the ring on the notice board; the base and a rerun pass).
- controller ending: 4 FAILs, the same on the base ac810e7e (old, not this branch).
- Phone probe (talk_play.py): far tap: card with what they're doing and Walk over only; Walk over walks you to 2.46 m and the full card
  opens; near tap: full card at once; the "would like a word" chip from 5 m: far card, walk, full card with their line. No page errors.
- should: a far card nobody acts on never closes (no walk-off distance in far mode) and holds back seeks, visits and chatter while open;
  the person wandering within 2.5 m then opens the full card unasked (seen in the probe).

## W6 p5s6-core 95ef6947 (base 07e033c9)
- cadet_test ALL IDENTICAL; names_check OK (build and a Step 5+6 ON copy); day_check 26 ON copy OK.
- Code read: switches behind P5_STEP6; holds inside Step 5's block; section 28 consts read only at run time; ladder rows at the end and
  inert (the offer needs WORK_MECH[id]).
- note: devmodeNextTraining and Dev mode's career list don't check WORK_MECH (Step 6 on before its pieces: Dev mode could offer m22).

## VB2 ending-checks leftovers, on staging-0.94.0 d69473b7 (everything ON; lead 41 asked for the switched-on build): PASS
- arrows_check endgo teachoff OK, endgo track OK (staging's arrows_check, newer than 0a2993cc): Go Day 34, settled Day 35, ended Day 36;
  every ending arrow led, 475 minutes due, 0 missed. day_check 31-36 left to BM19's gate (lead 41).
- "stuck" = arrows outside the ending the follower couldn't act on: "Clock in: shift at 09:00" from Day 32 16:03 (both); track also
  "air plant, Deck 5" from Day 31 08:01. Not blocking.

## BM19's events_check fix c03d51da (staging, test-only; glance on lead 41's word)
- Read: accepts 'crossingBack' as the event left at Day 31 00:00, and __vfresh logs only calendar rows before the vessel. Looks right;
  no reply sent (BM19: reply only on a problem). Could be tighter (accept crossingBack only with the ending on), not needed.

## W6 talk-close-fix 6dfc4ec1 (game ea9e0f3c): PASS
- Far card closes 1.5 m further off than it opened or after TALK_FAR_STAY (6 ship min) unless Walk over; full card only after Walk over.
  talk_play.py on it alone (Walk over clicked with force=True): all cases as before; no full card unasked. W6: cadet identical, player,
  controller pick/day, check_fast OK.

## W6 vessel-words 0f8a2406: PASS
- The 4 lines keep meaning and voice; content_gen --check up to date; lines_check PASS (0 errors). Live 390x844 on the build (all ON;
  vw_play.py, VW_ONLY=shelf for the shelf part alone): signed toast by a real sheet tap, round-one missed 13:00, home missed 15:30, all
  2 lines. Shelf line fires at 12:00 but a jump-fired Zeke notice replaced it in the probe; my tap on the shelf sketch didn't land.
- Side note: the 12:00 heads-up reads "Put Taavek's sketch on your shelf is starting" (wording for an event, not a to-do).

## check-offcopies 00161062 (test only): code read OK
- Off copies for events vessel-off and promo_beats t3off when the build ships on; mech ps stand-in first; arrows follower closes a device
  a nearby tap opened. Not run.

## Next
- Lead 41 (10:25): 0.94.0 published; I'm Step 6's reviewer. Wave 1 on claude/staging-p5s6 64e296df: W6 S6-3 day parts, N6 S6-1 nights
  (session_01GKuymnDA25R2a5yZGYpaBS), MA6 S6-2 briefing (session_01GKuymj1UEDuEYMnG9rmFkc), PZ6 S6-8 cases (session_01GKuymjrmdGE4vaHHHGkvYF).
  Verdicts to lead 41 + the builder; OFF identical vs 64e296df; base worktree /tmp/rv23/wt-64e296df.

## Step 6 wave 1 (base 64e296df)
- MA6 27166be: PASS. cadet identical; mech_check m21 OK; controller m21 OK (arrow "Your seat at the table" at 08:25, briefing by pad);
  the seated briefing at 390x844 (controller's shot). Merge note: W6 bfcebb6d also edits the Step 6 ladder rows (t4 before m21).
- In progress: W6 promo4 bfcebb6d (turn 1 d40a95ee: cadet identical; p4_play.py live offer probe queued), N6 nights 157fe11 (9e176f6
  cadet identical; 157fe11 cadet identical; day_check 23 + player_check ON running), PZ6 puzzles fd1f27f (3046fb5 cadet identical,
  puzzle p6 OK; fd1f27f cadet + p6 p7 p8 queued).
- To raise: N6's isWorkDay reads P5_LEAVE (section 28, later in the file) inside try: if the planner runs at load before that line,
  Navarro's leave is missed there and seen later (ON only; day_check's "same day twice" should show it). W6: no controller part for t4.
- PZ6 fd1f27f: PASS. cadet identical (3046fb5, fd1f27f); puzzle_check p6 p7 p8 OK; controller s6cases OK (aed3f73).
- N6 c806c78: FIXES NEEDED. cadet identical (9e176f6, 157fe11, c806c78); day_check 23 + player_check ON OK (157fe11); n6_play.py:
  notice 22:40, arrows clock in / engine room / clock out OK. MUST: Day 22 Calder stood 22.7 m off 09:16-09:58, never came; notice at
  10:00. should: p5nNear 2.2 m (use a looser reach while fetching).
- Queued: W7 promo4 (latest 9ac35bfd; p4_play on a1ea8034; cadet 76e59409, 9ac35bfd; clothes_check), DA6 deck 469b606b (base
  3e502ca; d6_look.py), MA6 m24 8f943e82 (base 3e502ca).
- Shared cause (W7 offer, N6 night word): worksEscort's follow puts Calder in the lift car ('@') on your deck, esc "follow|42,17",
  path 0; she never walks out (p4_diag.py on a1ea8034 ON). crewComeTo (VB1's vessel) works across decks. Sent to lead 41, W7, N6.
- W7 9ac35bfd: cadet identical at every turn; MUST above; should: controller part for the Tier 4 test at the board.
- DA6 469b606b: PASS. cadet identical vs 3e502ca; d6_look.py: coil service spots reachable in E, 104-107 calls; kit tappable.
- MA6 8f943e82: PASS. cadet identical vs 3e502ca; mech_check m24 OK; controller m24 OK (pick, book, six calls by pad).
- Queued: DA6 dd32a9a7 (cadet vs 5dc0f13, controller deck6).
