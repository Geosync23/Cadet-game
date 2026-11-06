# Checks R3: round 0997b, 0.99.7 candidate 2 (row R3 of plans/round-0997.md, BM26 for lead 50)

- Build: claude/staging-0997 at c052cc8, `starship-cadet.html` sha256
  1b17203d4281afa28485d7ba05f5afe829931169888d392d97ef5e4f61a0bff9 (matches the GO), build 0.99.7.
- OLD: 0.99.6, d7ad4c58, game sha256 f6ff5ec1e4b55c44425d046765d30c8f1173464cad9327913372b579c57db8a8 (matches).
- Check files from c052cc8: controller_check with GM1's J (3966a4a) and SC1's I (f536097); devmode_check and
  arrows_d_check with CR1's fixes. controller_check has the same 57 parts (every part but reach).
- Runner: R3, the candidate's own checkout (a worktree), CADET_CHROME=/opt/pw-browsers/chromium, CADET_WORK /tmp/work-r3
  and /tmp/work-r3b, two browsers at most, 90 min timeout each. sound_check first and alone (backlog BM24-1), then two lanes.

| Check | Result | Key lines |
|---|---|---|
| sound_check (alone) | OK, exit 0 (571 s) | SOUND CHECK OK; long on [0,0,0,0]; live piano and jam: 4 stalls [0,0,0,0]; through a wall quieter |
| devmode_check (all parts) | OK, exit 0 (992 s) | DEVMODE CHECK OK (D closed: trad and the career table) |
| dev_arrow_check | OK, exit 0 (212 s) | DEV ARROW CHECK OK |
| promo_sight_check | OK, exit 0 (24 s) | PROMO SIGHT CHECK OK |
| arrows_d_check | OK, exit 0 (84 s) | arrows_d_check: OK (E closed) |
| arrows_f_check | OK, exit 0 (37 s) | arrows_f_check: OK |
| ending_check | OK, exit 0 (145 s) | ENDING CHECK OK |
| controller G3: m19 m20 s5cases s6cases vessel ending m21 m24 team m23 deck6 promo4 promo3 | OK, exit 0 (1846 s) | all 13 OK (ending OK: I closed) |
| controller G4: nights mentor props jobs2 beam court | OK, exit 0 (357 s) | all 6 OK |
| controller G1: idle save calls touch walk pick lift door day games unplug odd | OK, exit 0 (1874 s) | all 12 OK |
| controller G2: shut off quiet base deck pick1 panels api lists tiles disc screens marks touch3 drop settings a11y firstuse cards clock devpad edge savesland sound saves words | OK, exit 0 (2026 s) | all 26 OK (tiles OK: J closed) |

controller_check: 57 of 57 parts OK, no FAIL lines anywhere in the share.

**R3: OK.** No FAILs. The four from candidate 1 (devmode, arrows_d, controller ending, controller tiles) all pass.
