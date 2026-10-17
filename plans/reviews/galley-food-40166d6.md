# Re-review: claude/galley-food 6efe188..40166d6 (0.29.32, final)

Reviewer 1, 2026-10-17. **Verdict: PASS WITH FIXES.** Every galley change in 0.29.32 is verified in the browser: both medium fixes from my last note work, and the player is served and leaves the real line correctly. The one fix is in the combine, not the galley's code: **food_check fails on galley 40166d6 + sim bfcd864**, though it passes on 40166d6 alone. All four FAIL lines have one cause: a 6-minute wait at the servery (Friday 17:22, Sunday 18:16) against food_check's `WAIT_MAX` of 5, outside any busy window. The cold store never runs short (the lowest it gets is 127). The galley and the sim engineer should settle it before 0.60.3: either the sim's 0.26.31 plan changes bunch dinner arrivals, or `WAIT_MAX` / serving needs a minute more.

Scope: the galley's own commits since my last note, 6ae14b5 and 40166d6. The 0.60.2 merge (9d0fb54) brings in content and other seats' work only; there are no section 16 lines in it. Read as `git diff 9d0fb54 40166d6`. Every changed line is in section 16, except the build line. There are no new `schedU` keys and nothing random or clock-based.

Scratch merge **M** = 40166d6 + claude/sim-engineer b9089d9 (bfcd864 plus a docs-only handover) + claude/player-needs b728101 (0.28.35). Both are full `git merge`; I resolved only the build lines, keeping the galley side for the design-doc, player_check and cadet_test text conflicts (tests not run from those). name_check on M: NAMES OK, and `node --check` parses. `--branches 6efe188 40166d6`: NAMES OK. Browser runs used my private `CADET_WORK` and browser2.lock.

## The fixes

1. **lateMeal carries `t: m`** (my finding 1). Proven on M: a 9-day jump (Day 1 06:00 straight to Day 10 10:00) posts each late meal with its own minute (`t` at 08:19 and 08:25 on the day it happened), not the jump's end (10:00). food_check on M also checks it: `your note's t 102045` (20:45, the minute you ate). The payload's `kind` is untouched.
2. **`GALLEY_QUIET`: a fresh galley's catch-up from midnight posts no late meals** (my finding 2). Proven on M:
   - **New game** (from Day 10 10:00): 0 late-meal notes in the ring, `GALLEY_QUIET = -380` (Day 0 17:40). A real late meal later still posts: one on Day 1 after the New game.
   - **A fresh first launch** (`?debug`, localStorage cleared, reload, 20 frames): Day 0 17:40, 0 late-meal notes; the ring holds only `newGame`.
   - **A fresh galley at 23:59:** posts 0.
   - food_check on M: "a fresh galley's catch-up from midnight to 20:45 posted 0".
   - **When it ends:** it's a minute threshold, set to `to` on each fresh start (no state, or time went backwards), and `galleyLate` drops only `m < GALLEY_QUIET`. So it covers exactly the replayed minutes before now. The minute `to` itself and everything after post normally.
   - It can't swallow real notes later. A sleep or Night/Day jump isn't a fresh start (`S.at <= to + 1`), so its minutes post with their own `t`. A reload mid-day restores `SHIP.galley` from the save, so there's no fresh start and `GALLEY_QUIET` stays `-Infinity`. Dropped minutes aren't added to `GALLEY_LATE`, so they don't block later posts.
   - The one case it drops: a save with no galley (pre-0.29 saves) replays its day quietly. That's correct: those minutes weren't played.
3. **`galleyBirthdays` uses `shipYearDay`** (my finding 7): on Day 0 the galley and section 18 now agree, and neither has a birthday.
4. **Tasting plates read `S.tasting.n`** (my finding 6): `galleyShow` no longer calls `galleyTasting` each frame. Old saves without `n` fall back to 20.
5. **Not done (low, as before):** `galleyFresh` doesn't see one-offs or tradition flags (my finding 5).

## The player in the real line (the coordinator's extra check, on M)
The lead's ruling is that section 16 owns the player's line membership.

Proven on M (`?nosave&debug`, Deck 3, day 2, through the real tap `playerTap(Servery)`):
- **Tap at 18:13:** you're 4th in `servLine()` (index 3), queueing. By 18:16 you've been served (`tray: "fish pie"`), you're out of the line, and nobody is stuck behind you.
- **`LINE_LOG.served` keeps growing after you're served:** 2 at 18:13, 6 at 18:16, 10 at 18:19, 20 at 18:25, 34 at 18:37. The line has emptied by 18:37 (`len` 0).

  The reported bug, where the player stays first in the line after being served and nobody else is served all evening, **does not happen on this merge**. That bug was seen on player fabc552 + sim 0cf991a. Since 40166d6, `takePortion` calls `lineLeave`, and `galleyTick` calls `galleyLeave` once section 15's `ACT` isn't a queue.
- **Tap, then walk off before reaching the line:** at 18:55 you're index 0 while walking. 3 frames later you abort (`actEnd(true)`) and you're out of the line at once (`joined: false`). 12 minutes later you're still not in it.
- Section 15 (0.28.35) still calls `lineJoin('player')` itself at the tap, as well as `galleyJoin`. That's harmless because `lineJoin` is idempotent, but under the lead's ruling the player engineer should drop it.

## Findings
1. **MEDIUM (combine, before 0.60.3): food_check FAILED on galley 40166d6 + sim b9089d9 (bfcd864), with and without player 0.28.35. It passes on 40166d6 alone.**
   - **The four FAIL lines:** `day 7: hart-ravi 18:16 waited 6 minutes`, `carts: the cold store ran short`, `spoilage: the cold store ran short with carts running`, `busy: day 7 waits {'dinner': 6}`.
   - **All four are the same 6-minute wait:** despite their wording, the two "ran short" lines fail on `wait_ok` (Friday's 6-minute wait for silva-bea at 17:22, Sunday's for hart-ravi), not on an empty store. With carts running the cold store's lowest is 127; in the broken-chiller run it falls to 1, against 9 on 40166d6 alone, but never runs out.
   - **Fix:** the galley owns food_check and the sim owns the plans. Find which bfcd864 change bunches the dinner arrivals (night workers to evening traditions, trays in the mess hall), then either spread them or raise `WAIT_MAX` to 6 with a reason in DEV_NOTES. The galley's DEV_NOTES row says food_check is OK on a trial with sim 0cf991a; that was before bfcd864.
2. **LOW, still open (from my last note):** `galleyFresh` doesn't see section 18's one-offs or tradition flags.
3. **Not a galley issue, seen while testing:** in `?debug`, a save made during the first-launch arrival (time moved to Day 9 by my probe) reloads at Day 0 17:40, with the galley's `at` from Day 9. The galley copes (time going backwards gives a quiet fresh start), but whether section 21 really should reload a mid-arrival save at 17:40 is the arrival engineer's call.

## Tests
- name_check: `--branches 6efe188 40166d6` OK; on M OK.
- food_check: **OK** on 40166d6 alone; **FAILED** on 40166d6 + sim b9089d9; **FAILED** on M (galley + sim + player), with the same four lines.
- Browser probes on M (scratchpad `g/probe.py` with `f1.js`, `f2.js`, `f3.js`, my own copy, loading my merge's build), with private `CADET_WORK=/tmp/cadet-work/rv-galwork` and browser2.lock: outputs as quoted.
- Not rerun: day_check, cadet_test, player_check (the galley reports them OK on 0.60.2 and on the sim 0cf991a trial).
