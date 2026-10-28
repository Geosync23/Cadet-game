# 0.95.0 full round 3: runner R5 (the build master's share)

- Build: `claude/staging-p5s6` b5199dc3, game sha256 `b18d2b6487e71ba5b1d806997821b6c11368a92659b8d4f6e97d9ffbb434238a` (matched).
- OLD: 0.94.0, integration 6f1915cb, game sha256 `5f4c5415...0a0f`.
- Checks as they are at b5199dc3, run 2026-10-27/28, at most two browsers at once, each its own CADET_WORK.

| Check | Result | Key lines |
|---|---|---|
| check_fast.sh | OK | QUICK CHECK OK in 445 s (words, names, deck, device, machine, leave) |
| cadet_test OLD BUILD | OK | ALL IDENTICAL |
| machine_check (run 1) | OK | MACHINE CHECK OK |
| machine_check (run 2) | OK | MACHINE CHECK OK; same as run 1 except one timing line (shipEffects us/ms) |
| mech_check (all rows) | OK | MECH CHECK OK |
| bigevents_check | OK | BIGEVENTS CHECK OK |
| events_check | FAIL, known old (FX24-2) | reading-corner day 7: `not reached: ['farouk-olu>3-lounge-28 16:00']`, nothing else |
| fridays_check | OK | FRIDAYS CHECK OK |
| promo_beats_check (whole) | OK | PROMO BEATS CHECK OK |
| ending_check | OK | ENDING CHECK OK |
| arrows_check endstay (all ways) | OK | ARROWS CHECK OK |
| arrows_check endgo (all ways) | OK | ARROWS CHECK OK |

## The one FAIL

- events_check: **known old, backlog FX24-2.** Proof: events_check on OLD (0.94.0) fails the same way, the only FAIL
  line being the same `farouk-olu>3-lounge-28 16:00` miss at reading-corner day 7 (2/3 reached).

**R5: OK** (the only FAIL is known old FX24-2).
