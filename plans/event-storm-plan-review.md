# The ion storm: adversarial review of the event plan

Reviewer ER2 (session_01S8pboNujAzZgMSWFK84CxD), 2026-10-21. Branch `claude/event-plan-review-2`.
Plan reviewed: `claude/event-plan-storm` 57e980b, `plans/event-storm-plan.md` (EP3, v1). Reports to lead 22.

## Round 1 (57e980b): PASS WITH FIXES

**How I checked:** a new game on claude/events-base 18f0d9d, with a copy where `EVENTS_ON = true`, in headless
Chromium. I read `schedPeople`, `aboard`, `isWorkDay`, `planDay`, `eventsOn`, `eventDueDay`, `SHIP_EVENTS.ionStorm`,
`eventBand`, the machines and places, `content/facts.md`, and the Brennan and Lukas cards and arcs.

### True as written
- **Aboard:** 76 on Day 11 and 75 from Day 12. Of the 74 crew, the number working is 57 on Day 11, 61 on Day 12,
  45 on Day 13, 45 on Day 14 and 57 on Day 15.
- **Who's off:** Vance and Zeke on Day 11; Brennan and Zeke on Day 12; the Captain, Calder, Sato, Holt, Brennan,
  Rina and Raman on Day 13; the same less Brennan on Day 14; Tomas on Day 15.
- **Day 12:** the Captain is on a double shift from 14:00 to 20:30, and Vance from 11:22 to 20:30. So S2's
  exception for the 16:00 address is needed for both, as the plan says.
- **Lukas** (facts.md and his rota: `cover: { for: 'brennan', days: [4, 5] }`):
  - Friday: cooking 16:50-20:30, tea 20:30-20:45, in his bunk 20:47.
  - Saturday: on from 14:30 to 20:45.
  - He has berth 5 in Bunk 1.
- **Brennan on Saturday:** Deck 4 all afternoon (her cabin 4-05, the music room, bench 3), and dinner in the mess
  18:05-18:32.
- **The calendar:** `eventDueDay` gives Day 11 with the base on. Day 13's traditions are all paused today. Day 14
  has talent night at 19:30 and the Lap at 20:30 next to the party. Day 15 has running and then book circle (20:15),
  so moving the Lap there keeps the two-at-once voice budget.
- **The result:** `eventBand` rounds the average of the threads. So bumpy, bumpy, bumpy, rough comes out bumpy;
  three smooth and one bumpy comes out smooth; two and two comes out bumpy. q2's "it takes all three" is honest.
- **The range** is a real machine (`3-range-1`, with its panel `3-range-1-panel`, in the galley).

### Is story A worth telling? Yes. It's the right recommendation.
- It comes from the ship's own facts: Lukas covers Brennan on Friday and Saturday, so the storm's two worst days
  are his, and so is the lantern supper.
- It gives a dry, guarded junior something he wants (her galley not slipping on his watch). He talks in numbers,
  and "I've got onions" is an in-joke from the facts (Tariq leads him at onions).
- Your choice sits in your trade (the range), in errands (Brennan) or in trust (two rings).
- It pays off at the storm's big crowd moment, and it works if you miss it.
- Brennan's three supper lines are in character. "Make it again on Friday" is a lovely touch: Friday is his day.
- B and C are fairly called weaker. C's clash with the supper is real, and so is Sato's naming at the comet.

