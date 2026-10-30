# Handover: AR1, the arrows analyst (then builder of pieces B and E)

Written 2026-10-22 ~14:45 UTC by AR1 (session_01XcfcbFvi4nMVUPZgT2BcmE, about 58% memory; stopping here as agreed with
lead 28). Lead: **lead 28** (session_01S7AdxK1ZyXiEFowP3k5gng; lead 27 before). Read CLAUDE.md, DEV_NOTES ("The arrow
queue"), plans/arrows-briefs.md, then this.

## Branch and what's on it
`claude/arrows-plan`, from claude/integration 2b4a05db (0.64.15). This session could push only to this branch, so plan docs
and game commits share it (lead 27 agreed). The build master can merge it whole or cherry-pick the game commits.
- **Plan docs:** `plans/arrows-pillar5-plan.html` (the plan page, published by the lead at
  https://claude.ai/artifact/7rKvXwbZLRsJj8k7yrXXkK; republish from the tip after page edits), `plans/arrows-pillar5-notes.md`
  (raw notes: my tracked-shift play, how the arrow works today, helpers' notes A-D, Steps 3+ kept at the end),
  `plans/arrows-tools/` (play harness, bot, honest shift player), `plans/arrows-briefs.md` (briefs for B and C, the arrows
  check, the decisions, the Settings switch), design-doc.md ("Teaching arrows" under the player + Answered entries).
- **Piece B, the arrow queue** (5c798b5, c0ab64c, 5dd6b6f with RV2's points): switched off, `var GUIDE_ON = false` in 15b's slot.
- **Piece E, the training arrows T1-T3** (the commit after 5d47d1d): `guideTrain()` in 15b's slot, read-only from `SHIP.works.cur`.
- **arrows_check.py**: parts `queue` (piece B + T1), `shift` (Day 9) and `week` (Days 2-8), a player who only follows the
  arrow; option `guide` plays shift/week with the queue on. On 2b4a05db shift and week FAIL by design: each FAIL names its
  fixer. Checks on the last game commit: names_check OK, check_fast OK, cadet_test vs 2b4a05db ALL IDENTICAL (run alone).

## Decisions recorded (as passed on by leads 27 and 28)
Fixes first; the shift's arrows always while the shift is tracked; panel pointers the first three times; a meeting may
take the arrow from 15 minutes before; Settings switch for teaching arrows (AC1 owns it: `SHIP.device.settings.teach`,
`teachMode()`; B reads it via `guideMode()`); the burst pipe's job taken at the pipe; scan first (FX2); Tomas's
Wednesday warning (built by FX3); "Beyond the arrows" (FE1, DS1 now; no silent no, What's next, week check as a release
rule later).

## Who's who
- FX1 session_01WmdPR5B5QC56Hid3F5M1wv (arrow/tracking lifecycle; never answered which lines it edits: B changed
  `goalNow`, the ixFrame goal line and `toast` (section 11, HUD seat to review); expect a small clash there).
- FX2 session_01JRCSTi6r1qQ51mTgwgJ7es (drill and side jobs, scanner job and scan first, Tuning words, galley calibrate,
  dropped part). FX3 session_01UZWrZRivwQJPKL3x7c8Ft9 (lift, burst pipe, small lessons, reputation, Record, hauling any
  day with per-stop words, Tomas's warning). PR9 session_01B1FUTc4sJR4Q5FFnx7L6Db reviews FX1-3. All have the
  arrows_check lines and commands.
- RV2 session_01E1TTHbhLzy2U6pAoGh7E9a reviews B (full round on 5dd6b6f under way), then C, then E.
- AC1 session_01LDmfZ93ttCJ4XfoSDkJqx2 (claude/arrows-c): piece C, the pointer; `arrows_pointer_check.py`. The arrows
  check's follower already presses `pointNow()`'s element when C is in.
- AR2 session_015pnwa5oK7TDF5gZXNFLLvx (claude/arrows-plan-2): its section is merged into the page ("Step 2 in play").

## Next (for the fresh session lead 28 starts)
- Piece D, the shift chain S1-S9 as queue entries, **after FX1 lands** (it fixes clock out, the empty board, "On shift",
  tracking): rebase onto FX1, then add level-4 entries (clock out over the job at shift end, the empty-board line) and
  the pointer half once AC1's `pointAsk` is in.
- Pieces F1-F4 (each lesson's own moments, in its owner's section), moving each `setGoal` caller onto the queue (the
  list of all 31 is in the brief).
- Re-run `arrows_check.py BUILD.html week guide` on each fixer's build; it is the measure, and later a release rule.

## Gotchas
- Dev mode's Set career switches tracking off (track = null); real play has a stale job id. arrows_check sets it as in a
  real game. Dev mode's clock skip marks skipped workdays as excused.
- The game caps a frame's time step: run the clock by shipNow(), not frame counts.
- `GUIDE_ON` must stay a `var` (goalNow above it and toast below it may run first).
- The follower: taps what the label names (a shelf by its name), else a real screen tap at the pin; reads a tuning card's
  word; treats time spent working or in a meeting as not stuck; tops up needs at night (a normal evening).
- The safety check refused a commit that wrote "the user said" from a relayed message: attribute relayed decisions.
- A "Your bunk, Deck 4" arrow stayed up over 3 hours on Day 8 in the `week guide` run (not a queue entry; a needs or
  sick arrow, not yet looked at).

## Open questions for the user
None of mine.
