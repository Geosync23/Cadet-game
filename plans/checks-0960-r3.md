# Checks R3: 0.96.0 full round (row R3 of plans/round-0960.md)

- Build: claude/staging-pad at 6db1cdd2f7f47e76d4f46ba3f05843ec10900dd6, `starship-cadet.html` sha256
  c62d63999e6b596d21806d1cb14fa9ab3168a50c5038dfcc1c04f3163d37a74e (matches BM20's). PAD_ON and SND_R3_ON are true in it.
- OLD: 0.95.0, claude/integration b5199dc3, game sha256 b18d2b64...238a (matches). Not needed: no FAILs.
- Runner: R3, the candidate's own checks, CADET_WORK /tmp/work-r3 (lane A) and /tmp/work-r3b (lane B),
  CADET_CHROME=/opt/pw-browsers/chromium, two browsers at most (one per lane), each check under a 90 min timeout.
- Setup note: this container lacked Python's playwright; `pip install playwright` fixed it (no browser download).

| Check | Result | Key lines |
|---|---|---|
| sound_check | OK, exit 0 (388 s) | SOUND CHECK OK |
| promo_sight_check | OK, exit 0 (18 s) | PROMO SIGHT CHECK OK |
| arrows_d_check | OK, exit 0 (61 s) | arrows_d_check: OK |
| arrows_f_check | OK, exit 0 (32 s) | arrows_f_check: OK |
| ending_check | OK, exit 0 (121 s) | ENDING CHECK OK |
| controller_check G1: idle save calls touch walk pick lift door day games unplug odd | OK, exit 0 (1725 s) | all 12 OK; CONTROLLER CHECK OK |
| controller_check G2: shut off quiet base deck pick1 panels api lists tiles disc screens marks touch3 drop settings a11y firstuse cards clock devpad edge savesland sound saves words | OK, exit 0 (2314 s) | all 26 OK; CONTROLLER CHECK OK |
| controller_check G3: m19 m20 s5cases s6cases vessel ending m21 m24 team m23 deck6 promo4 promo3 | OK, exit 0 (1906 s) | all 13 OK; CONTROLLER CHECK OK |
| controller_check G4: nights mentor props jobs2 beam court | OK, exit 0 (357 s) | all 6 OK; CONTROLLER CHECK OK |

controller_check: 57 parts (all 58 in its list but reach, which BM20 runs), every one OK, no FAIL lines, no "not yet".

## FAILs

None.
