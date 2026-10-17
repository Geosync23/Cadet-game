# Review: device 0.35.33 (dfc1df2) and 0.35.34 (e5d7227), heads-ups and the HUD on phones

**Reviewer:** adversarial reviewer 2b. **Verdict: PASS WITH FIXES** (two MUST-FIX, both in the 0.35.34 CSS).

## Tests
- device_check (e5d7227's): **OK**.
- cadet_test 0.35.32 vs 0.35.34: pixel differences only, no data differences. All explained:
  1. every shot: the HUD's new backing (top left, x 8 to 167, y 8 to 77);
  2. d_wallslow, and i_tap2 to j_steer2: the heads-up strip ("Your shift starts in 15 min") isn't drawn in 0.35.34.
     I logged the state at every shot: `HU_Q` still holds "Your shift" and `devHuBusy()` is true from i_tap2 (the tap
     brings up a card; no dialogue or tip), so the strip waits, as 0.35.33 intends (in 0.35.32 it showed on top of
     the card). It drops out on time (the soon one at the start, the start one 10 minutes later).
- **HUD layout, measured in the browser** at 320x568, 360x640, 375x667, 390x844, 414x896, 600, 601, 667x375, 680, 740x360,
  844x390, 915x412, 900x760: the boxes of the HUD, the clock, every control button and the Device button, with the real
  text, with each of the 130 room names, and with clocks for days 9, 99 and 365 on each weekday.

## What's better
Portrait phones: no room name runs under the buttons any more (before: all 130 at 320 and 375, 40 at 360); long names
end in "..." on one line. The New game "Tap again" toast on narrow phones works.

## Findings
1. **MUST-FIX: on narrow phones the clock wraps onto two lines and the HUD covers the Device button.**
   At 320 wide the clock wraps every day ("Day 1, Monday 06:00" too); the HUD grows to 93 px tall and the Device button
   starts at 86 px, so the backing sits over the top of the button (shot: plans/reviews/device-e5d7227-hud.png, top).
   At 360 it wraps on Wednesdays from day 10 and on Thursdays from day 100; at 375 on Wednesdays from day 100.
   Fix idea: keep the clock on one line (`white-space:nowrap`) and make it fit, e.g. a short weekday ("Wed") or a smaller
   font under about 380 px; or let the Device button sit below the HUD whatever its height. Check: 320 to 600 wide, all
   weekdays, days 1 to 365: one line, and the HUD's bottom above the Device button.
2. **MUST-FIX: landscape phones (601 to about 900 wide) are worse than before.** The new backing adds 22 px of padding,
   but the width cap and the "..." only apply up to 600 px, so long room names run under the labelled buttons:
   names that collide, before vs after: 601: 5 vs 11; 667x375: 9 vs 19; 740x360: 0 vs 2; 844x390: 2 vs 4
   (e.g. "Senior Watch Officer's cabin" under Rotate at 740x360; the same shot, bottom). Fix idea: apply the HUD's
   `max-width` (the space left of the buttons) and the one-line "..." at every width, or also switch to the icon buttons
   for short landscape screens (`(max-height:500px)`).
