# Review log: RV23 (reviewer, from RV22), 2026-10-27

Lead: lead 41 (session_01GKuymjWR1dqfbCw1MyEP9j). Notes-only branch `claude/review-rv23`. Probes: `plans/rv23-shots/`.

## Verdicts
| Branch | Verdict | Sha |
|---|---|---|
| claude/vessel (VB1): RV22's must (round-one fetch) + 2 shoulds | PASS | 03b63d95 (game 705c6fc5) |
| claude/talk-close (B3): talk only up close | PASS (1 should) | f52e2abc |
| claude/p5s6-core (W6): Step 6 first turn, all off | PASS (1 note) | 95ef6947 (game 7c13cfe7) |
| claude/ending-checks (VB2): RV22's leftovers | see below | 571b073f (head 0a2993cc, handover only) |

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

## VB2 ending-checks 571b073f: running (arrows endgo teachoff, track; day_check 31, 50 on an ending-ON copy)
