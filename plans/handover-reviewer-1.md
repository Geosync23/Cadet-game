# Handover: adversarial reviewer 1 (Pillar 4)

**Role:** adversarial reviewer 1. Before a helper's branch is combined, try hard to break it; report real problems, ranked, with evidence. No game code, ever. Push only review notes and reviewer tools to `claude/reviews`.
**Lead:** session_01PJtmxWgAPLebXSZKP6ZRpG (from 2026-10-17 ~02:40; before that session_01PxXKwc5mkC7tV5MPi3p7PP). **Build master:** session_012K7RZ3oSX2vpBb1rR66MBh. Reviewer 2 covers dialogue, traditions, device, decks, tiles, content.
**Chain of command (the user's rule):** the user → the lead → everyone. Never contact the user; report to the lead (and the helper).

## My seats (session ids)
| Seat | Branch | Session | Last reviewed | Verdict |
| --- | --- | --- | --- | --- |
| Sim engineer | `claude/sim-engineer` | session_01R6RBwwBM9aorpsqDCrztDU | 56e0a89 (0.26.24) | PASS. 0.26.25 coming: the aboard set (crewStay/crewLeaving/crewArriving/crewState), the first-launch switch (see Open 1), the dinner edge |
| Onboarding | `claude/arrival` | session_01KaHzfqSqF8B4bkNFrH1tsx | 11ceb84 (0.42.12); 07642cc is check-only (intro_check part 9) | PASS |
| Social A | `claude/social` | session_012pK2XVi5UhqEd28fakYk68 | 73c3938 (0.36.43) | PASS |
| Social B | `claude/social-stories` | session_019aEJaAGyZir9oq47CBRfA3 | 192e9c8 (0.39.2) | PASS WITH FIXES (save size, the lead decides). 0.39.3 (moments) WIP, not reviewed |
| Crew designer | `claude/deck-plans-1-2-6` | session_01JScnVG158eYAHYvKDz3jZG | 98df62f (0.16.13) | PASS |
| Systems (on call, the lead added it) | `claude/ship-systems` | session_01TqLepvhqDZRwFj7ZuLb6Xa | f211129 (0.33.39) | PASS |

Every review note is in `plans/reviews/<branch>-<commit>.md` on `claude/reviews`; read the latest per branch before re-reviewing.

## Open items to follow up
1. **The first-launch arrival, crossing fixes.** Arrival 0.42.12 reads section 13's `ARRIVING` (`if (typeof ARRIVING !== 'undefined' && ARRIVING && !SAVED) introBegin();`). The sim's coming 0.26.25 removes `ARRIVING` and expects section 21 to call `newGameStart(true)`. Combined as they stand, the typeof guard hides the gap: a first launch starts on Monday again. Both seats and the lead are told. Check intro_check part 9 on their merge.
2. **Social save size:** 27.8 kB with the reserve, mostly social B's `affWeek` snapshots. **Decided (the lead):** option (a), snapshots keep only pairs with |aff| ≥ 30 (section 14 seats on ±30; the lead changed it from 40), budget 30 kB. Check social B 0.39.3 keeps ≥ 30 pairs, that seating on paper is unchanged by it, and that social_check.s limit is 30000.
3. **Sim 0.26.25 review:** on rotation days (35, 77, ...) the leaver and the newcomer are both "aboard" by day and share one bed. Run day_check on day 35, and check that `ROSTER_ROTATIONS.out` (now a list of ids) is read right.
4. **Social B 0.39.3** (moments engine) once it's marked final.

## Tools (on `claude/reviews`)
- `name_check.py`: `python3 name_check.py COMBINED.html` (names declared twice, and `node --check`); `--branches BASE REF...` (names two branches both add; names a branch deleted but still uses). On a re-review, run `--branches <last reviewed> <new>`: it caught `socP` in social f05d7db. The build master runs it on every combine.
- `plans/review-checklist.md`: the checklist helpers apply themselves when the team is scaled down.
- In my scratchpad (not pushed; quick to rebuild): `probe.py` (load a build, run JS blocks, `STEP n`, `RELOAD` with storage kept), `upgrade.py` (play in an old build, open a new one in the same storage), `roster.js` / `r2.js` / `r3.js` (roster diffs, staffing, rotations). `probe.py` is about 40 lines on top of cadet_test.py's `Game` setup. Use the `?debug` query (saves on) to test saves and New game; `?nosave&debug` for everything else.

## How I test
- Setup: `pip install playwright`; three r128 in `/tmp/cadet-work/three` (`npm pack three@0.128.0`); `CADET_CHROME=/opt/pw-browsers/chromium`. One browser check at a time.
- **Scratch merges:** a `git worktree` at the branch, merge the others, resolve the build-line conflicts (keep one), then name_check and the seat's checks. Most real bugs only showed up combined: the introOn clash (arrival + social), the flags left over (arrival + sim), the reserve test shadowed (social + crew), the save size (social B + crew).
- **Prove in the browser,** not by reading alone: New game, a fresh first launch (clear localStorage, `RELOAD`), a reload mid-walk, chatLine on a real person.

## Gotchas found so far (worth looking for again)
- `typeof X` doesn't guard a `const` that hasn't been declared yet (the temporal dead zone): it throws. It bit sim's `arriving()` → section 21's `introWanted`, and the checks of not-yet-baked `VOICE`.
- A test that sets `window.X` is shadowed by the game's own `const X`.
- A default argument that calls a deleted helper only fails at run time (`node --check` passes).
- Day 0 minutes are negative: `%` with negative numbers, regexes for `\d+`, `t.day >= 1` checks.
- New game isn't a reload: every section with state must reset (section 13 now sends `simNote('newGame')`).
- name_check reads only lines that start with a declaration; a declarator carried on to the next line is handled since 4ad33f0.

## Memory
Handed over (this note written) at about half memory, ahead of the 70% rule; it's kept current as reviews land.
