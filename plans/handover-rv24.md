# Handover: RV24 (reviewer, Step 6), 2026-10-27

**Role:** reviewer, from RV23. Lead: lead 43 (session_01GKuymjoDoY2kA9yCK12NG1) from 2026-10-28 02:05; before that lead 42 (session_01GKuymjnCHnpwDqB94PVwmV). send_message, priority "next". My session:
session_01GKuymnJuoJTWnmYunbN7EP. Notes-only branch `claude/review-rv24`; full log and verdict table: `plans/review-rv24.md`.
Never change the game or push to builders' branches. Verdicts to lead 42, the builder and BM19 (session_01GKuymncYhRTKs8t4byNfdj).

## State at writing (17:5x): idle for the Step 6 round, on lead 42's word. Nothing open from me.
PASSes sent: W8 promo4 6f13b61a and 9063aafe (whole W8 item); DA6 p5s6-deck 2df6bfce, 5c27b740, 4a84e153; AS1 m24-pick-pointer
5f649b45; code-read OK: PZ6 escort-seated-check 775c3ca, AS1 arrows-step6 ee18d663/75f6262c (both merged, the round covers them).

## Seats and ids
W8 session_01GKuymk95u5t4uDsahatkPN (claude/p5s6-promo4; it didn't have my id at first: message it directly). DA6
session_01GKuymjJ4sU5hfdU8bH49UW (claude/p5s6-deck). AS1 session_01GKuymmdgtDvbd8P7URXd4z (took over from PZ6). RV23 idle.

## How I test (as RV23, plus)
- Setup per plans/testing-guide.md section 2; two lanes (/tmp/cadet-work, /tmp/cadet-work2), at most 2 browsers on 4 cores; a third
  browser makes screenshots time out and cadet_test show 1-level renderer noise (re-run alone).
- Worktrees /tmp/rv24/wt-<sha>; ON copy: sed of the P5_STEP6 line to `P5_STEP5 && true`.
- Dev presets in probes: `devmodeRun('Set career: beat', () => devmodeSetCareerTo(day, DM_BEATS.find(b => b.id === 'x')))`.
  devmodeSetCareer (the panel's) steps by setTimeout and never finishes under the test stepper (why RV23's mt_play stayed on Day 0).
- Probes in plans/rv24-shots/: cq_play.py (Calder's question: parts stand, sit, miss), m23_door.py (night 2's reactor door at each
  step), d2b_look.py (room B keepsakes), mt_play.py (Basil's day; takes no job, so only the hello and the arrow), d22_play.py
  (Day 22 coarse follower; stalled at 08:47: debug before relying on it).
- Gotchas: never `pkill -f`/`pgrep -f` with a name in your own command line (exit 144 kills your shell); bash reads a running script
  as it goes, so don't sed-edit a lane script that's already waiting (my DA6 lane3 ran the old sha); copying promo_beats_check.py
  under another name breaks its cadet_test lookup (it uses its own file name); git push can hang: use `timeout 60 git push`.

## Open questions for the user
None from me.
