# Handover: adversarial reviewer 1e

- **Role:** adversarial reviewer. I report to **lead 8** (session_01FutyR6xiAmZv29oS4TWKdS). It took over from session_01KPJMYjXAPkNUcrQ8VRkhLE at about 19:57, which confirmed the handover. I message the owning seat with send_message too. I never change game code and never contact the user.
- **Branch:** `claude/reviews-4`, notes only, under `plans/reviews/`. The format is reviewer 1c's and 1d's: PASS / PASS WITH FIXES / FAIL, a severity per finding, a concrete fix, and a probe saved next to the note where it matters.
- **Cost rules (the user):** in-depth reviews only for behaviour and save changes; run only the checks you need.

## Done (2026-10-17)
| Item | Note | Verdict |
| --- | --- | --- |
| player-needs 0.28.41-0.28.47 (f2c2f81, 48f66e8): '+go', warnings, 34 tips, social by bond, News feed, Relationships, tray fix | player-needs-f2c2f81.md (+ news probe) | PASS WITH FIXES. **MEDIUM open:** feed tradition posts show the id ("late-piano") because `ctx.trad = id` and `linesFill` uses a string ctx value as-is. Fix: `{ trad: name, tradId: id }` plus `linesOk` 'trad' matching `tradId` (section 22). With player engineer 5 (session_01SyRmwPxQEVKab6re9UgyrD). |
| social-fixes 0.62.5 (9463960), calls home stay open, postbox gone | social-fixes-9463960.md | PASS, one LOW (a recorded message on a tile with no room closes) |
| leave 0.61.12 (0af21bf), day-0 sick | leave-0af21bf.md | PASS |
| poses 0.27.38-0.27.41 (perf 3, session_01S8FWAPFnpaAAUN1wpDQbbo) | poses-405270f.md (+ 3 probes) | 0.27.40 PASS WITH FIXES: +40 MB heap. **Fixed in 0.27.43** (0f017737): heap 150 MB over a week and round trips, cadet_test identical, PERF CHECK OK. |
| poses 0.27.42 (b44f1b6, deck architect 3, session_01NsysH87qqJnf1dBEVRz2fW), Deck 4 toilets and WC signs | poses-b44f1b6-wc.md | PASS |
| arrival 0.42.29-0.42.30 (01a96d20, onboarding 3, session_016TRcnsFqFB1q5zZp6vjGBn) | arrival-01a96d20.md | PASS. The walk-up LOW is left as it is (lead 8: by design). |
| leave 0.61.13-0.61.16 (c08342c, career engineer, session_01862tURG1qXAVGj2sdUrVCw): time clock, rep chip | leave-c08342c.md (+ clock probe) | PASS WITH FIXES. **MEDIUM open:** `shiftTick` says missed at 10:00, but the career and the clock allow until 12:30. |

## Queue (from lead 8)
1. **DA3's 0.27.44 on claude/poses:** deep seats, plus Deck 4's washrooms back to 2 showers. Not on origin when I last looked. Light review: perf_check against 0.27.43 and cadet_test.
2. **PE6's builds:** the lead will send the range.
3. **Re-checks when they arrive:** PE5's trad-id fix (bake claude/content's `news.lines` and rerun `player-needs-f2c2f81-news-probe.py`; no post should contain an event id) and the career engineer's 10:00/12:30 fix (rerun `leave-6f5bc37-clock-probe.py`; the 10:30 and 12:00 rows should read late, not missed).

## How I test
- **Setup:** `pip install playwright`; three r128 in /tmp/cadet-work/three (`npm pack three@0.128.0`, then untar); `CADET_CHROME=/opt/pw-browsers/chromium`. Copy the build and the checks into the scratchpad with `git show <hash>:<file>`.
- **One browser job at a time.** Don't queue jobs with `while pgrep -f "_check.py"`: it matches its own shell and never starts. `pkill -f` on a pattern in your own command line kills your shell (exit 144). Chain jobs in one script instead.
- **Baking content into a build:** take the branch's own `content/` and `content_gen.py` (and `plans/trad_parse.py`, or the traditions bake empty), add the bank file under test, then `python3 -I content_gen.py game.html`.
- **perf_check.py** (on claude/poses): `perf_check.py NEW [OLD]` takes about an hour. It reports draw calls, the per-frame game-code time and the heap over a week and round trips. The dinner game time is noisy (±0.5 ms), so run a scene 2-3 times before calling it.
- **Timings:**
  - player_check: over 25 minutes (give `timeout` 2400+);
  - social_check: about 20 minutes;
  - day_check: about 15 minutes a day;
  - intro_check --evening: about 15 minutes.
- **Probes:** exec cadet_test.py's harness (`Game(pw, html)`, `ev`). For anything ticked by the game, step **every ship minute**. Ticking only at a few chosen times gave me false results once.
- **Gotchas:**
  - `linesFill` uses a string `ctx[k]` before `socialFill`.
  - section 20 saves its news inside `s.social`.
  - The player is never in `DECK_CREW`.
