# Checks R3: round 0998, 0.99.8 (row R3 of plans/round-0997.md with the "Round 0997b" changes; BM27 for lead 50)

- Build: claude/staging-0998 at d7f5bd6, `starship-cadet.html` sha256
  298291963584a62fbf0f7953afaa402924cdd22e474d526353494ec02d22c462 (matches the GO), build 0.99.8.
- OLD: 0.99.6, claude/integration d7ad4c58, game sha256 f6ff5ec1e4b55c44425d046765d30c8f1173464cad9327913372b579c57db8a8 (matches; not needed, no FAIL).
- Check files from d7f5bd6, byte-identical to round 0997b's (controller_check with GM1's J and SC1's I). 57 controller parts (every part but reach).
- Runner: R3, the candidate's own checkout (a worktree), CADET_CHROME=/opt/pw-browsers/chromium, CADET_WORK /tmp/work-r3
  and /tmp/work-r3b, two browsers at most, 90 min timeout each. sound_check first and alone (backlog BM24-1), then two lanes.

| Check | Result | Key lines |
|---|---|---|
| sound_check (alone) | OK, exit 0 (554 s) | SOUND CHECK OK; long on [0,0,0,0] |
| devmode_check (all parts) | OK, exit 0 (968 s) | DEVMODE CHECK OK |
| dev_arrow_check | OK, exit 0 (212 s) | DEV ARROW CHECK OK |
| promo_sight_check | OK, exit 0 (24 s) | PROMO SIGHT CHECK OK |
| arrows_d_check | OK, exit 0 (81 s) | arrows_d_check: OK |
| arrows_f_check | OK, exit 0 (37 s) | arrows_f_check: OK |
| ending_check | OK, exit 0 (141 s) | ENDING CHECK OK |
| controller G3: m19 m20 s5cases s6cases vessel ending m21 m24 team m23 deck6 promo4 promo3 | OK, exit 0 (1804 s) | all 13 OK |
| controller G4: nights mentor props jobs2 beam court | OK, exit 0 (342 s) | all 6 OK |
| controller G1: idle save calls touch walk pick lift door day games unplug odd | OK, exit 0 (1809 s) | all 12 OK |
| controller G2: shut off quiet base deck pick1 panels api lists tiles disc screens marks touch3 drop settings a11y firstuse cards clock devpad edge savesland sound saves words | OK, exit 0 (1950 s) | all 26 OK |

controller_check: 57 of 57 parts OK, no FAIL lines anywhere in the share.

**R3: OK.** No FAILs.
