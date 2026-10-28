# Handover: build master BM18 (session_01A3S2VBMYmTt2wCZa8ej7XR)

Read this first if you take over as build master (BM19). Before me: `plans/handover-bm17.md` (0.92.5-0.92.6). Finished 0.93.3 (GO), then built the combined staging-0.94.0 (everything merged, nothing switched on yet). Stopped 2026-10-27 ~03:00 UTC: the user is moving the project to another account (lead 40).

## Who

- Lead: **lead 40**, session_01NXybH7NNqM8M4ngiyidq6m (took over from lead 39, session_019V68fz33UFv4cK5Z4iCDvi, 2026-10-26 ~22:00 UTC; lead 39 from lead 38 ~17:58 UTC). Report to the lead with priority "next", never "now".
- Publisher: PUB1, session_01GnpjFR6oumvuvTrmcXSqeg. On GO, tell PUB1 and the lead together (lead 40's rule).
- Check runners (0.93.3 round): CR1 session_01CsWNjCsy8u5mrHJgTVgCst (~55% memory), CR2 session_01DsTDi6xJcpdDVhSkELEm24 (~55%), CR3 session_01Pw3EQ24pSz4gjsFcLBMjUF, CR4 session_01RgnU5d6Um75LNznFSotXYH (fresh 2026-10-26), CR5 session_01UH1U1UpsoL7viYaRRBu2bZ (fresh 2026-10-26; the old CR5 session_01CHoEsvv7zMPZDr1ir7uAiz retired), CR6 session_013wLtAmKooMrgGrXF4Ljiof.
- Reviewers: RV18 session_01PMfvrCN6StPzwVSPGX7ijH (doors), RV20 session_01PyJwfvfQVu4oXTYDMGkacw (Step 5, workstep fix), RV21 session_01AmTyMHLr5UuCY9zo3nQcwS (vessel, ending, puzzles).
- 0.94.0 builders: B3 session_014FBmsiTsA9QymoN2qt4NyL (shutdowns, sensor array, talk-close, train-titles), B5 session_01CgbXRamJJp66pFTP43KYoB (Senior Officer promotion), VB1 session_01UsjGN26E88zwrNPWwef4iT (the vessel's events), VB2 session_01KRBGtugjBpv5iGcV5WDvCP (vessel sky, kit, ending checks). Reviewer RV22 (Step 5, vessel; ask lead 40 for its session). EN1, EN2, B4, FX29, EC1 archived.
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

## 0.93.3 after GO

Published by PUB1; the user said yes to integration: **claude/integration fast-forwarded d9c7e5f0 -> 3fd762cb** (staging-0.93.3's tip: 19400976 + docs), check_fast OK on it. 0.93.4 was never built on its own: the user's new rule ("everything on, nothing should be installed off", 2026-10-27 via lead 40) folded it into 0.94.0.

## staging-0.94.0 (the combined build; last game merge 64a1ba76, game sha256 958493d0697cca4c...; this note sits on top)

From integration 3fd762cb. **No switch flipped, HUD still 0.93.3.** On every push: check_fast OK and cadet_test vs 0.93.3 (19400976) ALL IDENTICAL (everything new is off). Merged, in order (merge commits on the branch name each):

| Piece | Sha merged | Review |
| --- | --- | --- |
| B2 claude/workstep-tap-fix (M15 rewiring tap + team-job arrow, live fixes) | b7e84f81 | RV20 PASS |
| FX30 claude/week-guide-fix (arrows_check week guide) | fa6b7de0 | test only; CR1 OK on 0.93.3 (CR1-W1 can be marked fixed) |
| B1 + VB2 kit + B5 claude/p5s5-promo (Step 5 skeleton, career 51b1a9c6, S5-2 promotion, kit 69eb706d, SW3 words) | 5703dfb6, cbca3e3e, ea40ae51, **f00d93c1**, **c3d36cde** | RV22 PASS f00d93c1 (its MUST: ladderBigP5's sort had been commented out; I checked the fixed line); c3d36cde = RV22's one should |
| B2 claude/p5s5-mech-a (M19 power and relays) | deefa61a | RV20 PASS (B2's part) |
| B3 claude/p5s5-mech-b (M18 shutdowns) | fa1e152c, **98460d79** | RV20 PASS fa1e152c; 98460d79 = its should |
| B3 claude/p5s5-m20 (M20 sensor array) | 989b1759, **247420aa** | RV22 PASS 247420aa |
| B4 claude/p5s5-puzzles (S5-6 cases, t5-t7) | 6b07b624 | RV21 PASS |
| VB1 + VB2 claude/vessel (the Veyli vessel, contains vessel-sky 3fb8eac7) | 5578c78d, **0340b6f9** | RV21 PASS up to 6d4b5192 + vessel-sky; 0340b6f9 (three switch-on fixes) with RV22 |
| EN1 + EN2 claude/ending-crossing (the whole ending) | d1a61402 | RV21 PASS |
| VB2 claude/ending-checks (ending arrows/controller parts) | 6fe92ead, **571b073f** | test only; all 7 arrow ways + controller ending green (VB2) |

Checks with things switched on, on copies: machine_check with P5_STEP5 = true OK twice (after B5's fix); controller_check ending OK on 64a1ba76. VB1, VB2 and B5 each confirmed my conflict fixes in their areas.

**Conflicts I resolved (owners confirmed):** section 18's vessel and ending data blocks each opened an `if (...) {` sharing one closing brace: I added the missing `}` (the parse error names_check caught); words re-baked with content_gen twice (baked-words clashes); controller_check.py had NEEDS/PART_FN re-declared by two pieces (would have dropped door, shut, s5cases): now one table after part_vessel; arrows_check.py one PARTS/WAYS line for step5 (B5), vessel (VB1), endstay/endgo (VB2): 'track' and 'teachoff' mean the same for both (B5 + VB2 checked); bigevents_check late saves: Day 23 due = the first row after Day 22, Day 28 (vessel passed over) due = the next row after Day 28; docs/backlog/build-table duplicates removed.

**NOT merged yet (waiting for RV22's PASS):** B3's claude/talk-close **f52e2abc** (talk only when close; the user's request; on, no switch; from ac810e7e); B3's claude/train-titles **7cbc1ad0** (4 strings: "with Calder"; from 64a1ba76); VB1's round-one fix (sha from VB1 / lead 40). Merge each on its PASS, then check_fast, cadet vs 0.93.3, and controller_check ending.

## Switch-on and round steps for the next build master

1. Merge whatever has passed since (above). check_fast; cadet vs 19400976 must stay ALL IDENTICAL while everything new is off.
2. On lead 40's word, one commit per switch, each with check_fast: `const P5_STEP5 = URL_FLAGS.has('p5s5');` -> `true` (its sub-switches P5_PROMO3, P5_M19, P5_M18, P5_M20, P5_CASES5 are already `P5_STEP5 && true`); `const EV_VESSEL_ON = URL_FLAGS.has('evvessel');` -> `true`; `const EV_ENDING_ON = URL_FLAGS.has('ending');` -> `true`. Update design-doc.md and DEV_NOTES ("switched on in 0.94.0") in the same commits.
3. Ask lead 40 about the older `false` switches still in the file (TRAY_TRAVELS, INTRO_ASK_ON, ZEKE_CABIN_MAIL, PAD_ON; END_WAY_BACK is CUT by the user and stays off): the "everything on" rule may or may not cover them; cut items stay off.
4. Set the HUD lines (header `build` line and GAME_BUILD) to 0.94.0.
5. Gate before the round: check_fast; cadet vs 19400976 (expect differences now: explain each); machine_check twice (same faults both runs); bigevents, events, fridays; day_check 16-19, 22, 27-30, 31-36 (the vessel and the ending's week); controller_check (all but reach, with ending, m19, m20, s5cases, vessel, shut, door); arrows_check incl. step5, vessel, endstay, endgo.
6. Full six-runner round (plans/testing-guide.md shares; add the new event days 27-36 and the new parts to the lightest runners), OLD = 0.93.3's game (19400976). Known-old: career "Relied on" before Day 5 (backlog 12), events FX24-2, perf one-offs (backlog 14, 32).
7. GO/NO-GO to the lead and PUB1 together.

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
