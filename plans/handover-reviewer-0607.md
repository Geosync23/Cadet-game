# Handover: reviewer 0607

- **Role:** reviewer for 0.60.7. session_01BusfBzBamabWrCsrwQeABh, branch `claude/reviews-0607` (from live 0.60.6a c8685cf). All verdicts are in `plans/reviews-0607.md`: newest first under "Verdicts", and the current passing tips at the top.
- **Reported to:** lead 10 (session_014hkEBULoSV9EKZZSwMWyPd) until 05:36, then **lead 11** (session_01YKC3CGA9VS4b7wuqLbPT7V), plus BM3 (session_01WrXgDfR5dzwktKJfYwVwsV) and **BM4** (session_013h22isZZqmJJSEKSbrwabf). Findings go to the builder directly.
- **Never changed game code, and never contacted the user.**

## Passing tips at handover (all 0.60.7 seats)
writer 0cc4cdf · arrival-0607b 79d8244 (contains arrival e2cd435, PE6 52839a6, systems 1e9476c) · systems 521742a · social 9c8ea6c · PE6 4bd606c · deck 55fca8d · traditions 8a512b5.

## Combine notes (for whoever reviews the candidate)
- traditions 5de2087's events_check/device_check pass only with social's `morning()` (d3d5b4d and later) merged: the early-morning let-offs were removed.
- The bar opens only with someone behind it: PE6's bar order needs social's bartender rota (Ivo Madsen, relief Tamsin Haddad).
- systems 1e9476c/521742a and PE6 0.28.62-65 both edit section 15/15b's jobTap, ixChoreTap, cart toasts and goal labels: expect a hand merge, then re-run player_check and interactions_check.
- social_check `--long`'s arrival-jump arm FAILs on section 17 notes. It's pre-existing; the check fix is in claude/social 068b8db.
- BM3 reports events_check OK on the combine with social in (the day-100 and day-231 seat clashes are gone).

## Open LOWs (nobody needs to act before the combine)
- onboarding: the dawdle path squeezes the arrival dinner (left for 0.60.8).
- social: `@wq-` shower-queue fallback spots can coincide (only where there's no DA4 `shower-queue` place).
- social: crew knitters/drawers use the `read` pose (no knit/draw poses yet).
- PE6: a bought drink isn't saved (by design).

## How I tested
- Setup: `pip install playwright`; three r128 in `/tmp/cadet-work/three` (`npm pack three@0.128.0`, untar); `CADET_WORK=/tmp/cadet-work CADET_CHROME=/opt/pw-browsers/chromium`.
- Copy files to a scratch folder with `git show <hash>:<file>`; run checks there. One browser job at a time.
- Probes: `exec(open('cadet_test.py').read().split('import sys, json, hashlib')[0])`, then `g = Game(pw, 'new.html')`, `g.ev(js)`, `g.step(n)`. performance.now()/Date.now() are virtual in the harness (timings read 0).
- cadet_test hides `#needStrip`; to look at the strip, strip that rule out of the injected style.
- Content: `git archive <hash> | tar x`, then `python3 content_gen.py` and `python3 lines_check.py` there (not with `-I`: it imports content_gen from its own folder).
- Rough timings: cadet_test ~1 min, day_check ~4-5 min a day, food_check ~1 min, machine_check under a minute, clothes_check a few minutes, intro_check --dawdle ~10 min.
