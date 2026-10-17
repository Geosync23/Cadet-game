# Re-review: claude/social 2cfbc63..a033f17 (0.36.77-0.36.78)

Reviewer 1, 2026-10-17. **Verdict: PASS (with notes).** All four claimed fixes hold in the browser, and the size rule holds when the save is measured every day from the real Day 0 arrival. The worst day to 140 is 29,700 B, 300 B under 30 KB. The worst day to 280 is 32,821 B. Nothing here blocks combining. Two things are worth doing soon: the 300 B headroom is thin, and the DEV_NOTES worst case for `news` is lower than the cap really allows (finding 1). The point about the feed shrinking on reload (old finding 6) is still open, but in play it is only a constructed case (finding 2).

Scope: a033f17 (0.36.78) and 4686a3a (0.36.77). I read the game diff, social_check and DEV_NOTES in full. At the coordinator's request I also ran social A's test-only commit 8c9b52f (`--long` from the arrival).

## Setup
- Merge: social a033f17, then social-stories 7d8be10, then deck-plans-1-2-6 55e98e7, then sim-engineer 7c1feea. All plain merges (no -X, no ship-systems). The only conflicts were in the build lines (kept 0.36.78). `player_check.py` kept ours. Worktree: `/tmp/cadet-work/rv-socA78m`.
- To make a 0.36.76 save, a second merge: 2cfbc63, then the same three branches (social-stories fast-forwards over 2cfbc63, so it keeps the old `#a`/`#l` knownPack). Worktree: `/tmp/cadet-work/rv-socA78old`. Both have the same 147-person roster.
- Probes are in `/tmp/cadet-work/rv-socA78tools` (`probes.py`, `probes2.py`, `probes5.py`, `probes6.py`, `probes7.py`, `long_arrival.py`, `long_big.py`), with results in `P12.json`, `P3.json`, `asis.json` and `day1.json`. The private CADET_WORK is `/tmp/cadet-work/rv-socA78work`.
- Checks:
  - `name_check --branches 2cfbc63 a033f17`: NAMES OK.
  - `name_check` on the merge: NAMES OK, the file parses.
  - `social_check` (14 days) on a033f17 alone: SOCIAL CHECK OK (18,759 B). On the merge: SOCIAL CHECK OK (18,995 B), including the new "Reviewer 1's save notes" block.

