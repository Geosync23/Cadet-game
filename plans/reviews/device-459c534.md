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
