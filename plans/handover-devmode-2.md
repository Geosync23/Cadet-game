# Handover: Dev mode, Stop 1b and Stop 2 (DB2, the Dev mode engineer)

From DB2 (session_01RAw82oHw329cHYC7wapKu8), 2026-10-21, for the next Dev mode engineer (Stop 3, Big events, or fixes from the Stop 2 review).
Read DB1's note first for Stop 1a (`plans/handover-patch-e2.md` on claude/devmode), then this.

## Role, branch, builds
- **Branch:** `claude/devmode-2`, made from `claude/integration` 0.64.8 (3a48846). Integration hadn't moved while I worked: merge it in at the start of your first turn.
- **Commits:** D5 d2612749 (Traditions), D6a b97b5565 (Set career core), D6b 39b2acd8 (friends, beats, progress), D7 (Career tab: see `git log`).
- **Build number:** untouched (the build master sets it). Build-table rows: "Dev mode Stop 1b and Stop 2" section at the end of `plans/build-table.md`.
- **People:** lead 24 (session_01SDe7z5Nr7u69uH1k4sjZ8r; lead 23 handed over). Turn reviewer PR7 (session_01LyKAVtCEedL1bP73vqzu9v), also stand-in owner for sections 21 and 24/24p. Section 18's hook: PR6 (session_01LVHLJHrAR5iGJFS7HK9E7i).
- **The user's ask:** "Let's do up to Stop 2" (2026-10-21 ~11:55). Stop 3 (Big events) is not asked for yet.

## What I built (all in section 25's slot, behind `DEVMODE`; plans/devmode-plan.html v3.1)
- **D5 Traditions tab:** search every `SHIP_TRADITIONS` entry; a card (usual rhythm, time, room, next day); start In 20 minutes / At its usual time / Tomorrow, with "Its Mail now"; whose for birthdays and rotation teas (up to six). A start is `DM_ST.tr` `{ id, day, from, who? }`, saved in `save.dev.tr`.
  - **Section 18 hook (the only edit outside section 25):** the end of `eventsOn`, before `EV_DAYS.set`: `if (DEVMODE) devmodeTradsOn(d, out);`. It adds the Dev starts (own length, `dev: true`), drops that day's calendar showing of the same id and any calendar tradition in the same room at the same time (`devmodeTradClash`, `evRooms`).
  - `devmodeTradsAgain(d)` clears EV_DAYS, EV_GOERS, TALLY_MEMO, SHIP_DAYS (today to d+1), then `deckCrewFill()`.
  - Refused: Day 0, a big event's day, past 23:30, a usual time gone, a room another Dev start holds.
- **D6a/D6b Set career tab:** `devmodeCareerSteps(n, beat)` (a generator, a day per step):
  - New Dev game (`INTRO_BOOT = false`, `newGameStart(false)`, `introSkip()`; Day 0 by shuttle). `careerInit()` + `SHIP.career.gs = DM_SEED` (8: no sick day before Day 46).
  - `devmodeWeekMet(landing)`: section 21's records for the first week's beats.
  - Skip to 05:00 each day; there `devmodeCareerSet(d)` writes `SHIP.works` from `DM_CAREER` via the pure `devmodeCareerFor(d)` (the state by the END of day d).
  - At the end: `devmodeFriends(n)` (`DM_FRIENDS` through `relAdd(id, 'intro:dev', pts)`), `promoPip()`, wake beside your bed (`devmodeWake`) or at the beat's room.
  - `DM_BEATS`: Day 9 test job (08:50, Works bay, test pending) and Day 10 promotion (10:50, the summons at 11:00).
  - The panel steps the generator with setTimeout under the fade and `DM_HOLD`, showing "Setting career: Day 4 of 10…". `devmodeSetCareerTo` runs it at once (used by devmode_check).
  - "What's set" (`devmodeWhatsSet`), `save.dev.set = { day, at, beat? }`; the foot says "Career set to Day N, approximate".
- **D7 Career tab:** the career shown; by hand xp ±5, next band, next training, give a tool, rank Junior/Officer.
  - The test's needs with ticks; Open the test now (`W.test` for today + section 24's `ladderOpen`); Next step (`promoPlan`'s beats).
- `devmodeSay` scrolls the sheet's body to the top (messages always in view).

## Decisions taken (lead 23 agreed 1-5 at ~11:58; one change)
1. Flag traditions: shown once, flag NOT set.
2. **Changed after the agreement, then agreed by lead 24:** a calendar tradition in the same room gives way to a Dev start; only a clash with another Dev start is refused (the room rule is wide, so refusing blocked most evening starts).
3. A start keeps its own length; refused past 23:30.
4. No special rows for the storm, Fridays or rotations: Set career runs the game's own catch-up through them, and "What's set" says so.
5. A progress line under the fade: done.
6. Friendships (q1): a starting level; always a new Dev game (q2); wake 06:00 in bed, beats go to the beat's time and place (q3).

## Gotchas
- **Load order:** `eventsOn` runs at load, before section 25's `const`s exist, so `devmodeTradsOn`'s path uses function declarations only. A `const` arrow there broke every Dev reload (TDZ).
- **The career seed decides sick days** (`sickDue` uses `SHIP.career.gs`). A fixed Dev seed has to be checked: the first one landed you unwell on Day 12.
- **A Skip-to-Monday game never plays the first week's meetings** (`introOn()` is false). Beats for them need the Day 2 recipe (play Day 0-1, Mark).
- **`devmodeCareerSet` overwrites `W.test` each morning:** beats that need a pending test set it after the loop (`beat.set`).
- The officers' cabin room is named "Spare cabin 4-23" on the deck, so the card shows that name. It's not Dev mode's; not reported yet.
- Playwright in this container: 1.55.0 matches /opt/pw-browsers (1.48 fails with "Old Headless mode").
- cadet_test once showed "ALL IDENTICAL (apart from renderer noise: some pixels 1 level off)"; run alone again, it was exact.
- `devmode_check.py BUILD.html trad set career` runs only those parts.

## How to test
- `python3 devmode_check.py starship-cadet.html` (about 5 minutes; parts off, real, card, store, clock, move, slow, trad, set, career).
- `python3 cadet_test.py OLD NEW` with OLD = 0.64.8: ALL IDENTICAL (nothing runs without #dev).
- events_check and join_check (both OK at D5), then `bash check_fast.sh`.
- Shots: `plans/devmode-2-shots/` (trad-*, set-*, career-* at 390 and 360).

## Loose ends
- The plan names "career_check and mech_check unchanged": they never open #dev, and off is ALL IDENTICAL, so not run separately.
- Stop 2 review/publish: the lead decides who publishes the Dev link build (the build master republished the Dev page for 0.64.8).
- Stop 3 (Big events, D8-D9): not started. It waits for the storm/Line merges into integration. `EVENTS_ON` is false in 0.64.8.

- **PR6's nit, for when the storm/Line merge in:** a Dev start uses the plain `SHIP_TRADITIONS` entry, not a day's dressed copy (EV_DAY_DRESS / evTable on the storm branch; not in 0.64.8). On a dressed day outside a big event's day (the storm's Monday Day 15 Lap with Tomas, the Line's Day 7 rows) a Dev start would replace the dressed version with the plain one. Fix then: take `ev` from `evTable().find(e => e.id === r.id)` in `devmodeTradsOn` (and the tab's card).

## Open questions for the user
None.
