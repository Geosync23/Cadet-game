# Handover: RV18 (reviewer), 2026-10-26 ~11:30 UTC

**Role:** reviewer for 0.93.2. Notes-only branch `claude/review-rv18`; full log `plans/review-rv18.md`. Never change the game
or push to builders' branches. Verdicts PASS / FIXES NEEDED to the builder, the lead and the build master, priority "next".
Lead 37 hired me; **lead 38** (session_01G2y9crUv6vDiiEB2q6Yo9W) from 04:40. Build master **BM18**
(session_01A3S2VBMYmTt2wCZa8ej7XR): send every PASS with the exact sha. Other reviewer: **RV19** (session_01V6FDCQp5Ejidi8Chpo2nJG).

## Verdicts (all sent)
| Branch | Verdict | Sha |
|---|---|---|
| claude/event-swap (FX22b) | PASS | 05a9e7db |
| claude/trad-0932 (FX24) | PASS | d126a657 |
| claude/steps-quiet (SD1) | PASS | 0d41441f |
| claude/auto-doors-0932 (FX24) | PASS | 98768969 |
| claude/tray-seat-0932 (FX24) | PASS | 5892511c |
| claude/comet (FX25; includes sound-comet and event-swap) | PASS | 157d1cfb |
| claude/inspection fix (FX20b) | PASS | e45b7fe (0.93.2); 1872153 PASS for 0.93.3 |
| claude/storm-sat (FX26) | moved to RV19 after my first look | |
Nothing open. Comet shoulds for whoever next builds the comet (in review-rv18.md): the bedtime arrow hides the arrow to
Saruth at 22:02; one present speaker repeats one line every 4 minutes.

## How I test (and what bit me)
- Setup as plans/testing-guide.md 2.0; worktrees per sha under /tmp/rv18/; a switched-on copy by `sed` on the switch line.
- **At most 2 browser checks at once** on 4 cores. With 4-5, interactions_check and join_check time out (page load 30 s).
- Background commands stop at 2 hours, including time spent waiting in a queue: start a long run when the machine is free.
- Never edit a running queue script (bash keeps reading the old file); kill with a bracket pattern (`pgrep -f "[q]ueue5"`).
- fridays_check hangs in this container (no output, even on 0.93.1); CR6 runs it for us.
- Probing events: the crew only walk while frames run, so jumping the clock with setShipNow makes hosts look absent. For
  anything about who is where, play in real time (probes step continuously).
- Probes (in /tmp, not the repo): play.py (traditions: the host's tap, card, activity, bubbles, close line), comet_real.py,
  doors.py, seat.py, stormsat.py, stage.py, speech.py; RV19's plans/rv19-probe-inspect.py on claude/review-rv19.

## Open questions for the user
None from me.
