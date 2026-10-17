# Review: claude/deck-plans-1-2-6 f7a18d2 (0.16.12, crew designer, Pillar 4 seat 9)

Reviewer 1, 2026-10-17. Diff: `git diff origin/claude/ship-integration...origin/claude/deck-plans-1-2-6`. In the game file only the generated ROSTER block (plus the build line), and the generator and the roster page: in seat.

**Verdict: PASS WITH FIXES.** The roster itself is sound. The fixes are contracts with the social seats, settled now so nothing is lost silently later.

## Checked, fine
- **The generator is deterministic:** re-running `plans/crew-roster-gen.py` on the branch gives a byte-identical game file and roster page.
- **"Nothing else moved":** comparing every roster entry with 0.41.10, the only field that changed (apart from the new ones) is `rota.offDays`, on 52 people; ids and order are unchanged. Torres is off [3, 4] (Thu-Fri), Calder and Halloran [5, 6] (Sat-Sun). Everyone has exactly two days off in a row; 24 of the 59 on the day shift are off at the weekend. Every department and shift with two or more people has someone on every day.
- **day_check passes** on day 1 (Monday) and day 6 (Saturday): nobody stuck, no short shifts, plans the same twice, draw calls peak 268 (budget 450).
- **The reserve:** 12 people, no id or seed shared with the roster, rotation days 35, 77, ..., 245 all Sundays, none in the first four weeks. Couples are mutual. `about` topics (work, hobby, home, secret, past) match social B's `KNOW_SECTIONS`.
- **Combined with social A 3d266bf:** it merges cleanly (only the build line), name_check is OK, and social_check runs with 86 crew with no errors. Its only failure is social A's own test-order bug, which happens without this branch too. The social part of the save grows from 6.7 to 12.3 kB (limit 20).

## 1. SHOULD FIX (agree with social B): the struggle theme ids don't match
- The roster writes `thread` as `notgood`, `startover` and `arc:<id>`. Social B's 20c (`VOICE_THEMES`) uses `notEnough` and `starting`, and the plain id for story arcs (`thread: arc || theme`). When the moments engine (B3) looks up `MOMENT_THEMES[thread]`, 14 people (`notgood` 10, `startover` 4) and all 10 story-arc crew (`arc:tomas` and so on) find nothing, so their moments never open, with no error.
- Fix: one frozen list, written once in DEV_NOTES and used by both seats and the writers' file names. Either the generator writes `notEnough` / `starting` and the bare arc id, or 20c accepts these spellings.

## 2. SHOULD FIX (social A and the sim; this branch makes it real): leavers never leave on the social side
- Every crew member has `aboard: null`, and the reserve has `[day, null]`; "the sim picks who leaves, 10 days ahead". But section 20's `socAboard` only asks section 14's `aboard(p, d)` when the roster's `p.aboard` is set (`... || !p.aboard || aboard(p, d)`), and `leavingSoon`, `socTransfers` and the farewell all read `p.aboard[1]` from the roster. So whoever the sim picks to leave stays aboard for social: no "transferring" news, no goodbye, no farewell, still in the Crew app.
- Fix: social A always asks `aboard(p, d)` when section 14 has it, and gets leaving days from the sim (e.g. `crewLeaving(p) -> day | null` from `SHIP.crew`), never by changing the roster's data. Agree the shape with the sim engineer and add it to the hook register.

## 3. Low: 12 people love only things you can't give
- For 12 crew, every loved tag is `music` or `game` (Marrow, Vance, Ferreira, Mensah, Isak Lindqvist, Olu Farouk, ...), and social A's gift list (`SOC_GIFTS`) has nothing tagged `music` or `game`, so they can never get a loved gift. Either social A adds an item or two (sheet music, a deck of cards), or the generator makes sure each person's loves include at least one giftable tag. Tell social A which.

## 4. Low: couples rarely share a day off
- The plan says couples "share a day off where rotas allow". One of the four couples shares one. If their departments allow it, line them up. If not, say so in the report.

## Note for the lead
- This branch brings in `ROSTER_RESERVE`, which triggers social A's save-wipe finding (social-3d266bf.md, 4; now a must). Combine them only once social A keeps the id-keyed parts across a crew-list change.
