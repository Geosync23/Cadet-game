# Handover: social engineer (Pillar 3, C4/C5)

Written by session_01DzZ669spGpdSdVMYzUog2N while still working (ahead of the 70% rule), so a fresh session can pick up. Read CLAUDE.md, DEV_NOTES.md ("Social life (section 20)") and plans/pillar3-plan.md (Part 3, "How news spreads", favours) first.

## Role, branch and builds
- Branch `claude/social`, builds 0.36.x. Last: **0.36.13** (0fdf48d), fully checked. Based on ship integration 0.41.5 (merged at 0.36.7).
- I own section **`// 20. SOCIAL`** in starship-cadet.html (after section 18, before `// 6. CAMERA`) and `social_check.py`.
- Hooks outside section 20 (one line each): the main loop calls `socialTick()` after `eventsTick()`; New game calls `socialNew()` after `playerNew()`; section 10's `tapCrew` calls `if (typeof chatOpen === 'function' && chatOpen(a.p)) return true;`.
- Report to the lead (now session_015QoyPWBdMPM4ywf5W2jMMs) with send_message after each push.

## What's built (DEV_NOTES has the detail)
- 0.36.0: on paper. `SHIP.rel` (relAdd/relTier, tiers 0/10/30/60/100), crew affinity `SHIP.aff` (Int8Array, 2,701 pairs, drifting hourly from `planWhere` room groups), the news model (`NEWS`, `SHIP.knows`, `newsAdd`, `newsKnownBy`, `playerHeard`), gossip from birthdays, traditions, habits, faults and pairs; `socialTo(t)` catches up by the hour; saved as `save.social`.
- 0.36.1: chat cards (`chatLine`, `chatOpen`, `chatDo`, `CHAT_SKIN.draw` for the device skin). 0.36.2: time together (meal +3, work +6). 0.36.3: favours on section 17's favour API; Ask about by topic (the roster's `about`). 0.36.4: friends wave you over (`#seek`). 0.36.5: chatter bubbles (`bubbleSay`). 0.36.6: `crewContacts`, `newsFeed`. 0.36.7: merge + `affinityPlan`. 0.36.8: the device's Crew app. 0.36.9: Crew badge on tier up, `shipNews`. 0.36.10: story arcs (Tomas, Pell, Rina). 0.36.11: small dramas (feuds). 0.36.12: Crew app map/meet-up buttons, `where.placeId`. 0.36.13: kept/missed appointments.

## Shared formats others rely on
- `relAdd(id, why, pts)`, `relTier(id)`, `REL_NAMES`, `REL_PTS` (events engineer calls `relAdd(id, 'meeting:<id>', pts)`).
- `newsAdd({ id, about, lines, weight, seed (ids, 'dept:<d>', 'all'), born, kind, event, life })` (events engineer feeds ion-storm news).
- `affinityPlan(a, b, d)`: pure (affStart, memoised). The sim engineer (session_01R6RBwwBM9aorpsqDCrztDU) builds seating by friendship on it. **Never make it read live affinity**: plans would differ between runs.
- `crewContacts()`, `newsFeed()`, `shipNews(limit)`, `deviceApp('crew')`: the device engineer (session_01LGbDXmiNuSmR6dPGjRj8mX) draws Maps and the Ship news from them.
- Flags on appointment objects: `a.socKept`, `a.socSaid`.
- schedU keys 600-642 are section 20's.

## Loose ends
- Privacy match with the device's Maps (0.35.9): Maps hides anyone asleep or washing; my Crew app's detail page and `crewContacts().where` still show them. Make `crewWhere` return null for act `sleep`/`wash` (one line) when the lead next gives work.
- Seating by friendship is live in the sim engineer's 0.26.18: about 19% of seats are next to a friend. No starting pair is at <= -30, so their "keep rivals apart" rule never fires; if the user wants visible rivalries, make the clash penalty in `affStart` bigger (for example -12 to -30) and re-run social_check. `shipDay(d).occ.who` (person -> [[from, to, placeId]]) can tell who sat with whom.
- **Pell's show:** done in 0.36.14 on the events engineer's eventOneOff (0.34.13). Re-test it once their build is merged into the integration.
- Merge ship integration 0.41.6 when published (it has Appointments and the device).
- On hold until the user plays the check-in build (the lead's call): arcs for the officers, tuning numbers.
- Friends who wave you over don't walk over yet (it needs a hook in section 10's crew agents, the sim engineer).
- Rivalries are rare (none in 14 days on paper; clashing pairs need about a month). Tune `socialHour`'s clash drift if the user wants more drama.
- Gossip is thin on days with no tradition or birthday; more sources (guests arriving, jobs finished, meals) would help.

## Gotchas
- Section 20 is placed before ROSTER (section 9) in the file: everything must be lazy (`socInit()` on first use). Load-time code must not touch ROSTER.
- In tests, call `socInit()` **before** `setShipNow(...)`, or the social clock starts at the jumped-to hour and nothing runs.
- `socialHour` calls `machinesNow()` when the hour's machine record is missing; keep it that way so faults are read hour by hour.
- Chatter only picks speakers well inside the screen; the bubble itself is section 8b's.
- The auto-mode classifier sometimes blocks long chained shell commands or a commit; plain single commands go through.

## How to test
- `CADET_CHROME=/opt/pw-browsers/chromium python3 social_check.py BUILD.html [DAYS]` (about 2 minutes).
- The full set before each push, one at a time: social, deck, day 1, player, events, interactions, food, machine, then cadet_test against the previous build. Copy the build to a scratch file first, so editing doesn't change what's under test.
- Feature tries used ad hoc scripts on cadet_test's `Game` class (open a card with `chatOpen(p)` after pushing a fake `{ p, x, z, settled }` into `DECK_CREW` beside the player; drive buttons with `chatDo(id)`).

## Open questions for the user
- Are the relationship numbers right once played (how fast Tomas becomes a friend; favour odds 0.2-0.45 a day)?
- More drama (rivalries) or keep it gentle?
- Which officers' arcs next (the plan: Captain, Vance, Calder, Brennan, Holt, Saruth)?
