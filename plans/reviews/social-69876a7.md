# Re-review: claude/social 3a68d74..69876a7 (0.36.64-0.36.72)

Reviewer 1, 2026-10-17. **Verdict: PASS.**

## What this covers
- **0.36.64:** merge of ship integration 0.60.2.
- **0.36.65:** A10, guiding a newcomer. Behind `flag('promoted')`.
- **0.36.66:** A11, your own room ("Come over"). Behind `flag('promoted')`.
- **0.36.67:** the save packs 20c's bonds.
- **0.36.68:** Day 0 hours (`socHr`), `momentWantsVisit` in the visit picker, and the kin/lost/hobbyNoun fill-ins.
- **0.36.69-0.36.71:** the lead-approved tuning:
  - ship standings climb more slowly near the top;
  - rivalries stop at -45 and ease with time;
  - an unclaimed job costs its department once a week.
- **0.36.72:** the fixes for my four findings from social-3a68d74.

The branch has moved on to 0af9cb8 (0.36.73: rel arrays saved without trailing zeros). I read and tested that too: every run below is at 0af9cb8, which contains 69876a7.

## The previous note's four findings: all fixed
1. **The visitor never takes your seat.** `seekSpot` now counts `PLAYER_PLACE` as used, checks `seatsBeside`'s pick against `used`, and skips anything within 0.5 of you.
   - Probe on the full merge: I put the player on each of Deck 4's 22 sitting places in turn (position and `PLAYER_PLACE`) and called `seekSpot()`.
   - Result: `{"places": 22, "own": 0, "close": 0, "none": 0}`. Before the fix it was 18 of 22 on your own place.
2. **No walk while you sleep.** `socialSeekAsks` returns early while `sleeping`. Probe with `sleeping = true`, an ask for Tomas and `crewComeTo` counted: `{"r": false, "calls": 0, "walking": false}`.
3. **{since} in words.** The probe gives:
   - 599-609 days: "twenty months";
   - 610-729 days: "nearly two years";
   - 730 days: "two years";
   - 3000 days: "eight years".

   No digits anywhere.
4. **Cue tie-break.** The sort is now time, key, `who`, then `you`, so it only ties on cues that are the same in every field it reads. Fixed.

## Checklist
- **Names:** `name_check.py --branches` run pairwise on every commit (3a68d74→84e992e→790e712→131f747→9c16a83→0811adc→4ad49dd→80fdcb5) and on 142b503→84e992e: NAMES OK each time. On the full merge: NAMES OK, and `node --check` parses.
- **Hash keys:** social's new keys are 659 (the visit picker's tie-break), 666 (the answer line in `guideAnswer`) and 667 (the host line in `hostCame`). All are in A's range (644-671), and each is used exactly once in the file. Every other new `schedU` key in the range comes from the integration merge (other seats).
- **Hooks:**
  - `momentWantsVisit`, `introGuide`/`introGuideEnd`, `apptReply`, `deviceNotify`, `flag`/`flagSet` and `playerBed` are all `typeof`-guarded.
  - Nothing runs at load, so there's no TDZ risk.
  - `momentWantsVisit` returns booleans, which subtract cleanly; an `undefined` gives NaN, which falls through to the next tie-break.
- **Reputation (A12 curve).** The full-merge probe sets `R.ship.work` and calls `repAdd`:
  - at the top: `[100+5 → 100, 99.99+1 → 99.99, 100-5 → 95, 50+1 → 51, 49+10 → 59, 90+50 → 100]`;
  - at the bottom: `[0-5 → 0, 0.01-1 → 0.01, 0+5 → 5, 1-100 → 0, 50-1 → 49]`;
  - NaN, `undefined` and 0 deltas leave it at 70;
  - 2000 rises of +3 from 50 end at 99.92, and 2000 falls of -3 end at 0.08.

  It never goes NaN or out of [0, 100]. The ends are reached asymptotically, then clamped.
- **Rivalry floor and healing.** `socHeal` only raises pairs below -25 on even ship days (Day 0 counts as even): -60 → -59, -26 → -25, and -25 stays. Old saves with pairs down to -60 heal upwards; nothing pushes a pair below -45 any more.
  - This fits 20c's hysteresis: rivals at -40 or less, rivalry off above -25.
  - The full merge shows 5 rival bonds at day 14. A12's numbers are in DEV_NOTES.
