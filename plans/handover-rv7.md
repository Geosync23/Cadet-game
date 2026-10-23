# Handover: RV7 (reviewer: Pillar 5 fixes, the guiding arrows, the teaching-arrows switch)

Written 2026-10-23 by RV7 (session_01RLTBGbbdRbUkKME189xL4k) at about 50% memory, kept up as work goes.

## Role, branch, people
- Reviewer. Never edits the game. Notes only, on `claude/review-rv7` (push only there).
- Lead now: lead 31, session_0118SXBCdg87nDiXdtrGNVSR (leads 29, 30 before).
- Builders: AC3 session_01DiLRzrXgkeoAZCoX1mVJn9 (owns claude/arrows-c; AC2 session_015uhdrDuE49CJ8iWWX2SEeP handed over),
  FX3 session_01UZWrZRivwQJPKL3x7c8Ft9 (claude/p5-fix3). Other reviewers: RV8 session_01Q6uHYWus4ncyEgqWEYhJh5 (fresh-eyes),
  RV9 session_01E31oZQU7DFbZnh2BesWsnM (FX4, FX5).
- Verdicts go to the builder and the lead with send_message, plain words, PASS / PASS WITH FIXES / FIXES NEEDED, memory %.

## Verdicts (all in plans/review-rv7.md)
1. AC2 6610dc7 (Take it for rounds and hauls): PASS WITH FIXES; fixed in 78fef90.
2. FX3 2cdc1df (fix 14, laundry pin): PASS.
3. arrows-c 69d1ed9 + 78fef90 (FX3 merge, tea arrow, BOARD_KINDS): PASS.
4. arrows-c 86faa86 (no job arrow after clock-out): PASS; its follower (86faa86/5160b81): FIXES NEEDED, later fixed.
5. FX3 fixes 16-18 (410954b, c3d246f, cc61962; a9cabf75 check line): PASS.
6. arrows-c 483c3da..14249d8 (pop-up queue keeps "Trained", F2 inspection arrows): PASS.
7. arrows-c 8dd03049 (follower: career arrows, wait in a meeting room): PASS.
8. The shipped default before the switch: Off lost the watch arrow (fixed in f8ed8521).
9. arrows-c e3c7c183 + 764438d4 + f8ed8521 (teaching arrows ON in 0.92.0; Off keeps the watch arrow): PASS.

## Still to do (lead 31's list)
- FX3's fix 19 (the hydroponics vent and "Mop up (2 of 2)" stucks: the only things left in the week).
- BM14's merge of arrows-c onto 0.91.0 (the combined 0.92.0 build). Check: the merge's conflict resolutions, cadet_test
  alone vs 0.91.0 (explain every difference), the week on the merged build with the default setting and with Off
  (p_audit.py, TEACH=off), the pointer under Off (p_ptr.py), arrows_d/f/pointer, check_fast.

## How I test (scratchpad, not in the repo; copies of the probes in plans/review-rv7/)
- Setup: `pip install playwright numpy pillow`; three r128 and acorn in /tmp/cadet-work (testing guide 2);
  `export CADET_CHROME=/opt/pw-browsers/chromium`; two browsers at most, each its own CADET_WORK (/tmp/w1, /tmp/w2 with
  `test/` and symlinks to three and acorn).
- Builds: `git show SHA:starship-cadet.html > b.html`; check files copied from the same SHA next to them.
- `p_week.py BUILD [guide]` (ACHK=arrows_check file to use): the week with arrows_check's follower, logging learned
  lessons, toasts that reached the screen ("Trained", reputation, the board word), jobs taken, stuck lines.
  `p_audit.py` adds every arrow's source and level; TEACH=off sets Settings' Teaching arrows to Off.
  `p_ptr.py`: the Clock in pointer asked or not, First times vs Off. `p_cart.py`, `p_toast.py`: one-off probes.
  With arrows_check from f8ed8521 on, set `TEACHOFF = False` after the exec (p_audit.py already does).
- Planted faults: exact-string replace on a copy (`mut.py`), run the check, expect one FAIL naming it.
- cadet_test strictly alone.

## Gotchas
- The arrows_check follower is not a player: older versions call playerTap directly with no screen tap (FX3's ray-based
  fixes can't help it); check with a real tap (`page.mouse.click` at the projected pin) before calling something stuck.
- With the arrows on, a toast wrapper sees queued toasts twice (the queue replays them through toast): log only what
  reaches #tx.
- `pgrep -f` with `\|` doesn't match; wait on a log line instead. Foreground `sleep N; cmd` is blocked.
- Notifications arrive only between turns: ReadNotifications.

## Open questions for the user
None of mine.
