# Handover: CP1 (controller package 1, panels; merger of claude/controller)

Session: session_015ZhJRKCEditHrVhwdhszYq. Leads in turn: 26, 27, 28, now lead 29 (session_01A9rNreAGVbsY1HgPucDMA7).

## What I own and built
- **P1, panels and menus** (plan section 3; claude/controller-p1, merged as 0.90.3): the panel helper in section 26's slot.
  API for the other packages: `padPanelAdd(sel, { on, before, first, back })`, `padOwn(when, { move, a, b, x, lt, rt, frame })`,
  `padLayer`, `padPanel`, `padItems`, `padFocusTo`, `padStep`, `padPress`, `padBack`, `padScroll`, `PAD_MUST`, `PAD_FOCUS_CSS`,
  `PAD_BUILT` (CTT's package names). Same row/column first in `padNearest`; the highlight kept after a redraw
  (`PAD_FOCUS.last`, by name then place); a touch after the pad blurs the pad's own focus and removes the tabindex it added.
- **Pick fix** (turn 3's ring; claude/controller-pickfix, RV5 PASS, in 0.90.7): the way you face first; a thing found from
  two places (the lift) keeps both.
- **Merger of claude/controller** and its 0.90.x numbers: 0.90.3 P1, 0.90.4 P2, 0.90.5 P3, 0.90.6 P4, 0.90.7 P5 + CP2's
  7b11451 + pick fix, 0.90.8 CP4's firstuse (fda82c1a). Everything still behind `PAD_ON` (off).

## Where things stand (2026-10-22 ~17:10 UTC)
- claude/controller pushed at fda82c1a (0.90.8). Locally (worktree /tmp/claude-0/wt-ctl, branch claude/controller):
  92fb2414 swaps controller_check.py for CTT2's single file (1fa67e9). NOT pushed: waiting for CTT2's full run on 0.90.8
  and its final commit (it made walk/odd/touch fixes after 3fdcdbd); take that final file, re-commit, check_fast, push,
  then RV5 checks the swap.
- Next (lead's plan): once BM13's 0.64.17 round passes, merge claude/integration INTO claude/controller (merge, no
  rebase), usual set, then the six-runner round. Switch-on only on the user's go.

## Merge notes for integration (RV5, lead 28)
- CP4's New game in Settings (claude/new-game-settings 63710eb2) removes #newgame, its CSS and section 13's newBtn
  handler: take integration's side. controller_check's Sweep SKIP {'#newgame'} can go; P5's DEV_NOTES line about New
  game's 4 s tap-again is stale.
- bubbles-device (6261ecc) moves #seek and #needPop to z-index 2: P1's PAD_HUD_SEL reaches #seek; check the outline shows.
- Settings' last line clashes with arrows C: keep both.

## Usual set before every push (read every output in full)
controller_check (all parts), cadet_test no pad vs the previous build with PAD_ON off and on (each run alone; three at
once gave screenshot noise once), check_fast. Setup: pip install playwright; three.js r128 and acorn into
/tmp/cadet-work; CADET_CHROME=/opt/pw-browsers/chromium; a separate CADET_WORK per parallel run.

## Gotchas
- A package's check that stubs another package's function with `window.X = ...` stops working once that package's real
  `const X` is merged (seen with padMarkFamily, PAD_LAYOUTS): use the real setting when it exists.
- P3's one-time "Controller connected" message lands at its own moment: lockstep comparisons must turn it off or ignore it.
- Check changes now go to CTT2 (claude/controller-tests), not straight into claude/controller's copy.
- Merges of packages clash at the end of section 26's slot; when git keeps one shared closing `}` outside, add one
  between the two blocks.
