# 0.99.7 full round: R6's share (interactions_check whole)

- Candidate: claude/staging-0997 7fd8f6b (build turn 363107d; later commits docs only), build 0.99.7, GO from BM25; BM26 build master from ~13:00 UTC, lead 50 from ~13:40 UTC.
- Game sha256: b14421f82e04602cd608505756ddb8fb05bea4571af813d8e345424ebcd1cf7d (matches the GO).
- OLD: d7ad4c58 (claude/integration = main, 0.99.6), game sha256 f6ff5ec1...db8a8 (checked).
- Setup: CADET_WORK=/tmp/work-r6, CADET_CHROME=/opt/pw-browsers/chromium, three r128 and acorn via npm pack; two browsers at most.

| Check | Result | Key lines |
|---|---|---|
| interactions_check (whole), candidate | FAILED, exit 1, 13:00-13:37 UTC | two FAILs below; draw-call peak while doing things 220 (as 0.99.6) |
| the same check on OLD d7ad4c58 | OK, exit 0, 13:42-14:42 UTC | `INTERACTIONS CHECK OK` |

## The FAILs (both NEW: neither shows on OLD)

1. `FAIL the Orange tree tapped off the pin is the garden, not the vent (None)` (FB1 block, interactions_check.py ~892-980).
   - Cause: at the block's clock (Day 4 13:10) the tap shows "In use: Elif Yoon is there. Eleven oranges this year...",
     so nothing starts. On OLD nobody is at the tree and the tap starts ixGarden. Normal play, so check-side (lead 50).
   - Piece: EV1's EV997_LIGHT_ON (the first Thursday's Last Light lead-up closes the bow lounge, so Elif goes to the tree).
     JB3 found it first; confirmed here with a one-block probe on the candidate with one piece's switches turned back off:
     all-off PASS, JB3-off FAIL, CH1-off FAIL, EV1-off PASS (search stopped there, as agreed). Candidate: FAIL 3 of 3 runs.
   - Owner: EV1 (fixing; lead 50 / BM26).
2. `FAIL the briefing, the Chief's office, the booths and the store on the Schedule with a goal, only during the intro`: the store
   is missing. By design: CL1's note 15 (the crew store isn't a tradition). Check updated by CL1 in claude/p997-calendar adf96c5;
   CL1 reports that part passes on candidate 3a98019 with the updated check.

## BM26's question: the camera-turn swap (Orange tree vs Salad bed on the vent's line) with every switch off

Noise, not a switch-off difference. The FB1 probe run twice on OLD itself gives different rows: OLD run 1 garden turns
[Orange, Orange, Salad, Salad], OLD run 2 [Salad, Orange, Salad, Salad]; the things under the pin differ between the two OLD
runs too (Washer 2, Salad bed, the Senior Watch Officer's bed come and go). The all-off copy varies the same way. No '-'
(pin not drawn) rows in any run: always 60 taps, so the skipped-#rot idea doesn't apply. In every run all four turns still
clean the vent (ixStop), which is what the test asks.

Probe: plans' FB1 block lifted unchanged into fb1_probe.py (lines 1-58 + 892-980 of interactions_check.py), plus a print of
the toast and job after the off-pin tap. Logs kept in /tmp/r6logs on R6's machine.

R6: FAIL (both NEW, both owned: EV1 fixing the Orange tree; the store is by design with CL1's check update). Re-run on the
next candidate when BM26 sends it.
