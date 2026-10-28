# Handover: CP4 (controller package 4, then fresh-eyes fixes), 2026-10-22

Role: a helper under the lead (lead 26, then 27, 28, 29: session_01A9rNreAGVbsY1HgPucDMA7 now). Each job came from the lead, on its own branch; every branch has a row in plans/build-table.md under its own heading. Nothing here sets build numbers.

## Branches and state (all pushed, all checks run before each push)
| Branch | Base | Tip | What | Review |
|---|---|---|---|---|
| claude/controller-p4 | claude/controller a2c80df6 (+ P1 cff5bab merged) | f904532 | The Controller settings page (plan section 7): rebinding, confirm/back swap, stick swap, dead zone, gentle walk, zoom speed/flip, flick or hold turning, button pictures, menu repeat, vibration hooks; saved as s.pad only when changed | PR9 PASS |
| claude/controller-firstuse | claude/controller 95b6129 | 3f6bb66 | First use needs a press or a firm stick push (0.5 for 0.15 s); a drift never walks, turns or zooms; the touch hand-back listeners from the first use | RV5 PASS on a505b42; 3f6bb66 (listeners) sent to RV5 |
| claude/new-game-settings | claude/integration b9f053ba | 63710eb2 | New game moved from the HUD's "+" into Settings, with an in-page Start over / Keep playing | RV5 PASS |
| claude/bubbles-device | claude/integration b9f053ba | 6261ecc0 | The "would like a word" chip (#seek) and the low-need pop (#needPop) on layer 2, under the device and panels | RV5 PASS |
| claude/bubble-jump | claude/patch-play1-f 7f07d035 | 36f8abf7 | A bubble's layout slide capped by its whole distance (bubble_check's 49.8 px on 0.64.17 -> 41.1) | RV3 PASS |
| claude/fe2-tracked | claude/arrows-c 6610dc7 | 016fc65e | Fresh-eyes batch 2: (24) a Tracked row for tomorrow says "That's tomorrow"; (41) the row the arrow follows is highlighted; (38) the pin sits on the item's middle and a tap on it does the item's tap | RV8 PASS on 251d9788 (24, 41); f59b471e (38) RV8 PASS with FX3's 3b7b13d; 016fc65e (the pin reads a tap on release as the deck does, not on click; RV8's 1-in-9 note) sent to RV8 |

## Names others read
- Controller (section 26): PAD_SET (settings; s.pad saves only the difference), padButtonFor(action), padMarkFamily() (CP3), PAD_REP (menu repeat, CP5), PAD_SET.map { action: button } (CP5's PAD_LAYOUTS use this shape), padBuzz(kind) with kinds pick / done / test (hooks in sections 15 and 15b beside the "You take ..." and "Job done" toasts), PAD_FIRST_USE.
- Section 19: devNewSure / devNewAct (New game's question); section 13: newGameGo().
- Section 15b: TRK_SAID / trkSaid, trkFollowKey(items), ixGoalItem(g), ixGoalTap().

## Loose ends
- RV8's wording note on fe2-tracked: the tomorrow row reads "Tomorrow · ... · That's tomorrow: track it on the day" (tomorrow twice); the writer's call.
- RV5's merge note: claude/controller still has the HUD New game button and its handler; whoever brings new-game-settings into claude/controller takes the integration side (controller_check's sweep skips '#newgame').
- On the arrival evening the device is locked until it's handed over, so New game in Settings can't be reached then (told lead 28).
- backlog CP4-1 (on claude/controller-firstuse): controller_check's tiles part flaky; CP2's 7b11451 fixes the check.

## Gotchas
- Run cadet_test alone: with three checks at once, shots f/g/h differ (the known load effect).
- `pgrep -f name` inside a bash loop matches the loop's own command line; it never ends. Run steps in sequence instead.
- Tests use ?nosave; for a real reload, write the save as saveGame does and page.goto the same file with ?debug only (controller_check part settings, device_check's new-game part).
- The device is locked on the arrival evening (deviceLocked): introFlagSet('intro.device') before opening it in a check.
- elementFromPoint skips pointer-events:none layers (the bubbles): switch them on to test stacking (bubble_check item 5).

## How to test
check_fast before every push; cadet_test alone against the branch's base; plus the area's check: controller_check (parts settings, firstuse), device_check, player_check, bubble_check, interactions_check (the Tracked blocks at the end), plans/build-master/newgame_check.py (copy cadet_test.py next to it to run).
