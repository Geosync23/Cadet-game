# Handover: RV29 (second reviewer, patch 0.99.5; lead 47)

Session session_014zyJYM3D7UBkZN49CsZVuA. Lead 47 session_014zyJYM4mt9ZDCD5H9JZDtN. Build master BM22
session_014zyJYNgBPdEPHLxTGrM889. Branch claude/review-rv29: notes only (plans/review-rv29.md, probes in plans/rv29-probes/).

## State (2026-10-31 ~12:55 UTC): queue empty, all PASS, sent to builders, lead and BM22
- JB2 claude/p995-jobs 1e056bd (game ef0941da...7d04): re-review of RV28's FIXES NEEDED (W1 words baked, F1 scanner's first
  job rotates over Tier 2 pump machines held for you, J1 the tour's own lines). PASS.
- PL2 claude/p995-player 6b2f135 (game e462d177...bf80b): notes 3, 12, 13. PASS. Lead told: Stop partway pays its share of
  the real talk length (was a flat share of 15).
- CT5 claude/p995-controller 7c6c2477 (game 5fae9bbf...f0cd): notes 2, 5, 6. PASS.

- TB4 claude/p995-trad926 bd0fa61 (game 347b4996...d2e9, TB4 + SW4's words): the 0.92.6 traditions' Tap to join. PASS
  (~14:10 UTC). Non-blocking note: a tap in the last ~7 min runs the card past the end (as the 0.93.2 joins).

## Probes (plans/rv29-probes; the Dev ones exec the worktree's devmode_check.py harness, the paper ones cadet_test's Game)
- tour_play.py WT BUILD OUT: Day 2 Dev jump, Zeke's rounds talk, the first round taken, every stop walked and its card
  pressed, save + reload after stop 2, turn in; logs Zeke's lines, toasts, tips, cards.
- rv28/jb_scan.py, scan_take.py: the scanner's first job (which machine by day; on your board, takeable, minutes).
- door_sweep.py WT BUILD: every locked door side on Decks 1, 2, 4, 5, 6 x Doors settings: path through, slides open,
  edgeBlocks, lockedBehind of both sides (PL2's function; null on older builds).
- crew_doors.py WT BUILD: crew rooms each minute + locked doors drawn open, a hash to compare builds.
- talk_play.py WT BUILD N: real-game Talk a while (stands you next to a seated person), meter, lines, rewards.
- seat_sweep.py WT BUILD, seat_shot.py WT BUILD OUT: the seat button by every public seat; a real click.
- t926_pace.py WT BUILD_ON [ids]: TB4's traditions at a reader's pace (A), a late tap (B), reload on card 2 (C); uses TB4's
  plans/tb4-probes/t926_probe.py helpers. LOOK's m is the minute of the day. overlap73.py WT BUILD [DAY MIN]: joinables on now.
- seat_talk_pad.py BUILD WT: controller, seated, D-pad right through the ring, A on the 2nd and 3rd person.

## Gotchas
- pip install playwright; three r128 + acorn 8.12.1 in /tmp/cw-w1, /tmp/cw-w2; CADET_CHROME=/opt/pw-browsers/chromium.
- Never `pkill -f` a name in your own command line (it killed my shell, as RV26 warned).
- Probe toasts: the harness's real clock is frozen, so a second toast waits behind the first (looks like a stale card).
- PLACE_OF holds the current deck only; DECKS[n].places has every place with its room.
- check_fast uses two browsers: run nothing else beside it.

## Open questions for the user
None from me.
