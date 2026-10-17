# Review: claude/deck-plans-1-2-6 d53cf40 (0.16.15: kin, lost and hobbyNoun, data only)

Reviewer 1c, 2026-10-17. Diff: `git diff 4613d43 d53cf40`. Section 9's generated block, `plans/crew-roster-gen.py`, the roster page, DEV_NOTES and the crew designer's handover note.

**Verdict: PASS WITH FIXES** (one should-fix in the data, for the talent theme; nothing blocks merging).

## What I checked
- **Regenerates byte-identical:** `python3 plans/crew-roster-gen.py` on d53cf40 leaves `git status` clean.
- **Nothing else moved:** every roster table (`HABITS`, `ROSTER`, `ROSTER_GUESTS`, `ROSTER_PLAYER`, `GUEST_TEMPLATES`, `GUESTS`, `ROSTER_RESERVE`, `ROSTER_ROTATIONS`) is the same as 4613d43's once `kin`, `lost` and `hobbyNoun` are taken out. All 74 crew, Saruth and the 12 reserve have the three fields (87 people).
- **cadet_test 4613d43 vs d53cf40:** 14 of 15 shots identical. `f_noshadow` differs only by a "+69 Energy" need note caught at a different point of its fade (a real-time timer the test doesn't control); the code that draws it is the same in both builds, so it's not this change. Nothing else in the game reads the new fields yet.
- **kin:** every `family` theme person has one, and it matches their about lines (Ferreira's "my mum" fits "Her mother has been ill"). Partners and the dead are never kin. "" for Sato, Holt, Calder, Brennan, Oduya and Saruth.
- **lost:** set for exactly the nine `loss` theme people (Oduya "my wife"; the eight with "Lost someone close" get grandad x6, best friend x2, uncle x1). Nobody's lost is anyone their other lines treat as alive.
- **The readers agree on the format:** social A's `socialFill` (0.36.68) and dialogue's `LINE_ROSTER_FILL` (0.43.24) both treat "" as missing; head writer 3's `family`, `loss` and `talent` beats list them in `needs:`.

## SHOULD FIX (medium): three of the six talent-theme crew get a hobbyNoun the talent lines don't fit
`hobbyNoun` is only read by the `talent` theme today (content a6dd44c). Those beats read as a skill you make or perform and can teach: "Oh! You caught me. I do a bit of {hobbyNoun}. When nobody's looking.", "I've done {hobbyNoun} since I was small. Nobody aboard's ever seen it.", "A little show in the common room", "Me, teaching {hobbyNoun}. Imagine.", "I made it for you."

| Talent person | hobby | hobbyNoun | How it reads |
| --- | --- | --- | --- |
| quist-ilse | reading mystery novels | reading | "Me, teaching reading." (sounds like teaching someone to read); "I do a bit of reading when nobody's looking" |
| jovanovic-petra | playing Tiles | Tiles | "Nobody aboard's ever seen it": Tiles is played in the common room every evening (Rina keeps count) |
| juarez-nell | collecting mission patches | collecting | "I've done collecting since I was small", "Me, teaching collecting" |
| ibarra-rafael, silva-bea, amadi-asha | crosswords, tea tasting, stargazing | | fine |

This is the same bug reviewer 2 found ("Me, teaching reading mystery novels"), now one word shorter.

**Fix (generator only, no random draws, nobody else moves):** give the talent-theme crew a hobby that is a craft or a performance, by hand, and assert it:
- e.g. `HOBBY_HAND` (or a small `TALENT_HOBBY` applied in `hobby_since`) for quist-ilse "writing mystery stories" (noun "story writing"), jovanovic-petra "carving Tiles sets" ("carving") or "playing the fiddle" ("fiddle"), juarez-nell "sewing mission patches" ("patch sewing"). The writers' choice of words, of course;
- in `kin_lost`, `assert e['thread'] != 'talent' or e['hobbyNoun'] not in ('reading', 'collecting', 'Tiles', 'recording')` (or a positive list of making/performing nouns), so a regenerated roster can't put it back.
Their `hobby` changes too, which is fine: only `{hobby}` in moments reads it, and a craft reads well there.

## Low
- `HOBBY_NOUN` has three keys written twice ('growing cuttings', 'recording messages for home', 'doing crosswords in the bow lounge'). Same values, so harmless; drop the repeats.
- 'recording' (from "recording messages for home") reads as music recording, and bare 'collecting' is odd for anyone; neither is read today (no talent person has them), but the next theme that uses `{hobbyNoun}` will meet them. "message recording" / "souvenir hunting" / "patch collecting" / "music boxes" would be safer.
- Loss variety: six of nine loss people lost "my grandad". Fine for now; if the writers add more loss lines, a fourth `LOST_OF` choice (say "my aunt" where the aunt isn't their kin) would spread it.

## For head writer 3 (content, not this seat)
- The loss beat "It's the day we lost {lost}. Years ago now. I was younger than you." doesn't fit Oduya, the only senior with `lost` (a counsellor who lost his wife as an adult). Either a line without the age, or `needs: lost` plus a cadet-only gate on that beat.
