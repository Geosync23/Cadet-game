# Handover: fresh-eyes player 2 (FE2)

**Role.** Play the game as a brand-new player at phone size, using only what is on screen (no game code, no design docs, no dev shortcuts), and write down every moment of confusion, block or delight. No game edits. Report to the lead with send_message (lead 31, session_0118SXBCdg87nDiXdtrGNVSR, took over from lead 30 during this run), one message per batch.

**Branch.** `claude/fresh-eyes-2` (started from `claude/integration`; only plans/ files added): `plans/fresh-eyes-2-diary.md` (the diary and the top 10), `plans/fresh-eyes-2/*.png` (38 screenshots, 256-colour), this note, and FE1's driver in `plans/fresh-eyes-driver/`.

**Build played.** 0.92.0, claude/integration 685af944, game file sha256 f2329b62...6ebd (checked). Teaching arrows on (Settings default "First times"); the controller and Crossing the Line off.

**Where I got to.** Day 0 complete; Day 1 complete (06:00 to bed at 21:12); Day 2 from 06:00 to 09:05 only. Got out of the bunk wing by the spine ladder and reached Calder's desk at 08:58, but the 08:45 "first solo job" never started (diary item 46). Stopped there, at about 60% memory, by the Chief's office on Deck 5, not clocked in. Days 2 (rest) to 8 are not played. Item numbers 1-46 in the diary match the six batches sent to the lead.

**The save does not carry over.** My game's save lives in this container's browser profile (/tmp/cadet-work/profile), which a new session can't reach. A fresh FE starts a new game from Day 0 (or the lead decides how to get to Day 2+).

## How I ran the game

- As FE1 (see `plans/handover-fresh-eyes.md`): three.js r128 from `npm pack three@0.128.0`, `pip install playwright aiohttp`, a copy of the game served on 127.0.0.1:8080, and FE1's `drv.py` (I added a second argument: the browser profile folder, so each run gets a clean save).
- **Avoid the 2-hour kill:** start the server and the driver detached, not as background tasks: `setsid nohup python3 -m http.server 8080 --bind 127.0.0.1 >/dev/null 2>&1 </dev/null &`, and the same for `drv.py`. Background tasks are killed at 2 hours. That cost me two reloads; the game reloads its last save, made on reaching a deck or on the hour.
- My helpers (in /tmp, easy to rebuild): `g` (tap / wait / text / shot), `watch N` (prints only the new on-screen lines every 8 s), `s NAME` (a screenshot, plus a half-size copy for viewing, which saves memory), `x` (closes a card by finding its × button).
- **Memory:** a half-size screenshot (195 x 422) is enough to see the scene. Read the text dump first, and take a picture only when the layout matters.
- **Speed:** about 3 frames a second, so about 10 real seconds per ship minute. A full waking day is about 2.5-3 real hours, and most of it went on walking and mis-taps. Days 0-8 in full is not possible in one session's memory; plan to sample (sleep through nights, wait cheaply through quiet hours, and play the key moments in full).

## Gotchas for a player in this build

- Floor taps near furniture sit you down; tap open floor. People's cards take taps meant for things behind them.
- A card's × is hit about 20 px below and right of where it's drawn.
- Rotate (top right) after nearly every walk; the camera turns as you move.
- The lift opens from the keypad on the wall beside the lift door (it worked first time once I could see it). The lift list marks your arrow's deck.
- Grab and go (the chilled counter beside the servery) is the reliable meal: about 4 minutes, no seat needed.
- The Tracked list reopens at its old scroll position; check the time on a row before you tap it.
- The relay job (Day 1) can't be finished: the lit shelf answers as "Filters" (diary item 28).

## Open questions for the user

- None from me; the findings and the top 10 are in the diary.
