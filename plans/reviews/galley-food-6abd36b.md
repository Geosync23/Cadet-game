# Re-review: claude/galley-food 812bedd..6abd36b (0.29.27-0.29.31)

Reviewer 1, 2026-10-17. **Verdict: PASS WITH FIXES** (812bedd..6abd36b; 6efe188 in the addendum, also PASS WITH FIXES). The galleyBirthdays fix that was owed is in and correct. The tasting vote through section 18's tally works on a real merge. Two late-meal problems should be fixed before the combine (1, 2). Item 3 (who calls the line hooks) is now low, because the sim made them idempotent. Item 4 is fixed in 6efe188. The rest are low.

Scope: section 16, food_check.py, DEV_NOTES and the galley handover, in builds 0.29.27 (dc644bc), 0.29.28 (84700e0), 0.29.29 (944f520), 0.29.30 (28ce141) and 0.29.31 (galley commits 3721d34..6abd36b, on top of the 0.60.1 merge d828b1c, read as `git diff d828b1c 6abd36b`). Every changed line is in section 16, except the build line. There are no new `schedU` keys, and no `Math.random`, `Date.now` or `performance.now`.

Scratch merges, all full `git merge` with only the build-line conflicts resolved (cadet_test.py's style line too on the player merge):
- **E** = 28ce141 + claude/ship-events 4e72597 (has `tallyOf`, `tallyVote` and the real tasting-table and Sunday-table ties).
- **S** = 28ce141 + claude/sim-engineer 971b4c7 (the new `simNote` that honours `data.t`).
- **P** = 6abd36b + claude/player-needs b8dde49 (0.28.34, which calls `lineJoin` itself).

## Findings, most severe first

### 1. MEDIUM: lateMeal notes carry the send time, not the minute it happened
- **Path:** `galleyLate()` calls `simNote('lateMeal', { who, meal, late, how, dish, deck: 3 })` with no `t`. During any catch-up (sleep, the debug Night/Day button, `SIM_ADVANCE`, a fresh start), `galleyAdvance` steps many minutes at once. Every late meal in that span gets stamped with the end of the jump. Social queues each note by its `t` (`socHear`), so the cue starts late. This also breaks the "a jump plays out the same as hour by hour" rule: this is the time part of notes-bus-contract-0601, which the sim fixed on its side in 2f6d8dd (`simNote` takes `data.t`).
- **Evidence (merge S, probe `late.js` block 1):** I played day 9 live, minute by minute: `liveT: "08:18 08:20"` (vance and sato, late grab breakfasts). The same day in one jump: `jumpT: ["23:59"]`, `t: 12959` for both. The payload `kind` survives (`kind: 'lateMeal'`; the payload has no `kind` of its own, so the open "simNote overwrites kind" bug doesn't touch it). `dish` is the servery's dish, or null for the shelf and for missed.
- **Fix:** add `t: m` to the payload in `galleyLate` (one word). On 0.60.0's old `simNote` the payload's `t` is overwritten, so it's harmless there.

### 2. MEDIUM: New game (and every first launch) fires about 48 lateMeal notes at once, about 30 of them "missed breakfast"
- **Path:** `newGameStart` sets the time back to Day 0 17:40 but leaves `SHIP.galley` alone. `galleyAdvance` then sees time going backwards and makes a fresh start at Day 0 00:00. It replays 00:00-17:40 with `st = null`, which is the live path, so every late or missed breakfast becomes a note. They go into the ring that New game has just cleared, and to social as cues for the arrival evening. `GALLEY_LATE` is in memory only, so nothing stops this. A first launch goes through the same `newGameStart(true)`, or starts with `SHIP.galley` null, which is the same fresh start. The DEV_NOTES 0.29.28 row's claim "Live only (never in replays)" doesn't hold for fresh starts.
- **Evidence (merge S, `?debug`, probe `save.js` last block):** set Day 10 10:00, then `newGameStart(true)`, then `galleyTick()`. Result: `time: "Day 0, Sunday 17:40"`, `before: 15001, after: -379`, `heard: 48`. All 48 are in `SHIP.notes` with `t: -380`. Examples: `["yoon-elif","breakfast","servery",32,-380]` and `["quist-ilse","breakfast","missed",104,-380]`, with 30 "missed" in total. The missed breakfasts are the replayed galley starting cold at midnight on Day 0. That's an existing quirk, but now it reaches the bus.
- **Fix (section 16 only):** mute notes for minutes stepped by a fresh start. For example, in `galleyAdvance`, when it makes a fresh `S`, record `GALLEY_QUIET = to`, and have `galleyLate` (and ideally `galleyMail` and `galleyScore`) return when `m < GALLEY_QUIET`. Or listen for `onSim('newGame')`, reset `SHIP.galley` and `GALLEY_LATE`, and start quiet. Add a food_check case: New game, then expect no lateMeal notes.

### 3. LOW (contract; the risk is gone with sim 0cf991a): both the galley and the player seat call `lineJoin` / `lineLeave` for the player
- **Path (merge P):** tapping the servery runs section 15's `const j = galleyJoin('player'), ln = lineAt(typeof lineJoin === 'function' ? lineJoin('player') : null)`. In 0.29.31, `galleyJoin` already calls `lineJoin(who)` when `galleyLine()` is true, so that's two joins. On arrival, section 15's `if (A.kind === 'queue') { const j = galleyJoin('player'); ... }` makes a third. Leaving has the same overlap: section 15 calls `lineLeave('player')` in `actEnd` (when there's no dish) and in `queueLeave`; section 16 calls it in `takePortion`. They also read the spot differently: the player's `lineAt` wants `sp.x` / `sp.z` (metres) and `sp.at`, the galley wants `sp.at` and `sp.xy`. Nothing breaks today, because no branch defines `lineJoin` yet (I searched every `origin/claude/*`). Once it exists, a `lineJoin` that appends would put you in the line two or three times, or send you to the back when you reach it.
- **Update (sim 0cf991a, see the 6efe188 section below):** `lineJoin` is idempotent (`if (!LINE.includes(id)) LINE.push(id)`) and `lineLeave` is a no-op when you're not in the line, so the extra calls do nothing. 6efe188 also reads `lineSpot`'s real shape (`x`, `z`, `face` in radians). What's left is only who owns the calls; write it in the hook register.
- **Fix:** the lead names one owner. The simplest is that section 15 joins and leaves (it owns the walk and the abort), and `galleyJoin` / `takePortion` only read `lineFront` / `lineSpot`. Or section 10 makes `lineJoin` idempotent (joining again keeps your place) and fixes `lineSpot`'s shape in the hook register.
- Checked otherwise: the hooks are `typeof`-guarded (`galleyLine()` needs all three of `lineJoin`, `lineSpot`, `lineFront`). Without them, the fallback spot and `galleyAhead` work (food_check's live-line stand-in). There's no fight with the player branch's removed count: section 15 0.28.30+ ignores `j.ahead` in the join toast and still uses `j.turnAt` for the bar and the tap line. name_check on P: NAMES OK.

### 4. LOW-MEDIUM (fixed in 6efe188): a queue you walk away from leaves a stale join, and your next meal of the day posts a false "late" note for you
- **Path:** `GALLEY_JOINED` is cleared only in `takePortion`. If you leave the queue (section 15's abort), the entry keeps `since`. Your next `takePortion('player')`, hours later from the shelf, computes `waited = m - j.since`, and that is ≥ `LATE_WAIT.you`. The result is a `lateMeal` note with `who: 'you'` and a huge `late`, which becomes the cue `lateMeal.you`.
- **Evidence (merge S, `late.js` block 3):** control: no join, grab at 12:30, no 'you' note. Stale: `galleyJoin('player')` at 07:00, walk away, grab at 12:31. Result: `["you","breakfast","grab",331,"12:31"]`.
- **Fix (galley side):** in `takePortion`, use `j` only while it's fresh, for example `j && m - j.since <= 120` or `j.turnAt` within the same meal window. Or clear entries older than the meal's close in `galleyJoin` / `galleyTurn`.

### 5. LOW: `galleyFresh()`'s signature misses one-offs and tradition flags
- `evSig()` covers section 14's ship event, its log and the intro. Section 18's `eventOneOff` clears its own `EV_DAYS` and `SHIP_DAYS` without changing `evSig`, and so does a tradition flag (`eventsOn`'s `EV_ARR`). So `GALLEY_TASTE`'s voters, which come from `planDay`, can stay stale for a Wednesday already worked out if a one-off is booked over the tasting. The ties themselves are safe today (one-offs carry no ties). This partly closes my previous note 1.
- **Fix:** add `SHIP.events.oneOffs.length` (guarded) and the flagged traditions' states to the signature, or ask section 18 for an `eventsSig()`.

### 6. LOW: allocation every frame while the tasting plates are out (Wednesday 18:15-19:30, on Deck 3)
- `galleyShow` calls `galleyTasting(day)` every frame before its key check. Each call builds an `evSig()` string, does `JSON.stringify(SHIP.events.votes)`, builds the `tallyOf` memo key and an object spread, and makes three small arrays. That breaks the checklist's "no allocation per frame".
- **Fix:** compute `tl` from `S.tasting.left` and the cached `GALLEY_TASTE.get(day).tastes`, and only when `S.tasting.left` changes.

### 7. LOW (latent): Day 0's day of the year differs between the galley and section 18
- `galleyBirthdays(0)` uses `((d-1)%364+364)%364+1 = 364`, while section 18's `eventsOn` uses `shipYearDay(0) = (0-1)%364+1 = 0`. A crew member with birthday 364 would get a servery cake and Mail on Day 0 but no birthday gathering. No one has that birthday today (`galleyBirthdays(0) = []`).
- **Fix:** use `shipYearDay` when it's defined. Better, tell the traditions engineer that `shipYearDay(0)` should be 364 (guestStay already treats Day 0 as the last day of the year before).

## Verified OK
- **Birthdays aboard (the item owed, 0.29.29):** `schedPeople()`, then `rank !== 'guest'`, then `birthdayOf`, then `aboard(p,d) && guestStay(p,d) !== 'leave'`. This is the same rule as ship-events' `eventsOn`. On merge S, I gave three people stand-in rotations (`aboard [null,35]`, `[35,null]`, `[50,null]`), each with a birthday on the day tested:
  - leaver on day 35 ('leave'): no cake. Day 34: cake. Day 36 ('away'): no cake.
  - newcomer on day 35 ('arrive', 17:40 off the shuttle, cake 20:15): cake. Day 34 ('away'): none.
  - reserve not yet aboard (day 40 and Day 0): none.

  Days 0-120 with the real roster: the galley and section 18 agree on every day (`diff: []`). The section 18 on sim/0.60.0 has no aboard filter, so there the galley is stricter. That's correct and matches ship-events.
- **Tasting through the tally (merge E):** `tallyOf` / `tallyVote` signatures match section 18 (`choices` with `per: 2`, `counts`, `winner`, `you`). Wednesdays 3, 10, 17 and 24 give the right pairs (herb flatbread / pickled beans, ...). `voters` are in absolute minutes (18:15 to 18:17), matching `planDay`. 20 tastes are cooked at 17:15, out at 18:15, two a taster (`left` 20 → 4 for 8 tasters), and cleared at 19:30. `galleyVote(1)` counts (`[7,1]` → `[7,2]`, `you: 1`); a second vote is refused. Sunday's side is that week's winner (days 7, 14, 21). Every hook is `typeof`-guarded. With no `tallyOf` (0.60.0, merge S), the fallback pair and "no winner" path runs (food_check's stand-in). With section 18 missing entirely, there are no ties and no tasting.
- **0.29.30 cake away from Deck 3:** `away(e)` leaves out four weeks aboard (Deck 5 tea corner). Founding Day (decor on the event, not `ties.decor`, on Deck 3) and the birthday still bake.
- **Save:** galley state round-trips through the real `saveGame` / `loadGame` (`?debug`, merge S). The galley is about 1.1 kB of a 55 kB save. A save with `galley.tasting` deleted loads and plays (every read is `S.tasting && ...`). `SAVE_V` is unchanged. `GALLEY_LATE` isn't saved; a reload restores `S.at`, so there's no replay and no duplicate (except the fresh-start case in 2). Your tally vote is saved by section 18 (`ship.events.votes`, last 20).
- **Day 0 negatives:** `galleyLate` computes `d = floor(m/1440)+1` (0 on Day 0). takePortion's after-midnight rule and the tasting fallback's `floor((d-1)/7)` only run on Wednesdays ≥ 3. No NaN was seen.
- **0.29.31:** `galleyAhead` reads real `CrewAgent` fields (`spot.id`, `x`, `z`, and `placeSpot`'s `x`, `z`). `galleyServeMins` / `galleyCanServe` are pure reads plus `galleyAdvance`. `GALLEY_QUEUE` is now front first, which DEV_NOTES says is pixel-identical against 0.60.1 (I didn't rerun cadet_test).

## Tests run here
- `name_check.py --branches 812bedd 944f520`, `944f520 28ce141` and `28ce141 6abd36b`: NAMES OK. `name_check.py` on merges S, E and P: NAMES OK, `node --check` parses.
- food_check: **OK** on 28ce141 and **OK** on merge S (crew late notes the report would post: `[1,1,1,2,1,3,5]` a day; my 14-day count: 0-5 a day). **OK** on 6abd36b.
- events_check on merge E: FAILED on one line, `FAIL 231 dayReport double: 3-store-1 esposito-yara/ishikawa-orla@14:30` (the store, not the galley). The same line fails on claude/ship-events 4e72597 alone, so it isn't from this branch (traditions engineer's or crew's to look at). Everything else passes, including the tallies (`'ok': True`).
- Browser probes (scratchpad `g/probe.py` with `tally.js`, `late.js`, `save.js`, `save2.js`, `bday.js`): outputs as quoted above. Tasting save on E (`?debug`): vote at 18:20, then `saveGame` and reload. Result: `tasting {d:10,left:2,out:true}` and the vote `tasting-table@10` are both back, and `you: 0`.

## Addendum: 6abd36b..6efe188 (WIP 0.29.32), on a merge with claude/sim-engineer 0cf991a (0.26.30, the real food line)

**Verdict for 6efe188: PASS WITH FIXES.** The line contract matches. Findings 1 and 2 are still open (the late-meal code didn't change). Finding 4 is fixed.

Merge **L** = 6efe188 + sim 0cf991a. Conflicts were the build lines, plus design-doc and player_check text (I kept the galley side for these; not run). name_check `--branches 6abd36b 6efe188` and on L: NAMES OK.

- **The contract matches section 10's code:**
  - `servLine()` returns ids, front first. `lineJoin(id)` is idempotent and returns the spot. `lineLeave(id, gaveUp)` is safe when you're not in the line. `lineFront(id)` is true for index < `LINE_COUNTER`. `lineSpot(id)` returns `{ x, z, face (radians), at, front }`.
  - `galleyJoin` turns that spot into the galley's deck coordinates and degrees: `xy = [x+OX, z+OZ]`, `face*180/π`.
  - `lineTick` skips `'player'` ("you're served by section 15"). It uses the galley's `galleyServeMins` / `galleyCanServe` (typeof-guarded on its side).
  - Section 10's own header comment says `lineSpot` gives `{ at, xy, ... }`, but its code returns `x, z`. The galley follows the code. Ask the sim engineer to fix the comment.
- **Probe on L (Deck 3, day 2 17:25, after 900 frames, 54 crew on the deck):**
  - `galleyJoin('player')` gives `ahead: 1` and you're at index 1 of `servLine()`.
  - Joining again leaves you in the line once (`again: 1`).
  - `xy [33.55, 5.5]`, `at [33, 5]`, `face 90`.
  - While `ACT.kind === 'queue'`, `galleyTick` keeps you in the line.
  - With `ACT = null` (walked away), `galleyTick` takes you out (`afterWalkAway: false`, `joined: false`).
  - A stale join with `since` 300 minutes old is cleared by the next tick. So finding 4's path is gone: `takePortion` can no longer see an old `since`.
- **Without the sim's line** (6efe188 alone, or with 0.60.x): `galleyAhead` falls back to the `DECK_CREW` / plan count. `galleyLeave` guards `lineLeave` with typeof. food_check's live-line stand-in passes.
- **New `galleyTick` work every frame** is one `Map.has` and an `ACT` check. No allocation.
- **Tests:** food_check **OK** on merge L (`longest line seen: 12`; live line `{'real': True, 'line': True, ..., 'ate': True, 'left': []}`). I didn't rerun player_check, day_check or cadet_test for 6efe188 (it's WIP; the galley says its checks are pending).
- **Still to do before the combine:** findings 1 (`t: m` on lateMeal) and 2 (no notes from a fresh-start replay / New game). Finding 3's owner goes in the hook register. When player 0.28.34 combines, section 15's own `lineJoin` / `lineLeave` overlap the galley's, which is harmless now that both are idempotent.
