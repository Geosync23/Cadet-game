# Handover: Pillar 5 designer (seat D, no game code)

- **Role:** design only. Reports ONLY to the lead (TEAM.md names it; on 2026-10-18 lead 11, session_01YKC3CGA9VS4b7wuqLbPT7V) with send_message: one line when starting, one per finished page with its commit hash, at once if blocked. Never contacts the user. Never starts sessions. Stay inside `plans/` and `design-doc.md`.
- **Branch:** `claude/p5-design` (made from `claude/pillar5-plan` 93a5a7f). Predecessor: session_01FDy4na3u2FS8L8vEjR6gAR (archived), then session_01VXENaUt4vdyYtr3KjVZk9z (this note's writer, 2026-10-18).
- **Messaging rule (lead 11, ~09:00):** answer builders' questions directly (no cc to the lead); message the lead ONLY for a design call beyond the approved pages or a real blocker. Record every answer in the page's "Builders' questions" section.
- **Seats (2026-10-18):** C Works career session_01LgTgzjeqLNrjeCa2iRzbYx; H cases session_013nqpqRFX4hh3cLPhhpZirJ; S systems session_01KxfsfBWkCGcncuuH2n1hFB; R reviewer session_01MSLjUdmeVJetxFhh9PqzLt; seat A's branch is claude/deck-0607.
- **Authority overnight (2026-10-18):** the lead approves or rejects each page against the approved plan; nothing waits for the user (`plans/overnight-decisions.md` on `claude/lead-pillar1`, last section).

## Done (2026-10-18)
| Commit | What |
| --- | --- |
| 8a50917 | Plan v9 (`pillar5-plan.md` + `.html`): P3 on Day 5 with the scanner, M2 uniform Day 8, puzzle rates 1/10 (Days 5-9), 1/5 (10-15), 1/4 (16-22; 1/3 own tier), 1/3 (23+), a T1 band; the case engine in Step 1 (seat H joins Step 1), P3 in Step 2; 24g scanner moved from M3 to H so Step 2 stays at 6 seats (D, B, M1, M2, H, A); M5's stale question fixed. `design-doc.md` taken from `claude/lead-pillar1` (newest) plus two bullets (Day-2 dates; puzzles from Day 5) |
| 46f10be | `plans/mechanics/foundation.html` (17 playerTier, jobs by rank, real faults, causes, job kinds with steps, reserved training/test jobs; 15 work steps, careerSpeed; 24 core: ladder, training, tools, reputation bands, Works app, save; hooks; tests; build and key ranges; the name clash) |
| 29904c1 | `case-engine.html` |
| 374dc66, 9b94208, 7c860ad, 3c6e396, c481db1, 62a9ae4, 0a99c09 | `m1-rounds`, `m2-uniform`, `m3-drill-inspection`, `m4-hauling`, `m5-tuning`, `m6-incidents`, `m7-scanner` + `p3-whats-been-tried` |
| 9cca2dc | `fault-tables.html` (Tier 1 complete, Tier 2 draft), `plans/mechanics/index.html`, plan notes on the corrections |

## How the pages are made
`plans/mechanics/src/`: each page's source is a `.body` file (four header lines TITLE/H1/SUB/NAV, then the sections), `mk.py BODY OUT base.css` wraps it in the plan page's style; `chk.js` (`NODE_PATH=$(npm root -g) node chk.js FILE...`) checks no sideways scroll at 390 px. Edit the body, rebuild, commit the html (and the body).

## Facts found that the plan didn't have (all on the pages)
- **Name clash:** `SHIP.career`, `ship.career`, `CAREER`, `career…` functions are the 0.61.x leave/missed-shift/time-clock system (section 20). Pillar 5 uses `SHIP.works` / `ship.works`; `CAREER_LADDER`, `careerSpeed` keep their names. Seat C is a different seat from the 0.61.x career engineer.
- **Builds:** systems next 0.33.43+ (0.33.42 is 0.60.7's Wednesday delivery), player 0.28.71+; 0.44, 0.45, 0.47, 0.49-0.59 (but 0.48 is the content writer's), 0.63+ free on every branch (checked 2026-10-18).
- **Hash keys:** 850-899 free (split on the foundation page: 850-854 core, 855-859 section 17, 860-879 mechanics, 880-894 cases, 895-899 spare). 900-949 is NOT free (901 sick, 920+k and 930 galley); 951-952 (time clock) are inside Pillar 6's 950-999. Suggested second range 1000-1049.
- **Deck 4 has no light-relay machine with a panel** (4-lights-1 is a dropped stand-in); real machines list is in the game's `DECKS[n].machines`. P3's first case is `4-washer-2` leaking.
- **Tiers in code:** junction Tier 3, doorgear Tier 2, valve Tier 2 (so a burst pipe's fix is a Tier 1 joint job).
- 0.60.7 builds clothes in 15c (`player.clothes`, the onboarding engineer's), the Wednesday delivery as crates (0.33.42), right-shelf parts (0.33.41), `HOLD_MAX` 3 and `shareOut` (0.33.40). Details: `plans/plan-0607.md` on `claude/plan-0607`.

## Since the first pages (all approved; FAQs record the builders' answers)
- Day 5's teacher is Emeka Halloran (Torres off Thu+Fri), by-lists first-on-shift; the work-step field is `how`; real faults are made by finding worn machines already at the top of faulty (S, key 856); lift machine 5-mainlift-1; galley alarm on 3-galleyplant-1; worksTabAdd; a case kind is open when its ladder row opened; P3 borrows the scanner lesson's escort at Washer 2.

## Next (in order)
1. Whatever the lead sends back on the pages (fix and re-push; one line each).
2. Step 3 pages when the lead asks: the Tier 2 test job and the first promotion, M8 team jobs, M9 tracing (with the pipe graph), P1, P2, the T2 band; finish the Tier 2 fault tables (signs, still lines, traced causes).
3. Tier 2 bands for rounds (Officer routes), the drill's muster job, M5 stage 2.

## Gotchas
- Line numbers on the pages are from `claude/cand-0607`'s game file; builders match by text.
- Every cause in a fault table needs a part already in `STOCK` (listed on `fault-tables.html`), and causes sharing a card need different signs.
- The solver's rule "no single clue solves it" catches plan examples (P3's did); check each later kind's example against it.
- Day 2 has only one new thing (rounds): 0.60.7's laundry and health check fill it.
