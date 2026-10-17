# Handover: the crew designer

Written at the end of Pillar 2 (combined build 0.40.8) and brought up to date in Pillar 4 (0.16.15), so a fresh session can take over the crew.

## The role

- **Branch:** `claude/deck-plans-1-2-6`.
- **Builds:** 0.16.x (0.16.1 to 0.16.15 so far; the next is 0.16.16). The lead merges them onto `claude/ship-integration`.
- **What I own:**
  - section 9 of `starship-cadet.html` (`// 9. CREW DATA`): the generated ROSTER block and the two lines after it;
  - `plans/crew-roster-gen.py`;
  - `plans/crew-roster.html`;
  - my own rows in DEV_NOTES: the build rows 0.16.x and the section "The crew roster (builds 0.16.x, the crew designer)".
- **Before the roster:** I drew the plan pages for Decks 1, 2 and 6, and Deck 2's Sketch 8. Other architects own those pages now.
- **What I don't touch:**
  - `design-doc.md`, `TEAM.md` and the plan files under `plans/` that aren't mine;
  - anyone else's sections, including the `CREW` list of the 8 original walkers, which sits above the ROSTER block in section 9.

## What I built

All 75 crew are fixed data, made by a seeded generator. With you included, that's:
- by rank: 1 Captain, 1 XO, 4 Department Chiefs, 6 Senior Officers, 16 Officers and 47 Juniors;
- by shift: 60 on days and 15 on nights.

Everything sits between the markers `// ---- BEGIN ROSTER` and `// ---- END ROSTER ----` in section 9:

- **`HABITS`:** the shared habit vocabulary, 24 habits, each with one line saying what it does to a day.
  - The first 18 are about the shape of a day (early-riser, tea-break and so on).
  - Six were added for Pillar 2, one room's regulars each: `runner`, `shopper`, `musician`, `gardener`, `bar-regular` and `stargazer`.
  - The sim engineer's section 14 reads them.
- **`ROSTER`:** 74 entries, everyone but you. The fields:
  - `id`, `name`, and the flags `story` and `player`;
  - `rank` (captain | xo | chief | senior | officer | junior), `dept` and `uniform`;
  - `role`;
  - `shift` (day | night), `rota`, `bed` and `work` ({deck, place});
  - `habits`, `traits`, `looks`, `bio`, `life` and `seed`.
  - Notes on these:
    - `uniform` is the makeCharacter department key: command | works | watch | survey | infirmary.
    - `bed` ids look like `4-B<room>-<berth>`, `4-01`..`4-24` (cabins) and `2-<letter>` (Deck 2 rooms).
- **`ROSTER_GUESTS`:** Envoy Saruth (rank `guest`), who is outside the 75.
- **`ROSTER_PLAYER`:** you. You're a Works junior, bed `4-B1-4` (the top berth of the second bunk in Bunk 1, which matches the bunk's text), off Sat and Sun. You aren't scheduled.
- **After the END marker:** `ROSTER_RANK` and `rosterSpec(p)`, which turns an entry into a makeCharacter spec. The crowd (8b) and full rigs (10) use it.

### Shared formats other sections rely on

- **`rota.offDays`:** two days in a row (0 = Monday), staggered within each department so no department is ever empty.
- **`rota.hours`:** optional `[[from, to], ...]` in minutes from midnight. It replaces the shift's hours on work days. Section 14 reads it (schedDesks and planDay). Only the storekeepers have it:
  - Yara Esposito works 08:00–14:30, off Mon and Tue.
  - Orla Ishikawa works 14:30–21:00, off Thu and Fri.
  - They share the one till (`work:store`, Deck 3), hand over at 14:30, and their days off never meet.
- **Galley teams:** the galley engineer's section 16 (`galleyTeam`, `galleyDeputy`) reads these. The hours themselves live only in section 16; don't copy them into the roster.
  - `rota.team` is `chef` | `early` | `late`, and the deputy has `rota.cover: { for: 'brennan', days: [4, 5] }`.
  - The chef is Brennan, off Fri and Sat.
  - The early team is Varga [0,1], Haddad [2,3] and Dlamini [1,2]. Dlamini is the deputy: he cooks on Brennan's days off.
  - The late team is Walsh [5,6] and Madsen [0,1].
  - The generator asserts there's a chef plus at least one early and one late hand every day.
  - Section 16 also still accepts an older `galley: chef|cook|hand` field, but nothing sets it now.
- **The story crew** (Marrow, Vance, Sato, Holt, Pell, Rina, Brennan, Tomas) have looks and bios copied exactly from `CREW` and must stay identical. Section 14 and the crowd rely on their ids.

### Added since (0.16.6 to 0.16.15)

