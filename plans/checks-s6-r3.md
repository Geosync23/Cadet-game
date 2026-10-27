# 0.95.0 full round (Step 6 on): runner R3

Runner R3 (session_01GKuymmv95Tm7siWzMeEgmS), 2026-10-27. Lead: lead 42. Build master: BM19.
OLD = 0.94.0, claude/integration 6f1915cb (game sha256 5f4c5415814c78eb4c93eaad76ecc35dfa53f1f7cbb4c1f5af541f3971900a0f).

## Result: R3 OK on candidate 2

Candidate 2: claude/staging-p5s6 82b02fb9, game sha256 `4a4bed1c6d7b8cb4354d4c4217e970ba2d5b3758a7f0ade48c3c22b159069595` (confirmed).
Checks from 82b02fb9, except controller_check.py from e5193f0 (BM19's two test-only fixes, below). Game file the same in all.

| Check | Result | Key lines |
|---|---|---|
| day_check Day 0 | OK | DAY CHECK OK |
| day_check Day 1 | OK | DAY CHECK OK |
| day_check Day 5 | OK | DAY CHECK OK |
| day_check Day 7 | OK | DAY CHECK OK |
| weekend_check | OK | WEEKEND CHECK OK |
| arrows_d_check | OK | arrows_d_check: OK |
| arrows_f_check | OK | arrows_f_check: OK |
| promo_sight_check | OK | PROMO SIGHT CHECK OK |
| sound_check | OK | SOUND CHECK OK |
| ending_check (moved to R3 by BM19) | OK | ENDING CHECK OK; offer: none None, slow 39, week offer 39, back 32 |
| controller_check, every part but reach (4 runs, each under 2 h) | OK | see below |

controller_check (e5193f0), all CONTROLLER CHECK OK:
- C1 idle save calls touch walk pick lift door day games unplug odd: OK (run alone; see note 3)
- C2 shut off quiet base deck pick1 panels api lists tiles disc screens marks touch3 drop settings a11y firstuse: OK (check 211fd316; those parts unchanged in e5193f0)
- C3 m19 m20 s5cases s6cases vessel ending m21 m24 team m23 deck6 promo4: OK
- C4 nights (check 211fd316): OK; mentor (e5193f0): OK

## Notes: what failed on the way, and why (all check-side; no game change)

1. **ending_check (part offer)**, round 1, d695d899's check: FAIL "offer: Day 32 (Step 6 off), none before Calder's
   question, Day 32 after Day 26, Day 39 after Day 33" (none 32, slow 32); OK on OLD. Cause: part_offer turns Step 6 on
   with `window.P5_STEP6 = true`, but 0.95.0 declares P5_STEP6 inside the game's wrapper function `(() => { ... })()`,
   which hides the window property (a `var` there is local too). Fix (BM19, 82b02fb9): the Step-6-off copy assigns
   `window.P5_STEP6 = ...` instead of declaring it. Proven OK on the e0084ca9 game and on candidate 2.
2. **controller_check ending (pad)**, round 1: FAIL "the offer (Day 32): no choice by pad / not met": same cause (the part
   jumps to Day 32; with Step 6 on the offer waits for Calder's question). **m21**: FAIL "the wall screen ... should show
   the agenda" (m21Screen right; a "Starving" hunger card in the box). Both fixed in the check by BM19 (211fd316: ending
   part with Step 6 off; m21 feeds the player first). OK on candidate 2.
3. **controller_check C1**, candidate 2, run beside other browsers: idle 2 FAILs (`.f_device.page.domHash` differs with
   PAD_ON on and an untouched pad) and walk crashed (Page.click('#rot') 30 s timeout: the known load false alarm). Re-run
   alone on the machine: all 12 parts OK. Load, not the game (the only game change e0084ca9 -> 82b02fb9 is M23_GOAL).
4. **controller_check mentor**, 211fd316: FAIL "not yet: no P5_STEP6 switch line": its guard missed the "Step 6 already
   on" case the other Step 6 parts have. Fix: `if (on == src and not p6_on(src)) or 'function mtSettle' not in src:`
   (BM19, e5193f0). OK.

## Round 1 (e0084ca9, game d1666007...f278), for the record
day_check 0/1/5/7, weekend, arrows_d, arrows_f, promo_sight, sound: all OK. Taken from R1: `arrows_check step5`: OK.
For BM19: mech_check m15 (d695d899): OK; ending_check: notes 1. controller: notes 2; cut at the 2 h limit in nights
(nights and mentor skipped on BM19's word: candidate 2 replaces round 1).
