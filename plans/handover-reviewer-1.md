# Handover: adversarial reviewer 1 (Pillar 4)

**Role:** adversarial reviewer 1. Before a helper's branch is combined, try hard to break it; report real problems, ranked, with evidence. No game code, ever. Push only review notes and reviewer tools to `claude/reviews`.
**Lead:** session_01PJtmxWgAPLebXSZKP6ZRpG (from 2026-10-17 ~02:40; before that session_01PxXKwc5mkC7tV5MPi3p7PP). **Build master:** session_012K7RZ3oSX2vpBb1rR66MBh. Reviewer 2 covers dialogue, traditions, device, decks, tiles, content.
**Chain of command (the user's rule):** the user → the lead → everyone. Never contact the user; report to the lead (and the helper).

## My seats (session ids) — refreshed 2026-10-17 ~10:20 by reviewer 1 (session 2)
Lead: **session_01KPJMYjXAPkNUcrQ8VRkhLE**. Build master 2: **session_01F8ph7FKqViF3heRn94YgBr**. Reviewer 1c (notes on claude/reviews-3): **session_01YcSJkhhJ2MnCjsJs7QV8ud**; owns player (from 5e61e12), arrival 0.42.20+ and the roster. Reviewer 2b has galley 0.29.33+.
| Seat | Branch | Session | Last reviewed | Verdict / open |
| --- | --- | --- | --- | --- |
| Sim engineer 4 (10/13/14/17) | `claude/sim-engineer` | session_01EJUGywZv9BpcUezjXES9AC | 6e87e6b (0.26.33) | PASS WITH FIXES. MUST (0.60.3): Calder's 3-mess-9 shared with Torres (introLay free() ignores occ.res). food_check fails on full merge + ship-events Sunday day 7 (being traced). 236810f (0.26.34) addendum in progress. Deferred should: breakfast tray return lateness |
| Galley (16) | `claude/galley-food` | session_018cicfPQZQXbxmtn6ygmL84 | 6abd36b PASS WITH FIXES; final 40166d6 (0.29.32) in progress, gates 0.60.3 | galley owns the player's line membership |
| Social A (20) | `claude/social` | session_012pK2XVi5UhqEd28fakYk68 | 2cfbc63 (0.36.76) PASS WITH FIXES | news uncapped; --long samples every 28 days (peaks missed); knownPack keyed by roster position |
| Social B2 (20c) | `claude/social-stories` | session_014A3w2gK8FBNWs66YC3LfME | 3947822 (0.39.21) PASS WITH FIXES | arrival start never packs bonds (negative since) |
| Onboarding 2 (21) | `claude/arrival` | ? (ask the lead) | partial 54d7911 (b7ad3e9) | 1c owns arrival now |
| Device engineer 3 (19) | `claude/device` | session_01SskqNx45iEGyQq2W9Fjg5Y | partial ee3fcdd | off my queue |

Every review note is in `plans/reviews/<branch>-<commit>.md` on `claude/reviews`.

## Open items to follow up
1. The lead's long-play save rule: every saved social part has a hard bound by design with its worst case in DEV_NOTES; social save <= 30 KB at day 140 and < 40 KB at any length; --long to day 280. My advice (sent): measure EVERY day from the real day-0 arrival start, not every 28 days from day 1 (peaks: 31.4 KB day 115/130, 35.6-35.7 KB day 242).
2. The jump test on the newest full merge differed in social A's cues, rep and noteq (seen by the social B 0.39.21 review; not attributed).
3. For the dialogue engineer: section 22's linesFill can add {home} {family} {hobby} {since} to SOCIAL_FILL.
4. For ship-events: events_check fails on ship-events 4e72597 alone at day 231 (3-store-1 double).
5. social and sim-engineer conflict in player_check.py (not a build line).

## Tools (on `claude/reviews`)
- `name_check.py`: `python3 name_check.py COMBINED.html` (names declared twice, and `node --check`); `--branches BASE REF...` (names two branches both add; names a branch deleted but still uses). On a re-review, run `--branches <last reviewed> <new>`: it caught `socP` in social f05d7db. The build master runs it on every combine.
- `plans/review-checklist.md`: the checklist helpers apply themselves when the team is scaled down.
- In my scratchpad (not pushed; quick to rebuild): `probe.py` (load a build, run JS blocks, `STEP n`, `RELOAD` with storage kept), `upgrade.py` (play in an old build, open a new one in the same storage), `roster.js` / `r2.js` / `r3.js` (roster diffs, staffing, rotations). `probe.py` is about 40 lines on top of cadet_test.py's `Game` setup. Use the `?debug` query (saves on) to test saves and New game; `?nosave&debug` for everything else.

## How I test
- Setup: `pip install playwright`; three r128 in `/tmp/cadet-work/three` (`npm pack three@0.128.0`); `CADET_CHROME=/opt/pw-browsers/chromium`. One browser check at a time.
- **Scratch merges:** a `git worktree` at the branch, merge the others, resolve the build-line conflicts (keep one), then name_check and the seat's checks. Most real bugs only showed up combined: the introOn clash (arrival + social), the flags left over (arrival + sim), the reserve test shadowed (social + crew), the save size (social B + crew).
- **Prove in the browser,** not by reading alone: New game, a fresh first launch (clear localStorage, `RELOAD`), a reload mid-walk, chatLine on a real person.

## Gotchas found so far (worth looking for again)
- Parallel browser runs clash: cadet_test.py's Game copies every build to $CADET_WORK/test/_run_<name>.html, so give each parallel job its own CADET_WORK (with a test/ folder and a `three` link). Never share a probe script between agents (one was overwritten with a hard-coded build path).
- Save-size checks that sample every 28 days miss the peaks: measure daily, from the real day-0 arrival start.
- A mid-line `//` comment silently disables the rest of the line (social 0.36.61): name_check and node --check both pass.
- `typeof X` doesn't guard a `const` that hasn't been declared yet (the temporal dead zone): it throws. It bit sim's `arriving()` → section 21's `introWanted`, and the checks of not-yet-baked `VOICE`.
- A test that sets `window.X` is shadowed by the game's own `const X`.
- A default argument that calls a deleted helper only fails at run time (`node --check` passes).
- Day 0 minutes are negative: `%` with negative numbers, regexes for `\d+`, `t.day >= 1` checks.
- New game isn't a reload: every section with state must reset (section 13 now sends `simNote('newGame')`).
- name_check reads only lines that start with a declaration; a declarator carried on to the next line is handled since 4ad33f0.

## Memory
(Session 2 note: run each review in a background subagent with `flock /tmp/cadet-work/browser.lock` around browser runs; `/tmp/cadet-work/three/package` must exist (a link to the folder) for cadet_test. Tips move fast: tell running agents the new hash rather than starting over.)

At about 70% (2026-10-17 ~04:30 UTC): handing over now, per the rule. A fresh reviewer should start by reviewing: social A 0.36.52-0.36.57 (the tip), social B 0.39.6 when final, arrival's fixes for 4f6d0b2 (the briefing start), the sim's introPlan occupancy fix, and galley's next push (the galleyBirthdays aboard() fix).

The full-merge recipe I used: a worktree at origin/claude/arrival, then merge sim-engineer, deck-plans-1-2-6, social, social-stories, player-needs (never ship-systems, never `-X ours/theirs`), resolve only build-line conflicts and keep both sides elsewhere, then name_check, intro_check, social_check (social A's copy), day_check on the days that matter (0, 6, 15, 35).