DEV_NOTES' crew roster section has every detail; in short:
- **Birthdays and door plates (0.16.6):** `birthday` (a ship day of the year, 1–364) on everyone; `plate: { rank, name }` on everyone with a cabin.
- **Habit changes (0.16.7):** `habitShifts: [{ add?, drop?, why }]`; the sim's `habitWeek` applies them.
- **Visitors (0.16.8–0.16.10):** `GUESTS` (60: event guests and 52 everyday visitors) and `GUEST_TEMPLATES`, after `ROSTER_PLAYER`; `rosterSpec` returns a plain-clothes guest's own `spec`.
- **Gardeners (0.16.11):** Tove Cruz (senior), Ravi Hart (early) and Imani O'Neill (late), dept `garden`, with `rota.hoursOn` for Tove's cover days.
- **Pillar 4, seat 9 (0.16.12–0.16.13):**
  - varied days off (`days_off`), with fixed days for Torres, Halloran and Calder;
  - the social fields on everyone (`tpl`, `openness`, `needs`, `loves`, `likes`, `joy`, `thread`, `keepsake`, `home`, `family`, `mentors`, 6 or more `about`); thread spellings are frozen with social B;
  - four couples (`partner`, sharing a day off and a `transferTo`);
  - `stays` and `transferTo`;
  - `ROSTER_RESERVE` (12, four cadets, each `replaces` a same-role leaver and copies their bed, work, shift and rota) and `ROSTER_ROTATIONS` (six Sundays, `out` and `in` ids). Leavers have `aboard: [null, day]`.
