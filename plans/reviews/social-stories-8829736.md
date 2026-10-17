# Re-review: claude/social-stories 47b02d6..8829736 (0.39.18-0.39.19)

Reviewer 1, 2026-10-17. **Verdict: PASS WITH FIXES.** The code follows the lead's ruling. Pairs under |aff| 30 are never kept, and the 300 ceiling only trims pairs that already qualify. The selection is deterministic. Old saves load, a time jump matches hour by hour, and the 0.39.19 query fixes hold.

The fixes needed:
- One decision for the lead (finding 1): on the 86-person crew, the "safety ceiling" is reached from week 5. After that it decides seating every day.
- The DEV_NOTES row's numbers need correcting (finding 2).

What the range covers:
- 0.39.18 (ba09f2b): `affWeekTake` keeps at most `AFF_SNAP_MAX` = 300 pairs a week. It keeps the strongest |aff| first, then pair order.
- 0.39.19 (8829736) fixes my 47b02d6 notes:
  - `storyPeek` is a read-only peek, used in `momentNextId`, `momentReady` and `goodbyeMoment`.
  - `momentWantsVisit` is now `momentReady(p, t, {anywhere:true}) === id`.
  - `momentCtx` takes `w.deck` while the person is walking.
  - The tradition overlap is noted in DEV_NOTES.

## Findings

### 1. Medium (the lead's call): the 300 ceiling is reached from week 5, so seating's ±30 line drifts up to about ±42
**Path:** 86 crew (the reserve is in SOC from the start), no player, hour by hour to day 140. I compared 47b02d6 (no ceiling) with 8829736 under the same seed. Probe: `seat.py`, which counts `affinityPlan` friend (30+) and foe (-30 or less) pairs for every day, and hashes `shipDay(d).plans` for days 56-70.

Pairs at |aff| 30+ in the live affinity: 302 at the week-5 snapshot (day 36), 379 at day 56, 519 at day 100, 582 at day 140. So the ceiling decides seating from day 43 on, not only in rare cases.

| day | friend pairs (no ceiling → 0.39.18) | foe pairs | smallest \|aff\| kept | affWeek bytes |
|---|---|---|---|---|
| 44 | 292 → 290 | 10 → 10 | 31 | 2543 → 2411 |
| 57 | 344 → 287 | 15 → 13 | 33 | 2771 → 2411 |
| 72 | 394 → 288 | 21 → 12 | 36 | 3408 → 2412 |
| 100 | 487 → 289 | 19 → 11 | 39 | 4109 → 2413 |
| 135 | 541 → 289 | 20 → 11 | 42 | 4553 → 2413 |

- **Seating changes:** crew plans differ on every day checked (56-70). By day 135, 252 friend pairs and 9 rival pairs between 30 and 41 read as neutral (0), so they're no longer seated together, or kept apart. All three other readers lose them too:
  - section 18's `friends-of-host` (40+)
  - the tradition `who` odds (`max(0, aff)/100 * .6`)
  - `farewellCrew` (60+; unaffected while the cut stays under 60)
- **Live affinity drifts as well**, because seating feeds who eats together: from day 60, the live 30+ count differs by 1 to 8.
- **The saving is 2.1 KB** at day 140 (affWeek 4553 → 2413).
- **Ties at the cut:** they're broken by roster index, so the reserve (last in the roster) always loses them. It's deterministic but systematic. Low.

**Fix (pick one):**
- (a) Raise `AFF_SNAP_MAX` to about 600. That's about 4.8 KB for both weeks. At day 140, 582 pairs qualified, growing by about 10 a week. With the --long numbers below, the save would be about 27.9 KB at day 140, under 30,000.
- (b) Keep 300 and write down in design-doc / DEV_NOTES that seating's friend line rises to about 40 after the first month.

Either way, the ruling's wording ("only a safety ceiling") doesn't match what happens on the reserve crew.

### 2. Low: the DEV_NOTES row's numbers
**The row says:** "2.4 KB from day 56 on" and "the whole social save 19.7 KB at day 140".

**Measured:**
- affWeek is at its fixed 2,411-2,415 bytes from the day-44 snapshot on (table above).
- The 19.7 KB is a figure with no player. My no-player run on the branch swings between 16.6 and 22.5 KB from day to day after day 56, and gives 22.2 KB at day 140.

