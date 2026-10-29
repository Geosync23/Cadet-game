# Handover: DM1, the Dev mode engineer (2026-10-28)

For a fresh session taking over the Dev mode update (plan v4.4). Read this first, then DEV_NOTES "Dev mode" (the "Jump to (plan v4.4, J0, ...)" bullets and J1, J3, J4 under it) and `plans/devmode-plan.html` (v4.4, on claude/devmode-plan-2; published at https://claude.ai/artifact/X2GVBU4c5hZdt1R3dNxqy4 with the user's answers).

## Role and branches
- Seat: the Dev mode engineer (section 25 of starship-cadet.html, its slot; owner in plans/owners.md). Lead 43 (session_01GKuymjoDoY2kA9yCK12NG1) hires and gives GO; RV24 (session_01GKuymnJuoJTWnmYunbN7EP) reviews each turn.
- **Trunk: `claude/devmode-j0`.** Passed J turns are merged into it by the Dev mode engineer (a fast-forward when possible; otherwise a merge plus the test-only proof: devmode_check all, dev_arrow_check, cadet identical). BM20 takes the whole update into staging after the 0.96.0 round. The build-number lines are the build master's: never touch them.
- Plan: `claude/devmode-plan-2` (v4.4; v3.1 kept as plans/devmode-plan-v3.1.*). The old `claude/devmode-plan` holds an earlier draft over DP1's history: leave it.

## The turns
| Turn | Branch | Build row | State |
|---|---|---|---|
| J0 groundwork | claude/devmode-j0 eef5b56 | 0.95.0-dm.1 | RV24 PASS, the trunk |
| J1 Career and Nights jumps | claude/devmode-j1 d9b7b3c | 0.95.0-dm.2 | RV24 PASS, merged (trunk = d9b7b3c) |
| J3 the ending, answers row, Its next showing | claude/devmode-j3 2b88ad2 | 0.95.0-dm.3 | RV24 PASS, merged (trunk = 2b88ad2) |
| J4 the arrow's later sources | claude/devmode-j4 (the trunk with J3 merged in) | 0.95.0-dm.4 | to RV25 (session_01GKuymnnpKvNH4Ki69KEzwG, RV24's successor); on PASS fast-forward the trunk to it |
| J2 ship events | not started | | waits for the Diplomatic visit to be really on (below) |
| J5 notes, full round | not started | | after J2 |

J4 already has J3 merged in (the only clash was DEV_NOTES, both notes kept). J4 also moved the goodbye jump to 09:16 (RV24's note on J3).

## What each turn built (details in DEV_NOTES)
- **J0:** Jump to tab (DM_JUMPS, `devmodeJump({ id, group, label, day, at, by?, where?, set?, ans?, stops?, slow?, on? })`), the runner with stops (`devmodeAnsStops`, `devmodeRunTo`), `DM_UI.ans` (cq, offer), plain Set career says Stay past Day 32, the table only adds and stops after its last day (F1, DM1-1), `devmodeCareerFor(n, slow)`, DM_MAXDAY 40, DM_JUMPMAX 45, By rank, Senior/Specialist by hand, progress in place + Stop, tabs four to a row, empty blocks J1-J4, DV_MORE. devmode_check `jumps`.
- **J1:** 12 jumps (ps, t3, t3res, t3bar (pauses at 10:00), t3toast, m19, m18, m20, m21, n1-n3); Engine Specialist Steady by Day 26. devmode_check `beats`.
- **J3:** answers row (DM_JUMP_DRAW.ending), 7 ending jumps (endOffer, endOpen, endAddress, endBye, endPage, endStay, endSlow), `devmodeTradNextGo`. devmode_check `ending1`, `ending2`.
- **J4:** DV_MORE sources night, m21 (first), mtcq, end, event; `dvRoomKey`. dev_arrow_check `s6`, `ev`, `end`.

## J2 (ship events), to build
- Group 'events' rows in J2's block: the Line (Day 6 Mail 17:55, Day 7 oath ~14:25, the supper ~17:55), the ion storm (Day 11 briefing (a meeting at 14:00 in the Works bay, seen by J4's `ev`), Day 12 front 13:55, Day 13 05:55, storm Saturday, Day 14 all-clear 09:55, the lantern supper), the Diplomatic visit (Days 16-19: memo 08:25, the Veyli aboard Day 17 09:55 shuttle bay, the guests' day, the formal dinner Day 18 evening, gifts Day 19 08:15, farewell 08:55), the comet (Day 22 21:25, 22:35), the Veyli vessel (Day 27 07:55, Day 28 09:25, Day 29 test fit and 17:35, Day 30 09:10), the crossing back (Day 31 07:55, Day 34 09:55, Day 35 14:25), plus the Short Friday 15:20 and the Friday address (Day 5 15:50, the rec deck auditorium) and the first rotation (Day 21). Read each time from the event's own phases/meetings/moments (getters), as J1/J3 do.
- The running-event card through `DM_JUMP_HEAD`: Next phase (the clock to the next phase's minute), threads − and + (`eventScore`; greyed once `e.mine.settled`), its meeting (Take me to its room), End and keep (`eventFinish(e, def, shipNow())` then `devmodeTradsAgain(today)`-style replanning). End and undo is cut (the user's q8).
- **The visit is still `draft: true`** in SHIP_EVENTS.diplomatic on staging (the swap block never clears it; evCalPlan passes drafts over): it doesn't run. Lead 43 took it to the events side (EV1). Its jumps' `on` should check `!SHIP_EVENTS.diplomatic.draft`.
- Checks: devmode_check `events1`, `events2` (stubs now).

## Gotchas
- **Determinism within a page:** the first run in a page differs from later ones (backlog DM1-3) and the clock log survives a New game (DM1-2). Compare saves in fresh browsers.
- **Excused days move beats:** a skip past 12:30 with you not clocked in excuses the workday (devmodeSkipTo), which can move a beat (the Tier 3 result went to Day 17). Use a stop before 12:30 (J1's t3bar) when a jump lands after 12:30 on a beat day.
- **Beats that need you up:** some asks run on play-only minute ticks (Power safety's). A jump lands before them and the game asks once you play; checks play frames (50 frames a ship minute).
- **The first week's meetings** don't run after the Skip-to-Monday start: no jump (the recipe stays).
- **Shell:** set the scratch variable outside a backgrounded subshell (a stray `/j0_arrow.log` at the disk root came from that; the safety check refused to delete it: the user may remove it).
- Runs: Set career to Day 36 about 10-15 s headless (65 s at 4x slowdown per CA1).

## How to test
`CADET_WORK=/tmp/work-a CADET_CHROME=/opt/pw-browsers/chromium python3 devmode_check.py BUILD.html [parts]` (all parts ~20 min), `dev_arrow_check.py` (~8 min), `cadet_test.py base.html BUILD.html` (base = staging e158dcf), then `bash check_fast.sh`. Two browser checks at once at most, each in its own CADET_WORK (setup in plans/testing-guide.md 2).

## Open for the user / lead
- The visit switch-on (events side).
- J2's builder, then J5 (DEV_NOTES/design-doc final words, the full round on six runners).
