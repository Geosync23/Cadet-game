# RV15 review notes (patch 0.92.6, lead 36)

Base: staging-0.92.5 53c11f8 (game fddc0ef6...5559).

## FX18 claude/p926-fx18 ed23b890 (game = f5f5d0bf, fc4539674f4e...a806): PASS (2026-10-25 ~09:00 UTC)
Items 1 (auditorium archway), 6 (bench bar), 12 (Tracked), 16 (Lift button), 17 (outfit line).
- cadet_test vs 53c11f8 ALL IDENTICAL; deck_check OK; clothes_check ALL OK; player_check OK; day_check Day 6 (film night) OK.
- bench_probe OK on FX18, FAILS on 53c11f8 (bar level, hands on bar).
- Question to lead (not blocking): the user said the outfit line is "at the top" of the device summary; it sits after the needs lines.

## FX19 claude/p926-fx19 dd5bd426: FIXES NEEDED (2026-10-25 ~09:00 UTC)
Items 14, 18, 11; switches PROMO_SIGHT_ON, BOARD_TRADE_ON (off).
- cadet_test (off) ALL IDENTICAL; promo_sight_check OK; career off/on OK; arrows promo off/on OK (the old FAIL is fixed);
  day_check 9/10 on OK; interactions off OK (on: pending).
- Fix 1: promoReady adds "Tomorrow, your test job" even when the test is Monday (Friday/Saturday offers in the bay).
- Fix 2: Calder can say "well done" in the Works crew's cheer after the summons (worksGather includes her; the
  promo-works bank and CHEER_LINES have "well done"). This path is older (0.71.2).
Probes: /tmp/rv15/probe_cheer.py, probe_tomorrow.py (container only).

## Final (2026-10-25 ~09:45 UTC)
- FX18 a9fc0eb2 (game 82fd7a1f...4e51): PASS. Outfit line moved under the season line (lead 36); clothes_check ALL OK.
- FX19 b7c4e3c5 (game c64590d0...6c10): PASS. Fix 1 (Tomorrow only when it is) and fix 2 (cheerTick skips Calder,
  not behind a switch) confirmed; promo_sight OK, cadet_test ALL IDENTICAL, arrows promo with the switches on OK.

## FX18 claude/fx18-det 8ed625fa (test-only, backlog FX17-2): PASS (~09:50 UTC)
Each run copy gets its own name (pid + count); two cadet_tests at once in one CADET_WORK each used their own copy; staging vs itself ALL IDENTICAL; no _run_ files left.

## FX18 claude/fx18-det 28f4669d (test-only, backlog FX18-1): PASS (~10:45 UTC)
RUN_ID per process in 8 checks; two career_checks at once in one CADET_WORK both OK, own copies, none left; controller_check named its copies per run, no FAILs, hit my 50 min timeout under load (not a fault). The cleanup is atexit only: a killed run leaves its uniquely named copies.

## FX20 claude/p926-fx20 bb0aefed (item 10, odd jobs, ODD_ON off): PASS (~15:40 UTC)
f8c9235b: cadet_test off ALL IDENTICAL; on: machine, day 2, deck OK; IX_ODD=oddall interactions FAIL (oj-d3prom-rail dead after oj-d5bay-clock, the time clock). Fixed by parking oj-d5bay-clock (9755ca3f): oddall interactions OK, 114 rows. bb0aefed = staging 1fe6d523 + that line; machine_check on OK (revised bar). Crew-occupancy note: 12 of 114 places busy at least 20% (FX10: 46 of 181).
