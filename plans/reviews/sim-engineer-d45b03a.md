# Review: claude/sim-engineer d45b03a (0.26.22, the ship notes bus and the flag store)

Reviewer 1, 2026-10-17. Diff: `git diff origin/claude/ship-integration...d45b03a`. Section 13 only (plus the build line): in seat.

**Verdict: PASS WITH FIXES** (1 must-fix before 0.60.0, 1 should-fix, 1 small).

## 1. MUST FIX: New game keeps the old game's flags and notes
- Path: play (or let the intro set) any flag, e.g. `flagSet('week1.done')`; tap New game twice. The handler (section 13, `newBtn.onclick`) resets time, decks, habits, needs and social, but not `SHIP.flags` or `SHIP.notes`, then calls `saveGame()`, which writes the old flags into the new save.
- Proven in the browser (`?debug`, saves on): after New game, `flag('met.calder')` and `flag('week1.done')` are still true, the new save has `flags: {"met.calder": true, "week1.done": true}`, and after a reload they're still there, with the old `introStep` note in `simNotes()`.
- Effect once wave 1a combines: a second playthrough starts with Calder already met, week 1 done, so social's week-1 gating is open on Day 0 and the arrival thinks it's over.
- Fix: in the New game handler, `SHIP.flags = {}; SHIP.notes = [];` next to `HABIT_SAVED = null`. Better still, send `simNote('newGame')` (or a `NEWGAME_EXTRA` list like `SAVE_EXTRA`) after the reset, so sections 20, 20c and 21 can reset their own state without more hook lines in section 13.

## 2. SHOULD FIX: one note with a non-JSON value stops all saving, silently, for days
- `simNote` keeps a shallow copy of `data` in `SHIP.notes`, and `saveGame` stringifies the ring inside its try/catch. If a sender passes an object instead of an id (a walker, a machine record, a person from `schedPeople()`: the appendix kinds have `who` and `machine` fields, so this is an easy slip), `JSON.stringify` throws on the cycle, the catch swallows it, and nothing is saved until that note leaves the ring. The ring only drops old notes when a new one is pushed, so on a quiet stretch that can be much longer than two ship days.
- Proven: `simNote('repair', { who: walkers[0], machine: 'oven' })` and then `saveGame()`: the stored save's clock stays at 06:00 while the game is at 10:00.
- The shallow copy also means a listener or sender that later changes a nested object rewrites the saved history.
- Fix (small): in `simNote`, `let note; try { note = JSON.parse(JSON.stringify(Object.assign({}, data, { kind, t }))); } catch (e) { return null; }` (or keep only primitives and arrays of primitives). In `?debug`, a `console.warn` names the bad kind.

## 3. Small: "any section may call these while it loads" isn't true above section 13
- `SIM_CUE` and `SIM_RING` are `const`. `SHIP` exists from section 4 (line ~493), so a load-time `simNote` from sections 1-5 gets past the `typeof SHIP` guard and then throws a ReferenceError (temporal dead zone) on `ring.length > SIM_RING`. `typeof` doesn't protect a `const` that hasn't run yet. No caller does this today; the comment and DEV_NOTES promise it's safe.
- Fix: `var SIM_CUE = 2880, SIM_RING = 200;` (like `SIM_ON`), or write the numbers inline.

## Heads-up for the next step (day 0), not this commit
- `loadGame` rejects any save with `time.day < 1` (`!(t.day >= 1 && ...)`). Once a new game starts on Day 0 at 17:40, a reload during the arrival evening throws the whole save away and starts a fresh Monday. Day 0 needs `t.day >= 0` there (and in any other check that assumes day ≥ 1, e.g. `weekday(d)` for d = 0).
- Day 0 note times are negative (`(0 - 1) * 1440 + min`). That's fine with `isFinite`, but anyone writing `if (!note.t)` or `t >= 0` will get it wrong. Worth one line in DEV_NOTES.

## Checked, fine
Listener order is fixed (registration order); unsubscribing during a dispatch is safe (`concat` copies); the depth cap works; no `R()`, `Math.random` or `Date.now`; the ring is capped at 200; flags and notes are read back defensively; `SAVE_V` unchanged; nothing runs per frame. The DEV_NOTES row matches the code.
