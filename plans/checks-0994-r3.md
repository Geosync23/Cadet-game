# Checks R3: 0.99.4 full round (row R3 of plans/round-0994.md on claude/lead-47, BM22)

- Build: claude/staging-0994 at 8976965effdbff3473a85f31b4deb7c7f3a4a669, `starship-cadet.html` sha256
  a01d1a4c7864801b19541d70b9358089fba1ed84cee5145ca85931ea3012bc4a (matches BM22's GO). Changes: 0.99.3 + ST1's crew
  stories stage 2 switched on (STORIES2_ON = true).
- OLD: 0.99.3, claude/integration 57eceec4, game sha256 04c821fe5619c9709f233be195c6cd5590c73d3caf81a106fc77bc1083a4c2a9 (matches).
- Runner: R3, checks from the candidate's own checkout (a worktree at 8976965e), CADET_CHROME=/opt/pw-browsers/chromium,
  lane A CADET_WORK /tmp/work-r3 (controller groups one at a time), lane B /tmp/work-r3b, two browsers at most, each
  check under a 90 min timeout. All eight check scripts in this share are byte-identical to OLD's, so the controller
  groups cover the same 57 parts as last round (every part but reach).
- Controller G1 was handed to R4 (R4 finished early and offered; agreed before either started it, lead and BM22 copied).

| Check | Result | Key lines |
|---|---|---|
| devmode_check (all parts) | first run FAIL (1040 s); whole rerun OK, exit 0 (1146 s) | see "FAILs" below: a one-off, not reproduced |
| sound_check | OK, exit 0 (610 s) | SOUND CHECK OK |
| dev_arrow_check | OK, exit 0 (237 s) | DEV ARROW CHECK OK |
| promo_sight_check | OK, exit 0 (25 s) | PROMO SIGHT CHECK OK |
| arrows_d_check | OK, exit 0 (93 s) | arrows_d_check: OK |
| arrows_f_check | OK, exit 0 (45 s) | arrows_f_check: OK |
| ending_check | OK, exit 0 (161 s) | ENDING CHECK OK |
| controller G3: m19 m20 s5cases s6cases vessel ending m21 m24 team m23 deck6 promo4 promo3 | OK, exit 0 (2066 s) | all 13 OK |
| controller G4: nights mentor props jobs2 beam court | OK, exit 0 (370 s) | all 6 OK |
| controller G2: shut off quiet base deck pick1 panels api lists tiles disc screens marks touch3 drop settings a11y firstuse cards clock devpad edge savesland sound saves words | OK, exit 0 (1962 s) | all 26 OK |
| controller G1 (run by R4): idle save calls touch walk pick lift door day games unplug odd | PENDING | |

## FAILs

**devmode_check, first run only:** `FAIL real: #dev.debug (real arrived key True): the real game's keys or bytes changed
in a Dev session` (every other part passed). Judged a one-off timing flake, not new and not from the stories:
- Reruns with a copy of the check that prints which real key and which save fields differ: `off real` on the
  candidate 2/2 OK and on OLD 2/2 OK; the whole devmode_check on the candidate OK. Nothing differed in any rerun.
- RV28 (reviewer of stage 2): the stage 2 diff has no storage writes (no localStorage, setItem or saveGame); its state
  rides inside the normal save, which is the -dev key in Dev mode. RV28 ran `off real` on 8976965e 4/4 OK, and OK on
  0.99.3. The game's only saves outside the check's own calls are on visibilitychange and pagehide, so the likely cause
  is the real page's pagehide save landing late on a busy host (controller_check was running beside it).
- Not on the known-old list; reported to BM22 and the lead at once, with the reruns.
