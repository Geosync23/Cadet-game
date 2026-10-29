# Handover: build master BM21 (session_01GKuymkAoLNTFXef9RgiYLn)

Written 2026-10-29 ~20:10 UTC at about 37% memory, idle after 0.99.1 went live. Before me: plans/handover-bm20.md (claude/handover-bm20).

## Who
- Lead: lead 46, session_01GKuymiks9CC1WYr2may5nM (took over from lead 45 at ~13:00 UTC). Reviewer: RV26 session_01GKuymjwVsweGh8p9EbTGHU.
- Runners: R1 AS1 session_01GKuymmdgtDvbd8P7URXd4z, R2 session_01GKuymmiqCTVdUwF2rf5qBM, R3 DM2 session_01GKuymoBtAFGaak9qYYXS24 (pushes only to claude/devmode-j2), R4 session_01GKuymmw8rrCaw9Rn8frQ7Y, R5 = build master.
- Publisher: PUB2, on the lead's GO (the build master never publishes).

## Published today
- 0.98.0 = claude/staging-098d 37b858b4 (BM20; no RB1 turn 3).
- 0.99.0 = claude/staging-099 6d5684ba (game 041a699c...4ee2). Round plans/round-0990.md (claude/lead-46): five shares, all OK.
- 0.99.1 = claude/staging-0991 bc4579aa (game 8e4ac545...2d9d): 0.99.0 + TB1's title tap-to-wake gate 812dd3a0. All five shares OK. claude/integration = bc4579aa.
- User rule (via lead 46): every update now is 0.99.x; 1.0 = only the user's playtest notes.

## How I ran merges (worked well)
- Each merge in its OWN worktree (`git worktree add --detach /tmp/wt-x <base>`); never switch a worktree's checkout while a check runs in it (I did once and had to rerun everything).
- Gate per merge: verify_merge.py (base = merge-base), names_check, check_fast, the area's checks, then cadet_test vs the previous tip strictly alone. Long runs as `setsid nohup bash script.sh &` from the scratchpad; wait with one background `until grep -q ALLDONE` loop.
- cadet noise: a first run can show many 1-level pixels or a speech-bubble shift (bubbles follow on real time); rerun alone and compare the base with itself before calling anything.
- Build turn: header `build` line + GAME_BUILD, DEV_NOTES paragraph (mark the previous one published), build-table row; after the round, a docs-only commit recording the round, and send that commit with the unchanged game sha256.
- R5 share script: scratchpad r5.sh (WORKTREE LOGDIR): check_fast alone, then two lanes. fridays takes ~28-30 min now (not stuck).

## Loose ends
- controller_check reach (extra, not in the gate): stopped on 0.99.0 at 2 h 48 min with no FAIL in what ran; never completed. Needs > 3 h alone.
- Worktrees in my container: /tmp/b21, /tmp/wt-*, all safe to remove.
- Backlog closed in 0.99: 12 (BAL2), BM20-1 (OP1). Known-old list for the next round: backlog 14 / perf one-off spikes only.
