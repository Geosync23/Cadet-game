# Handover: build master BM21 (session_01GKuymkAoLNTFXef9RgiYLn)

Written 2026-10-29 ~20:10 UTC, updated 2026-10-30 ~05:30 UTC at about 57% memory, during the 0.99.3 round. Before me: plans/handover-bm20.md (claude/handover-bm20).

## Who
- Lead: lead 46, session_01GKuymiks9CC1WYr2may5nM (took over from lead 45 at ~13:00 UTC). Reviewer: RV26 session_01GKuymjwVsweGh8p9EbTGHU.
- Runners: R1 AS1 session_01GKuymmdgtDvbd8P7URXd4z, R2 session_01GKuymmiqCTVdUwF2rf5qBM, R3 DM2 session_01GKuymoBtAFGaak9qYYXS24 (pushes only to claude/devmode-j2), R4 session_01GKuymmw8rrCaw9Rn8frQ7Y, R5 = build master.
- Publisher: PUB2, on the lead's GO (the build master never publishes).

## Published today
- 0.98.0 = claude/staging-098d 37b858b4 (BM20; no RB1 turn 3).
- 0.99.0 = claude/staging-099 6d5684ba (game 041a699c...4ee2). Round plans/round-0990.md (claude/lead-46): five shares, all OK.
- 0.99.1 = claude/staging-0991 bc4579aa (game 8e4ac545...2d9d): 0.99.0 + TB1's title tap-to-wake gate 812dd3a0. All five shares OK. claude/integration = bc4579aa.
- 0.99.2 = claude/staging-0992 d180a704 (game 27d605e7...3920): title melody sooner (SD3) + no old-deck flash on New game (TB1). All five OK (R2 slow host: BM21 ran R2's day 0/1/5 + arrows endgo, R4 ran R2's perf). claude/integration = d180a704.
- 0.99.3 (in its round now): claude/staging-0993 df74ce0f (game 04c821fe...c2a9) = d180a704 + SD3 mess-sound 2348a5e6 + CH2 callhome ce742cb7 (contains CH1 chief 9346b1c3) + SD4 title-song 27caa4c3 + the turn. Gates all OK, cadet identical. GO sent to R1-R4 at ~05:25 UTC, OLD = d180a704. R5 log: scratchpad r5log3. User pre-approved publishing: final GO to lead 46 when all five OK (after a docs-only round-record commit on top, as for 0.99.1/0.99.2).
- Overnight mode (lead 46, 02:18): the user is asleep; carry rounds through, raise only real blockers.
- New sessions: reviewer RV27 session_01GKuymijhhErJ9V47wTGYrJ; SD4 session_01GKuymmn9csS8urK7bKkq5u; CH1 session_01GKuymnjryPMbX1HjbKRuWa; CH2 session_01GKuymmijFCFjHCppJyVuuP.
- User rule (via lead 46): every update now is 0.99.x; 1.0 = only the user's playtest notes.

## How I ran merges (worked well)
- Each merge in its OWN worktree (`git worktree add --detach /tmp/wt-x <base>`); never switch a worktree's checkout while a check runs in it (I did once and had to rerun everything).
- Gate per merge: verify_merge.py (base = merge-base), names_check, check_fast, the area's checks, then cadet_test vs the previous tip strictly alone. Long runs as `setsid nohup bash script.sh &` from the scratchpad; wait with one background `until grep -q ALLDONE` loop.
- cadet noise: a first run can show many 1-level pixels or a speech-bubble shift (bubbles follow on real time); rerun alone and compare the base with itself before calling anything.
- Build turn: header `build` line + GAME_BUILD, DEV_NOTES paragraph (mark the previous one published), build-table row; after the round, a docs-only commit recording the round, and send that commit with the unchanged game sha256.
- R5 share script: scratchpad r5.sh (WORKTREE LOGDIR): check_fast alone, then two lanes. fridays takes ~28-30 min now (not stuck).

## Loose ends
- controller_check reach (extra, not in the gate): stopped on 0.99.0 at 2 h 48 min with no FAIL in what ran; never completed. Needs > 3 h alone.
- Worktrees in my container: /tmp/b21, /tmp/wt-*, all safe to remove except /tmp/wt-r5d (R5 running) and /tmp/wt-0993b (the 0.99.3 candidate).
- Gotcha: a builder may move its tip after the review (SD3 0.99.2, SD4 0.99.3 twice): always take the exact commit RV27 named, and ask RV27 to confirm a newer one.
- Backlog closed in 0.99: 12 (BAL2), BM20-1 (OP1). Known-old list for the next round: backlog 14 / perf one-off spikes only.
