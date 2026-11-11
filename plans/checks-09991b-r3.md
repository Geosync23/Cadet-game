# Checks R3: round 09991b, 0.99.91 candidate 2 (BM28 for lead 51)

- Build: claude/staging-09991 at 844f3c23, `starship-cadet.html` sha256
  b321a4ec9f15ac692f342b4339991a1c7d4011f9a083eaa3cde8b79fae7495f3 (matches the GO), build 0.99.91.
- OLD: 0.99.9, main bfbcbdf, game sha256 583d99ba12d299a70cb431ca41dfa2cdb86a3a03e12e646cbf0e861aa741bd16 (matches).
- Check files from 844f3c23, byte-identical to OLD's. 57 controller parts (every part but reach).
- Runner: R3, the candidate's own checkout (a worktree), CADET_CHROME=/opt/pw-browsers/chromium, CADET_WORK /tmp/work-r3
  and /tmp/work-r3b, two browsers at most, 90 min timeout each. sound_check first and alone, then two lanes.

| Check | Result | Key lines |
|---|---|---|
| sound_check (alone) | OK, exit 0 (573 s) | SOUND CHECK OK |
| devmode_check (all parts) | OK, exit 0 (1060 s) | DEVMODE CHECK OK |
| dev_arrow_check | OK, exit 0 (227 s) | DEV ARROW CHECK OK |
| promo_sight_check | OK, exit 0 (25 s) | PROMO SIGHT CHECK OK |
| arrows_d_check | OK, exit 0 (86 s) | arrows_d_check: OK; drill: "Fire drill, 15:00: Chief Calder at the Works bay" (round 09991's FAIL fixed) |
| arrows_f_check | OK, exit 0 (40 s) | arrows_f_check: OK |
| ending_check | OK, exit 0 (156 s) | ENDING CHECK OK |
| controller G3: m19 m20 s5cases s6cases vessel ending m21 m24 team m23 deck6 promo4 promo3 | OK, exit 0 (1964 s) | all 13 OK |
| controller G4: nights mentor props jobs2 beam court | OK, exit 0 (384 s) | all 6 OK |
| controller G1: idle save calls touch walk pick lift door day games unplug odd | OK, exit 0 (1997 s) | all 12 OK |
| controller G2 (first run): shut off quiet base deck pick1 panels api lists tiles disc screens marks touch3 drop settings a11y firstuse cards clock devpad edge savesland sound saves words | FAIL, exit 1 (2166 s) | 25 OK; `FAIL tiles: tiles: A on square 13 should put the tile down (a move made)` |
| controller tiles alone, candidate (x2) | OK, exit 0 (35 s, 34 s) | CONTROLLER CHECK OK |
| controller tiles alone, OLD | OK, exit 0 (33 s) | CONTROLLER CHECK OK |
| controller G2 again, candidate (alone) | OK, exit 0 (1410 s) | all 26 OK |

controller_check: 57 of 57 parts OK (G2 on its second run).

## The one FAIL: controller tiles "A on square 13", a one-off

- First G2 run only (beside controller G1 in the other lane). It passed alone twice on the candidate, once on OLD,
  and in the whole of G2 again on the candidate. 0.99.91's game diff vs 0.99.9 (333 lines) has nothing on tiles.
  A one-off timing miss in the check's tile press, not the build. Not repeated in four runs.

**R3: OK.** Every check OK; the one first-run controller tiles line did not repeat.
