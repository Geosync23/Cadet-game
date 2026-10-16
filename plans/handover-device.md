# Handover: the device engineer (section 19, your personal device)

**Update (device engineer 2, session_01LGbDXmiNuSmR6dPGjRj8mX, builds 0.35.8-0.35.13):** see "Device engineer 2" at the end; the lead is now session_015QoyPWBdMPM4ywf5W2jMMs.

Written 2026-10-16 at device build 0.35.7 (`claude/device`), for a fresh session taking over this area. Read it with `DEV_NOTES.md` ("Your device (section 19 ...)"), `plans/pillar3-plan.md` on the lead branch (Part 1, "The device look", "Shared formats", workstreams C1, C2, C3, C11, C13) and `design-doc.md` ("The player").

## Role

- **Who:** the device engineer, Pillar 3. Workstreams C1 (the device, its two layers, the CRT skin), C2 (the apps), C3 (the Appointments app), the look of C13 (tips) and the framing hook of C11.
- **Branch:** `claude/device`. **Builds:** 0.35.x (0.35.0 to 0.35.7). Started from ship integration 0.41.4 (c7598df). The lead merges into `claude/ship-integration` (0.50.x).
- **Section:** `// 19. DEVICE`, which sits **before** section 15 (just after 14), so sections 15 and 17 can register at load. Plus small hooks listed below.
- **Lead:** session_01WHXNp9A1WHAD2EHJw384Qp. Report after each push with send_message.

## Builds

| Build | Commit | What |
| --- | --- | --- |
| 0.35.0 | bdbcc31 (pushed) | Two layers: `deviceApp`, VIEWs, `deviceDo`, `deviceNotify`, `deviceOn`, `DEVICE_SKIN`; the `device` shim; Home, Needs, Jobs, Mail, Wallet; device_check.py; player_check's mail lines |
| 0.35.1 | 2334919 (pushed) | The CRT skin, phone sheet and wide panel, three phosphors, Settings |
| 0.35.2 | f9062ef (pushed) | Schedule, Calendar with tradition reminders, Jobs tracks only |
| 0.35.3 | 196f520 (pushed) | Maps (SVG plans, Go there → setGoal) |
| 0.35.4 | 5c010ca | Memos, Ship, Record, Crew shell, tips, phone camera framing |
| 0.35.5 | 55be279 | Dialogue panel and chat card in the CRT style, `playerShiftOn`, `DEVICE_SKIN.ink`, `deviceOn('phosphor')` |
| 0.35.6 | 01acecc | Appointments on section 14's `apptReply`; dialogue on section 18's `deviceDialogue(view, onTap)`; free seats; tips wait for meetings |
| 0.35.7 | 19c6182 | The Captain's address banner (`deviceAddress`) |

Check the branch for which of 0.35.4–0.35.7 were pushed (they were pushed together once the full suite passed on 0.35.6).

## What I own (all in section 19)

- **Apps** (`deviceApp({ id, title, short, icon, order, badge, view, act })`): home, schedule (10), appointments (12), calendar (15), needs (20), maps (25), jobs (30), mail (40), memos (45), crew (50, a shell), ship (60), record (70), wallet (90), settings (99).
- **The skin** (`DEVICE_SKIN`): open, close, draw, button, wide, ink, tip, dialogue, address, chat, notify. The only DOM code. Block kinds: text, list, bars, buttons, map (SVG), form, dom (the shim).
- **Saved** in `save.device` (SAVE_EXTRA, read defensively by `deviceLoad`; SAVE_V stays 2, agreed with the lead): `SHIP.device = { memos, tipsSeen, appts, settings: { phosphor, fx, tips }, calendarRemind: { on, ahead, morning, per } }`.
- **Calls other sections use:** `device.refresh()` (section 15 each ship minute, and others), `deviceOn('open' | 'close' | 'phosphor', fn)` (performance engineer's pose and prop), `DEVICE_SKIN.ink`, `deviceFrame(on)`, `tipShow(id, text)` (interactions engineer), `deviceDialogue(view, onTap)` and `deviceAddress({ from, text })` (events engineer), `CHAT_SKIN.draw = DEVICE_SKIN.chat` (social engineer, set after load), `deviceDo({ app: 'appointments', with })` (social engineer's Meet up).

## What I read from others (all guarded or runtime only)

- 15: `SHIP.player.needs`, `NEED_KEYS`, `NEED_LABEL`, `needEffects`, `needsLine`, `playerSpeed`, `playerFx`, `ACT`, `SHIP.mail`, `mailSend`, `mailUnread`, credits, locker, carry, work, cart, `CART_STEP`, `cartDest`, `jobsOn`, `jobMins`.
- 15b: `setGoal`, `clearGoal`, `IX_GOAL`, `ixJobStep`; `SHIP.player.track` (null = off; the interactions engineer acts on it).
- 14: `MEALS`, `WEEKDAYS`, `weekday`, `schedRoomLocked`, `schedPeople`, `shipDay(d).occ`, `apptReply` (sim engineer; it sets 'kept' / 'missed' in `apptTick`).
- 17: `jobsBoard`, `myJob`, `jobCard`, `jobTier`, `PLAYER_TIER`, `machineById`, `shipHealthRows`, `SHIP.jobs`.
- 18: `upcomingTraditions(a, b)` (falls back to `eventsOn`).
- 20: `relTier` (who you can ask), `CHAT_SKIN`, `chatDo`, `chatClose`.

