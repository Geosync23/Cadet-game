# Review: claude/player-needs 5e61e12..fabc552 (0.28.30-0.28.34)

Reviewer 1, 2026-10-17. **Verdict: BLOCK** (with the sim's real food line, once you're served nobody else is ever served)

Scope:
- 0.28.30: no queue count or countdown; the call picker at a booth (`homeBooth`); Mail keeps a `play` field.
- 0.28.31: the food line asks Leave/Stay; served, you hold your tray and choose a seat.
- 0.28.32: the needs strip and the activity line (7a99461 didn't load because `NEED_LOW` was declared twice; fixed in 1d647a3).
- 0.28.33: the strip folds to a heart, saved.
- 0.28.34: you move with section 10's real line (`lineJoin`/`lineSpot`/`lineLeave`).
- fabc552: player_check fixes.

All game lines are in section 15 apart from the build line. Hooks into other sections (`homeBooth`, `lineJoin`, `lineSpot`, `lineLeave`) are `typeof`-guarded and do nothing when those sections are missing.

Scratch merge B: worktree at origin/claude/arrival d24b017 (0.42.20), with full merges of sim 0cf991a (0.26.30, the real line), origin/claude/deck-plans-1-2-6 and player fabc552. I kept HEAD's build lines, both sides of DEV_NOTES, the player's own player_check.py, and the union of cadet_test's style line. Probes are in `scratchpad/rv/`: `line.py`, `strip.py`, `bunk.py`.

## Findings (most severe first)

### 1. Once you're served, you stay at the front of the sim's line, and nobody is served again (BLOCK, merge with sim 0cf991a)
Section 10's contract (sim 0cf991a, comment above `LINE_AT`) says: "you're served by section 15, which calls lineLeave('player')". `lineTick` skips `'player'` at the counter (`if (f === 'player') continue;`). Section 15 only calls `lineLeave` in `actEnd` when `A.kind === 'queue' && !A.o.dish`, that is, when you leave without food. When you're served, the queue's `until` sets `A.o.dish`, so `lineLeave` is skipped. `'player'` stays first in `LINE` for good, `lineTick` never serves anyone behind you, and the line grows all evening.

Evidence (merge B, `line.py` part A: Day 1 18:05, tap the Servery, step frames; columns are `[time, ACT kind, phase, your tray, servLine() first 6, LINE length, LINE_LOG.served, ...]`):
```
["18:07", "queue", "do", null, ["player"], 1, 0, ...]
["18:23", null, null, "Brennan's spiced lentils", ["player", "shah-dara", "ferreira", "janssen-hugo", "mensah", "rina"], 32, 0, ...]
ten ship minutes after you were served: ['18:59', None, None, "Brennan's spiced lentils", ['player', 'shah-dara', ...], 32, 0, ...]
```
You've walked off with your tray, 32 people stand behind a 'player' who isn't there, and `LINE_LOG.served` is still 0 at 18:59.

**The same ghost appears without being served** (part B): tap the Servery, then walk somewhere else before you reach the line.
```
tap True ['18:40', 'queue', 'walk', None, ['player'], 1, ...]
walked off: ['18:41', None, None, None, ['player', 'zielinski-oona'], 2, ...]  player in LINE: True
```
`playerTap` calls `lineJoin('player')` at the tap. Leaving during the walk takes `actUpdate`'s `if (A.phase === 'walk') { if (player.onArrive !== A.cb) ACT = null; return; }`, which clears `ACT` without `actEnd`, so `lineLeave` never runs. `actStart`'s "You can't get there just now" branch (`ACT = null`) leaks it the same way.

**Fix:**
- Call `lineLeave('player')` whenever a queue activity ends, served or not: drop the `!A.o.dish` condition, or call it where the queue's `until` takes the portion.
- Join on reaching the back, as the sim's contract says ("joined on reaching its back"). Call `lineJoin` in `actBegin` for `queue`, not in `playerTap`, so an abandoned walk never joins. Otherwise, also call `lineLeave` in the two `ACT = null` paths.
- Also consider serving you when `lineFront('player')` is true, rather than on `galleyJoin`'s `turnAt` estimate. As it stands, your turn comes on the estimate wherever you are in the line, and crew who are physically ahead of you can be passed.

Leave/Stay itself works with the real line (part C): a floor tap in the line shows the question and keeps you queued; Stay hides it; Leave takes you out of `LINE`:
```
floor tap in line: ['18:52', 'queue', 'do', None, ['player'], 1, 0, [33, 6], False]
Stay: ['18:52', 'queue', 'do', None, ['player'], 1, 0, [33, 6], True]
Leave: ['18:52', None, None, None, [], 0, 0, [33, 6], True]  in LINE: False
```

### 2. Your tray is kept through the night and onto other decks (low)
`SHIP.player.tray` is cleared only when you sit at a `mess-seat` and in `playerNew`. If you walk away with it, you carry it all evening. You go to sleep holding it and wake holding it, then eat last night's dinner at breakfast. Meanwhile the Servery refuses you ("You already have your tray"), so you can't queue again until you've eaten it on Deck 3.

Evidence (1d647a3, phone viewport, `strip.py`; the tray code is the same in fabc552):
```
holding before sleep: ['Lentil stew', 'tray']
after sleeping to Day 2, Tuesday 06:00 : ['Lentil stew', 'tray', 4]
Deck 3 next morning, still: ['Lentil stew', 'tray', 'Day 2, Tuesday 06:00']
```
**Fix:** drop the tray (back to the rack, or "you leave it on a table") on a time skip (`SIM_ADVANCE`), on leaving Deck 3, or after N ship minutes. Optionally let a Servery tap with a tray return it.

### 3. The needs strip rebuilds strings and writes to the DOM every frame (low, phones)
`stripTick` runs every frame from `floatsTick`. Each frame it calls `NEED_KEYS.filter(...)`, builds `sig` with `map().join()` and `toFixed`, and calls `el.querySelector` on a change. While any need is under `NEED_LOW`, `sig` includes the pulse `g.toFixed(2)`, so it changes every frame. All six icons then get style, transform and textContent writes every frame, plus the folded heart since 0.28.33. During an activity, `actBar` then reads `sb.offsetTop`, `offsetHeight` and `offsetWidth` straight after those writes, which forces a layout every frame.

Evidence (1d647a3, a MutationObserver on `#needStrip`, 30 frames):
```
mutations over 30 frames, needs steady: 0
mutations over 30 frames, one need low: 353
```
**Fix:**
- Do the pulse in CSS (a `low` class with a keyframe animation), or update it at most every few frames.
- Build `sig` without allocating, for example as a number from the six rounded values.
- Keep the `.nsMini` element in a variable.
- Cache the strip's size in `actBar` and refresh it only on open, fold or resize.

### 4. The "Leave the queue?" box stays up when the queue ends some other way (low; from the code)
`queueAsk` shows `#qAsk`, and only its own buttons hide it. If you tap while queued (the box shows) and then get served, or hit a time skip, or change deck, the box stays up. "Leave" then does nothing (`queueLeave` returns because `ACT` isn't a queue) while you hold your tray.
**Fix:** hide `#qAsk` in `actEnd` when `A.kind === 'queue'`.

## Checked and fine
- **`homeBooth` and the mail `play` contract with social B** (origin/claude/social-stories 244fe0f):
  - `homeBooth(t = shipNow())` is a function declaration and returns false when a dialogue is up. Section 15 calls it with no arguments once, in `actBegin` for `call`; player_check counts 1.
  - Social B queues recordings as `SHIP.social.mail` entries with `play: 'home:<k>'` and delivers them with `mailSend(x)`. The new `play` parameter carries the field through, and `mailLoad` keeps a string `play` (cut to 60 characters).
  - Old saves without `play` load unchanged, and social B's `homeMailOf` falls back to matching sender and subject. player_check's save test keeps `Kept|home:gran`.
- **0.28.33 fold:** `save.player.stripFold` is read only when it is `=== true`. An old save, `?nosave` or a junk value gives false. It's a display preference, so not resetting it on New game is fine.
- **Phone layout** (390x844, 1d647a3): the strip sits at 14,124 (187x36), under the Device button (86-116). Open, it's 210x129. There's no horizontal overflow (`scratchpad/rv/strip-open.png`).
- **Lines `typeof`-guarded:** `lineJoin`, `lineSpot` and `lineLeave` are checked at call time and run only from frames and taps, so there's no TDZ. `lineAt` checks `isFinite`.
- **name_check:** `--branches 5e61e12 1d647a3` NAMES OK. `--branches 5e61e12 7a99461` gives NAMES CLASH (`NEED_LOW` twice, fixed in 1d647a3). `--branches 5e61e12 fabc552` NAMES OK (16 new). Merge B html: NAMES OK, node --check parses.

## Tests
(results below)
