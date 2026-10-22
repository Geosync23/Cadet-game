# Playtest patch 1 (the user's playtest notes, 2026-10-22 ~03:20 UTC)

Build: **0.64.15**, from `claude/integration` 32b699a6 (0.64.14 game, sha256 94f32868...881e9). Nine builders on nine branches, three reviewers (the user, 03:30: hire as many as needed; the lead's recommended size, one builder per area so nobody edits the same lines), then BM13 merges, the six runners do a full round, PUB1 publishes, the user is notified.

The rules as always: small exact-string edits, new code in your slot, no build number (BM13 sets it), a build-table row, your area's checks + `check_fast.sh`, never push on FAILED. **The look doesn't change** except where a note asks for it (open ladder rooms). cadet_test differences must each be explained by a note below. Design decisions go into design-doc.md in the same commit.

## The notes, by builder

### A. Arrival and the Chief (notes 1-6): ON1 (new onboarding builder), branch `claude/patch-play1-a` (sections 21, 21b, 19, 24/24p, and 22 through content/ only)
1. **Arrive at 16:30**, so people don't walk away when you reach dinner.
2. **Zeke takes you to your room to drop your things**, says so, and you put them in your wardrobe.
3. **Zeke hands you your device** in person.
4. **Zeke's device message goes** (it repeats what he now says in person). Judgement call by the lead; the user asked "Get rid of Zeke's message?": flag it in the summary.
5. **The Chief, sitting at a nearby table, comes over physically** to talk to you.
6. **Zeke and the Chief don't stand up and walk away straight after speaking**: they stay a little, then go naturally.
### D. The Chief's first solo job (note 7; note 8 hygiene moved back to ON1, who had coded it): CJ1 (new), branch `claude/patch-play1-d` (sections 24/24p, 21b, 15)
7. **The Chief's first SOLO job is still broken** (the user's correction): the cut scene starts, then nothing happens. The Chief says what they say now, then explains the new job type is on the board, which unlocks the new mechanic. Find the root cause and fix it; add a check that would have caught it (intro_check or career_check).
8. **Hygiene and clothes**: hygiene goes down while wearing dirty clothes, and ticks up when you change into clean ones (21b with section 15's needs; the player engineer's numbers through PB2/owners if shared).

### B. Pointer and the lift (notes 9-12): FR4, branch `claude/patch-play1-b` (sections 15b, 11, 15r/8c, 4d only for ladders)
9. **Clock-in pointer**: when the green tip about clocking in shows, the arrow points to the time clock; once you clock in, it points to the job board; once you take a job, to the task (as now).
10. **Tea time**: when you track the tea quest, an arrow points to the table.
11. **After tea, tracking goes back to your job.**
12. **The lift panel's marker says "Tracked", not "Goal".**
### G. More jobs (note 13): JB1 (new), branch `claude/patch-play1-g` (sections 15b, 17, 24)
13. **Not enough jobs on the board**: the user cleared it on Day 1. More jobs, sensibly paced (keep machine_check's player jobs and ship health sane).
### E. Ladder taps and the rower (notes 14, 16): LD1 (new), branch `claude/patch-play1-e` (sections 11, 4d, 15r/8c)
14. **Ladders**: tapping the ladder itself works (today only the door of the ladder room does).
16. **The rowing machine**: the bar moves, but not in time with the pull. Sync the animation.
### H. Open ladder rooms (note 15): LR1 (new), branch `claude/patch-play1-h` (sections 4d, 4b, 7)
15. **Every ladder room can be entered** (a map change: deck_check, path_check and tiles_check must stay OK; it's the one place the look may change).

### C. Wall clipping (note 17): PB2, branch `claude/patch-play1-c` (sections 7, 10, 14, 15b toilet use, 16)
17. **Crew clip through walls when walking alongside them** (not straight at them). This is NEW: it didn't happen before. Bisect between builds (0.64.11 / 0.64.12 camera / 0.64.13 storm / 0.64.14 opt-render) to find the commit that caused it, fix the cause, and add a check (path_check or day_check) that would have caught it. **Top priority of the patch.**
### F. Breakfast at 07:00 (note 18): SC1 (new), branch `claude/patch-play1-f` (sections 14, 16, 15b)
18. **Breakfast starts at 07:00.** Move whatever depends on it (shifts, the rota, food_check's expectations) with it.
### I. Toilet queue (note 19): TQ1 (new), branch `claude/patch-play1-i` (sections 15b, 10, 14)
19. **Toilets: the crew wait in a queue**. Today you can't use a toilet an NPC has "targeted", even from across the ship. You can always use it unless its red light is on (someone inside); the crew queue for it.

## Review and release
- Reviewers: **OR2** reviews A, C, D; **RV3** reviews B, E, F; **RV4** (new) reviews G, H, I. Each names the exact tip.
- BM13 merges all nine into integration as 0.64.15, check_fast + cadet_test (each difference explained by a note).
- The full round on all six runners, then PUB1 publishes both pages, and the user gets a notification with a plain summary.
- Order of merging: C first (clipping), then F, I, A, D, B, G, E, H (H, the map change, last).

## Lead's judgement calls (tell the user)
- Note 4 (Zeke's message) read as "yes, remove it", since Zeke now hands over the device in person.
- Seats: the user lifted the limit for the patch (03:30), so the controller team keeps its five package builders.
