# Re-review: claude/social-stories 3947822..7d8be10 (0.39.22)

Reviewer 1, 2026-10-17. **Verdict: PASS.** All five fixes do what they claim, and I checked each one in the browser. A real game that starts with the day-0 arrival now saves bonds in the compact form (v:2, z:1) every day to day 280, and they load back exactly. A 0.39.21 save with no `z` loads with the right times; the offset is not applied twice. Nothing blocks the merge. Two small leftovers are below; neither needs to hold the merge.

Scope: one commit, 7d8be10. It changes `starship-cadet.html` (build line, `BOND_T0`/`BOND_H0`, `z`, `affCrewTag`, the `SOC.n > 255` guard, the `STORY_CAP` reset, the reworded comment) and adds one DEV_NOTES row. No test files changed.

## Checks (browser, `?debug` with storage on, real `saveGame`)

**(1) Offsets, from the real arrival.** I called `newGameStart(true)`, which starts at shipNow -380 (hour -7). Then I stepped `socialTo` day by day to 280, ran `saveGame()` every day and read the stored JSON.
- **All 280 daily saves were `bonds.v === 2 && z === 1`.** `bondsUnpack` of the stored part matched the live bonds exactly (sorted keys and fields), every day.
- The smallest `since` was -390 (the couples), and 4 bonds stay negative. The smallest `seen` was 13.

| day | bonds | bonds part | round trip | STORY_CAP |
|---|---|---|---|---|
| 1 | 9 | 0.16 KB | exact | 0 / 0 |
| 35 | 99 | 1.57 KB | exact | 0 / 0 |
| 140 | 168 | 2.64 KB | exact | 0 / 0 |
| 280 | 200 | 3.14 KB | exact | 0 / 0 |

- **Real reload:** I made an arrival save at day 35 and reloaded the page. The bonds were identical: v:2, z:1, and the 4 negative values survived.
- **Ranges.** Each value below went through `storyBondsPack` alone. Where it packs, I also checked the round trip.

| value | result |
|---|---|
| since -20160 | packs, exact |
| since -20161 | null |
| since 0xFFFFFF-20161 | packs, exact |
| since 0xFFFFFF-20160 | null (doesn't collide with the 0xFFFFFF "none" marker) |
| seen -336 | packs, exact |
| seen -337 | null |
| seen 0xFFFF-337 | packs, exact |
| seen 0xFFFF-336 | null |
| fractional since | null |

  Through `bondsPack`, a bond with since -30000 and seen -400 falls back to v:1 and comes back exact.
- **0.39.21 save without `z`:** I played 40 days in the real 3947822 build from a Monday start, which gives a v:2 save with no `z`. I put that save into the 0.39.22 page's storage before it loaded.
  - The real `loadGame` path gave 107 bonds identical to the old build's. The largest `since` was 56430 at shipNow 56640, so the times are not shifted.
  - Both decoded snapshots loaded.
  - The next save was `[v:2, z:1]` and decodes to the same bonds.

**(a) `affCrewTag`.** It is `(socHash(SOC.crew ids joined by ',') >>> 0).toString(36)`. That is the same hash as the save's `ids`, so it **covers the ids and their order**.
- Day-280 snapshot parts look like `38:86:n3xm4a/~...`.
- The same list keeps both weeks.
- The same 86 people reversed drops both. Swapping only the first two people also drops both.
- Restoring the list brings both back.
- If I strip the tags (the 0.39.21 `~` form), the snapshots decode the same as before.
- The old triple form can't be mistaken for a tag: base64 has no `~`, and the lookahead needs one.

**(b)** The comment now says a waking bond can take someone "one or two over" `BOND_MAX`, and the total is "about" n·14/2. That's accurate.

**(c)** With `SOC.n = 300` (forced), `storyBondsPack` returns null, so the save falls back to v:1 instead of `btoa` throwing.

**(d)** I set `STORY_CAP` to full 7, gone 3, firstFull 99, then called `newGameStart(true)` and ran 2 hours. It went back to `{0, 0, null, null}` with h -6.
- Between `newGameStart` and the first `storyHour`, it still shows the old values, which is harmless.
- A test that rewinds the clock (social_check does this with `keepS` and `setShipNow(t0)`) also clears it. That only matters if a check ever asserts on it after a rewind.

## Tests
- `name_check.py --branches 3947822 7d8be10`: 3 new names, **NAMES OK**.
- `node --check` on the main script: parses.
- `social_check.py` on 7d8be10: **SOCIAL CHECK OK**, errors [].
  - The first try timed out loading the page while the machine was busy (load about 7). The rerun passed.

## Leftovers (Low, none blocking)
1. **No test guards finding 1 yet.** social_check still starts at h0 = 6 and never asserts `bonds.v === 2`, and `STORY_CAP` is still only checked by hand. If something else stops the compact form from fitting, the save would quietly get about 2.4 KB bigger again.
   - **Suggestion:** an arrival-start (`newGameStart(true)`) step in `--long` that asserts `z === 1 && v === 2` and `STORY_CAP.full === 0 && gone === 0` at the end.
2. **Untagged 0.39.21 snapshots from a different same-size crew list are still read by position.** This is unavoidable for old saves: there is no tag to check, and `socLoad` doesn't drop `affWeek` when `!same`. It lasts at most two weeks, and only for a save made before 0.39.22 under a different roster order.
   - **Suggestion:** have `socLoad` set `affWeek: null` when `!same`. That would close it fully.
3. **Nit:** the DEV_NOTES row says "the worst whole social save with no player is 27.5 KB (day 2)". "Day 2" looks like a typo, maybe for day 242. Worth checking. For scale, my whole `saveGame` string, with every section included, was 45.7 / 71.6 / 90.0 / 88.9 KB on days 1 / 35 / 140 / 280 with no player. Most of that isn't social (the bonds part is 3.1 KB). I'm passing it on for the lead; it isn't this branch's concern.

Probe scripts: /tmp/claude-0/-home-user-cadet-game/1598d9e8-8f30-5fac-8e56-61dd4f5bfb08/scratchpad/probe.py and probe2.py (the worktree has been removed).
