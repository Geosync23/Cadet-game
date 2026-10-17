# Light review: claude/arrival 1148cc20 + 01a96d20 (0.42.29-0.42.30, onboarding engineer 3): the walk-and-talk to the lift, the briefing played in full

Reviewer 1e, 2026-10-17. Tested by the engineer's recipe: a worktree at origin/claude/cand-0605, `git apply -3` of e47fb282..01a96d20 (only the two build-line conflicts; I kept cand's), claude/content's `content/` and `content_gen.py` baked in, then `intro_check --evening`.

## Verdict: PASS

**intro_check --evening:** OK.
- Torres is 0 tiles away after each real lift ride (5→4 at 18:02, 4→3 at 18:22).
- The walk to the lift: paused 0.0 s, and never standing still.
- Core lines heard 18/18, and the line count per place matches what's written.
- Draw-call peaks: Deck 5 193, Deck 4 207, Deck 3 257.
- The ramp closes at 17:40 and opens at 18:37.

**From the lift on, nothing changes (checked in the code):**
- `pace` applies only on Deck 5 before `tour:lift`.
- Every place after the lift is non-`walk`, so the new `hold` condition (`Q.some(q => !q.t.walk)`) behaves as before there.
- At the lift, the splice only drops non-`must` walk entries.

**The `must` works entry:** it is queued in front of any walk lines. At the lift, the lift's own non-walk entry lets `hold` keep Torres there while the works lines finish, which is what's intended.

**`introWriterLines`:** returns an array, or null, like `introWriterLine`. Its fallback without `VOICE` returns `introWriterLine`'s array or null. `introSay` takes an array. Unfillable lines are filtered out.

**The scene guard (0.42.30):**
- While any `intro-` dialogue is open, nobody's week escort mode applies, so they follow their own plan until it closes.
- The engineer's part 10 asserts the briefing plays to its last line and that the follow doesn't start during it.
- I didn't run part 10. It runs only in the full intro_check (not `--evening`), and this is a light review. The engineer's results are in DEV_NOTES 0.42.30.

## LOW (content and pacing, for the engineer and head writer 4)
- **Most walk-up lines go unsaid.** In the following run, the walk from the ramp to the lift is 17:41-17:52 ship time (12 real seconds with him on Deck 5). At `INTRO_TOUR_GAP` spacing, only **3 of the 8 `walk.up` lines** were said before the lift dropped the rest (the per-place counts read "up 3/8"). That's by design (unsaid walk lines are skipped at the lift), but five written lines are never heard by a player who just follows him.
- **Options:**
  - trim `walk.up` to about 4 lines;
  - slow the stroll further (`INTRO_STROLL` 0.5 → 0.35);
  - or let the 3 most important lines be `core`.
- It's the user's or the head writer's call.

**Nit:** the tour only moves on in order (`INTRO_TOUR.find(...)` is the next one not done), and the works stop fires within 2 tiles of [16,6]. The usual path from the haulway to the lift passes (14,8)/(15,8), which is inside that, so it's fine. A player who goes round some other way and never comes within 2 tiles would stall the tour at works. That was true before this change too.
