# Playtest patch 1 (the user's playtest notes, 2026-10-22 ~03:20 UTC)

Build: **0.64.15**, from `claude/integration` 32b699a6 (0.64.14 game, sha256 94f32868...881e9). Three builders on three branches, one reviewer, then BM13 merges, the six runners do a full round, PUB1 publishes, the user is notified.

The rules as always: small exact-string edits, new code in your slot, no build number (BM13 sets it), a build-table row, your area's checks + `check_fast.sh`, never push on FAILED. **The look doesn't change** except where a note asks for it (open ladder rooms). cadet_test differences must each be explained by a note below. Design decisions go into design-doc.md in the same commit.

## The notes, by builder

### A. Arrival and the Chief: ON1 (new onboarding builder), branch `claude/patch-play1-a` (sections 21, 21b, 19, 24/24p, and 22 through content/ only)
1. **Arrive at 16:30**, so people don't walk away when you reach dinner.
2. **Zeke takes you to your room to drop your things**, says so, and you put them in your wardrobe.
3. **Zeke hands you your device** in person.
4. **Zeke's device message goes** (it repeats what he now says in person). Judgement call by the lead; the user asked "Get rid of Zeke's message?": flag it in the summary.
5. **The Chief, sitting at a nearby table, comes over physically** to talk to you.
6. **Zeke and the Chief don't stand up and walk away straight after speaking**: they stay a little, then go naturally.
7. **The Chief's first job is still broken**: the cut scene starts, then nothing happens. The Chief says what they say now, then explains the new job type is on the board, which unlocks the new mechanic. Find the root cause and fix it; add a check that would have caught it (intro_check or career_check).
8. **Hygiene and clothes**: hygiene goes down while wearing dirty clothes, and ticks up when you change into clean ones (21b with section 15's needs; the player engineer's numbers through PB2/owners if shared).

### B. Pointer, jobs and the lift: FR4, branch `claude/patch-play1-b` (sections 15b, 11, 15r/8c, 4d only for ladders)
9. **Clock-in pointer**: when the green tip about clocking in shows, the arrow points to the time clock; once you clock in, it points to the job board; once you take a job, to the task (as now).
10. **Tea time**: when you track the tea quest, an arrow points to the table.
11. **After tea, tracking goes back to your job.**
12. **The lift panel's marker says "Tracked", not "Goal".**
13. **Not enough jobs on the board**: the user cleared it on Day 1. More jobs, sensibly paced (keep machine_check's player jobs and ship health sane).
14. **Ladders**: tapping the ladder itself works (today only the door of the ladder room does).
15. **Every ladder room can be entered** (a map change: deck_check, path_check and tiles_check must stay OK; it's the one place the look may change).
16. **The rowing machine**: the bar moves, but not in time with the pull. Sync the animation.

### C. Crew moving and the day: PB2, branch `claude/patch-play1-c` (sections 7, 10, 14, 15b toilet use, 16)
17. **Crew clip through walls when walking alongside them** (not straight at them). This is NEW: it didn't happen before. Bisect between builds (0.64.11 / 0.64.12 camera / 0.64.13 storm / 0.64.14 opt-render) to find the commit that caused it, fix the cause, and add a check (path_check or day_check) that would have caught it. **Top priority of the patch.**
18. **Breakfast starts at 07:00.** Move whatever depends on it (shifts, the rota, food_check's expectations) with it.
19. **Toilets: the crew wait in a queue**. Today you can't use a toilet an NPC has "targeted", even from across the ship. You can always use it unless its red light is on (someone inside); the crew queue for it.

## Review and release
- Reviewer: **OR2** reviews each branch (names the exact tip).
- BM13 merges A, B, C into integration as 0.64.15, check_fast + cadet_test (each difference explained by a note).
- The full round on all six runners, then PUB1 publishes both pages, and the user gets a notification with a plain summary.
- Order of merging: C first (clipping), then A, then B.

## Lead's judgement calls (tell the user)
- Note 4 (Zeke's message) read as "yes, remove it", since Zeke now hands over the device in person.
- Seats: the user's limit is 14 active. Tonight the patch takes PB2, FR4, ON1 (new) and OR2, so the controller team starts three package builders now and the last two when the Line merge seats (LB3, PR10) go idle.
