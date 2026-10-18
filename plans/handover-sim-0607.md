# Handover: sim engineer 0.60.7 (session_01F7zv2wjhyPPuoHxM8hFzzy)

Stopped early: the user cut the team and the sim seat folds into the systems seat (lead 10's call, 2026-10-18). **No game code was changed.** Branch `claude/sim-0607` = live 0.60.6a (c8685cf) plus this note only. My build series would have been 0.26.43 and up (sim engineer 5's last was 0.26.42).

Read first: CLAUDE.md, `plans/brief-0607.md` (claude/lead-pillar1), `plans/plan-0607.html` (claude/plan-0607, "Around the ship"), and the long note `plans/handover-sim.md` (claude/sim-engineer).

## What I found (all in live 0.60.6a)

### Trays: THE USER'S DECISION (lead 10, 04:01): no tray return and no clearing walk. A diner's tray simply goes away once their meal is over, and no crew walk for trays. The galley and dish pit must keep working (food_check green). So build only the "smallest fix" below plus the removals, and skip the "galley crew clearing" part.
- Section 10, around line 33990-34235: `TRAY_AT` [[33,2],[33,1]], `CrewAgent.mealStep` calls `this.trayBack(m, now)` once the meal is over (`if (m.tray && N === 3) return this.trayBack(m, now);`). `trayBack` walks the diner to `@tray-<n>` and drops the tray there (`LINE_LOG.returned`, `LINE_LOG.back`).
- **Smallest fix:** in mealStep, swap the trayBack line for `if (m.tray) { m.tray = false; LINE_LOG.returned++; }` and fall through to `m = this.meal = null`. The tray stays on the table, the diner just leaves. That also closes reviewer 1's old should-fix (breakfast tray returns made about 36 crew up to 6 minutes late for the lift). Then remove `TRAY_AT`, `trayBack` and the `@tray-` branch of `lineSpotMake`, and day_check's "walk back with a tray over 12 minutes" rule (check day_check.py for `back`/`returned`).
- **Galley crew clearing (not started):** section 16's `galleyRota` turns 'line' stints into serve/wash by turns (`GALLEY_SHIFTS`, `GALLEY_AT`). One way: add a `clear` job (a wash stint at 3-galley-7 tagged 'clear') that section 10 turns into a round of the mess tables carrying trays (hold 'carry'), then back to the dish pit. The food model already counts dirty plates coming back when people finish eating, so food_check shouldn't move. Drawing the trays left on tables would need new meshes (an InstancedMesh copied from `TRAY_ON`, line ~11318, one draw call) and is optional.
- **The player's side (PE6):** the `eat` act's done text (line ~10910) still says "You clear your tray and take it to the return by the servery." It needs new wording. The deck architect removes the `trayReturn` object (line ~5163).

### Showers (only Decks 2 and 4)
- Beds: 14 on Deck 2 and 133 on Deck 4 (roster, guests and reserves); no one sleeps anywhere else. Shared showers: Deck 4 has 4 (washrooms p and q, 2 each), Deck 5 has 1 (`5-shower-1`). Cabins own their wash pods.
- Schedules (section 14, `wash()` ~line 8597) already use the bed deck's showers only. **Deck 5's shower is used only by Works crew washing up after the shift** (`evening()`: `take('wash', [[wd,'shower'],[wd,'basin']] ...)`, about 1-2 a day). Once the deck architect turns `5-shower-1` into a toilet, that falls back to a basin by itself: no sim change needed.
- About 63 shared-shower uses a day on Deck 4. A shower wait is planned (`wait: 25`), but the person waits wherever they were (usually their bunk), so nobody queues where you can see them. **Shower queue idea:** when `take` finds its start later than the arrival, add a short 'showerq' stop at a queue spot in the washroom. That needs queue spots (places from the deck architect, or a sim-owned list like `LINE_AT`).

### Crew hobbies
- The roster already has `hobby` and `hobbyNoun` text (87 entries), e.g. Zeke "knitting", "reading", "drawing comics", "keeping a journal", "doing crosswords in the bow lounge", "mapping the stars". A `crewHobby(p)` hook can map them by keyword to the plan's seven: knit, draw (draw/sketch/paint), read (read/novel), write (writ/journal/letters), puzzle (crossword/card tricks/knots), games (Tiles), stars (star). Anyone else gets null. Social and traditions will want this hook early.
- Poses: `ACTS` (section 8b, ~line 32506) has read, drink, talk, but no knit, draw or puzzle. `crewPose` (~line 33968) already makes seated leisure crew read/talk/drink, seeded per person and day. Hook a hobby in there: on a SIT_ABOUT seat, use the person's hobby act when `CROWD_ANIMS.has(it)`, else 'read'. Ask PE6 which acts they add for the player's hobbies.

### Bartender (not started)
- The plan says a galley hand on bar duty 17:30-23:00, two taking turns. That fits as a new `GALLEY_SHIFTS` role or block in section 16's `galleyRota`, at the deck architect's new bar place (not pushed yet when I stopped). Bar regulars already use `3|bar` seats (`specials`, tag 'bar').

## Gotchas
- Test kit setup: `pip install playwright`, then three@0.128.0 into /tmp/cadet-work/three (DEV_NOTES "Testing"). A probe can reuse cadet_test's `Game` class: `exec(open('cadet_test.py').read().split("a, shots = run(")[0])`, then `g.page.evaluate("src => window.__sc(src)", js)`.
- Give every parallel check build its own file name (cadet_test copies to `_run_<name>`).
