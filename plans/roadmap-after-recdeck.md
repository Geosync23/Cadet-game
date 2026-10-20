# Roadmap after the rec deck (agreed with the user, 2026-10-19; step 2 changed 2026-10-20)

> **2026-10-20, the user: NO CUT for now.** After the split plan's two adversarial reviews (claude/split-plan `plans/split-plan-review.md`, claude/split-review-2 `plans/split-review-2.md`) and a full rehearsal (claude/split-rehearsal `plans/split-rehearsal-report.md`: 13 real merges replayed byte-identical, 689 merges swept, 20+ attack scenarios, a real GitHub check), both found the split brings no safety the new ways of working don't already give (clashes land in the same places; 393 of 508 past clashes were only the build number). Step 2 is now **the new ways of working on the one file** (option d): names_check.js, check_fast.sh, the exit-code fixes for 10 checks, cadet_test's stale-file refusal where it applies, the GitHub check, the build master sets the build number, early combining on a shared branch, labelled per-seat append slots in the file, a section finder (tools/section.py), plans/owners.md, plans/map.md, plans/backlog.md, DEV_NOTES' build table moved out, the whole-file copy kept. The rehearsal's tools are on claude/split-rehearsal; the split tools stay on the shelf and are reconsidered after Dev mode only if the numbers say so. GitHub emails the user on every failed run: settle the user's email setting before switching the check on.

