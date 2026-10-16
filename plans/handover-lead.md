# Lead handover (2026-10-16, ~15:20 UTC, Pillar 3 in progress)

From the outgoing lead (session_01WHXNp9A1WHAD2EHJw384Qp) to the new lead. You are the PROJECT LEAD for Starship Cadet. Read this, then CLAUDE.md, TEAM.md, `plans/pillar3-plan.md` (the AGREED plan), design-doc.md's "The player", "Social life", "Ship-wide events" and "Open questions", and skim DEV_NOTES.md's build table.

## The user

New to Claude Code and git: plain language, no jargon, short updates. Active today. Every request comes through the lead. They like PushNotification pings when something they wait for is ready (a new build on the link). PRs to `main` only when they approve; they approved and merged 0.41.4 (PR #2). Rules they set today:
- **Hand over before memory fills** (CLAUDE.md). This brief exists because the user had to ask: (Updated by the user later on 2026-10-16: helpers at ~70%; the lead judges before each bigger step whether it has room, and hands over first if not.)
- **Resume fast after a usage limit**: keep a REPEATING hourly check-in (create_trigger cron). Mine is trig_01NKBjg2UJa1tXFjWU5Zd29L ("Lead check-in (repeating)", fires :53 into THIS old session) — DELETE it and create your own pointing at your session. If a limit is coming, also add a one-shot send_later just after the reset time.
- **At most ~5-6 helpers actively building at once** (the user's "be more careful" after the 15:10 reset). Others on standby answering questions only.

## Builds and the playable link

- `main` = 0.41.4 + all docs (PR #2, 4b2ee4f). `claude/lead-pillar1` restarted from main (shared history now).
- `claude/ship-integration` = **0.41.5** (8027d4b, all nine checks pass): the player carries a tray (user's note), jobs taken and turned in at the board (TURN_IN on), chore walk, plus Pillar 3 groundwork, mostly inert.
- Playable link https://claude.ai/artifact/XCcqMGBhAa149cf7s4Mc8y: version 12 = 0.41.4. **0.41.5 is being republished** by a subagent of the old lead; if it finished, the link is version 13 = 0.41.5 (check with Artifact read/list; if not, republish: steps in plans/handover-deck6-architect.md section 3, or delegate to a fresh helper — the publish needs a full Read of the live ~13k-line page). Then ping the user.
- Morning report: https://claude.ai/artifact/VDETEN1m2yWca1C2vxFKkU (plans/morning-report.html). Pillar 3 pitch (agreed): https://claude.ai/artifact/A3HL2vuWXa1cguTQxnBbiZ (plans/pillar3-pitch.html).

## How merging and checking works now (fast)

- Combine in a local worktree (the old lead used /home/user/si-work, branch lead-wip; recreate with `git worktree add -B lead-wip <dir> origin/claude/ship-integration`). Tools in tools/: resolve.py, fixrate.py, kitdup.py. ALWAYS reset the HUD line + GAME_BUILD after merges: clean merges silently bring helpers' build numbers in.
- Push the unchecked attempt to **`claude/integration-test`** (user-approved test branch), then start short-lived **check-runner sessions** (create_session, source_revision claude/integration-test, model claude-sonnet-5-5, tag cadet:check-runner) each running 1-3 checks and reporting by send_message; archive them after. ~8-25 min total instead of ~30-60. player_check takes ~25 min alone.
- Checks: deck_check, day_check BUILD 1, food_check, machine_check, player_check, events_check, interactions_check, social_check, cadet_test old new. Setup: pip install playwright; three r128 in /tmp/cadet-work/three; CADET_CHROME=/opt/pw-browsers/chromium. Only builds where ALL pass go to ship-integration.
- When a combined check fails, have the owning helpers diagnose on their own machines from integration-test (it worked well: the food-supply bug was found that way).

## Queued for 0.41.6 (base 8027d4b)

- device 196f520 (0.35.0-0.35.3: two layers, CRT skin — the user chose **Wren cyan** as default, Schedule/Calendar with tradition reminders, Jobs as tracker, Maps) — 0.35.4-0.35.6 coming (Memos/Ship/Record/Crew shell/tips/framing, dialogue panel + chat card CRT, Appointments).
- social fbef6ff (0.36.1 chat cards, 0.36.2 time together, 0.36.3 favours).
- ship-events 7248bce (0.34.9 meetings at run time, eventFeel) — storm still `draft: true`.
- ship-systems 1d32621 (0.33.26 blackout thread score, event jobs per hour). Decision: drop `stormTrays` from the storm data (galley's cartTrays is the one tray run) — events engineer told.
- galley 0.29.21 pending (scores 'spoiled' and 'bridgeHungry'); then events engineer prepares the switch-on (draft off) as its own push.
- crowd-render 07c2a9b (0.27.14 civilian outfit, 0.27.15 punch/stretch, 0.27.16 prop follows phosphor).
- player-needs 42de361 (0.28.16 texts: jobs taken at the board).
- crew designer a56b3a1 (0.16.9 about tiers/topics, 0.16.10 rosterSpec civilians).
- decks-p3 27f50d9 (0.38.1 event dressing/traces); 0.38.2 coming (ready room, Captain's dining room, gym kit).
- **DO NOT merge sim 0.26.14 (guest schedules)** until a fresh sim engineer fixes it against the real GUESTS (day-of-year arrive/leave, null arrive for event guests, GUEST_TEMPLATES). See plans/handover-sim.md on claude/sim-engineer (f2f4b9f).

## Team (details in TEAM.md)

Active (6): device session_014TpEMbWarRFJM8BHC9WM8c (claude/device 0.35.x), social session_01DzZ669spGpdSdVMYzUog2N (claude/social 0.36.x), events 2 session_01GW9QtevJxaMQzzCGPBHaxb (claude/ship-events 0.34.x), interactions session_01GGbtSiy4tDygCzrSUBDMYa (claude/player-interactions 0.37.4 = job-loop tips), systems session_01FtwFYLBjAB9zFvPSpLezaR (claude/ship-systems 0.33.x), deck architect session_014PT5L2QxXYoVhqFP7qhj3y (claude/decks-p3 0.38.x).
Standby: performance session_01TiBtENVFJV7RqEQ7YkxH1Z (next: shipFeel for the storm's felt-everywhere, CRT phone review), player session_01BQjtEzvKXuvPZNzGRRRwpZ, galley session_01AVGVnj4Q1jFmVoD6xi5asT (doing 0.29.21 then standby), crew designer session_01JScnVG158eYAHYvKDz3jZG.
Retired today: sim session_01S5xTHRBpJ9kqytfrwKipUG (handover written), events 1 session_01YXDbUmtB1mg4kiJyuToqKA, three architects, Pillar 3 planner, old lead session_0158BCCswtdujm3t5d2LXsFz.
**To hire next** (when a slot frees): a fresh SIM engineer — first the guest-schedule fix above, then C7 event routines (storm keys in handover-sim.md: doubleShift, patrol, closed, stayIn, rush; needs; the bow-lounge party via gatherSpots('bow-lounge')).

## Decisions made today (beyond the design doc)

Ship traditions = official name (Calendar reminds ~30 ship min ahead); jobs taken and turned in at the board, device only tracks; favours in person (user confirmed); first tips for the job loop; see your character use the device; device colour Wren cyan; meetings with dialogue (never cutscenes); full event order kept (7 main + 6 short); crew Works juniors are Tier 2, player Tier 1; jobs left for the player ~5.6/day; galley owns cold-store accounting; thread owners: blackout = systems, spoiled + bridgeHungry = galley, calls = events; traditions pause during a ship-wide event's onset/escalation (birthdays kept); afterglow to end of day 5. **Open, asked the user:** should the player get days off (suggested two a week like a Works junior)? Device engineer reads playerShiftOn(day) (default true) so a rota can drop in.

## Next milestones

0.41.6 (above) → switch the storm on once galley scores land and all checks pass → **Pillar 3 check-in 1** with the user (device in cyan with its apps, jobs at the board, tips, chats/favours/relationships) → the full ion storm (check-in 2).

## Lessons

- A one-shot reminder that fires while the account is limited is lost: use a repeating trigger.
- Clean merges carry helper build numbers: always reset build lines.
- `const` functions can't be stubbed by tests; tests should use a test hook (the galley's GALLEY_TEST pattern).
- Two helpers adding the same safeguard (double counting) or the same job (storm trays): decide one owner fast.

## Update by the new lead (session_015QoyPWBdMPM4ywf5W2jMMs, 16:20 UTC)

- Lead check-in: trig_01Kr24HNvp976B4MapBpEqRo (hourly at :15, into the new lead's session). The old one is deleted.
- Playable link: version 13 = 0.41.5 (done by the old lead's worker).
- **0.41.6 attempt on `claude/integration-test` = 5555236**, built on 8027d4b in /home/user/si-work (branch lead-wip): crew designer a56b3a1, crowd-render 5add99d, device 985ff28 (0.35.7, final), player-needs 72f5646 (0.28.17 = the user's treadmill fix), social 944dbc7 (0.36.6), ship-systems 7b12687, ship-events 78c6062 (0.34.10), decks-p3 01852f5 (0.38.3), galley 7ab48d1 (0.29.21), player-interactions 6368760 (0.37.4). stormTrays removed; events_check.py test-only fixes (stand-ins in game scope, #devDlg accepted). Passed: deck, day 1, food, machine, events, device. Running in check-runner sessions: player_check (session_01CHiFN5aUx65yS32e2ocPkp), interactions + social (session_0137d9jfVTbwg51LjFmuj5RK), cadet_test vs 8027d4b (session_01UFMJTiPJvYGpZoTSnYAjNA). All pass → push to ship-integration, republish the link, ping the user (they're waiting for the treadmill fix), archive the runners.
- **Queue for 0.41.7:** ship-events 0.34.11 (occasions) + **0.34.12 storm switch-on** (head of claude/ship-events after 3da517b); social 267d881 (0.36.7-0.36.12); ship-systems 155c95f (0.33.28 traysArrivedAt, 0.33.29 volunteered storm jobs); player-needs 4fbdd17 (ixHold hook, PNGs); galley 0.29.22 (bridgeHungry until trays arrive; coming); player-interactions 0.37.5 (chore props; coming); sim 0.26.15 (guest fix; coming — the sim brief says merge it only once fixed).
- New hires: sim engineer 2 session_01R6RBwwBM9aorpsqDCrztDU (guest fix → storm routines → friendship seating), device engineer 2 session_01LGbDXmiNuSmR6dPGjRj8mX (Ship news, people on Maps, Calendar appointments, Quiet off shift, phone review). Retired: first device engineer (handover-device.md), old lead.
- Decisions: bridgeHungry counts until trays arrive (fallback: until 18:00); the deck architect added a 'conference' visit; social holds officer arcs and tuning until the user has played the check-in build.
- Still open with the user: days off for the player.
- The account showed a seven-day usage warning (resets Sat 08:00 UTC). If work stops, the hourly check-in resumes it.
- **16:55 UTC: 0.41.6 = 9bb9409 on claude/ship-integration** (all checks pass; player_check's treadmill test from 0.28.18 skips treadmills crew are using). Republish of the link to 0.41.6 in progress (lead's background worker). 0.41.7 waits on galley 0.29.22 and sim 0.26.16; heads then: events 4344612, social 907b16a, systems e894246, player-needs bf5b5af, interactions a12d159, decks 7d228c2 (0.38.4 patient beds), device 16a4291, crowd-render 2d0e1ed (note only).
- **17:02 UTC: playable link = version 14 = 0.41.6** (published by a fresh publisher session; a subagent can't do it, the two full reads don't fit — use a full session).
- **18:05 UTC: 0.41.7 attempt = a773bea on claude/integration-test** (storm ON; all queued heads incl. sim 17a7fca, events 981ef3a, device 74ba996, social f0d9615). Merge fix in section 18 eventTakeJob (always records wants:) — events engineer to confirm. Pass: deck, events, day 1/10/13, food. FAIL: machine_check (storm wears comms array to failing in the no-repairs run) — systems engineer on it (test change). Runners: player session_01DE4L7y4qaBavk3hMw8FtTC, interactions+social+device session_01R1oYAjYbNEaCXgUTEuF7CY, cadet_test session_01Vc7o2nmC5b4zk4iE7YPXuq. Device 0.35.14 (keeps socKept/socSaid on load) may join. Asked the user: device pull tab, strangers on Maps, days off.
- **20:10 UTC: resumed after the 5-hour usage limit (stopped ~18:15).** 0.41.7 attempt now d89a3f5 (adds systems' machine_check fix 0.33.30). Passed on a773bea game code: deck, events, day 1/10/13, food, interactions, social, device, cadet_test; machine_check fixed (systems ran it on the combined build). player_check + machine_check rerun: session_01DNiTv5qVwCo8aFRSkdrrV3. Then push to ship-integration, publish via a fresh publisher SESSION (not a subagent), ping. Queue for 0.41.8: sim 0.26.18 (7ef9c17, friendship seating), device 0.35.14+, events 0.34.15+ (diplomatic visit in progress), systems 0.33.31 coldCabins. Lead memory ~34% at 20:10.
- **20:16 UTC jobs out:** device 2 = pop-up bug (device opens by itself), Maps without people, new Roster tab, 'Day off' on Schedule; sim 2 = playerShiftOn (days off Sat/Sun); interactions = job board panel off screen + board always empty (user's bugs on 0.41.6); systems = coldCabins, then days-off jobs to crew if it fits; social = discourtesy thread; events = live greeting test, comet viewing (visit stays draft). All for 0.41.8. 0.41.7 waits on player_check rerun (session_01DNiTv5qVwCo8aFRSkdrrV3).
- **20:25 UTC, the user:** events engineer stops after the diplomatic visit (draft); comet + other events later. Priority now: the user's tweaks and the personal device, then check-in 1.
- **20:52 UTC: 0.41.7 = d89a3f5 on ship-integration** (all checks pass). Publisher session_01LibC3b2PPyHrg7asNMsEb1 → link version 15. Next: 0.41.8 merge (sim b623606, device f26f960+, interactions 55f2dc8+ (strict jobs pending), systems a9c41bd, social 3e50a6d, events (visit draft, 0.34.17+), galley/decks small asks).
- **20:58 UTC: link = version 15 = 0.41.7.**

## Handover-ready summary (lead session_015QoyPWBdMPM4ywf5W2jMMs, 21:20 UTC, ~53% memory)

Read this section first; the lines above are the running log.

**Builds.** ship-integration = **0.41.7 (d89a3f5)**, the ion storm ON. Playable link https://claude.ai/artifact/XCcqMGBhAa149cf7s4Mc8y = **version 15 = 0.41.7**. **0.41.8** is being merged by the lead's background merge worker into /home/user/si-work → claude/integration-test (from d89a3f5): sim b623606, systems a9c41bd, social 3e50a6d, device f26f960 (+ newer if the Works-meeting fix lands), interactions d62aee4, events 7966136 (visit DRAFT). Then check runners (player, social, device, cadet_test; plus whatever the worker didn't run), push to ship-integration, publish with a fresh **publisher SESSION** (a subagent can't hold the two full reads), PushNotification the user.

**What 0.41.8 has (the user's tweaks):** job board panel always on screen + jobs actually on the board (held until end of shift, cap 6, none on days off, day 1 from 06:00), ship health panel, two days off (Sat/Sun, playerShiftOn), Roster tab, Maps without people, no swipe-to-open (the pop-up bug), Day off on Schedule, friendship seating, discourtesy thread (inert), coldCabins (inert).

**In progress (for 0.41.9+):**
- Device engineer 2 (session_01LGbDXmiNuSmR6dPGjRj8mX, claude/device, ~35%): the "Works meeting" Schedule bug (Schedule listed a meeting that never happened) + device_check case; screenshots of Roster/Maps (git add -f); Needs row for the new bathroom need.
- Player engineer 2 (session_012J4ctzJgFRBaUFU5sJvega, claude/player-needs, new): bathroom need + toilets; "+25 Food" style feedback when a need fills; progress bars for every timed activity.
- Performance engineer (session_01TiBtENVFJV7RqEQ7YkxH1Z, claude/crowd-render, ~60%, LAST job): zoom-out limit so culling never shows; then final handover. Storm visuals (shipFeel) → a fresh performance session later.
- The working garden (design-doc "Dependencies"): galley engineer session_01AVGVnj4Q1jFmVoD6xi5asT leads (claude/galley-food, ~50%, plan approved: crops, growth by water/feed/light/tending, daily pick + harvest morning, produce in cold store, carry run, menus; steps 0.29.23-25); systems 3 session_01TqLepvhqDZRwFj7ZuLb6Xa (gardenAt, 'growlight' machines, gardenCarry job); crew designer session_01JScnVG158eYAHYvKDz3jZG (2-3 gardeners); deck architect session_014PT5L2QxXYoVhqFP7qhj3y (4-6 'work:garden' places); sim 2 session_01R6RBwwBM9aorpsqDCrztDU (gardener shifts, gardenDay). Herbs for the visit's dinner come from garden stock (later, inert).
- Standby: social session_01DzZ669spGpdSdVMYzUog2N (~51%), interactions session_01GGbtSiy4tDygCzrSUBDMYa (~51%), events 2 session_01GW9QtevJxaMQzzCGPBHaxb (done; close after 0.41.8 passes; plans/handover-events.md is final; comet draft in plans/comet-viewing-draft.js).

**The user's decisions today (all in design-doc):** device button only (no pull tab, never opens by itself); Maps without people + Roster tab; two days off Sat/Sun; jobs held to end of shift; bathroom need; need-fill feedback and progress bars; a garden that really grows food; zoom-out limit; events paused after the diplomatic visit (draft) — comet + remaining events later; helpers hand over at ~70%, the lead judges before each big step; the user allowed extra check runners to speed testing.

**Next milestones:** 0.41.8 out → 0.41.9 (bathroom, feedback/progress, zoom, Works-meeting fix, garden step 1) → Pillar 3 **check-in 1** with the user (device, Roster, jobs at the board, crew life, days off) → storm visuals (fresh performance session) → check-in 2 (play the full storm).
