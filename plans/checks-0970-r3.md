# Checks R3: 0.97.0 full round (row R3 of plans/round-0970.md)

- Build: claude/staging-pad at b9b7e3d7bdee47016477770349c5bfa7e8fc84e1, `starship-cadet.html` sha256
  0bd1b5b69d640c7d2bd82032f2258e5be944f7905541dada62f9e4e9e615b36f (matches BM20's). The game differs from 0.96.0
  (fe11cd66) only in section 25 (Dev mode J0-J5, nothing without #dev) and the two build-number lines.
- OLD: 0.96.0, fe11cd66, game sha256 33292500...129e (matches). Not needed: no FAILs.
- Runner: R3 (DM2), checks from the candidate's own checkout (a worktree at b9b7e3d7), CADET_CHROME=/opt/pw-browsers/chromium,
  lane A CADET_WORK /tmp/work-r3 (the controller groups, one at a time), lane B /tmp/work-r3b, two browsers at most,
  each check under a 90 min timeout.

| Check | Result | Key lines |
|---|---|---|
| devmode_check (all parts) | OK, exit 0 (1060 s) | DEVMODE CHECK OK |
| sound_check | OK, exit 0 (517 s) | SOUND CHECK OK |
| dev_arrow_check | OK, exit 0 (232 s) | DEV ARROW CHECK OK |
| promo_sight_check | OK, exit 0 (22 s) | PROMO SIGHT CHECK OK |
| arrows_d_check | OK, exit 0 (90 s) | arrows_d_check: OK |
| arrows_f_check | OK, exit 0 (44 s) | arrows_f_check: OK |
| ending_check | OK, exit 0 (149 s) | ENDING CHECK OK |
| controller_check G1: idle save calls touch walk pick lift door day games unplug odd | OK, exit 0 (1830 s) | all 12 OK; CONTROLLER CHECK OK |
| controller_check G4: nights mentor props jobs2 beam court | OK, exit 0 (339 s) | all 6 OK; CONTROLLER CHECK OK |
| controller_check G3: m19 m20 s5cases s6cases vessel ending m21 m24 team m23 deck6 promo4 promo3 | OK, exit 0 (1319 s) | all 13 OK; CONTROLLER CHECK OK |
| controller_check G2: shut off quiet base deck pick1 panels api lists tiles disc screens marks touch3 drop settings a11y firstuse cards clock devpad edge savesland sound saves words | OK, exit 0 (1444 s) | all 26 OK; CONTROLLER CHECK OK |

controller_check: 57 parts (every part but reach, which BM20 runs), every one OK, no FAIL lines.

## FAILs

None.

## The first attempt (stopped; not a FAIL)

The first start ran two controller_check groups side by side (G1 and G2), as R3 did for 0.96.0. G1 stopped in part
walk on a Playwright timeout (clicking #rot "Rotate view": 30 s waiting for it to be visible and stable) after three of
its four views, and about 35 minutes in the container restarted (G2 had only reached its first part). Restarted with one
controller group at a time: G1 then passed whole, walk included, so the timeout was load. Logs of the first attempt
were kept locally, not committed.
