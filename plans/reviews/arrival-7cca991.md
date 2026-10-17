# Review: claude/arrival b16436f..7cca991 (0.42.22-0.42.24, for 0.60.4: the start in the Tern, the arrival-0603 merge, tap-to-ask)

Reviewer 1c, 2026-10-17. Diff: `git diff b16436f 7cca991` (section 21, intro_check, DEV_NOTES, design-doc). Tested on **arrival 7cca991 + decks-p3 cad5c89 (the walkable Tern) + sim e4d6ace (SHIP_START_ARRIVAL [5,7] face 0, 0.26.35)**, content 910e88e baked with its content_gen. Only build-line conflicts, plus player_check's washer case.

**Verdict: PASS.**

## Checked (intro_check on that merge: OK)
- **The Tern:**
  - you start at [5,7] in the aisle (the start, `INTRO_START` and the sim's start all agree) with the ramp shut (0) while you sign;
  - 2.4 s after signing the ramp is open (1), with the pilot's toast in the writers' words ("Down gently. Ramp's opening. Welcome to the Wren.");
  - it closes behind you at 17:49 (you at [6,11], once everyone's off) and opens again at 18:58 ('free');
  - a skip leaves it open.
- **A reload can't shut you in:** `TERN` starts open on every deck build, and only the manifest step shuts it. Part 9 reloads at 'ramp' and loads at 'ramp', and part 11 reloads mid-walk; both pass.
- **Tap-to-ask:** tapping Torres on the ramp opens `introAsk`; tapping anyone else doesn't. At a tour place with extras left, a tap plays the next extra instead. At most three asks.
- **The 0.42.21b tour, as passed in arrival-0603-046a019.md:** 27/27 core lines in order (34/61 in all); dinner at 18:55; seats you 3-mess-10, Torres 3-mess-12; the bunk arrow at 19:00.

## For the combine (0.60.4)
- It needs sim 0.26.39 (7ca2249) as well. Without it, a crew diner can take Torres's seat at dinner, and Torres then takes yours (arrival-0603 addendum and sim-7ca2249.md). That needs no change here.
- It also needs decks-p3's Tern and the sim's `SHIP_START_ARRIVAL` = [5,7] together, as the DEV_NOTES row says.

## Low
- The pilot's toast and the ramp opening run on a real `setTimeout` (2 s), not the frame clock. A reload in those 2 s loses the toast, though the ramp is open on reload anyway, so nothing breaks. In a test driven by virtual time it depends on the machine's speed; it passed here. Driving it from `introTick` with a ship-time or frame-clock deadline would make it deterministic.