The user: "I don't care about usage, we will get it there." Order:
1. Finish the rec deck 0.64.0 (see START-HERE.md).
2. **Split the game file** into pieces (crew, machines, decks, phone screens, content, ...) joined by a small build step into the one playable file. Proof: the joined file is byte-identical to today's. Plan page for the user first (it's a big move). Then a light clean-up of obviously unused code, one area at a time, with checks.
3. **Dev mode** (the user, 2026-10-20), after the split and clean-up: a hidden testing panel to move the clock forward (hours, days), set career progress (xp / rank), and start any ship tradition on demand to test it. Also (the user, 2026-10-20): **jump to any day of the career progression** (Day 0 to the career's end, Day 26 plus the visit finale), arriving with the career, rank, jobs and ship state a player would have on that day; and start any ship-wide event or jump to one of its phases (events plan F6). Plan page first. Built gated, so the normal game is unchanged with it off.
4. Pillar 5, Steps 5 and 6.
5. Ship-wide events, only those up to the end of the promotions (the user cut the rest), one at a time, each built switched off, then switched on. They touch every system: do them after the split.
6. Basic text-based stories for key crew members, written alongside 4 and 5 (mostly content/ files) and added when ready.

## Ways of working to keep quality up on a big codebase (APPROVED by the user, 2026-10-19: "integrate all this into the plan for the next team")
Set them up in step 2, alongside the split (the split's plan page shows the user how; the user still signs off that page before the file is cut). The rec deck (step 1) finishes the current way, so it isn't held up.
- **Ownership map** (`plans/owners.md`): which seat owns which file/area and which shared functions (with their exact signatures, e.g. recShow(state)). A change outside your area goes through its owner.
- **A fast pre-push check** (`check_fast.sh`): parses the game (node --check), scans for duplicate top-level names, greps for "Deck 7" on screen and runs 3-4 quick checks; under 5 minutes. Every worker runs it before every push. Today's name clash would have been caught hours earlier.
- **Automatic checks on GitHub** (GitHub Actions): the fast check runs by itself on every push, so nothing depends on a session remembering. (One-time setup in step 2.)
- **Integrate early, not at the end:** a shared integration branch that each seat merges into after each reviewed piece, with the fast check, instead of one big combine at the end (today's hand merges and the late clash came from combining two days of work at once).
- **Rules that caught us today, written into DEV_NOTES "Rules that keep it working":** the crew planner must never read records that are built while the game runs (the MACH_HIST bug); checks must not assume a deck is empty or a time slot is free (two check fixes today); new features stay gated (switch off = identical) until switched on.
- **A "where things live" map** (`plans/map.md`), kept current by whoever moves code, so a fresh session finds its way in minutes.
- **A small known-bugs list** (`plans/backlog.md`), so things found in passing aren't lost: the unclosed CSS comment (~line 181), the hidden door gear (~line 1724), the double clock hold in the evenings, two wall faults leaving you queued, rec talent night only skipping day 152, the Tracked panel filling small phones, "seven decks" Deck 4 texts not gated.
- **Keep the user's review rhythm (unchanged):** one step at a time, a plan page before building, the user's sign-off before the next step.

## Step 2 checklist for the lead (the split + the new ways of working)
1. Plan page for the user: the pieces and their owners, the build step, the byte-identical proof, the fast check, GitHub Actions, the integration branch. Wait for sign-off.
2. **Keep the whole file first** (the user, 2026-10-20): before cutting, tag the last one-file version in git (e.g. `whole-file-0.64.0`) and keep a copy of it, so the whole game can always be fetched in one piece.
2b. Cut the file; build step; prove byte-identical; publish nothing new (the game hasn't changed).
3. Write `plans/owners.md`, `plans/map.md`, `plans/backlog.md` (start it from the list above), `check_fast.sh`; add the GitHub Action; create the integration branch.
4. Add today's rules to DEV_NOTES "Rules that keep it working"; update CLAUDE.md "How we work" (fast check before every push, merge reviewed pieces into the integration branch, owners map) and the worker start messages (plans/start-prompts-lead20.md) to match.
5. Light clean-up, one area at a time, each with checks and a review.

## Check speed (talked through with the user, 2026-10-20)
Keep the full checks as they are (play from Day 1). With the split, add the quick check on GitHub; also run checks side by side across helpers, and let number-only checks skip drawing. Saved starting points (e.g. start of Day 5, stamped with the game version and rebuilt whenever the game changes, with a full from-Day-1 run before every release) only if check time is still the bottleneck after the split.

## The user's calls on the split plan (2026-10-20; the user asked lead 20 to take them as described)
Plan page: https://claude.ai/artifact/9v7C1oRCJUUTGkAujsAoUt (claude/split-plan cc833f8). Not yet signed off: the user asked for a deeper test first (rehearsal SX1, second reviewer SR2) and may still choose not to split.
- Keep the glued starship-cadet.html committed in git: yes.
- The GitHub check on every push: yes (free while the repo is public).
- Build number: the build master sets it when merging into the shared branch; helpers stop bumping it (CLAUDE.md change in turn 4).
- Owners: small edits in another seat's piece are fine, the owner reviews before merge; changes to a shared function's inputs or a shared table's shape go to the owner first.
- GitHub Releases tag: skip; the frozen branch + archive copy keep the whole file.
- Public or private: open, the user's call (the plan covers both).

## The user's playtest patch and next steps (2026-10-20, from the user's playtest of 0.64.2)
New order after Dev mode (the user): **Dev mode → playtest patch → "Talk a while" dialogue pack → the first ship event** (the ion storm's deeper fixes can come later). Where Pillar 5 steps 5-6 go: to confirm with the user.

**Playtest patch (after Dev mode):**
1. **Day 2, "Your first solo job":** the meeting never started when the user walked into the Chief's office; Calder wasn't there, a red-haired crew member was. Fix so Calder is in her office for it and the meeting starts reliably on arrival. No cutscenes, but the conversation may auto-play, and the player may auto-sit.
2. **Naming:** everything about it says "first solo job" (e.g. the Schedule/heads-up title "The Chief's office: your first job" → "…your first solo job"; Mail, Tracked, Settling-in, lines).
3. **Welcome tour / intro to the Chief:** Calder is there but doesn't walk up to you. She should.
4. **Zeke's line after the dinner with the Chief** ("the evening's ours" or similar) should be a speech bubble over Zeke, not the green text at the bottom of the screen.
5. **Maintenance access:** no more tiered (rank-based) access to maintenance areas like the ladder. And the ladder must work: tap it and a panel like the lift's comes up, with up/down and which deck is which.
6. **Clocking in/out:** it's too easy to clock in and out by accident; add a way to undo a clock-out (and clock-in) right after punching.

7. **Captain on Deck 4:** she hangs out there too often; occasionally is fine.
8. **Washroom light:** should actually show red when a toilet is in use.
9. **Toilets:** the user sees few or no crew using them; crew should visibly use them.
10. **Crew walking inside each other:** two crew with the same destination who leave the lift together stay overlapped for long stretches; they should keep apart.
11. **Arrow after the Chief's first briefing (Day 1):** if you track the briefing, the arrow doesn't then point to the job board.
12. **Stuck on Zeke on training day:** with hold-to-walk you get stuck on him (collision drops only after ~2 s of pushing); tap-to-walk gets past. Hold-to-walk must slide past him.
13. **The green tip about checking your device while working:** great timing, keep it, but make it more specific: it's about using the device while a long work action fills up (don't say "meters", don't say "in between jobs"); it popping during a long work action makes it clear.
14. **The device button the first time you get the device:** an arrow to it, or it lights up.
15. **Welcome tour:** Zeke points out the laundry room, but it's on the other side of the ship. Fix where he points (or what he says).
16. **Repair times, Tier 1:** have got a bit slow (tuning).
17. **Zeke and the player clip into the same spot** during the welcome tour and training day; they should stand apart.
18. **End of training day:** Zeke mentions breakfast instead of dinner and gets the time wrong (it's after 5). When the shift ends he should say good job and that you'll be on your own tomorrow.
19. **Your name on the Works beam:** should happen before dinner so players don't miss it; and the arrow must point to the right spot on the beam (upper left, where your name goes).
20. **Hunger** should go down more during a work day (tuning).
21. **Clicking someone:** show their rank and title along with their name.
22. **Social** should go down faster, the same as fitness (tuning).
23. **Large-group moments:** the user loves them; more of them, especially in ship-wide events (feeds the events plan).
24. **The shopkeeper:** tapping them opens a simple buy menu.
25. **Lift panel label:** should read "Officer's Quarters - Science" (which deck: to confirm with the user in the patch plan).
26. **One more tradition on Day 1,** so a new player sees how traditions flow.
27. **Waking up:** it shouldn't be so easy to wake up with Energy at 100 (tuning).
28. **Day 2 laundry tutorial** breaks if you don't wake up at 06:00; it must work whenever you get up.

**"Talk a while" dialogue pack (after the patch):**
- First rule: **no repeats** — once a conversation fires, it's done for that save.
- A **shared pool** any character can draw from (unless it really doesn't fit them), plus **a few of their own** per character.
- Shorter talks are fine, but **keep the question** (your three replies and their answer).

## The order from here (the user, 2026-10-20, replaces earlier orders)
1. Dev mode (planning now, with DJ1's measurements and two reviews).
2. The playtest patch (above).
3. The "Talk a while" dialogue pack. Talks run out in this order: the character's own talks first, then the shared pool; only when both are used up, light small talk with no question and an occasional "We've talked about everything, haven't we?".
4. The ship-wide events in chronological order, starting with the first: the ion storm (its update per the events plan), then the comet, then the diplomatic visit. Events plan: https://claude.ai/artifact/Qi1Uvev6p4TbPwYFQvRB1P (the user's answers pending).
5. Pillar 5 steps 5-6 (the later promotions). Note: built after the events, so Pillar 5 must fit around the events' fixed days (the events plan's calendar F0 and career-beat guard F1), not the other way round.
6. Character arcs (content/arcs/).
7. Optimization.
8. Balancing and polish (incl. the career-pace numbers parked earlier).

## Dev mode: the user's answers (2026-10-20 ~12:05) and the lean version
The user answered the Dev mode plan (artifact https://claude.ai/artifact/2ugbTkkAFkEsgTZa3bbFdH, db answers/devmode-plan) and, after talking it through, chose a **lean Dev mode**: Stop 1 (patch kit: clock with "excused" shifts, needs kept + top up, Take me to, Mark/Back, Undo, Copy my real game; then traditions) as planned; **Stop 2 = "Set career"** (pick a day; rank, trainings and reputation set from a table of what a steady player has by that day, marked approximate) instead of the steady-player replay; Stop 3 events. The full steady-player replay is **parked**, its design kept on record. Dev mode stays in published builds behind the Dev link (q10); every Dev action undoable (q11).
- Talk a while pack (2026-10-20): written by TW1 (claude/talk-pack, 160 talks, ~1,470 lines), reviewed line by line by TR1 (7 blockers, mostly arc spoilers, being fixed). The user: keep strict once-per-save for the pool; write more talks when the game grows past Day 30.
- Events plan v3.1 answered by the user (12:25 UTC): Day 6-ish event = Crossing the Line (the one extra short event); the user suggests Sunday (2nd day off) so the player keeps one free day; storm all-clear cast called in on their day off, with crew comments about it; crowds ~60 until a phone test; talent night moves a week and Lap of the Wren moves to another day that week; the commendation comes at the all-clear.
- Playtest patch plan answered by the user (12:52 UTC, artifact https://claude.ai/artifact/BrEniitA4gGKf1wFMvwy2s): lift label Deck 2 "Officer's Quarters - Science"; a different new Day 1 tradition (planner proposes 3); clock: confirm early clock-out + Undo for the rest; shop sells today's goods; ladder + Engine control + Sensor array open, Reactor sealed; climbing costs 2 energy, +1 fitness a deck; Tier 1 repair 30 min; hunger 7/h at work; social ~18 a day; full energy only after 8 h; Captain on Deck 4 Thursday + one evening; Calder walks over at dinner; Zeke's lines as goodnight bubbles; device button glow + pointer; beam at 17:05 with Zeke holding you from 16:50 and telling you to clock out (arrow to the time clock); lowest rank "Junior Officer"; big moments in the events.
- Dev mode v3.1 answered (12:58 UTC): starting friendships after Set career; always a new Dev game; wake 06:00 in bed (beat shortcuts go to the beat). Building starts: DB1 on claude/devmode, Stop 1a first.

## Weekly Captain's address and short Fridays (the user, 2026-10-20 ~17:55 UTC)
- No all-hands in the auditorium for the ion storm.
- A weekly Captain's address with the whole crew, first one in week one, on Fridays: everyone gets off work early on Friday (shift ends 15:30), the address at 16:00, dinner at 17:00. Needs dialogue explaining the short Friday workday. Place not named (lead recommended the plaza). PP1 is planning it (patch item #31 or its own page), with questions for the user.
