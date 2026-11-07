# Checks R3: round 0999, 0.99.9 (same share as round 0998; BM27 for lead 51)

- Build: claude/staging-0999 at 8d8073a9, `starship-cadet.html` sha256
  583d99ba12d299a70cb431ca41dfa2cdb86a3a03e12e646cbf0e861aa741bd16 (matches the GO), build 0.99.9.
- OLD: 0.99.8, main 33c737b, game sha256 13681748513f9b7cb51fc299c4789085d0636829d8297b9f0d29d00683259fd3 (matches).
- Check files from 8d8073a9, byte-identical to round 0998b's. 57 controller parts (every part but reach).
- Runner: R3, the candidate's own checkout (a worktree), CADET_CHROME=/opt/pw-browsers/chromium, CADET_WORK /tmp/work-r3
  and /tmp/work-r3b, two browsers at most, 90 min timeout each. sound_check first and alone, then two lanes.
- My container restarted mid-round (~05:15 UTC): the seven finished results were kept; controller G3 and G4 (mid-run)
  and G2, G1 (not started) were lost and all four re-run from the start. The three sound proof runs went to R2 (agreed,
  lead 51's idea, BM27 copied; R1 and R6 also offered and were told no, so nothing ran twice).

| Check | Result | Key lines |
|---|---|---|
| sound_check (alone) | FAIL, exit 1 (583 s) | one line: `FAIL hide: hidden while a resume is on its way, the sound ends stopped (running)`; every other part OK |
| devmode_check (all parts) | OK, exit 0 (988 s) | DEVMODE CHECK OK |
| dev_arrow_check | OK, exit 0 (207 s) | DEV ARROW CHECK OK |
| promo_sight_check | OK, exit 0 (23 s) | PROMO SIGHT CHECK OK |
| arrows_d_check | OK, exit 0 (80 s) | arrows_d_check: OK |
| arrows_f_check | OK, exit 0 (37 s) | arrows_f_check: OK |
| ending_check | OK, exit 0 (134 s) | ENDING CHECK OK |
| controller G4: nights mentor props jobs2 beam court (after the restart) | OK, exit 0 (387 s) | all 6 OK |
| controller G3: m19 m20 s5cases s6cases vessel ending m21 m24 team m23 deck6 promo4 promo3 (after the restart) | OK, exit 0 (2228 s) | all 13 OK |
| controller G1: idle save calls touch walk pick lift door day games unplug odd (after the restart) | OK, exit 0 (1965 s) | all 12 OK |
| controller G2: shut off quiet base deck pick1 panels api lists tiles disc screens marks touch3 drop settings a11y firstuse cards clock devpad edge savesland sound saves words (after the restart) | OK, exit 0 (1524 s) | all 26 OK |

controller_check: 57 of 57 parts OK.

## The one FAIL: sound_check "hide while resuming", a one-off timing race in the check

- The part hides the page while the audio's resume is still on its way and expects it to end stopped ("suspended"); this
  run it ended "running". The other hide cases (visibilitychange, pagehide, freeze) all ended suspended.
- 0.99.9's game diff vs 0.99.8 is 15 lines with nothing on sound, audio, visibility or resume (BM27 checked the same).
- Proof runs by R2, each alone on its own machine:
  - OLD 0.99.8: exit 1, SOUND CHECK FAILED, `hide while resuming: suspended` (hide passed); its FAIL was a different
    timing line: `live: after a stall the band plays nothing late, and plays on ([0, 14, 0, 0], ['jam', 8, 1])`.
  - candidate run 1: exit 0, SOUND CHECK OK, `hide while resuming: suspended`.
  - candidate run 2: exit 0, SOUND CHECK OK, `hide while resuming: suspended`.
- So: not repeated on the candidate in two alone runs, and OLD fails a different timing line once. One-off timing races
  in sound_check (hide-while-resuming and live-after-stall), not the build. BM27 to add a backlog row for the sound seat,
  next to BM24-1.

**R3: OK.** Every check OK except one first-run sound_check line, a check-side timing race (proof above).
