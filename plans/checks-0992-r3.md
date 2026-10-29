# Checks R3: 0.99.2 full round (row R3 of plans/round-0990.md on claude/lead-46, BM21: same share)

- Build: claude/staging-0992 at 60d477e8619a373f8d7e6b27a59236f64d5d2427, `starship-cadet.html` sha256
  27d605e72510827101552b3bd3e29197f800669b644a7101775729defd5e3920 (matches BM21's). Changes: title music C's melody sooner; New game keeps the terminal up until the signing screen.
- OLD: 0.99.1, bc4579aa, game sha256 8e4ac545...2d9d (matches). Not needed: no FAILs.
- Runner: R3 (DM2), checks from the candidate's own checkout (a worktree at 60d477e8), CADET_CHROME=/opt/pw-browsers/chromium,
  lane A CADET_WORK /tmp/work-r3 (the controller groups one at a time, G3 first so G1's walk runs after lane B), lane B
  /tmp/work-r3b, two browsers at most, each check under a 90 min timeout. The controller groups were checked against the
  candidate's own part list (ALL_PARTS and the parts added after it): all covered but reach.
- Notes on claude/devmode-j2 (this session pushes only there), not a checks branch.

| Check | Result | Key lines |
|---|---|---|
| devmode_check (all parts) | OK, exit 0 (1181 s) | DEVMODE CHECK OK |
| sound_check | OK, exit 0 (667 s) | SOUND CHECK OK |
| dev_arrow_check | OK, exit 0 (246 s) | DEV ARROW CHECK OK |
| promo_sight_check | OK, exit 0 (27 s) | PROMO SIGHT CHECK OK |
| arrows_d_check | OK, exit 0 (102 s) | arrows_d_check: OK |
| arrows_f_check | OK, exit 0 (48 s) | arrows_f_check: OK |
| ending_check | OK, exit 0 (185 s) | ENDING CHECK OK |
| controller G3: m19 m20 s5cases s6cases vessel ending m21 m24 team m23 deck6 promo4 promo3 | OK, exit 0 (2249 s) | all 13 OK |
| controller G4: nights mentor props jobs2 beam court | OK, exit 0 (345 s) | all 6 OK |
| controller G2: shut off quiet base deck pick1 panels api lists tiles disc screens marks touch3 drop settings a11y firstuse cards clock devpad edge savesland sound saves words | OK, exit 0 (1514 s) | all 26 OK |
| controller G1: idle save calls touch walk pick lift door day games unplug odd | OK, exit 0 (1315 s) | all 12 OK; day's bedtime: the ring offered "Bunk", the alarm card shown, Set alarm by pad ok |

controller_check: 57 parts (every part but reach), every one OK, no FAIL lines.

## FAILs

None.
