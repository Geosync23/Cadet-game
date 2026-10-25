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
