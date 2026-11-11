# 0.99.91 round 09991: runner R1

- NEW: `claude/staging-09991` 4d8869ec, game sha256 `475bac8605fe9e26d2cd6035bcbd924dff315bac7eecdd39be12ff287f5b453e`
  (matched BM28's GO), build 0.99.91 (0.99.9 + pieces A-D, all four switches on); check files at 4d8869ec.
- OLD: 0.99.9, main bfbcbdf, game 583d99ba...bd16 (matched).
- GO ~00:04 UTC 2026-11-11 (BM28 for lead 51). Two browsers (/tmp/work-r1, /tmp/work-r1-b, test copies cleared first);
  a third (/tmp/work-r1-c) only for the two FAIL proofs; player_check alone at the end.

| Check | Result | Key lines |
|---|---|---|
| p5retry_probe | OK | P5 RETRY PROBE OK (22s; off copy, P5_RETRY_ON false, 1 line) |
| bubble | OK | BUBBLE CHECK OK (446s) |
| puzzle | OK | PUZZLE CHECK OK (120s) |
| social | OK | SOCIAL CHECK OK (29s) |
| talk | OK | TALK CHECK OK (39s) |
| arrows_pointer | OK | arrows_pointer_check: OK (146s) |
| day_4 | OK | DAY CHECK OK (276s) |
| day_11 | OK | DAY CHECK OK (282s) |
| arrows_default | **FAIL** | `FAIL week: Day 3: "m3d" not learned by following the arrow (fix: FX2 (the drill)); training None, opened ['m4', 'm3d']` (1395s) |
| day_25 | OK | DAY CHECK OK (405s) |
| arrows_step5 | OK | ARROWS CHECK OK (392s) |
| day_26 | OK | DAY CHECK OK (439s) |
| arrows_step6 | OK | ARROWS CHECK OK (623s); asis 698/0/0, teachoff 697/0/0, track 697/0/0, skiptea 692/0/0 (due/missed/stuck) |
| day_2 | OK | DAY CHECK OK (438s) |
| day_9 | OK | DAY CHECK OK (442s) |
| arrows_endstay | OK | ARROWS CHECK OK (943s) |
| player | OK | PLAYER CHECK OK (292s, alone) |

## The FAIL: arrows_check week, Day 3 m3d: NEW (piece C)

- Every other part of arrows_check default (queue, clockin, shift, promo, vessel) passed; the only FAIL line is the one above.
- OLD 0.99.9, `arrows_check.py OLD week promo`: ARROWS CHECK OK; Day 3 learned ['m1', 'm3d', 'm4']. So not known old: NEW.
- Candidate with only TB9991_DRILL_ON false (1 line), `arrows_check.py COPY week`: ARROWS CHECK OK. So the cause is piece C alone.
- Cause (TB7, the piece's owner): with the drill as a tradition only a tap on Calder counts, but the drill arrow points at
  the muster-line place; a player who only follows the arrow taps a person only for a join arrow. TB7's fix (from 15:00 the
  arrow is on Calder as a join arrow) is coming on claude/p9991-drills; re-run arrows_check (default, or week) on the new candidate.
- Not a FAIL: the promo part's "(not the promotion) stuck from Day 12 18:20 at "A toilet"" is the same on OLD (which also
  has a 06:06 one at the circulation pumps).

**R1: FAIL on 0.99.91 candidate 4d8869ec (game 475bac86...b453e): arrows_check week Day 3 m3d, NEW, piece C (fix coming from TB7).
Every other check in the share passes.**
