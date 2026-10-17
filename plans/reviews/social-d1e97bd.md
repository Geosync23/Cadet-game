# Re-review: claude/social 945c447..d1e97bd (0.36.52-0.36.58)

Reviewer 1, 2026-10-17. **Verdict: PASS WITH FIXES.**

Nothing crashes, nothing breaks determinism or saving, and social_check passes on the full merge. Two fixes are about contracts with other seats. Neither breaks the game today, but the first means section 21's three "they come and find you" beats will mostly never happen in play.

Also covered: 9c5b27a (the test-only beatOf fix, after d1e97bd) and 0.36.59 dc80136 (the tip, see the end).

## The five things asked
1. **The beatOf test leaving a rel record for Torres: fixed** in 9c5b27a (test only: the check copies `SHIP.rel[id]` first and puts it back, or deletes it). On the full merge social_check reports `"beatMap": true`, `"pure": true`, then SOCIAL CHECK OK.
2. **socialSeekAsk contract:** the call shape matches on both sides. Section 21 passes `id`, `{ from, until, why }` in absolute ship minutes, and social reads the same. What the call is supposed to *do* doesn't match: see finding 1.
3. **Theme fill-ins:** `socialFill` works on the merge and returns null when a field is missing (the probe below: none of 86 crew gives null; social_check's stripped Tomas gives `since: null` and falls back to his habits for `hob`). But no dialogue line ever reaches them, and `{family}` disagrees with the roster about "my": see finding 2.
4. **Hash keys:** none new. The added lines use `U(624)`, `U(634)` and `U(648)`, all already in 945c447 (634 is in code moved into `seekShow`).
5. **Determinism, save, New game, Day 0:** OK (details under "Passed").

## Findings

### 1. (Medium) socialSeekAsk: section 21 expects the person to come to you; social waits for you to happen to be near them
- **Section 21 (arrival a86d052)**, hook register row: "`socialSeekAsk` (20): that person comes and finds you in the window". DEV_NOTES 0.42.18 says the same: "Tomas, Pell and Zainab come and find you". The 'tomas' step says `where: 'the junior common room or Bunk 1'`.
- **Social (0.36.58)** only shows the wave when that person is *already* on your deck, within `SEEK_NEAR` of you, and free. Nobody walks them to you: `introPlan` drops the `where: 'seek'` beats (`beats.filter(x => x.where !== 'seek' ...)`, around line 8295 on the merge), so these three people keep their ordinary day.
- **Evidence** (full merge, `?nosave&debug`, `introBegin('Sam')`, `whereIs` every 15 minutes in each window):
  - Tomas, Day 0 19:00-22:00: `leisure`, **Deck 2** (stargazing) for the whole window. Your arrival evening is on Decks 3 and 4 (the mess, then your bunk), so his wave only fires if you happen to walk to Deck 2.
  - Pell, Day 3 18:30-20:00: `leisure`, Deck 3. This one can fire if you're near him.
  - Zainab, Day 4 16:30-18:00: `work` on Deck 5 until 17:00, then `wash`, the lift, then `dinner` on Deck 3. It fires only if you're next to her at dinner. Her favour is still forced that day, but only if you chat with her.
- **What works:** once someone *is* near you, the real path does work. Probe: ask Orla, put the player 1 m from her, step 120 frames: `SEEK = ishikawa-orla`, chip "Orla calls out: \"Got a minute?\"", ask marked `done`.
- **Fix (the lead decides who owns it).** Either:
  - (a) section 21 gives each seek beat a place in `introBeats`, for example Tomas in the junior common room or Bunk 1, as the step's own text says; or
  - (b) while an ask is live, social walks the person to the player, the way the escort does.

  Then make both hook-register rows say the same thing. social_check part 14 only tests the time windows on paper, so add one in-play check that the wave actually fires in the window.

### 2. (Low-medium) The {home} {family} {hobby} {since} fill-ins never reach a line, and {family} would come out as "my my ..." if they did
- **Nothing calls them.** Section 22's `linesFill` fills these four itself from the raw roster field (`case 'home': case 'family': case 'hobby': case 'since': return p[k] ? String(p[k]) : null`). Its `SOCIAL_FILL` list (`me, partner, friend, best, rival, mentor, mentee, boss, thing, trad`) doesn't include them. Every other `socialFill` caller asks only for 'trad', 'thing' or the bonds. The same is true on dialogue 47ba9e8, content, writer-commons and ship-integration. So 0.36.55/56 change nothing in play: the habit fallback for {hobby} and the growing {since} never show.
- **{since} doesn't grow in play.** Rotation newcomer bramwell-basil (arrives Day 35), on Day 61: `socialFill(p,'since')` = "three weeks", but `linesFill('{since}')` = "one week".
- **The "my" clash.** Crew designer 0.16.14 and the head writer agreed that `family` is written to read *after* "my", and lines say `my {family}`. Social's `{family}` adds "my" itself: `socialFill(tomas,'family')` = "my little brother, who I write to every week". If section 22 ever sends {family} through `socialFill`, a writer's "I miss my {family}." becomes "I miss my my little brother, who I write to every week." (probe output). Today the raw path gives the right "I miss my little brother, ...".
- **Fix:**
  - `socialFill`'s `{family}` returns the roster field as written: drop the "my " prefix and the article stripping, which do nothing since 0.16.14.
  - The dialogue engineer adds `'home', 'family', 'hobby', 'since'` to `SOCIAL_FILL` (one line in section 22).
  - Update social_check's `fam` expectation.
  - Or, if the lead prefers, social drops the four and leaves them to `linesFill`. Either way, write down in the hook register which one fills them.

### 3. (Low) {since} stays frozen for everyone aboard at the start
Tomas's roster `since` is "one week", and on Day 61 both paths still say "one week". Five crew have "one week" and eight have "two weeks", so the oldest hands are fine but the newest juniors are not. **Fix:** for crew aboard from Day 1, when the roster phrase is in days or weeks, add the game days played (or work it out from `SHIP.time.day` plus the phrase). Otherwise ask the writers to keep {since} out of lines for the short ones.

## 0.36.59 (dc80136, the tip after d1e97bd), reading only
- It's one line in `beatOf`: `typeof homeBeatOf === 'function' && /^home\./.test(arcId)` sends home arcs to social B's `homeBeatOf`. It's in section 20 and typeof-guarded. `homeBeatOf` is a `const` declared later in the file (the temporal dead zone), but `beatOf` only runs in play, so that's fine.
- (Low) `homeBeatOf` calls `homeState()`, which *creates* `SHIP.social.stories.home` when it's missing. So a line condition `beat:home.mum.1` now writes to the save. That breaks the "queries are pure" rule: `socSave()` before and after differ. It's harmless in content but will trip any purity check. **Fix (social B's):** `homeBeatOf` reads `(SHIP.social.stories || {}).home` without creating it.
- I haven't run it in the browser: the lock queue was long. No other game code changed in 0.36.59.

## Passed
- `name_check.py --branches 945c447 d1e97bd`: NAMES OK. Same for `9c5b27a`. `name_check.py` on the combined html: NAMES OK, node --check parses.
- **Full merge** (arrival b4f0ac4 + sim 971b4c7 + crew 4613d43 + social 9c5b27a + social B 507479e + player 3713f20 + galley 944f520, conflicts only on build lines, DEV_NOTES and the cadet_test style line, both sides kept): `social_check.py` SOCIAL CHECK OK.
  - The same twice: True. The two-day jump matches hour by hour. The real bus: cue True. Purity True.
  - Save 22,956 bytes (limit 30,000), and save then load gives back the same.
  - Asked-for waves: `{'ok': [True, False], 'win': [False, True, False], 'saved': True, 'fav': True}`.
  - Note: social B's tip has since moved to 9304c37. My fetch raced with another session's, so the merge has 507479e.
- **socialSeekAsk inputs:** unknown id gives false, NaN `from` gives false, a duplicate gives true and adds nothing.
- **Day 0:** Tomas's ask at negative minutes works. Section 21's favour day `Math.floor(from / 1440) + 1` is right for negative `from` too.
- **Save** through the real `saveGame()` with storage on (`?debug`), then a reload: `seekAsks` come back the same. Bad entries are filtered out (a wrong `id` type, null, a `from` that isn't a number), and an old save without the field gives `[]`.
- **New game:** `newGameStart(false)` clears `seekAsks` (`socReset` rebuilds `SHIP.social`).
- **Cue records** (0.36.53): the new `who` / `dept` / `room` fields survive `socLoad`'s filter. `repDeptOf` is cached per machine. Nothing else on the bus reads gift's new `who` as the doer: social's `you` also reads `from: 'you'`, and section 21's settleNote listens to `favour` only, which the new favour note now ticks ("Do a favour").
- **Per frame:** the ask check runs inside `socialSeek`, once per social minute. It's a `find` over a list of at most a few asks.
- **intro_check on the merge: not run yet.** My first run was killed while it waited for the browser lock. The second run is still in the lock queue: it writes to `/tmp/claude-0/-home-user-cadet-game/1598d9e8-8f30-5fac-8e56-61dd4f5bfb08/scratchpad/intro.txt`, ending with an `exit N` line. intro_check doesn't test the seek beats anyway: it has no `seek` in it.

The merge worktree is at `/tmp/cadet-work/rv-social-merge`. It isn't committed past the sim/crew/social/social B/player/galley merges: the working tree drops four duplicate `GAME_BUILD` lines, and that edit isn't committed.
