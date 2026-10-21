# Handover: patch builder A (PA)

Written by PA near its memory line (about 470k of 1M), 2026-10-20, so a fresh session can take over.

## Role and branch
- Patch builder A for the playtest patch (`plans/patch-plan.html` / `.md`, final). Lead: **lead 21** (session_01KYPEbF745ZQ9g9kr4XJgre). Reviewer: **PR2** (session_013ttt3gV3DaF9y4caBtFnh9). Owner stand-in for hooks: **OR1** (session_01W7AHxrcgBM3rJNtCFKwp9W). Section 14/10 owner: **PB** (session_01FWW2piuXkFYaRRzLXZiqYb, claude/patch-b).
- Branch `claude/patch-a`, last push 75aa54a (integration 0.64.5 merged in). Never touch main; never change the build-number lines.
- Seat: onboarding engineer (sections 21 and 21b). New code goes in `// ---- slot: Onboarding engineer (section 21b)`, just above its end line.

## What's built (batches A, B, C plus the review fix round): all done and pushed
- A: #1 (Day 2 meeting at Calder's own desk; `early`, `release`, `hold`, `stand` beat fields; desk field `desk: 'calder'` + schedDesks trade), #2 (first solo job words), #28 (Day 2 laundry tip any time, 3 wordings).
- B: #3 (Chief at the next table, `away: 3-mess-26`, walks over), #4 (how a day runs in Zeke's goodnight bubbles; `introHush`; owed goodnight said later or by Mail), #14 (device glow + pointer, 30 s cap, hidden in dialogues), #15 (laundry line).
- C: #11 (Tracked clears itself: `trkDoneCheck` in 15b's slot, `trkFrom/trkTo/trkAway`), #12 (`shuffleable` for following escorts), #13 (device tip waits for a long work step), #17 (`escBeside`, `ESC_GAP`, `escToYou`, 2 s give-up `gapT`, `tapBeside`), #18/#19 (`d1-end` beat 16:44-17:05, `introDayEndTick`, walk.trainend.1-3, arrows clock-out then the beam's top-left slot via `beamSlotWorld` and goals with `beam: true`, `introHoldNudges`, `introQuiet`).
- Build-table rows: `plans/build-table.md`, "Patch A" section. Shots: `plans/patch-a-shots/`.
- Every hook into another seat's section is its own commit (lists in the reports to the lead and in git log, "(hook, section N)").

## Shared formats (agreed)
- `introBeats(id, d)` entries may carry `early` (minutes before `at` the block starts); omitted = old rule (PB OK).
- Place field `desk: '<crewId>'` (4d); schedDesks trades that desk with whoever had it on that person's shift, skips when the person has no desk (PB OK).
- Goal field `beam: true` (15b's ixGoalWorld returns your name's spot with a height `y`; ixFrame draws at `w.y`).
- SHIP.intro.done keys added (saved): `d2-solo:end`, `d1-end:told` (never `:said`, introBeatTick owns `<id>:said`), `d1-end:start`, `arrow:clockout`/`arrow:beam`, `goodnight:owed` (1 owed, 2 said, 3 mailed).

## Loose ends
- #31 (remove "Ask Zeke") is PB's (claude/patch-b 95c22e7, touches introTap, intro_check part 8's ask block, design-doc). Take it from PB's commit when merging; don't edit those lines.
- career_check fails "busy: Relied on before Day 5": the same on integration; backlog #12, known and accepted.
- Batches D-F are other builders'.

## Gotchas
- intro_check in one run crawls in part 12 (about 10 min a beat after the earlier parts' state): run `--evening` and `--week` separately. Parts 0-11 in one go take ~1.5 h here.
- Never run more than ~3 Chromium checks at once on 4 cores: page loads time out (30 s) and screenshots hang.
- `pkill -f <pattern>` can kill your own shell (the pattern is in its command line): kill only python pids.
- Probes: copy `plans/patch-plan-probes/*.py` to a scratch folder and point `pp.py`'s SHOTS there, so shots don't land in the repo. Each run its own exported CADET_WORK.
- Staging part of a file: `git diff -U1` hunks applied with `git apply --cached` (a small script); indices shift after each commit.

## How to test
`bash check_fast.sh` (QUICK CHECK OK); cadet_test integration → branch (ALL IDENTICAL expected; everything new is intro-only or proven identical); intro_check `--evening` and `--week`; interactions, player, join, events, mech, clothes, day_check 2. Probes for each item are named in the build-table rows.

## Open questions for the user
None outstanding from PA.