## The claims, checked
1. **Daily `--long`, NEWS_MAX, no `seed`, CUE_MAX: holds.**
   - a033f17's `--long` measures every day at 23:00 and fails on the worst day to 140 (> 30,000) and to 280 (>= 40,000). It started at Day 1 06:00 (`socReset(6)`), **not** at the arrival. 8c9b52f fixes that: `newGameStart(true)`, `socHr` for the negative Day 0 hours, and week 1 marked done on day 8.
   - Run on this merge, 8c9b52f's `--long` matches social A's figures exactly: worst day to 140 = **day 138, 29,700 B**; worst day 141-280 = **day 244, 32,821 B**.
   - Its exit code is still FAILED, but only because of the new arrival jump check: section 17 sends 4 extra notes in the jump, which shows up in `noteq` (the sim's, as the coordinator said). The size part passes.
   - `seed` is never read after `newsAdd` builds the item. I grepped the merged file: `newsKnownBy`, `socialHour`'s spread (it uses `SHIP.knows`), `playerHeard`, `newsFeed`, `heardKept` and every `NEWS.*` use. The only `.seed` reads on news items are in the tests: social_check's `stats.spread` and the long run's listener `x.seed[0]`, and events_check's log line. All of them run in memory, never after a load. Loading puts back `seed: []`.
   - Reload gives the same picks (claim 3 below), which confirms nothing deterministic depends on `seed`.
   - CUE_MAX 24 is in place.
2. **Known facts by text hash: holds.**
   - Kovac's `about[0]`, `about[2]` and `life[0]` (+ `news`) are saved as `#rs3a`, `#vy33`, `#08on`, `news`.
   - Real path: the full save object goes into localStorage, and the page loads with no `?nosave`. In that page's HTML, `about[2]` was rewritten in place, as deck-plans did in 57b0089. After the load, Kovac knows `about[0]`, `life[0]` and `news`. The edited line is **forgotten**, and nothing new is shown. Pell's known line is kept, and the time is kept (day 5, 06:00).
   - The same save in the unedited build loads all three and saves them again to the same tags.
   - The in-page `socLoad` with an edited `SOC.crew` gives the same result.
   - Duplicate tags are written out as text (`indexOf === lastIndexOf` guard), which I checked by reading the code.
3. **0.36.76 saves load: holds.**
   - A save from the old merge (`#a0`, `#a2`, `#l0`, `news`; news items still carry `seed`) was loaded into the new merge through localStorage. Time kept, no page errors.
   - Kovac and Pell know exactly the lines they were told. Cues 16/16 and news 1/1, with no null heard lines.
   - Saving it again writes the new `#xxxx` tags.
4. **`heardIt` and reload picks: holds.**
   - Each run went to day D on paper. Then the save was either kept in memory or round-tripped (`socLoad(socSave())`), and the next 24 hours were run.
   - For every crew member aboard, every hour, I recorded what they'd tell you (the chatLine / ask-news filter with `heardIt`).
   - Cases:
     - D = 30 with a light listener;
     - D = 45 and D = 75 with a heavy listener: `heard` at 60 in memory, and only 16 / 24 after the load.
   - Each case was run three ways: hour by hour with the listener hearing at 18:00, hour by hour quiet, and one 24-hour jump.
   - In every case, the picks are identical in memory and after the reload, and the end `socSave()` is byte-identical. The jump's final picks equal the hour-by-hour final picks, both in memory and after a load.
   - (Probe pitfall, not a game bug: `SHIP.device.appts` survives `socReset`, so repeated runs in one page must clear it, as social_check does.)
5. **`pairsLoad`: holds.**
   - Day 60 from the arrival, 113 pairs. I built a save under a reversed crew list and under a shuffled one, with aff, pairs and idl all re-encoded.
   - Both loads gave back the same id pairs in the same order.
   - With one id swapped for an unknown `ghost-person`, its 3 pairs were dropped and the other 110 kept, in order.
   - Re-setting a pair now does `delete` then set in `socialHour` (both branches) and in `feudTalk`, so it moves to newest (read in the code).

## Findings

### 1. LOW-MEDIUM: day 138 is only 300 B under 30 KB, and `news`'s written worst case is lower than the cap really allows
- DEV_NOTES says `news` is "worst about 5.5 KB".
- The largest single saved news item I measured (the hook on `newsAdd` over the 280-day arrival run, knowers bits at full width, no seed) is **414 B** (`habit:`). Others: friends 368, fault 357, tradition 335, transfer 332, rivals 317.
- The largest event-engine items are 296 B (`ionStorm`).
- So the cap allows about **20 x 414 = 8.3 KB**, not 5.5. Measured `news` peaks at 6.3 KB (days 0-39) and 5.0 KB later.
- The rule holds on the measured stand-in, but only by 300 B on day 138, when `news` was 4.5 KB. If `news` came near its real bound that day, the save would be about 33 KB.
- `--long` also runs with `tickShip` off, so no event-engine news (`kind: 'event'`) is ever born in it. The cap still bounds that news, but the test's news mix is lighter than real play.
- **Suggested:**
  - Correct the worst case in DEV_NOTES to about 8.3 KB (20 x the largest item).
  - Either lower NEWS_MAX (for example to 16, about 6.6 KB) or accept the thin margin and say so in DEV_NOTES.
  - Any content growth in rel, bonds or lines will tip day 138 over 30 KB.

### 2. LOW (old finding 6, not taken up): the in-memory `heard` trim can still disagree with a reload
- In memory, `playerHeard` keeps 60 entries. After a load, `heard` holds only live + 12 (13 in the probe).
- If a live item's heard entry is the oldest of 60, the next `playerHeard` removes it in memory, so `heardIt` turns false and the crew retell it. After a reload it is kept, so `heardIt` stays true.
- Constructed probe (`P3.json` "evict"): `heardLiveInMemory: false`, `heardLiveAfterReload: true`.
- Not reached in play: from the arrival to day 140, with a listener who hears everything going round each evening (619 heard, at most 11 in a day), no live item's entry was ever pushed out (`probes5.py`, 0 cases). It needs 59 hearings within one item's life of at most 10 days.
- **Fix as before:** trim the in-memory `heard` the same way `heardKept` does, or never splice an entry whose news is still live.

### 3. INFO
- **The cap goes by age only.** The NEWS_MAX cap drops the oldest by `born` and ignores `life` and `weight`. Example: a 10-day `leaving:` notice (weight .8) goes before a newer 1-day birthday. That's acceptable, but it's a design choice worth a line in design-doc/DEV_NOTES. The cap's choice is deterministic (born, then id).
- **Dead code.** `while (NEWS.length > 40)` in `socialHour` can no longer trigger.
- **Old `--long` and Day 0.** a033f17's own `--long`, if pointed at the arrival, would have used `h % 24`, which is negative on Day 0 (my first probe showed this: no 23:00 sample on Day 0). 8c9b52f uses `socHr`, so it's fixed.
- **Hash collisions.** A collision between a forgotten line's tag and another current line of the same person is possible in theory (about 1 in 1.7M per line). Negligible.

## Daily social save, from the Day 0 arrival (8c9b52f's `--long` on the merge, measured at 23:00 every day)
| Days | Worst (day) | Lowest | news max | NEWS count max |
| --- | --- | --- | --- | --- |
| 0-19 | 23,424 (day 17) | 7,004 | 6,343 | 19 |
| 20-39 | 25,511 (day 31) | 20,602 | 6,329 | 19 |
| 40-59 | 25,067 (day 52) | 20,879 | 4,309 | 13 |
| 60-79 | 28,329 (day 73) | 21,636 | 5,737 | 18 |
| 80-99 | 26,310 (day 87) | 23,132 | 3,619 | 11 |
| 100-119 | 28,810 (day 118) | 23,383 | 4,755 | 15 |
| 120-139 | **29,700 (day 138)** | 24,081 | 4,758 | 15 |
| 140-159 | 30,426 (day 150) | 25,732 | 5,491 | 17 |
| 160-179 | 30,091 (day 179) | 26,294 | 3,538 | 11 |
| 180-199 | 30,758 (day 188) | 26,599 | 4,130 | 13 |
| 200-219 | 31,316 (day 201) | 27,188 | 4,568 | 14 |
| 220-239 | 31,995 (day 223) | 27,620 | 4,145 | 12 |
| 240-259 | **32,821 (day 244)** | 27,371 | 5,038 | 15 |
| 260-279 | 32,686 (day 263) | 27,954 | 4,202 | 13 |
| 280 | 29,474 | | 1,863 | 6 |

- **Days 0-140:** no day over 30,000. Only 2 days are within 1 KB: 138 (29,700) and 139 (29,623).
- **Days 141-280:** 50 days are over 30 KB, all under 40 KB. The peak is 32,821, so 7.2 KB short of the limit.
- **The parts on day 244:** rel 5,137, news 5,038, aff 4,878, bonds 3,092, affWeek 2,739, cues 2,369, rep 2,075, heard 1,798.
- **For comparison, a033f17's own `--long` (Day 1 06:00 start):**
  - worst to 140: day 115, 29,470 B;
  - worst to 280: day 242, 32,890 B;
  - SOCIAL LONG CHECK OK.
  - The arrival start shifts the worst day to 140 by +230 B.

## Tests run
- `name_check` (branches and merge): OK.
- `social_check`: OK on a033f17 alone and on the merge.
- a033f17's `social_check --long` on the merge: OK.
- 8c9b52f's `social_check --long` on the merge: sizes OK, exit FAILED only on the arrival jump `noteq` (section 17's 4 jump-only notes).
- Probes P1-P6 as above, with no page errors.
- Not run: cadet_test, deck_check and day_check. No drawing or schedule code changed.
