# Checks R3: 0.99.1 full round (row R3 of plans/round-0990.md on claude/lead-46, BM21: same share)

- Build: claude/staging-0991 at f77c26d9525395a290e2b902fedcbf09f4849364, `starship-cadet.html` sha256
  8e4ac5459ca78df284390d9438c09b7118ce5448d4c0093dbf9b894bf19e2d9d (matches BM21's). The title screen now starts asleep (the first press only wakes it).
- OLD: 0.99.0, 6d5684ba, game sha256 041a699c...4ee2 (matches). Not needed: no FAILs.
- Runner: R3 (DM2), checks from the candidate's own checkout (a worktree at f77c26d9), CADET_CHROME=/opt/pw-browsers/chromium,
  lane A CADET_WORK /tmp/work-r3 (the controller groups one at a time, G3 first so G1's walk runs after lane B), lane B
  /tmp/work-r3b, two browsers at most, each check under a 90 min timeout. The controller groups were checked against the
  candidate's own part list (ALL_PARTS and the parts added after it): all covered but reach.
- Notes on claude/devmode-j2 (this session pushes only there), not a checks branch.

| Check | Result | Key lines |
|---|---|---|
| devmode_check (all parts) | OK, exit 0 (1821 s) | DEVMODE CHECK OK |
| sound_check | OK, exit 0 (1053 s) | SOUND CHECK OK |
| dev_arrow_check | OK, exit 0 (379 s) | DEV ARROW CHECK OK |
| promo_sight_check | OK, exit 0 (38 s) | PROMO SIGHT CHECK OK |
| arrows_d_check | OK, exit 0 (133 s) | arrows_d_check: OK |
| arrows_f_check | OK, exit 0 (71 s) | arrows_f_check: OK |
| ending_check | OK, exit 0 (258 s) | ENDING CHECK OK |
| controller G3: m19 m20 s5cases s6cases vessel ending m21 m24 team m23 deck6 promo4 promo3 | OK, exit 0 (3587 s) | all 13 OK |
| controller G4: nights mentor props jobs2 beam court | OK, exit 0 (463 s) | all 6 OK |
| controller G2: shut off quiet base deck pick1 panels api lists tiles disc screens marks touch3 drop settings a11y firstuse cards clock devpad edge savesland sound saves words | OK, exit 0 (2404 s) | all 26 OK |
| controller G1: idle save calls touch walk pick lift door day games unplug odd | OK, exit 0 (1970 s) | all 12 OK; day's bedtime: the ring offered "Bunk", the alarm card shown, Set alarm by pad ok |

controller_check: 57 parts (every part but reach), every one OK, no FAIL lines.

## FAILs

None.
