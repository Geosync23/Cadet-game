# Checks R3: 0.94.0 full round (old CR5 + CR6 shares)

- Build: claude/staging-0.94.0 at 9faaee80, `starship-cadet.html` sha256 04cc0cb65f2272c8f7afbeb438b94d972d80a8f59d42580515b86a1a380e0dbf (matches).
- OLD: 0.93.3 (19400976), game ec93b94d...d085.
- Step 5, the Veyli vessel, the ending and talk-only-when-close are on in this build.
- Runner: R3, CADET_WORK /tmp/work-R3 (+ R3B, R3C), CADET_CHROME=/opt/pw-browsers/chromium, at most two browsers at once (except the four short career --s5 splits, see mech_check).

| Check | Result | Key lines |
|---|---|---|
| interactions_check | OK, exit 0 (3495 s) | INTERACTIONS CHECK OK |
| career_check (9faaee80's check) | exit 1 | FAIL busy: "Relied on" before Day 5 (known old, backlog 12); FAIL s5: a steady Senior is "Trusted" by Day 21 (52 reliable); FAIL s5: ... by the end of Day 19 (54 reliable) |
| career_check (70628b5d's check, W6's fix; same game) | known old only, exit 1 | FAIL busy: "Relied on" before Day 5 (backlog 12) only; steady D19-D21 60 trusted |
| check_fast.sh | OK, exit 0 (264 s) | words, names, deck, device, machine, leave OK; QUICK CHECK OK in 264 s |
| mech_check | exit 1 (twice: 918 s, 876 s; same FAILs) | FAIL t3: never trained / the training's steps [] / the teacher's job, then yours / stage -1 once trained; FAIL ps: in person, Calder says it, then the Mail as the record ... ([None, None, 0, [], '{"mode":"follow","to":null}']) |
| disc_check | OK, exit 0 (520 s) | ALL OK |
| tiles_check | OK, exit 0 (165 s) | ALL OK |
| join_check | OK, exit 0 (406 s) | JOIN CHECK OK |
| food_check 1 7 | OK, exit 0 | FOOD CHECK OK |
| food_check 11 4 | OK, exit 0 | FOOD CHECK OK |
| clothes_check | OK, exit 0 | ALL OK |
| stories_check | OK, exit 0 | STORIES CHECK OK |
| promo_beats_check | OK, exit 0 | PROMO BEATS CHECK OK |
| ending_check (9faaee80's check) | exit 1, the check | FAIL the switch line is not in the build (it looked for the off line; 0.94.0 has `const EV_ENDING_ON = true;`), so the off parts saw it on |
| ending_check (f4914555's check) | OK (run by R1, by agreement) | rc 0 in 143 s, ENDING CHECK OK, 0 FAIL lines |

## FAILs and proof

- **career s5** (new; OLD has no P5_STEP5, so no OLD comparison). Splits with `--s5`, steady run D19 / D20 / D21:
  vessel + ending off 54 / 52 / 52 (FAIL); d69473b7, before talk-close 54 / 52 / 52 (FAIL); c3d36cde, B5's tip with P5_STEP5 true 58 / 58 / 58 (OK);
  64a1ba76, combined staging with P5_STEP5 true 54 / 52 / 52 (FAIL). W6 found the cause in the M19 merge (0b06cca5): the check's
  paper player gave no answer at M19's battery-cell pick, held the job and dropped it. A fix to the check only (70628b5d); with it, only backlog 12 is left.
- **ending_check**: the check, not the game. Fixed in the check at f4914555 (BM19); R1's run of that check is OK.
- **mech_check t3** (4 lines): the check exempted only t2, the test job, not t3. Fixed in the check (W6, mech_check skips t3 like t2; staging 68151ff8).
- **mech_check ps**: open. Same in both of my runs, so it isn't load. W6 found it passes run alone ("t3 ps") but fails in the whole run (an earlier part leaves state behind). W6 is checking it on d69473b7. OLD has no ps (Step 5).
