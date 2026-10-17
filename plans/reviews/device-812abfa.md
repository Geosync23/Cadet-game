# Review: device 0.35.36 (812abfa), the HUD fix

**Reviewer:** adversarial reviewer 2b. **Verdict: PASS.** Both MUST-FIXes from device-e5d7227.md are fixed. Three LOW notes.

## Tests
- device_check (812abfa's, with the new 17-size sweep): **OK**, "HUD sweep (sizes with a problem): none".
- cadet_test 0.35.35 vs 0.35.36: differences only inside the HUD text (x 21 to 159, y 15 to 75, at most 6 levels:
  the text now clips and ends in "..."), every shot. Explained.
- **My own sweep** (not the author's): 17 sizes (320x568, 340x640, 360, 375, 390, 414, 600x900, 601x375, 601x900,
  667x375, 740x360, 844x390, 900x420, 900x760, 1024x600, 1280x800, 1920x1080). At each size I tried all 130 room names
  and the clock on all 365 days at 06:00 and 23:59, through `updateClock()`. Result: **no name runs under a button, the
  HUD never reaches the Device button, and the clock is always one line and never cut** at any size. The short weekday
  is used at 320 (700 of 730 clocks), 340 (256) and 601x900 (692); never at 360 and up, nor on any landscape phone.

## Findings (all LOW)
1. **Between 601 px and about 700 px wide on a tall screen** (a narrow desktop window or a small tablet in portrait),
   the labelled buttons wrap to two rows and the HUD is capped at about 154 px: 40 room names end in "...", and the
   clock always uses the short weekday. The icon buttons would leave far more room there; consider widening the
   icon-button query (to about 720 px).
2. **At 900x760 the cap (244 px) is narrower than the space** (the buttons start at 307 px): 3 long cabin names are
   cut when they would fit. Cosmetic.
3. **The short clock is built by hand** in updateClock, not from `clockText()`. If another seat ever changes
   clockText (a season tag, the arrival evening), the short form won't follow. Building it from the same parts, or
   replacing only the weekday in `clockText()`'s result, would keep them together.
