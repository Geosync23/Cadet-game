# Handover: IM1, the trial-merge helper

Role: merge helper. Trial-merge the next build's pieces ahead of the build master (BM14) so the real merge is quick;
write every clash and its resolution down; run the checks; report reds to the lead (now lead 31,
session_0118SXBCdg87nDiXdtrGNVSR) and the owners; send resolutions to BM14 (session_016mhGtsCxEgPCFn9C767yjq).
Push only to `claude/trial-p5-on-controller`. No game behaviour changes beyond resolving clashes.

## Where things stand (2026-10-23, about 03:40)

The 0.92.0 combined build for the user's morning (lead 30, then lead 31): on BM14's staging `claude/integration-next-fe1`
01b237f4 (0.91.0 + CP1's controller follow-up 1 + CTT3's controller_check), merge in this order:
arrows-c, breakfast-back, zeke-tour, dinner-spread, tip-clear, hygiene-cool (FX6), tiles-sit (FX7).
Coming later on arrows-c via AC3: FX3 fix 19, FB1 8438e7f + bd291e4, FX5's booth-arrow fix (maybe DV1's Dev-mode career
arrow, likely the next build).

`claude/trial-p5-on-controller` = round 10, e819950a (plus this note): 01b237f4 + arrows-c 8eb57151 (arrows ON) +
breakfast-back 0cd37b1b + dinner-spread ed6bcbf3 + tip-clear feb2e54a + zeke-tour 99687fc8. (dinner-spread was merged
before zeke-tour because zeke-tour landed later; the merge order made no difference: no clash.)
Round 11 = 14d80a87: + hygiene-cool cbd41548 (FX6), only a build-table row clashed; check_fast OK; its area checks not run
(player_check is the one it touches most). Not yet on GitHub when I stopped: tiles-sit.

## The resolutions (the full table is plans/trial-p5-on-controller.md)

1. Settings view (section 12): arrows-c's Teaching arrows row inside the list, then the controller's
   `.concat(typeof padSetBlocks === 'function' ? padSetBlocks() : [])`. New game sits higher; no clash.
2. jobEnd's repair finish (17b): arrows-c's `caseFitted` branch first, `else if (finishJob(...))` with the
   controller's `padBuzz('done')`.
3. FX3 fix 10 (on 0.91.0 and on arrows-c): take arrows-c's side in design-doc and interactions_check (it contains
   0.91.0's lines word for word); its build-table row once.
4. player_check: 0.91.0's "tray at any seat" and arrows-c's "tea corner" tests, both kept.
5. Section 19's Device engineer slot: arrows-c's panel pointer block, then tip-clear's `tipClear()`; both kept.
6. Build table: every piece's rows kept, in merge order. dinner-spread's branch carries breakfast-back's rows, so the
   "meal traditions thin out" row can land twice: keep it once. Check for stray `=======` lines after joining rows
   (my row script once left one; it now refuses to finish with a marker left).
   Every other file merged by itself in every round.

## Check results on the latest rounds

- Round 5c (01b237f4 + arrows-c, arrows OFF): everything green (check_fast, arrows queue/d/f, player, interactions,
  controller_check all parts but reach). Reach takes over 2 hours on these 4-core containers; left to the full round.
- Round 8 (arrows ON, before zeke-tour): day_check OK, events_check OK. interactions_check: the "Clock in" failures
  (fixed in the check by AC3, 8eb57151) plus two bar ones to recheck ("the bar by day: Back at 17:30", "every bar stool
  held: In use"). controller_check walk CRASHED: `page.click('#rot')` timed out (Rotate view not clickable with the
  arrows on?). Not yet confirmed or reported to CP1/AC3.
- Round 10 (e819950a, game = e1007025): check_fast OK; day_check OK; events_check OK. interactions_check FAILED (87
  lines: pins still "Clock in: shift at 09:00" at turn-in and job stops even after AC3's 8eb57151; "the bar by day";
  3 pageerrors "reading 'updateWorldMatrix'" in the haul tests); BM14 saw the same (184 lines on e1007025) and is
  isolating it on 168900ea and arrows-c 8eb57151 alone. controller_check: walk OK this time ('#rot' did not repeat);
  pick FAILED 4 ("the bottom line never named it": crew, item, sealed door, the lift) and day FAILED 2 ("the ring never
  named the lift", "bedtime: the lift panel never opened"); green on round 5c (arrows off), so likely the arrows on;
  not isolated. Later results: food_check OK, arrows_d OK, arrows_f OK; intro_check FAILED 2 ("no pilot's line when the
  ramp opened"; the solo job's arrow stuck on "10:45 meet Zeke: Works bay": try it on 168900ea, without zeke-tour);
  controller_check also marks and drop: the one-time "Controller connected" never shows (guess: the arrows' pop-up queue
  holds the toast; AC3 and CTT3). player_check and arrows_check queue had not run when I stopped. All sent to BM14 and
  lead 31; BM14 is isolating interactions_check.

## How to test (what I ran)

- Setup: three.js r128 and acorn 8.12.1 in /tmp/cadet-work (testing guide section 2); `pip install playwright`;
  `CADET_CHROME=/opt/pw-browsers/chromium` for every check outside check_fast.
- check_fast in the trial's folder; then, each lane in its own CADET_WORK: interactions_check, player_check,
  arrows_check queue | intro_check, food_check, arrows_d_check, arrows_f_check | day_check, events_check |
  controller_check with every part but reach. About an hour on a loaded 4-core container.
- cadet_test is only meaningful with a "same build without the change" to compare; round 3 proved the controller off
  is invisible (ALL IDENTICAL).

## Gotchas

- Never stop runs with `pkill -f <pattern>` when the pattern is in your own command line: it kills your own shell.
  List the PIDs first (`ps -eo pid,args | grep ...`) and kill those.
- Background waiters on a file being non-empty trip early; wait for the `== exit` line instead.
- Keep each trial in its own git worktree so running checks keep their files when you merge the next piece.
- Known check-only reds: controller_check touch and day on the old check (fixed by CTT3's file on 01b237f4); tiles is
  flaky (backlog CP4-1).

## Open for the next session

Who gets what (lead 31): the controller_check walk '#rot' timeout, if it repeats, goes to AC3
(session_01DiLRzrXgkeoAZCoX1mVJn9; likely an arrow or tip over the Rotate button, which matters for players even with the
controller off), copy CTT3 (session_0197zJtQyLkNz6dxc3NgoNgy); CP1 has stopped. The bar failures go to lead 31 with
their cause. zeke-tour will get a new commit from DS1 (the user rejected the bag auto-stow): merge it when it lands.

1. Rerun round 10's area checks; chase the controller_check walk `#rot` crash and the two bar failures (are they on
   arrows-c alone? then AC3's; otherwise the merge's).
2. Run the area checks on round 11 (hygiene-cool: player_check first); add tiles-sit when on GitHub; then AC3's remaining arrows-c fixes.
3. Send BM14 the final sha and results.
