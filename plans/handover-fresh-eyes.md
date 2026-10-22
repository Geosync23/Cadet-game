# Handover: fresh-eyes player (FE1)

**Role.** Play the game like a brand-new player at phone size, using only what is on screen, and write down every moment of confusion. No game edits. Report to the lead (lead 28, session_01S7AdxK1ZyXiEFowP3k5gng) with send_message.

**Branch.** `claude/fresh-eyes` (started from `claude/integration` at 2b4a05d, build 0.64.15). Only plans/ files are added: `plans/fresh-eyes-diary.md`, `plans/fresh-eyes/*.png`, this note.

**Scope given.** First: Pillar 5 Steps 1-2, Days 0-8. Then the lead narrowed it (2026-10-22): Day 0 to the end of Day 2 only, then push the diary, send the top points and stop. The full Days 0-8 run comes later on the build with the Pillar 5 fixes (FX1-FX3) and the new arrows switched on; the lead will wake a session for it.

**Where I got to.** See the diary. Day 0 complete; Day 1 played 06:00-17:16 (0.64.15), all in real time, no clock skips. Stopped at 17:16 still clocked in, holding a lamp (the lamp job unfinished), the crew gathered for Name on the beam. Day 2 not played (memory). The top 10 is at the end of the diary.

**Screenshots:** the repo's .gitignore drops *.png; add them with `git add -f` (I shrank them to 256-colour PNGs first).

## How I ran the game (so the next player can repeat it)

- Three.js: `mkdir -p /tmp/cadet-work/three && cd /tmp/cadet-work/three && npm pack three@0.128.0 && tar xzf three-0.128.0.tgz`. `pip install playwright aiohttp`.
- Serve a copy of the game: `python3 -m http.server 8080 --bind 127.0.0.1` in a folder holding `game.html` (a copy of starship-cadet.html).
- A small driver keeps one phone-sized Chromium open (390 x 844, touch, `is_mobile`, a persistent profile so the game's own save survives) and takes commands over HTTP: `shot` (screenshot), `tap x y`, `drag` (press-and-hold via CDP touch events), `wait s`, `text` (every visible text element with its box and font size), `logs`. Script and helper were in my scratchpad (`drv.py`, `c`); the idea is all that matters: tap where a person would, read the screen, never call the game's functions.
- Run the driver with `run_in_background` and `timeout: 7200000`. It is killed at 2 hours; the game then reloads its last hourly save (lost up to an hour of play twice for me).
- **Speed:** SwiftShader gives about 2.7 frames a second here, so ship time runs about 6 times slower than on a phone (10 real seconds a ship minute). A ship day is about 4 real hours. Waiting (a repair, the shift's end) is done by waiting in real time in a background command.
- Screenshots cost memory (about 1.5k tokens each). Use the `text` dump first and take a picture only when the layout matters.

## Gotchas for a player in this build (0.64.15)

- The lift opens only from the small keypad on the wall beside the lift door; tapping the lift itself does nothing. People and speech bubbles often cover the keypad. The spine ladder (next to the lift) always opens its deck list, but a tap can also start a climb with no list.
- People standing in front of a thing take the tap. Close their card with its X at the top right of the card (a tap elsewhere walks you).
- Rotate (top-right, the circular arrow) is the most useful button when you can't see what the pin is on.
- Tracked: tap a row to follow it. Nothing shows which row is followed; a career arrow (tea with Zeke) can hold the arrow until its time is over (known, FX1).

## Open questions for the user

- None from me; the findings and the top 10 are in the diary.
