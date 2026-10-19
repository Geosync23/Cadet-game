# Handover: seat E5 (E2's seat, mechanic engineer), Pillar 5 Step 4

Written 2026-10-19 by E5 (session_01QsZymCraDjLzVDooLvigNk). Read `plans/handover-mech-e2.md` first (everything E2 built,
gotchas, how to test); this note adds only what E5 did.

## Branch and builds
- `claude/mech-incidents`. E2's last: 0.51.12 (93fbdb5: `playerRigRebuild` in 24l, a leak +1 in all). E5: 0.51.13 (60a418f),
  0.51.14 (2c513e6). Next build: 0.51.15.

## What E5 built
- **0.51.13:** `playerRigRebuild` (24l, E5 owns it: lead 17's call) also remakes your stand-in at a place (`recBody(ACT)`).
  mech_check `ff` proves the pin is merged into the chest (16 meshes before and after: no extra draw call), back after a
  reload, gone with no grade; `m13` checks a leak pays +1 in all and `m15` that right first time pays +2, only where 24
  core's side-job turn-in (`WORKS_SIDE_KINDS`) is in.
- **0.51.14, M8 stage 2 team parts (24h):** `TEAM_PARTS`, `TEAM_PARTS_DAY` 18, `TEAM_PARTS_LATE` 10, `teamT0`, `teamPartsN`,
  `teamParts(j, t)` (at `teamPost`), `teamPartsCheck(j, t, skip)` (at `teamTick`'s start). Uses E1's `manifestRun`,
  `manifestRunDelivered`, `manifestRunEnd` (hook register). Saved: `j.partsRun`, `j.partsLate`, `side.parts`.
  mech_check `tparts` (only with manifestRun) and `side.parts` in the `side` save round trip.

## Loose ends
- None open. Rewiring's right-first +1 is paid by 24 core's turn-in (E6, claude/mech-rounds 2edb69c, R5 PASS; lead 17: nothing
  for this seat). R5: 0.51.11 PASS WITH FIXES (the pin, done), 60a418f (0.51.13) PASS; 2c513e6 (0.51.14) PASS (notes only: the lead's late fetch takes no stock while your run does; an empty shelf still loads, E6's).
- Trial with E6 910131e: mech_check m8 m4 m13 m15 ff tparts side OK.
- E1 retired: manifestRun's owner is now E6 (session_018cZuXpb4XdFs47zXoPcF8B). W2 retired: new lines go on this branch in
  W2's style, listed in the DEV_NOTES row (plans/handover-writer-w2.md on claude/writer-p5).
- R5's note: promoPip could call playerRigRebuild later (E6's code, not this seat's).

## Trial merge with E1 (how E5 did it)
Worktree from HEAD, `git merge origin/claude/mech-rounds`: the two build-number lines in the game (take ours) and two
mech_check blocks conflict (keep both; in the EXTRA loop take ours' line plus E1's side/mrun lines).

## Open questions for the user
- The parts each team job asks for are E5's pick (two from STOCK per job); easy to change in `TEAM_PARTS`.
