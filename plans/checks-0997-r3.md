# Checks R3: 0.99.7 full round (row R3 of plans/round-0997.md, BM25 then BM26; lead 49 then lead 50)

- Build: claude/staging-0997 at 7fd8f6b (build turn 363107d; later commits docs only), `starship-cadet.html` sha256
  b14421f82e04602cd608505756ddb8fb05bea4571af813d8e345424ebcd1cf7d (matches the GO), build 0.99.7.
- OLD: 0.99.6, claude/integration = main d7ad4c58, game sha256 f6ff5ec1e4b55c44425d046765d30c8f1173464cad9327913372b579c57db8a8 (matches).
- Runner: R3, checks from the candidate's own checkout (a worktree), CADET_CHROME=/opt/pw-browsers/chromium, three r128
  and acorn 8.12.1 by npm pack, CADET_WORK /tmp/work-r3 and /tmp/work-r3b, two browsers at most, 90 min timeout each.
- sound_check ran first and alone (backlog BM24-1), then two lanes side by side. sound_check and promo_sight_check
  changed since OLD; the other six checks are byte-identical. controller_check has the same 57 parts (every part but reach).
- R4 took two OLD proof runs off my queue (agreed, BM26 and lead copied): devmode_check and arrows_d_check on OLD.

| Check | Result | Key lines |
|---|---|---|
| sound_check (alone) | OK, exit 0 (576 s) | SOUND CHECK OK; long on [0,0,0,0]; live piano and jam heard in the music room; live: 4 stalls [0,0,0,0] |
| devmode_check (all parts) | **FAIL**, exit 1 (1014 s) | 10 FAIL lines: trad (8 + stopped), set, career (below) |
| dev_arrow_check | OK, exit 0 (216 s) | DEV ARROW CHECK OK |
| promo_sight_check | OK, exit 0 (24 s) | PROMO SIGHT CHECK OK |
| arrows_d_check | **FAIL**, exit 1 (88 s) | S3 and pass-over (below) |
| arrows_f_check | OK, exit 0 (40 s) | arrows_f_check: OK |
| ending_check | OK, exit 0 (148 s) | ENDING CHECK OK |
| controller G3: m19 m20 s5cases s6cases vessel ending m21 m24 team m23 deck6 promo4 promo3 | **FAIL**, exit 1 (2192 s) | 12 OK; ending FAIL, 3 problems |
| controller G2: shut off quiet base deck pick1 panels api lists tiles disc screens marks touch3 drop settings a11y firstuse cards clock devpad edge savesland sound saves words | **FAIL**, exit 1 (2160 s) | 25 OK; tiles FAIL, 3 problems |
| controller G1: idle save calls touch walk pick lift door day games unplug odd | OK, exit 0 (1867 s) | all 12 OK |
| controller G4: nights mentor props jobs2 beam court | OK, exit 0 (405 s) | all 6 OK |

controller_check: 55 of 57 parts OK; ending and tiles FAIL.

## The FAILs: all four NEW (each passes on OLD)

1. **devmode_check** (OLD: OK, exit 0, run by R4). Three groups:
   - trad: `quiz soon / harvest tomorrow / founding usual / running tomorrow not started: {'refused': "Not on a big event's
     day (The Last Light): the ship's evening is the event's."}`, each with `only None going`, and `trad: stopped: 'd'`.
     The Last Light is new in 0.99.7 (EV1, notes 8/34). EV1 reports a fix in claude/p997-events ecc5236.
   - set: `the table and CAREER_LADDER disagree: ['t2: table 9, ladder 8']` (CR1 moved the first test to Day 8, note 55).
   - career: `Day 8 09:30 test needs (only the day missing): [True, True, True, True, True]` (same cause).
2. **arrows_d_check** (OLD: OK, exit 0, run by R4):
   - `FAIL S3: a round on the board counts as a job to take (the board's own rule) ({'lab': 'Your Tier 2 test, 09:00: the Works bay', 'L': ['arrows-round']})`
   - `FAIL pass-over: T3 (the pick) has nothing to show, the next live entry should ({'lab': 'Your Tier 2 test, 09:00: the Works bay', 't3': True, 'pick': 'promo:testday:9'})`
   - On the check's day the arrow now shows the Tier 2 test (CR1's Day 8 test). On OLD, S3 shows "Your Tier 2 test job (a
     lesson on the board)".
3. **controller_check ending** (OLD: `controller_check.py starship-cadet.html ending` OK, exit 0, 831 s), all Day 34 by pad:
   - `"About the transfer" on the Captain's chat card by pad: never highlighted (the ring said ATalk to Captain Odile Marrow◀ ▶)`
   - `Not sure by pad not kept ([])`
   - `no friend's "About the transfer" pressed by pad ([('pell', False, 'no chat card'), ('tomas', True, 'never highlighted'), ('kovac-zainab', False, 'no chat card'), ('bramwell-basil', True, 'not there'), ('halloran-emeka', True, 'never highlighted'), ('rina', True, 'never highlighted')])`
   - On OLD: "the button ok, choices [staying / taking the post / not sure / not yet], Not sure ok"; tomas "ok".
     Likely SC1's talk-option rework (note 17). Days 32, 35 and 36 by pad pass; ending_check (mouse) passes.
4. **controller_check tiles** (OLD: `controller_check.py starship-cadet.html tiles` OK, exit 0, 35 s; on the candidate
   alone: the same 3 lines again):
   - `A on Next should go through How to play`
   - `after How to play the highlight should be on a square, not etnext`
   - `A on your hold should pick its tile and keep the highlight there (etnext)`
   - Likely GM1's tiles tutorial rework (note 41).

**R3: FAIL.** Four NEW FAILs: devmode_check (EV1 + CR1), arrows_d_check (CR1), controller ending (SC1?), controller
tiles (GM1). Everything else in the share OK, sound_check included.

## After the round

- Controller tiles is check-side (GM1): with controller_check.py from claude/p997-games 3966a4a (one line: one A per
  How to play step; the new tutorial has 15 steps, the old check pressed at most 12), the tiles part on the candidate game
  b14421f8...cf7d passes (exit 0, CONTROLLER CHECK OK). Run from a copy of the candidate's folder (the check finds
  cadet_test.py by its own file name, so it must be called controller_check.py).
- devmode trad: EV1 reports a fix in claude/p997-events ecc5236 (not re-run here yet).
