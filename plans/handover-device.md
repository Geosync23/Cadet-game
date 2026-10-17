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
| 0.35.14 | a6e072b | `{ app: 'maps', do: 'person' }`; deviceLoad keeps other sections' appointment fields (socKept, socSaid); CRT made cheaper (flicker on ::after, will-change, contain: paint, Maps plan kept, dots redrawn) |
| 0.35.15 | 4f69bde | Only the Device button opens it: the bottom-edge swipe (which opened it while steering) is gone; device_check runs a day of reminders/tips/notices/address/dialogue/invitations and asserts it never opens |
| 0.35.16 | bded336 | Maps shows no people; new Roster app (everyone by department, people you know first, where they are via whereIs, "In their quarters" for sleep/wash/locked cabins, Go there); Maps' person links open the Roster |
| 0.35.17 | a1de068 | Days off: section 19's playerShiftOn stand-in removed (read via `devShiftOn`); Day off in Schedule, strip and Calendar once section 14's `playerShiftOn` lands |
| 0.35.18 | 22839e5 | The Schedule lists only what really happens (Monday's made-up Works briefing gone); device_check checks a week of items against the crew |
| 0.35.19 | e2f6658 | A need's bar pulses while section 15's needPulse(k) is true |
| 0.35.20 | 19833c1 | From 0.41.10; device_check's pulse check sets section 15's real NEED_PULSE |
| 0.35.21 | afe6f08 | Pillar 4: locked until handed over (section 15's deviceLocked/deviceLockedTap), the first switch-on ('boot', SHIP.device.booted), Settling in (section 21's SETTLE) |
| 0.35.22 | 459c534 | Pillar 4: season (section 18's seasonOf), reputation in Record (section 20's repView), keepsakes in Wallet, Left the Wren in Roster (movedOn/movedOff) |
| 0.35.23 | 89ab0ca | Pillar 4: deviceChoose(view, onPick) for section 13's New game question |
| 0.35.24 | 8b502d4 | Reviewer 2's fixes: settleSure resets on leaving Settling in or closing; keepsake and leaver rows guarded |
| 0.35.25 | (this push) | Reviewer 2: deviceChoose refuses while the panel or a meeting is up; a meeting cancels a pending question first |

Loose ends now: 1-7 are done (days off wait only on section 14's playerShiftOn). User's answers (2026-10-16): no pull tab, the Device button is the only way in; no people on Maps; a Roster app for where people are; Saturday and Sunday off. Still open: 8 (a real phone; the performance engineer was asked to check the CRT skin's paint cost on a real GPU). Bottom-edge swipe-up fights the iPhone home bar; the Device button is the main way in.

Gotchas added: a group meeting is one appointment per person (each a seat of their own) sharing `grp`, so section 14 needed no change; `deviceTick` keeps the group together (one kept → all kept). The full suite takes 25-40 minutes a build; run browser checks one at a time. For testing against the social branch's newer section 20 without merging, splice its section 20 into a scratch copy (between the `// 20. SOCIAL` and `// 6. CAMERA` headers).

## State at 0.35.25 (device engineer 2, retiring)

- **Lead:** session_01PJtmxWgAPLebXSZKP6ZRpG (from 2026-10-17 ~02:40; before: session_01PxXKwc5mkC7tV5MPi3p7PP). Chain of command: the user → the lead → everyone; helpers never contact the user. **Build master:** session_012K7RZ3oSX2vpBb1rR66MBh (report each push to both). Reviewer 2 reviews this branch.
- **Pillar 4 seat 7** (plans/pillar4-plan.md Part 6, brief 7): all done. "The Crew app's 'what you know' without counts" was section 20's (social B's knowBlocks, 0.39.0), closed. 0.35.21-0.35.23 are queued for ship integration 0.60.1; 0.35.24 and 0.35.25 are the review fixes after them. deviceChoose returns false when it can't ask (a meeting is up): section 13's New game should treat that as "try again". Reviews: reviewer 2 (session_0142TQw4ke8caPSyAC93VT98, notes on claude/reviews-2 plans/reviews/device-*.md).
- **Who owns what next door:** section 15 player engineer 3 (session_016EJg9DempByUCWwpszyWmV: deviceLocked, deviceLockedTap, NEED_PULSE/needPulse, the button relabel); section 21 onboarding engineer (session_01KaHzfqSqF8B4bkNFrH1tsx: SETTLE, SHIP.intro, introOn, introEnd, introSkip, introArrived); section 13 sim engineer (session_01R6RBwwBM9aorpsqDCrztDU: playerShiftOn, New game wiring to deviceChoose); section 18 traditions (seasonOf); section 20 social A (session_012pK2XVi5UhqEd28fakYk68: repView, keepsakes, movedOn, movedOff, crewContacts, the Crew app; shapes confirmed 2026-10-17, they'll warn before changes).
- **New hooks this round:** apps may have `hidden: () => bool`; `deviceDo` lets an app's act('open') return another app id to show; `devTry`, `devLocked`, `devSeason(Line)`, `settleList`, `settleDone`, `settleGoal`, `rosterWhere`, `rosterPeople`, `deviceChoose`/`devChosen` (DEV.choose).
- **Testing other sections' real code:** make a scratch worktree, merge their branches (only the two build lines conflict), and run device_check on it; device_check's cases use stand-ins when a function is missing and the real state when it's there (a top-level const can't be replaced by a window stand-in: set its state instead).
- **cadet_test:** the player engineer's #needFx notes are hidden in cadet_test from player-needs 2806e6d (0.60.0); before that, use a scratch copy that hides #needFx.
- **Open with the user:** nothing pending from section 19.
- **Next for a successor:** nothing assigned. Watch for: section 13 wiring New game to deviceChoose (sim engineer), the real-phone paint check of the CRT skin (performance engineer's notes in DEV_NOTES 0.35.14), and any device rows in Pillar 4 waves 3-4 (plans/pillar4-plan.md Part 6).

## Device engineer 3 (from 2026-10-17, session_01SskqNx45iEGyQq2W9Fjg5Y)

- **Lead:** session_01KPJMYjXAPkNUcrQ8VRkhLE (report only to it). Reviewer 2 reviews each push.
- **0.35.26 (b081853):** claude/device fast-forwarded onto ship integration 0.60.1 (it already held 0.35.25), so the branch now has sections 13-21 and intro_check.py. `tipSeen(id)` for section 21 (onboarding engineer told), and `Number.isFinite` for the keepsake / leaver days (reviewer 2's "Day null" nit). device_check, intro_check OK; cadet_test ALL IDENTICAL vs 0.60.1.
- **Setup in a fresh container:** `pip install playwright`, then three.js r128 into /tmp/cadet-work/three (see DEV_NOTES "Testing"); `CADET_CHROME=/opt/pw-browsers/chromium`.
- **0.35.27 (4979eec):** calls home in Mail with social B2 (session_014A3w2gK8FBNWs66YC3LfME, section 20c): "From home" group from `homeFolks()`, Play while `mailPlayable(m)` → `mailPlay(m)`, device closes on true (helpers `devHomeFolks`, `devPlayable`). Home's servery queue line has no guessed wait (lead, for the user). Reviewer 2 passed 0.35.26.
- **0.35.28 (b12fe50 + a250452; the wip commit was pushed early by mistake):** the Needs page redesign the user approved: section 15's NEED_ICON / NEED_COL / NEED_AMBER under NEED_LOW per bar (bars block items take optional `icon`, `color`), short effect lines from NEED_FX (`devFxLine`, `DEV_FX_WORD`). Tested on a scratch merge with claude/player-needs 1d647a3 (7a99461 alone doesn't load). Screenshots plans/shots/device-needs-*.png (`*.png` is gitignored: `git add -f`).
- **Reviews:** reviewer 2 passed 0.35.26, 0.35.27 and 0.35.28 (no fixes). Social B2: "From home" matches by sender name only (their rule: home names stay distinct from any other sender).
- **Next (from the lead, the user's feature):** schedule heads-ups, 0.35.29+, starting after the usage reset (~07:32 UTC, self-reminder trig_01XEPaWF5TjwMcrEaqU9TV7B). Build on section 19's Calendar reminders (`calendarRemind`), not a second system; cover every Schedule item (traditions, events, meetings, appointments); a short toast ~15 ship min before ("Tiles night starts in 15 min · Bow lounge", tap opens Schedule / sets the goal arrow) and a gentle one at start; only real items, one toast at a time, queued behind cards, meetings and sleep, no repeats, a Settings switch, ON by default. Read-only hooks with traditions engineer 2 (session_01WEEoe5DyRegEqVMZgKRHWB) if needed. Phone screenshot to the lead; reviewer 2 reviews.
- **Rule (the user):** refresh this note right before handing over. Section 15 is player engineer 3's: don't edit it on claude/device.
- **Gotcha:** a `git add` that fails stops a `&&` chain but not a push on the next line: keep the push in the chain.
- **device_check fixes owned by the combine (build master, 0.60.3; the lead, 11:01):** two test-only changes live in the combined builds (claude/cand-0603 9cea94c), not on claude/device: (1) "Mail: From home, Play on a recorded message": with section 20c's real home code, the check queues a real waiting recorded message from Gran (`homeC('gran').msg`) and puts the home state back after; without home data it only checks "no Play on plain mail" (social B2's claude/social-stories 788b4af, reviewer 2b PASS); (2) the heads-up cases count only the test's own appointments (`HU_Q.filter(q => q.key.startsWith('appt|')).length`): a real Late piano heads-up can share the window (the same as claude/device 24f1920). claude/device's newer device_check already has (2) and needs only (1)'s three edits (its block is near line 262); the build master applies them in each combine until a device engineer carries them.
