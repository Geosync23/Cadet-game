# Handover: build master (BM11, BM12, BM13, BM14; newest first)

# BM14's update (newest: read this first)

- **Session:** BM14, session_016mhGtsCxEgPCFn9C767yjq (0.91.0 and 0.92.0). Took over from BM13 at ~16:00 UTC 2026-10-22. Reported to lead 28, lead 29 (session_01A9rNreAGVbsY1HgPucDMA7), then **lead 30 (session_016evGvfNY88TNKgaHErG9Q8, branch claude/lead-30)**.

## State right now (updated ~12:15 UTC 2026-10-23, after 0.92.0)

- Reports to **lead 31** (session_0118SXBCdg87nDiXdtrGNVSR) since ~02:55 UTC.
- `claude/integration` = `claude/integration-next` = `claude/integration-next-fe1` = **685af944 = 0.92.0**, game sha256 **f2329b620c113b0a585d6129ef70a3cbb8f8112c6ef9d19a13587fb996271ebd**. Full round PASSED; PUB1 published it (Playtest and Dev links, Version 9). The build-table's 0.92.0 row has every piece, every round fix and the known items (KC1/KC2 controller day, KS1 save size, KP1 Line 335 draw calls, reach partial with the controller off, backlog 14/23/32).
- 0.92.0 = staging 01b237f4 (0.91.0 + controller follow-up, off) + breakfast-back, zeke-tour, dinner-spread, tip-clear, hygiene-cool, tiles-sit, floor-tap-fix, CTT3's controller_check, then arrows-c 7d97d538 last (teaching arrows ON: POINT_ON and GUIDE_ON true), then test-only check fixes and FX5's Day 0 table game fix (153084a1). Switches: PAD_ON and EV_LINE_ON false.
- **Next job: 0.92.1** on 685af944, pieces as they pass (lead 31): DS1 bag-no-net (RV9), AC3 join notices never dropped + the check test hook (RV10), FX4 save trim (RV10), FX7 gym bike tap (RV10). Later: FX6's Crossing the Line check, the controller follow-up.

## 0.92.0's lessons (read before the next arrows-on build)

- With the teaching arrows on, toast() goes through guideToast(): a pop-up is queued while another is fresh and later replayed by guideTick() with GUIDE.pass true. Checks that read a toast or IX_GOAL saw the wrong one or counted twice. The shared test-only fix is one line after load: `if (typeof GUIDE_ON !== 'undefined' && GUIDE_ON) { GUIDE.tq.length = 0; guideToast = () => false; }`; for the arrow, read goalNow() (the arrow you see), not IX_GOAL. A game-side test hook is backlog LEAD31-2 (AC3, in 0.92.1).
- Isolate any new FAIL by running the check on a copy with POINT_ON and GUIDE_ON set false (sed on the two lines). It sorted every FAIL into arrows-on vs other pieces in minutes. Then bisect the other pieces over the merge's first-parent commits (stop each run once it passes the failing part).
- Run a copied check under its own file name next to cadet_test.py (player_check execs cadet_test.py by path).
- Build-table cherry-picks that EDIT a row (not add one) leave both rows with my keep-both helper: check for doubled rows after each one. Never amend a commit already pushed to the candidate: fix it with a new commit (the candidate only fast-forwards).
- Runners' background jobs stop at 2 hours; controller_check reach takes ~2.5 h, so it needs a detached run (nohup/setsid) or a split.

## What happened today (in order)

