# Review: claude/arrival cd6a9ca..2c4aaee2 (0.42.27-0.42.28: the 17:30 start, the goodnight, the Chief's welcome waited for; merged in sim 57ed91a9)

Reviewer 1c, 2026-10-17. The combined re-check of my arrival-9de4291 finding (no slack before 19:00). Tested on the **full combine: sim 57ed91a9 (arrival 2c4aaee2 merged in) + decks-p3 cad5c89 (the Tern) + player-needs 19afd7f (dinnerTick seats you)**, content de32f5b baked with its content_gen. Only build-line conflicts, plus player_check's washer case. `SHIP_START_ARRIVAL` and `INTRO_START` both read 17:30.

**Verdict: PASS.** My finding is fixed by design: the evening now waits for you instead of ending at a fixed 19:00.

## Checked
- **intro_check `--evening` (part 8): OK.**
  - 27/27 core tour lines in order (34/61 in all);
  - table at 18:47 (16 portions of tacos, 18 crew in the mess);
  - **the Chief's welcome played in full** (shown 18:56, ended 19:00), **then Torres's goodnight** (19:02), **then the bunk arrow** (19:02).
- **Seats** (part 8's stop-and-sit assert, and my seat probe): you sit in 3-mess-10, Torres in 3-mess-12, Calder in 3-mess-9.
- **Why the slack problem is gone:** 'free' is now ended by the goodnight, which waits for the Chief's welcome (`done['chief:met']`, `done['chief:end']`), with fallbacks at 19:30 instead of a fixed 19:00. A slower player still gets the dinner chat, the Chief and the goodnight, as long as they reach the table by about 19:30.

## Low
- The new guard fails if the table comes after 18:50. On this full combine it came at 18:47; sim 5 measured 18:41 on a merge without the player branch. Three minutes is little for a test that runs on many combines. Since the scenes now wait until 19:30, a guard around 19:00 would still catch a real squeeze without flaking. That's the onboarding seat's call.
