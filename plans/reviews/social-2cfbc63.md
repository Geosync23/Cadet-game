# Re-review: claude/social 0154e8d..2cfbc63 (0.36.75 + 0.36.76), the save headroom and the save bounds

Reviewer 1, 2026-10-17. **Verdict: PASS WITH FIXES.** Nothing crashes and nothing is lost on load. Old saves of every older shape load and save again unchanged. The real `saveGame()`/`loadGame()` round trip keeps cues, pair news, live heard and known the same. A jump comes out the same as hour by hour, and New game resets everything. Three things should be fixed before this is combined:
1. The size claims rest on a check every four weeks, which misses the peaks. Measured every day, the save goes over 30 KB on 8 days before day 140 and reaches 35.7 KB.
2. `knownPack` keys by position in the roster list, so a roster content update can silently swap a line the player was told for one they never heard. This is shown below with Kovac.
3. `news` has no count cap in code, and its measured size (10.3 KB) is above the worst case written in DEV_NOTES.

Scope: 0.36.75 (b6e72b5: heard, cues and pairs packed) and, at the lead's request, 0.36.76 (2cfbc63: known packed, PAIRS_MAX, MOVED_MAX, old asks dropped, `--long` to day 280). Diffs read in full (game, social_check.py, DEV_NOTES).

## Setup
- Merge 1: b6e72b5 + social-stories 0d02c21 (AFF_SNAP_MAX 600) + deck-plans-1-2-6 cadfbdd + sim-engineer 236810f.
- Merge 2: 2cfbc63 + social-stories d30b16f + deck-plans-1-2-6 + sim-engineer.
- Both merges are plain (no -X, no ship-systems). Only conflicts in the build lines were resolved. deck-plans' only conflicting side was its old `GAME_BUILD` line next to the sim bus, and we kept the bus. `player_check.py` (a conflict between sim and player, not game code) kept ours.
- `name_check.py COMBINED` on both merges: NAMES OK, the file parses. `name_check --branches 0154e8d b6e72b5`: OK. `--branches 0154e8d 2cfbc63`: OK.
- Our private CADET_WORK is `/tmp/cadet-work/rv-socA75work`. Worktrees: `/tmp/cadet-work/rv-socA75m` (merge 1) and `/tmp/cadet-work/rv-socA75n` (merge 2).

## Findings, most severe first

### 1. MEDIUM: the 30 KB / 40 KB claims rest on a check every four weeks; the real peaks are higher
- **Path:** `social_check.py --long` measures `socSave()` only at days 28, 56, 84 and so on. `news` swings from 1.3 KB to 10.3 KB from one day to the next, depending on what's going round, so the check every four weeks lands wherever the swing happens to be.
- **Evidence:** we ran the same `--long` run with `socSave()` measured every day at 23:00. The scripts are `scratchpad/long280.py` (merge 1) and `scratchpad/long276.py` (merge 2), and the daily data is in `daily280.json` / `daily276.json`.
  - Merge 1 (0.36.75), the official `--long` (140 days): day 140 = **29,088 B**, OK, so the claimed margin of about 0.5 KB holds. Measured every day, though, 13 days before day 140 are over 30,000 B (max **32,002 B on day 115**). Past day 140, the save reaches **35,947 B (day 242)** and is 31,094 B at day 280.
  - Merge 2 (0.36.76), its own `--long` (280 days): "SOCIAL LONG CHECK OK". Day 140 = **28,454 B** (claimed 28.6 KB, which matches). Measured every day, 8 days before day 140 are over 30 KB (73, 74, 115, 129, 130, 137, 138, 139; max **31,355 B on day 115**). From day 150 on, most days are over 30 KB. The peak is **35,677 B on day 242**, not the 31.5 KB in DEV_NOTES. It never reaches 40 KB: the closest day is 4.3 KB short.
  - Largest size of each part over 280 days (merge 2): news 10,291 (day 19), bonds 5,586, rel 4,715, cues 3,225, affWeek 2,749, heard 2,583, rep 2,362, pairs 1,237, aff 4,878 (fixed).
- **Under the lead's rule:**
  - "Under 40 KB at any length" holds (35.7 KB).
  - "At most 30 KB at day 140" holds on day 140 itself, but not on 8 earlier days. If the rule means "by day 140", it fails by 1.4 KB.
  - The worst case for `news` written in DEV_NOTES ("worst about 8 KB") is below what we measured: 10.3 KB on day 19.
- **Fix:**
  - In `--long`, measure the size every day (calling `socSave()` once a ship day costs little), and fail on the largest size over days 1-140 (> SAVE_MAX) and over days 1-280 (>= LONG_MAX). Report the peak day.
  - Give `news` a real cap. Two ways: a count cap such as NEWS_MAX of 24, dropping the lowest weight first then the oldest, decided by a fixed rule so it stays deterministic; or keep at most 2 lines a saved item. Then correct the DEV_NOTES worst cases and the "peak 31.5 KB" line.

