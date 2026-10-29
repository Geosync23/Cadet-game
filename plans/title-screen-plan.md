# Title screen: build plan for option B, the crew terminal

TS1 for lead 44, 2026-10-29. Branch `claude/title-screen-plan`. Mockups: `plans/title-screen-mockups.html`
(https://claude.ai/artifact/LTBMF7BhAXNb1a3M5njNVm).

**The user's picks (via lead 44, 2026-10-29):** option B, the crew terminal; no Credits screen; a music track on the
title. For the 1.0 patch. Nothing is built yet; this is the plan.

## What it is

The game opens on the device's old-school phosphor screen, full size, in its bezel. A few boot lines
("CONCORD SURVEY SERVICE", "CSV WREN · CREW TERMINAL", "> crew record found"), the title STARSHIP CADET in
glowing type, then the menu as a list:

- **> CONTINUE**, with your day, time and deck underneath ("DAY 12 · THU 07:40 · DECK 5"). Only when there's a save.
- **NEW GAME**
- **SAVES** (the Saves app; it was on the mockup the user picked. Easy to drop if the user would rather not.)
- **SETTINGS**

There's no Credits line (the user said no). Underneath is a loading line and bar for the deck ("LOADING DECK 5 ... 62%").
The menu works while the bar is still filling. Choosing Continue before the deck is ready waits for it with
"BOARDING ..." and then goes in.

It uses the screen colour from your save (amber, green or Wren cyan), and follows the screen-effects setting and
reduced motion, the same way the device does.

## Where it lives (sections it touches)

| Where | What | Owner to review |
| --- | --- | --- |
| **New section 30, TITLE SCREEN** (placed just above section 12, MAIN LOOP), with its own slot `// ---- slot: Title screen (section 30)` | The switch, `TITLE` state, the menu's actions, the loading steps, the hand-over, the controller panel registration | Title seat (new); add rows to `plans/owners.md` and `plans/map.md` |
| **The page, top of `<body>`** (line ~245, *before* the three.js `<script>` tag at ~287) | A `<div id="title" hidden>` with the boot lines and the menu, plus a tiny inline script that shows it straight away (see "Showing before three.js") | Page owner (HUD seat) |
| **The page CSS** (section 19's skin rules) | Add `#title` to the selector list that defines the `--crt-*` colours, and its three phosphor variants, so the title uses the device's exact skin. The title's own layout CSS goes in a new block after the skin | Device engineer (section 19) |
| **Section 13, `freezeSync()`** | One more term: `|| (typeof titleHold === 'function' && titleHold())`, so the ship's clock and the whole sim stand still while the title is up (like Pause; nothing saves) | Sim / save owner (section 13) |
| **Section 27, SOUND** | The title track (below) and a small `SND.title(on)` hook | Sound seat |
| **Section 26, CONTROLLER** | No edit: section 30 calls the existing helpers `padPanelAdd` and `padOwn` | Controller seat reviews only |
| **Word files (`content/`)** | The terminal's lines, baked like every other word | Words owner |

Nothing in the deck, crew, schedules or save format changes. No new save fields.

## Showing before three.js

Today three.js (about 600 KB from cdnjs) loads before anything else runs, so the screen is empty navy for a moment.
The title's HTML sits *above* that script tag, so the browser paints it while three.js is still downloading.

The inline script (about 20 lines) only reads. It never writes. It:
1. stays hidden when its own switch (`TITLE_EARLY`) is off, under `navigator.webdriver`, or with `nosave`/`dev` in the link,
2. reads the current save slot's key from localStorage, only for the screen colour and the Continue line,
3. shows the div and sets the first loading step.

If reading the save fails for any reason, it shows cyan and leaves Continue out until section 30 confirms the save
with the real `saveOk()`. Section 30 then takes over the same element, and nothing is drawn twice.

## The loading bar: real steps

The bar moves on real milestones, never on a timer:

| Step | Bar |
| --- | --- |
| page shown | 10% |
| three.js arrived, game script running | 35% |
| textures and kit made (end of section 4b) | 60% |
| your deck built (`goToDeck` done) | 90% |
| first frame drawn (main loop's first `renderer.render`) | 100%, the line reads "READY" |

Each step is one line, `titleStep(n)`, guarded with `typeof` so nothing breaks while the switch is off.

## Handing over to the game

- **Continue:** the CRT "switches off" (a quick collapse to a bright line, about 0.3 s; with reduced motion, a plain
  0.2 s fade). Then `TITLE.on = false`, the freeze lifts and you're exactly where your save left you. The clock didn't
  move while the title was up. The HUD is hidden under the title and shows as it fades.
- **New game, with a save:** the terminal asks on itself: "Start a new game? Your current game will be lost.", with
  **START OVER** and **KEEP PLAYING** (the same words and guard as Settings). Start over closes the title and calls
  section 13's `newGameGo()`, which already offers "Arrive by shuttle" or "Skip to Monday morning" to a player who has
  arrived before.
- **New game, no save** (first time ever): NEW GAME is the first line and there's no Continue. It closes the title and
  starts by shuttle, as today.
- **Settings / Saves:** opens the device on that app (`deviceShow('settings')` / `'saves'`) on top of the title. Closing
  the device returns to the title. If a save is switched or loaded in Saves, the page reloads as it does today, and the
  title shows again with the new Continue line.
- **Tab hidden, Pause:** nothing to do. The title already holds the ship, and Pause isn't reachable while it's up.

The title shows once per page load. It doesn't come back mid-game. (For later, if the user wants it: "Back to title" in
Settings.)

## Touch and controller

- **Touch:** each menu line is a full-width button, at least 48 px tall. The highlight box follows your finger and one
  tap chooses. Taps elsewhere on the terminal do nothing (they only wake the sound; see below). Landscape uses the
  mockup's two columns: title and boot lines on the left, menu on the right.
- **Keyboard:** up/down move, Enter chooses, Escape works like B.
- **Controller:** `padPanelAdd('title', { on: () => TITLE.on, first: '#tiGo', back: PAD_MUST })`, registered at the top
  of the panel list so it wins over everything while it's up. The D-pad or left stick moves the highlight and A
  chooses. B does nothing on the main menu, and on the New game question it's Keep playing. Start is Continue (a
  `padOwn` handler). The highlight starts on Continue, or on New game when there's no save.

## The title music

- **One new track, made live like the others** (no files), in the same planetarium style the user chose for the ship's
  music. The sound seat makes 2 or 3 short candidates on a small Wren Sounds page for the user to pick from, the same
  way as the earlier sound rounds.
- **When it plays:** browsers only allow sound after your first tap or key press. The track fades in on the first touch
  of the title, including the tap on a menu line. On Continue or New game it fades out over about 2 s as the deck's hum
  comes in. The ship's time-of-day music then follows its usual rules (none on arrival night until Day 1).
- **Settings respected:** Sound Off or Music Off means no title track. Volume applies. Nothing plays under webdriver,
  `?mute` or `?nosave` (section 27's existing rule). It never calls `R()` and draws nothing.
- **Known limit:** a controller's buttons may not count as that first touch in some browsers. With only a pad, the music
  may wait for the first key or tap. That's a browser rule we can't change.

## Staying out of the regression checks

- **Switch:** `TITLE_ON = false` in section 30, mirrored by `TITLE_EARLY = false` in the page's inline script.
  names_check gets one line to fail if the two differ. Off means the div stays hidden, no hold, no hooks: the game is
  identical, and regressions stay pixel-identical.
- **On, it still stays out of the checks:** the title never shows under `navigator.webdriver` (every check), `nosave` or
  `dev` in the link, unless the link has `title` (`?title` / `#title`). So once it's switched on, every existing check
  still opens straight into the game as today, and only the new check opens the title.
- **New check: `title_check.py`** (on a copy with the switch on, plus `?title`), about 2 minutes. It checks:
  - the title shows before the deck is built;
  - the loading steps reach 100;
  - Continue goes in with the ship's day and minute unchanged;
  - nothing is written to localStorage while the title is up;
  - the New game guard, both answers;
  - no save means no Continue line;
  - Settings and Saves open the device and come back to the title;
  - a pretend-pad walk through the menu (as controller_check does);
  - the three screen colours and reduced motion;
  - draw calls the same as without the title;
  - the switch off gives no title.

  It goes in the full round's split (plans/testing-guide.md) and the test picker's map, and in check_fast if the build
  master agrees (it's short).

## Turns and ETA

| Turn | Who | What | Time |
| --- | --- | --- | --- |
| T1 | Title seat | Section 30 skeleton and switch, the early HTML and CSS (sharing the device skin), the hold in `freezeSync`, Continue and New game (with the guard), touch and keyboard, loading steps. title_check parts 1-6. Switch off. | about half a day |
| T2 | Title seat | Settings and Saves hand-off, the controller panel and Start, landscape, phosphor and reduced motion, the CRT switch-off. title_check complete. Owner reviews (sections 13, 19, page). | about half a day |
| T3 (alongside T1-T2) | Sound seat | 2-3 title track candidates on a Wren Sounds page; the user picks. Then wire the pick in with `SND.title(on)` and the fade. | about half a day, plus the user's pick |
| T4 | Title seat, build master | A switched-on playable copy for the user to try. Then the full round on six runners (about 30 min), merge into `claude/integration`, switch on for the 1.0 patch. | about 2 hours, plus the user's look |

**ETA:** about two working days for one builder, with the sound seat in parallel, plus the user's two looks (the track
pick and the playable copy). No art and no 3D work, and no new draw calls.

## Risks

- **The early inline script runs before the game's own code.** It must stay read-only and tiny, and agree with
  `saveOk()`. Section 30 re-checks and corrects the Continue line once the game has loaded.
- **The page and section 19 CSS are shared.** These are small edits, reviewed by their owners.
- **Music before the first touch:** see "Known limit" above.

## Open questions for the user (via the lead)

1. **SAVES on the menu:** keep it (as in the mockup), or only Continue, New game and Settings?
2. **A "TAP TO LOG IN" first line:** this would let the music start before you choose anything, at the cost of one
   extra tap every time. My recommendation: no gate; the music starts on your first touch.
3. **"Back to title" in Settings** for later: yes or no? Not planned for 1.0.
