# CR6 check results

## Side job for lead 37 (2026-10-26): fridays_check on claude/event-swap 56fa0ca5 (game sha 9387754f...222a)

- OFF (file as is): exit 1 (1617 s), `FRIDAYS CHECK FAILED (1)`: "on: lines that never fill", the 7 Friday lines tagged `swap`.
- ON (copy, line 9395 `const EV_SWAP_ON = true;`; the check takes no URL flag): exit 1 (1618 s), `FRIDAYS CHECK FAILED (1)`:
  the same check, the 11 lines tagged `!swap`.
- Everything else passes in both. The check's never-fill filter (~line 289) excuses the storm's other side but not the
  swap's; it needs a `swap` / `!swap` excuse. Reported to lead 37, FX22b and RV18.
- Re-run on 4e13d5e3 (FX22b's check fix; game sha eb999383...b853): OFF exit 0 (1679 s) `FRIDAYS CHECK OK`. ON exit 1
  (1677 s) `FRIDAYS CHECK FAILED (1)`: one line never fills, Day 26 `wiak8h` "A month ago {me} came aboard. Since then:
  the Line, a storm, our first guests, and a comet." (tagged `swap`). It is 91 characters before {me} is filled, and
  friFill drops any line over 90, so the game never says it. A real (small) game fault: the line needs shortening.

## 0.93.1 full round (2026-10-26): all 11 OK, plus CR3's 3 (OK after RV16's check fix)

- **Build:** `claude/staging-0.93.1` 0a2fc617 (RV16's promo-arrow fix; the Tier 2 test arrow names the job only once
  it's on the board), game sha256 `6cd54ab97f4290aa5665ff40b5db35d0abc485dc8401d011084dfaa2f35a8eee` (matches BM18's).
  Later b957b92d (arrows_d_check fix only, game byte-identical). OLD df8d58b9 (0.93.0).
- Two lanes: my share in /tmp/work-cr6, CR3's three in /tmp/work-cr6b (so join and tiles ran beside controller_check,
  not alone; both passed).

| Check | Result | Key lines |
|---|---|---|
| check_fast.sh | OK (exit 0, 291 s) | `QUICK CHECK OK in 291 s` |
| stories_check | OK (exit 0, 61 s) | `STORIES CHECK OK` |
| mech_check | OK (exit 0, 750 s) | `MECH CHECK OK` |
| bigevents_check | OK (exit 0, 198 s) | `BIGEVENTS CHECK OK` |
| join_check | OK (exit 0, 359 s) | `JOIN CHECK OK` |
| tiles_check | OK (exit 0, 166 s) | `ALL OK` |
| disc_check | OK (exit 0, 471 s) | `ALL OK` |
| food_check 1 7 | OK (exit 0, 143 s) | `FOOD CHECK OK` |
| food_check 11 4 | OK (exit 0, 93 s) | `FOOD CHECK OK` |
| clothes_check | OK (exit 0, 125 s) | `ALL OK` |
| fridays_check | OK (exit 0, 1126 s) | `FRIDAYS CHECK OK` |
| arrows_f_check (taken from CR3) | OK (exit 0, 54 s) | `arrows_f_check: OK` |
| controller_check minus reach (taken from CR3) | OK (exit 0, 2853 s) | `CONTROLLER CHECK OK` |
| arrows_d_check, 0a2fc617's check (taken from CR3) | **FAIL** (exit 1, 120 s) | 2 lines in S3 (below); stale check |
| arrows_d_check, b957b92d's check | OK (exit 0, 86 s) | `arrows_d_check: OK` |

### arrows_d_check S3: stale check, fixed by RV16 (b957b92d)
```
FAIL S3: clocked in, a job to take: "Take a job at the board" at level 4 (Your Tier 2 test job, {'id': 'shift:job:9', ...})
FAIL S3: on the board, the pointer on Take it ({'up': True, 'now': 'p:board:lesson:t2', 'label': 'Take this one: your Tier 2 test job', 'text': 'Take it'})
```
- Same check on OLD df8d58b9's game: exit 0, S3 "Take a job at the board", pointer p:board:take. So the 0.93.1 game
  change caused the difference; BM18 and RV16 judged the game right and the check stale. b957b92d's check passes on
  the same game (S3 now reads the Tier 2 lesson).

## 0.93.0 full round (2026-10-25): all 11 OK, plus 2 taken from CR5 (OK)

