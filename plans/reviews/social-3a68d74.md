# Re-review: claude/social dc80136..3a68d74 (0.36.60-0.36.63)

Reviewer 1, 2026-10-17. **Verdict: PASS WITH FIXES.**

This note covers four builds:
- **0.36.60:** the asked-for waves now come and find you; the fill-ins are returned as written; {since} grows.
- **0.36.61:** lamp favours are remembered as `fav.lamp`; notes are applied at the end of their hour; cues are sorted by time.
- **0.36.62:** the favour line fixed after 0.36.61's comment cut it off; a new social_check part 15.
- **0.36.63:** an asked-for visitor walks to a free seat by you.

All three findings from social-d1e97bd are dealt with, at least as far as social's side goes. The 0.36.61 regression is fixed in 0.36.62, and part 15 really does catch it.

## Findings
### 1. (Medium-low) In the junior common room, seekSpot can send the visitor to your own seat
- **The code.** 0.36.63's fallback picks the nearest sitting place nobody in `DECK_CREW` has as a goal. It doesn't leave out `PLAYER_PLACE`, and it dropped 0.36.60's `d > .5` (not right on top of you). `seatsBeside` only offers mess seats, lounge seats and benches, so in a room without those the fallback runs.
- **On paper** (merge5, every sitting place on each deck, `PLAYER_PLACE` set to it, `seekSpot()`): the result is your own place for **18 of 22 places on Deck 4** (the junior common room, `4-common-1`...), 4 of 123 on Deck 3 (the garden) and 2 of 47 on Deck 2 (window seats).
- **In play** (merge5: player at `4-common-1`, Tomas asked): Tomas walked to `4-common-1` itself and waved from 0 m, standing in your spot.
  - In the probe section 15 cleared `PLAYER_PLACE`, because I couldn't actually sit the player down. So this is the "standing" case.
  - With you really sitting there, the sim's `elsewhere()` returns null for a non-seat that is `PLAYER_PLACE` ("wait nearby for you"). He then never reaches `visit.placeId`, `onArrive` never fires, and the wave waits for `SEEK_WALK` and a retry that picks the same place again (reading only).
  - The 'tomas' step's own place is "the junior common room or Bunk 1", so this is the Day 0 case.
- **Fix (one line in `seekSpot`):** add `PLAYER_PLACE` to `used`, and keep 0.36.60's `d > .5` so the visitor never gets your own spot.

### 2. (Low) A visitor starts walking while you're asleep
`socialSeekAsks` checks `CHAT || SEEK || sleeping` only once the person is already near you. Before it starts a walk it checks nothing. Probe (merge5, `sleeping = true`, Tomas asked): `{"calls": 1, "walking": true}`. So during a window, someone walks to your bunk while you sleep, and then retries every `SEEK_RETRY` minutes. **Fix:** `if (CHAT || SEEK || sleeping) continue;` before `seekSpot()`. Or only start a walk when `!sleeping`.

### 3. (Low) {since} says "21 months" in digits
`socDuration`'s `W()` falls back to digits above twenty. The months branch runs up to 729 days, which is `mo` = 24, so 630-729 days come out as "21 months" to "24 months". Every other phrase is in words. **Fix:** use the years branch from 600 days, or add "twenty-one" to "twenty-four" to `SOC_NUM`.

