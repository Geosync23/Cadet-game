# Re-review: claude/social-stories 0d02c21..3947822 (0.39.21), packed saves

Reviewer 1, 2026-10-17. **Verdict: PASS WITH FIXES.** The packed forms are lossless. Every out-of-range value falls back to social A's v:1 form; nothing is clamped or wrapped. Old saves load and re-save, a time jump matches hour by hour for this branch's parts, and the caps never bind in 280 days.

There is one medium fix. A real game starts with the day-0 arrival, and in that game the compact bond form is **never used**. The couples' `since` is negative, so `storyBondsPack` returns null on every save, for good. That one problem explains social A's review seeing bonds at 5.6 KB and still growing. It also makes the social save peak at 35.6 KB, against 33.4 KB with the packed form.

Scope checked:
- The merges 4a50ff3 and c7f4ded only change build lines. I redid both merges from their parents and diffed against the commits: the only differences were the two build-line conflicts.
- The game changes are d30b16f and 7d077b2 (`affWeek` '~' form, `storyBondsPack`/`storyBondsUnpack`, `BOND_MAX`/`BOND_GONE_MAX`/`STORY_CAP`).
- 3947822 is the DEV_NOTES row.

Test merge (`/tmp/cadet-work/rv-socB21x`): origin/claude/social tip, then 3947822, then origin/claude/deck-plans-1-2-6, then origin/claude/sim-engineer. These were plain merges. The only conflicts in `starship-cadet.html` were build lines. **Note for the build master:** social and sim-engineer also conflict in `player_check.py` (the washer-tap check). That is a test file and not this branch's concern; I didn't resolve it.

## Findings

### 1. Medium: a game that starts with the arrival never saves bonds in the compact form (since < 0), so the save is about 2.4 KB bigger
**Path:** first launch, or New game, then "Arrive by shuttle". The game starts on day 0 at about 17:40, so `shipNow()` is -380 and the social hour is -7. The first `storyHour` forms the roster's couples with `since = h*60+30 = -390`. `storyBondsPack` treats any negative `since` (or `seen`, or `gone` 0) as "not a shape this form holds" and returns null for the **whole** map. `bondsPack` then falls back to v:1. Couples never end, so every later save is v:1 too.

**Evidence (browser, `?debug` with storage on, real `saveGame()`):**
- After the arrival, 30 days, `saveGame()`, a reload and another save: `savedForm: 1, resave: 1`. Four couples had since -390.
- After New game, then "Skip to Monday" (`newGameStart(false)`), the same steps give `savedForm: 2, resave: 2`.
- Measured every day to day 280 with social_check's long-play driver (the stand-in player):