- **Day 0:** `socHr` = `[23, 23, 0, 23, 0]` for h = -25, -1, 0, 23, 24.
  - The hourly hooks that can now fire on the arrival evening are the 19:00 crew gift and the 20:00 Holt courtesy check. The gift needs tier 3+ friends and the courtesy check needs a guest event, so neither does anything on Day 0.
  - `repOnce('unclaimed.' + dp, 'w' + socWeek())` gives 'w-1' on Day 0, which is harmless.
- **Bonds packing (0.36.67).** Full-merge probe, `socSave`/`socLoad`:
  - the packed form round-trips, `spar` and `gone` included;
  - a save whose `idl` is the crew list reversed (with the indices remapped) gives back the same bonds;
  - a kind not in `SOC_BOND_KINDS` is dropped (frozen list, 20c uses only those);
  - junk rows (`null`, an index of 999, kind 99, a string) load as `{}` without throwing.
- **Real `saveGame`/`loadGame` (`?debug`, storage on):**
  - With Tomas pts, `hostDay` 3, two bonds, a `guide` record and Work 55, a reload gives back an identical `socSave()` (8008 bytes; the whole save is 17.7 kB on Day 0).
  - **Old save:** a save edited to have object-form bonds, 16-field rel arrays (no `hostDay`) and no `guide` was injected before the page loaded, so `pagehide` couldn't overwrite it. It loads to the two object bonds, `guide: null` and `hostDay: 0`, then re-packs as `{"v":1,...}`.
- **New game** (`newGameStart(false)`): day 1, `guide` gone, rel {}, bonds {}, rep null, `flag('guide.active')` undefined.
- **Per frame:** nothing new runs per frame.
  - `seekSpot` runs only when an asked-for visitor is due and not yet walking.
  - `socHeal` loops over the 3655 pairs once every two ship days.
  - The visit picker's comparator calls `momentWantsVisit`, but only on the minute the visit odds pass.
- **A10/A11 behind the flag:** everything that runs is reached only through `flag('promoted')`: `socGuideDay`, `hostOk`, Calder's assignment line (it needs `SHIP.social.guide`) and the `bondOf` mentor branch. That flag is off in normal play. social_check parts 16-17 run both features with the flag set.

## Not a finding, for the lead (0.36.73, past the asked range)
- **Save size at 140 days.** 0.36.73's own DEV_NOTES row measures the social save at 32.3 KB on day 140, or about 29.6 KB in play.
  - That is at the 30 KB budget, and it grows: social B's `affWeek` is 4.6 KB.
  - social_check measures only day 14 (21.1 KB on the full merge), so nothing would catch it.
  - The helper has told social B2. Worth a lead decision: cap `affWeek` further, or set a budget for long play and check it in social_check at day 140.

## Tests
- **social_check on the branch at 0af9cb8:** SOCIAL CHECK OK.
  - The same twice; the jump the same as hour by hour (True); save and load the same; a different crew list and a reserve person handled; the real bus.
  - Part 16 "Guiding a newcomer", part 17 "Your own room" and part 18 "Small seams" `['my gran', None, 'chess', 19, 7, 1, 2, 'twenty months', 'nearly two years', True]` all pass.
  - Social save 20876 bytes (limit 30000).
- **Full merge** (`/tmp/cadet-work/rv-socA6-full`):
  - **Build:** arrival d24b017 + sim-engineer b9089d9 + deck-plans-1-2-6 d53cf40 + social 0af9cb8 + social-stories 10d8805 + player-needs b728101 + galley-food de83d99.
  - **Conflicts:** only build lines and DEV_NOTES/design-doc table rows, except for two test files.
    - `player_check.py`: took social's side, the integration 0.60.2 version.
    - `cadet_test.py`: one style line, kept both selectors.
  - **Results:** NAMES OK, and SOCIAL CHECK OK (jump True, bus cue True, save 21135 bytes, no page errors).
- **Browser probes** (scratchpad `tools/probeA6.py`, `probeA6s.py`, `probeA6o.py`): as quoted above, no page errors.