### 4. (Low) Equal-time cues are ordered only by key, so a jump and an hour-by-hour run can keep different ones
The new sort is `a.at - b.at || key`. Two cues with the same minute and key but a different `who` or `you` keep the order they arrived in (V8's sort is stable). In a jump the sim sends its notes all at once, which can be a different order from the hours played one by one. `cue()` returns the newest match, and `.slice(-30)` drops the oldest, so in that case the two modes can disagree. It's rare: it needs two repairs of the same machine kind in the same minute. **Fix:** add `|| (a.who || '').localeCompare(b.who || '') || (a.you - b.you)` to the tie-break.

## The things asked
- **The seek fix (0.36.60/63): the wave now happens in play on the merge.**
  - merge5 = full merge + sim 0cf991a. Tomas starts in the Deck 3 mess at Day 1 08:00 and you're on Deck 4 in Bunk 1.
  - 08:05 walking; 08:17 he's 4.1 m from you and SEEK is tomas; the chip reads "Tomas waves you over."; the ask is marked done; by 09:05 he's gone home.
  - This is with the real `crewComeTo`. social_check's own walk test stubs it to arrive at once, so it doesn't test the walk itself.
  - Exception: the seated case in finding 1.
- **Double-booking with the sim's seat-taken rule (0cf991a `elsewhere`/`ALT_SEAT`):**
  - `seatsBeside` already leaves out held spots (`a.spot.id`), `BUSY` and `PLAYER_PLACE`, and the fallback leaves out crew goals.
  - If a seat is taken while the visitor walks there, the sim sends them to another seat. But section 10 fires the visit's `onArrive` only when `spot.id === visit.placeId`, so on the other seat there's no wave until `SEEK_WALK` runs out. Social then retries with a new seat 20 minutes later: slower, but no double booking.
  - Taken places that aren't seats (the kettle, the common room's places) are shared, as before. My BUSY probe aimed at `4-common-kettle`: Tomas still arrived and waved at 08:24.
- **Theme fill-ins (0.36.60):**
  - `{family}` is returned as written: social_check `fam: "a brother in the Concord navy"`. This matches the roster and the writers' "my {family}".
  - `{since}` grows: `grow` "six years" equals `growWant`.
  - A phrase the parser can't read ("two and a half years") stays as written.
  - Still open, but for the dialogue engineer: section 22's `linesFill` fills these four from the raw roster fields, so the growing {since} and the {hobby} fallback reach lines only once section 22 adds `'home', 'family', 'hobby', 'since'` to `SOCIAL_FILL`. That is now safe: both paths give the same {family}.
- **The jump-test fix (0.36.61):**
  - On the refreshed full merge (merge4: arrival 8c28e91 + sim 5687bec + crew 4613d43 + social 3a68d74 + social B 4222804 + player b8dde49 + galley 6abd36b): "Two days in one jump the same as hour by hour (with bus notes): True". The real bus: `cue True, queued 0`.
  - Moving `socNotesTo` to the end of `socialHour` delays no cue. `socialHour(h)` only runs once the clock has passed `(h+1)*60` (in `socialTo`), so a note from hour h was always applied when that hour finished. Within the call nothing can ask for a line.
  - All it changes is that the hour's own work (memFade at 04:00, repWeek on Sundays, the 07:00 transfers and invites, the 19:00 crew gifts) no longer sees that hour's notes. It's the same in both modes, which is the point.
  - `SOC_IN` is set and cleared inside `socialHour`.
- **0.36.62's line:** `memAdd(p.id, 'fav.' + fk); repAdd(p.dept, 2, { kindness: 3 }, 'kind');` is back before the comment.
- **Part 15 guards it.** The part's own JS, run on both builds:
  - On f75e484: `{"mem": false, "kind": null, "dept": null}`, so the part fails.
  - On 3a68d74: `{"mem": true, "kind": 53, "dept": 12}`, so it passes.

## Passed
- `name_check.py --branches dc80136 9929222`, `9929222 f75e484` and `f75e484 3a68d74`: NAMES OK. name_check on merge4 and merge5: NAMES OK, node --check parses.
- social_check on the branch at 3a68d74: SOCIAL CHECK OK. On merge4: SOCIAL CHECK OK.
  - The same twice; the jump True; save and load the same; purity True; `beatMap` True.
  - Asked-for waves `[True, False] / [False, True, False]`; the walk `{'walked': 1, 'chip': True, 'done': True, 'once': True}`; a favour handed in `{'mem': True, 'kind': 53, 'dept': 12}`.
- **Save:** `seekAsks` are saved as `{ id, from, until, why, done }` only. The live `walking`, `next` and `stop` (a function) never reach the save, and `socSave()` still stringifies after a walk.
- **Hash keys:** no new `schedU` keys in dc80136..3a68d74.

The merge worktrees are left in place:
- `/tmp/cadet-work/rv-social-merge4`: the full merge with social 3a68d74.
- `/tmp/cadet-work/rv-social-merge5`: merge4 plus sim 0cf991a.

In both, the duplicate `GAME_BUILD` lines are removed in the working tree only.
