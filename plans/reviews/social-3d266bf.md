# Review: claude/social f8fe12e..3d266bf (0.36.21-0.36.30: memories, lineFor kinds, week 1, gifts, reputation, invitations, bunk visits, crew coming and going, the fixes)

Reviewer 1, 2026-10-17. Diff: `git diff f8fe12e origin/claude/social`. Every hunk is in section 20 (plus the build line): in seat. The 0.36.20 findings are fixed (BOND_KINDS/BOND_FILL, repBand's fallback, knowsNews tested).

**Verdict: BLOCK** until finding 1 is fixed: combined with the arrival branch, the game doesn't load. Finding 2 before combining as well.

## 1. BLOCK: `introOn` and `introNote` are declared in both section 20 and section 21
- Section 20 (0.36.23) adds `const introOn = ...` and `function introNote(d)`. Section 21 (claude/arrival, since 0.42.0) already has `const introOn` and `const introNote`. Both live in the same script scope, so a combined file is a SyntaxError and nothing runs.
- Proven: merging origin/claude/arrival into origin/claude/social (the only conflicts are the build line and the adjacent insertion point, both sides kept) gives a page that never starts. `node --check` on its script: `SyntaxError: Identifier 'introNote' has already been declared`. A name scan of every Pillar 4 branch against ship-integration finds exactly these two collisions (plus one stale one on an old branch, nothing to do with this seat).
- They also mean different things: section 21's `introOn` is `on && !ended`, so it stays on after skip-intro and the week's beats still run. Section 20's turns off on `skipped` (and on `week1.done`).
- Fix: section 21 owns `introOn` (the plan's appendix lists it there). Rename section 20's to `socIntroOn` and `socIntroNote`. Better: make `socIntroOn` call section 21's `introOn()` when `typeof introOn === 'function'`, so the two seats can't drift. Then agree, in DEV_NOTES, what skip-intro means for social: an open week, or the week as walked?

## 2. MUST FIX: social_check fails on 3d266bf itself
- Run here on the pushed build: `FAIL affBand, moodOf or purity wrong` (`"pure": false`), `SOCIAL CHECK FAILED`.
- Cause: the new knowsNews test calls `newsAdd({ id: 'test:one', ... })` after `before = JSON.stringify(socSave())` and before `out.pure`, so the check changes the state it then calls unchanged. A test bug, not a game bug. But the branch can't be combined while its own check is red.
- Fix: add the test news before taking `before` (or remove it again before `out.pure`).

## 3. SHOULD FIX: a missed arrival step still gives a core memory you never made
- Section 21 sends `introStep { step, who, missed: true }` when a step falls back. `introNote` ignores `missed` and gives `intro.arrival` or `intro.dinner` as a core memory (weight 100, never fades) to the step's person, the escort and Calder.
- Path: idle through the arrival evening (intro_check's idler). `bunk` and `chief` fall back with `missed: true`, and Torres and Calder each keep "the dinner together" / "your arrival" for good, so callback lines will talk about an evening that didn't happen.
- Fix: `if (d.missed) return;` at the top (or a sour or no memory for a missed one).

## 4. SHOULD FIX: the reserve pool in `SOC.ids` wipes every existing save's social side, once now and again with each change
- `socInit` adds `ROSTER_RESERVE` to `SOC.crew`, and `socLoad` refuses any save whose `ids` hash differs. When the crew designer's reserve lands in 0.60.0, every existing save loses all friendships, memories, news and reputation on its first load, and again every time the reserve list changes (a re-run of the generator that adds or renames one future crew member).
- `rel`, `mem`, `rep`, `bonds` and `moved` are all keyed by id already. Only the affinity array depends on the order.
- Fix: when the hash differs, keep the id-keyed parts and rebuild only `aff` (copy each pair present in both lists by id, `affStart` for new people). At the very least, say in the 0.60.0 notes that saves lose their social progress.

## 5. SHOULD FIX: the shadow-shift core memory never forms
- `INTRO_MEM` maps `d1-shadow` to `intro.shadowShift`, but section 21 sends `introStep` notes for only two week beats, `d1-briefing` and `d6-sowing` (`introAdvance`). No note for `d1-shadow` is ever sent, so the memory is dead code. Either the arrival sends `introStep` for `d1-shadow` (and `d1-lead`) when it starts, or social listens for the `job` turn-in with `reserved: 1`. Agree with the onboarding engineer and add a row to the hook register.

## Checked, fine
- **The reserve with a stand-in:** a copy of the build with one `ROSTER_RESERVE` member (`aboard: [30, null]`) runs the whole social_check with no errors: 75 crew, the same twice, two days in one jump the same as hour by hour, save and load identical. Only the purity failure above shows, the same as without the reserve. `planDay` returns `[]` for anyone without a plan, so `memRepair`, `repDeptOf` and `socInvites` are safe with people who aren't aboard.
- **Determinism:** every pick is `schedU(seed, day or hour, key)` with keys 644-664, inside social A's 644-671; no `Math.random`. `performance.now()` only times the knock prompt, as SEEK did before.
- **Save:** every new part is read back defensively (types and ids checked); memories are stored with their keys once; rings capped (cues 30, notes 10, given 20, rep notes 20, keepsakes 8). The social save is 6.7 kB of 20.
- **Phones:** the new work is in the hourly `socialHour` (memFade, gifts, invitations, transfers, the Sunday reputation) or once a ship minute (`socInviteMail`, `socialVisit`, whose crew scan runs only when its roll passes). Nothing new runs every frame.
- Small (not blocking): `socWeek(0)` is -1, so a gift given on Day 0 stores `giftWeek` 0 ("never") and the once-a-week limit doesn't hold that evening. `repWeek` also runs on Day 0 (it's a Sunday) at 04:00, before you've arrived.
