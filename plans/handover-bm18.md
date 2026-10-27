# Handover: build master BM18 (session_01A3S2VBMYmTt2wCZa8ej7XR)

Read this first if you take over as build master (BM19). Before me: `plans/handover-bm17.md` (0.92.5-0.92.6). Stopped at the user's call (2026-10-26, via lead 40) after finishing 0.93.3.

## Who

- Lead: **lead 40**, session_01NXybH7NNqM8M4ngiyidq6m (took over from lead 39, session_019V68fz33UFv4cK5Z4iCDvi, 2026-10-26 ~22:00 UTC; lead 39 from lead 38 ~17:58 UTC). Report to the lead with priority "next", never "now".
- Publisher: PUB1, session_01GnpjFR6oumvuvTrmcXSqeg. On GO, tell PUB1 and the lead together (lead 40's rule).
- Check runners (0.93.3 round): CR1 session_01CsWNjCsy8u5mrHJgTVgCst (~55% memory), CR2 session_01DsTDi6xJcpdDVhSkELEm24 (~55%), CR3 session_01Pw3EQ24pSz4gjsFcLBMjUF, CR4 session_01RgnU5d6Um75LNznFSotXYH (fresh 2026-10-26), CR5 session_01UH1U1UpsoL7viYaRRBu2bZ (fresh 2026-10-26; the old CR5 session_01CHoEsvv7zMPZDr1ir7uAiz retired), CR6 session_013wLtAmKooMrgGrXF4Ljiof.
- Reviewers: RV18 session_01PMfvrCN6StPzwVSPGX7ijH (doors), RV20 session_01PyJwfvfQVu4oXTYDMGkacw (Step 5, workstep fix), RV21 session_01AmTyMHLr5UuCY9zo3nQcwS (vessel, ending, puzzles).
- Builders: FX29 session_01XmCJrSagiUiqhdfGLG9sTv (doors, check fixes), FX30 (week-guide test fix), B2 session_015mjNkxuGoEZGKA2ksBPz9u (workstep / team-arrow fixes), SW2 session_017dLaLFBnRUQin3PQEQq6so.

## Builds I made

| Build | Commit | Game sha256 | Notes |
| --- | --- | --- | --- |
| 0.93.2 | claude/staging-0.93.2 **d9c7e5f0** | c99ea59c...d5d3 | Two rounds (round 1 fixes: inspection Thursday clash, follower on the bunk, storm board, workbench tap, saves file:// quirk, p926 Day 14). Published by PUB1 ~17:40 UTC; claude/integration fast-forwarded to d9c7e5f0 on the user's OK (~17:50 UTC). |
| 0.93.3 | claude/staging-0.93.3 **19400976** | ec93b94dfe01d8a9f392257bb1f026ea8b1ca1c0cc24bce3d154ea3d2bcad085 | From d9c7e5f0: EV_SWAP_ON true (the diplomatic visit Days 16-19, comet Mon Day 22; 026278be), SW2's swap words bf7ba1ca, FX29's events_check fix 8da5f87d + bigevents_check fix 8a91f1dc (test only), FX29's doors-3way bdb6f00a (RV18 PASS), backlog rows CR1-W1, BM18-1, RV18-D1, the testing guide's rebalanced shares. HUD 0.93.3. Full round: see below. |

## 0.93.3 round (OLD = d9c7e5f0)

All six shares done, no new FAIL:
- CR1 all 11 OK (+ promo_sight, sound for CR3). CR2 cadet = expected only (Bunk 1's door shut at the start; walk 1-unit diffs), path, arc, lines (69 warnings = 0.93.2), lines --day, intro, p926, day 21, 22 OK. CR3 day 0/1/5/7, weekend, arrows_d, arrows_f, controller (incl. the new door part) OK. CR4 day 6/8/12/13/16/19, appt, saves OK; perf (moved from CR2, alone). CR5 interactions OK (2449 s), career known-old only, join OK (rerun for CR6). CR6 check_fast, stories, promo_beats, mech, bigevents, tiles, disc, food x2, clothes, day 27, fridays OK; events known-old FX24-2 only; its first join crashed on a page-load timeout (overload), CR5's alone rerun OK.
- perf: "3 problem(s)", all one-scene js-time flags (backlog 32 pattern): Sunday dinner mess portrait 2.82->4.31 ms; storm all-clear party landscape 1.73->2.74; garden picnic trifold-open-turned 1.09->2.51. No draw-call or memory problem (round trips 521->521->521; week 521->522). CR4 re-measured those 3 scenes alone, twice: none repeated (run 1 OK; run 2 one flag in a different shape, storm party trifold-open 2.25->3.54, 2.24 in run 1) = backlog 32 noise.
- **GO from testing** sent to lead 40 and PUB1 together, 2026-10-26 ~23:46 UTC. Publish and the integration fast-forward are the lead's/PUB1's (not done by me before stopping).

## The 0.93.4 plan (lead 40; NOT started, the user stopped here)

staging-0.93.4 = published 0.93.3 (19400976) + B2's claude/workstep-tap-fix **c79a66dc** (RV20 PASS; the live M15 Rewiring tap bug; branched from acbb52e0, so merge onto 0.93.3) + B2's **b7e84f81** on the same branch (stale team-job "your turn" arrow; **RV20 PASS** 2026-10-27 ~00:00 UTC: cadet identical vs c79a66dc, check_fast OK, mech teamgoal m8 OK; so merge the branch head b7e84f81) + FX30's claude/week-guide-fix **fa6b7de0** (arrows_check.py + build-table only; test only, no reviewer needed; CR1 ran `week guide` OK on 0.93.3's game: stuck 0, so mark backlog CR1-W1 fixed when it lands). Gate: check_fast, cadet vs 19400976, mech m15/m5/wstap/teamgoal, then the full round; tell the lead the sha when the round starts.

## Passed and held for later sets (the lead sends each set)

- Ending: RV21 PASS claude/ending-crossing **d1a61402** (the whole ending behind EV_ENDING_ON off; replaces every earlier ending sha). Merge note (RV21): its switch line sits after P926_APPT, as the vessel's will; keep the vessel's line first. Words: SW6 ending-words-a b8c89e7a PASS; SW5 ending-words-b 8ed1545a (bake only with EN2's endgame condition).
- Vessel: RV21 PASS VB1 claude/vessel **6d4b5192** (V-1..V-4) + VB2 claude/vessel-sky **3fb8eac7** (v.6; contains SW4's vessel words 7dd2eb5d); both needed. VB1 has shoulds pending.
- Step 5: RV21 PASS B4 claude/p5s5-puzzles **6b07b624** (t5-t7, behind P5_CASES5; check with B4 that it supersedes RV20's 4e5c878f/55b2e6a8); RV21 PASS B3 claude/p5s5-m20 **7c5d9f79** (sensor array, behind P5_M20); SW3 p5s5-words 277b9c15. FIXES NEEDED (don't merge): p5s5-skeleton 5957d244, p5s5-mech-a 3c38a65f, p5s5-mech-b 5ad090ff (RV20: 3 musts). RV20 (2026-10-27): B2's part of claude/p5s5-mech-a deefa61a PASSES, but the build fails machine_check on its switched-on copy ("traced faults", not the same twice) from B1's **51b1a9c6**, which deefa61a and B5's branch carry: merge NO Step 5 branch carrying 51b1a9c6 until B5 fixes it.

## Gotchas (new ones; BM16/BM17's still apply)

- A shell line `a && b && export X && (job1) & (job2) & wait` backgrounds the whole `a && ... (job1)` chain in a subshell, so job2 does NOT get X. Set env vars per job (`X=... python3 ...`).
- More than about three browsers on one 4-core machine gives Page.goto 30 s timeouts: false fails. A crash with no FAIL line on a timeout is a rerun-alone, never a game FAIL.
- interactions_check now takes ~40-68 min (backlog BM18-1); the shares in plans/testing-guide.md were rebalanced for it. When a runner finishes early, hand it a not-yet-started check from the slowest runner, agreed directly between the two runners so nothing runs twice (CR4 took CR2's perf; CR1 took CR3's promo_sight and sound; CR5 took CR6's join rerun).
- Lead hand-overs: check a new lead's claim against TEAM.md on the old lead's branch (and get_session's parent) before switching who you report to.
- A switch turned on makes old check expectations stale (bigevents' late saves assumed the old calendar): isolate with a one-switch-off copy before calling it a game bug.
- The keep-both merge helper (scratchpad, gone with this session) keeps both sides except the two HUD lines; always run names_check after it (it once made SAVE_KEY twice).
- check_fast before every push, even docs-only commits; when a stop hook nags about unpushed commits, still wait for check_fast.

## How to test

As handover-bm16/17: CADET_CHROME=/opt/pw-browsers/chromium, a CADET_WORK per parallel run (symlinks to three/ and acorn/), at most two browser checks at a time. cadet_test writes A_*.png/B_*.png in the working folder; crop the differing box to see what changed.

## Open questions for the user (via the lead)

- Backlog 12: the busy player's career pace (still the balancing pass).
- Backlog BM18-1: trim or split interactions_check so the round fits in ~35 min again?
