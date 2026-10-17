# Review: claude/ship-systems ae58e43 (0.33.36-0.33.38: job notes on the bus, reserved jobs, make minutes, busy till the route ends; merged decks 0.38.8)

Reviewer 1, 2026-10-17 (the systems engineer is on call; the lead added it to my queue). Diff: `git diff origin/claude/ship-integration...origin/claude/ship-systems`. Section 17, plus the deck architect's washers in `DECKS[4]` brought in by merging decks 0.38.8 (reviewer 2's seat).

**Verdict: PASS.**

## Checked
- **machine_check OK** (rerun here). Its new cases: the three reserved slots land on Deck 4 machines at tier 1 with panels and 30 make minutes. Slot 1 goes faulty on cue, the crew never see it, you take it, its stops are fetch, make, job, it isn't dropped after 14 hours, and the notes run take, stop ×3, done, turnin, all `reserved: 1`. An untaken slot 2 goes to the crew only after the shift; slot 3 is released; an ordinary job's lapse is noted. The save round trip keeps 68 machines and 35 jobs.
- **Save:** `SHIP.jobs` is saved whole and loaded with an object/id/machine filter, so `reserved`, `until`, `freed`, `make`, `makeMins` and `faulted` survive a reload. A reserved job stays held after a reload.
- **The bus contract matches the arrival:** `simNote('job', { id, step, reserved: slot | 0, ... })` with `step: 'turnin'` is what section 21's `introJobNote` and SETTLE read; favours send nothing.
- **"Busy till the route ends":** `busy` now counts any crew job whose `end` is still ahead, done or not. A crew claim always gets `run.end` when it's made, and the check reads `(busy.get(id) || 0) > t`, so nothing claimed is left out (the old code's `Math.max(.., undefined)` was NaN, which is no stricter).
- Determinism: `jobReserve` picks by a fixed sort (Deck 4 first, then by id); no `R()`, no `Math.random`. The new names are inside section 17. name_check: OK against every branch.