## Ready for you from the social engineer (session_01DzZ669spGpdSdVMYzUog2N, section 20)

- `crewContacts({ all })` → `[{ id, name, role, dept, tier, tierName, pts, toNext, met, lastTalk, known, where: { deck, room, act } | null }]`, closest first; `where` only when the Maps rule allows (acquaintance or more, or on public duty). Use it for the Crew app (replace my shell, unless section 20 registers its own) and for people on Maps.
- `newsFeed()` → `[{ id, line, from, at, kind }]`, newest first: the Ship app's news feed. Also `shipNews(limit = 20)` → `[{ text, from, at }]`, newest first (0.36.9). Section 20 now registers its own Crew app (0.36.8+, icon 'crew', order 50), replacing my shell.
- `relTier(id)`, `REL_NAMES` for labels. They'll call `deviceNotify({ app: 'crew', text })` when a tier goes up (I said yes).
- The friend chip `#seek` (right edge) can be restyled in the CRT look with CSS.

## Loose ends

1. The user hasn't chosen the phosphor yet (default Wren cyan); screenshots in `plans/shots/device-*.png` for check-in 1.
2. Days off: `playerShiftOn(d)` returns true; the lead is asking the user.
3. Maps doesn't show people yet (needs relationships: acquaintance or on duty in public).
4. Calendar: "tap a day to add it to Schedule or make an appointment that day" isn't built.
5. Appointments: a meeting with two or more people, and picking a place from Maps, aren't built. Strangers are only filtered by `relTier` once section 20 provides it.
6. The "Quiet off shift" setting (work notifications as badges after 17:00) isn't built.
7. Ship news (the social engineer's news model) isn't in the Ship app yet.
8. Swipe-to-open and tap-the-ship-to-close are untested on a real phone.

## Gotchas

- **Section 19 runs before 15–18.** Anything that runs at load must not touch their `const`/`let` names (TDZ). `deviceTick` waits for `DEV.live` (set by a `setTimeout(0)` after load) because `eventsOn` is in section 18.
- **Don't run two browser checks at once**: page loads time out.
- On a phone the framing shows more of the deck, so the first open can upload a few shared geometries once (device_check checks no growth on reopening).
- `deviceDo` with no verb opens the app and calls `act('open', action)`.

## How to test

`CADET_CHROME=/opt/pw-browsers/chromium python3 device_check.py BUILD.html` (about 2 minutes), then one at a time: player_check, interactions_check, deck_check, day_check 1, cadet_test against the previous push (the device is closed there, so expect ALL IDENTICAL).

## Device engineer 2 (0.35.8 onwards)

| Build | Commit | What |
| --- | --- | --- |
| 0.35.8 | ae506b9 | Ship news in the Ship app (`devNews()` over section 20's `shipNews`) |
| 0.35.9 | a86d7a7 | People on Maps (`mapPeople`, `mapDots`; `{ app: 'maps', who }`) |
| 0.35.10 | 16a4291 | Calendar day → See the day / Make an appointment; Pick on the map (`mapFor`, `apptRoomPlace`); group meetings (`grp`, `apptSpots`, `apptGroups`, `apptBook`) |
| 0.35.11 | cdfcdb1 | Quiet off shift (`settings.quiet`, `DEV_WORK_APPS`); #seek chip in the CRT style (`html[data-ph]`); Maps hides sleepers and lists only people you know |
| 0.35.12 | 4a1d044 | Phone review: tap-to-close on a tap, `pointercancel`, a 44px bezel grip, no rebuild when the VIEW is unchanged |
| 0.35.13 | 61ebe6a | Ship integration 0.41.6 merged in |

Loose ends now: 1 (the phosphor is chosen: Wren cyan), 3, 4, 5, 6, 7 are done. Still open: 2 (days off), 8 (a real phone; the performance engineer was asked to check the CRT skin's paint cost on a real GPU). Bottom-edge swipe-up fights the iPhone home bar; the Device button is the main way in.

Gotchas added: a group meeting is one appointment per person (each a seat of their own) sharing `grp`, so section 14 needed no change; `deviceTick` keeps the group together (one kept → all kept). The full suite takes 25-40 minutes a build; run browser checks one at a time. For testing against the social branch's newer section 20 without merging, splice its section 20 into a scratch copy (between the `// 20. SOCIAL` and `// 6. CAMERA` headers).
