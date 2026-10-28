# 0.96.0 round, share R5 (BM20)

Candidate: claude/staging-pad 6db1cdd2 (later 652297471f, check-only), game sha256 c62d63999e6b596d21806d1cb14fa9ab3168a50c5038dfcc1c04f3163d37a74e (matched). OLD: 0.95.0 b5199dc3, b18d2b64...238a. Run 15:24-16:45 UTC, 2026-10-28, two lanes (plus a third for lane A's tail once lane B was done).

| Check | Result | Notes |
|---|---|---|
| check_fast | OK, 319 s | before the GO |
| machine x2 | OK, OK | |
| mech | FAIL, then OK on the fixed check | part_mrun crashed (`j2.status`): the visit's Day 16 lamp job takes the last lamp, so MRUN's lamp-only run on Day 17 had none. Bisect: OLD and e01bcee OK, 736b23a fails. EV1's check-only fix 65229747 (MRUN stocks lamps); mech whole on 652297471f OK (run by R3, 569 s). |
| bigevents | OK | |
| fridays | OK | 1548 s |
| events | known-old only | farouk-olu 3-lounge-28 16:00 (FX24-2) |
| disc, tiles | OK, OK | |
| join | FAIL (new) | farewell (Day 19): marker "Envoy", arrow "Tap Saruth" (`same` False). Bisect: 44ea40ef OK (farewell not joinable there), 6db1cdd2 fails; the visit pointer made it joinable. RV25: a game gap in section 18's tjFirst; EV1 fixing on claude/visit-pointer (with vesselLights' old "Tap Envoy to stand at the glass with Saruth"). A Page.goto timeout in the same run didn't repeat alone (load). |
| food 1 7, food 11 4 | OK, OK | run in lane C |
| clothes, stories, promo_beats | OK, OK, OK | run in lane C |
| day_check 12, 13, 16, 17, 18, 19, 27 | all OK | |
| arrows endstay / endgo | moved | lead 44 moved them to R1 / R2 |

Not in the gate: controller_check reach (detached, after the final game).

## Targeted rerun on fe11cd66 (game sha256 332925003934b49686c080515e154131a07f7fe7a3c14fbe0f6f7684933a129e)

EV1's fixes (puzzle_check to Day 33, p9's week of retries, tjFirst + the vessel lights' tip), RV25 PASS. 17:26-18:24 UTC.

| Check | Result |
|---|---|
| check_fast | OK, 313 s (on this tree before the push) |
| cadet vs 0.95.0 | ALL IDENTICAL (renderer noise) |
| lines, lines --day | PASS, PASS |
| join | farewell now OK; my run under load stopped at the page reload after the Sunday table (Page.goto 30 s); R3 ran it alone: JOIN CHECK OK, 228 s |
| promo_beats, bigevents, fridays | OK |
| events | known-old FX24-2 only |
| day_check 16, 17, 18, 19, 20, 22 | all OK |

controller_check reach: started detached 18:25 UTC on fe11cd66 (CTL_STATES / CTL_PADDONE in my scratchpad, so it resumes).
