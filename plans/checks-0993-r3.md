# Checks R3: 0.99.3 full round (row R3 of plans/round-0990.md on claude/lead-46, BM21: same share)

- Build: claude/staging-0993 at df74ce0fbf33f40bb2cee71369ef589871a1eb94, `starship-cadet.html` sha256
  04c821fe5619c9709f233be195c6cd5590c73d3caf81a106fc77bc1083a4c2a9 (matches BM21's). Changes: the mess hall sound and the original title song back; the Day 0 dinner's Chief on the cards and the call-home card after you eat.
- OLD: 0.99.2, d180a704, game sha256 27d605e7...3920 (matches). Not needed: no FAILs.
- Runner: R3 (DM2), checks from the candidate's own checkout (a worktree at df74ce0f), CADET_CHROME=/opt/pw-browsers/chromium,
  lane A CADET_WORK /tmp/work-r3 (the controller groups one at a time, G3 first so G1's walk runs after lane B), lane B
  /tmp/work-r3b, two browsers at most, each check under a 90 min timeout. The controller groups were checked against the
  candidate's own part list (ALL_PARTS and the parts added after it): all covered but reach.
- Notes on claude/devmode-j2 (this session pushes only there), not a checks branch.

| Check | Result | Key lines |
|---|---|---|
| devmode_check (all parts) | OK, exit 0 (1354 s) | DEVMODE CHECK OK |
| sound_check | OK, exit 0 (827 s) | SOUND CHECK OK |
| dev_arrow_check | OK, exit 0 (302 s) | DEV ARROW CHECK OK |
| promo_sight_check | OK, exit 0 (32 s) | PROMO SIGHT CHECK OK |
| arrows_d_check | OK, exit 0 (111 s) | arrows_d_check: OK |
| arrows_f_check | OK, exit 0 (60 s) | arrows_f_check: OK |
| ending_check | OK, exit 0 (220 s) | ENDING CHECK OK |
| controller G3: m19 m20 s5cases s6cases vessel ending m21 m24 team m23 deck6 promo4 promo3 | OK, exit 0 (2937 s) | all 13 OK |
| controller G4: nights mentor props jobs2 beam court | OK, exit 0 (334 s) | all 6 OK |
| controller G2: shut off quiet base deck pick1 panels api lists tiles disc screens marks touch3 drop settings a11y firstuse cards clock devpad edge savesland sound saves words | OK, exit 0 (2086 s) | all 26 OK |
| controller G1: idle save calls touch walk pick lift door day games unplug odd | OK, exit 0 (1803 s) | all 12 OK; day's bedtime: the ring offered "Bunk", the alarm card shown, Set alarm by pad ok |

controller_check: 57 parts (every part but reach), every one OK, no FAIL lines.

## FAILs

None.