**With a player** (the coordinator's question), on a merge of social 4cccc6d + 8829736 using social A's `social_check.py --long`:
```
Day 28: 21417 | Day 56: 22673 | Day 84: 23443 | Day 112: 25538 | Day 140: 25465 bytes
Day 140 parts: aff 4878, bonds 4483, cues 2756, affWeek 2415, rel 2266, pairs 1839, rep 1739, news 1420
SOCIAL LONG CHECK OK
```
Social A's 25.5 KB is the number that holds. affWeek is 2,415 B of it (9.5%). The two snapshots hold 300 pairs each, with the smallest |aff| kept at 41.

**Why the numbers differ:**
- B2's 19.7 KB has no stand-in player (no rel, rep or heard growth).
- A's earlier 32.3 KB (0.36.73) used the 14-day check's stand-in for 140 days. I repeated that run: 32,279 B on a merge of 8829736 + social 6353c2d + deck-plans-1-2-6 + sim-engineer, and 31,524 B on the tip alone. The extra is:
  - `heard`: 7.1 KB. That stand-in marks everything Rina knows as heard every day, which fills the 60-entry ring at about 118 B an entry.
  - story Mail: 2.6 KB that the test never delivers.

**For social A:** a real player who listens a lot can fill `heard` the same way. That leaves about 4.5 KB of headroom with 0.39.18, or about 2.4 KB with fix 1(a).

**Fix:** correct the row: "the ceiling is reached from the week-5 snapshot; whole social save 25.5 KB at day 140 by `social_check --long`".

### 3. Latent: `momentWantsVisit` now also needs no dialogue open
`momentReady` returns null while section 18's `DIALOGUE` is up. The visit picker (`socialVisit`) waits only for `CHAT`, `SEEK` and sleep. So if a dialogue panel is open at the minute the evening visit is picked, the beat's visitor isn't preferred that evening. It's rare, and harmless apart from that.

## Checked and fine
- **Deterministic:** the comparator `|b|-|a| || i || j` is a total order, because (i, j) is unique per pair. Each kept list goes back into pair order, so the bytes don't depend on how the list was built.
- **The ruling (|aff| ≥ 30, ceiling on top):** the filter runs before the ceiling. In 20 weekly snapshots, no snapshot ever has more than 300 pairs. The smallest |aff| kept is always 30 or more (30 while under the ceiling; 31 → 42 above it). No snapshot is filled up with weaker pairs. Before week 5 the snapshots are byte-identical to 47b02d6's (the same affWeek lengths and the same pair hashes through day 42).
- **Jump vs hour by hour:** weekly jumps (`socialTo` 7 days at a time) to day 134 match hour by hour at every weekly checkpoint (pair hash, live 30+ count, affWeek, per-week sizes).
- **Old saves:** I loaded 47b02d6's day-140 `affWeek` (561 and 574 pairs, 4553 B) into 8829736:
  - it decodes in full (affPlanWeek reads both weeks);
  - `socSave` → `socLoad` → `socSave` round-trips the same;
  - the next week's take obeys the ceiling, and the old week drops off a week later.

  The format string is unchanged.
- **0.39.19 purity:** in a fresh game, I asked `momentWantsVisit`, `momentReady` (and with `anywhere`), `goodbyeMoment` and `momentHint` for all 86 crew every hour:
  - over 48 hours from Day 1, and again with tiers boosted: `SHIP.social.stories` stayed `{}` and `socSave()` was unchanged.
  - over days 32-36 with tiers boosted (15,042 ready hits, 144 goodbye hits): `socSave()` was unchanged after every query at t = now.

  The only state that moved was `SHIP.machines.*.cond`. That's section 17's lazy catch-up to the current minute (my harness doesn't call `machinesNow`), which the next tick does anyway.

  Asking at now + 30 min did change `socSave()` on 20 of 72 hours. That's probably the machine catch-up running ahead of the clock, but I didn't trace it. Every caller in play passes `shipNow()`, so it's not a finding against this range.
- **Names:** `name_check.py --branches 47b02d6 ba09f2b`, `47b02d6 8829736` and `ba09f2b 8829736` all give NAMES OK, as does `name_check.py` on the full merge.
- **social_check:** OK on the tip (21,143 B; same twice True; jump True) and on the full merge (21,087 B; OK). The branch's limit is 30000.
- **Full merge:** 8829736 + origin/claude/social 6353c2d + deck-plans-1-2-6 caedef2 + sim-engineer f9a145c, plain merges with no `-X` and without ship-systems.
  - In starship-cadet.html, only build-line conflicts. The deck-plans hunk spanned section 13's notes bus because of where the build line sits, so I kept ours. The bus is intact (`function simNote` appears once).
  - One test-only conflict in `player_check.py`: I took sim-engineer's side; it isn't used here.

## Tests
- Probes (all `?nosave&debug`, under browser.lock, no page errors) are in my scratchpad's `rv-socB18/`:
  - `seat.py`: 140 days, two builds, plus weekly jumps
  - `pure.py` and `purediff.py`: query purity
  - `old.py`: an old snapshot loaded into the new build
  - `save140.py`: 140 days with the 14-day stand-in
- social_check (tip, full merge) and `social_check --long` (social 4cccc6d + 8829736) as above.
