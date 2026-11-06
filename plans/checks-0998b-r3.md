# Checks R3: round 0998b, 0.99.8 candidate 2 (P fixed; BM27 for lead 50)

- Build: claude/staging-0998 at bbb7bb0, `starship-cadet.html` sha256
  13681748513f9b7cb51fc299c4789085d0636829d8297b9f0d29d00683259fd3 (matches the GO), build 0.99.8.
- OLD: 0.99.6, claude/integration d7ad4c58, game sha256 f6ff5ec1e4b55c44425d046765d30c8f1173464cad9327913372b579c57db8a8 (ready; not needed, no FAIL).
- Check files from bbb7bb0, byte-identical to round 0998's. 57 controller parts (every part but reach).
- Runner: R3, the candidate's own checkout (a worktree), CADET_CHROME=/opt/pw-browsers/chromium, CADET_WORK /tmp/work-r3
  and /tmp/work-r3b, two browsers at most, 90 min timeout each. sound_check first and alone (backlog BM24-1), then two lanes.

| Check | Result | Key lines |
|---|---|---|
| sound_check (alone) | OK, exit 0 (544 s) | SOUND CHECK OK |
| devmode_check (all parts) | OK, exit 0 (959 s) | DEVMODE CHECK OK |
| dev_arrow_check | OK, exit 0 (209 s) | DEV ARROW CHECK OK |
| promo_sight_check | OK, exit 0 (24 s) | PROMO SIGHT CHECK OK |
| arrows_d_check | OK, exit 0 (82 s) | arrows_d_check: OK |
| arrows_f_check | OK, exit 0 (36 s) | arrows_f_check: OK |
| ending_check | OK, exit 0 (141 s) | ENDING CHECK OK |
| controller G3: m19 m20 s5cases s6cases vessel ending m21 m24 team m23 deck6 promo4 promo3 | OK, exit 0 (1804 s) | all 13 OK |
| controller G4: nights mentor props jobs2 beam court | OK, exit 0 (339 s) | all 6 OK |
| controller G1: idle save calls touch walk pick lift door day games unplug odd | OK, exit 0 (1805 s) | all 12 OK |
| controller G2: shut off quiet base deck pick1 panels api lists tiles disc screens marks touch3 drop settings a11y firstuse cards clock devpad edge savesland sound saves words | OK, exit 0 (1945 s) | all 26 OK |

controller_check: 57 of 57 parts OK, no FAIL lines anywhere in the share.

**R3: OK.** No FAILs.
