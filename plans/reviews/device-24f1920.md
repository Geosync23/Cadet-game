# Review: device 0.35.39 (c89f00f) and the device_check fix (24f1920)

**Reviewer:** adversarial reviewer 2b. **Verdict: PASS.** Device is clear through 24f1920.

- device_check (24f1920's): **OK**. cadet_test 0.35.38 vs 0.35.39: **ALL IDENTICAL**.
- My HUD sweep, now 22 sizes (adding 640x960, 700x1000, 720x1100, 721x1100, 768x1024) x 130 room names x 730 clocks:
  no button overlap, never over the Device button, and the clock is always one line and never cut. Names cut short
  with "..." (before -> after 0.35.39): 601x900 40 -> 0, 900x760 3 -> 0, 640/700/720 wide 0. Only phones narrower than
  420 px still cut some long cabin names (320: 46, 360: 16, 414: 4), plus 721x1100: 5 (two rows of labelled buttons
  just above the icon cut-off). Expected, LOW, no change asked.
- `hudFit` runs in `updateClock` (each minute) and on resize; it sets a cap (max-width), so a longer room name entered
  between minutes is still capped by the last measure, never over a button. The short clock is now
  `clockText()` with the weekday shortened.
- 24f1920: the heads-up cases count only `appt|` keys. On the merge with ship-events it no longer trips over Late piano.