1. **0.64.17 (breakfast)**: first round on 8193458e found three new FAILs and a rise: mech m12 (test fixture; SC1 5640cf5a), bigevents Line supper (silva-bea ate standing; SC1's tradMeal 599de448), bubble_check 49.8 px (CP4's bubble-jump 36f8abf7), perf Line ceremony 301->335 (camera tile moves with the crowd; accepted, backlog LEAD29-1). Re-round on 1498dbf4 passed; published; then **the user rolled breakfast back** (problems found in play). Rollback = 2cabe96b: game, content/, design-doc, food_check, mech_check exactly as 0.64.16 b9f053ba, history kept. Breakfast work kept on claude/patch-play1-f 7f07d035 and claude/bubble-jump 36f8abf7, and in history (1498dbf4), for later.
2. **0.91.0** built twice: first on the 0.64.17 controller base (e27b8bfe, dropped with the rollback), then on 9a8eac0b (989fd566). Staging branch `claude/integration-next-fe1` is mine and spent (I overwrote it once).

## Round notes

- controller_check: run every part but reach (`python3 controller_check.py starship-cadet.html idle save calls touch walk pick day games unplug odd off quiet base deck pick1 panels api lists tiles disc screens marks touch3 drop settings a11y firstuse`); touch and day are known items (check-only / controller-only; CTT2/CTT3 fixing the check), tiles flaked once on IM1's trial (backlog CP4-1).
- Known-old: backlog 14 (perf +2 geometries, same on OLD), 23, 32; machine_check repair share edge 40% (on 0.64.16-based builds it's ~50%).
- fridays_check is CR6's (I once started a second copy by mistake; stopped it). Before running any check yourself during a round, confirm it isn't in a runner's share.
- When a cadet_test difference shows, isolate it: apply only one part's game hunk to the base and compare again (did this for the lift arrow).
- Build-table "both" resolutions: the eating cherry-pick drags FX2's Pillar 5 rows as context; keep only its `| fix-eat` row under its own heading.

## Gotchas

- My merge-conflict helper is in BM13's section below (resolve.py ours|theirs|both); a version that also skips diff3 base sections is fine.
- Type full commit numbers when pushing (`git push origin <full sha>:claude/integration`); a typo makes the push fail quietly in a chain.
- Run browser checks from a worktree that isn't being changed underneath them; I once switched branches in the folder a check was reading (harmless only because the files it read didn't change).
- three/acorn under /tmp/cadet-work must be untarred WITH their `package/` folder (`tar xzf three-0.128.0.tgz -C three`), not stripped.

---

# BM13's update (newest: read this first)

