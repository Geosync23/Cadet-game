# Re-review: claude/social-stories c689063..47b02d6 (0.39.12-0.39.17)

Reviewer 1, 2026-10-17. **Verdict: PASS WITH FIXES.** There is one medium fix: queries write the save through `storyM`. The other findings are low.

What the range covers:
- 0.39.12: `momentTrad` / `momentCtx`, `momentWantsVisit`, and `arc_check.py`.
- 0.39.13: theme `needs` are met by `socialFill`.
- 0.39.14: bonds with someone not aboard are frozen and marked `gone`, and `bondOf(id, 'missed')` is new.
- 0.39.15: sparring partners for the rivalry theme.
- 0.39.16: `farewellCrew`.
- c62db59: merges social A 0.36.71, which brings in the combined 0.60.2.
- 10e904f: restores section 13's notes bus and flag store.
- 0.39.17: `voiceOf`'s thread comes from VOICE only for `arc:` threads; themes come from the roster.

Social B's own game lines are all in 20c. No new `schedU` keys.

## The restored section 13 (10e904f)
I redid the merge 10d8805 + c08142c myself, resolving only the build lines. My result is byte-identical to 10e904f's `starship-cadet.html` (`diff` printed nothing). So the restore brings back exactly what the merge should have produced, and nothing else in that hunk was lost.

Other checks on the merge:
- Across the merge, 20c differs only by 0.39.17's one `voiceOf` line (awk-extracted 20c, 773 lines each).
- `name_check.py --branches c689063 47b02d6`: NAMES OK (294 new names, no deleted helper still in use).
- `--branches c08142c 47b02d6`: OK.

## Findings

### 1. Medium: moment queries create saved records for everyone they look at
Path:
- `momentNextId(p)` reads `storyM(p.id).b`.
- `storyM` creates `SHIP.social.stories.m[id] = { b: 0, at: null, hf: null }` on read.
- `momentNextId` runs under `momentWantsVisit`, `momentReady`, `momentHint` and the chat card.
- Since social A 0.36.68 it also runs inside the visit picker's sort comparator.

Evidence (probe p10 on the tip, a fresh game, `momentWantsVisit(p, 20:00 Day 2)` for every crew member):
```
"same": false, "grew": 3162, "mBefore": 0, "mAfter": 75,
"sample": {"nandakumar":{"b":0,"at":null,"hf":null},"kowalczyk":...}
```
Calling `momentReady` for everyone also changes `socSave()` (`readySame: false`). In play, every person whose card you open, or who is checked for a visit, gets a record. That is up to about 3 kB of the 30 kB social budget. My rotation probe already sat at 25.2 kB with strong friendships seeded.

This is the same class of bug as `homeBeatOf` in 0.39.10.

Fix: a read-only peek in `momentNextId`:
```js
const M = SHIP.social.stories && SHIP.social.stories.m;
const b = M && M[p.id] ? M[p.id].b : 0;
```
`momentDone` / `momentShow` keep using `storyM`.

### 2. Low: `momentWantsVisit` ignores `momentReady`'s gates
`momentWantsVisit` checks only `where: visit` and `when`. It does not check the tier, met-days, gap, one-a-day or serious-a-day gates. The visit picker sorts people who "want" a visit first. So on an evening when their beat can't open (for example they had a moment today, or the gap hasn't passed), they still take the evening's visit, and the visit plays no moment.

Fix:
```js
return [].concat(d.where || []).includes('visit') && !!momentReady(p, t, { anywhere: true });
```
`momentReady` already skips `where` when `ctx.anywhere` is set, and it uses `momentCtx`.

### 3. Low: `momentCtx`'s deck falls back to the player's deck
When the person is walking, `whereIs` gives no `placeId`, so `deck` is `undefined`. Section 22's `deck:` condition then uses `deckDef.num`, which is where the player is.

Probe evidence: Holt at 2460 is moving on deck 3, and `momentCtx(...).deck` is `undefined`.

In live play you're with them, so this is right. In paper paths (`momentWantsVisit`, `arc_check`) the answer depends on where the player stands.

Fix: `deck: pl ? pl.deck : (w && w.deck != null ? w.deck : undefined)`.

### 4. Latent: `momentTrad` returns only one tradition when two overlap
Film (20:00-22:00) and observatory night (21:15-22:35) overlap. Between 21:15 and 22:00 `momentTrad` returns `observatory-night` (table order), so a beat with `trad: film` would fail during the overlap. Today only `observatory-night` is used in moments (marrow:4, tomas:7), so nothing breaks yet. If a moment ever says another tradition, test against all traditions on now.

The window edges are right: 1274 gives `film`, 1275 and 1354 give `observatory-night`, 1355 gives `null`. Day 0 and negative minutes give `null` with no exception. With section 18 missing, the `typeof` guard gives `[]`.

## Checked and fine
- **Not aboard (0.39.14), on the tip's own roster:** rotation day 35 has teague-theo out and bramwell-basil in; the reserve is in SOC from the start.
  - Hour by hour and one jump over days 34-37 give identical bonds (`same: true`).
  - Teague's bonds are marked `gone@36`, the day after he leaves (`socAboard` is true through his leave day).
  - `bondOf(x, 'missed')` gives teague-theo for his friends (calder, pell, torres-zeke...).
  - Frozen bonds skip fading, best friends, mentors and couples.
- **Sparring partners (0.39.15):** they are deterministic, one per rivalry person at 04:00, aboard only, and stay frozen when one of them leaves. Example: `holt:moreau-signe` (Moreau leaves on day 77).
- **farewellCrew (0.39.16):** it is pure. It reads the weekly snapshot (`affinityPlan`), `socAboard` and `leaveDay`, and gives the same answer twice.
  - Nothing calls it yet; it is for section 14's leavers in the bay at 14:30-15:00.
  - It excludes anyone leaving the same day and the player.
  - My probe got `[]` for Teague because I seeded affinity live after the weekly snapshot, so this is not a finding. When the sim wires it in, check that the friends it lists aren't also needed at social A's 14:00 Sunday farewells or on duty.
- **0.39.13 `needs`:** `socialFill` for home, family, hobby and since only reads the roster (`relTier` doesn't create records).
- **0.39.17 threads:** on the tip, VOICE gives `arc:` to the ten story crew (Kovac's `arc:kovac` beats the roster's `notgood`). Saruth (a guest) now takes the roster's `lonely`.
- **arc_check on the tip** (it now carries the writers' content through 0.60.2):
  - ARC CHECK OK: all ten crew arcs finish, the last on day 55 (Tomas 7); all four home arcs reach 6.
  - It uses the real path (`momentReady` -> `momentShow` -> `dialogueStep`, `homeCall`, `socialTo`).
  - Appointments and visits are stand-ins (pushed into `SHIP.device.appts`, `VISIT` set directly), so it shows the arcs can finish, not how often play gets them there.
- **social_check on the tip:** OK. Save 21143 bytes with the reserve; same twice and jump both True.

## Tests
- name_check as above.
- Browser probes p9, p10 and p11 (`?nosave&debug`), arc_check and social_check, each run under the browser lock: no page errors.
