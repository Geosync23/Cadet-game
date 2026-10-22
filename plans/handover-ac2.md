# Handover: AC2, arrows builder (piece D) and assembler of claude/arrows-c

AC2, session_015uhdrDuE49CJ8iWWX2SEeP, 2026-10-22. Leads: 28, then 29, now **lead 30** (session_016evGvfNY88TNKgaHErG9Q8).
Read CLAUDE.md, DEV_NOTES ("The arrow queue"), plans/handover-ac1.md, plans/arrows-c-assembly.md (what's in the branch,
reviews, what's waiting) and this.

## Branch
`claude/arrows-c`: the assembly branch for the Pillar 5 + arrows + fresh-eyes batch 2 build (lead 29). Merge commits and
`cherry-pick -x` only, never rewrite. BM14 merges it onto 0.91.0 once every piece has a PASS (lead 30).
Keep `plans/arrows-c-assembly.md` current with each merge.

## What I built
- **Piece D, the shift chain** (15b slot, `guideShift()`, once a ship minute from `guideTick`, GUIDE_ON / POINT_ON):
  S2 clock in, S3 take a job (`guideTakeable`, which reads `ixBoard.doable`), S7 clock out (over a held job, until
  friAutoOut), pointers on Clock in / Take it / Turn it in / Clock out (3 times), S8 Work log, S9 reputation word (up:
  "Works reputation: X" + Training pointer once; drop: "Works reputation down: X"). S1 is FX1's On shift row; S6's word is
  FX1's `boardEmptySay` (held through a meeting, a training's watch/turn, a dialogue). `guideGoal` passes over an entry
  with nothing to show (RV6's T3 note); T3 gives way at the shift's end. FX1's `trainArrow` stays down with the queue on.
  RV6 PASS (4ef580e) and RV7 on the later commits.
- **Switched-on fixes:** the board's Take it for rounds and hauls (`BOARD_KINDS`, 15b; RV7 PASS); the tea arrow clears
  when tea's over (15 `teaOffer`, trk window; RV7); the job arrow rests after clock-out (15b `ixJobStep`; RV7 PASS);
  the pop-up queue keeps "Trained: ..." / "Works reputation" words (`TQ_KEEP`, 15b slot, GUIDE_ON only; RV7).
- **arrows_check follower** (RV7 reviewing): a job "asked for you" first at the board; a real screen tap at the pin
  *as drawn* (`#ixGoal`'s pin) for your held job's own step only (never the board, the time clock or a named thing);
  a tap on a thing sets the ray through it first; a leisure activity started while you hold a job is ended; up from a
  sit-down once its minutes are in; Fault notes for a head-scratcher's call; a device left open is closed;
  `careerClockedOut` for "clocked out".
- **Checks:** `arrows_d_check.py` (about 2 minutes; every line has a planted fault it catches; mutant list lives in my
  scratchpad, the names are in the build-table rows). interactions_check (board kinds), player_check (tea not taken).

## Where the week stands (arrows_check week guide)
On the tip before FX3 16-18 and before the pin-tap follower: m1 Day 2, m3d + m4 Day 3, m5 Day 5, m7 Day 6; m3i, p3, m6
not learned; stucks at machine pins (the floor-tap follower's miss, fixed by 3430ea1). Rerun on 3c42632 under way when
this was written (see the latest message to lead 30).

## Loose ends
- The inspection morning's queue entry (FX3's direct arrow in 24c steps aside with the queue on: `inspectGoal(d)`,
  `inspectDue(d)`; add a level-4 entry in 15b, 06:00-06:30).
- FB1: the galley dry-goods drop (a tap on its pin walks, never drops; lead 30 routed it). Merge when RV8 passes.
- FX3: the climbing wall. Merge when RV7 passes.
- Game note (raised, not owned): with the queue off nothing points a player at Fault notes after "it still leaks".

## Gotchas
- `careerClockedIn(d)` stays true after clocking out: use `careerClockedOut(d)`.
- A follower that mixes real clicks and `playerTap` must set `ray` first (FX3's `jobRayDist` reads the last tap's ray).
- A `//` comment inside a one-line JS block in arrows_check's FOLLOW swallows the rest of the line: comments last.
- Background `until` watchers time out at 30 minutes; write runs to a log with `nohup` and poll the log.
- Run cadet_test alone; use a second CADET_WORK (/tmp/cadet-work2) for check_fast while another browser check runs.

## How to test a merge here
names_check, check_fast, then the area checks of what came in (interactions_check, player_check, intro_check --firsts,
mech_check fx3, arrows_d_check, arrows_f_check), then arrows_check week (off) and week guide (on), and shift guide.
