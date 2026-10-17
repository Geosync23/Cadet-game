# Review: claude/player-needs 1c735bb..5e61e12 (0.28.28-0.28.29)

Reviewer 1, 2026-10-17. **Verdict: PASS WITH FIXES** (one real bug, New game during or after the arrival dinner; the rest are small)

Scope: a759778 `playerSitNear`/`dinnerTick`, f4afd8f `introSeat('you')`, two player_check commits, DEV_NOTES (0.28.28); 5e61e12 lying in your bunk (0.28.29). Every changed game line is in section 15, apart from the build line.

Set-up: worktree at 3713f20, then at 5e61e12. Scratch merge: worktree at origin/claude/arrival b4f0ac4, with full merges of origin/claude/sim-engineer 971b4c7, origin/claude/deck-plans-1-2-6 4613d43, then player 3713f20 and 5e61e12. I kept HEAD's build lines, kept both sides of DEV_NOTES, and took the `.nf` superset in cadet_test's style line. Nothing else conflicted. Browser checks used cadet_test.py's `Game` with `?nosave&debug`, or `?debug` for the reload test.

## Findings (most severe first)

### 1. New game doesn't reset `DINNER_SAT`, so a second arrival never seats you (medium)
`DINNER_SAT` is a page-level `let` that is set once and cleared only by a page reload. Nothing resets it: `playerNew()` doesn't, and there is no `onSim('newGame')` listener. Path to the bug: play the arrival, sit at dinner, then press New game (arriving) in the same page. At the second dinner you stand at the table and are never seated.

