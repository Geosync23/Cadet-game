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

## Addendum: 0.35.31 (a946f7c) and 0.35.32 (ee3fcdd): PASS
- device_check OK. It covers the heads-up against the needs strip on a phone (moved to 210 to 276, no overlap; 128 on wide). The apptAdd case: the Captain's table becomes an appointment with Marrow in Deck 2 room C, `occ` is set, it reaches section 14's plan (`sched: ['appt']`), there's no Cancel, it's saved, and it's kept after you meet.
- Once only: apptAdd returns the existing appointment for the same `occ`. devOccasions skips booked keys. Older saves whose occasions were never booked still show through devOccasions.
- The host now actually walks to the room through section 14, which wasn't true before. Section 18's `meeting()` only waits for you to be in the room and moves nobody, so nothing pulls the host two ways.
- One notice: with traditions 0.34.45 (the toast is off when deviceApp exists), occasions get only the heads-up strip.
- For 1b's side: a missed summons now counts as a missed appointment with the host in section 20 (that's how appointments already work). Make sure that's wanted for the Captain's ready room.
