# Handover: build master BM23 (session_014zyJYPpetpQqNvn9pkGrig)

Written 2026-11-01 ~01:15 UTC for lead 48 (session_014zyJYMuqdRYh4dQhmVPr8S, branch claude/lead-48). The project is about to
move to another account (GitHub already says the repo moved to Geosync23/Cadet-game; pushes to the old URL still work by the
redirect). This note is meant to be enough for a fresh build master who has never seen the project.

## Who
- Build master (BM): merges reviewed pieces into one staging branch, sets the build number, runs the merge gates, sends the
  GO to the round's runners, runs share R5 itself, writes the round record, sends the final GO to the lead. Never publishes,
  never pushes to `claude/integration` or `main` (the lead does that after the publisher reports).
- Before me: BM22 (session_014zyJYNgBPdEPHLxTGrM889), plans/handover-bm22.md. Read it too: its tools and gotchas still hold.
- Leads this round: lead 47 (session_014zyJYM4mt9ZDCD5H9JZDtN) then lead 48. Reviewers RV29 (session_014zyJYM3D7UBkZN49CsZVuA)
  and RV30 (session_014zyJYNFR7ewWJGvEQNUAHr), both stopped at their memory limits (RV30's notes: claude/review-rv30
  plans/handover-rv30.md). Runners R1 session_014zyJYQ4EiB7CipGp4HsYV8, R2 session_014zyJYMsL5YqKnLb9Q6Lvyz,
  R3 session_014zyJYPN2WU6wpJgghsXiAe, R4 session_014zyJYNRijQBB389vXWxWNJ. Session ids will not carry over to a new account.

## State at handover: 0.99.5 done, final GO sent, being published
- `claude/staging-0995` = 6475bb30 (round record). Game sha256
  93aed54fa9296e75c308ae199cbac32465c776c650161fe41bf22535839a5164. Lead 48 verified it and is fast-forwarding
  `claude/integration` and `main` after PUB3 publishes.
- Chain on staging (from BM22's 023c416): b6dcefd TB5 merge, 49945bb switch-on (SND_LONG, MESS_SCALE, SND_BUF_ON,
  TRAD995_ON, TRAD926_JOIN_ON on; the user's pick on Mess Hall Murmur 2026-10-31), b7f027e build turn (0.99.5 lines),
  c1b737f + 96d902e sound_check r3mess (RV30), 247fc12 PL2 fix merge (75e22d2: Day 2 office meeting), ee66e35 RV30 tea fix
  (Works hot water makes tea again; ixTeaFirst), e00bfab docs (GO commit), cc18dad arrows_check walker (RV30),
  93839bf puzzle_check paper line (RV30), bb45099 puzzle_check P5FIRST clock order (me, lead 48 read it), 6475bb3 record.
- The round's whole story is in the 0.99.5 row of plans/build-table.md and the 0.99.5 paragraph at the top of DEV_NOTES.md.
- Runners' notes: claude/checks-0995-r1 dd8f4738, -r2 67b87609, -r3 f952c5b3, -r4 5530b789. My R5 results are in the
  build-table row (21/21 on e00bfab; no separate notes branch).
- Backlog rows added this round: P5-1, JB2-2, JB2-3 (for 0.99.6). Older open ones still matter: PL2-1, PL2-2, TB5-1, RV29-1,
  BM22-1/2/3.
- Other branches of mine: claude/bm23-wip (my working copy, = 6475bb3 now), claude/bm23-cand (247fc12, the pre-tea-fix
  candidate for RV30), claude/bm23-puzzle-p5 (bb45099). All can be deleted once 0.99.5 is on main.

## What a build turn looks like (as done for 0.99.5)
1. Staging branch from the last published build. Merge each piece at its reviewer's exact PASS commit (`git merge --no-ff`),
   then `python3 plans/build-master/verify_merge.py` (after the commit; see gotchas). Table-row clashes: keepboth.py.
2. One switch-on commit (only the switches the user/lead approved), with design-doc's Open question moved to Answered.
3. Build turn: header `build` line and `GAME_BUILD` (setbuild.py), DEV_NOTES paragraph, build-table row.
4. Gates on that exact file, at most two browsers at once, cadet_test alone at the end vs OLD: names_check, check_fast, and
   every check the pieces touch. For 0.99.5 this also needed the WHOLE intro_check and interactions_check: each caught a
   real game bug the pieces' own reviews missed (Day 2 office door; Works hot water). Run the long whole checks in the gates.
5. Explain every cadet_test difference (diff A_*.png vs B_*.png) before the GO.
6. Push staging, send each runner the GO directly (commit, game sha256, OLD commit + sha, the share file, corrections),
   copy the lead. Run R5 (`bash plans/build-master/r5.sh WORKTREE LOGDIR`).
7. Any FAIL: is it on OLD too? Run it there. NEW ones to the lead at once. Find game vs check before anyone edits:
   turn switches off one at a time in a copy (sed the `const X = true` line; JB2's three are one line:
   `var JOBCAP_ON = true, SPREAD_ON = true, CHECKS_ON = true;`). A check-only fix keeps the game sha, so only that check
   re-runs. A game fix means a new sha and a re-run list the lead approves.
8. All five shares OK: round record (build-table row + backlog rows + DEV_NOTES "full round green, waiting for the user's
   OK to publish"), push, final GO to the lead.

## Round plan
plans/round-0995.md (written by BM22 before the switch-on: its "stay OFF" line is out of date, all switches are on now).
Shares R1-R4 fresh runners, R5 the BM. Reuse it for 0.99.6 and add the areas the new pieces touch. Times this round:
R2's perf_check alone ~70 min, intro whole ~50-60 min, interactions whole ~45-60 min, events ~25 min, check_fast ~5 min.

## Tools (plans/build-master/; see handover-bm22 for the list)
run1.sh, gate.sh, r5.sh, keepboth.py, verify_merge.py, setbuild.py as BM22 described. Setup: `pip install playwright numpy
pillow`; three@0.128.0 in /tmp/cadet-work/three and acorn@8.12.1 in /tmp/cadet-work/acorn; `export
CADET_CHROME=/opt/pw-browsers/chromium` (forget it and Playwright says "Executable doesn't exist"); each run its own
CADET_WORK. A quick partial check: copy the check file into a scratch folder with cadet_test.py and cut it at a part's
`print('== ...')` line (I did this for interactions' parity part, ~5 min instead of an hour).

## Gotchas (new this round; BM22's still hold)
- `pkill -f <name>` with the name in your own command line kills your own shell. Kill by pid from `ps`.
- The stop hook asks you to push unpushed commits: never push ungated work to staging; push a backup branch instead.
- Going back in time in a check (setShipNow earlier than before) makes machinesNow reset and replay every machine: set
  machine state AFTER the clock (that was puzzle_check's p5 FAIL).
- arrows_check's walker must tap a person for a tradition's join arrow (`g.tj`), not open a chat; new tap-to-join or job
  kinds may need the walker taught.
- appt_check prints planted FAIL lines as its self-test; fine when it ends OK. lines_check: 112 warnings is normal.
- perf_check: a one-off spike that doesn't repeat when re-measured alone is known noise (backlog 32).
- Messages from other sessions can cross; reread the latest before acting. Runners may have an older sha from the lead:
  the GO's sha is the one.

## Open questions for the user
None from me.