Evidence (merge, `dinner2.py ... newgame`: follow Torres to the Chief's step, walk for real to [28,1], then `newGameStart(true)` and do it all again):
```
A ... "me": [28, 1], "act": ["sit", "do", "3-mess-10"], "sat": true ...
after the dinner, New game: DINNER_SAT = True
second arrival at chief, walking [28, 1]
B ... "me": [28, 1], "act": null, "sat": true, "seats": {"3-mess-9": null, "3-mess-10": null, "3-mess-12": "torres-zeke"}, "path": 0
```
At the end of run B you stand idle on the checkpoint, your seat is free, and nobody seats you.
**Fix:** add `DINNER_SAT = false;` to `playerNew()`.

### 2. A reload during the dinner seats you again, in a different seat (low)
`DINNER_SAT` isn't saved. Get up from the table (tap anywhere), let the game save, then reload while still within the Chief's step. You are sat down again without asking. In the probe it was also not your seat: 3-mess-8, although 3-mess-10 showed as free.

Evidence (merge, `?debug`, `dinner2.py ... reload`):
```
A ... "act": ["sit", "do", "3-mess-10"] ...
got up; saving: chief
R {"t": "Day 0, Sunday 18:22", ... "me": [27, 1], "act": ["sit", "walk", "3-mess-8"], "sat": true, "seats": {"3-mess-9": null, "3-mess-10": null, ...}}
```
I didn't pin down why the own-seat branch was skipped on the first frame after loading. My guess is that `heldBy('3-mess-10')` briefly saw a crew goal while the crew were being laid out again.
**Fix:** keep the flag in the save (e.g. `save.player.dinnerSat`, or a `SHIP.intro` flag), or only auto-seat when the step became yours in this page session. Then make sure the own-seat branch wins once the crew have settled, for example by waiting a ship minute after a load.

### 3. `dinnerTick` allocates every frame when no seat near the table is free (low, phones)
When the own seat is held, or missing, `dinnerTick` falls through to `playerSitNear`, which runs `[...PLACE_OF.values()].filter().map().filter().sort()`. When it finds nothing it returns false, `DINNER_SAT` stays false, and it runs again on the next frame. That repeats every frame while you stand idle within 3 m of the checkpoint, for the whole Chief's step plus 30 minutes. `cellPos(...cp.tile)` also builds a new Vector3 every frame while you're on Deck 3 during that window.
**Fix:** try at most once a ship minute (keep the minute of the last try), and reuse one vector.

### 4. Lying down by day, then staying in bed past 20:00, never sleeps you (low, UX)
`bunkLie` decides `sleep: bedtime()` once, at the tap. If you lie down at 19:50 and stay, you're still awake in bed at 20:15 and later. You have to get up and tap the bunk again.

Evidence (merge 5e61e12, `bunk.py`):
```
1 lying at 19:50: ['Day 1, Monday 19:51', 'lie', 'do', False, 99.9, 4, False]
1 after ~20:00: ['Day 1, Monday 20:15', 'lie', 'do', False, 100, 4, False]
```
**Fix:** in `bunkSleep`, read `bedtime()` live (`A.kind === 'lie' && !A.o.slept && bedtime()`) instead of the flag set at the tap. Waking at 06:00 still lying is fine, because `slept` stops it sleeping again.

## Checked and fine
- **section 21's `introSeat('you')`:** it exists on origin/claude/arrival (b4f0ac4, later d24b017) as a function declaration, `function introSeat(who)`. It returns a place id string (`'3-mess-10'`) or null, only during the 'chief' and 'free' steps. Every section 21 name that `dinnerTick` reads (`introOn`, `introStepById`, `introSeat`) is `typeof`-guarded. `introOn` and `introStepById` are `const` arrow functions declared at about line 14946, after section 15. They are only read from `playerUpdate`, which section 12's loop calls after the whole script has run, so they're never read in the temporal dead zone. On the branch alone (no section 21), `dinnerTick` returns at `typeof introOn !== 'function'`, and player_check prints `[False, [28, 2], None] ['sit', 'do', '3-mess-10', True, None]`.
- **The real arrival dinner on the merge:** you're seated in 3-mess-10, beside Torres in 3-mess-12, and nobody else holds or heads for 3-mess-10 from 18:12 to the end of the run (`dinner.py`, `dinner2.py base`, screenshot `scratchpad/rv/dinner-base.png`). Mid-walk you aren't seated: `player.path.length` is 1 on [28,2], and you sit once you arrive at [28,1]. On another deck it returns at `deckDef.num !== cp.deck`. Day 0 maths: `shipNow() - done` subtracts two negative numbers, which is fine.
- **The test loosening (ae24d71, 850c56a):** in the real merged play nobody targets 3-mess-10 (above), so the clause `or dn0[2]` isn't hiding a double booking in the real evening. It only covers player_check's own jump to 18:31, where crew are mid-plan. The test still checks for a `sit` in a `3-mess` seat, at `do`, with `DINNER_SAT` set. Note that nothing in section 14 reserves 3-mess-10 for you: `introPlan` blocks only the cast's seats. If a later roster or seed puts someone's dinner there, you'd fall back to the nearest free seat, which is the intended behaviour.
- **Lying (0.28.29):** your bunk only. `playerBed()` is `ROSTER_PLAYER.bed` (`4-B1-4`, a const). Bed places are never handed out to the crew. `ROSTER_ROTATIONS` arrivals take the leaver's bed, and nobody leaves 4-B1-4, so day 35 can't give it away. The upper or lower bunk on the same tile, 4-B1-3, is Santos's. The sleep fade and skip keep the `lie` activity, and you wake at 06:00 still lying with energy 100 (player_check). New game while lying, both kinds, clears the activity and shows your Walker again, with no errors (`bunk.py` 3). Reloading while lying brings you back standing, because activities aren't saved; that's acceptable. Energy while lying: no drain, +3 an hour (50 -> 53.0). The `SIM_ADVANCE` change keeps only `lie`.
- **Determinism:** none of the new code uses `R()`, `Math.random` or `Date.now`.

## Tests
- `name_check --branches 1c735bb 3713f20`: NAMES OK (5 new names). `--branches 3713f20 5e61e12`: NAMES OK (3). Merge html: NAMES OK, node --check parses.
- player_check on 3713f20: PLAYER CHECK OK. On 5e61e12: PLAYER CHECK OK (lying by day, walking off, 21:00 to 06:00 still lying).
- interactions_check on 5e61e12: INTERACTIONS CHECK OK.
- Merge (arrival + sim + deck-plans + player): the real arrival dinner played in the browser (above). intro_check on the merge with player 1d647a3: everything passes except "the Monday briefing did not play" (part 10). That merge has extra player commits; I'm checking it against arrival alone (see the 1d647a3/fabc552 note).
