# Review: claude/device 459c534 (0.35.20-0.35.22), reviewer 2

**Verdict: PASS WITH FIXES** (all low; nothing blocks combining). Base: ship-integration 0.41.10. I read the diff;
I didn't re-run device_check.
Fine: every new call into another section is wrapped in typeof and try (deviceLocked, deviceLockedTap, seasonOf,
SETTLE, introEnd, introOn, movedOff, movedOn, repView, keepsakes). There is only one way to open the device
(deviceShow), and the lock guards it. `booted` is saved through SHIP.device with a strict `=== true` on load. The
Record shows reputation in words only. No R(), no per-frame cost beyond one guarded call in deviceTick. The mail badge
and light are off while the device is locked.

1. LOW: "I know my way around" can end the welcome with a single tap. `settleSure` is a module-level flag that is
   never reset when you leave the app. Tap it once, close the device; any later single tap on that button calls
   `introEnd(false)`, which ends the welcome week for good. Reset `settleSure` when the Settling-in view closes, or
   when the device opens.
2. LOW: one bad keepsake blanks the whole Wallet. `k.what.charAt(0)` throws if a keepsake has no `what`. The throw
   happens inside `view`, so deviceView shows "(this app failed to draw)" in place of your credits and locker too.
   Use `String(k.what || 'a keepsake')`. The same goes for `movedOn()` rows (`x.name`, `x.day` unguarded: you'd
   get "undefined"). Agree both shapes with social A.

## Addendum: 89ab0ca (0.35.23, deviceChoose): PASS WITH FIXES (low-medium)
deviceChoose shares the meeting panel (deviceDialogue / devDlgTap) with section 18's meetings, and nothing stops the
two overlapping:
- **A meeting starts while a question is open:** section 18's dialogueDraw calls `deviceDialogue(v)` with no onTap.
  That replaces the question and sets devDlgTap to null, but `DEV.choose` stays set. The question's onPick then never
  fires, and the meeting's × now takes the `DEV.choose` branch (`devChosen(-1)`). That hides the panel without
  calling `dialogueClose()`, so the meeting stays active with no panel.
- **A question opens during a meeting:** it replaces the meeting's panel. Answering it calls
  `DEVICE_SKIN.dialogue(null)`, so the meeting carries on invisibly until its next draw.
- Fix: deviceChoose returns false (or waits) while DIALOGUE / a panel is up, and deviceDialogue(v) with a new view
  cancels a pending question first (`if (DEV.choose) devChosen(-1)`). The New game choice at game start is the likely
  first caller, and the arrival evening's scripted meetings are the likely overlap.

## Addendum: 8b502d4 (0.35.24): the two 459c534 fixes PASS
- settleSure resets when you leave Settling in, and on device close; keepsake and "Left the Wren" rows are guarded.
- Tiny: `isFinite(null)` is true, so a keepsake or leaver with `day: null` reads "Day null". Use `Number.isFinite`.
- **Still open: the 89ab0ca deviceChoose / meeting-panel overlap** (addendum above). 0.35.24 doesn't touch it, and the
  device engineer's handover says they're ready to retire, so the lead should give it to the next device owner.

## Addendum: edb320a (0.35.25): the 89ab0ca panel overlap PASS
- deviceChoose refuses while #devDlg is shown (the skin uses `hidden`, so the check is real), while a section 18
  DIALOGUE is up, or while a question is already pending. `DEV.choose` is now set *after* deviceDialogue draws, so
  deviceDialogue's new "cancel a pending question" step can't cancel the question being opened.
- A meeting drawn over a question calls the question's onPick(-1) and leaves the panel and close path to section 18.
  Both orders are covered by device_check.
- Still cosmetic: `isFinite(k.day)` / `isFinite(x.day)` (2 places) should be `Number.isFinite`, or day: null shows
  "Day null". It doesn't block.
