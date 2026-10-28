# Controller audit (CA1, for lead 43, 2026-10-28)

Build audited: **0.95.0** (claude/staging-p5s6 b5199dc3), branch claude/controller-audit. No game change, no check change.
Method: read section 26 (CONTROLLER, 72191-73064) and every part of the game a player can touch; two helper read-throughs
(the Works career, sections 17, 24-28f; ship life, events, social and the ending, sections 16, 15r, 18, 18f, 20, 20c, 21,
21b, 23, 23b, 29-29c); headless runs with a pretend pad on a PAD_ON copy for the doubtful cases (probe scripts in CA1's
scratchpad, not kept: Dev mode's opener, the shop menu, the chat card, Load a save file, sound).

## 1. Summary

- **The base is sound and mostly current.** Every device app, every question card (`deviceChoose`), every scene (`devDlg`),
  the job board, the lift, the alarm, the ladder, the time clock, the shop menu, Lightdisc, Tiles, the arrival form and
  the end page are panels the pad knows. All of Step 5 and Step 6 (the Tier 4 test, nights, the badge, the reactor, the
  Team tab, the coil swap, the briefing, mentoring, Calder's question) is built from those same pieces, so it works by pad
  with no new code. controller_check already has pad parts for most of it (m19, m20, m21, m23, m24, deck6, s5cases,
  s6cases, promo4, nights, mentor, team, shut, vessel, ending).
- **What's wrong is a short list, mostly in section 26 itself:**
  1. The two most used cards land the highlight on the close cross: **the chat card** and **the shop menu** (confirmed by
     run: the first A press closes them).
  2. **Time clock Undo:** after Clock in the screen itself focuses Undo, so a second A press (after the 0.5 s guard,
     within 5 s) undoes the punch. Touch puts Undo on the far side on purpose.
  3. **Things that appear on the deck while you're already there never get the ring** (`padRaw` caches the item list by
     the list's identity, and props are pushed into the same list): the birthday cake, the vessel's parts sheet, Tiles
     night boards, event decor, the cabin touch spots, the Wednesday delivery crates.
  4. **Only one "Your job" stop is offered:** `padRaw` takes the first held job with any next stop (often a side job such
     as tomorrow's team job, held from 16:00), never the one on this deck, so board stops at plain floor places (leak
     puddles, incident clean-ups, nozzle racks, odd jobs) get no ring.
  5. **Dev mode can't be opened by pad** (its opener is the clock card, `.hud`, not among the screen-edge buttons;
     confirmed by run). Its "reload" bar (`#dmLink`) isn't reachable either.
  6. **No sound for a pad-only player:** sound starts only on a real touch or key press (section 27's `gesture`); a pad
     press never starts it (confirmed: the audio context stays empty until a tap).
  7. Smaller: Name on the beam's floor fallback and the Lightdisc court's far edges aren't in the ring; Take a seat and
     Lift (`#seatBtn`, `#liftBtn`) are reachable by D-pad up but not on X; a few cards only a tap puts away; "Tap ..."
     words shown to pad players; typing (memos, Dev search) needs a phone keyboard.
- **controller_check gaps:** `part_promo3` exists but is never registered (not in `PART_FN`/`ALL_PARTS`); no part covers
  Undo, the chat card's landing, props appearing mid-visit, tradition joins, the birthday, the beam, the comet, the rec
  deck activities, the wardrobe/hamper/washers, Calder's question, the first promotion, Dev mode by pad, the Saves app by
  pad. The full `reach` sweep has never finished a run (handover-controller-tests.md).
- **Counts (rows in section 2a-2c):** 110 rows: 82 works, 22 partly (2 of them work in most cases), 3 missing, 3 to test on a real device.

## 2. The table

Verdicts are for a copy with `PAD_ON` on (in 0.95.0 it is off, so nothing works by pad today). "Works" means reach,
focus, use and close all work. Check = the controller_check part (or ending_check `pad`) that plays it by pad.

### 2a. Screen edge, device, settings, saves, Dev mode (sections page, 11, 13, 15, 15b, 19, 25, 26, 27)

| Feature | Shown as | Code (approx line) | Pad | Check | Note |
|---|---|---|---|---|---|
| Pause button, Pause card, Resume | HUD; `#pauseCard` panel | `pauseSet` 14038 | works | panels, unplug | Menu toggles; B resumes |
| Rotate, Shadows, Walls, Crew, Night | `.controls` (HUD) | 70914-70931 | works | panels | D-pad up |
| Device button (and "No device yet") | HUD; Y | 12450, 14746 | works | panels | the lock's capture listener runs on click() too |
| Schedule tracker button and panel | HUD; View; `#trkPanel` | `trkOpen` 17258 | works | panels | |
| Needs strip open/close | HUD `#needStrip` (role=button) | `needStrip` 14790 | works | panels | |
| Needs strip fold button | `.nsFold` inside the strip | 14794 | partly | none | not among the screen-edge buttons; unfold works (strip click) |
| Need warning pop-up | `#needPop` div | 13808 | partly | none | only a tap puts it away; it hides itself after 6 s |
| Toasts | `#toast` | | works | panels | B on the deck hides |
| Tip card | `#devTip` (HUD; B on deck) | `skin.tip` 12391 | works / partly | panels | over the open device it can't be reached (hides itself after 9 s) |
| Captain's address card | `#devAddr` (HUD; B on deck) | `skin.address` 12416 | works | panels | |
| Heads-up and Go there | `#devHu` (HUD) | `skin.heads` 12434 | works | panels | |
| Goal pin tap (the arrow's pin) | `#ixGoal .ixpin` | 16800 | partly | none | shortcut only; the ring offers the thing itself |
| Panel pointer (gold ring) | `#ptr`, display | `pointAsk` 13380 | works | none | sits on real buttons |
| Repair / Hobby / Put down | `#handBtns`, `#putDown`; X | 15358, 16764 | works | pick, day | |
| Take a seat, Lift (0.93.2, 0.92.6) | `#seatBtn`, `#liftBtn` | 15362 | partly | none | reachable by D-pad up; not on X, no mark |
| Lift panel | `#lift` | `pressPanel` 71048 | works | lift, day | lands on the goal deck |
| Alarm card | `#sleepAsk` | 9810 | works | day | lands on Set alarm |
| Spine ladder panel | `#ladderPanel` | `ladderPanel` 16156 | works | reach | B = Escape |
| Queue question | `#qAsk` | `queueAsk` 14558 | works | panels | B = Stay |
| Shop menu (storekeeper, 0.95.0) | `#shopMenu` panel | `shopMenuOpen` 16055 | **partly** | none | lands on the × (confirmed): the first A closes it |
| Job board, Ship health | `.ixpanel` | 15b 16805 | works | day | |
| Device apps, all (home grid, Schedule, Calendar, Jobs, Roster, Needs, Mail, Wallet, News, Record, Relationships, Appointments, Hobbies, Tracked, Music, Tiles, Works, Scanner, Pipe kit, Fault notes, Old mysteries) | `#device` blocks (buttons, list rows, chips) | section 19 12230 | works | panels (every app) | LB/RB Back/Home |
| Maps plan (SVG) | `map` block | 12290 | works (ruled) | panels | rooms also in the list below (PR9's ruling) |
| Memos: new memo | `form` block (text boxes) | 12832 | partly | none | A brings the phone keyboard; none on a TV or computer |
| Settings: colour, effects, tips, quiet, Doors, Sound, Volume, New game (two presses), heads-ups, teaching arrows | device buttons | 13172 | works | panels | |
| Settings: Controller page | `padsettings` app | 72959 | works | settings | shown once a pad is used |
| Saves: Play, New game (two ways), Delete + guard | device buttons, `deviceChoose` | `slotsView` 13350 | works | none | |
| Saves: Download my save | device button | `slotDownload` 13280 | to test | none | a link click / the claude.ai downloads call from a pad press: allowed in the test browser; a real phone may want a touch |
| Saves: Copy save as text | device button | `slotCopy` 13291 | to test | none | the clipboard may refuse without a touch |
| Saves: Load a save file | file picker | `slotPick` 13300 | to test | none | the picker opened from a pad press in the test browser (Playwright's), but browsers normally ask for a touch first |
| Sound: start | section 27 `gesture` | 74370 | **missing** | none | starts only on a trusted pointerdown/keydown; a pad-only player never hears anything (confirmed) |
| Dev mode: open the Dev panel | the clock card `.hud` (role=button) | `devmodeBuild` 71150 | **missing** | none | not in `PAD_HUD_SEL` (confirmed) |
| Dev mode: tabs, every row button, Close, Undo, Mark, Dev clock, Take me to, career arrow Show/Hide | `#dmSheet` panel | 71155+ | works | none | once open; B closes |
| Dev mode: Traditions search box | input | 71611 | partly | none | needs a keyboard |
| Dev link changed: Reload bar | `#dmLink` | 71210 | **missing** | none | not a panel, not on the edge (rare) |
| Arrival name form | `#introManifest` | 55264, 72771 | works | screens | no keyboard: the name is George (the user's choice) |
| Walking, turning, zooming | stick, LB/RB, triggers | 72303 | works | walk | |
| Doors shut to you (0.93.3) | ring, A | `padWhat` 72345 | works | door | |
| Disconnect pause | Pause card line | `padPauseLine` | works | unplug, drop | |

### 2b. The Works career and machines (sections 17, 24-24x, 28-28f)

All switches here are on in 0.95.0. No custom overlays, keys, drags or text boxes in these sections: every screen is a
device app (buttons, list rows, chips), a `deviceChoose` card or a scene.

| Feature | Shown as | Code (approx line) | Pad | Check | Note |
|---|---|---|---|---|---|
| Job board: Take it / Turn in / Ship health | `.ixpanel` | 15b; `openJobs` 21066 | works | day (Take it) | |
| Jobs app | device | 12637 | works | panels | |
| Repair loop: shelves, look-over, Repair | items; X | `jobEnd` 15610, `shelfGlowTap` 21149 | works | pick | |
| Hover-cart restock / Wednesday unload | items; loads itself | `cartAuto` 15884 | works | none | |
| Wednesday delivery crates item | item at y -10 until shown | 7729 | partly | none | prop gap (2d, D); loading still happens by itself |
| Works app tab bar and tabs (Training, Work log, Tools, Your career, Home) | device | `worksView` 58129, `cqPage` 67290 | works | shut | |
| Fault notes: cases P1-P9 | buttons, chips | `caseView` 60300, 60957, 61610, 61710 | works | s5cases (P4), s6cases (P6-P8) | P1-P3, P5, P9 not by pad |
| Case: ask a witness | chat button | `caseAskButton` | works | none | chat lands on × (2c) |
| Old mysteries board and job | item, `oldcases` app | `mysOpen` 61399 | works | s5cases | |
| Scanner (M7), Pipe kit / tracing (M9) | items, apps | 59116, 59202 | works | none | |
| Rounds, uniform, drill, inspection, hauling (M1-M4) | stops, cards | 58159-58844 | works | none | |
| Tool bench, tool wall (M11), logbook (M12) | items, cards | 58889, 58896, 59018 | works | none | |
| Workshop: order board, lathe, tinkering, Give | items, cards, chat button | 59507, 59522 | works | none | |
| Cabin touches (4-23, the Deck 2 suite) | spots pushed into ITEMS during play | `cabinDraw` 59591 | partly | none | prop gap: about half of arrivals never offer them |
| Star log (telescope) | item, card | 59672 | works | none | |
| Lift roof (M17) | lift tap, card | 59752 | works | none | |
| Tuning (M5), incidents (M6), team jobs (M8) | cards, stops | 61860, 62024, 24h | works / partly | team | incident clean-up stops: job-stop gap (2d, E) |
| Favour cases | chat, stops, cards | 62477 | partly | none | job-stop gap |
| Leak hunting (M13), irrigation (M14) | stops at plain places | 62711, 63030 | partly | none | job-stop gap |
| Rewiring (M15) | panels, cards | 62926 | works | none | |
| First promotion (test, summons, ceremony, move to 4-23) | stops, scenes | 24p 63046 | works | none | |
| Power safety lesson; Tier 3 test, shutdown warnings, result, cake | stops, chat button, scenes | 63784, 64209, 64421 | works | promo3 written, **never run** | |
| Tier 4 test, badge, room B move, refit pick | stops, scenes, card | 24u, 65071 | works | promo4 (refit: none) | |
| Relays, batteries, conduit (M19); drill calls | stops, cards | 65294, 65327 | works | m19 | |
| Shutdowns tab, warn in person (M18) | device; chat button | `sdView` 65540 | works | shut (tab) | |
| Sensor array (M20) | stops, cards | 65929 | works | m20 | |
| Night shift: clock, day sleep, kept plate | `#clockScreen`, `#sleepAsk`, servery | `p5nClockScreen` 66079 | works | nights | |
| Monday briefing | seat, scene, wall screen | `m21Screen` 66430 | works | m21 | |
| Engine work, reactor: coil dials, board swap, permit, Watch, door, dosimeter rack | stops, cards | `m23Card` 66646 | works | m23, deck6 | |
| Leading a team: Team tab, Book, spots, Next step, coil swap | device, cards | `m24View` 66899 | works | m24 | |
| Mentoring Basil | scenes, cards | 28e | works | mentor | |
| Calder's question (tea corner) | sit, scene with 4 answers | `cqAskScene` 67207 | works | none | |

### 2c. Ship life, events, social, the ending (sections 16, 15r, 18, 18f, 20, 20c, 21, 21b, 23, 23b, 29-29c)

| Feature | Shown as | Code (approx line) | Pad | Check | Note |
|---|---|---|---|---|---|
| Chat card: every button (Say hello, Talk, Ask about, Help, Meet up, Come over, Sit with them, Give, Buy something, Goodbye, the ending's) | `#chat` panel | `chatShow` 53111, `skin.chat` 12426 | **partly** | panels, day, ending | lands on the × (confirmed): the first A closes it |
| Chat from afar: Walk over | `#chat` | 53165 | partly | none | same landing |
| Rank on crew cards (0.95.0) | text on the card | `rankCardRole` 15973 | works | n/a | display |
| Time clock screen: Clock in/out, early ask, Cancel, Close | `#clockScreen` | `clockScreen` 52154 | works | nights | |
| Time clock Undo (0.95.0) | button | `clockButtons` 16014 | **partly** | none | the screen focuses Undo after a punch; a second A undoes it |
| Waking sick card | `#sickCard` | 52340 | works | panels | B does nothing (a must-answer card) |
| Career-over card, New game choice | `#careerEnd`, card | `careerCard` 52381 | works | none | |
| "Would like a word" / knock at the door | `#seek` (HUD) | 52753 | works | none | B doesn't put it away (it times out) |
| Relationships app | device | 52898 | works | panels | |
| Social stories moments, home calls | `devDlg` | 53891, 54159 | works | none | |
| Tradition join: tap the leader | crew | `tradJoinTap` 45801 | works | none | crowded: the ring keeps 8 things; walk closer |
| Joining by being in the room, the Friday address | walking | `meetingsTick` 47297 | works | none | |
| Event meetings and scenes, volunteering | `devDlg` | `dialogueShow` 47221 | works | vessel, ending | |
| Event decor props (sign-up sheets, lanterns, party decor, Line punch and plaque, lectern, cup board, talent stage) | items via `dressShow` | 7951-8339 | partly | none | prop gap when they appear while you're there |
| Birthday cake slice | item (`bdayCake`) | 48054 | partly | none | prop gap: it appears about 30 min before, usually while you're in the mess |
| Birthday seats, long tables | places | `padPlaces` | works | pick | |
| Name on the beam | item "The beam" | `beamPaint` 45860, `beamFloorTap` 45868 | partly | none | the floor fallback (2.5 tiles) isn't in the ring |
| Tasting table: join, dishes, vote | crew, card | 48406, 18200 | works | none | |
| Tiles ladder, swap meet, spice guess, talks, talent night | crew, cards | 47980, 48186, 48251, 45644 | works | none | |
| Invitations | Appointments app | 51539 | works | panels | |
| Veyli vessel: Calder's sheet, ramp, bench, helper card, stock card, making steps, chain | crew, cards, walking | 49526-49808 | works | vessel | |
| Vessel parts sheet: sign | item (`vesselSheet`) | `vesselSign` 49542 | partly | vessel (after a deck jump only) | prop gap if you're in the bay at 09:30 Saturday |
| Comet: Saruth's knot, naming | crew, scenes | 49037 | works | none | |
| Storm, Crossing the Line, crossing back | scenes by walking in | 48653, 49895 | works | ending (oath) | |
| Friday address seats; lectern | rec items | `recTap` 17799 | works | none | |
| Arrival: ramp, tour, Torres, first-week meeting, Call home card, kit bag | walking, crew, cards, wardrobe ring | 55319, 56105, 55537, 15161 | works | screens | "Tap your device" pointer says Tap (`#devPoint`) |
| Wardrobe, hamper, washers | ring, X, items | 55758-55893 | works | none | |
| Servery, grab and go, kept plate, eating | items, places | 14282, 14400 | works | day, nights | |
| Rec deck: pool, kayaks, wave gate, climbing wall, beanbag, sim pod, seats, stands, lockers, scoreboard, float room, waiting your turn | items, walking | `recTap` 17799, 17882 | works | none | the pad taps near an item's middle (lane, route chosen by the point: cosmetic) |
| Lightdisc court (tap the floor) | item 12.6 x 4.6 m | `recTap` | partly | none | its middle is often more than 3.2 m away; the gate panel works |
| Lightdisc: Ask someone, Cup day, Winner Stays On | item, card | 57109 | works | none (disc calls `discAsk` directly) | |
| Lightdisc game: How to play, stick, result, Leave | `#ld` panel, `padOwn` | 57243, 72711 | works | games, disc | |
| Tiles: station, table, game, hold, Next/Skip/Again/Done | item, device dom block, `padOwn` | 56803, 72684 | works | games, tiles | B in a game goes to device Home (the game waits) |
| Tiles night boards | props | | partly | none | prop gap |
| The offer, Calder comes to find you, the Captain's search | scenes | 29a 74533, 74685, 74713 | works | ending | |
| About the transfer, Zeke Friday/Sunday, Call home about it | chat button, cards, scenes | 74659, 74779-74826 | works | ending (part) | |
| Oath at the Line, Monday farewells, into the Tern | walking, chat, scenes | 75056-75090 | works | ending | |
| End page: Keep this ending, Start a new game | `#endPage` panel | `endPage` 74931, 74971 | works | ending; ending_check pad | B does nothing (must answer) |
| Endgame Works Home tab | device | 29c 75130 | works | none | |

### 2d. The gaps, with their code places

| Id | Gap | Where | Kind |
|---|---|---|---|
| A | Chat card and shop menu land on the × | `PAD_FIRST` (72563); panels `chat`, `shopMenu` | partly |
| B | Time clock: the highlight on Undo after a punch | `clockScreen` 52154 focuses the row's first enabled button; pad side: a `padOwn` or `PAD_FIRST` rule for `clockScreen` | partly |
| C | Dev mode opener and the Dev link bar | `PAD_HUD_SEL` (72566): add `.hud` when `DEVMODE`, `#dmLink button` | missing |
| D | Props added to ITEMS mid-visit never offered | `padRaw` 72432 (`PAD_PICK.of !== ITEMS`); pushers: `dressShow` 8339, `cabinDraw` 59617, 7729 | partly |
| E | Only one job stop offered, maybe on another deck | `padRaw` 72441 (`ixChores().find(...)`) | partly |
| F | Beam floor fallback; large floor items (Lightdisc court) beyond 3.2 m by their middle | `padRaw` (item middles), `padWhat` 72340 | partly |
| G | Take a seat / Lift not on X | the `x` handler 72691, `PAD_MARKS` 72825 | partly |
| H | Sound never starts by pad | section 27 `gesture` 74370 (needs a hook from section 26's first press) | missing |
| I | Cards only a tap puts away (`#needPop`, `#seek` by B, the tip card over the device), the strip's fold button, the goal pin | `PAD_HUD_SEL`, the `b` handler 72336 | partly (minor) |
| J | "Tap ..." words to pad players (`#devPoint`, some toasts) | 21b 56164, toasts | partly (minor) |
| K | Typing with no phone keyboard (memos, Dev search) | device `form` block; 71611 | partly (accepted: the user's answer to question 6 covers only the name) |
| L | Download / Copy / Load a save file from a pad press | `slotDownload`, `slotCopy`, `slotPick` 13280-13308 | to test on a real device |

## 3. Proposed build waves

Section 26's slot is one block, so each wave owns a different stretch of it (named by its turn header) plus its own
places outside it, and appends its new code as its own labelled block at the end of the slot in merge order (A, then B,
then C). controller_check.py: each wave adds its own `def part_<name>` block just above the `NEEDS = {` line of its own
area (A above line 2886, B and C at the end of the file before `ON_SRC =`, in that order) and its own one-line
registration (`PART_FN[...] = ...; NEEDS[...] = ...; ALL_PARTS.append(...)`), so the three never touch the same lines.
Every part runs on the PAD_ON copy the check already makes.

### Wave A: panels and the screen edge (one builder)
- **Owns:** section 26's turn 4 block (72534-72700: `PAD_FIRST`, `PAD_HUD_SEL`, `PAD_BACK`, the `b`, `x`, `lb`/`rb`
  handlers), P3's `PAD_MARKS` line (72825); nothing outside section 26.
- **Builds:** A (`PAD_FIRST.chat = '#chat .act'`, `PAD_FIRST.shopMenu` = its first enabled goods button); B (on
  `#clockScreen`, while `CLOCK_UNDO` is open, land on the × instead of the game's Undo focus; pad-only, the touch layout
  stays); C (`.hud` among the edge buttons when `DEVMODE`; `#dmLink` reachable); G (X also presses `#seatBtn`, `#liftBtn`,
  with its mark); I (`#needPop`, `#seek` put away by B on the deck; `.nsFold` and the goal pin among the edge buttons).
- **Check parts:** `cards` (chat card and shop menu: first A presses a real choice, not ×; B closes), `clock` (Clock in by
  pad, wait 1 s, A again: still clocked in; Undo reachable by moving to it; B closes), `devpad` (with `#dev`: D-pad up
  reaches the Dev card, A opens the sheet, a tab and a row by pad, B closes), `edge` (Take a seat by X with a tray; the
  need pop and the seek card by B).

### Wave B: picking on the deck (one builder)
- **Owns:** section 26's turn 3 block (72342-72532: `PAD_PICK`, `padWhat`, `padPlaces`, `padRaw`, `padFind`,
  `padSearch`, the ring); nothing outside section 26.
- **Builds:** D (refresh the item cache when ITEMS grows or changes, not only when it's replaced: e.g. keep its length
  and a cheap signature; one line in `padRaw`); E (offer every held job's next stop that is on this deck, each its own
  key, the board job first as `jobHere` takes it); F (the beam's floor fallback as a pickable spot while Name on the beam
  is on; for an item wider than the reach, use its nearest edge point, not its middle). Keep `PAD_PICK.budget` and the
  draw-call budget (perf part).
- **Check parts:** `props` (stand in a room, then make a prop appear without a deck change: the birthday cake by its
  phase, a cabin spot by its tick; the ring offers it and A uses it), `jobs2` (a team job held as a side job plus a leak
  stop on this deck: the ring offers the leak stop and A starts it), `beam` (Name on the beam by pad from 2 tiles away),
  `court` (Lightdisc court offered from its gate). And register the existing `part_promo3` (one line).

### Wave C: outside section 26, browser rules and words (one builder, with the owners' reviews)
- **Owns:** one-line hooks in section 27 (SD1's: let section 26's first pad press call `SND.start()`; if the browser
  refuses, a toast "Sound starts at your first tap" once), section 21b's device pointer words (`INTRO_DEV_POINT` 56164:
  pad words while `PAD.used`), section 19's Saves app (`slotsView`: with the pad in use, a line under Load a save file:
  "Opens your files: a tap may be needed"), plus their words. Needs plans/owners.md's owners to review each hook.
- **Builds:** H, J, L's wording; and a real-device test list for the user (Download, Copy, Load, sound, the Back button
  on a phone clip-on), since the test browser can't prove what a phone allows.
- **Check parts:** `sound` (pad-only play with `?sound`: the audio context starts, or the once-toast shows), `saves`
  (Saves app by pad: Play, New game's choice, Delete's guard, Download fires a download, Load opens the picker in the test
  browser), `words` (no "Tap" on screen while the pad is in use, for the device pointer and the door toast).

### Then: the switch-on (build master, its own reviewed step)
`PAD_ON = true`, the build number lines, DEV_NOTES and design-doc ("being built, switched off" becomes on), the full round
across six runners plus a full controller_check run (all parts, `--mutants` on the new parts) and the long `reach`
sweep in a slot of its own (about 2 hours; it has never finished). The user's real-controller test outside the Claude app
before the switch-on is published.

## 4. Risks when PAD_ON goes on (sweep list)

With the switch on and no pad, the game adds two listeners (`gamepadconnected`, `gamepaddisconnected`), registers the
hidden `padsettings` app and runs the main loop's `if (PAD.live)`. Headless test browsers have no pads, so nothing else
runs. Checks to sweep:
1. **cadet_test** (switch-on build against 0.95.x): must be ALL IDENTICAL; controller_check `idle` and `save` already prove
   the off-against-on case in a copy every round.
2. **controller_check:** handles a build with the switch on (it makes its own off and on copies); after the switch-on,
   `idle` and `save` compare the shipped build to an off copy, fine. Parts not run in any recent round should be run once
   before: `reach` (never finished), `day`, `promo3` (unregistered), the legacy parts (`off`, `quiet`, `base`, `deck`,
   `pick1`, `panels`, `api`, `lists`, `tiles`, `disc`, `screens`, `marks`, `touch3`, `drop`, `settings`, `a11y`,
   `firstuse`): they were written on 0.90.x and many panels moved since.
3. **ending_check `pad`:** replaces the text `const PAD_ON = false;` with true; with the switch on that is a no-op and the
   part still runs. Fine, but the comment should say so.
4. **device_check, interactions_check, saves_check, sound_check, player_check, p926_check, appt_check** read
   `DEVICE_APPS` by id only; the hidden `padsettings` app doesn't show on the home grid (its `hidden()` is true). No
   change expected; the full round confirms.
5. **names_check.js:** `deviceApp({ id: 'padsettings' })` is inside `if (PAD_ON)`, made once. No change expected.
6. **Words:** the door toast (15b 17441) already switches words when `PAD.used`; nothing else on screen changes until a pad
   button is pressed.
7. **The Claude app:** unknown whether its page passes controllers through (the plan's risk 1). The user plays the
   exported file in a browser, so this only matters for the published Playtest page.

## 5. Open questions (recommended answer first)

1. **Sound for a pad-only player:** start it from the first pad press if the browser allows (recommended), with a
   once-only "Sound starts at your first tap" note where it doesn't; or leave sound to a touch.
2. **Time clock Undo with a pad:** land on the × during the 5 s Undo window (recommended: keeps the touch layout, a double
   A can't undo); or land on Undo as the screen does now (a deliberate second A undoes).
3. **Dev mode by pad:** add the Dev card to the screen-edge buttons when `#dev` is in the link (recommended: the user and
   testers use Dev mode); or leave Dev mode touch-only.
4. **Typing with no keyboard beyond the name (memos, Dev search):** leave as is (recommended; the user's answer to plan
   question 6 was about the name); or an on-screen keyboard (about 4 hours, the plan's estimate).
5. **Download / Copy / Load a save file:** test on the user's real pad before the switch-on (recommended); if a phone
   refuses from a pad press, the one-line hint in Wave C is enough.
6. **Merge order:** A, B, C in parallel from claude/staging-p5s6, merged A then B then C (recommended: A's and B's
   section 26 stretches don't meet; C is outside section 26).
