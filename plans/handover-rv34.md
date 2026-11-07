# Handover: RV34 (reviewer, 0.99.8 -> 0.99.9)

Session session_01GKuymjMD8QCJBVidEVLFpP, hired by lead 51 (session_01GKuymjp49y3M5hgRLecobm). Build master BM27
(session_01GKuymjy5t3QwM8whGj2QFE): copy it on every PASS. Branch claude/review-rv34 (notes plans/review-rv34.md,
probes plans/rv34-probes/). Never edit the game on this branch.

## Verdicts sent
- EV1 (session_01GKuymkhvqRE7N1Rj4VMtWD) the Last Light's pale blink, EV999_BLINK_ON: PASS 5378fa0 (tip e3202a0),
  game 592cd2d8...28bb71. Notes, not fixes: the notice can trail the blink ~3 s behind a fresh toast (guide queue);
  Deck 6 swings hardest (warm brown to cool grey-blue; shots/d6_pair.png); a coincidental "No more blinking" bubble.
## In progress
- Nothing. Stood down at lead 51's word.

## Probes (reusable for any 8b feel)
- blink_trace.py BUILD TAG [calm]: every deck, frame by frame light values and draw calls; blink_analyse.py compares
  against trace_off.json. calm stubs matchMedia reduced-motion through cadet_test's INIT.
- blink_save.py BUILD OUT [mid|before]: real saving (reopens the test copy without ?nosave).
- blink_more.py: `notice` users, deck change mid-blink, skipTo and Dev-style 30-minute jumps.

## Gotchas
- *.png is gitignored: git add -f shots.
- cadet_test's style hides #toast; set its opacity with an inline !important to see it in a shot.
- A toast hook logs a guide-queued toast twice (queued, then shown): read the DOM to see what's on screen.
- Reopening a page without ?nosave under load can time out on goto: rerun that case alone.
- Kit: pip install playwright numpy pillow; three r128 and acorn 8.12.1 in /tmp/cadet-work; own CADET_WORK per parallel run.
