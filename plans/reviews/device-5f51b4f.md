# Review: device 0.35.29 (5f51b4f): heads-ups before Schedule items start

Reviewer 2, 2026-10-17. Diff against d90d70c (be8e2ab). **Verdict: PASS.**

Checked:
- device_check OK, including the rewritten reminders case and the new heads-ups case. cadet_test against be8e2ab: ALL IDENTICAL, no errors.
- Load and new game: SHIP.device always comes from deviceLoad, so `heard` and `everyday` always exist. `heard` survives a save round trip: keys of 120 characters or more are dropped, and only the last 80 are kept. onSim('newGame') resets it. The old `DEV_REMINDED` (forgotten when you closed the game) is gone, so a reload no longer repeats a reminder.
- Cost: devHeadsTick runs at most once per ship minute (deviceTick's devTickMin guard) and not while you sleep. It runs devDay for two days, which is light.
- Settings args reach `act` as numbers, so `[15,30,60].includes(arg)` works.
- Traditions get Go there on the combined build: ship-events' upcomingTraditions returns deck and room. The device branch on its own shows no button, as in the screenshot.
- Busy: when a device chat card is open, a waiting heads-up holds (`busy` true, not shown), and tips and the address take the top via devHeadsBack.

Low (no fix needed for the combine):
1. A strip already on screen stays up when a chat card opens afterwards, for up to 9 s. Only tips and the address call devHeadsBack. On a phone they don't overlap (strip at y 128 to 194, chat at 621 to 830), so it's cosmetic. A one-line devHeadsBack() in chatShow would match the "never over a chat card" comment.
2. Appointment reminders now follow the one "Heads-ups" switch. Before, the 10-minute appointment toast came whatever the setting. That's a design change, so worth one line in the Settings text or the design doc.
3. Keys include the title. An appointment group that gains a person ("With A" becomes "With A and B") can be announced again. Harmless.

## Addendum: 0.35.30 (2ef3cce): booked occasions in the Schedule

**PASS.** device_check OK, including the new occasions case: the Captain's table heads-up with Go there to Deck 2 room C, chance occasions left out, and kept ones too.
- `devOccasions` matches section 18's record `{ id, key, at, len, deck, room, status }` and `OCCASIONS[id].title/chance` on ship-events 2951e5b. It is wrapped in try and does nothing when section 18 is missing.
- **Watch at combine (it's on the traditions side, see reviews/ship-events-2951e5b.md):** section 18 0.34.44 turns off its own 15-minute toast only when `apptAdd` exists, and no section defines `apptAdd`. In the combined build you'd get both the toast and this strip for each occasion.
