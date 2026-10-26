# Handover: RV21 (reviewer: the Veyli vessel + the ending), 2026-10-26 ~23:50 UTC (final)

**Role:** reviewer for "A Veyli vessel needs help" (EV_VESSEL_ON) and the ending (EV_ENDING_ON); also took two Step 5
reviews for RV20 at lead 40's ask. Lead is now **lead 40** (session_01NXybH7NNqM8M4ngiyidq6m); BM18
(session_01A3S2VBMYmTt2wCZa8ej7XR) gets every PASS with its sha. Notes-only branch `claude/review-rv21`; full log and the
verdict table: `plans/review-rv21.md`. Never change the game or push to builders' branches.
Specs: plans/veyli-vessel-spec.html and plans/ending-spec.html on claude/p5-specs. User answers: vessel C1 commendation
yes, C2 ship visible yes, C3 wait at the ramp (Calder finds you 09:45, Zeke after 10:30); ending Q1 NO way back (two
end-page buttons: Keep this ending, Start a new game), Q2 change your mind until the address, Q3 post by Calder's answer.

## Builders
VB1 session_01UsjGN26E88zwrNPWwef4iT (claude/vessel), VB2 session_01KRBGtugjBpv5iGcV5WDvCP (claude/vessel-sky; also takes
ending fixes if EN2 is gone), EN2 session_013er8NqC8eftyZqXBzcSibF (claude/ending-crossing; handing over), EN1 retired,
SW4 inactive (vessel word fixes via the lead), SW5/SW6 done.

## Where things stand
- **The ending: PASSED as one: claude/ending-crossing d1a61402** (EN1 395fe62e + EN2's E-1/E-4 + SW5/SW6 words). Before
  switch-on (lead 40 assigned EN2 / its successor): arrows_check endstay/endgo parts, controller presets (Days 32, 34, 35,
  36), day_check 31 and 50 on an on-copy. Hook owner reviews: careerOff (RV20 OK); chatShow/chatDo (social engineer) and
  devDay/Record (device engineer) still owed. Watch in play: the endgame pool's +250 weight for 14 days.
- **The vessel: VB1 claude/vessel 6d4b5192 PASS (V-1..V-4).** VB1's next push should carry the open shoulds: no crowd at
  the ramp (SW4's talk.rampCrowd unused); Taavek's goodbye arrow only from 14:45 (start 14:30, the Tern waits, Calder
  fetches); the round one has no fallback if missed; Saturday's sheet: Calder should come to you; the pilot's toast
  doubled; setTimeout x7 in the slot (use simTimeout); and **merge VB2's claude/vessel-sky 3fb8eac7** (12 blades, SW4's
  tap keys, the bench places; 6d4b5192 still has c070862c). Then the arrows_check vessel part and controller presets
  (lead 40 gave them to VB1). On that sha re-run: cadet vs its staging base, events_check (only known-old FX24-2),
  bigevents on an on-copy (must be OK), day_check 27-30 on-copy, a phone look (plans/rv21-shots/v2_probe.py,
  v34_probe.py, vsky_bow.py).
- **VB2's ending arrows checks**: review when sent.
- **Step 5 (for RV20):** B4 claude/p5s5-puzzles 6b07b624 PASS; B3 claude/p5s5-m20 7c5d9f79 PASS with 4 shoulds (its m20
  check parts skip without the preview switch; teacher name mixed Mori/Calder; Tracked row doubled; 06:20 Mail before the
  in-person word; recheck the Day 19 opening after the ladder-order merge deefa61a). Further Step 5 goes back to RV20.

## How I test
Setup per plans/testing-guide.md 2.0 (/tmp/cadet-work and a second CADET_WORK /tmp/cadet-work2 for a parallel lane). One
worktree per sha under /tmp/rv21/wt-<sha>; old.html = the branch's merge base with staging (git merge-base), cadet_test
old vs new; switched-on copies by replacing the switch line (`URL_FLAGS.has('evvessel')` / `('ending')` with `true`).
At most 2 browsers at once; cadet_test's a_start 14812 px beside another check is the known flake (FX17-2): rerun alone.
Known-old: events_check FX24-2 (Farouk, reading corner Day 7). Run long queues as one tracked background command (a
plain `&` inside a command dies with it; `pkill -f` with a pattern in your own command line kills itself).
Probes in plans/rv21-shots/ (vsky_probe.py + stub.js, vsky_bow.py, v2_probe.py, v34_probe.py, end_probe.py, cb_probe.py,
m20_live.py): `CADET_CHROME=/opt/pw-browsers/chromium CADET_WORK=... python3 -I <probe> <wt>/starship-cadet.html <outdir>`
(m20_live.py and RV20's probes also take a serve dir and a port). Screenshots need `git add -f` (*.png is ignored).
Probes that jump the clock leave banners and toasts up: judge them in real-time play, not after a jump.

## Gotchas
- Look at the HUD and tips in every shot, not just the scene: the "You missed a shift" tip found EN1's must.
- Checks that print "not yet" for a preview switch did not test the piece: run them on a switched copy.

## Open questions for the user
None from me.
