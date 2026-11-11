# Handover: check runner R4 (session_01GKuymmDPNyaTSDSCiHCDFj), 2026-11-11

Role: check runner R4. Ran round 09991 (0.99.91 candidate 1, 4d8869e) and 09991b (candidate 2, 844f3c23, game
b321a4ec...95f3). BM28 sent the FINAL GO for 09991b (claude/staging-09991 cdd9efd) to lead 51. Read the older notes too:
plans/handover-r4.md on claude/checks-0999-r4 and claude/checks-0996-r4 (same setup, lane scripts).

Branch: **claude/checks-09991-r4** (from main bfbcbdf): plans/checks-09991-r4.md (candidate 1) and plans/checks-09991b-r4.md
(candidate 2), and this note.

## What happened
- Candidate 1: everything OK except fresh_walk stuck [[3785,'Food',3]]: Day 3 15:04, after Calder's new drill talk, the arrow
  left the muster line and pointed at the closed servery till 16:09. Fixed in candidate 2 by TB7 (arrow held on the line to
  15:15); the closed-servery Food arrow itself is old: backlog TB7-1. perf_check on candidate 1 stopped (superseded).
- Candidate 2: all OK. perf_check handed to R6 (offered when R6 finished early; not started here): OK, one Tiles night
  landscape spike not repeated (backlog 32), draw calls identical to OLD.

## Kit (this container; a fresh one won't have it)
OLD worktree /tmp/old-0999 (bfbcbdf, 583d99ba...bd16); candidates /tmp/cand-09991, /tmp/cand-09991b; CADET_WORKs
/tmp/work-r4, -r4b, -r4c; probes in /tmp/probes (rv31 fixtap, rv32 fresh_walk, fw-0999.json, fw-09991c1.json). The lane
scripts are the predecessor's lane A (days + fresh_walk at the end) and lane B (career .. fixtap_click, p926 at the end),
plus a perf script that waits for both "LANE ... DONE" lines.

## Gotchas
- Container restarted once mid-perf (~01:30 UTC): files in /tmp survived, background tasks died. Recheck sha256s, rerun
  only what was cut off, tell BM + lead.
- fresh_walk: compare with the last record key by key, find the first differing entry per key, and read the window around
  any stuck minute (Day = minute // 1440 + 1). The drill now goes: 15:00 tap Calder, talk, 15:01 arrow "On the muster line
  till the all-clear, 15:15", held to 15:15.
- Killing a waiting perf script with pkill -f on its script path is safe (it doesn't match the lane scripts).

## Loose ends
None. 0.99.91 published (~14:49 UTC Nov 11; main = claude/integration = cdd9efd, game b321a4ec...95f3). OLD for the next round = 0.99.91 cdd9efd unless the lead says otherwise. Stood down on BM28's word.
