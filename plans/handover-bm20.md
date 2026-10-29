# Handover: build master BM20 (session_01GKuymiwDEgkwGmjJ2nokvg)

Written 2026-10-29 ~10:00 UTC at 63% memory. Read CLAUDE.md, plans/testing-guide.md, then this. Before me: plans/handover-bm19.md.

## Who
- Lead: **lead 45**, session_01GKuymnu4NeXJhwPe21FWk7 (claude/lead-45). Before: lead 44 (session_01GKuymj3tKpX7xwDZwBh8RM), lead 43. Merges only on the lead's GO; questions to the lead via send_message.
- Reviewers: RV25 session_01GKuymnnpKvNH4Ki69KEzwG, RV26 session_01GKuymjwVsweGh8p9EbTGHU.
- Runners (0.98.0 round): R1 AS1 session_01GKuymmdgtDvbd8P7URXd4z, R2 session_01GKuymmiqCTVdUwF2rf5qBM, R3 DM2 session_01GKuymoBtAFGaak9qYYXS24, R4 BB1 session_01GKuymne2zVMSTZjvCCmXKH, R5 = build master.
- Builders: OP1 session_01GKuymkG9JWDcSK9pMb28aj (0.98 walk fix + check fixes), RB1 (render), SD3 (sound), EV1/EV2 (visit), TB1 (title), DM2 (Dev mode), BB1 (backlog).

## Published
- 0.96.0 (controller + sound update + Diplomatic visit on): fe11cd66.
- 0.97.0 (Dev mode J0-J5 + docs): integration = 610ad7f1, game 0bd1b5b6...b36f. Live.

## NOW: 0.98.0 on claude/staging-pad
- Candidate game 7a2ae7d2's game, sha256 22f8939dbfea2dcf4b994dd8bfd7c8868f9d5450dd73c680c1dfd3c19d11918f; tip **10865180** (= 7a2ae7d2 + OP1's check-only fixes 34adecc s5cases, 1086518 puzzle p6; game unchanged).
- In it: SD3-2 sound tick (fb603947), OP1 walk-time fix FX24-2 + FX12-1 (2b79af3d merge of 3307e843), OP1 join_check 120 s (1d5ce762), RB1 render turn 3 (c7953218 merge of 8d7a3148, NOT the WIP 3468725), 0.98.0 turn (7a2ae7d2).
- Round (OLD = 610ad7f1): R2 OK (perf: calls lower everywhere; cadet only mem/calls), R4 OK (backlog 12 only), R5 OK 21/21 (plans/checks-0980-r5.md on claude/checks-0980-r5), R3: devmode/sound/etc OK, controller G2/G3 + walk-alone still to report (walk #rot timeout = load, known). R1: 12 OK + the two below.
- FAILs: s5cases and puzzle p6 = check expectations, fixed (in 10865180). **arrows step6 'sleep by day' (p5n:bed:22)** = old game gap in 28a p5nGuide (needs S.day; null at 12:30 Day 22 if you never clocked in); also in 0.97.0.
- **Lead 45's decision (09:53):** (a2) OP1 makes a small 28a game fix (~60 min) -> RV26 -> targeted rerun on the new candidate: check_fast, cadet vs 610ad7f1 (expect only mem/calls), arrows step5 + step6 (all ways), nights checks, day_check 22 (whatever touches 28a). If not PASSED by ~11:00 UTC: (a1) ship 0.98 as is (10865180) with the gap as a known old gap + a backlog row, fix in 0.99. Then send the lead GO from testing.
- claude/staging-098b 3dc9afda (hedge without OP1's walk fix, check_fast OK, cadet as expected): no longer needed (lead 45).
- cadet note: RB1's turn makes cadet report DIFFERENCES (state 'mem','calls': calls 173->142, geometries 453->422, textures 34->36) with renderer noise <= 1 level. Lead 45 accepted this as by design.

## claude/staging-099 (0.99), tip de05b965, game d61a9ead...
From fb603947: SD3-1 sound-099 7529b1e4 (644e8286), EV2 visit-099 3dda559 (cc81987f), staging-pad 2b79af3d (5dabfe9d), BB1 backlog-triage d9eb18ba (7f4d60d3; backlog TQ1-1 kept as closed + RV25-1 added), TB1 title-on-099 b980518d (de05b965; section 27 clash resolved: 0.98's 4-a-second event pick, THEN the title line). Each: check_fast OK, cadet vs fb603947 identical; sound + title checks OK at the last.
- To come: merge staging-pad again when 0.98 is final (OP1's check fixes + the 28a fix). BAL2 claude/balance-099 and RB1 turn 4 wait for the user. Then the 0.99.0 turn and a round.

## Gotchas (new)
- Container restarts happen (3 so far). Background jobs die; detached ones (setsid nohup) die too. Scratchpad survives. Re-run after a restart.
- Background tasks stop at their timeout (max 2 h): perf_check with OLD takes ~55 min + setup; run long things detached.
- Never `pkill -f`/`pgrep -f` with a pattern that's in your own command line (I froze my own shell once). Kill by PID.
- Two browsers at most; check_fast is two by itself.
- The build master copies RB1/OP1-style branches by exact commit, never the branch tip without checking (WIP commits appear on top).
- Worktrees I left: /tmp/w099 (bm20-099 = staging-099), /tmp/w098b, /tmp/wr7, /tmp/wr8 (notes). Safe to remove.
- My round scripts (scratchpad): r97.sh pattern (two lanes, join alone at the end); gates via a small script file.
