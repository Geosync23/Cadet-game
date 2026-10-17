# Review: traditions 0.34.42 to 0.34.44 (0c40589, 234a454, 2951e5b)

Reviewer 2, 2026-10-17. Diff against f78dd03. **Verdict: PASS WITH FIXES.** Two small fixes.

Checked:
- events_check on 2951e5b: rc 0. Every rotation, days 35 to 245, gets a farewell supper (the day before) and a new hand's tea (the first Friday after). The honorees are right and 10 to 35 people come. upcomingTraditions gives a deck for every entry and a room key where there is one room (19 of 21).
- Keys 483 and 484 are inside traditions' 434 to 499 (jitter 583 and 584 are inside 534 to 599); no baked k repeats.
- `evRotation` is pure. Reading ROSTER_ROTATIONS too early (it loads later) is caught and gives null. Nothing plans before the roster exists, since schedPeople needs ROSTER, so no day gets cached without its rotation.
- trad_parse: `rotation -7..+7` or `rotation <weekday>`, with the range checked.
- Content: no romance, no serious lines, names come from the rotation. The tone is gentle ("never sad for long").

## Fix 1 (MEDIUM, every combined build with device 0.35.30): two notices for each occasion
0.34.44 turns off section 18's own 15-minute toast only `if typeof apptAdd === 'function'`, and **no section defines apptAdd**. Device 0.35.30 reads SHIP.occasions itself (devOccasions) and shows its own heads-up 15 minutes before, by default. So the Captain's table and the progress talk each give a toast **and** a heads-up strip at the same moment. Fix: test `typeof devOccasions === 'function'` (or both).

## Fix 2 (LOW-MEDIUM, player-facing text): verbs and {first} with several honorees
Rotations have 1 to 3 leavers (day 77: Signe Moreau and Luca Alvarez; day 161: three).
- The farewell Mail reads "{names} leaves the Wren on Sunday's shuttle", which gives "Quinn Zamora, Davi Keane and Vera Ueda leaves the Wren".
- `{first}` lines name only the first leaver: "Save a seat for {first}. It's still theirs tonight." on a three-person farewell; "New hand's tea for {first} tonight" with two arrivals.
- Either word the Mail with no verb agreement ("Leaving on Sunday's shuttle: {names}.") or add a plural line set. A `{first}` that becomes "everyone" when there are several honorees would also do.

Low:
- Both .trad files still open with "DRAFT (not baked ...)" comments, and the welcome tea's comment promises a Works-corner mug for Works arrivals that isn't built.
- "honoree always" doesn't always attend: day 244 Lars Achterberg, day 250 Jem Castellano (events_check passes, because it counts others). Worth a look: if they are off shift and aboard, the honoree should be there.
