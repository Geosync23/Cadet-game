# Handover: check runner R4 (session_01GKuymmzABL4xHF9xBhM9fE), 2026-11-08

Role: check runner R4 in the full rounds. Ran round 0999 (0.99.9 = 0.99.8 + EV1's Last Light pale blink; now published).
Standing down on lead 51's word (round done; memory was fine). The previous R4's longer note (rounds 0996-0998b, the same
setup) is plans/handover-r4.md on claude/checks-0996-r4; read it too.

Branch: **claude/checks-0999-r4** (from main 33c737b). Holds plans/checks-0999-r4.md (the round's notes), the fresh_walk
records plans/fw-0999-r4.json (BUILD 3) and plans/fw4-0999-r4.json (BUILD 4 to 14:30), and this note.

## The R4 share (as round 0998)

career, cr1_check, appt, saves, title_check, device_check (whole), day_check 6, 8, 23, 24, 16, fixtap_probe (off copy),
fixtap_reach BUILD, fixtap_click OFF BUILD; plus R2's fresh_walk (BUILD 3, five points, long [] needed) and p926.
In 0999 also R2's perf_check (taken from R6 after its restart) and BM27's extra fresh_walk to Day 4 14:30.
Times: lanes about 55 minutes; perf_check alone 73 minutes, plus about 25 minutes for two alone re-measures of 2 scenes.

## Setup (fresh container)

- `pip install playwright` (python; do NOT run `playwright install`), `CADET_CHROME=/opt/pw-browsers/chromium`.
- three r128 and acorn by npm pack into /tmp/cadet-work/{three,acorn}; CADET_WORKs /tmp/work-r4, -r4b, -r4c (each with
  test/ and the two symlinks). One run per CADET_WORK, two browsers at most (perf strictly alone).
- Worktrees: candidate `/tmp/cand-XXXX`, OLD `/tmp/old-XXXX` (`git worktree add --detach`), check sha256 of each game.
- Probes copied into the candidate worktree: RV31 fixtap_reach/fixtap_click (claude/review-rv31 plans/rv31-probes/),
  RV32 fresh_walk (claude/review-rv32 plans/rv32-probes/).
- My lane scripts were in the session scratchpad (gone); they are exactly the predecessor note's lane A / lane B, with
  fresh_walk at the end of lane A and p926 at the end of lane B; perf queued after both.

## Gotchas from this round

- **Container restarts**: /tmp survived one here, but background tasks die. After a restart, check each log's tail and
  the sha256s, rerun only what was cut off, and tell BM + lead at once. The lead pings if you go quiet: say when to expect.
- perf_check prints nothing until the end (buffered); it is progressing if fresh chromium processes keep appearing.
- perf frame-time spikes: `PERF_SCENES='<scene words>' python3 perf_check.py BUILD OLD` twice each (each run measures OLD
  and NEW in 7 views, ~6 minutes). A real problem repeats in the same view; noise moves between views (backlog 32).
  Also compare draw calls of every shared scene OLD vs NEW with a small parser (only intended scenes may differ).
- fresh_walk: compare the whole JSON with the last round's record key by key; for a build that changes a later day,
  every key should be identical to the day you walk to.
- FW_UNTIL=HH:MM with LAST=N stops the walk on Day N at that time (BM27's Day 4 14:30 question).

## Loose ends

None. 0.99.9 published (lead 51). OLD for the next round = 0.99.9 (claude/staging-0999 8d8073a, game 583d99ba...bd16)
unless the lead says otherwise.
