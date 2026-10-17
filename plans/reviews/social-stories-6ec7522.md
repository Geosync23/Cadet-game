# Re-review: claude/social-stories 368ae8a..6ec7522 (0.39.6)

Reviewer 1, 2026-10-17. **Verdict: PASS** (two low content notes, no blocker).

Range: 37b3b69 (arcCrew, `where: 'meal'`), 77c30c9 (STORY_FAVOURS: brennanSage, pellPractice, liftBrakes), c42d809 (merge of social A 0.36.57: build line only, the html merged clean, `git show --cc` empty), then notes-only commits up to 6ec7522 (6ec7522 itself is empty; game code identical to 0191177). Social B's own game lines in the range are 20c only. No new `schedU` keys, no `Math.random` / `Date.now` (grep of `git diff 368ae8a 77c30c9`: 0 hits).

## Findings

### 1. Low (content): the lift-brakes favour is a lamp swap with a lift title
Path: Kovac's beat 3 (`kovac-zainab:3`), practical reply `favour: liftBrakes` -> `storyFavour` -> `favourPost({ kind: 'lamp', where: p.work.place, parts: ['lamp'] })`.
Evidence (probe on the full merge with the content branch's 45 MOMENTS baked in, `storyFavour(socP('kovac-zainab'), 'liftBrakes')`):
`"Check the lift brakes with Zainab", chore "lamp", steps [["fetch","5-parts-1|5-parts-2|5-parts-3|5-parts-4",5], ["lamp","5-bench-1",5], ["return",...,"kovac-zainab"]]`.
So the player is sent to Deck 5's parts shelves for a lamp, then to the works bench (not the lift), and the stop is labelled as a lamp job. pellPractice is similar but milder: its one stop at 5-bench-1 carries the tag `pickup`.
Fix (inside the "no new jobs" ruling): drop `kind: 'lamp'` and `parts` from liftBrakes and give it a plain stop, e.g. `stops: [{ deck, placeId: <the lift lobby or its panel place>, mins: 15, tag: 'favour' }]` (as brennanSage does with the garden), and use tag `favour` for pellPractice's stop.

### 2. Low (to the build master, not a code bug): arcCrew needs the content branch's VOICE baked with the MOMENTS
On the tip and on the full merge, without content's VOICE, `voiceOf('torres-zeke').thread` and `voiceOf('kovac-zainab').thread` are themes, not arcs, so `arcCrew('torres') === 'torres'` and `beatOf('torres')` stays 0 (probe p1: `arcs: {"torres": "torres", "kovac": "kovac"}`, thread list without them). With content's VOICE baked in as well (probe p5 on the tip and on the full merge): `arcCrew('torres') === 'torres-zeke'`, `arcCrew('kovac') === 'kovac-zainab'`, `beatOf('torres')` follows Torres's `rel.arc` (3 = 3), and Torres and Kovac get `torres-zeke:1` / `kovac-zainab:1` as their next moments; all 45 load. So the code is right; bake VOICE and MOMENTS from the same content commit.

### Test-only (no action now)
Social B's own social_check at 6ec7522 still has social A's old beatOf test that leaves a rel record for Torres: on the full merge `FAIL affBand, moodOf or purity wrong` with B's copy, OK with social A's copy (9c5b27a). 52561f6 (0.39.7's merge of social A 0.36.58) brings the fixed test in.

### Out of range, for others (seen while testing)
- **Social A (section 20, since 0.36.21):** on handing a favour back, `fk = f.kind === 'lamp' ? 'lamp' : ...`, but `f` is the job, whose `kind` is always `'favour'` (the chore is in `f.chore`). Lamp favours are remembered as `fav.job` and send `simNote('favour', { fav: 'job' })`, so `fav.lamp` / `cue:favour.lamp` never happen. Fix: `f.chore === 'lamp'`.
- **Sections 13/17:** New game keeps `SHIP.jobs` when the clock goes forward (Day 0 arrival -> "Skip to Monday"): probe p2 (`?debug`) posted two story favours on Day 0, `newGameStart(false)`, and `myFavours()` still listed both (`machinesReset` only runs when time goes back). Any favour or claimed job does the same. Fix: reset jobs on `simNote('newGame')`.

## Checked and fine
- **The 45 moments load** (content's MOMENTS and MOMENT_THEMES baked into the tip and the full merge): `momentDef` gives all 45; every `who` is a crew id; the only speaker not in `SOC.crew` is `saruth` (holt:4), the Envoy, a ROSTER_GUESTS guest that section 18 knows. Unknown arc: `arcCrew('nobody') === 'nobody'`, `beatOf('nobody') === 0`, and no rel record is made. A crew member who left stays in SOC.crew (fixed at load, reserve included), so arcCrew's cache never goes stale with the roster; it rebuilds when VOICE_SRC changes.
- **Favour types match section 20's:** the three use section 17's `favourPost` / `favourAccept` the way section 20's `favourOf` does (fetch: `bring` + a pickup stop; lamp: `kind`, `where`, `parts`). They're accepted at once, in `myFavours()`, not `myJob()`; `favourOf(pell)` returns the story favour, so handing it back on his card works. Unknown favour id or an unknown person: `storyFavour` returns false. Day 0 (`setShipNow(-300)`): `favour:brennan@-300`, expires 1860, fine.
- **`where: 'meal'`:** Holt is at a mess seat at breakfast 07:10-07:55 and dinner 19:40-20:00 on days 2 and 3; every rostered crew member matches at some meal.
- **Save:** story favours live in `SHIP.jobs`, saved by section 17; a real `saveGame()` + reload (`?debug`) gave them back (14.8 kB save). Social part on the full merge 22956 bytes (limit 30000, the reserve in: 86 crew); tip 15113.
- **Determinism:** social_check "the same twice" and "two days in one jump" both True on the tip and the full merge.
- **Merges:** social-stories + social A tip (d1e97bd): only the two build lines conflict, DEV_NOTES and social_check merge clean, name_check OK.

## Tests
- `name_check.py --branches 368ae8a origin/claude/social-stories`: NAMES OK (6 new names). `name_check.py` on the full merge: OK.
- Full merge: worktree at the arrival tip of 04:40 (0.42.19) + sim-engineer, deck-plans-1-2-6 (4613d43, the reserve), social (62ae491), social-stories, player-needs, galley-food; only build-line and DEV_NOTES-table conflicts (cadet_test.py: the toast style line, kept the superset).
- social_check (B's copy): tip OK; full merge FAIL on the test-only purity item above. social_check (A's copy, 9c5b27a): full merge OK.
- Browser probes (`?nosave&debug`, `?debug` for save/New game): load, arcCrew, the three favours, meal, Day 0, save round trip; no page errors.
