# Re-review: claude/social 3d266bf..c9ffe12 (0.36.31-0.36.37 and 9f63e91)

Reviewer 1, 2026-10-17. Everything is in section 20 (plus the build line). name_check across every Pillar 4 branch: **NAMES OK** (`socIntroOn` / `socIntroNote` and `SOC_BOND_KINDS` remove the clashes).

**Verdict: PASS WITH FIXES.** The BLOCK is lifted, and so is the "don't combine with the crew designer" hold for the game code. But social_check itself crashes on the combined build (finding 1), so fix the check before 0.60.0.

## Fixed (checked)
- The name clashes (see above). `socIntroOn` asks section 21's `introOn()` when it exists.
- social_check's order bug: it passes on c9ffe12 alone, `pure: true`.
- A missed step leaves no memory (`if (d.missed) return`).
- **The save keeps progress across a crew-list change, proven for real:** I played a little in c9ffe12 (74 crew) with saves on, then opened social + crew 0.16.12 (86 crew, the real reserve) in the same browser storage. Tomas 30, Pell 16, the `fav.lamp` memory, Tomas-Pell affinity -2 and galley reputation 15 all came through unchanged.

## 1. MUST FIX before 0.60.0: social_check crashes on any build with the real ROSTER_RESERVE
- On a scratch merge with claude/deck-plans-1-2-6 f7a18d2: `TypeError: Cannot read properties of undefined (reading 'dept')` in the reserve test (9f63e91), and the check stops.
- Cause: the test sets `window.ROSTER_RESERVE = [...]`, but the game's own `const ROSTER_RESERVE` (section 9) shadows it, so `socInit` never sees the test person. `SOC.idx.get('reserve-test')` is undefined and `affStart(t, undefined)` throws. On your branch alone (no reserve const) the test works, so it only fails in the combined build, which is the one the gate runs.
- Fix: add the test person to the real array (`ROSTER_RESERVE.push(...)` when it exists, else the window stand-in), and remove it afterwards. Or build the "old" save by dropping one id from `idl` and its pairs, which needs no reserve at all.

## 2. SHOULD FIX (open from the crew designer's review): leavers chosen by the sim never leave socially
- Unchanged: `socAboard` asks section 14's `aboard(p, d)` only when the roster's `p.aboard` is set, and every crew member's is `null`. `leavingSoon`, `socTransfers` and the farewell `eventOneOff` (booked 10 days ahead from `p.aboard[1]`) read only the roster. Agree a call with the sim engineer (e.g. `crewLeaving(p) -> day | null`) and use it everywhere `p.aboard[1]` is read.

## 3. Low: `typeof introOn` in `socIntroOn` is outside the try
- Section 21's `introOn` is a `const` declared after section 20. If anything calls `socGate` / `socIntroOn` while the file is still loading (a load-time `simNote` reaching a social listener, for example), `typeof introOn` throws (temporal dead zone) before the `try`. Nothing does today. Moving the `typeof` inside the `try` costs nothing.

## Checked, fine
- The id-list remap (`idl`) checks lengths before reading; news knowledge is remapped by id or dropped; saves without `idl` keep everything keyed by id and restart affinity only.
- The farewell through `eventOneOff` is wrapped in try; the Sunday test `weekday(...) === 6` is right (Monday is 0). New schedU keys stay inside 644-671. The affinity tuning (clash -24, friend caps) is the designer's call and runs the same twice.
- Social save: 12.1 kB alone, 13.3 kB with the reserve (limit 20).