### 2. MEDIUM-LOW: `knownPack` stores roster lines by their position, so a roster update swaps what you "know"
- **Path:** `knownPack` saves an `about` or `life` line as `#a<i>` / `#l<i>`, and `knownUnpack` reads back whatever text is now at index i. The crew designer rewrites `about` lines in place: deck-plans 57b0089 rewrote all five of Kovac's about lines, with different facts at the same positions. After an update like that, a save made before it loads with the player "knowing" a different fact, one never told. The Crew app shows it (`knowSections`), and the line actually told now counts as untold.
- **Evidence:** probe E on merge 2 (`scratchpad/E.json`):
  - Told Kovac's `about[2]` "Bolts breakfast to get to the garden; her beans are the tidiest rows there." It was packed as `#a2`.
  - One line was then moved down (`about[2]` and `about[3]` swapped), and the save loaded.
  - Result: `known` = "Browses the crew store for wool; never buys the first ball she likes." That line was never told.
  - Before 0.36.76, the raw text was kept: at worst stale wording, never a different fact. We found no reordering in the current roster history (0154e8d to deck-plans tip: 755 lines the same, 7 edited, 0 moved). Edits made at the same position, as in 57b0089, already give a different fact.
  - Nothing checks the tier on load. A line gated to a higher tier that moves into a told position would show early.
- **Fix:** key by a short hash of the text, for example `'#' + socHash(text).toString(36)`, which is 6-7 characters instead of 3-4. When no current line matches on load, either keep nothing (the line can be told again) or keep the text as it was before. Old saves (raw text) still load, as they do now.

### 3. LOW: trimming `heard` changes who tells you what when a news id comes round again
- **Path:** `playerHeard` skips a news item if `SHIP.heard` holds the same id. Some ids repeat:
  - `friends:<a>:<b>`: friends, then rivals (`pairs` goes `'r'`), then friends again;
  - `rivals:`;
  - `leaving:` and `arriving:<id>` for someone who comes back.

  In memory, `heard` keeps 60 entries. After a reload it keeps only the live ones plus the latest 12 older ones (`HEARD_FEED`), so the old entry is gone. The claim "picks never change" therefore only holds when ids never repeat.
- **Evidence:** probe B on merge 1 (`scratchpad/B.json`). We heard `friends:tomas:pell`, it expired, and 14 more entries followed. Then the same id became news again:
  - in memory: `heardNow: false, pts +0`;
  - after `saveGame` and a reload: `heardNow: true, pts +1.2`.

  social_check's "In memory the same after a save" compares only the live heard entries, so it can't see this.
- **Fix:** in `playerHeard`, skip only if the same news was heard since it was born: `SHIP.heard.some(x => x.id === newsId && x.at >= it.born)`. This also fixes a bug that happens without any reload: today a pair's second friendship is never news to you.

### 4. LOW (from before 0.36.75, carried into the new string form): `pairs` is keyed by crew position and isn't moved across for a different crew list
- **Path:** the keys are `i-j`, positions in `SOC.crew`. When a save comes from a different crew list (`!same`), `socLoad` moves `aff` (by `idl`), `knows` and `bonds` across by id, but `pairs` keeps the old positions. Ids with `-` (122 of 147 roster ids, for example `torres-zeke`) are harmless here, because the keys are numbers. No roster id contains `,` or `:`.
- **Evidence:** probe E with the save's crew list reversed: `0-1f` was meant for castellano-jem / juarez-nell and now applies to marrow / vance (`affMovedById: true`, `pairs: {"0-1":"f"}`). The effect: news for the wrong pair is held back, or comes twice. The upgrade tests below didn't hit this, because 0.36.66 to 0.36.76 all have the same 86-person list.
- **Fix:** in `socLoad`, when `old`, change each key to `SOC.idx.get(old[i])` and `SOC.idx.get(old[j])`, put the smaller first, drop pairs that are gone, and keep the order.

### 5. LOW: `socTrim` keeps the first-told pairs as "oldest", not the least recent
- **Path:** setting `P[key] = 'r'` on a key that exists doesn't move it in the key order, so "the 300 newest" really means "the 300 first told after the oldest". A pair that turned to rivals yesterday can be dropped first.
- **Evidence:** probe E with 310 keys: the first key, changed to `'r'` last, was dropped (`firstKeptStill: false`). The order does survive a save and load (`sameOrderAfterLoad: true`). The only reader is the guard against repeat news (`socialHour`, `feudTalk`), so the effect is at most one repeated "best of friends now" news. The trim never runs in 280 days (184 pairs at day 280), so `--long` doesn't exercise it. Jump vs live: `socTrim` runs from `socialHour` at 04:00 on both paths, and the jump test passes.
- **Fix:** `delete P[key]` before setting it again, in the two places that write.

### 6. LOW: the Ship app's feed shrinks on reload
- `newsFeed()` showed 60 entries before `saveGame` and a reload, and 28 after (probe A). The design ("12 for the feed") is fine, but play and reload disagree until 60 new items arrive.
- **Fix:** apply the same rule in memory (trim the older entries to HEARD_FEED in `playerHeard`), so the session and the save agree. This also makes finding 3's skip check behave the same both ways.