### Fixes
1. **The lantern job doesn't exist yet.** Story A's first reply "holds the supper's lantern job for you", "What you
   can do" says "carry the lanterns", and q8 counts the lantern job toward your commendation. But no turn builds it,
   and it's not in the storm's jobs. Add it to S5: an escalation job (an id, its time, tier 1, stops from the stores
   to the mess's long tables) next to `DECK_DRESS.lanternMess`. Or drop it from the story and from q8.
   **Without it, q8's recommendation promises a job that doesn't exist.**
2. **Brennan's "And tell him I said he's ready" touches her arc.** Her beats 4-5 are about leaving the Wren (Nell
   Arrowby's offer, and her choice to stay). "He's ready" reads as "ready to take over from me", which is the
   question her arc keeps for later. Add a guard rail alongside "no leaving": nothing that hints at handing the
   galley on. Reword it, for example: "And tell him it's his galley tonight." EW1 and the head writer check.
3. **Don't assume you've moved or been promoted.** The promotion "can only be delayed, never failed" (design-doc),
   so a slower player is still a junior in Bunk 1 on Day 12. Lukas's lines and the plan text ("your bunkmate until
   Wednesday", "I'm Works" as an officer) must read the save: "since you moved" only if you have.
   - **A related question for EV1 and the lead, not the user:** a delayed promotion can push the summons, the move
     or the commissioning onto Days 12-13, into the storm. F1's guard holds only the default days. Say what happens
     then. My suggestion: `guardFree` holds those beats until after the all-clear, with the storm's hours, the
     address and the supper never displaced.
4. **The range job's stop.** `3-range-1` is the machine's id, not a place. Write the stop the way the ballasts job
   does, `{ deck: 3, machine: '3-range-1' }`, which resolves to the panel `3-range-1-panel`.
5. **One `EV_DAY_DRESS`, shared with the Line plan.** This plan builds it first (S6), and the Line plan's L2 also
   says it builds it. Agree one shape now: rows keyed by tradition id and day, made at load from `EV_CALENDAR` and
   the event's data. The Line's L2 then says "reuses". I've told EP2.

### Small points (nits, no turn needed)
- The supper's draw calls were measured with 20 people in the mess (239). S5's perf_check scene must measure about
  60 plus the lanterns at 390x844, as risk 9 says. The party reached 367 with 64 in the lounge, so this one looks
  safe.
- The minute table says "Story A begins at dinner". The moment needs you near the galley while he's cooking, and
  the servery queue at 17:00-18:00 is the natural place. Say "at the servery" so the 20c moment has a room.

**Verdict: PASS WITH FIXES** (fixes 1-5). Story A and questions q1-q7 are safe to take overnight. q8 is safe once
fix 1 adds the lantern job, or once q8 stops counting it.

## Round 2 (91ab377): PASS
- **1, the lantern job:** `stormLanterns` is built in S5, from Deck 5's Main storage to the mess's seats. It's held
  for you if you promised Lukas, and q8 names it.
- **2, Brennan's line:** "it's his galley tonight", plus a new guard rail against anything that hints at handing the
  galley on.
- **3, rank-neutral lines:** Lukas's lines read the save. The delayed-promotion question is put to EV1 and the lead,
  with a sound proposal: `guardFree` holds the storm's onset-to-all-clear hours for career beats.
- **4, the range stop: EP3 is right, and my fix was wrong.** `eventStopOf` matches a machine's `kind`, or the second
  part of its id ("range"), never the whole id. So `{ deck: 3, machine: 'range' }` is correct and lands on
  `3-range-1-panel`.
- **5, `EV_DAY_DRESS`:** one shape, with rows of drop, add (same `k`) or changes, made at load from each event's
  `dayDress` data. Both plans' rows are written out, and they match EP2's d01acd6.
- **Nits:** both done. The supper's perf_check is at about 60 plus the lanterns, and A begins "at the servery".

**Verdict on claude/event-plan-storm 91ab377: PASS.** All recommendations, q1-q8 and story A, are safe to take
overnight.

### 06ce585: final
- `EV_DAY_DRESS` now uses the agreed shape: a Map keyed `trad@day`, with drop, set or add rows. An add keeps its k,
  the Map is empty when off, and skipped events add no rows. A walk's stop is a 20c moment, which matches the Line
  plan's L4.
- The delayed-promotion question is settled by lead 22 as proposed.

**PASS stands at 06ce585.**
