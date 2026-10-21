# Handover: build master (BM11)

- **Role:** build master. I alone pushed to `claude/integration` (the shared branch). For each reviewed piece of work the lead sends: merge it (never rebase or force-push the shared branch), set the build number on the two build lines (the header's `build` line and `GAME_BUILD`), add the merge row to `plans/build-table.md`, run `bash check_fast.sh` plus the area checks the lead names, push, read the GitHub quick check for that exact commit, and send the lead the hash and one line.
- **Session:** BM11, session_01W7NHRM4JjqaNEJQUWNxgcE. Started by lead 20; reported to lead 21, lead 22, then lead 23 (session_01XXiKm9iPgm565SZ4n1knmU). Handed over at ~500k memory, before the Fridays work (lead 23's call).
- **Clashes that needed a person: 0.** Every clash so far was `plans/build-table.md` only (two branches both adding rows at the end of the file): keep both sides, give the incoming rows their own `###` heading if they have none.

## Merges (all on `claude/integration`)

| Build | Commit | What | GitHub check |
| --- | --- | --- | --- |
| 0.64.3 | da5e2aa | Dev mode Stop 1a (claude/devmode fa394b3) | success |
| 0.64.4 | 5d6ee1c | Talk a while pack + work pools (claude/talk-wire 6484d3e) | success |
| 0.64.5 | 7958332 | Patch batch E (claude/patch-e a9345ed) + events_check skips first-light when FLC_ON is off (c58c7d2) | success |
| 0.64.6 | 675588c | Patch batches D and F, #31 parked (claude/patch-b 16df5bd) | success |
| 0.64.7 | 6ea5acf | Release round: patch-a efba55a, patch-b 319f541, First Light Cocoa's place names (EW1 fdf4339, baked), LADDER_ON / MUG_ON / FLC_ON switched on; three check-only fixes (below) | success |
| 0.64.8 | 0ca6a58 | The ship-wide events base (claude/events-base-2 a1f2344) + EC1's bigevents_check f9b2b0b, every event switch off; cadet_test vs 0.64.7 ALL IDENTICAL | see below |

## Check-only fixes made in the 0.64.7 round (lead 22's overnight orders)

- **`cadet_test.py` (3555675):** `Game.step` puts the draw-only-the-last-frame switch (`SKIP_SWITCH`) back when a page reload has lost it. TS1's find (plans/handover-test-speed.md). Before it, every simulated frame after a reload was drawn: intro_check took over 2 hours; now its whole run takes about 14 minutes. Proven identical, old harness against new, on join, devmode, career and mech_check on 0.64.6 and 0.64.7, except devmode on 0.64.7, where the old harness gave a false FAIL.
- **`intro_check.py` (aa67ad3):** parts 9 and 11 wait up to 120 s for their page reloads (`RELOAD_MS`). The reload right after part 8 takes 31-32 s in a cloud container, past Playwright's 30 s default.
- **`mech_check.py` tparts (d62aea5):** each run stocks the team parts (3 each) after its reset. With FLC_ON the crew's plans shift the machines' wear and the last pump and bearing went at the same tick as the Day-18 parts ask.

## Loose ends

- **career_check** fails only on backlog row 12 ("busy: Relied on before Day 5"): known and accepted (the user's later balance pass). PB's 9e34423 fixed it, then 319f541 reverted that.
- **day_check Day 12** fails ("the rec deck is on but nobody came to it in the evening"): backlog #18, identical on 0.64.6 and 0.64.7.
- **perf_check's scenes stand in the wrong rooms** (OP1, backlog 18b), so its "Sunday dinner, the mess" numbers may not be the mess.
- **perf_check** always flags "memory grows across deck round trips" (548 -> 548 -> 550 geometries): the same on 0.64.6, 0.64.7. A single frame-time spike can also show; re-measure the scene before calling it real (a trimmed copy of perf_check with `SCENES` filtered works).
- **lines_check** passes with 6 warnings (5 old "(Just listen)"/"(Say nothing)" repeats, and "Tracked" read as a name in patch-a's tip.device line).
- OR1's optional idea for events_check, not done: with FLC_ON off, also fail if first-light IS loaded.

## Gotchas

- **Run browser checks one at a time** (at most two). Five at once on 4 cores made page loads time out (30 s). Give each run its own `CADET_WORK` (`mkdir -p $W/test; ln -sfn /tmp/cadet-work/three $W/three; ln -sfn /tmp/cadet-work/acorn $W/acorn`).
- **Never wait on a process with `pgrep -f <pattern>` / `pkill -f` from a shell whose own command line contains the pattern:** it matches itself. One of my runners waited an hour for itself; two `pkill`s killed my own command. Use `ps -eo pid,args | grep "[p]attern"` and kill by PID, or just chain the steps in one script.
- **Background commands stop at 2 hours.** Split long rounds into scripts under that (check_fast + cadet_test + 6-8 checks; then the rest). player_check takes ~28 min, perf_check ~20 min, intro_check whole ~14 min now.
- **perf_check writes `perf_check.json` in the folder it runs from**: move it out before committing.
- **Splitting cadet_test differences:** build copies with one switch on at a time (`sed` the switch line in a copy under /tmp) and compare each against the switches-off build. cadet_test doesn't compare crew positions, only the player's walks and taps; "g_nocrew 0 px" with other shots differing means the crew are placed differently.
- **Prepare merges in a separate worktree** (`git worktree add --detach /tmp/wt-x origin/claude/integration`) so the main folder stays on the pushed branch and the stop hook doesn't nag about unpushed or uncommitted work.
- **A switch flip:** `let X = URL_FLAGS.has('x')` -> `let X = true;   // 0.64.7: switched on (...)`. Check nothing else reads the URL flag directly.
- Content: after copying a `.meet`/`.trad`/`.lines` file in, run `python3 content_gen.py starship-cadet.html` and then `--check`.

## How to test (setup in a fresh container)

`pip install playwright numpy pillow`; three r128 and acorn 8.12.1 in `/tmp/cadet-work/three` and `/tmp/cadet-work/acorn` (`npm pack three@0.128.0`, `npm pack acorn@8.12.1`, untar each); `CADET_CHROME=/opt/pw-browsers/chromium`. `bash check_fast.sh` (6-7 min alone; must print QUICK CHECK OK). The release round: check_fast, cadet_test against the last build, day, events, food, player, career, interactions, bubble, join, lines, devmode, mech, perf (against the last build), intro_check whole (or `--evening`, `--firsts`, `--week` pieces), and bigevents_check once the events base is in. Read the GitHub quick check with the GitHub tools (`actions_list` list_workflow_runs on branch claude/integration).

## Next (lead 23's queue)

Fridays (FR2's turns) when they pass review, then the storm update. Event switches stay off until the lead orders them on; off must be ALL IDENTICAL against the build before.

# BM12's update (session_01Pdzb8wT4UA5tPgwQStRoqd; reports to lead 24, session_01SDe7z5Nr7u69uH1k4sjZ8r)

## State right now

- **`claude/integration` = 0.64.9, f782c5d** (pushed; GitHub quick check success): Dev mode Stop 2 (claude/devmode-2 d686b86; PR7 PASS, PR6 PASS on the s18 hook). Clean merge. check_fast OK, cadet_test vs 0.64.8 ALL IDENTICAL, devmode_check, events_check OK. Lead 24 put Dev mode ahead of Fridays.
- **The 0.64.10 candidate is on `claude/integration-next`** (NOT on claude/integration: waits for lead 24's go after PR5's pass on Fridays turns 5-9). It is claude/integration 0.64.9 plus: Short Fridays **11b2220** (switch off; NOT the branch tip 0dc4562, which is turn 10 = `SHORT_FRIDAY` on and ships only together with the storm's switch-on), FD1's food_check fix (claude/food-waits 2ad7db8, check only, PB OK), build lines 0.64.10 and the row. On the go: `git push origin <integration-next tip>:claude/integration` (a fast-forward: it sits on f782c5d), then read the GitHub quick check and tell the lead.
- Checks on the candidate: check_fast OK; cadet_test vs 0.64.9 ALL IDENTICAL; fridays, events, bigevents OK; food_check 11 4 OK; devmode_check OK but its clock part failed once (backlog 21, real-time flake: alone twice OK here, and it failed once on 0.64.9 too). The whole release round was also run on the Fridays merge onto 0.64.8 (same Fridays game code): only the known fails (day 12 #18, career row 12, perf memory row 14).

## Backlog numbering (clashes I settled)

Fridays and Dev mode both added a row 18: Fridays' kept 18 (quoted elsewhere), Dev mode's clock flake is **21**. FD1's cookers row 20 is **22**, because Fridays turn 10 brings its own **#20** (Halloran / d5-mug) and quotes it. When turn 10 merges, its backlog row 20 slots in between 19 and 21.

## Queue (lead 24)

1. 0.64.10 push on the go (above).
2. One release with **both** switches on: the storm (claude/storm-update, EV6's S10) + Fridays turn 10 (claude/fridays 0dc4562 or later). Never either alone (Day 12's Friday speech mentions the storm).
3. PT1's claude/patch-crew (rotation Day 21 + camera); the Line (claude/line-update: EV7 merges the latest storm into it first; don't resolve its 5 game-code clashes yourself); TS2 / opt branches. For `perf_check.py` clashes take claude/opt-render 3af9f15's version (RN1's note).

## Setup notes for a fresh container

The test kit wants `/tmp/cadet-work/three/package/build/three.min.js` and `/tmp/cadet-work/acorn/package/dist/acorn.js` (the `package/` level matters: untar each npm pack into its own folder without --strip-components). Worktrees used: /tmp/wt-fri2 (the candidate), /tmp/wt-dev (0.64.9).
