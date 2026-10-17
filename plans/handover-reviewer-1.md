# Handover: adversarial reviewer 1 (Pillar 4)

**Role:** adversarial reviewer 1. Before a helper's branch is combined, try hard to break it; report real problems, ranked, with evidence. No game code, ever. Push only review notes and reviewer tools to `claude/reviews`.
**Lead:** session_01PJtmxWgAPLebXSZKP6ZRpG (from 2026-10-17 ~02:40; before that session_01PxXKwc5mkC7tV5MPi3p7PP). **Build master:** session_012K7RZ3oSX2vpBb1rR66MBh. Reviewer 2 covers dialogue, traditions, device, decks, tiles, content.
**Chain of command (the user's rule):** the user → the lead → everyone. Never contact the user; report to the lead (and the helper).

## My seats (session ids) — refreshed 2026-10-17 ~09:00 by reviewer 1 (session 2)
Lead from ~04:35: **session_01KPJMYjXAPkNUcrQ8VRkhLE**. Build master 2: **session_01F8ph7FKqViF3heRn94YgBr**. Reviewer 1c (added ~08:15, notes on claude/reviews-3): **session_01YcSJkhhJ2MnCjsJs7QV8ud**; took player from 5e61e12 and roster d53cf40.
| Seat | Branch | Session | Last reviewed | Verdict |
| --- | --- | --- | --- | --- |
| Sim engineer 4 (sections 10/13/14/17) | `claude/sim-engineer` | session_01EJUGywZv9BpcUezjXES9AC | bfcd864 (0.26.31) | PASS WITH FIXES. MUST: crew already in the food line never leave it while galleyCanServe() is false (38 late for shift). f9a145c (0.26.32) fixes a7673e0's two must-fixes (Calder's seat, repair note t); being verified |
| Onboarding (21) | `claude/arrival` | session_01KaHzfqSqF8B4bkNFrH1tsx | in progress: 4f6d0b2..54d7911 (0.42.18-0.42.21, Zeke's tour) | headline of 0.60.3 |
| Social A (20) | `claude/social` | session_012pK2XVi5UhqEd28fakYk68 | 3a68d74 (0.36.63) PASS WITH FIXES; 69876a7 (0.36.72) in progress | |
| Social B2 (20c) | `claude/social-stories` | session_014A3w2gK8FBNWs66YC3LfME | 47b02d6 (0.39.17) PASS WITH FIXES (medium: storyM creates records on read); ba09f2b (0.39.18, top-300 snapshot pairs; asked the lead if approved) in progress | |
| Galley (16) | `claude/galley-food` | session_018cicfPQZQXbxmtn6ygmL84 | 6abd36b PASS WITH FIXES; final 40166d6 (0.29.32) in progress (blocks 0.60.3); 2bfd042 (0.29.33) next | galley owns the player's line membership (lead) |
| Player engineer 4 (15) | `claude/player-needs` | session_01XPwaJeT8eATK5At45zEJ5w | 5e61e12 (0.28.28-29) PASS WITH FIXES; later builds are reviewer 1c's | draft player-needs-fabc552-DRAFT.md |
| Device engineer 3 (19) | `claude/device` | session_01SskqNx45iEGyQq2W9Fjg5Y | ee3fcdd (0.35.32, occasions as appointments) in progress, asked by the lead | |
| Crew designer 3 | `claude/deck-plans-1-2-6` | - | d53cf40 is reviewer 1c's | |

Every review note is in `plans/reviews/<branch>-<commit>.md` on `claude/reviews`; read the latest per branch before re-reviewing.

## Open items to follow up
1. The full-merge jump test: fixed by social A 0.36.61 (SOC_IN, notes applied at the end of the hour) plus sim f9a145c's max(t, SIM_AT). Re-check on each full merge.
2. Social save: social B 0.39.18 replaces the |aff| >= 30 snapshot rule with "strongest 300 pairs a week"; asked the lead whether approved.
3. For the dialogue engineer: section 22's linesFill can add {home} {family} {hobby} {since} to SOCIAL_FILL now.
4. For ship-events: events_check fails on ship-events 4e72597 alone at day 231 (dayReport double: 3-store-1).
5. Social B's farewellCrew isn't wired yet; check against social A's 14:00 Sunday farewells when it is.
6. A hook owner: section 16 (galley) owns the player's food-line membership (lineJoin/lineLeave), the lead's ruling.

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
(Session 2 note: run each review in a background subagent with `flock /tmp/cadet-work/browser.lock` around browser runs; `/tmp/cadet-work/three/package` must exist (a link to the folder) for cadet_test. Tips move fast: tell running agents the new hash rather than starting over.)

At about 70% (2026-10-17 ~04:30 UTC): handing over now, per the rule. A fresh reviewer should start by reviewing: social A 0.36.52-0.36.57 (the tip), social B 0.39.6 when final, arrival's fixes for 4f6d0b2 (the briefing start), the sim's introPlan occupancy fix, and galley's next push (the galleyBirthdays aboard() fix).

The full-merge recipe I used: a worktree at origin/claude/arrival, then merge sim-engineer, deck-plans-1-2-6, social, social-stories, player-needs (never ship-systems, never `-X ours/theirs`), resolve only build-line conflicts and keep both sides elsewhere, then name_check, intro_check, social_check (social A's copy), day_check on the days that matter (0, 6, 15, 35).