### 7. INFO: `moved` 24 and `seekAsks`
- `moved` only gets leavers. By day 245 the rotations have 13 leavers, so `MOVED_MAX` 24 won't trigger before about day 400. When it does, the oldest leavers stop sending letters and drop out of `movedOff` / `movedOn`, with no re-processing, because the check for the day only matters on the day they leave. That's acceptable. A friend's letters could be kept by trimming entries with `next == null` first.
- `seekAsks`: dropping asks that ended over a day ago loses nothing, because `seekAskFor` needs `t < until`. The trim only runs when a new ask is added (section 21's first week), so it's bounded by what section 21 adds.

## The lead's long-play rule: bounds per saved structure (merge 2, n = SOC.n = 86)
| Part | Bound in code? | Worst case / measured max |
| --- | --- | --- |
| aff | yes, n(n-1)/2 | 4,878 B fixed |
| ids/idl | yes, crew list | about 1 KB fixed |
| rel (+ known) | yes, at most n; known at most about+life+keys | 4,715 B at day 280 (still growing) |
| mem | yes, MEM_MAX 8 a person | under 0.5 KB in play |
| **news** | **no count cap, life ≤ 10 days only** | **10,291 B (day 19); DEV_NOTES says worst about 8 KB** |
| heard | yes, 60 in memory; live + 12 saved | 2,583 B |
| cues | yes, 30 | 3,225 B |
| pairs | yes, PAIRS_MAX 300 (0.36.76; before that only n²) | 1,237 B (184 pairs) |
| fault / feuds / courtesy | machines / 3 days / fixed keys | small |
| mail / invites / notes / given / keepsakes | delivered / 7 days / 10 / 20 / 8 | small |
| moved | yes, MOVED_MAX 24 (0.36.76) | small |
| seekAsks | dropped a day after they end, when a new one is added | small |
| rep | bounded by departments and keys | 2,362 B |
| bonds / affWeek / stories (20c) | affWeek AFF_SNAP_MAX 600; bonds only by pairs at the thresholds (no hard cap) | 5,586 / 2,749 / 2 B |

The `--long` in 0.36.76 does run to day 280 and fails at 40 KB, but only checks every four weeks (finding 1). bonds is social B's and still grows (5.6 KB at day 280), so its bound should be confirmed in B's notes.

## Other attacks that came up clean
- **The real save path** (probe A, merge 1, `?debug`, intro skipped, 30 days with a listener who hears everything): `saveGame` then a reload gave cues, pairs and live heard identical (`memSame: true`). The time came back right. No heard entry had a null line. The cue keys came back in the original order (`key,at,until,you,deck,who,dept,room`, the same as the push in `socNote`). A second save and reload gave an identical `socSave()`. The first reload differs only in `news` knowers and `noteq`, because the probe drives the hours on paper without the machines, so section 17 catches up on load. That comes from the probe, not this build.
- **A heard item whose news is gone:** a live item's line comes from the save's own `news` (saved with all its lines). `heard.line` is always `lines[0]` (`playerHeard`), so a content update can't lose it. A live entry would only get a null line if the save's news were dropped (no `idl` and a different crew list), which only applies to saves from before `idl`, and those use the object form anyway.
- **Old saves** (probe D): saves made by 0.36.66 (131f747, bonds as an object), 0.36.67 (9c16a83, bonds packed), 0.36.73 (1e8f091), 0.36.74 (0154e8d) and 0.36.75, then opened in merge 1: every one loaded (`hour` kept). Heard, pairs, cues and bonds counts matched, with no null lines. Saving again and reloading changed no part.
- **New game** (`newGameStart()`): heard 0, pairs 0, cues 0, news 0.
- **Determinism / jump:** social_check (14 days) on both merges was SOCIAL CHECK OK: the same twice, a two-day jump the same as hour by hour, the query API pure, in memory the same after a save (with known on 0.36.76). The JSON order of cues is rebuilt exactly. pairs keep their order (the keys aren't integer-like, so object order is insertion order).
- **Readers of heard** besides the "still live" checks: `newsFeed` (the Ship app) reads old entries' `line` and `kind` only for display. `heard` is used as a Set only against live `NEWS` ids (lines 26645, 26938, 27085) and in `playerHeard`'s skip check (finding 3). Memories don't read heard.

## Tests run
- `social_check.py --long` on merge 1: day 140 = 29,088 B, OK.
- Measured every day, 280 days: merge 1 peak 35,947 B (day 242), merge 2 peak 35,677 B (day 242). Merge 2's own `--long` was OK (day 140 28,454 B, day 280 30,959 B).
- `social_check.py` (14 days) on both merges: OK.
- `name_check` on both merges and on `--branches 0154e8d b6e72b5` / `0154e8d 2cfbc63`: OK.
- Probes A, B, D, E (`scratchpad/probe.py`, plans `A.json`, `B.json`, `D.json`, `E.json`, made by `mk.py`).
- Not run: cadet_test / deck_check / day_check. No drawing or schedule code changed, and the helper reports ALL IDENTICAL against 0.36.75.
