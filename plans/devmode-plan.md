# Dev mode plan: summary (version 2)

Dev mode planner DP1, 2026-10-20. Version 2 takes in:
- DR1's technical review (`claude/devmode-review-1`, `plans/devmode-plan-review-1.md`)
- DR2's phone-use review and its addendum (`claude/devmode-review-2`, `plans/devmode-plan-review-2.md`)
- DJ1's day-jump measurements (`claude/devmode-dayjump`; marked *to be confirmed*)
- lead 20's call on the order (the playtest kit first)

Branch `claude/devmode-plan`, based on `claude/integration` (0.64.2 + step 2). The full page is `plans/devmode-plan.html`; section 10 there lists every change since version 1. Planning only: the game is unchanged.

## Opening it and keeping the real game safe
- **Opening:** a ready **Dev link** from the lead (the playable link with `#dev`), checked in the Claude app at Stop 1. The fallback is a separate Dev copy of the game. A change to the link in an open tab offers a reload.
- **The way in:** in Dev mode the whole place-and-clock card (the `.hud`, `pointer-events:none` today) becomes the tap target. It has a gold outline and the word **DEV** in letters. The panel's title reads "Dev mode: not your real game".
- **Names:** the switch is `DEVMODE` and the CSS is under `.devmode`. `DEV` is already section 19's device, and using it would stop the game loading. `SAVE_KEY` is declared before `URL_FLAGS`, so section 13's order needs fixing too.
- **Its own save:** `SAVE_KEY` and `INTRO_KEY` get "-dev" added, and `introWanted` uses `INTRO_KEY`. Dev mode doesn't use `nosave`. With `#dev`, even `#dev.debug` only writes the Dev save; a plain `#debug` writing the real save goes on the backlog.
- **Storage:** only the Dev save, one Mark and one Undo stay in localStorage (about 120 KB each). Kept days go in IndexedDB.
  - There's a space check before every write, and Dev mode never removes anything of the real game's.
  - "Clear Dev save" empties everything Dev mode stored.
  - devmode_check fills Dev storage and proves the real save still writes and stays byte-identical.
- **Copy my real game into Dev:** reads the real save, never writes it.
- **A fixed seed:** `careerInit`'s `gs` (`Date.now ^ Math.random`) is the only random source, so Dev mode fixes it (default 1). DR1 saw two unfixed replays differ by a sick day.
- **Every Dev action:**
  - keeps an Undo first;
  - settles what's in progress (a dialogue, an activity, a game);
  - freezes the game through `freezeSync`, with pop-ups quiet rather than off;
  - places the deck's crew once, at the end.

## Stops and turns (about 13-17)
**Stop 1: the playtest kit**
- **D1:** the switch, the Dev save, the card as the way in, the empty sheet, section 25.
- **D2:** IndexedDB, the space check, Clear, Undo, Copy my real game, the fixed seed.
- **D3:** Clock:
  - steps of 30 minutes, frozen;
  - "Excused" by default, "Counts as missed" as a choice;
  - needs kept as a normal day, plus Top up needs;
  - buttons to 08:55 and to 16:55.
- **D4:** Take me to… and Mark / Back to mark.
- **D5-D6:** Traditions:
  - started through a Dev list read by `eventsOn` (the traditions engineer reviews first);
  - plans remade, so 20 of 74 crew move and 57 evenings change (DR1);
  - a table of the ten readers of the traditions list;
  - honorees, flags, fixed hours, and refusals on Day 0 and during a big event.

**Stop 2: the day jump**
- **D7:** `DEV_PLAYER`'s frame, Days 0-2. The first week's meetings are attended in person, because `introWeekMeetings` needs the player in the room on the drawn deck with the speaker there. On paper they're marked missed and the career never starts.
- **D8-D10:** each career row's line, written with its owner. The starting points are mech_check's `PARTS`, intro_check's happy player, arc_check's diligent player and DJ1's script. The milestone "Officer on Day 10" starts as "not yet".
- **D11:** the Career tab:
  - trainings shown by name;
  - the promotion test's needs shown;
  - "Open the test now" (calls `ladderOpen`, agreed with section 24's owner) only when just the day is missing;
  - "Next step" through the beats;
  - set rank, marked approximate.
- **D12-D13:** Jump:
  - the request goes into the tab's short-term storage, then a reload, because a replay after New game isn't repeatable (DJ1);
  - frozen half-day pieces, progress and Stop;
  - kept days stamped with **a fingerprint of the game's script + the steady player's version + the seed**, not the build number (DR1's blocker);
  - loading in through the normal load path.

**Stop 3: big events (the events plan's F6)**
- **D14-D15:**
  - Start sets the event's day (today if its first phase is still ahead, else tomorrow).
  - Next phase, and the threads with − and +.
  - **End and undo** (the default) restores a copy of the event state.
  - **End and keep** waits for the ending to be split out of `eventAdvance` (section 18, owner first, with the events plan).
  - Phase jumps are labelled unreliable until F4.
  - The events plan's F6 turn shrinks to match.
- **D16-D17:** fixes from the reviews.

## Measured (headless, 4 cores, load not counted)
| Run | Day 2 08:40 | Day 10 | Day 26 | Same twice |
|---|---|---|---|---|
| DP1 v2: from the Day 0 arrival, saving on, seed 1 | 1.2-1.4 s | 6.3-7.3 s | 15.7-17.1 s | yes |
| DP1 v1: from Day 1, no saving | | 7.5-8.1 s | 18.9-20.5 s | yes |
| DP1 v1, CPU slowed 4× | | 40.4 s | 101.9 s | yes |
| DR1: saving on, seed not fixed (Day 14, ~12 s) | | | | **no** |
| DJ1: careful player, from Day 1 (*tbc*) | Day 3: 2.0 s | ~11 s | ~43 s (Day 30 ~56 s) | yes, byte for byte |
| DJ1's phone estimate (*tbc*) | | 35-55 s | Day 30: 3-5 min | |

- **What the player reaches:**
  - DJ1's careful player is an Officer by Day 16 and has 19 trainings by Day 26 (*tbc*).
  - With hourly steps it stays a Junior; trainings need minute steps.
  - The simple players (DP1's, DR1's) stay Juniors because they never answer m6's incident call.

## Questions (dm-q1 to dm-q15, plus dm-general; 11-15 new)
1. Opening: **a ready Dev link; tap the place-and-clock card.**
2. Saving: **its own save, with Copy my real game and Clear.**
3. The day jump: **(a) replay in a fresh page, with fingerprinted kept days.**
4. Players: **steady now, busy and lazy later.**
5. Shifts when skipping: **"Excused" by default, "Counts as missed" as a choice, "Play it steady" for whole days from Stop 2.**
6. The arrival in a jump: **yes.**
7. A tradition started today: **today, under the lift's fade.**
8. Career by hand: **show the test's needs, open it early only when just the day is missing, set rank marked approximate.**
9. The order: **three stops, playtest kit first.**
10. Kept in the published game: **yes, behind the Dev link.**
11. Undo: **"Undo last" for every Dev action.**
12. Kept days: **every fifth day plus the last asked for (~0.8 MB).**
13. A first long jump on a phone: **minutes is acceptable, with progress; then kept days.**
14. Take me to and Mark in Stop 1: **yes, both.**
15. Needs when skipping: **kept as a normal day would leave them, plus Top up.**
