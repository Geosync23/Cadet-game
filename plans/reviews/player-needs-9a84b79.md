# Review: claude/player-needs 0.28.50 (9a84b79), Pause follow-up

Reviewer 1f, 2026-10-17. Builder: player engineer 6. A re-check of my 0.28.48 review (player-needs-2e69a13.md) and the new frozen clock.

**Verdict: PASS WITH FIXES.** The MEDIUM is fixed. One new LOW; my two earlier LOWs are still open.

## Checked
- **The frozen clock (section 13).**
  - `FREEZE` plus `freezeSync()` runs once a frame and from `pauseSet`. It covers Pause and a game of Tiles (`PAUSE.tiles`).
  - `simNow()` is real time less frozen time, and `simTimeout`/`simClear` are run by the loop only while not frozen.
  - Leaving a freeze calls `pauseShift(d)` for the stamps that stay on real time.
- **The MEDIUM is fixed.** `SEEK.until` and `VISIT.until` are now set and compared on `simNow()` everywhere. So are chatter (`CHATTER_AT`), overheard lines (`OVH_AT`), the intro's call/tour/pilot timers, `FEEL` and `FEEL_S`. The device skin's tip, heads-up and address timers, the Captain's address and the intro's spoken lines now use `simTimeout`. I checked there are no mixed comparisons left (nothing set on `simNow` and read against `performance.now()`).
- **Taps while frozen.** `tap()` returns while frozen, and mid-Tiles it brings the board back. `MOVERS` now stop while frozen too.
- **The frame clock** (`clock.elapsedTime -= dt`) keeps poses and blinks where they stopped.
- **Pause on phones** sits beside the Device button (`pausePlace`, re-placed on resize, by a ResizeObserver and each ship minute), with a 44 px tap target.

## Findings
**LOW (new): the dust motes drift away during a pause or a game of Tiles.** With `t` frozen, the dust loop keeps adding `sin(t·.3 + seed)·.0015` each frame, a constant per mote, so they slide steadily instead of bobbing. Probe (`player-needs-18eedb8-dust-probe.py`, Deck 3): a mote's mean move is 0.10 m over 60 s running, and **2.25 m over 60 s paused**. After a long pause or game they've left the room for good. Fix: skip the DUST loop when `!run` (as `MOVERS` now does), or drive it by `dt`.

**LOW (from 0.28.48, still open):** the card's Resume button has no handler of its own and isn't focused, so keyboard Enter on it does nothing.

**LOW (from 0.28.48, still open):** Tab can reach the HUD buttons under the card while paused.