- **Hobby, since and family "after my" (0.16.14,** for social A and the head writer's moment lines `{hobby}`, `{since}`, `my {family}`):
  - `hobby`: an -ing phrase; `since`: time aboard the Wren, a duration phrase (Tomas "one week"; the reserve counts from arrival: cadets "one week", others "two weeks"). Both on all crew, Saruth and the reserve, added last by `hobby_since()` with no random draws (hand tables `HOBBY_HAND`, `SINCE_HAND`; the rest by rule and `stable(id)`).
  - `family` reads after "my" (no article, no he/she/him/her/they); `hobby_since` asserts it. `FAMILY` holds (about form, my form) pairs: the about templates still say "Has a twin", through `FAMILY_HAS`, so no `about` text moved.
  - A new person needs a `since` that agrees with their bio and about lines; check any "years"/"months"/"New to" wording.
- **Kin, lost and hobbyNoun (0.16.15,** a HIGH from reviewer 2's dialogue review: the theme .arc lines said "the day we lost parents, who run a repair shop"):
  - `kin`: one living relative with "my" ("my gran"), never a partner or anyone dead; "" for Sato, Holt, Calder, Brennan, Oduya, Saruth.
  - `lost`: only where existing text has a death (lead's ruling: no new deaths): Oduya "my wife"; loss-theme crew (secret "Lost someone close") get "my grandad"/"my best friend"/"my uncle", never their kin. "" for the rest.
  - `hobbyNoun`: a bare activity noun ("knitting", "piano", "Tiles") for "a bit of X" / "teaching X"; `hobby` stays the -ing phrase.
  - Added last by `kin_lost`, no random draws. A new hobby phrase needs a `HOBBY_NOUN` entry, a new family phrase a `KIN_OF` entry (the generator fails otherwise).
  - Readers: head writer 3 switches family/loss/talent .arc to {kin}/{lost}/{hobbyNoun} and adds `needs: lost`; social A exposes them in socialFill ("" = missing).

- **Every later pass runs at the end of the generator,** on its own random stream (`NEW_R`, `BDAY_R`, `SHIFT_R`, `VIS_R`, `P4_R`). Keep it that way, so nobody already written moves.

## How to regenerate

```
python3 plans/crew-roster-gen.py
```

- It rewrites the block between the markers in `starship-cadet.html` and writes `plans/crew-roster.html`. Re-running it with no edits gives byte-identical output.
- Check that after a merge: run it and `git status` should show nothing new.
- To change the crew, edit the generator (STORY, NEED, the bed rules, the days-off loop and so on) and re-run. Never hand-edit the block.

### Order matters

The generator draws everything from one seeded stream, `R`, in a fixed order: names, looks, habits, bios and life lines, then beds and days off. Anything that adds or removes a draw from `R`, or changes a list it samples from, reshuffles everyone after that point.

Later changes were made so they move nobody else:
- the player replaces the last Works technician (Kai Lachance) after beds and days off are given out;
- the Bunk 1 swap;
- the Pillar 2 habits use a second stream, `NEW_R`, and a separate `HABITS_P2`;
- the storekeepers and galley teams are applied at the end.

Keep doing it that way. To check, compare ROSTER before and after with a short script: only the entries you meant should differ.

### The roster page

- `plans/crew-roster.html` is grouped by department, with search (names, roles, bios and habits) and a night-shift filter.
- A published preview, for the lead and the user, is at https://claude.ai/artifact/H8h77xpeMD9vewewVvuCgB. To refresh it:
  1. Strip the page's doctype, html, head and body tags.
  2. Add `color-scheme:dark` to `:root`.
  3. Use the title "Wren Crew Roster".
  4. Republish to the same link.

## State at 0.40.8 (updated in the answers pass, 0.16.6)

- **The eight hand-written senior names were approved by the user** (0.16.6, so the `provisional` flag is gone). They're the department heads and seniors added for Pillar 1:
  - Calder (Head of Works);
  - Nandakumar (Head of Infirmary);
  - Kowalczyk (Second Officer);
  - Raman (Senior Helm);
  - Ferreira (Comms Chief);
  - Oduya (Counsellor);
  - Mensah (Senior Watch Officer);
  - Mori (Deputy Survey Chief).
  The lead put the names in design-doc.md. If the user renames anyone, change STORY in the generator and keep the id unless every reader is updated.
- **The spare berth:** `4-B1-6`, the one empty berth on the ship, in your room.
- **Loose ends I'd look at next:**
  - When one storekeeper is off, the store has staff for only half the day. The user said that is fine (no store open every day).
  - Galley hands' habits `skips-breakfast` and `late-diner` do nothing on their working days, because the galley staff eat at fixed times. That's harmless, but they could be swapped for habits that matter.
  - Works lost three juniors (one to you, two to the store). It still has the most people, and the Works bay has 19 places, so that's fine for now. It's worth checking when the job board (B2) needs Works hands.
  - The page shows habits in words from `HABIT_WORDS`. A new habit must be added there too; the generator asserts this.

## Gotchas

- **Test setup in a fresh container:** `pip install playwright`, then fetch three.js as DEV_NOTES "Testing" says (`npm pack three@0.128.0` into `/tmp/cadet-work/three`). cadet_test's f_noshadow can differ once by about 1934 px in the "+69 Energy" note (a timing flake); re-run before chasing it. To run two cadet_tests at once give the second its own `CADET_WORK`.

- `ROSTER_PLAYER` is read by the sleep code (`playerBed()`). Moving your bed moves where Sleep works.
- `uniform` must be a real makeCharacter DEPT key: `store` and `galley` map to `works`.
- `rank` maps to makeCharacter's 0–4 through `ROSTER_RANK`. A new rank needs a row there.
- Changing anyone's days off changes who's where on Monday morning, so the cadet_test crew shots will differ. Even `g_nocrew` differed by about 300 px once, in a Bunk 1 patch, after a days-off change. To prove the cause, make a copy of the base build with only your intended data change, and compare that copy with your build. It should be ALL IDENTICAL.

## How to test

Run each check on its own, about 1–4 minutes each. A fresh container needs `pip install playwright` and three r128 unpacked into /tmp/cadet-work/three (DEV_NOTES "Testing"):

```
CADET_CHROME=/opt/pw-browsers/chromium python3 cadet_test.py BASE.html starship-cadet.html
CADET_CHROME=/opt/pw-browsers/chromium python3 deck_check.py starship-cadet.html
CADET_CHROME=/opt/pw-browsers/chromium python3 day_check.py starship-cadet.html 1      # and 2 when schedules change
```

- The base build is `git show origin/claude/ship-integration:starship-cadet.html`.
- The combined build also has `food_check.py`, `player_check.py` and `machine_check.py`. Run `food_check` if the galley staff change.
- Also run `node --check` on the extracted script after any generator change. A broken block breaks the whole game.

## Ideas and questions for the user

- Loose end from 0.16.14: one reserve arrival, Priya Kowal, has the generated detail "an old rivalry with someone aboard that goes back years" though she is new aboard (from before the Wren, at a stretch). The reserve's `since` is fixed text from arrival; a reader that wants it to grow could work it out from `aboard[0]` instead.

- The user said no to a store open every day (answers pass, row 19).
- Birthdays: built in 0.16.6 (`birthday`, ship day of the year 1–364, about one a week). The galley bakes the cake and the sim engineer gathers the mess.
- Habits that change over time: built in 0.16.7 as `habitShifts` (see DEV_NOTES); the sim engineer's `habitWeek` applies them and owns `SHIP.habitLog`. To add or reword one, edit `SHIFTS_HAND` or the swap/add/drop lists in the generator; keep `why` a whole sentence that names the person.
