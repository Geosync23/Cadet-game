# Handover: lead 49 -> lead 50 (written 2026-11-06 ~13:25 UTC / 8:25 AM ET)

Lead 49 = session_01GKuymjjreuZtZeDMBX79xn, branch claude/lead-49 (TEAM.md log current). An earlier lead 49 session
(session_01GKuymjPvM7XFzxM7XqFREd) did 0.99.6 on Nov 1 and stood down; this session took over on Nov 6.
Read first: CLAUDE.md, plans/patch-0997.md (the user's 56 notes, seats, ALL defaults for the user), the bottom of TEAM.md.

## Where things stand
- **0.99.6 LIVE** (published 2026-11-06 ~06:13 UTC on the user's OK): Playtest https://claude.ai/artifact/2Uyqpm6jS9dvUW4ML7mb5H
  (slug 0c01401d-1612-4e1c-a69a-5df090589360, v3 = 1793945593-3443), Dev https://claude.ai/artifact/JftiS793gzEPhKRekatcon
  (slug 8f197d97-106b-4f75-83f3-37b6695372ad, v3 = 1793945609-190d), {downloads}. claude/integration = main = d7ad4c58.
  Publish recipe: tools/publish on claude/publish-pub3 (build.py, phone.js); publish_files needs files inside the working
  folder (copy in, publish, delete). Then fast-forward integration + main.
- **0.99.7 (the user's 56-note overnight list)**: every piece reviewed PASS and merged on claude/staging-0997; switch-on (21
  switch lines) + build turn 363107d; candidate 7fd8f6b, game sha256 b14421f82e04602cd608505756ddb8fb05bea4571af813d8e345424ebcd1cf7d
  (lead verified; GAME_BUILD 0.99.7; integration fast-forwards).
- **ROUND 0997 running since ~12:59 UTC** (plans/round-0997.md): R1 session_01GKuymnpcUSBmpZYiDK67GH, R2 ..mmnJnzWMxP769P9Edd,
  R3 ..o7sJwyufjkoEsCacB, R4 ..mmvXPrmsnyaH858XoJ (results on its own claude/checks-0996-r4), R6 ..jS1cBK12RvWv7L5ka;
  R5 = build master. **BM26 session_01GKuymkyzjd6auLTCEZK5CN** took over from BM25 (session_01GKuymnYTNkfxgLvtfFRg7w, memory)
  at ~13:00 UTC: R5 share, cadet vs 0.99.6 (every difference explained), round record, FINAL GO.
- Open in the round: R2 sees crew walking different routes from Day 2 ~07:45 (Pell, Noor, Luca, Petra, Davi, Yara, Vera):
  bisecting by switch; expected if one of the switches explains it.
- **Publish 0.99.7 only on the user's OK.** Then: same two pages (v4), phone test, ff integration + main.

## Seats (all idle unless noted)
Builders: CH1 ..jRkyieJLWiov9xvyp, MV1 ..mmL8h3gYY1Td9gxV3n, TP1 ..mneLr9U5MnEvACLMvS, CR1 ..mizPyyNVZeZ2xUhGm6,
JB3 ..mmiCEm3CMMrMTdWMEo, SC1 ..mk1xmJCgzW4Ee8Drz8 (also reviewed GM1, wrote TB6's words), CL1 ..mjnwwEESL9W6V7kQFK,
EV1 ..mkhvqRE7N1Rj4VMtWD, GM1 ..mmzSJiWGVamRuV5nSG, TB6 ..mj43WbsuRbKgL2mYc2, AV1 ..mmkjHutWouc88NdLkn (all session_01GKuy...).
Reviewers RV32 ..mkDX3gviqiGJcKLWuS and RV33 ..moAK9gACR31MRd1CMX: stopped (handovers on claude/review-rv32/-rv33).
Each builder has plans/handover-<seat>.md on its branch (SC1's is handover-sc1-p997.md).
Hourly check-in: trig_01V6DHhDEEAh21tr6iQRSm3S (disable it when you take over and make your own).

## Lessons from tonight
- Probe week-1 notes from a fresh save with the intro ON, following arrows like a player (fresh_walk.py in plans/rv32-probes).
- Builders ran check_fast with their switch OFF only; two failures appeared only with everything ON. Always run check_fast
  switched ON before merging, and on the all-on candidate before GO.
- machine_check's Sunday food run and ship-meters lines are knife-edges any schedule change can tip (fixed: JB3_FOOD_ON,
  5v exemption). Containers restart when running 4-6 browsers: two at a time.
- Messages cross a lot: restate decisions; verify branches.

## Open questions for the user (also in plans/patch-0997.md)
All the defaults in patch-0997's "Step-1 reports" table, plus: Pockets (snacks to pocket instead of eaten at the till);
not passing the bunk inspection costs nothing; Talk a while "answer then ask back"; birthdays every 14 days, never Fridays
(Days 4, 22, 41...); Captain's address clock 0.6; live music level; film score. Backlog rows added tonight: EV1-1 (fixed by
MV_SOFA_ON), CR1-2/3, JB3-1/2, GM1-1, CL1-4, MV1-1/2, EV1-2 (fixed).
