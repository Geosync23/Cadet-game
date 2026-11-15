# Handover: build master BM29 (session_01GKuymivPt7VEMWm4jUuY4G), 0.99.92-review (the Fable review version)

For lead 52 (session_01GKuymmPLvgySfNEhDYyACj) and the next build master. Read plans/handover-bm28.md (claude/handover-bm28)
and plans/handover-bm27.md (claude/handover-bm27) first: their "How I ran it" and gotchas still hold. Then this.

## State (2026-11-15 ~11:50 UTC)
- Nothing of mine is running. FINAL GO given for 0.99.92-review: claude/staging-fable-review, game commit c4999dae (the
  tip is later, docs only), game sha256 d6b9ce81a5254ab089f07afad01ed20edbd05e38d12a6043092f0578f9efa1c0.
- **main and claude/integration are untouched: 0.99.91, cdd9efd, game b321a4ec...95f3.** The review version is a SEPARATE
  version on its own link; lead 52 publishes it when the user approves. I published nothing.
- Record: plans/round-fable.md (the whole round on one page: shares, cost rules, wave 1, every share's result).
- Local scratch (goes with the container): /home/user/wtfr (worktree), /home/user/bm29 (logs, old.html, pre_onebyte.html).

## What 0.99.92-review is
0.99.91 + FR1's claude/fable-review-code a077808 (safety and speed, nine switches; robust_check.py; tools/one_byte.py) +
FR2's claude/fable-review-play fe156c8, then ab130f2 (twelve FRP_ switches; frp_check.py), both RV37 PASS, each merged on
lead 52's word. Then: the 21 switches on (TEX_READ_ON stays OFF: it changes pictures, a question for the user),
tools/one_byte.py last, label 0.99.92-review, DEV_NOTES paragraph (top of the file), build-table row.

## If the user asks to adopt the review version into main (a new job)
1. It is a game change to main: the user's rule means the full round again on the adopted file, unless the adopted file
   is byte for byte d6b9ce81 (then lead 52 decides whether round fable stands; I would say it does, the round ran on that
   exact file against OLD = 0.99.91).
2. Decide the build number with the lead: "0.99.92-review" is a review label. A plain number (0.99.92) changes the file
   (two lines), so its sha256 changes: at the least check_fast, cadet_test vs d6b9ce81 (ALL IDENTICAL expected) and the
   lead's call on the round.
3. Merge claude/staging-fable-review into claude/integration, then main (fast-forward if nothing else moved).
4. DEV_NOTES: the two review sections still say "off" (the pieces were built off); the top paragraph says they are on.
   Tidy the wording when adopting.
5. From now on the script is in one-byte form: a helper who writes an arrow, a long dash or a curly quote in the script
   fails names_check. Write \uXXXX in strings, plain words in comments. content_gen and lines_check follow the mark.

## Tools (plans/build-master/bm29/)
- switchon.sh GAME: the 21 switches on, each line found exactly once, TEX_READ_ON checked off. LIB_SAY_ON's line is
  indented (`  const LIB_SAY_ON`), inside the page's first script: any all-off or switch-on script must allow for it.
- r5-fable.sh: R5 as a re-runnable script (BM27's pattern; paths point at /home/user/wtfr and /home/user/bm29).
- The five round checks that used to live on review branches are now in the repo (plans/rv31-probes/, plans/rv32-probes/).

## What worked this time
- **A rehearsal before any PASS**, on a local scratch branch never pushed: merge both tips, all switches on, escape,
  label, then check_fast, lines_check, the pieces' own checks and cadet. It found four faults before the real build (a
  194-character line; lines_check not knowing the one-byte mark; device_check failing with FRP_PANELS_ON; frp_check
  unable to run on a switched-on build). Ask each fixer to run check_fast, lines_check and its own check on an ALL-ON
  copy before it calls a piece cleared.
- **Cost rules** (in round-fable.md): runners read only the round page and their own handover note, never DEV_NOTES
  (190,000 tokens); no check twice (the build master's gates are the round's runs when on the final sha256, and the
  record names the seat); OLD only on a FAIL; wave 1 by the build master alone before the runners are hired; runners
  silent until their final report. One candidate, one round, about 2 h 10 min from the GO to the FINAL GO.
- cadet_test with the switches on was not identical, by design. The proof that nothing else moved: the same comparison
  with only the picture-changing switches off (here FRP_LABEL_ON and FRP_FOOD_ON) gave ALL IDENTICAL.

## Gotchas this time
- The account's 5-hour usage limit stopped every seat once (about 05:11 to 07:40 UTC). /home/user and /tmp survived.
- lines_check is not in check_fast; run it after every merge and after one_byte.py.
- frp_check and robust_check make their own off/on copies; both run on the switched-on build.
- fresh_walk repeats itself on one build (only a few minutes' drift under load), and FRP_TRAY_ON / FRP_FOOD_ON change
  the walker's days from Day 0 18:26 on: its record no longer matches 0.99.91's line for line. That is intended.
- Checks that flicker when another browser runs beside them: title_check (backlog R4-1), lines_check --day (R2-1),
  sound_check (BM27-1), controller G2 tiles (CP4-1, clean this time).
- Reviewer and fixer messages arrive before the lead's; merge only on the lead's word and commit (the lead changed
  FR2's commit from fe156c8 to ab130f2 a minute after the first word).

## Sessions (round fable)
R1 session_01GKuymidX8V6F2KKDcoZ5LE, R2 session_01GKuymigbASLB86pjcbY5LY, R3 session_01GKuymjwGjfNXnjezjs87rS, R4
session_01GKuymnZfZ6qmpeytQExvGQ, R6 session_01GKuymjzQWrtt6PCGyfmQUB (notes on claude/checks-fable-rN). FR1
session_01GKuymmYzraWXg9ELUMmqri, FR2 session_01GKuymj5amgjHqQCKPsVnFs, RV37 session_01GKuymo8n7x4hGZtoPmWXqX.

## Open (lead 52's, for the user)
- TEX_READ_ON (A9): built, off; it changes pictures.
- A player following the arrows has a different first three days than in 0.99.91 (tray seat, Food marker): intended.
- Quiz question 34 says "rec deck" with no switch.
- Backlog rows added in this job: BM29-1 (the test picker and the guide's table are out of step with the real round),
  FR1-3, FR1-4, R4-1, R2-1, R6-1 (Day 14: Theo stuck 20 minutes, in the live game too), RV37-2 (a room arrow gives a tap
  nothing to do).
- FR1's B10 items not done: a WebKit smoke check, setTimeout on the test clock, the round as a GitHub job, an
  expected-parts list per build; food_check has a part that tests nothing ("Schedules: not using the rota yet").
