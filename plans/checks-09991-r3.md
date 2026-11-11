# Checks R3: round 09991, 0.99.91 (same share as round 0999; BM28 for lead 51)

- Build: claude/staging-09991 at 4d8869ec, `starship-cadet.html` sha256
  475bac8605fe9e26d2cd6035bcbd924dff315bac7eecdd39be12ff287f5b453e (matches the GO), build 0.99.91.
- OLD: 0.99.9, main bfbcbdf, game sha256 583d99ba12d299a70cb431ca41dfa2cdb86a3a03e12e646cbf0e861aa741bd16 (matches).
- Check files from 4d8869ec, byte-identical to OLD's. 57 controller parts (every part but reach).
- Runner: R3, the candidate's own checkout (a worktree), CADET_CHROME=/opt/pw-browsers/chromium, CADET_WORK /tmp/work-r3
  and /tmp/work-r3b, two browsers at most, 90 min timeout each. sound_check first and alone, then two lanes.

| Check | Result | Key lines |
|---|---|---|
| sound_check (alone) | OK, exit 0 (560 s) | SOUND CHECK OK |
| devmode_check (all parts) | OK, exit 0 (1007 s) | DEVMODE CHECK OK |
| dev_arrow_check | OK, exit 0 (218 s) | DEV ARROW CHECK OK |
| promo_sight_check | OK, exit 0 (26 s) | PROMO SIGHT CHECK OK |
| arrows_d_check | **FAIL**, exit 1 (87 s) | `FAIL drill: the 14:50 arrow is up (None; ['Day 3, Wednesday 14:51', False, None])` |
| arrows_f_check | OK, exit 0 (38 s) | arrows_f_check: OK |
| ending_check | OK, exit 0 (143 s) | ENDING CHECK OK |
| controller G3: m19 m20 s5cases s6cases vessel ending m21 m24 team m23 deck6 promo4 promo3 | OK, exit 0 (1895 s) | all 13 OK |
| controller G4: nights mentor props jobs2 beam court | OK, exit 0 (351 s) | all 6 OK |
| controller G1: idle save calls touch walk pick lift door day games unplug odd | OK, exit 0 (1886 s) | all 12 OK |
| controller G2: shut off quiet base deck pick1 panels api lists tiles disc screens marks touch3 drop settings a11y firstuse cards clock devpad edge savesland sound saves words | OK, exit 0 (2089 s) | all 26 OK |
| arrows_d_check on OLD 0.99.9 (proof) | OK, exit 0 (84 s) | arrows_d_check: OK |
| arrows_d_check on the candidate with only TB9991_DRILL_ON false (proof) | OK, exit 0 (85 s) | arrows_d_check: OK |

controller_check: 57 of 57 parts OK.

## The one FAIL: arrows_d "the drill arrow", NEW, from piece C (TB9991_DRILL_ON) alone

- On Day 3, Wednesday 14:51, the check expects the drill's 14:50 arrow ("Fire drill, 15:00" on 0.99.9) and finds none.
  Every other arrows_d part passes.
- Passes on OLD and on the candidate with only TB9991_DRILL_ON false, so it's piece C alone.
- TB7 confirmed: the new drill's arrow only went through the arrow queue (guideAsk); arrows_d runs with the queue off,
  so there was no direct arrow at 14:50. TB7 is fixing it on claude/p9991-drills (switch-gated: a direct arrow at
  14:50 to the muster line, onto Calder at 15:00). To re-run arrows_d on the fixed candidate.

**R3: FAIL** (one NEW: arrows_d drill, piece C, owner TB7, fix in progress). Everything else OK.
