# Ship-wide events plan: summary (version 3)

Events planner EP1, 2026-10-20. Branch `claude/events-plan`, build 0.64.2.

- **The full page:** `plans/events-plan.html`.
- **Screenshots:** `plans/events-plan-shots/`.
- **Decisions:** in `design-doc.md`, "Ship-wide events".
- **Earlier versions and the reviews:** in git (`claude/events-plan-review`).
- **What v3 does:** it folds in the user's answers to v2 (saved 05:47 UTC).
- **Planning only:** the game is unchanged.

## The user's answers to v2
1. **Other:** "one more short one". The user also asked for a one-day ship-wide event around Day 6, first in the game, with the ion storm still built first. **I assumed the Day 6 event *is* the one more short one** (new question 1 checks this).
2. **(b):** the storm moves one day later, to Days 11-15, with a shorter afterglow.
3. **The comet** is on Tuesday Day 16.
4. **The diplomatic visit** is the weekend finale, Days 26-30.
5. **Events come by the calendar**, not by rank.
6. **Prep jobs and help move the storm's threads.** Left alone it comes out bumpy; with good help, smooth.
7. **The rec deck's first all-hands** is unhooked from the storm, and the rec deck closes from the front to the all-clear.
8. **All the Captain's scenes stay separate**, not folded together. They're spaced out with the career-beat guard.
9. **A small rotation arrival on Day 21** (built with Pillar 5).

## The calendar (F0)

| Day | What happens |
| --- | --- |
| Fri 5 | Day 6 event warning |
| **Sat 6** | **Day 6 event:** plaza 17:00-17:45, supper 18:15-19:30 |
| Thu 11 | Storm warning. Calder's briefing at 13:30, after the 09:30 team job. Nothing 17:00-18:30 (the ceremony is at 17:15). |
| Fri 12 | The front, 14:00. The rec deck closes. |
| Sat 13 | **New:** the lantern supper in the mess |
| Sun 14 | The all-clear at 10:00, with the Captain and Calder called in, and the commendation letter. The party in the evening; talent night moves a week. |
| Mon 15 | Debrief at 18:00 (Pillar 5's Tier 3 test day: no summons) |
| Tue 16 | Comet viewing, 21:30 |
| Thu 18 | The commendation summons |
| Sat 20 | The Captain's table |
| Mon 22 | Vance's memo about the visit |
| Fri 26 | The visit's warning |
| Sat 27 | **Greeting:** the crew line the shuttle bay |
| Sun 28 | One dinner |
| Mon 29 | **Farewell** |
| Tue 30 | Afterglow |

Pillar 5's beats on Days 15-26 are held free in F1 now, so the events steer around them before they're built.

## The Day 6 candidates
- **A. Crossing the Line** (recommended). The Wren crosses into the Veyli reach, and everyone crossing for the first time is welcomed.
  - the horn and gold hull lights;
  - a plaza ceremony for the first-timers (you included), about 50 people;
  - the Line supper in the mess, about 60;
  - a certificate and a plaque.

  About 3-4 turns.
- **B. Power surge** (from the parked list). Two decks go dark, with a dark supper in the Commons. It steals some of the storm's thunder.
- **C. Letters from home.** A relay buoy, busy booths and a letters evening. The letters evening was scratched once before.

## Order and size
The order runs after Dev mode, the playtest patch and the Talk-a-while pack.

| Order | Piece | Turns |
| --- | --- | --- |
| 1 | Shared base F0-F8 | 13-16 |
| 2 | Ion storm (with the lantern supper) | 9-11 |
| 3 | Day 6 event | 3-4 |
| 4 | Comet | 2-3 |
| 5 | Visit | 9-11 |
| | **Total** | **about 36-45**, plus the head writer's lines |

## New questions for the user (ids `ev-v3-q1` to `ev-v3-q7`, plus `ev-v3-general`)
1. **Is the Day 6 event the one more short one, or is a second one wanted?** Recommended: one.
2. **Which Day 6 event?** Recommended: A, Crossing the Line.
3. **Saturday Day 6 or Friday Day 5?** Recommended: Saturday.
4. **On the storm's Sunday all-clear, do the Captain and Calder come in?** Recommended: yes.
5. **How big should crowds be for now?** Recommended: about 60, then a test on the user's phone.
6. **Should talent night move off the party night?** Recommended: yes.
7. **Is the bridge invite tied to the storm, or to the first event?** Recommended: the storm. A Day 6 event would otherwise bring bridge hour forward to Day 8.

## Parked (kept on record, never deleted)
The crew rotation day, then the garden creature, power surge, illness, the Founders' Day festival, nebula, the late supply shuttle, salvage, the Veyli vessel and déjà vu. They're marked parked in design-doc's events table, and the full breakdowns are in `plans/pillar3-plan.md`.

## Pending for v3.1 (to fold in with ER1's review)
- **F6 gets smaller** (lead 20, 2026-10-20). Dev mode plan v2's Stop 3 already builds starting an event, the threads view and "End and undo". F6 keeps only two things:
  - jumping to a phase;
  - "End and keep", once the ending is split out of `eventAdvance`.
- **The estimate changes to match** (about 1 turn less).
