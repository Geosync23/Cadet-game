# Checks R3: 0.99.5 full round (row R3 of plans/round-0995.md, BM23 for lead 48)

- Build: claude/staging-0995 at e00bfabd8cefbfd66c5c71f2a22676c763a7eb8d, `starship-cadet.html` sha256
  93aed54fa9296e75c308ae199cbac32465c776c650161fe41bf22535839a5164 (matches BM23's GO; lead 48 confirmed this is the
  intended file, with RV30's tea fix; the earlier 5733867d... number was superseded).
- OLD: 0.99.4, claude/staging-0994 596712bc, game sha256 a01d1a4c7864801b19541d70b9358089fba1ed84cee5145ca85931ea3012bc4a (matches).
- Runner: R3, checks from the candidate's own checkout (a worktree at e00bfabd), CADET_CHROME=/opt/pw-browsers/chromium,
  lane A CADET_WORK /tmp/work-r3 (controller groups one at a time), lane B /tmp/work-r3b, two browsers at most, each
  check under a 90 min timeout.
- controller_check and sound_check changed since 0.99.4; the others in this share are byte-identical. controller_check's
  part list is unchanged (CT5's changes are inside deck and settings: turning right is now -pi/2 a push, the user's
  note 6), so the four groups cover the same 57 parts (every part but reach). sound_check runs its new parts (hide,
  mess_scale, long) by default.

| Check | Result | Key lines |
|---|---|---|
| devmode_check (all parts) | OK, exit 0 (1018 s) | DEVMODE CHECK OK (no "real" flake this time) |
| sound_check | OK, exit 0 (749 s) | SOUND CHECK OK; hide: visibilitychange, pagehide, freeze all suspended; mess_scale layers and the rush checked; long on |
| dev_arrow_check | OK, exit 0 (224 s) | DEV ARROW CHECK OK |
| promo_sight_check | OK, exit 0 (26 s) | PROMO SIGHT CHECK OK |
| arrows_d_check | OK, exit 0 (93 s) | arrows_d_check: OK |
| arrows_f_check | OK, exit 0 (46 s) | arrows_f_check: OK |
| ending_check | OK, exit 0 (158 s) | ENDING CHECK OK |
| controller G3: m19 m20 s5cases s6cases vessel ending m21 m24 team m23 deck6 promo4 promo3 | OK, exit 0 (1994 s) | all 13 OK (promo3 OK) |
| controller G4: nights mentor props jobs2 beam court | OK, exit 0 (364 s) | all 6 OK |
| controller G2: shut off quiet base deck pick1 panels api lists tiles disc screens marks touch3 drop settings a11y firstuse cards clock devpad edge savesland sound saves words | OK, exit 0 (1799 s) | all 26 OK |
| controller G1: idle save calls touch walk pick lift door day games unplug odd | OK, exit 0 (1224 s) | all 12 OK |

controller_check: 57 parts (every part but reach), every one OK, no FAIL lines.

**R3: OK.** No FAILs in this share.

## Extra runs for R1 (agreed with R1, BM23 and lead 48 copied; R1 took them off its own queue)

| Check | Build | Result | Key lines |
|---|---|---|---|
| arrows_check week | OLD 596712bc | OK, exit 0 (775 s) | ARROWS CHECK OK; stuck 0 every day, Days 2-8 |
| puzzle_check | OLD 596712bc | OK, exit 0 (147 s) | PUZZLE CHECK OK; cases posted 1; p5's first 3-pump-1 seal, slot 29, hidden True |

Both show R1's candidate FAILs in these checks do not happen on OLD (R1 and RV30 follow them up).
