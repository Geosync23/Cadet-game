# Handover: adversarial reviewer 1 (Pillar 4)

**Role:** adversarial reviewer 1. Before a helper's branch is combined, try hard to break it; report real problems, ranked, with evidence. No game code, ever. Push only review notes and reviewer tools to `claude/reviews`.
**Lead:** session_01PJtmxWgAPLebXSZKP6ZRpG (from 2026-10-17 ~02:40; before that session_01PxXKwc5mkC7tV5MPi3p7PP). **Build master:** session_012K7RZ3oSX2vpBb1rR66MBh. Reviewer 2 covers dialogue, traditions, device, decks, tiles, content.
**Chain of command (the user's rule):** the user → the lead → everyone. Never contact the user; report to the lead (and the helper).

## Handover to reviewer 1c — FINAL, 2026-10-17 ~11:50 (reviewer 1, session 2, standing down)
Reviewer 1c (**session_01YcSJkhhJ2MnCjsJs7QV8ud**) takes my sim / galley / social queue (the lead's decision). Lead: **session_01KPJMYjXAPkNUcrQ8VRkhLE**. Build master 2: **session_01F8ph7FKqViF3heRn94YgBr**. All my notes are in `plans/reviews/` on `claude/reviews`.

### Where each seat stands
| Seat | Branch | Session | Last reviewed (verdict) | Next for 1c |
| --- | --- | --- | --- | --- |
| Sim (10/13/14/17) | `claude/sim-engineer` | sim engineer 4 session_01EJUGywZv9BpcUezjXES9AC is **inactive** (ask the lead for the next sim seat) | e4d6ace 0.26.37 **PASS** (6a1906c): Calder's seat fixed; take 0.26.36+0.26.37 together | anything after e4d6ace (e1bb1e6 is docs) |
| Galley (16) | `claude/galley-food` | session_018cicfPQZQXbxmtn6ygmL84 | 40166d6 0.29.32 PASS WITH FIXES (bb66700); 0.29.33/0.29.34 were reviewer 2b's | low: day caches miss one-offs/tradition flags |
| Social A (20) | `claude/social` | session_012pK2XVi5UhqEd28fakYk68 | a033f17 PASS (mine); 1c already passed to 752d964 (0.36.81) | 0.36.82+ |
| Social B2 (20c) | `claude/social-stories` | session_014A3w2gK8FBNWs66YC3LfME | 7d8be10 0.39.22 PASS (5a83ca9) | anything after 7d8be10 |
| Player 4 (15) | `claude/player-needs` | session_01XPwaJeT8eATK5At45zEJ5w | 1c's | whole-save size check (250 KB to day 280) is owed |
| Onboarding 2 (21) | `claude/arrival`, `claude/arrival-0603` | session_0163dcLt17oTCdR8po9HRo2p | 1c's; my partial 54d7911 (b7ad3e9) | 046a019 (0.42.21b) has my 3 should-fixes + your tour pacing |
| Device 3 (19) | `claude/device` | session_01SskqNx45iEGyQq2W9Fjg5Y | my partial ee3fcdd; c4b2479 not reviewed | lead's call (missed-then-kept settled on partners' side) |

## Open items for 1c
1. **Arrival dinner, the player's seat:** on my e4d6ace full merge, your own seat 3-mess-10 was booked by Volkov during the arrival dinner (onboarding's intro_check saw it free on the b9089d9 merge). Check on the 0.60.3 combine.
2. **Jump vs hour by hour:** from the arrival, a 2-day jump makes section 17 send 4 notes hour-by-hour never sends (jobUnclaimed 3-growlight-2/3-oven-1/4-washer-2, repair 3-range-1, all t=2460). social_check 8c9b52f+ --long prints them and reports FAILED for it. The sim seat owns it.
3. **Social save rule (the lead):** every saved social part has a hard bound by design with its worst case in DEV_NOTES; <= 30 KB on every day to 140, < 40 KB to 280, measured daily from the real arrival (social_check --long does this). Last numbers: 26.6 KB / 29.7 KB (social A 0.36.81). Whole save: 250 KB to day 280 (player seat).
4. **Sim lows:** crewMakeWay builds lists per crew member every frame; the step-aside spot can be another station's tile; breakfast tray return makes ~36 crew up to 6 min late to the lift (deferred by the sim engineer); a crewHold on someone in the line blocks the counter; 0.26.35's start tile needs claude/decks-p3's walkable Tern (0.60.4).
5. **Social B lows:** no test asserts v:2 from an arrival start or STORY_CAP 0; a pre-0.39.22 untagged snapshot with a reordered roster is read by position for up to 2 weeks.
6. For the dialogue engineer: section 22's linesFill can add {home} {family} {hobby} {since} to SOCIAL_FILL. For ship-events: events_check fails on 4e72597 alone at day 231 (3-store-1 double); section 18 doesn't reset SHIP.occasions/commendations on New game.

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
