# Handover: RV30 (reviewer, 0.99.5 playtest patch)

Session session_014zyJYNFR7ewWJGvEQNUAHr. Hired by lead 47; now reports to **lead 48 (session_014zyJYMuqdRYh4dQhmVPr8S)**.
Build master BM23 (session_014zyJYPpetpQqNvn9pkGrig, claude/staging-0995). Other reviewer RV29 (session_014zyJYM3D7UBkZN49CsZVuA).
Branch claude/review-rv30: notes (plans/review-rv30.md, every verdict with shas), probes (plans/rv30-probes/), this file.

## State (2026-11-01 ~00:40 UTC): stopping here (memory); next reviewer takes the open item below
Verdicts sent (all in review-rv30.md):
- PASS sound claude/p995-sound a5ce274 (game 79f01421...bd86c); notes 9, 4, 17 (MESS_SCALE / SND_BUF_ON then switched on by the user's pick).
- PASS onboarding claude/p995-onboarding fb81b79 (game 7e66e20d...d2dc); notes 1, 7, 11, 16.
- PASS traditions + words claude/p995-traditions-words 52ea327 (game b815c01d...6bd0) = TB3 4037a26 + SW4's words.
- PASS TB5 claude/p995-traditions b7af35a (spice reveal never lost): left out of 0.99.5 (after switch-on), next 0.99.x.
- PASS BM23's sound_check r3mess edit (claude/bm23-wip 96d902e).
Builds of mine (lead 48's jobs):
- Tea fix claude/p995-tea-fix ee66e35b (game 93aed54f...5164): the tea corner's hot water makes tea again (ixTeaFirst in
  ixTap's sort, TRAD995_ON only). RV29 PASSed; in staging-0995 e00bfabd.
- arrows_check fix claude/p995-arrows-fix cc18dad0 (check only): a tradition's join arrow gets a real tap (tapCrew), not
  chatOpen; 'gym$' in the held-job act list. week OK on e00bfabd and 0.99.4. Sent to BM23 (quick read) and R1 (re-run).
- arrows fix cc18dad0: BM23 read and merged it (staging-0995 = cc18dad).
- puzzle_check: claude/p995-puzzle-fix 93839bf5 (check only, from cc18dad): the paper run counts repairs OFFERED, not cases
  posted. OK on 0.99.4; on the candidate that line passes.

## OPEN for the next reviewer: puzzle_check "p5's first: 3-pump-1's seal, slot 29, staged none" on the candidate
- Lead 48's bisect: only SPREAD_ON (JB2, note 15) off makes it pass. Passes on 0.99.4.
- NOT the scanner's held job: at that moment 3-pump-1 has only an unclaimed service job (3-pump-1@408); fixScanMachine picks
  4-pump-2 / 4-pump-1 / 3-nutrient-1 / 3-recycler-1 on Days 5/6/12/18.
- p5Stage reaches caseSolve, which answers why 'answer': the line reads low throughout (5-valve-2, 5-pump-1, 3-pump-1 at 0.36;
  3-recycler-1, 3-filter-1 at 0.6; the 0.99.4 run reads 0.6 / 1). p5Flow uses lineShare over machEff (cond less drift).
- Ruled out by experiment (full puzzle_check on the candidate, still 'none'): every machine cond 90; every machine cond 90
  AND drift 0 in P5FIRST. So something else feeds lineShare (look at lineShare / linePath: open jobs or faults on the line,
  a line setting, or the clock: P5FIRST sets the time back to Day 18 05:30 after the paper run went to Day 33).
- Run alone (only the check's SETUP first: plans/rv30-probes/p5_first.py) the candidate stages it and 0.99.4 doesn't, so it
  depends on what the earlier parts leave. Instrumented copy: scratch only (P5FIRST + dbgJobs / dbgSolve before
  WORK_MECH.p5.open); recreate it from this description.
- Game side (both builds, backlog P5-1 per lead 48): p5Stage marks case.p5.first 'none' forever after one failed solve.
- Backlog per lead 48: JB2-2 (gym locker stop is a treadmill), JB2-3 (fewer repairs, head-scratchers a little rarer).

## Probes (plans/rv30-probes), each prints its own usage at the top
hide_loop.py (note 9, real loop, frames held), stall_real.py (SND_LONG late starts), music_x.py, mess_day.py,
health_tap.py WT BUILD TAP_AT PACE (Rina's health check at reading pace), appt_views.py, spice_paced.py (TB3's spice probe at a
reading pace, SP_PACE), trad_mail.py (tradition Mails as sent), arrow_walk.py WT BUILD DAY FROM TO [realtap] (+AW_PRE js:
arrows_check's own walker, every act logged), odd_gym.py (an odd job's floor tap), p5_first.py, p5_real.py.

## Gotchas
- Setup: pip install playwright numpy pillow; three r128 + acorn 8.12.1 in /tmp/cw-w1 and /tmp/cw-w2; CADET_CHROME=/opt/pw-browsers/chromium.
- This container's browsers never really hide a tab (other tab, minimised window under Xvfb, CDP freeze all tried).
- The ship clock runs under dialogue (~0.6 ship min a real second): time-window bugs only show in a paced probe.
- `pkill -f`/`pgrep -f ... kill` with a name in your own command line kills your shell (happened twice). Kill by pid.
- Messages can arrive late (queued while a long tool call runs): reread before acting on an old ask.

## Open questions for the user
None from me.
