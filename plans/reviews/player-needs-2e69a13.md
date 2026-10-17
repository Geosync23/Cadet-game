# Review: claude/player-needs 0.28.48 (2e69a13), Pause

Reviewer 1f, 2026-10-17. Builder: player engineer 5 (session_01SyRmwPxQEVKab6re9UgyrD). Base: 48f66e8 (0.28.47, reviewed by 1e). Behaviour change, so reviewed in depth.

**Verdict: PASS WITH FIXES.** One MEDIUM (a pause eats real-time deadlines) and two LOWs. The fixes are a few lines in `pauseSet(false)` and the card.

## What changed
- A Pause button (`#pauseBtn`) and `pauseSet(on)`. While paused, the main loop skips steering, the walkers, `playerUpdate`, the crew, the crowd, the lift ride, `tickShip`, galley, Works, events, social and the intro, and still draws.
- A full-screen card (`#pauseCard`, z-index 60): a pointerdown anywhere on it resumes.
- Pausing saves the game, and a hidden tab pauses.
- On resume, the POP stamps, `TOAST_AT`, `TEACH_CK` and `DIALOGUE.at` move on by the length of the pause.
- `popupWatch` reads a toast's own stamp (`TOAST_AT`) instead of the DOM class.
- A new tip, `t:pause`.
- cadet_test turns tips off in its comparison runs.

## Checked
- **Nothing ticks the sim outside the guard.**
  - `needWarnTick`/`teachTick`/`popupWatch`, `deviceTick` and `newsTick` all run inside `playerUpdate`.
  - `careerTick`, `shiftTick` and `apptTick` run through `tickShip`, and dialogue auto-advance runs in `eventsTick`.
  - The code still running while paused is visual only: doors, lamps, `shipFeelFrame`, stars, dust, `MOVERS`, steam and the screen.
  - There's no `setInterval` sim.
  - Walkers are paced by `dt`, so they don't jump on resume.
- **No ghost tap on resume.** A deck tap needs a pointerdown on the canvas (`downAt`). The card's pointerdown stops propagation, so the pointerup that follows does nothing. A click that ends on the Pause button lands on `body`, not the button, so it doesn't pause again.
- **Saving.** `saveGame` honours `NOSAVE`, and the extra save on a hidden tab, next to the existing one, is harmless. `PAUSE` isn't saved, so a reload starts unpaused, which is right.
- **Layers.** Nothing else in the build is above z-index 60. The career end card shares 60 and is fine either way.
- **Determinism.** Paused frames don't advance ship time, and `R()` isn't touched.
- **player_check on 2e69a13:** see below.

## Findings
**MEDIUM: a pause (or switching apps on a phone) eats real-time deadlines that aren't moved on resume.** `pauseSet(false)` moves the POP/toast/tip/dialogue stamps, but not:
- `VISIT.until` (a crew member knocking at your bunk, 25 real seconds), checked in `socialVisit`;
- `SEEK.until` (someone waving you over, `SEEK_SECS` 25 s), checked in `socialSeek`. It's also how career and first-week asks (`socialSeekAsk`) reach you.

So if you pause, or your phone hides the tab, while someone knocks or waves, they give up the moment you resume. **Probe** (`player-needs-2e69a13-pause-probe.py`): a knock with no pause is still waiting after 3 s; paused for 30 s it's still up; 3 s after resuming → `"Another time, then." They head off.` and `VISIT` is gone. A once-only wave (a career "worried" ask, say) is lost the same way.
**Fix:** in `pauseSet(false)`, also do `if (SEEK && isFinite(SEEK.until)) SEEK.until += d; if (VISIT && isFinite(VISIT.until)) VISIT.until += d;`. Any of these left at -1e9 should stay as it is. For completeness, also move section 21's `INTRO_UI.pilotAt` / `callAt` / `next` the same way. On their own they only make the pilot's line and the tour call come early, so they're LOW. Ideally, move every `performance.now()` deadline in one place.

**LOW (accessibility):** the card's Resume button has no handler of its own; only the card's `pointerdown` resumes. A keyboard user who tabs to Resume and presses Enter gets nothing, and focus isn't moved into the card (it's `role="dialog"`). The Pause button still works from the keyboard, so you're not stuck. Fix: give Resume an `onclick` that resumes, and focus it on pausing.

**LOW:** while paused, keyboard focus can still reach the HUD buttons under the card (Tab + Enter on the device button or Walls), so you can change things while "paused". Fix: make the rest of the page `inert` while paused, or ignore HUD clicks when `PAUSE.on`.

## player_check
PLAYER CHECK OK on 2e69a13 (reviewer 1f), no page errors. The pause lines: paused, the overlay shows and time, needs and position stand still; resumed, time runs and the tip gap moved on by the pause.
