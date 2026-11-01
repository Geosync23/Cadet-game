# Checks R3: 0.99.6 full round (row R3 of plans/round-0996.md, BM24 for lead 49)

- Build: claude/staging-0996, GO from lead 49 at f3dbd11 and from BM24 at b97cb98 (game commit 5ac6864; the commits after
  it are docs only: f3dbd11 to b97cb98 changes only plans/round-0996.md). `starship-cadet.html` sha256
  f6ff5ec1e4b55c44425d046765d30c8f1173464cad9327913372b579c57db8a8 (matches the GO), build 0.99.6.
- OLD: 0.99.5, claude/integration 6475bb30, game sha256 93aed54fa9296e75c308ae199cbac32465c776c650161fe41bf22535839a5164 (matches).
- Runner: R3, checks from the candidate's own checkout (a worktree), CADET_CHROME=/opt/pw-browsers/chromium, three r128
  and acorn 8.12.1 by npm pack. Lane A CADET_WORK /tmp/work-r3 (controller groups one at a time), lane B /tmp/work-r3b;
  two browsers at most, each run under a 90 min timeout.
- All eight checks in this share are byte-identical to OLD's. controller_check has the same 57 parts as in 0.99.5, so
  the four groups are the same and cover every part but reach.

| Check | Result | Key lines |
|---|---|---|
| devmode_check (all parts) | OK, exit 0 (982 s) | DEVMODE CHECK OK (no "real" flake) |
| sound_check (first run, beside controller G3) | FAIL, exit 1 (702 s) | FAIL long: switched on, (almost) nothing starts or moves late after a stall ... ([0, 0, 49, 0], ['Porthole', True, 1]) |
| dev_arrow_check | OK, exit 0 (201 s) | DEV ARROW CHECK OK |
| promo_sight_check | OK, exit 0 (24 s) | PROMO SIGHT CHECK OK |
| arrows_d_check | OK, exit 0 (82 s) | arrows_d_check: OK |
| arrows_f_check | OK, exit 0 (39 s) | arrows_f_check: OK |
| ending_check | OK, exit 0 (143 s) | ENDING CHECK OK |
| controller G3: m19 m20 s5cases s6cases vessel ending m21 m24 team m23 deck6 promo4 promo3 | OK, exit 0 (1926 s) | all 13 OK |
| controller G2: shut off quiet base deck pick1 panels api lists tiles disc screens marks touch3 drop settings a11y firstuse cards clock devpad edge savesland sound saves words | OK, exit 0 (2011 s) | all 26 OK |
| controller G1: idle save calls touch walk pick lift door day games unplug odd | OK, exit 0 (1202 s) | all 12 OK |
| controller G4: nights mentor props jobs2 beam court | OK, exit 0 (232 s) | all 6 OK |
| sound_check on OLD (beside controller G2) | OK, exit 0 (723 s) | long on: [0, 0, 0, 0] |
| sound_check on the candidate again (beside controller G2) | OK, exit 0 (790 s) | long on: [0, 0, 0, 0] |
| sound_check on the candidate, alone (1) | OK, exit 0 (487 s) | long on: [0, 0, 0, 0] |
| sound_check on the candidate, alone (2) | OK, exit 0 (502 s) | long on: [0, 0, 0, 0] |

controller_check: 57 parts (every part but reach), every one OK, no FAIL lines.

## The one FAIL: sound_check "long", a one-off timing flake

- What the part does: on a copy with SND_LONG switched on, it holds the page busy for 1.2 s of audio time four times and
  counts sounds started or moved in the past after each. The first run gave [0, 0, 49, 0]: the third stall alone had 49.
- It ran beside controller_check (a second browser), so the machine was loaded.
- The game diff from OLD to the candidate (75 lines) has no sound or audio line; BM24 read the whole diff and found
  nothing that touches sound or the main loop with the picture switches off.
- Every later run passed: OLD once, the candidate again beside controller once, and the candidate alone twice (as BM24
  and lead 49 asked), each [0, 0, 0, 0].
- So: a timing flake under load, not a change in 0.99.6. It has no backlog row yet; the build master may want one (the
  "long" part is sensitive to a busy machine, like devmode's "real" and player's Saving).

**R3: OK.** One first-run FAIL in sound_check "long", not repeated in four runs (two alone); not a 0.99.6 change.