- **Session:** BM13, session_01ExFoVfhiFG3wYTFv2QrojC. Reported to lead 25, lead 26, lead 27, then lead 28 (session_01S7AdxK1ZyXiEFowP3k5gng). Handed over at about 60% memory (the user's rule: judge from 60%), during 0.64.17's round, before its fix and the arrows queue (lead 28 offered it).
- **How the shared branch works now (the user's rule, 2026-10-22):** every game change gets the six-runner full round BEFORE it reaches `claude/integration`. So game changes go onto the candidate branch **`claude/integration-next`**: merge each reviewed branch there (check_fast plus cadet_test against the step before, plus the area checks), set the build number there, send the lead the tip and the game file's sha256, and the lead (or you, on the lead's go) starts CR1-CR6. Only when every runner says OK do you fast-forward `claude/integration` to the candidate (`git push origin <tip>:claude/integration`, a fast-forward, never a force), then read GitHub's quick check on it. `claude/integration` only ever holds full-round builds. Check-only changes need check_fast plus the checks they touch, and may go straight to integration.
- **While a round runs on integration-next, don't move it.** Stage the next build on its own branch (I used `claude/integration-next-0.64.17`) so its reviewer can check it, and move it onto integration-next only after the round in flight passes and integration is fast-forwarded.

## State at handover

- `claude/integration` = **0.64.16** b9f053ba until 0.64.17's round passes (then 0.64.17, see below). 0.64.15 was 2b4a05db.
- `claude/integration-next` = **0.64.16** b9f053ba (the Zeke patch, ON1's claude/patch-zeke ce2f77bc, OR2 PASS; plus the testing-guide notes). Game sha256 70f9427354a398ef25e355e7428f10ba6f0800b4c83a83945c8c950a42e6a5c7. Full round PASSED; published from b9f053ba; claude/integration fast-forwarded to it.
- `claude/integration-next` = **0.64.17** 8193458e (1d2f3269 = breakfast at 07:00, SC1's claude/patch-play1-f dd83d896, RV3 PASS on the merged build; plus a docs commit: 0.64.16's round record, backlog 32, the testing guide's known-old list). Game sha256 225836918e5a70cad2a9809b2aea8febc21837617f3dee907b49a07655a4c4b5. Its full round started ~15:45 UTC on 2026-10-22 and **FAILED: CR6's mech_check m12 (the logbook)** is a NEW FAIL: on 0.64.17 the flagged Washer 3 is still open at 22:00 (nobody on the night crew claims it) and the written-up job isn't 10% quicker; 0.64.16 b9f053ba passes m12 (night: done by navarro-mateo, logged [12, 0.9]); same on a re-run of m12 alone. Likely breakfast's night-shift changes (SC1's b006ad0 / 8d65f86). Lead 28: 0.64.17 is NOT fast-forwarded or published; SC1 is fixing it, RV3 reviews; the other runners finish their shares so anything else shows. machine_check's repair share was 17/42 = 40.5% (passes, at the edge: the watch point below). **Your first job:** when RV3 passes SC1's fix, merge it onto `claude/integration-next` (this note rides on its tip, docs only; the game sha256 is still 22583691...c4b5 until the fix), keep the build at 0.64.17, run check_fast + mech_check (m12) + cadet_test vs b9f053ba alone + lines_check if content/ changed, give the lead the new tip and sha, and the lead decides a full round or the affected checks. Then fast-forward integration on the lead's go, tell PUB1 (session_01GnpjFR6oumvuvTrmcXSqeg) the commit + sha, read GitHub's quick check, and record both rounds in 0.64.17's build-table row (its `Checks: FULLROUND` placeholder). The staging branch `claude/integration-next-0.64.17` (1d2f3269) is spent; leave it.

## Builds I made

| Build | Commit | What |
| --- | --- | --- |
| (check only) | 7bc9ebc | DB2's devmode_check seed fix (BM12's parked integration-next) |
| 0.64.12 | 9654f37 | The opening camera 1.62 / 1.22 (the user's "go back 10-15%") |
| (docs) | a4a5735 | DB2's Dev mode phone shots |
| 0.64.13 | a7477a9 | The storm update + Short Fridays switched on together |
| 0.64.14 | 8e239328 | opt-render, checks-cr3, bigevents-check, PB2's four game commits (cherry-picked: claude/patch-b2 sits on claude/line-update), fridays-20 |
| (check only) | ed57dd78 | opt-tests (TS3) + the fridays-20 intro guard |
| 0.64.15 | 31c44cb9 (+2b4a05db docs) | Playtest patch 1: parts A, B, C, D, E, G, H, I, J, K, and the Line merged switched OFF (EV_LINE_ON false). First round found two new FAILs, both fixed (J's reminder covering a toast; intro part 14 after A's earlier arrival), then a full re-run passed |
| 0.64.16 | b9f053ba | The Zeke patch |
| 0.64.17 | 1d2f3269 (+8193458e docs) | Breakfast at 07:00 |

## Queue after 0.64.17 (lead 27)

1. FX1 `claude/p5-fix1`, FX2 `claude/p5-fix2`, FX3 `claude/p5-fix3` (Pillar 5 Steps 1-2 fixes), each after its review.
2. Arrows piece B (the arrow queue, `GUIDE_ON` off): AR1's game commits on `claude/arrows-plan` (its earlier commits there are plans/ and design-doc only).
3. Arrows piece C (the pointer, `POINT_ON` off): AC1's `claude/arrows-c`.
Each gets its own candidate and full round, or the lead may batch them; ask.

## Known clashes and asks for that queue

- **Arrows C vs controller P4** (RV2): both rewrite the same last line of section 19's Settings view. C adds the "Teaching arrows" row, P4 (in `claude/controller`) adds `.concat(padSetBlocks())`. Whichever merges second needs a hand merge that keeps both.
- **New checks into the guide and the split:** when C merges, add this row to `plans/testing-guide.md`'s table in 2.1, after device_check, and put the check in the full round's split (AC1, via lead 27):
  `| **arrows_pointer_check.py** | Section 19's panel pointer (arrows plan, piece C): off, nothing drawn or saved; on (a copy with POINT_ON true) at 360x640, 390x844, 844x390 and 1280x800, the ring on the Device button, a tile, a tab, Back, a choice card, a board row's Take it and the clock's Clock in, on screen, gone when used, once, the Teaching arrows switch, no draw calls. | 4 | `python3 arrows_pointer_check.py BUILD.html` | `arrows_pointer_check: OK` |`
  The same for piece B's `arrows_check.py` (AR1).
- **Words:** any branch touching `content/` makes the baked blocks clash. Never resolve those by hand: take one side, run `python3 content_gen.py starship-cadet.html`, then `--check`, then `lines_check` **inside the merged tree** (lead 26's rule: lines_check on every merge that touches content/).
- **Backlog numbering:** branches pick the next free number on their own base, so two branches often add the same row number. The one that merges second gets renumbered, with a note in the row. Open rows sometimes land under "Fixed" because their author appended at the end of the file; move them to the open table.
- **A row rewritten on both sides:** when a branch updates its own build-table row, the clash shows the old row in ours and the new one in theirs. Replace, don't keep both.

## More notes from the leads

- When piece C (claude/arrows-c, AC1, d7a55699 at the time) merges: add this row to plans/testing-guide.md's table in 2.1, after device_check, and put arrows_pointer_check.py into the full round's split (lead 27 / AC1):
  | **arrows_pointer_check.py** | Section 19's panel pointer (arrows plan, piece C): off, nothing drawn or saved; on (a copy with POINT_ON true) at 360x640, 390x844, 844x390 and 1280x800, the ring on the Device button, a tile, a tab, Back, a choice card, a board row's Take it and the clock's Clock in, on screen, gone when used, once, the Teaching arrows switch, no draw calls. | 4 | `python3 arrows_pointer_check.py BUILD.html` | `arrows_pointer_check: OK` |
- Likewise for piece B (claude/arrows-plan, AR1): a row for arrows_check.py in 2.1 and a place in the split.
- Known clash (RV2 via lead 27): arrows piece C (claude/arrows-c) and controller P4 (claude/controller) both rewrite the same last line of section 19's Settings view: C adds the "Teaching arrows" row, P4 adds `.concat(padSetBlocks())`. Whichever merges second needs a hand merge that keeps both.
- 0.64.17 round watch point (lead 28): machine_check's repair share was 40% (range 40-60) and swings 36-56% with small morning changes. If it lands just under 40, tell lead 28 before calling it a FAIL (RV3 judged it noise; backlog LEAD27-1). Put it in the brief to the runner with machine_check (CR6).

## Round notes for the runners

- Known-old FAILs: **backlog 14** (perf_check's +2 geometries a lap) and **backlog 23** (food_check 7 1 "garden, good"). Backlog 12 (career "Relied on" before Day 5) no longer shows since part G; its return would be the old failure, not a new one.
- **Run tiles_check alone** (it times out clicking "Quick game" when other checks share the CPU) and **cadet_test strictly alone** (with a second browser running, the HUD's blurred glass can come out 1 level off in 6-46 pixels; now in the testing guide, 8.1).
- fridays_check takes about 20 minutes on a runner, old and new alike.
- Runner sessions: CR1 session_01CsWNjCsy8u5mrHJgTVgCst, CR2 session_01BgMQaB1LQmhfU1rSJ2ATvv, CR3 session_016oCbvvzgcqzzCTsBFCkYRB, CR4 session_01636CfY2MhB3DzrzZ59dhXz, CR5 session_01CHoEsvv7zMPZDr1ir7uAiz, CR6 session_01B1FwE5sMmHnMPWsGn23nrk. The split (0.64.15's re-run): CR1 player, devmode, bubble, puzzle, social, talk, fridays; CR2 intro (whole), perf vs OLD, cadet_test vs OLD, path, arc, lines, lines --day; CR3 day_check 0, 1, 5, 7; CR4 day_check 12, 13, 16, 19; CR5 day_check 21, 27, interactions, events, career; CR6 check_fast, mech, bigevents, disc, tiles (alone), join, food 1 7, food 11 4, clothes.

## Gotchas I hit

- **Look up commit numbers before you report them.** I once sent a lead a commit number I hadn't checked; always copy it from `git log`.
- **A check-only merge still runs every check it touches.** I missed player_check on the opt-tests merge once and ran it after the push. `git diff --stat OLD NEW -- '*.py' '*.js' '*.sh'` lists them.
- **A branch may sit on another unreviewed branch.** claude/patch-b2 was built on claude/line-update; merging its tip would have brought the whole Line. Check `git log OLD..TIP` before merging, and cherry-pick the reviewed commits if needed (ask the lead).
- **Bisect by candidate steps.** When a new FAIL shows on a candidate, run the failing check on the merge steps (`git log --first-parent` of integration-next) to find which merge brought it; share the list with whoever else is looking so nobody repeats a run.
- The merge-conflict helper I used for build-table / backlog hunks (save as a scratch file; `python3 resolve.py FILE ours|theirs|both`). Before "both", check the incoming side for rows already present (a branch rewriting its own row shows up as a clash: replace, don't keep both):

```python
import sys,re
# resolve.py FILE ours|theirs|both
p,mode=sys.argv[1],sys.argv[2]; s=open(p).read()
pat=re.compile(r'<<<<<<< [^\n]*\n(.*?)=======\n(.*?)>>>>>>> [^\n]*\n',re.S)
def f(m):
    o,t=m.group(1),m.group(2)
    return {'ours':o,'theirs':t,'both':o+t}[mode]
s,n=pat.subn(f,s); open(p,'w').write(s); print(p,mode,n,'hunks')
```

---

# Earlier notes (BM11, BM12)


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

## State right now (updated 17:55, the account handoff stop)

- **`claude/integration` = 0.64.11, 70aa91f** (GitHub quick check success): 0.64.10 c6f665b + FD1's food_check part 2 (claude/food-waits 2a0ffe3, check only; backlog row 23) + PT1's crew patch (claude/patch-crew eb86a00: Day 21 rotation, camera 1.85/1.40, the Tern). cadet_test vs 0.64.10 differs only by the camera (ALL IDENTICAL with the camera line put back); check_fast, events, day 21/25, join OK.
- **Parked on `claude/integration-next`, NOT on integration:** DB2's claude/devmode-2 841a9d0 (devmode_check's new games take the Dev seed; check only; lead 24's ask and yes) merged as 9ecd66d on 70aa91f (build-table clash: DB2's row moved under the Dev mode heading), plus this note. devmode_check OK twice; check_fast was stopped unfinished at the handoff. To finish: run check_fast on integration-next's tip, then fast-forward claude/integration to it (no new build number: check only) and read the GitHub check.
- **Later, DB2 moved claude/devmode-2 to 21bdec7** (integration 70aa91f merged in + the same 841a9d0 check fix + the 36 Stop 1b/Stop 2 phone shots force-added under plans/devmode-2-shots/, since *.png is git-ignored; its row already under the Dev mode heading). Better to merge 21bdec7 onto claude/integration instead of my 9ecd66d (game file identical; PR6 OK), then check_fast and push.
- Merge note (FD1): when claude/line-update's food_check.py meets food-waits', keep both: the fresh() calls and EV5's eventMeetTag line (~526).

## Earlier state (the 0.64.10 round)

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
