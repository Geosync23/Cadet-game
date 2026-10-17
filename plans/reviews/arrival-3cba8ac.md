# Review: claude/arrival c55b7a9 + 3cba8ac (0.42.0-0.42.1, section 21 on paper, intro_check.py)

Reviewer 1, 2026-10-17. Diff: `git diff origin/claude/ship-integration...origin/claude/arrival`. New section 21 plus the build line: in seat. intro_check passes on the branch alone.

**Verdict: PASS WITH FIXES.** Fixes 1-3 before 0.60.0 (1 breaks intro_check once combined with the sim bus); 4-6 before wave 2 makes the evening playable.

## 1. MUST FIX: intro_check fails once combined with sim 0.26.22 (the flags aren't the intro's to keep)
- With the bus merged (a scratch merge of origin/claude/arrival with d45b03a; the only conflict is the build line), `introFlagSet` writes to section 13's `SHIP.flags`. `introBegin` / `introBlank` reset `SHIP.intro` but never clear the flags the intro set, so every `run()` in intro_check inherits the last run's flags. Result on the merged build: `FAIL idle: the device counts as handed over though you never came` (`intro.device` left over from the happy path), and `flagAt` is wrong for every run after the first.
- It's the same bug in the game: a second arrival (New game, or skip after a played intro) starts with `met.calder`, `intro.device` and `week1.*` already set (see also the sim review, finding 1: New game doesn't clear the flag store).
- Fix: an `INTRO_FLAGS` list (escort.*, week1, week1.d2-d7, week1.done, intro.device, met.calder, mug, seedling); `introBegin` clears them with `flagSet(k, null)`. Then run intro_check on a merge with the sim branch, not only on its own.

## 2. MUST FIX: "I know my way around" early locks you out of the device for good
- `introEnd()` sets only `week1.done`. The handover (`intro.device`), `met.calder` and `week1.d2`-`week1.d7` are set only by steps and beats, and `introAdvance` returns at once after `introEnd`.
- Path (proven on paper): miss the Sunday evening (the idler), then choose "I know my way around" on Monday at 07:00 before the 07:50 briefing; run to Day 8. Result: `intro.device=false`, `met.calder=false`, `week1.d2=false`, `week1.d5=false`, `week1.done=true`. The device seat's lock reads the handover, so the device stays locked forever. Any social gate that reads `week1.dN` (and not `week1.done` as well) stays shut.
- Fix: `introEnd` sets the end state: `intro.device`, `met.calder`, and all `week1.dN` (and their points if the plan wants them), or the hook register says, in writing, that every consumer checks `flag('week1.done') || flag('week1.dN')`. The first is safer.

## 3. SHOULD FIX: neighbouring checkpoints complete each other, and the wanderer test misses less than it says
- A step is done when you're within 3 tiles (Chebyshev) of its checkpoint, with no room test, though each checkpoint names its room. `hello` is at [9,8] and `haulway` at [12,8] (3 apart), and `works` [16,6] and `lift` [16,8] are 2 apart. So standing at the ramp foot completes "lead to the haulway", and reaching the Works door completes "take the lift" in the same tick, before the escort has moved.
- That's why intro_check's wanderer ("misses every other step") misses only 3 of the 7 odd steps (ramp, bunk, servery): its `here` for the next step is still the previous checkpoint, and the 3-tile radius counts it.
- Fix: require the checkpoint's room (`room` is already in the data) and a radius of 1-2, or check that no two consecutive checkpoints are within the radius (add it to intro_check's data test).

## 4. SHOULD FIX (before wave 2): a step's wait counts from its scheduled time, not from when it became the current step
- `late = at + wait` uses the step's nominal `at`. The steps run one after another, so a slow step uses up the next steps' waits. The DEV_NOTES and the comment say "wait so many ship minutes for you at the checkpoint".
- Proven on paper: a willing player who gets to each checkpoint 10 ship minutes (about 17 real seconds at 0.6 ship min/s) after it becomes current misses `wing` and `toMess`, though every wait is 20-30 minutes. At 8 minutes it just holds. Crossing two lifts in that evening will often take longer.
- Fix: keep `I.since` (the minute the step became current, saved), and `late = max(at, I.since) + wait`; keep `until` as an absolute cap for the dinner steps.

## 5. Small: `introBeats` gives Calder's dinner beat the wrong end
- For `chief` (fallback `{ until: 20:00 }`, no `wait`), `introBeats` returns `until: at + 20` = 18:50, so section 14 would walk Calder off at 18:50 while the step waits for you until 20:00, and the meeting could start with her gone.
- Fix: `until: f.until !== undefined ? f.until : st.at + (f.wait || 20)`.

## 6. Note for the combine (the crew designer's change)
- The roster at 0.41.10 has Torres as "Engine officer", working at Deck 6 `work:engine`, off Saturday and Sunday. The week assumes he's in the Works bay on Monday and off on Thursday ("Day off for me", Day 4). That depends on the crew designer's days-off change (Torres Thu-Fri). intro_check doesn't test it; add a data check that `INTRO_ESCORT`'s `rota.offDays` include Day 4's weekday.

## Also checked
- 4. "Save and reload at every step" round-trips only `SHIP.intro` through `introSave`/`introLoad`, not the real save. It can't catch flags (now in section 13's store) or Day 0 saves. Section 13's `loadGame` currently throws away any save with `day < 1`, so a reload on the arrival evening loses the game (flagged to the sim engineer for the Day 0 step). The check should save and load through `saveGame()`/`loadGame()` once wave 2 is real.
- No `R()`, `Math.random` or `Date.now`; hash key 700 reserved, not used; the save is read defensively; the skip flag stays outside the save and isn't written with `?nosave`; test URLs start with the intro off; every id in the steps is on the roster. Small: `introLoad` keeps `null` and `""` values (`isFinite(null)` is true). Harmless today.
- Merge note for the lead: section 21 and social B's 20c are both inserted at the same spot (after `chatTick`, before `// 6. CAMERA`). Expect a conflict there: keep 20c first, then 21.
