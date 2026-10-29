# Checks R3: 0.99.0 full round (row R3 of plans/round-0990.md on claude/lead-46)

- Build: claude/staging-099 at a4c9febe2264f02adf812602de5614a5f3130889, `starship-cadet.html` sha256
  041a699c00cb28607d97ef4f8add5594b47b6e204294f9b93aab7e82adad4ee2 (matches BM21's). Title screen on.
- OLD: 0.98.0, 37b858b4, game sha256 81c07a05...59b1 (matches). Not needed: no FAILs.
- Runner: R3 (DM2), checks from the candidate's own checkout (a worktree at a4c9febe), CADET_CHROME=/opt/pw-browsers/chromium,
  lane A CADET_WORK /tmp/work-r3 (the controller groups one at a time, G3 first so G1's walk runs after lane B), lane B
  /tmp/work-r3b, two browsers at most, each check under a 90 min timeout. The controller groups were checked against the
  candidate's own part list (ALL_PARTS and the parts added after it): all covered but reach.
- Notes on claude/devmode-j2 (this session pushes only there), not claude/checks-0990-r3.

| Check | Result | Key lines |
|---|---|---|
| devmode_check (all parts) | OK, exit 0 (1971 s) | DEVMODE CHECK OK |
| sound_check | OK, exit 0 (1158 s) | SOUND CHECK OK |
| dev_arrow_check | OK, exit 0 (418 s) | DEV ARROW CHECK OK |
| promo_sight_check | OK, exit 0 (47 s) | PROMO SIGHT CHECK OK |
| arrows_d_check | OK, exit 0 (162 s) | arrows_d_check: OK |
| arrows_f_check | OK, exit 0 (80 s) | arrows_f_check: OK |
| ending_check | OK, exit 0 (293 s) | ENDING CHECK OK |
| controller G3: m19 m20 s5cases s6cases vessel ending m21 m24 team m23 deck6 promo4 promo3 | OK, exit 0 (3927 s) | all 13 OK |
| controller G4: nights mentor props jobs2 beam court | OK, exit 0 (512 s) | all 6 OK |
| controller G2: shut off quiet base deck pick1 panels api lists tiles disc screens marks touch3 drop settings a11y firstuse cards clock devpad edge savesland sound saves words | OK, exit 0 (2653 s) | all 26 OK |
| controller G1: idle save calls touch walk pick lift door day games unplug odd | OK, exit 0 (2213 s) | all 12 OK; day's bedtime: the ring offered "Bunk", the alarm card shown, Set alarm by pad ok (the 0.98 FAIL, now fixed: PASS as required) |

controller_check: 57 parts (every part but reach), every one OK, no FAIL lines.

## FAILs

None.