- **Build:** `claude/staging-0.93.0` 4f1e52bf (sound and music, section 27; FX17's reserved-job fix), `starship-cadet.html`
  sha256 `97f21893d17bce087b2ab4b3a3cd769a2f696da88da263a3f5d4f2ae8c38f6a8` (matches BM18's). OLD 5898c190 (0.92.6).
- Fresh CR6 (session_013wLtAmKooMrgGrXF4Ljiof). Run from a separate worktree (/tmp/work-cr6/b093), one check at a time.

| Check | Result | Key lines |
|---|---|---|
| check_fast.sh | OK (exit 0, 240 s) | `QUICK CHECK OK in 240 s` |
| stories_check | OK (exit 0, 35 s) | `STORIES CHECK OK` |
| mech_check | OK (exit 0, 472 s) | `MECH CHECK OK` |
| bigevents_check | OK (exit 0, 153 s) | `BIGEVENTS CHECK OK` |
| join_check | OK (exit 0, 237 s, alone) | `JOIN CHECK OK` |
| tiles_check | OK (exit 0, 112 s, alone) | `ALL OK` |
| disc_check | OK (exit 0, 274 s) | `ALL OK` |
| food_check 1 7 | OK (exit 0, 54 s) | `FOOD CHECK OK` |
| food_check 11 4 | OK (exit 0, 59 s) | `FOOD CHECK OK` |
| clothes_check | OK (exit 0, 73 s) | `ALL OK` |
| fridays_check | OK (exit 0, 944 s) | `FRIDAYS CHECK OK` |
| events_check (taken from CR5) | OK (exit 0, 527 s) | `EVENTS CHECK OK` |
| sound_check (taken from CR5) | OK (exit 0, 169 s) | `SOUND CHECK OK` |

## 0.92.6 full round (2026-10-25): 3 new FAILs on b78e1e22, all OK on the final 6b425814

- **Build:** `claude/staging-0.92.6` b78e1e22 (all six switches on, odd jobs included), `starship-cadet.html` sha256
  `88f4cc8db099337d1ae61cf05e58be93af6577abea5458ba1449a27733f16fe4` (matches BM17's). The first candidate defc327f
  was withdrawn before any check finished. OLD 39f7741d (0.92.5).
- Share: all 11 here, one at a time (join alone), including the new stories_check.

| Check | Result | Key lines |
|---|---|---|
| check_fast.sh | OK (exit 0, 290 s) | `QUICK CHECK OK`; repair share 56% (45/80, Days 2-28); odd jobs: 10 posted, days with 2+ small jobs [1, 2, 3, 4] |
| mech_check | **FAIL** (exit 1, 638 s) | `FAIL m17: the paper part differs after the rides` |
| bigevents_check | **FAIL** (exit 1, 215 s) | two lines: Captain Marrow at the stands, not the Line (below) |
| fridays_check | OK (exit 0, 1280 s) | `FRIDAYS CHECK OK` |
| disc_check | OK (exit 0, 325 s) | `ALL OK` (0.92.5's #25 FAIL fixed by FX23) |
| tiles_check | OK (exit 0, 121 s) | `ALL OK` |
| join_check | **FAIL** (exit 1, 239 s, alone) | 9 lines `appt-<id>: not on in 400 days` |
| food_check 1 7 | OK (exit 0, 63 s) | `FOOD CHECK OK` |
| food_check 11 4 | OK (exit 0, 67 s) | `FOOD CHECK OK` |
| clothes_check | OK (exit 0, 91 s) | `ALL OK` |
| stories_check | OK (exit 0, 34 s) | `STORIES CHECK OK` |

### mech_check m17 (the lift roof): NEW
- `FAIL m17: the paper part differs after the rides` (mech_check.py:1692): m17's paper state read again after the two roof
  rides doesn't match the first read ('talk' aside). OLD `mech_check.py OLD m17`: exit 0. NEW m17 alone: fails again.

### bigevents_check: NEW (traditions vs the Line)
```
FAIL on: marrow (off) isn't planned at crossingCeremony (D7 Sun 14:40, Deck 3 bow lounge): leisure at 7-stand-28 (Stands, Deck 7)
FAIL on: marrow isn't on a lead spot at the oath: {'place': '7-stand-28', 'tag': 'ev-rec-wso-cheer', 'act': 'leisure', 'from': 743, 'to': 903}
```
- The Captain is planned cheering at the rec deck stands (a tradition, switched on in this build) 12:23-15:03 on Day 7,
  over the Line ceremony she leads at 14:40. OLD (traditions off): `BIGEVENTS CHECK OK` alone.

### join_check: NEW (appointments)
- 9 lines, all `FAIL appt-<id>: not on in 400 days` (brennan-book, scope, teach-me, shadow, show-tell, rehearse,
  midnight-feast, night-round, garden-bed); nothing else fails. join_check looks each tradition up on the calendar; the
  appointments are booked, not calendared. Probably the check needs to skip or book them. OLD has appointments off.

All three reported to BM17 and lead 36 at once.

### Re-run of the three FAILs on the final 0.92.6 commit: all OK

- `claude/staging-0.92.6` 6b425814, game sha256 `10f654de56f76598c0747530fe5d05185fcc6eb5e91398584d462aafc8ebf266`
  (matches BM17's): FX17's Line-clash fix in the game; FX17's m17 and FX22b's join_check fixes in the checks. Run with
  6b425814's own scripts, one at a time, join alone.

| Check | Result | Key lines |
|---|---|---|
| mech_check | OK (exit 0, 643 s) | `MECH CHECK OK` (m17 passes) |
| bigevents_check | OK (exit 0, 158 s) | `BIGEVENTS CHECK OK` (the Line ceremony's guard clear) |
| join_check | OK (exit 0, 264 s, alone) | `JOIN CHECK OK` (no appointment FAILs) |

## 0.92.5 full round (2026-10-25): FAIL (1 new: disc_check #25, traced to FX12 0aaf48b, check fix pending)

- **Build:** `claude/staging-0.92.5` 53c11f888efe00dbff89cadbfbd81c326e82de84, `starship-cadet.html` sha256
  `fddc0ef61c68ac012409a0f88e4ded2a62098b28377760461d99fb144b595559` (matches BM17's). OLD ba836359 (0.92.4, 2aa6427f...13a2).
- Share (the guide's): all 10 run here, one at a time; tiles and join alone.

| Check | Result | Key lines |
|---|---|---|
| check_fast.sh | OK (exit 0, 215 s) | `QUICK CHECK OK in 215 s`; `the repairs' share over Days 2-28: machine jobs 87, repairs 42 (48%)` |
| mech_check | OK (exit 0, 436 s) | `MECH CHECK OK` |
| bigevents_check | OK (exit 0, 131 s) | `BIGEVENTS CHECK OK` |
| fridays_check | OK (exit 0, 909 s) | `FRIDAYS CHECK OK` |
| disc_check | **FAIL** (exit 1, 251 s; same on a re-run alone, 255 s) | two lines in the new #25, below |
| tiles_check | OK (exit 0, 95 s, alone) | `ALL OK` |
| join_check | OK (exit 0, 187 s, alone) | `JOIN CHECK OK` |
| food_check 1 7 | OK (exit 0, 49 s) | `FOOD CHECK OK` |
| food_check 11 4 | OK (exit 0, 55 s) | `FOOD CHECK OK` |
| clothes_check | OK (exit 0, 62 s) | `ALL OK` |

### disc_check #25 (the crew's own lightdisc games): NEW

```
FAIL #25 their game: both players move to meet it ([2, 8] places each)
FAIL #25 Day 2 19:15: one alone at the stern practises, the disc in the air (0 of 8 looks)
```

- One player of the 17:22 pair moves to only 2 places in 8 looks (the other 8); the disc itself is in the air and
  moving (8 of 8). The lone player at 19:15 never has the disc in the air (0 of 8).
- Passing around them: the pair on the baselines at 17:22, the same rally twice, the crew's disc hidden during your game,
  all older parts, no page errors.
- Correction (BM17): #25 dates from 0.92.3, not this build; I misread the disc_check.py diff. OLD 0.92.4 (ba836359)
  passes all six #25 lines with the same script. A re-run alone here gave the identical two FAILs (deterministic).
- **Status: NEW FAIL, traced to FX12 0aaf48b, owner fixing the check.** BM17 bisected it to FX12's merge 0aaf48b: the new
  Tuesday late piano moves the 19:15 practiser off the court on Day 2, and the pair's rally differs, so one player moves
  to only 2 places in the 8 looks. A check pinned to a schedule, not a broken game; lead 35 is picking the owner.

## 0.92.4 full round (2026-10-24): OK

- **Build:** `claude/staging-0.92.4` 5bad724de037282a640bc742449a908ff8e8b7bb, `starship-cadet.html` sha256
  `2aa6427fde381f3ddf746900ed9e7a62f51aa27f0bb6460f73c557836fa313a2` (matches BM16's). OLD 3866c8f3 (0.92.3), not needed.
- Agreed before starting: controller_check (all but reach) to CR3; food 1 7, food 11 4, clothes to CR4 (CR4: all OK).

| Check | Result | Key lines |
|---|---|---|
| check_fast.sh | OK (exit 0, 261 s) | `QUICK CHECK OK`; `the repairs' share over Days 2-28: machine jobs 76, repairs 40 (53%)` |
| mech_check | OK (exit 0, 599 s) | `MECH CHECK OK` |
| bigevents_check | OK (exit 0, 152 s) | `BIGEVENTS CHECK OK` |
| fridays_check | OK (exit 0, 1137 s) | `FRIDAYS CHECK OK` |
| disc_check | OK (exit 0, 111 s) | `ALL OK` |
| tiles_check | OK (exit 0, 107 s, alone) | `ALL OK` |
| join_check | OK (exit 0, 144 s, alone) | `JOIN CHECK OK` |
| lines_check --day (taken from CR2) | OK (exit 0, 357 s) | `lines_check --day: PASS (0 errors)` |

## 0.92.3 (2026-10-24)

Taken from CR2 (its handover, nothing run twice; CR4 told), same build d9a387b6 (sha f18e8540...07853):

| Check | Result | Key lines |
|---|---|---|
| path_check | OK (exit 0, 78 s) | `PATH CHECK OK` |
| arc_check | OK (exit 0, 16 s) | `ARC CHECK OK` |
| lines_check | OK (exit 0, 5 s) | `lines_check: PASS (0 errors, 49 warnings)` (candidate 1 also 49) |
| lines_check --day | OK (exit 0, 382 s) | `lines_check --day: PASS (0 errors)` |

### Round 1: 0dd4e2e2 (sha 4e653844...cd0a2): stopped after one NEW FAIL

- check_fast OK (262 s; gated repair share 53% over Days 2-28, the 14-day line 39% for information), bigevents OK.
- mech_check FAIL (new): `FAIL m3d taps: done by you, trained, no arrow left (['done', 'you', True, 'Clock in at the time
  clock', [True]])`. OLD 0.92.2 (364c80cb) passes m3d with the same mech_check.py; NEW failed it again alone. BM16 traced
  it to AC3's item 6 (clock-in tracked on a Day 3 afternoon); fixed in 4928271f (RV12 PASS). The round was restarted.

### Round 2: d9a387b6: OK

- **Build:** `claude/staging-0.92.3` d9a387b6c795eacd448fc2419c09f6e95e6e1e70, `starship-cadet.html` sha256
  `f18e85405e2f18893bb97d10915f3d068a4b02ac66ff74c441353eb22f107853` (matches BM16's). OLD 364c80cb, not needed.
- Agreed before starting: controller_check (all but reach) to CR3; food 1 7, food 11 4, clothes to CR4 (CR4: all OK).

| Check | Result | Key lines |
|---|---|---|
| check_fast.sh | OK (exit 0, 246 s) | `QUICK CHECK OK in 246 s`; `the repairs' share over Days 2-28: machine jobs 76, repairs 40 (53%)` |
| mech_check | OK (exit 0, 609 s) | `MECH CHECK OK` (m3d passes) |
| bigevents_check | OK (exit 0, 151 s) | `BIGEVENTS CHECK OK` |
| fridays_check | OK (exit 0, 1175 s) | `FRIDAYS CHECK OK` |
| disc_check | OK (exit 0, 121 s) | `ALL OK` |
| tiles_check | OK (exit 0, 113 s, alone) | `ALL OK` |
| join_check | OK (exit 0, 155 s, alone) | `JOIN CHECK OK` |

## 0.92.2 full round (2026-10-24): OK

- **Build:** `claude/integration-next` ee974894 (0.92.2), `starship-cadet.html` sha256
  `ca2f908d603a53c24c110d26e22b71bc43d26b94d904f2129d9ea494a206e7e4` (matches BM15's).
- **OLD:** 0.92.1 e03505fd (2dbb11b8...59b18c). Not needed: no FAIL.
- Share: check_fast, mech, bigevents, fridays, disc, tiles (alone), join (alone). Handed to CR3 before they started:
  controller_check (all but reach), food 1 7, food 11 4, clothes.

| Check | Result | Key lines |
|---|---|---|
| check_fast.sh | OK (exit 0, 224 s) | `QUICK CHECK OK in 223 s`; machine repair share `machine jobs 39, repairs 19 (49%)` |
| mech_check | OK (exit 0, 481 s) | `MECH CHECK OK` (m8 passes) |
| bigevents_check | OK (exit 0, 121 s) | `BIGEVENTS CHECK OK` |
| fridays_check | OK (exit 0, 973 s) | `FRIDAYS CHECK OK` |
| disc_check | OK (exit 0, 72 s) | `ALL OK` |
| tiles_check | OK (exit 0, 94 s, alone) | `ALL OK` |
| join_check | OK (exit 0, 112 s, alone) | `JOIN CHECK OK` |

## 0.92.1 full round (2026-10-23): OK (mech after FX6's test-only m8 fix)

- **Build:** `claude/integration-next` 51a1bb34 (0.92.1, Crossing the Line ON), `starship-cadet.html` sha256
  `2dbb11b81c6d0da3bcaf32ad0d78ead80e4dcc8fa8b4ea5fc142bf1d2a59b18c` (matches BM15's; unchanged at 54efee21).
- **OLD:** 0.92.0 685af944 (f2329b62...1ebd).
- Share: check_fast, mech, bigevents, fridays, disc, tiles (alone), join (alone). Handed over before they started:
  controller_check (all but reach) to CR3; food 1 7, food 11 4, clothes to CR4 (all OK: 56 s, 69 s, 89 s).

| Check | Result | Key lines |
|---|---|---|
| check_fast.sh | OK (exit 0, 274 s) | `QUICK CHECK OK in 274 s`; machine repair share `machine jobs 39, repairs 19 (49%)` |
| mech_check | first run FAIL (exit 1, 604 s) -> **OK** on 54efee21's check (exit 0, 601 s) | first: `FAIL m8: a crew-only team job runs and puts the machines right` (OLD passes m8; BM15: the Line makes m8's team job the washers, two end at 88.6/89.3). Re-run with 54efee21's mech_check.py (sha f4a11f79), alone: `MECH CHECK OK` |
| bigevents_check | OK (exit 0, 164 s) | `BIGEVENTS CHECK OK` |
| fridays_check | OK (exit 0, 1208 s) | `FRIDAYS CHECK OK` |
| disc_check | OK (exit 0, 91 s) | `ALL OK` |
| tiles_check | OK (exit 0, 118 s, alone) | `ALL OK` |
| join_check | OK (exit 0, 148 s, alone) | `JOIN CHECK OK` |

## 0.92.0 re-run on FX5's Day 0 table fix (2026-10-23): OK

- **Build:** `claude/integration-next` 4e324417, `starship-cadet.html` sha256
  `f2329b620c113b0a585d6129ef70a3cbb8f8112c6ef9d19a13587fb996271ebd` (matches BM14's). My part: food x2, each alone.

| Check | Result | Key lines |
|---|---|---|
| food_check 1 7 | OK (exit 0, 74 s) | `FOOD CHECK OK` |
| food_check 11 4 | OK (exit 0, 69 s) | `FOOD CHECK OK` |

## 0.92.0 full round (2026-10-23): OK (after test-only check fixes)

**Final:** every check in my share passes on game sha256 c2180854...f1286. The five first-pass FAILs were all in the
checks (written for arrows off, or reading a pop-up that the arrows-on queue holds back); each was fixed in the check
only and re-run alone on the same game file:

| Check | Re-run with | Result |
|---|---|---|
| mech_check | a9823284's mech_check.py (sha 6a067a85) | OK (exit 0, 582 s), `MECH CHECK OK`; fx3 m6 goal `[4, '4-valve-panel', 'Follow Calder to the burst pipe, Deck 4']`; the last part ran |
| join_check | b842fa43's join_check.py (sha 6be4e077) | OK (exit 0, 143 s), `JOIN CHECK OK`, no FAIL lines |
| clothes_check | 6cc38797's clothes_check.py (sha 48241023) | OK (exit 0, 88 s), `ALL OK` |
| tiles_check | 567e39fc's tiles_check.py (sha 50f95a28), fully alone | OK (exit 0, 116 s), `ALL OK` |
| fridays_check | 6c55b296's fridays_check.py (sha a4a1e69c) | OK (exit 0, 1142 s), `FRIDAYS CHECK OK`; missed on Day 26 `[26, 19, 1] mails 1` |

controller_check (all parts but reach) went to CR3: 26 parts OK, day FAILs only with the known KC1/KC2.
A slip on my side: the first tiles re-run waited on itself (my "nothing else running" guard matched its own
command line), so cab36489's version never ran; only 567e39fc's (the one that ships) did, as BM14 asked.

### First pass

- **Build:** `claude/integration-next` 4147f03d (0.92.0: the teaching arrows ON, breakfast at 07:00, Zeke's tour, the
  dinner spread and more), `starship-cadet.html` sha256
  `c2180854a780936c21cbac0ba9e7932fb491759f740e1d5ac3b4d4494a4f1286` (matches BM14's; unchanged at 25a90ced/a9823284).
- **OLD:** 0.91.0 989fd566 (da9f1d08...aee).
- Share: check_fast, mech, bigevents, fridays, disc, tiles (alone), join, food 1 7, food 11 4, clothes, one at a time.
  controller_check (all but reach) was handed to CR3 before it started.

| Check | Result | Key lines |
|---|---|---|
| check_fast.sh | OK (exit 0, 255 s) | `QUICK CHECK OK in 255 s`; machine repair share `machine jobs 41, repairs 17 (41%)` |
| mech_check | FAIL (exit 1, 546 s) | new part fx3: `FAIL m6: after the talk the arrow follows the teacher to the pipe (None)`, then a crash at mech_check.py:1698 (TypeError on a None goal). The part was written for arrows off; fixed in the check (AC3 876711e7, FX3 f058b082); rerun pending |
| bigevents_check | OK (exit 0, 174 s) | `BIGEVENTS CHECK OK`; Line supper at most 38 at once, 48 seats |
| fridays_check | FAIL (exit 1, 1167 s) | `FAIL on: the missed banner and Mail [26, 19, 2] 1`: check artifact (BM14): a queued pop-up goes through toast() twice (guideToast queues, guideTick replays); the player sees it once. Check fix pending |
| disc_check | OK (exit 0, 93 s) | `ALL OK` |
| tiles_check | FAIL (exit 1, 117 s, alone) | new "partners sit" part: `once you sit, someone free comes over` (Zofia sits; the toast read is a "New job" one), `nobody free: a toast says so` (you stay sat; the toast read is the earlier "You leave the game"). Check reads a queued toast; fix pending |
| join_check | FAIL (exit 1, 148 s) | all 21 traditions `no join notice: You wake in Bunk 1 ...` (the first-wake tip is read; the join notice is queued). The rest passes. Same queued-toast pattern; fix pending |
| food_check 1 7 | OK (exit 0, 58 s) | `FOOD CHECK OK` |
| food_check 11 4 | OK (exit 0, 69 s) | `FOOD CHECK OK` |
| clothes_check | FAIL (exit 1, 86 s) | `the toast: your one spare` (the first-wake tip is read), `the toast says the kit came up from stores` (the washing-done toast is read); state checks pass. Same pattern; fix pending |

## 0.91.0 full round (2026-10-22): OK

- **Build:** `claude/integration-next` 989fd566 (0.91.0: the controller on 0.64.16, switched off, + fresh-eyes batch 1;
  no breakfast), `starship-cadet.html` sha256 `da9f1d0851efa06a307e2fafe9eef9ff4d867d625c2f5c2d3e584aa79dc94aee`
  (matches BM14's).
- **OLD:** 0.64.16 b9f053ba. Not needed: no FAIL.
- Share: all 10, one at a time, tiles alone. (CR1 offered to take fridays; it was already running here.)

| Check | Result | Key lines |
|---|---|---|
| check_fast.sh | OK (exit 0, 254 s) | `QUICK CHECK OK in 254 s`; machine repair share `machine jobs 40, repairs 20 (50%)` |
| mech_check | OK (exit 0, 197 s) | `MECH CHECK OK` |
| bigevents_check | OK (exit 0, 160 s) | `BIGEVENTS CHECK OK` |
| fridays_check | OK (exit 0, 1121 s) | `FRIDAYS CHECK OK` |
| disc_check | OK (exit 0, 82 s) | `ALL OK` |
| tiles_check | OK (exit 0, 107 s, alone) | `ALL OK` |
| join_check | OK (exit 0, 133 s) | `JOIN CHECK OK` |
| food_check 1 7 | OK (exit 0, 62 s) | `FOOD CHECK OK` |
| food_check 11 4 | OK (exit 0, 62 s) | `FOOD CHECK OK` |
| clothes_check | OK (exit 0, 83 s) | `ALL OK` |

## 0.64.17 round 2 (2026-10-22): OK

- **Build:** `claude/integration-next` 1498dbf4 (with SC1's m12 and Line supper fixes, CP4's bubble fix),
  `starship-cadet.html` sha256 `ff45b427d65d543ab8dfe10f289b49653f0102af8ef513b960dd2e2ecbfac306` (matches lead 29's).
- **OLD:** 0.64.16 b9f053ba. Not needed: no FAIL.
- Share (lead 29): check_fast, mech, bigevents, fridays (BM14 stopped its copy; this is the one), disc, tiles (alone), join.
  food 1 7, food 11 4 and clothes moved to CR4 before they started (CR4: all OK). One check at a time.

| Check | Result | Key lines |
|---|---|---|
| check_fast.sh | OK (exit 0, 251 s) | `QUICK CHECK OK in 251 s`; machine repair share `repairs 17 (40%)` of 42 = 40.5%, inside 40-60 at the edge (same as round 1) |
| mech_check | OK (exit 0, 196 s) | `MECH CHECK OK`; m12 fixed: `"night": ["done", "navarro-mateo", ["4-washer-3"]]`, `"logged": [12, 0.9]` |
| bigevents_check | OK (exit 0, 166 s) | `BIGEVENTS CHECK OK`; Line supper: 83 mean to go, 71 came, at most 44 at once, 48 seats, nobody standing |
| fridays_check | OK (exit 0, 1135 s) | `FRIDAYS CHECK OK` |
| disc_check | OK (exit 0, 86 s) | `ALL OK` |
| tiles_check | OK (exit 0, 103 s, alone) | `ALL OK` |
| join_check | OK (exit 0, 131 s) | `JOIN CHECK OK` |

## 0.64.17 full round (2026-10-22): FAIL (2 new)

- **Build:** `claude/integration-next` 8193458e (breakfast at 07:00, SC1's claude/patch-play1-f), `starship-cadet.html`
  sha256 `225836918e5a70cad2a9809b2aea8febc21837617f3dee907b49a07655a4c4b5` (matches BM13's).
- **OLD:** `claude/integration` b9f053ba (0.64.16, sha256 70f94273...e6a5c7).
- Share: check_fast, mech, bigevents, disc, tiles (alone), join, food 1 7, food 11 4, clothes. One at a time (my m12 re-runs
  overlapped bigevents; BM14 then re-ran bigevents alone on both builds).

| Check | Result | Key lines |
|---|---|---|
| check_fast.sh | OK (exit 0, 272 s) | `QUICK CHECK OK in 272 s`; machine_check's watch point: `a steady player, Days 2-14: 80 jobs ..., machine jobs 42, repairs 17 (40%)`: 40.5%, inside 40-60 at the edge |
| mech_check | **FAIL** (exit 1, 209 s) | m12, two lines (below) |
| bigevents_check | **FAIL** (exit 1, 184 s) | `FAIL line: the Line supper (seated): 1 eat standing, no seat for their sitting: ['silva-bea']` |
| disc_check | OK (exit 0, 92 s) | `ALL OK` |
| tiles_check | OK (exit 0, 110 s, alone) | `ALL OK` |
| join_check | OK (exit 0, 138 s) | `JOIN CHECK OK` |
| food_check 1 7 | OK (exit 0, 66 s) | `FOOD CHECK OK` |
| food_check 11 4 | OK (exit 0, 72 s) | `FOOD CHECK OK` |
| clothes_check | OK (exit 0, 90 s) | `ALL OK` |

### mech_check m12 (the logbook): NEW

```
FAIL m12: the open job written up is 10% quicker ([None, 1])
FAIL m12: the flagged machine seen to by the night crew at 22:00 (['open', None, ['4-washer-3']])
```

- NEW: the flagged Washer 3 is still open at 22:00, claimed by nobody; so the written-up job's 10% never applies.
- OLD (0.64.16, `mech_check.py OLD m12`): passes; `"night": ["done", "navarro-mateo", ["4-washer-3"]]`, `"logged": [12, 0.9]`.
- Re-run of m12 alone on NEW (own CADET_WORK): the same two FAILs. Likely the breakfast patch's night-shift changes
  (b006ad0, 8d65f86). Reported to lead 28 and BM13 at once; SC1 is fixing it (lead 28).

### bigevents_check: NEW

- The Line supper, Day 7 18:00-19:45: 83 mean to go, 70 came, at most 44 at once, 48 seats; one (silva-bea) eats standing.
- BM14 re-ran bigevents alone: 0.64.17 FAILED the same way, 0.64.16 OK. Reported to lead 28 (BM14).

## 0.64.16 full round (2026-10-22): OK

- **Build:** `claude/integration-next` b9f053ba, `starship-cadet.html` sha256
  `70f9427354a398ef25e355e7428f10ba6f0800b4c83a83945c8c950a42e6a5c7` (matches BM13's).
- **OLD:** `claude/integration` 2b4a05db (0.64.15, sha256 0c1f6fb4...259d2e). Not needed: no FAIL.
- Share: check_fast, mech, bigevents, disc, tiles (alone), join, food 1 7, food 11 4, clothes. One at a time.

| Check | Result | Key lines |
|---|---|---|
| check_fast.sh | OK (exit 0, 277 s) | `QUICK CHECK OK in 277 s` |
| mech_check | OK (exit 0, 220 s) | `MECH CHECK OK` |
| bigevents_check | OK (exit 0, 178 s) | `BIGEVENTS CHECK OK` |
| disc_check | OK (exit 0, 94 s) | `ALL OK` |
| tiles_check | OK (exit 0, 117 s, alone) | `ALL OK` |
| join_check | OK (exit 0, 148 s) | `JOIN CHECK OK` |
| food_check 1 7 | OK (exit 0, 69 s) | `FOOD CHECK OK` |
| food_check 11 4 | OK (exit 0, 66 s) | `FOOD CHECK OK` |
| clothes_check | OK (exit 0, 87 s) | `ALL OK` |

## 0.64.15 re-run (2026-10-22): OK

- **Build:** `claude/integration-next` 31c44cb9 (merge of claude/patch-play1-d 836db6c7), `starship-cadet.html` sha256
  `0c1f6fb487d6f7f7a47ab3f4f20a475f0ded2b53107030bdd4dbfb6ef8259d2e` (matches the lead's).
- **OLD:** `claude/integration` 32b699a6 (0.64.14). Not needed: no FAIL.
- Share as before minus fridays_check (moved to CR1). One check at a time; tiles alone; CADET_WORK=/tmp/work-cr6.

| Check | Result | Key lines |
|---|---|---|
| check_fast.sh | OK (exit 0, 280 s) | `QUICK CHECK OK in 280 s` |
| mech_check | OK (exit 0, 228 s) | `MECH CHECK OK` |
| bigevents_check | OK (exit 0, 193 s) | `BIGEVENTS CHECK OK` |
| disc_check | OK (exit 0, 102 s) | `ALL OK` |
| tiles_check | OK (exit 0, 129 s, alone) | `ALL OK` |
| join_check | OK (exit 0, 154 s) | `JOIN CHECK OK` |
| food_check 1 7 | OK (exit 0, 73 s) | `FOOD CHECK OK` |
| food_check 11 4 | OK (exit 0, 82 s) | `FOOD CHECK OK` |
| clothes_check | OK (exit 0, 102 s) | `ALL OK`; `ok a busy washer sends you to a free one` (the first run's NEW FAIL is fixed) |

## 0.64.15 full round (2026-10-22): FAIL (1 new)

- **Build:** `claude/integration-next` c5c43293 ("0.64.15: playtest patch 1 ..."), `starship-cadet.html` sha256
  `e955d667fe946b3e1e0a21c0b1f3049694460096f675dad5019c328e5d7d4a25` (matches the lead's).
- **OLD:** `claude/integration` 32b699a6 (0.64.14), sha256 `94f32868dbe7f27fc744eb834bb6b5f7c335bc15ac1bca86563d8ca4652881e9`.
- **Setup:** CADET_WORK=/tmp/work-cr6, CADET_CHROME=/opt/pw-browsers/chromium; one check at a time; tiles alone.

| Check | Result | Key lines |
|---|---|---|
| check_fast.sh | OK (exit 0, 251 s) | `QUICK CHECK OK in 251 s` (words, names, deck, machine, leave, device) |
| mech_check | OK (exit 0, 204 s) | `MECH CHECK OK` |
| bigevents_check | OK (exit 0, 166 s) | `BIGEVENTS CHECK OK` |
| fridays_check | OK (exit 0, **1197 s**) | `FRIDAYS CHECK OK` (the guide says ~4 min; see note) |
| disc_check | OK (exit 0, 89 s) | `ALL OK` |
| tiles_check | OK (exit 0, 106 s, alone) | `ALL OK` |
| join_check | OK (exit 0, 137 s) | `JOIN CHECK OK` |
| food_check 1 7 | OK (exit 0, 58 s) | `FOOD CHECK OK` |
| food_check 11 4 | OK (exit 0, 79 s) | `FOOD CHECK OK` |
| clothes_check | **FAIL** (exit 1, 87 s; same on a re-run) | `FAIL a busy washer sends you to a free one`, `1 FAILED` |

### clothes_check: NEW

```
     toast: "Time clock\nStill not clocked in. The time clock's in the Works bay, Deck 5. Late is better than missed."
FAIL a busy washer sends you to a free one
```

- The step (clothes_check.py line 86-89) taps a busy washer and reads the toast for "is free". On 0.64.15 the toast
  showing is the **new** time-clock nag (`later:` text, starship-cadet.html line 15176; the string isn't in 0.64.14),
  so the washer's answer is covered or replaced.
- Proof it's new: the re-run on 0.64.15 fails the same way (deterministic). On OLD (0.64.14) with the same
  clothes_check.py, this step is `ok`; OLD fails only the two steps the check added for patch 1 #8
  (`changing ticks hygiene up ... (CLOTHES_FRESH 0)`, `no clothesDirtyTick`), as expected for a build without the patch.
- Not on the known-old list (backlog 14, 23). Whether it's the check's timing (the cadet is late for shift during the
  laundry part) or a real clash (a nag toast hiding the answer to the player's tap) is for the owner of the time-clock
  nag / clothes to judge.

### Note: fridays_check took 1197 s: not the patch

Timed alone, back to back, with the same fridays_check.py (unchanged between the two builds): **OLD 0.64.14: 1212 s,
NEW 0.64.15: 1275 s**, both `FRIDAYS CHECK OK`, load ~4.5 (the check's own browser). So the ~20 minutes is the
check on this machine, not the patch (within ~5%). The guide's "~4 min" for fridays_check is out of date for a
4-core cloud session; the six-way split's minutes for CR6 are about 16 too low.
