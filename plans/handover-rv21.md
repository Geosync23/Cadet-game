# Handover: RV21 (reviewer: the Veyli vessel + the ending), 2026-10-26 ~22:10 UTC

**Role:** reviewer for "A Veyli vessel needs help" (EV_VESSEL_ON) and the ending (EV_ENDING_ON). Lead 39
(session_019V68fz33UFv4cK5Z4iCDvi) hired me; BM18 (session_01A3S2VBMYmTt2wCZa8ej7XR) gets every PASS with its sha. Notes-only
branch `claude/review-rv21`; full log `plans/review-rv21.md` (verdict table at the top). Never change the game or push to
builders' branches. Specs: plans/veyli-vessel-spec.html and plans/ending-spec.html on claude/p5-specs. User answers: vessel
C1 commendation yes, C2 ship visible yes, C3 wait at the ramp (Calder finds you 09:45, Zeke after 10:30); ending Q1 NO way
back (two end-page buttons: Keep this ending, Start a new game), Q2 change your mind until the address, Q3 post by Calder's
answer.

## Builders
VB1 session_01UsjGN26E88zwrNPWwef4iT (claude/vessel: V-1..V-4), VB2 session_01KRBGtugjBpv5iGcV5WDvCP (claude/vessel-sky, V-5,
done: cfc2dbe3 PASS), SW4 (inactive; vessel words 7dd2eb5d PASS), EN1 session_01Py28Kh6QV9kk64ri5AzQ5B (claude/ending:
cd4196d5 PASS), EN2 session_013er8NqC8eftyZqXBzcSibF (claude/ending-crossing: E-1 + E-4, the whole ending), SW5 (endgame
pool 8ed1545a PASS), SW6 (ending words b8c89e7a PASS).

## Open (as of this note)
- **VB1 V-2 73942e8a**: code read; checks were running (probe plans/rv21-shots/v2_probe.py, cadet vs acbb52e0, events,
  bigevents on-copy). Shoulds already noted to VB1: Taavek's goodbye window 14:45-15:00 missable; the round one has no
  fallback if missed; Saturday's sheet: arrow to Calder rather than Calder coming to you; vesselFind's setTimeout. V-2
  merged VB2's c070862c, not cfc2dbe3: the final vessel needs cfc2dbe3. V-3 (the chain) and V-4 (making the part) to come.
  Spec still wants arrows_check's vessel part (the arrow-follower, three ways + a Senior's rank) and controller_check
  presets: ask for them before the switch-on.
- **EN2 claude/ending-crossing**: da1f8e14 own parts PASS with 2 shoulds (the oath fetch + hold; Vance's notice words);
  waiting for EN2 to merge EN1's cd4196d5 and send the sha; then: cadet vs its staging base, ending_check, lines_check, a
  phone look (plans/rv21-shots/end_probe.py + cb_probe.py), PASS the ending as one. Spec also wants arrows_check endstay/endgo
  and day_check 31/35/36/50: ask before switch-on.
- Owners to review one-line hooks: section 14 guestTrim (VB1 vesselGuestTrim, sim owner); section 20 careerOff (EN1
  endOffDay, career engineer) and chatShow/chatDo (social engineer); section 19 devDay/Record (device engineer).

## How I test
Setup per plans/testing-guide.md 2.0 (/tmp/cadet-work and a second CADET_WORK /tmp/cadet-work2 for a parallel lane). One
worktree per sha under /tmp/rv21/wt-<sha>; old.html = the branch's merge base with staging (git merge-base), cadet_test
old vs new; switched-on copies by replacing the switch line (`URL_FLAGS.has('evvessel')` / `('ending')` with `true`).
At most 2 browsers at once (a 3rd risks timeouts); cadet_test's a_start 14812 px when run beside another check is the
known flake (FX17-2): rerun alone. Known-old: events_check FX24-2 (Farouk, reading corner Day 7).
Probes in plans/rv21-shots/ (vsky_probe.py + stub.js, vsky_bow.py, v2_probe.py, end_probe.py, cb_probe.py): run with
`CADET_CHROME=/opt/pw-browsers/chromium CADET_WORK=... python3 -I <probe> <wt>/starship-cadet.html <outdir>`.
Screenshots need `git add -f` (*.png is ignored).

## Gotchas
- SW4's session is inactive: vessel word fixes go through lead 39.
- A tip in the goodbye shot ("You missed a shift") found EN1's must: always look at the HUD and tips in shots, not just the
  scene.

## Open questions for the user
None from me.
