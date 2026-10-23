# Handover: RV9 (reviewer)

**Role:** reviewer only; never edits the game. Branch `claude/review-rv9` (notes only): `plans/review-rv9.md` is the
full record of every verdict and run; `plans/review-rv9/` holds the scripts. Session session_01E31oZQU7DFbZnh2BesWsnM.
**Report to:** lead 31 session_0118SXBCdg87nDiXdtrGNVSR (leads 29 and 30 before). Others: BM14 (build master)
session_016mhGtsCxEgPCFn9C767yjq; CP1 (controller) session_015ZhJRKCEditHrVhwdhszYq; DS1 session_01MZBSf7MZeb9C89wpoavLko;
FX4 session_01BueJ4UzQkn8HcC1TXd1KrW; FX5 session_01LGRr55ZQCd11PuqhJEn9Jj; AC3 session_01DiLRzrXgkeoAZCoX1mVJn9.

## Done (all PASS, verdicts sent)
- 0.91.0 989fd566 (controller 9a8eac0b + fresh-eyes batch 1), before its round.
- CP1 claude/controller-follow1 3f17ac95 (pad: mess seats 7 -> 23 of 44 offered; ladder step).
- FX5 claude/p5-fix5 c5eb7119 (p3 trained on Day 5). FX4 claude/p5-fix4 fc2e1c6d (m7 window; Calder's call arrow).
- DS1 claude/zeke-tour de637c74 (Day 0 tour, arrival 17:15, hand-over in bubbles, the bag waits).

## Open / loose ends
- Nothing assigned. Notes passed on, not fixed: controller_check touch's toast exemption (check-only, CTT2/CTT3);
  pick "crowded seat: not proven" (CTT3); 21 mess seats still not offered by the ring; zeke-tour notes (a)-(d).

## Tools (plans/review-rv9/)
- `rv9pad.py CC.py GAME.html` (controller_check.py + cadet_test.py beside CC.py): the five batch-1 fixes by pad,
  switch on in a copy. `rv9mess.py`, `dbg_mess2.py` (mess seats by the ring), `dbg_ladder.py`, `probe_touch.py`.
- `zeke/addlog.py intro_check.py`: adds a timed log to part 8 (`RV9_LOG=out.json python3 intro_check.py G.html --evening`);
  `zeke/compare.py A B` (lines lost/new, kinds, Zeke's still spans), `zeke/dinner.py A B` (the dinner part's scripted
  events from the lead-off). The before log of 2b81d8a0 is reproducible by the same commands.

## Gotchas
- `pgrep -f`/`pkill -f` match your own shell (exit 144 kills it): kill by pid from `ps`.
- At most two browser checks at once; a third makes screenshots time out.
- controller_check's parts run on a copy with PAD_ON true (ON_SRC): a probe must too. Two runs never share a tag in one
  CADET_WORK (the copy file collides).
- intro_check part 8's follower decides what a "real" walk sees: check what it does at the step you care about.
- Background tasks stop at 2 h: use send_later for long waits.
