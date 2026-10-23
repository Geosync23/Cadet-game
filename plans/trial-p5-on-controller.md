# Trial merge: Pillar 5 fixes + guiding arrows (claude/arrows-c) on top of the controller line

Merge helper IM1 (session_01PL57XDQC6t5hx7NtJ1pDMo), for lead 29. Branch `claude/trial-p5-on-controller`.

Why: the user wants all new work built on the controller version, so the Pillar 5 + arrows build will be
claude/arrows-c merged onto 0.91.0 (= claude/controller 0.90.9 [controller + 0.64.17] + five fresh-eyes fixes, BM14).
This trial finds and settles every clash ahead of time so the real merge is quick. Both switches stay as on their
branches: the controller off (`PAD_ON = false`), the arrows off (as arrows-c ships them).

## Rounds

| Round | Controller line base | claude/arrows-c | Result |
|---|---|---|---|
| dry run | fda82c1 (0.90.8, before 0.64.17) | c26f194 | 4 game conflicts + 3 docs conflicts, all resolved (below) |
| dry run 2 | fda82c1 | 00f4436 (FX3 fixes 10-14 merged) | no new conflicts (FX3's changes merge cleanly; all 4 controller hooks and the Settings hand-merge still in place) |
| round 1 | f929c0b0 (0.90.9 = controller + 0.64.17, CP1, on claude/controller-p1) | 7ff2c27 | 2 game conflicts (#3 Settings, #4 jobEnd; the build lines now merge by themselves to 0.90.9) + 2 docs conflicts; same resolutions. Commit 4415749b; superseded by the breakfast rollback (0.64.17 taken out by the user) |
| round 2 | e27b8bfe (BM14's 0.91.0 candidate on claude/integration-next-fe1 = 0.90.9 + fresh-eyes batch 1) | 7ff2c27 | 2 game conflicts (#3, #4, same resolutions) + the FX3 fix 10 duplicate in design-doc.md, interactions_check.py and build-table (#5) + backlog rows. Commit 62347604, not pushed: overtaken by the breakfast rollback |
| round 3 | 9a8eac0b (CP1's controller 0.90.9 redone on 0.64.16 b9f053ba, after the user rolled back breakfast) | 69d1ed9b | 2 game conflicts (#3, #4) + backlog and build-table rows; same resolutions. This is claude/trial-p5-on-controller (c91e04a8 to 77256a82; replaced by round 4) |
| round 4 | 989fd566 (BM14's new 0.91.0 candidate on claude/integration-next-fe1 = CP1's 9a8eac0b + fresh-eyes batch 1) | 69d1ed9b | as round 2: #3, #4, the FX3 fix 10 duplicate (#5) in design-doc, interactions_check and build-table; same resolutions. Commit 8bd5d1c4 (notes fce67dac, 9b7be696); replaced on the branch by round 5 |
| round 5 | 01b237f4 (BM14's staging on claude/integration-next-fe1 = 0.91.0 + CP1's controller follow-up dcdfe944 + CTT3's controller_check) | 12b67c70 (includes 3c42632, FX3 16-18) | as round 4 (#3, #4, #5, docs) + one new: player_check.py (#6). Commit a4f7d4f0 |
| round 5b | 01b237f4 | 9197ba11 (+ FB1's galley drop, 191bee5) | merged by itself into round 5, no conflict. Commit 45362bd6: replaced |
| round 5c | 01b237f4 | 46e594cd (F2) | merged by itself; all checks green (arrows off). Commit 9b3e7c3f |
| rounds 6-10: the 0.92.0 combined build (lead 30, then 31) | 01b237f4 | arrows-c up to 8eb57151 (arrows ON) | + breakfast-back 0cd37b1b, dinner-spread ed6bcbf3, tip-clear feb2e54a, zeke-tour 99687fc8. Clashes: build-table rows every time (kept, in merge order; one doubled row removed) and section 19's Device engineer slot (#7). Round 10 = e819950a: this is claude/trial-p5-on-controller now; see plans/handover-im1.md for its check status |

## Conflicts in the game (starship-cadet.html)

| # | Where (section) | Controller side | Arrows-c side | Resolution | Why |
|---|---|---|---|---|---|
| 1 | Header's `build` line | build 0.90.8 | build 0.64.15 | controller's | The controller line is the base; the build master sets the number at the real merge. |
| 2 | `GAME_BUILD` (section 3) | '0.90.8' | '0.64.15' | controller's | Same. |
| 3 | Settings view (section 12, `deviceApp({ id: 'settings' })`) | the list ends `].concat(typeof padSetBlocks === 'function' ? padSetBlocks() : [])` (the Controller page's button, once a pad is seen) | adds the "Teaching arrows" row (`...(teachShown() ? [...] : [])`) after "Meals and your shift too" | keep both: the arrows row inside the list, then the `.concat(padSetBlocks())` after it | The expected hand-merge. Order on screen: ... Meals and your shift too, Teaching arrows (when shown), then the Controller button (when a pad has been seen). With no pad, padSetBlocks adds nothing, so the list is exactly arrows-c's. On 0.91.0, New game (batch 1) sits higher in the same list (after "Quiet off shift", `devNewSure ? ... : New game`), so it does not touch this line: all three are kept. |
| 4 | Finishing a repair job (section 17b, `jobEnd`) | `finishJob` branch gains `if (typeof padBuzz === 'function') padBuzz('done');` | a new first branch: no call yet or the wrong part (`caseFitted`) keeps the machine faulty (p5-fix2, 24k / 24g); `finishJob` becomes `else if` | arrows-c's two branches, with the controller's buzz added to the `else if (finishJob(...))` branch only | The buzz says "job done", so it belongs only where the job really finishes; the new not-yet-fixed branch gets no buzz. Behaviour of each side is unchanged. |

| 5 | The lift-panel arrow (FX3's fix 10), round 2 only | 0.91.0 carries fix 10 alone (7886bfdf, cherry-picked): its design-doc line, its interactions_check part, its build-table row | arrows-c carries the same fix through the p5-fix3 merge, with fixes 11-14 beside it | arrows-c's side (it holds 0.91.0's lines word for word, in one block, plus fixes 11-14); the build-table row kept once | The same change twice: one copy, the version already on the line (BM14's rule). The game file's fix 10 lines merged by themselves; checked that none is in the file twice. |

| 7 | Section 19, the Device engineer slot (round 8) | tip-clear adds FX5's `tipClear()` and its requestAnimationFrame | arrows-c adds the panel pointer block (POINT_ON, TEACH_MODES, pointAsk...) at the same spot | keep both, arrows-c's first | Independent code; tipClear reads #ixGoal's translate the way arrows-c's own check does. |
| 6 | player_check.py (round 5) | 0.91.0 added "A tray at any seat" (the eating fix's test) | arrows-c added "Tea in the Tea corner, every seat taken" (FE1 item 48) at the same place | keep both, 0.91.0's first | Two different tests, not a duplicate. The game's eating-fix lines are each in the file once. |

The eating fix (191d1853, cherry-picked onto 0.91.0 as fb29d37a from p5-fix2) is not on arrows-c yet, so it causes
no clash now; when p5-fix2 reaches arrows-c (batch 2), expect the same kind of duplicate as #5: keep the line's version.

## Conflicts in the docs

| File | What | Resolution |
|---|---|---|
| plans/backlog.md (open bugs) | controller added CP5-1, CP5-2; arrows-c added 30, 31 at the same place | kept all four rows |
| plans/backlog.md (fixed) | controller added CP4-1; arrows-c added the promotion-talk row at the same place | kept both |
| plans/build-table.md | controller added its "Controller support" section; arrows-c added patch-play1-c, playtest 1 part B and patch-p5-fix1 rows at the same place | kept both blocks (controller's first) |

## Quiet clashes looked for (merged without a marker)

- The controller's footprint outside its own section 26 is small: the Settings list (#3), the pause card's line id and
  `padPauseLine`, and four `padBuzz` calls (storage pick-up in `jobEnd` and `ixStopDone`, job done in `jobEnd` and
  `cartEnd`). All four buzz lines are still in the merged file at their places.
- No function or table that section 26 uses was removed or renamed on arrows-c (no top-level name is dropped).
- New on-screen things on arrows-c: the arrow pointer `#ptr` (not a button, so the controller's highlight correctly
  never lands on it), the job board rows gaining `data-job` (still the same rows and buttons inside `.ixpanel`, which
  section 26 already walks).

## Checks

Round 1 (on 0.64.17, now rolled back), kept for the record: check_fast OK; cadet_test alone vs arrows-c + 0.64.17
(no controller) ALL IDENTICAL; arrows queue, d, f OK; interactions_check FAILED "Deck 3 landing: tapping where the arrow
points opens the deck picker" (the same failure on arrows-c + 0.64.17 without the controller, and a pass on arrows-c
alone: breakfast and FX3's fix 10 test together, not the controller; gone with the rollback); controller_check
FAILED touch (six lines, tap0.seen) and pick (crowded seat) before that run was cut short; not chased, as its base
was rolled back.

Round 3 (claude/trial-p5-on-controller, controller 9a8eac0b + arrows-c 69d1ed9b):

| Check | Result |
|---|---|
| check_fast | QUICK CHECK OK |
| cadet_test strictly alone vs arrows-c + 0.64.16 (2cabe96b), no controller | ALL IDENTICAL |
| arrows_check queue, arrows_d_check, arrows_f_check | OK, OK, OK |
| interactions_check | OK (round 1's Deck 3 landing failure is gone with the rollback) |
| controller_check | touch FAILS: after a pad press (B, UP+DOWN, UP), the first mouse click shows 57 -> 54 visible elements. The same on CP1's 9a8eac0b alone (its own controller_check), so not from this merge; it passed on 0.90.8 + arrows-c. Sent to CP1 and lead 29; CP1 and RV9: a check-only fault (the message box counted in one run and not the other), CTT3 fixing the check. The rest of this run was lost to a container restart; round 4 below covers 0.91.0, which contains this base |

Round 4 (0.91.0 989fd566 + arrows-c 69d1ed9b, commit 8bd5d1c4; now claude/trial-p5-on-controller):

| Check | Result |
|---|---|
| check_fast | QUICK CHECK OK |
| arrows_check queue, arrows_d_check, arrows_f_check | OK, OK, OK |
| interactions_check | OK |
| controller_check idle, save, calls, walk, pick | OK |
| controller_check touch | the known check-only failure (as round 3) |
| controller_check day | 4 FAILs (the lift's Deck 3 button not found, could not walk to the lift / the bunk by the stick, no crew to walk to): CP1's known check-only fault (its route looks for the button by old words and walks into a ladder hatch), fixed in CTT2's newer controller_check |
| controller_check tiles | failed once ("A on square 13 should put the tile down"), then OK on a rerun on round 4 and on 0.91.0 alone: the known flaky part (backlog CP4-1) |
| controller_check games, unplug, odd, off, quiet, base, deck, pick1, panels, api, lists, disc, screens, marks, touch3, drop, settings, a11y, firstuse | OK |
| controller_check reach | not finished: stopped at the 2-hour limit on this loaded machine after 40 screen states, no FAIL; leave it to the full round |

Round 5 (01b237f4 + arrows-c 12b67c70, commit a4f7d4f0):

| Check | Result |
|---|---|
| check_fast | QUICK CHECK OK |
| arrows_check queue, arrows_d_check, arrows_f_check | OK, OK, OK |
| player_check | PLAYER CHECK OK |
| interactions_check | OK |
| controller_check, every part but reach (CTT3's corrected file) | CONTROLLER CHECK OK (touch and day pass now) |
| controller_check reach | not run here (over 2 hours on this container; for the full round) |

Round 5b (45362bd6 = round 5 + arrows-c 9197ba11): check_fast OK; arrows queue, d, f OK; player_check OK;
interactions_check OK; controller_check every part but reach OK.

cadet_test is not run on rounds 4 and 5: there is no "0.91.0 without the controller" to compare against; round 3's
ALL IDENTICAL (same controller, same arrows-c) covers "the controller off changes nothing visible".

Dry run (trial file 83b8255 = controller fda82c1 + arrows-c c26f194):

| Check | Result |
|---|---|
| check_fast | QUICK CHECK OK in 161 s |
| cadet_test vs claude/arrows-c c26f194 (strictly alone) | ALL IDENTICAL (renderer noise only, max 1 level): the controller switched off changes nothing visible |
| controller_check (all parts) | CONTROLLER CHECK OK |
| arrows_check queue | ARROWS CHECK OK |
| arrows_d_check, arrows_f_check | OK, OK |
| interactions_check | INTERACTIONS CHECK OK |

Setup notes for whoever repeats this: three.js and acorn in /tmp/cadet-work (testing guide section 2); `pip install
playwright`; set `CADET_CHROME=/opt/pw-browsers/chromium` for every check run outside check_fast (check_fast sets it
itself; without it Playwright looks for its own browser and stops).
