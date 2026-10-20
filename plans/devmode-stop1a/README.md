# Dev mode, Stop 1a: the patch kit (D1-D4)

The Dev mode engineer DB1, 2026-10-20, branch `claude/devmode` (from `claude/integration` 5dd740c). For lead 20 to publish for the user. The build number is unchanged (the build master sets it).

## What's in it
- **The Dev link:** the game's link with `#dev` on the end. The place-and-clock card gets a gold outline and the word DEV, and tapping it opens the panel, "Dev mode: not your real game". Without `#dev`, Dev mode doesn't exist in the game.
- **Its own save:** the real game is never written; Copy my real game only reads it.
- **Quick tab:**
  - Take me to: Next appointment, A room… (the deck, then the room), The ladder, The time clock, The job board. The clock doesn't move.
  - This moment: Mark here, Back to mark, Undo my last Dev action, Top up needs, Copy my real game, Clear Dev save (two taps).
- **Clock tab:** Next morning, +1 hour, To a time… (− / + 30 minutes, then Go), To 08:55, To 16:55, To 21:40, +1 day, +7 days, +3 hours. A workday you skip past 12:30 without clocking in is excused, not missed, and your needs are kept.
- **Refusals, with the reason on the panel:**
  - Take me to: during the arrival evening and the escort, and inside a meeting.
  - The clock: during the arrival evening.
  - Anything: during a lift ride or while falling asleep.
- **The notice:** a jump past the Day 1 briefing or the Day 2 solo job meeting says "Skipped: the Day 1 briefing counted as missed. This isn't a real player's Day N." The notice stays until Undo.
- **Later tabs:** Traditions (Stop 1b), Career and Set career (Stop 2) and Big events (Stop 3) say when they're coming.

## The Day 2 meeting recipe
1. Open the Dev link: a new Dev game starts by shuttle.
2. Play Day 0 and Day 1 once, or use Copy my real game.
3. On Day 2: Clock, To a time…, 08:30.
4. Quick: Take me to, Next appointment.
5. Mark here.
6. Watch it, then Back to mark as often as needed. Each one reloads into exactly the same save.

## The Dev link check (Claude app note)
- **How the switch is read:** the game reads its switches from the `#hash` as well as the `?query`, since 0.27.12, because a claude.ai artifact page only keeps the hash. So the published link plus `#dev` turns Dev mode on, the same way `#debug` already works there.
- **Checked here, in Chromium at 390 x 844:**
  - Dev mode turns on with `#dev` and `#dev.debug`, and stays off with `?nosave#dev`.
  - Back to mark, Undo, Copy my real game and Clear each reload the page and come back in Dev mode, because a reload keeps the hash.
  - Adding or removing `#dev` in an open page shows a "Reload" bar.
- **Still to check by the lead on the published artifact:**
  - The Dev link opens with the DEV tag in the Claude app on a phone and in a phone browser.
  - Back to mark reloads inside the Claude app's frame and keeps the tag.
  - The plain link shows no tag.
  - Both use the same browser storage, so the real game started from the plain link is still there afterwards.

## Screenshots (390 x 844 at 2x; 8 landscape 844 x 390)
| File | What |
| --- | --- |
| 1-card.png | The card with DEV, at Day 2 08:30 in the Works Chief's office |
| 2-quick.png | The Quick tab |
| 3-rooms.png, 3b-rooms-deck5.png | Take me to, A room…: the decks, then Deck 5's rooms |
| 4-clock.png, 5-totime.png | The Clock tab; To a time… |
| 6-after-skip.png | +1 day from Day 9 08:30 to Day 10: "Day 9 excused" |
| 7-later-tab.png | A later tab (Set career: Stop 2) |
| 8-landscape.png | The sheet on the right, in landscape |

## Results (D4, the last turn)
- cadet_test against `claude/integration`: ALL IDENTICAL. Run alone, that is: once, run beside two other browser checks, shots f, g and h differed while the state matched; alone, identical, twice.
- names_check: OK.
- devmode_check: OK.
  - **off:** nothing without `#dev`.
  - **real:** the real save is byte-identical through `#dev` and `#dev.debug`, and still writes after.
  - **card:** the DEV tag, the sheet, 6 tabs, 44px buttons.
  - **store:** the space check is refused when space is short and the real game still writes; Undo, Copy and Clear are byte for byte.
  - **clock:** +7 days in 1.6-3.3 s; no misses; leave and needs kept; clocked-in kept; frozen under the fade.
  - **move:** 148 rooms on 7 decks. Two rooms have no walking way from the lift (2:P, 5:d) and you're put in them anyway. Mark and Back to mark are byte for byte, twice.
- check_fast: QUICK CHECK OK (438 s).

## Judgement calls
- **Excused** means a jump passes a workday's 12:30 (when the game counts a miss) while you're not clocked in, from Day 8 on (the first week never counts misses). A short hop past 09:00 excuses nothing (DR1's review).
- **Needs are kept** where they were during a jump. A normal day's ups and downs aren't modelled.
- **Clear Dev save** also removes Mark and Undo. The next Dev game starts by shuttle.
- **Copy my real game** keeps that game's own luck (its career seed), so it's not repeatable. Set career (Stop 2) brings the fixed Dev seed.
- **The panel's CSS** is made inside section 25, not in the page's style block: one seat, no page edit.
- **Rooms with no walking way back to the lift:** the Probe bay (Deck 2) and the Bay door gear (Deck 5) are marked "(no way back)" in the room list; Take me to still puts you there, and again gets you out. devmode_check keeps the list (`DM_SHUT`) true.