| start | worst day ≤ 140 | day 140 | worst day ≤ 280 | bonds at day 252 / 266 | bond form |
|---|---|---|---|---|---|
| 06:00 day 1 (social_check's h0 = 6) | 29.8 KB (day 115) | 26.7 KB | 33.4 KB (day 242) | 3.1 / 3.15 KB | v:2 |
| day-0 arrival (h0 = -7, the real start) | **31.4 KB (day 130)** | 28.7 KB | **35.6 KB (day 242)** | 5.5 / 5.56 KB | v:1 |

- With the arrival start, the save is over 30 KB on 10+ days before day 140 (74, 101, 102, 115, 116, 123, 129, 130, 137, 138 ...).
- The rule is checked only on day 140, so it still passes. But the headroom under 40 KB is down to 4.4 KB.
- social_check `--long` starts at h0 = 6, so it can't see this. Every-28-days sampling also misses the peaks (day 115 and day 242), as the coordinator said.
- DEV_NOTES' worst case for bonds (602 × 16 chars, about 9.7 KB) assumes v:2. In v:1, a bond costs about 28 bytes, so the worst case in real play is about 17 KB.

**Fix:**
- Store `since` with a bias in its 3 bytes, for example `since + 0x10000` (day 0 is never earlier than -1440), and `seen` with a bias too (hours ≥ -24).
- Let `gone` 0 mean none, as it already does on unpack. A gone of 0 can come from `day = 0` in `storyHour`; see the side note.
- Then give `social_check --long` an arrival start (h0 = -7), or a check that `bonds.v === 2`. Better still, sample the size every day and report the worst day, not just every 28th.

Side note (Low, existing behaviour): `storyHour`'s `day` is 0 for hours -24..-1. `if (!B[k].gone) B[k].gone = day` then sets `gone = 0`, which reads as not gone. So a bond with someone who isn't aboard on day 0 is only frozen from day 1.

### 2. Low (existing behaviour, asked): the weekly snapshot is decoded by roster position, so a save from a different crew list with the same count gives wrong pairs silently
**Path:** `affWeeks()` only checks `+m[2] === SOC.n`. `socLoad` keeps `affWeek` as it is, even when `s.ids !== socHash(SOC.ids)`; it moves `aff`, the news and bonds across by id (`idl`), but not the snapshot. The old triple form had the same problem.

**Evidence:** I took the day-70 save and re-encoded it as if a build had listed the same 86 people in reverse order: `aff`, `affWeek` (bit form) and `idl` all in that order. `socLoad` moved `aff` across correctly (`affSame: true`). But the snapshots decoded **384 of 391** (week 9) and **410 of 418** (week 10) pairs onto the wrong people. For the first 15 pairs, `affPlanWeek` on day 71 gave `0,0,…` instead of `90,32,0…`. It recovers on its own within two weeks.

A different count (a person added or removed) is safe: the snapshot is dropped.

**Fix:** in `socLoad`, when the save isn't `same`, either set `affWeek: null` (plans fall back to the starting affinity until the next Monday), or decode each part using the save's `idl` and re-encode it. The bit form makes the second easy, since bit q is pair (i, j) of the old list.

### 3. Low: `BOND_MAX` isn't a per-person limit once people come back; the total bound still holds
**Path:** a person with 10 active bonds. One of their friends moves on (the bond is marked gone), they make a new bond (back to 10), and then the friend returns. The gone bond wakes, and they have **11** active bonds.

**Evidence (forced, on the merge):** Calder had 10 active bonds. A new 80-affinity pair was refused (`STORY_CAP.full` +1). One friend left (`p.aboard` window) and the new bond formed (10). The friend returned and Calder had 11 active.

What does hold: a new bond needs fewer than 10 active, and someone aboard keeps at most 4 frozen bonds after each hour's trim. So active + frozen ≤ 14 for everyone at all times, and the total is ≤ 14n/2 = 602, as DEV_NOTES says.

When the cap binds, **no bond is dropped**. The new one waits, decided by loop order, which is deterministic. `BOND_GONE_MAX` drops the oldest frozen bond first, ties broken by key, also deterministic.

**Fix:** reword the code comment and the DEV_NOTES row: "a new bond waits while either has 10 active (returning bonds can take someone to 14); at most 14 a person, 602 in all".

### 4. Low: crew indexes are packed as single bytes; more than 256 people would stop saving silently
`storyBondsPack` writes `String.fromCharCode(i, j, ki)`. Above 255, `btoa` throws `InvalidCharacterError` (confirmed in the page), which takes down `socSave` and then `saveGame`. `saveGame` swallows the error, so the game would silently stop saving. With n = 86 this can't happen today. The old triple affWeek form had the same limit; the new bit form doesn't.

**Fix:** `if (i > 255 || j > 255) return null;` (falls back to v:1).

### 5. Low: no test checks the "never binds" claim; `STORY_CAP` counts tries, not bonds
- `STORY_CAP` isn't read by social_check or any other check. The "neither binds in 280 days" claim was a one-off measurement.
- `full` counts every refused try in every hour, so one waiting bond adds up to 24 a day.
- New game doesn't reset it (it carried `full: 1` over in my probe). It's a debug counter and isn't saved, so this is harmless.

My probe on the merge (no player, h0 = 6, 280 days, checked every day):
- `STORY_CAP` stayed `{full: 0, gone: 0}`, and also with the stand-in player from both starts.
- The most active bonds anyone had was 8 (sato, day 154); DEV_NOTES says 9 on the branch alone.
- The most frozen bonds anyone aboard had was 2.
- The most bonds in all was 196.

**Fix:** have social_check `--long` assert `STORY_CAP.full === 0 && STORY_CAP.gone === 0`, plus the per-person maximums, at the end of the run.

### 6. Nits
- In `storyBondsUnpack`, an `x` entry is applied after the packed fields, so a hand-edited save could change `kind` (`x: [[0, {kind: 'rivals'}]]` turned friends into rivals). It only affects a hand-edited save.
- A bond with `since: null` (or NaN) loads back without `since`. This matches v:1.

## Tests (all on the merge unless noted)
- **Merges:** I redid 4a50ff3 and c7f4ded myself; only the two build-line conflicts differ from the commits.
- **name_check:** `--branches 0d02c21 3947822`: 14 new names, NAMES OK. On the merge: NAMES OK, `node --check` parses.
- **social_check `--long` (social A's copy):** SOCIAL LONG CHECK OK.
  - Every 28 days: 22.7, 24.8, 23.9, 26.8, **26.7 (day 140)**, 26.4, 31.6, 30.4, 29.0, 28.5 KB.
  - Every day, from social_check's start: worst ≤ 140 is 29.8 KB (day 115), worst ≤ 280 is 33.4 KB (day 242).
  - Every day, from the arrival start: 31.4 KB (day 130) and 35.6 KB (day 242). See finding 1.
- **Pack edge cases:** each of these makes `storyBondsPack` return null, `bondsPack` then gives v:1, and the bond loads back exactly:
  - negative, fractional and 0xFFFFFF `since`
  - `peak` -128, 200 and 61.5
  - `seen` 70000 and -1
  - `gone` 0 and 70000
  - `spar` false and 1

  Other cases:
  - Extra fields (string, nested object) go into `x` and round-trip.
  - A bond whose id isn't in the roster is skipped, and the `x` rows still line up.
  - Bad base64 or a cut-off record loads as `{}`.
  - An unknown kind is dropped.
- **Daily pack round trip:** packing then unpacking was identical every day to day 280, and never fell back to v:1 from social_check's start.
- **Old forms:**
  - The `[i, j, v]` affWeek triples decode identically.
  - A's v:1 bonds and the object form load identically and re-save as v:2.
  - Day-70 sizes: bonds v:2 2.1 KB, v:1 3.3 KB, object 10.0 KB; affWeek bit form 2.3 KB, triples 3.2 KB.
- **Upgrade, real `saveGame`/`loadGame` (`?debug`):** played 40 days in 0d02c21 (0.39.20), then opened the merge on the same storage. Bonds and the decoded snapshots were identical, and the first save afterwards was v:2.
- **Jump vs hour by hour:** day 70 to 84 in one `socialTo` jump vs hourly: `bonds` and `affWeek` were byte-identical. For the lead: `cues`, `rep` and `noteq` differed. Those are social A's parts, from a bare driver without `tickShip` stubbed, so not attributed and not this branch's.
- **New game:** bonds `{}`, `affWeek` null, `stories` `{}` (`STORY_CAP` not reset; see finding 5).

## Social B's save parts and their bounds

| Part | Hard bound by design | Worst case (n = 86) | Measured (stand-in player, every day to 280) |
|---|---|---|---|
| `affWeek` | 2 weeks; each base64(ceil(n(n-1)/16) bit bytes + ≤ `AFF_SNAP_MAX` 600 values); dropped when n changes (not when the order changes: finding 2) | about 2.9 KB | max 2.76 KB |
| `bonds` v:2 | ≤ 14 a person (10 active to start a new one + 4 frozen; returns can make up to 14 active), ≤ 602 in all; 16 base64 chars each + `x` | about 9.7 KB | 3.15 KB, 196 bonds at day 280 (growth slowing: 169 at 140) |
| `bonds` v:1 (what the arrival start gets today: finding 1) | same count; about 28 bytes a bond | **about 17 KB** | 5.56 KB at day 266, still creeping up |
| `stories.m` | one record per person who had a moment (about 65 B) | about 5.6 KB | not in the top 6 parts |
| `stories.serious` / `home` (4 contacts, words bounded by the call files' lines) / flags | design-bounded by content | about 2.5 KB | not in the top 6 parts |
| `STORY_CAP` | not saved | 0 | n/a |

With finding 1 fixed, the real game's bonds drop to the v:2 numbers. The worst day to 280 then goes from about 35.6 to about 33.4 KB.
