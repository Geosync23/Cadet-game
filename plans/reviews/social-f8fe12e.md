# Review: claude/social f8fe12e (0.36.20, the query API, inert)

Reviewer 1, 2026-10-17. Diff: `git diff origin/claude/ship-integration...origin/claude/social`. Section 20 only (plus the build line): in seat. social_check OK on the branch (re-run here).

**Verdict: PASS WITH FIXES** (two small contract fixes; neither changes play today).

## 1. SHOULD FIX: `{friend}` never fills if 20c names the bond `friends`
- `socialFill` maps `rival` to bond kind `rivals` but passes `friend` through as `friend`. The social plan (B2) and `bondOf`'s own comment name the kinds "friends, best, rivals, mentor, drifting". If social B stores `kind: 'friends'`, every line with `{friend}` is skipped without a word (a placeholder that can't be filled skips the line), and a writer's `bond:friend` condition never matches.
- Fix: freeze the bond kind strings now, in one list both A and B use (e.g. `BOND_KINDS = ['friends', 'best', 'rivals', 'mentor', 'drifting', 'couple']`), and map each placeholder explicitly (friend→friends, rival→rivals). Tell the dialogue engineer which spellings the conditions use. social_check should fill `{friend}` from a stand-in bond.

## 2. SHOULD FIX (before A6): `repBand` throws when reputation dips below 0
- `REP_BANDS.find(([v]) => repOf(dept) >= v)[1]`: the lowest band is 0, so any value below 0 (the user wants dips) gives `undefined[1]`, a TypeError inside `lineFor`'s condition check. Today `SHIP.rep` is null, so it's latent.
- Fix: `(REP_BANDS.find(...) || REP_BANDS[REP_BANDS.length - 1])[1]`, or clamp in `repOf`.

## 3. Note: `typeof VOICE` / `typeof SHIP_TRADITIONS` don't protect a `const` declared later
- `socialFill` reads `typeof VOICE !== 'undefined'` and `typeof SHIP_TRADITIONS`. If the dialogue engineer's generated block declares `const VOICE = ...` further down the file and anything calls `socialFill` while the file is still loading, it throws (temporal dead zone). Nothing calls it at load today. Agree with the dialogue engineer that the baked blocks use `var`, or sit above section 20.

## Also checked
- The query functions are pure (social_check compares `socSave()` before and after); cues are capped at 30, saved, read back defensively and expire. `relAdd`'s `tierUp` note fires only when a tier rises. The listeners register only if `onSim` exists, so the build is inert alone. No `R()`; hash keys 644-671 (none used yet).
- Test gap: the knowsNews part of social_check printed `news: null` (no known news at that moment), so `knowsNews` wasn't exercised. Seed one item first.
- `SHIP.mem` isn't saved yet. Fine until A2 writes memories; `memTold`'s mark must be saved then too.
