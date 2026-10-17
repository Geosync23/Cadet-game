# Pillar 5 plan: new ways to work (expanded core mechanics)

**DRAFT 2 (2026-10-17, the Pillar 5 planner, branch `claude/pillar5-plan`).** Rewritten from the user's survey answers (`plans/pillar5-notes.md`, "The user's answers"): **Pillar 5 is expanded core mechanics only.** Ship-wide events move to Pillar 6; career progression, story and the night shift to Pillar 7 *(changed 2026-10-17: career progression is now in Pillar 5, Part 7; Pillar 7 keeps Tiers 3-4, the story and the night shift)* (design-doc.md, "Roadmap after Pillar 4"). The user asked for a detailed plan before any work, and for new mechanic ideas from the planner. **Nothing is built until the user approves this plan, and each mechanic gets its own short spec page the user reviews before it's built.** **Update 2026-10-17: the user answered every open question** (see the end); this draft takes them all in: laundry duty every two weeks, all seven "more ideas" on the ladder (M11-M17), and **Pillar 5 built on its own after Pillar 4**, by one lean team (Parts 4 and 5 rewritten).

Read with `design-doc.md` ("The clockwork", "The player", "Works progression", "Roadmap after Pillar 4"), `plans/pillar4-plan.md` (Part 6: the rules for sharing the one game file), `TEAM.md`, `DEV_NOTES.md` ("Machines and wear", "Chores and openJobs", "Player needs and the device", "Player interactions", "Hook register") and the handover notes for systems, player, galley and device.

A plain-language version for the user is `plans/pillar5-plan.html`.

**Added 2026-10-17 (the Pillar 5 designer): Part 7, career progression** (the user: fold it into Pillar 5 "since it all coincides"): how ranking up works (Works reputation from jobs → harder jobs → certification → promotion), the first promotion as a full sequence (an urgent summons to the Chief, the scene, the crew, an escorted move, an officer ceremony with the Captain), and the second promotion (Senior Officer, a Deck 2 cabin) designed now and switched on with Tier 3. Pillar 7 shrinks to Tiers 3-4 and the story.

**Added 2026-10-17 (the Pillar 5 designer): Part 6, deductive repair puzzles ("head-scratchers").** The user: keep the whole plan, and add deduction puzzles to some repairs, **starting about 30-50% of the way into the progression** (the early job has none). They begin about a third of the way in (Day 13 of the Day 1 to about Day 42 arc) and grow from there. Part 6 adds a track beside the ladder, inside the same arc; nothing in Parts 1-5 is removed or shrunk.

---

## The pitch (one page)

Today the Works job is one verb: **fetch a part and replace it** (or hold to work at a spot for a chore). Pillar 4's first week teaches that loop. Pillar 5 gives the job **a ladder of new mechanics**, each a different way of working with your hands, **unlocked slowly, one at a time, each taught to you by a person**, so you start simple and the job keeps opening up as you work on more of the ship.

**The ladder** (about one new mechanic every two or three ship days after your first week; numbers are starting points; M11-M17 are the seven "more ideas" the user added, numbered in the order they were listed, so the table is in day order):

| # | Mechanic | The new verb | Taught by | Opens around |
| --- | --- | --- | --- | --- |
| 0 | Fetch and replace (Pillar 4's first week) | take, fetch, fit, turn in | Zeke Torres | Day 1 |
| 1 | **Rounds** | walk a route, look, mark what you see | Torres | Day 8 |
| 2 | **Laundry and uniforms** | change, drop off, load, move, fold, deliver | a laundry hand | Day 9 |
| 3 | **The drill and the inspection** | muster with a drill job; get your berth and uniform ready | Calder; the duty officer | Days 10-11 |
| 4 | **Hauling and stores** | load a cart from a manifest, deliver, count shelves | a storekeeper | Day 12 |
| 5 | **Tuning** | adjust a machine by watching it respond | Brennan (the ovens) with Calder | Day 15 |
| 6 | **Making it safe** (small incidents) | isolate first, then clean up, then fix | Calder, at the first one | Day 16 |
| 7 | **The scanner and diagnosing** | read a machine and work out which part is failing | Torres | Day 18 |
| — | **Certification and your first promotion** (now a full sequence: Part 7) | a supervised job using what you've learned; the summons, the scene, the move, the officer ceremony | Calder; the Captain | about Day 20-22 |
| 8 | **Team jobs** | one pair of hands on a big job with others | a Works officer | Day 22 (after promotion) |
| 11 | **Tool upkeep** | recharge, clean and re-seal your tools at your bench | Torres | Day 23 |
| 9 | **Tracing connected faults** (Tier 2) | follow a symptom back along pipes and ducts | Calder | Day 24 |
| 12 | **The logbook** | write your shift's line in the Works log | Calder | Day 25 |
| 13 | **Leak hunting** | follow the wet (and later the sound) to the drip | Torres | Day 27 |
| 10 | **The workshop** | crew order small things; you make them | the machine shop tech | Day 28 |
| 14 | **Garden irrigation** | clear the racks' nozzles while the crew harvest | a gardener | Day 29 |
| 15 | **Rewiring** | follow a junction's colour chart, wire by wire | Calder | Day 31 |
| 16 | **Coolant rounds** (Deck 6) | read the coil gauges, top up the coolant | Torres and the engine crew | Day 33 |
| 17 | **On the lift roof** | ride the lift car's roof down the spine, greasing the guides | a Works officer | Day 35 |

**Added (Part 6):** beside the ladder, a **puzzle track**: some real faults become **head-scratchers** you solve by deduction from clues gathered around the ship (nine types designed, eight built in Pillar 5 (the clash waits for Tier 3); the first about a third of the way in, at Day 13, after hauling; then growing to the end of Pillar 5 at about Day 42, with fault-finder grades, two new tools and crew asking you for help).

**Added (Part 7): career progression.** Ranking up is one clear rule: good work grows your Works reputation, which brings harder jobs, then certification, then promotion. The first promotion (about Day 20) is a full sequence: an urgent summons to Calder's office, the badge, the crew's reaction, Calder walking you to cabin 4-23 with your things moved, and an officer ceremony with the Captain. The second (Senior Officer, a Deck 2 cabin) is designed now and switched on with Tier 3.

Around the ladder: **more real faults reach you**; **repairs get quicker with practice** (in words); **tools arrive one at a time, each with training**; **off-shift tinkering, cabin touches and star logging**; **the device's work pages** (your training record, work log, tools). Still Works only.

**How it's built:** each mechanic is **one self-contained sub-block of a new section 24 with one owner**, on top of a small shared foundation (the unlock ladder, training moments, work-step building blocks). A **designer** writes each mechanic's and puzzle type's one-page spec for the user ahead of the builders. **Pillar 5 is built on its own, after Pillar 4 is finished** (the user, 2026-10-17), by **one lean team: at most about 6 helpers at once** (a designer, a build master, a career engineer and up to three rotating builders), in six steps with **a check-in with the user after each** (Parts 4 and 5).

---

## Where we start

- **The build:** combined 0.60.0 (Pillar 4 wave 1a). Pillar 4 runs about 15 helpers in waves 1b-4.
- **What the job has today** (section 17; DEV_NOTES "Machines and wear", "Chores and openJobs"):
  - ~36 machine kinds, condition and five states, wear against an average day, visible faults (`machineLook`, `deckLook`), the ship health board.
  - Jobs: service, repair, overhaul, restock, and **chores** (`CHORES`: lamp, vent, calibrate, delivery, round, fault; crew filter and seal). Chores are already on the board, but **every one plays the same way**: walk to the stops and hold to work. That's the gap Pillar 5 fills: the same kinds of work get their own verbs.
  - Your loop (section 15): take at the board, fetch (two-slot carry), make a part (60 min), inspect (3 min; just tells you), repair, turn in; the food cart run (`SHIP.player.cart`). `jobReserve` holds jobs for Pillar 4's first week.
  - `PLAYER_TIER = 1` is a constant in section 17, read in 15b, 17 and 19.
  - **The crew are too good:** most of your jobs are routine.
- **Laundry today:** the washers are machines (stand-ins) that wear with the crew's uniforms (washed 06:00-10:00, about six to a load) and their weekly laundry visit (section 14's `schedWants`); faltering washers send uniforms back grubby (hygiene drains faster); you can fold at the laundry (`ixFold`, hygiene +12). **You have no uniform of your own**: no grubbiness, no change, no locker swap.
- **The drill and the inspection today:** in the crew's week (section 14: Wednesday 15:00, off-duty crew muster by the lift for 15 minutes; Thursday, juniors tidy their bunks). You take no part.
- **Pacing:** a ship day is 40 real minutes. Week 1 is Pillar 4's; the ladder's first nine steps fit in weeks 2-3 (about 9 real hours), so the first promotion lands at about 2 ship weeks of steady work after your first week (the user's "2 weeks"). The last ten mechanics (M8-M10 and the seven the user added, M11-M17) come after promotion, one every two or three days over weeks 4-6.

---

## Part 1: how mechanics unlock, are taught, and grow

### The rules every mechanic follows

1. **Start simple, add one at a time.** A new mechanic opens only when the one before has been used a few times (about 3), and never two on the same day. If you're slow, the ladder waits; nothing is missed.
2. **Taught by a person, on a real job.** Each opening is a **training moment**: a crew member finds you (or Mail asks you to meet them), shows you once on a real job (they lead, you watch; then you do one while they watch, like Pillar 4's shadow shift), and hands you anything new (a tool, a key, a clipboard). Then the mechanic is yours. Short lines, no pop-ups (one control tip at most, in the tips style).
3. **Physical, not a mini-game.** Every verb happens in the world with your character's hands: walking, looking, carrying, holding, turning. Where a choice is needed (which part, which valve), it's a choice you make with what you've seen on the deck. No timing games, no puzzles that stand in for the work. *(Tuning, M5, is the closest to a panel; it's an open question for the user.)* *(Added: head-scratchers, Part 6, are the "Diagnose" step done for real, with clues gathered in the world and a physical fix; see 6.2.)*
4. **It evolves.** Each mechanic has 2-3 stages that open as you use it (rounds: a set route on a clipboard → you plan your own route → the scanner reads from across the room).
5. **No fail state.** Doing it badly costs time, a remark, or a slower ship; never a fail screen.
6. **Words, not numbers.** The Record says "Trained: rounds, laundry, hauling" and "Ovens: you know these well"; no points or bars (the user's rule).
7. **It feeds the job list the ship already has.** Mechanics are new ways to do jobs on the same board (new job kinds or chores with their own steps), so the crew can do them too and the ship keeps running without you.

### The foundation (built first, shared by every mechanic)

- **The ladder** (`CAREER_LADDER` in section 24): each mechanic's id, what it needs first (the one before, used N times; a day; your tier), who teaches it, its training script, and its stages.
- **Training moments:** a training job held for you (`jobReserve`, extended with a `train` slot), a teacher who leads then follows (Pillar 4's escort lead-and-follow walker mode), meeting lines (`MEETING_SCRIPTS`), and `simNote('trained', { mech })`.
- **Work steps** (section 15, the player engineer): a small set of building blocks every mechanic uses, so no mechanic edits section 15 itself: `hold` (hold to work, exists), `look` (stand and look; marks what you see), `carry` (exists: two slots, plus a cart), `choose` (pick one of a few things, in the device's screen style), `turn` (a valve or a dial, with a pose), `wait` (start something, come back later: a washer, a cure). A mechanic is data: its steps, places and outcomes.
- **Tools** (`SHIP.career.tools`): each comes with its mechanic's training and lives on the device's Tools page and in your locker (not a carry slot).
- **Skill in words** (`careerSpeed(kind)`): repairs and steps on a kind get quicker with practice (100% → about 80% after 5 → 65% after 15), shown only in words.
- **More real faults** (section 17): about half of your 3-6 daily jobs become real faults, by having the crew leave your tier's faults longer and find worn machines later on your shift days; unchanged on days off and at night.
- **`playerTier()`** replaces the constant `PLAYER_TIER`, once, early and inert.
- **The device's work pages** (registered from section 24 with `deviceApp`, as section 20 does; no change to section 19): Training (what you're trained in, what's next in words: "Calder says the storekeepers want a hand next week"), Work log (the last 30 jobs, found by you or not, who noticed), Tools.

---

## Part 2: the mechanics

Each card: **the verb · how it's taught · how it unlocks · how it grows · what it touches (and whose section) · phone budget · test.** Each will get its own one-page spec (`plans/mechanics/<id>.html`, by the mechanic designer) for the user to approve before it's built.

### M1. Rounds (Day 8, Torres)

- **The verb:** walk a route of 4-6 machines and **look** at each (stand by it a moment; your character glances over it). Mark what you see: fine, worn, or "something's off". A worn machine you mark becomes a service job "found by you" (cheap and quick now, instead of a repair later). That's prevention made physical.
- **Taught:** Torres walks the first round with you and hands you the **round clipboard** (a Works item; the device shows the route).
- **Grows:** stage 1, a set route each morning on the clipboard; stage 2 (after 5 rounds), you pick which machines to look at, and the job list rewards a well-chosen round; stage 3 comes with the scanner (M7), which reads condition from across the room.
- **Touches:** 17 (the existing `round` chore gets real stops and "found by you"); 24a (the round, the marks); 15 (`look`).
- **Phone:** nothing new drawn (a small clipboard prop in the hand, shared kit).
- **Test:** `mech_check` (new): a round posts service jobs for worn machines and nothing for healthy ones; found-by-you counts; the same twice.

### M2. Laundry and uniforms (Day 9, a laundry hand; the user's ask)

- **The verb:** you now have a **uniform** that gets grubby as you work (oily jobs faster, a shower doesn't clean it). Change at your locker (a clean one from your stack), **drop the worn one in the laundry**, and **about every two weeks take a laundry duty** (the user's choice: less often): load a washer, start it, come back when it's done (it runs about 40 ship minutes: the `wait` step), move the load to the dryer, fold, and deliver the clean linen to the bunk rooms by cart.
- **Why it matters:** a grubby uniform drains hygiene faster and gets remarks (exists); **the Thursday inspection checks it** (M3); clean linen in the bunks helps everyone's sleep a little; the washers wear with use, so you also see their faults coming. Crew do laundry duty too (a junior rota), so if you skip it someone else does.
- **Taught:** a laundry hand (a Works junior on the rota) shows you a full duty once.
- **Grows:** stage 1, your own uniform; stage 2, laundry duty on the rota (about every two weeks; crew cover if you skip it); stage 3, you can service the washers between loads (the washers become real machines with panels).
- **Touches:** 24b (your uniform's state, the duty, the steps); 15 (`wait`, the locker change); 14 (the sim engineer: the junior laundry rota; reading only where possible); 17 (the washers become real machines; their wear from loads); 8b (performance: `fold` exists; a basket carry pose; your uniform drawn a shade duller when grubby, a material tint, no new meshes); DECKS[4] (deck architect 2: the laundry's places for load, dryer, fold; a linen cart dock).
- **Phone:** laundry baskets as one instanced mesh (at most 2 draw calls), only on Deck 4.
- **Test:** `mech_check`: grubbiness rises with work, a change resets it, a duty runs end to end with the wait, crew take the duty when you don't; `player_check`: hygiene drain, the remark; `day_check`: laundry days still flow.

### M3. The drill and the inspection (Days 10-11, Calder and the duty officer)

- **The drill (Wednesday 15:00):** a toast at 14:50; go to your **muster station** (the Works bay) and do your **drill job**: on a fire drill, take the extinguisher from the wall and stand by the hatch; on a pressure drill, close and dog the bulkhead door by the Works bay (a `turn`); on a power drill, stand by the breaker cabinet. The kind of drill rotates each week. Calder times the Works team, and a quick drill gets a word in the Friday tea (Pillar 4's tradition).
- **The inspection (Thursday 06:30):** get ready the night before or that morning: **a clean uniform** (M2), **your berth made** (tap your bunk: a short `hold`), **your locker tidy** (nothing loose: the things you bought or made put away). The duty officer walks the junior wing; each item gets a nod or a gentle remark ("Uniform's seen better days, cadet").
- **Why it matters:** both count toward reliability (trust, below) and the crew's opinion; missing them costs a remark, nothing more.
- **Taught:** Calder briefs you at your first drill; Tomas (your bunkmate) shows you how to get ready for the first inspection.
- **Touches:** 24c; 14 (the sim engineer: the muster station for you, the duty officer's walk, the drill kind); 15 (`turn`, `hold`); DECKS[5] (the extinguisher and bulkhead places).
- **Phone:** none new (the extinguisher and door exist or are one small prop).
- **Test:** `day_check` on a Wednesday and a Thursday (everyone still reaches their places); `mech_check`: the drill job, the three inspection items, the remarks.

### M4. Hauling and stores (Day 12, a storekeeper)

- **The verb:** **cart runs with a manifest:** collect a hover cart from the Cart bay, load the crates the manifest lists from the hold (tap each; the cart fills), ride the lift, drop at each stop (linen to the laundry, medical supplies to the infirmary, store stock, spares to the bridge). **Stocktake:** walk the storage aisles and count the shelves; a count that doesn't match finds a shortfall early (a restock job before a repair gets blocked).
- **Builds on:** the food cart run you already have, and the `delivery` chore (which today is one stop).
- **Taught:** a storekeeper (Yara Esposito) does your first manifest run with you.
- **Grows:** stage 1, single-stop deliveries; stage 2, multi-stop manifests (you choose the order: routes matter); stage 3, the Wednesday delivery: helping unload the supply shuttle's crates into the hold.
- **Touches:** 24d; 17 (manifests from `DELIVERIES`, the stock counts, the Wednesday delivery); 15 (`carry` with a cart, exists); DECKS[5] (storage count spots, the hold's crate stacks).
- **Phone:** the cart exists; crates are one instanced mesh (2 draw calls).
- **Test:** `mech_check`: a manifest run delivers every stop once; a stocktake finds a planted shortfall; carts never go over the cap; `machine_check`'s stock never below 0.

### M5. Tuning (Day 15, Brennan with Calder)

- **The verb:** some faults aren't a broken part but **a machine out of adjustment**: an oven running hot, a scrubber fan humming off-pitch, a light relay chattering, a cart dock charging slow. You **turn** a setting a step at a time and **watch the machine respond in the world**: the oven's glow steadies, the hum smooths, the lights stop flickering (the machine looks section 17 already draws). Settle it in the right range and it's done. Overshoot and it shows the other way; turn it back.
- **Why it's not a mini-game:** there's no timer or score; the feedback is the machine itself on the deck. *(Open question 1: is this the right side of the "no mini-games" line?)*
- **Taught:** Brennan complains her oven runs hot; Calder shows you how to tune it while Brennan watches (and feeds you a biscuit).
- **Grows:** stage 1, one setting (ovens, lights); stage 2, two settings that pull on each other (a scrubber's fan and flow); stage 3, with the scanner, you see the setting's drift before anyone notices.
- **Touches:** 24e; 17 (a `tune` fault kind: a machine's setting drifts; `calibrate` chores become tuning); 15 (`turn`, `look`); 8b (a `tune` pose: one hand at a panel).
- **Phone:** none new (it reuses the machine looks: glow, flicker, blink).
- **Test:** `mech_check`: a drifted machine settles only in range; the look follows the setting; the drift is the same twice.

### M6. Making it safe: small incidents (Day 16, Calder at the first one; the user's yes to Q17)

- **The verb:** about once a week, **a small incident**: an hour or two on one deck, from the machines. You do it in three steps: **make it safe** (isolate it: close the right valve or breaker, upstream, chosen from what you see), **clean up** (mop the water, clear the smoke, help someone out), then **fix** the cause (a normal repair).
- **The incidents:** **a burst pipe** (a corridor wet, crew rerouting; close the line's valve, mop, replace the joint); **the lift sticks** (someone inside for 20 minutes; release the brake at the lift machine room, then service it; they're grateful for days); **the galley alarm** (a scorched pan sets off the extractor; reset it, clear the air, check the hood; Brennan embarrassed). More can be added later as data.
- **Never on** an event day (Pillar 6) or a tradition evening (the voice budget); never at night (no on-call; the night shift handles them: Pillar 7).
- **Taught:** Calder takes you to your first one and walks you through the three steps.
- **Grows:** stage 1, Calder there; stage 2, you're first on the scene; stage 3, the crew wait for you to say it's safe.
- **Touches:** 24f (the incident table and its three steps); 17 (the machine side: the pipe, the lift brake, the extractor); 14 (the sim engineer: a corridor closed, someone stuck in the lift); 15 (`turn`, `hold` with a `mop` pose); 8b (performance: a `mop` pose; a water puddle as one flat decal); DECKS (deck architect 2: valve places by the corridors).
- **Phone:** a puddle decal and a smoke wisp (instanced), at most 3 draw calls, only during the incident.
- **Test:** `mech_check`: each incident's three steps in order; crew reroute and return; never on an event day, a tradition evening or at night; the same twice; `day_check` on an incident day.

### M7. The scanner and diagnosing (Day 18, Torres; the user: "comes later")

- **The verb:** the **diagnostic scanner** reads a machine's parts. Inspecting a faulty machine with it shows **its 3-5 parts with a reading each** (in the device's screen style): usually one is clearly off; sometimes two, and what you saw on the deck (the drip, the flicker) tells them apart. You **choose** the part to fetch. A wrong pick costs a walk back ("Fitted a new seal. Still low flow: it's the pump"), never a fail. Before the scanner, inspecting simply tells you the part (as now), so the early game stays simple.
- **Taught:** Torres hands you the scanner and does the first reading with you.
- **Grows:** stage 1, read the panel up close; stage 2, read condition from across a room on your rounds (M1 stage 3, M5 stage 3); stage 3 (after promotion), it reads flow along a pipe (M9).
- **Touches:** 24g; 17 (parts per machine kind with readings and symptoms; the failing part hashed from the machine and the hour; right or wrong fits); 15 (`choose`); the device's skin draws the panel through the app layer.
- **Phone:** none (a device view).
- **Test:** `mech_check`: every kind has parts; the failing part is the same twice; the right pick finishes; a wrong pick costs a fetch; before the scanner, no choice.

### Certification and your first promotion (about Day 20, Calder)

- **Experience** (no numbers shown): jobs finished, weighted by how bad (service 1, repair 2, failing 3, overhaul 4), found by you (+1), the right part first time (+½), and the mechanics you've been trained in (the ladder must reach M7 first).
- **Reliability (trust):** reads Pillar 4's **Work reputation** (social A's ship-wide Work axis), plus turning up to the drill and the inspection. One score for the ship, not two.
- **Calder's progress talks** (built in Pillar 3) say how close you are, in words.
- **The certification job:** a real Tier 2 job held for you (a Deck 4 air scrubber or the water recycler), using what you've learned (a round finds it, the scanner reads it, you fetch and fit, maybe a tuning step), with Calder following and saying a word at each step (Torres on her days off). Go wrong and she tells you what to practise and sets another in a week: **only delayed, never passed over** (the user).
- **The moment:** *(Changed: Part 7, "Added: career progression".)* An urgent summons to Calder's office during the next work day, the scene with the badge, the crew reacting, Calder walking you to your cabin with your things moved, and the officer ceremony with the Captain the next afternoon (7.3).
- **Your own cabin:** Spare 4-23 on the officers' corridor: your bed and locker move, the door opens for you, Tomas says goodbye as a bunkmate, and Pillar 4's "Come over" visits start. *(Career progression is now in Pillar 5: Part 7.)*
- **Touches:** 24 core; 17 (the held job; `playerTier()`); 14/13 (the sim engineer: `playerBed()` and the cabin door, after Pillar 4's wave 3); 20 (reads only).
- **Test:** `career_check` (new): end to end on paper, a live certification (pass, delay, pass), the bed and doors, an old save loads as Tier 1.

### M8. Team jobs (after promotion, a Works officer)

- **The verb:** a big job (the main fan's bearing, a washer overhaul, the recycler's membrane change) takes **three or four Works crew at once**. You're one pair of hands: be at your spot when it starts, **hold** your part (brace the housing, pass the tools, turn the crank) when your turn comes, and the job moves on. Crew talk while they work (overheard lines from Pillar 4).
- **Grows:** stage 1, a pair of hands; stage 2, you're asked to bring the parts for the whole team (M4's manifest); leading a team job is Pillar 7.
- **Touches:** 24h; 17 (a `team` job kind: several claims, one schedule); 14 (crew meeting at the job); 8b (`brace` and `crank` poses).
- **Phone:** 3-4 crew at one machine; no new meshes.
- **Test:** `mech_check`: the team assembles, waits for you (up to a limit), finishes without you if you don't come; `day_check` on a team-job day.

### M9. Tracing connected faults (Tier 2, after promotion, Calder; the user: "comes later in career")

- **The verb:** water and air machines are joined by pipes and ducts. A fault can **show in one place and start somewhere else**: weak showers on Deck 4, a valve in the manifold room on Deck 5. The job card names the symptom; with the **pipe kit** (a new tool, with training) and the scanner's stage 3, you read the flow at junctions and follow the low reading back to the cause.
- **Opens:** the Deck 5 machine rooms (air plant, fan hall, manifold room), the pipe galleries and the spine's crawlways (Deck 4's ladder hatch is already tier 2), each with real machines and panel places.
- **Touches:** 24i; 17 (the pipe and duct graph, `MACHINE_LINKS`; traced faults; real machines for the stand-ins); DECKS[4], [5] (deck architect 2: the rooms' machines and panel places, the manifold's flow board).
- **Phone:** the new rooms within 450 (`deck_check`); the flow board one canvas.
- **Test:** `machine_check`: a traced fault's symptom and cause on different machines; fixing the cause clears the symptom; every Tier 2 machine has a panel place; `deck_check`.

### M10. The workshop (after promotion, the machine shop tech)

- **The verb:** crew **order small things** at the machine shop (a hook for Pell's guitar, a shelf for Rina, a frame for Tomas's star chart): an order board in the shop. Take an order, **make** it on the lathe or the fabricator (the `wait` step plus a short `hold` to finish it), and **deliver it** in person: a small friendship moment.
- **Grows:** stage 1, simple orders; stage 2, orders that need a part from stores (M4); stage 3, your own designs (the tinkering below).
- **Touches:** 24j; 17 (the shop's lathe and fabricator as machines that wear); 20 (reads: a gift-like delivery via Pillar 4's gifts, through the lead); 15 (`wait`, `hold`).
- **Phone:** made things are small props from the existing kit, only where they're placed (at most 1 draw call each, a cap per deck).
- **Test:** `mech_check`: an order taken, made, delivered; the relationship note.

### Off shift (with the ladder; the user's yes to Q10)

- **Tinkering:** make small things in the machine shop on your own time (a lamp, a mug rack, a toy), for gifts (Pillar 4's machine-shop gifts) or your cabin.
- **Cabin touches** (after promotion): 3-4 spots in 4-23 take something bought or made (a rug, a plant, a lamp, a shelf of keepsakes). At most 4 extra draw calls.
- **Logging stars** at the observatory telescope for Survey: a short activity; the Survey crew warm to you; a line in your Record after ten.

### The seven from "more ideas", now on the ladder (the user, 2026-10-17: "all seven")

The user picked all seven. They come **after promotion**, in weeks 4-6, because the days before promotion already have an opening each (Part 1's rule: never two on one day), and several need things you only have by then (your tools, Tier 2 junctions, Deck 6 with the engine crew, the spine). Easy ones come first; the riskiest to build (the lift roof) comes last. With M8-M10 that's ten mechanics in 22 days after promotion: one every two or three days, the pace the user agreed. Each gets its own spec page like the rest.

#### M11. Tool upkeep (about Day 23, Torres)

- **The verb:** your tools wear with use: the scanner's charge runs down, the pipe kit's seals and the logger's clip get grubby. At your bench in the Works bay (Friday afternoons are the custom), **recharge** the scanner (the `wait` step), **clean and re-seal** the pipe kit (`hold`), check the logger. A tool that's due still works, just slower ("Your scanner's charge is low"); it never stops working.
- **Taught:** Torres shows you his own Friday bench routine.
- **Grows:** stage 1, the scanner; stage 2, the pipe kit and the logger as they arrive; stage 3, you look after the Works team's shared tools too (Calder notices).
- **Touches:** 24m; 24 core (a wear state per tool in `SHIP.career.tools`); 15 (`wait`, `hold`); DECKS[5] (deck architect 2: your bench place in the Works bay).
- **Phone:** none new.
- **Test:** `mech_check`: tools wear with use, upkeep restores them, a tool that's due slows a step and never blocks a job.

#### M12. The logbook (about Day 25, Calder)

- **The verb:** at the end of a shift, at the Works bay terminal, **write a line in the Works log**: choose one of three summaries made from your real shift (what you fixed, what you found, what's still open). Calder reads them and mentions them at your progress talks; a good note helps the next shift finish your open job sooner.
- **Taught:** Calder, on your first day as a Technician: "Officers write it down."
- **Grows:** stage 1, a line a shift; stage 2, flag a machine for the night crew to watch; stage 3, **your own notes come back as clues** in later head-scratchers (P3 What's been tried?).
- **Touches:** 24n; 17 (the job history it reads); 22 (the summaries as templates, through the Works writer).
- **Phone:** none (a terminal place and a device view).
- **Test:** `mech_check`: the three summaries match the shift; the note reaches the next shift and the progress talk; the same twice.

#### M13. Leak hunting (about Day 27, Torres)

- **The verb:** "A pipe drips somewhere" (the valve kind's line already says so). **Find it:** look for the puddle and the damp patch on the wall, follow the drip along the pipes, and, once sound is in the game, **listen**: the drip gets louder as you get close. Then tighten or replace the joint.
- **Taught:** Torres finds the first one with you ("Follow the wet, not the noise. Well, both").
- **Grows:** stage 1, a room on one deck; stage 2, behind a panel in the pipe galleries (Tier 2 rooms); stage 3, the pipe kit's damp reading narrows it down.
- **Touches:** 24o; 17 (drips as a `valve` fault's look, which exists); 8b (reuses M6's puddle decal); 15 (`look`); sound later, when it comes.
- **Phone:** the puddle decal is shared with M6 (1 draw call, only while a leak is open).
- **Test:** `mech_check`: a leak's place is reachable; it's found and fixed; the puddle goes; the same twice.

#### M14. Garden irrigation (about Day 29, a gardener on the rota)

- **The verb:** at harvest, while the garden crew pick, **walk the grow racks and clear the nozzles** (a short `hold` at each). Clear nozzles water the beds evenly, so the next harvest is a little bigger (the garden really grows food).
- **Taught:** a gardener on the rota shows you the first rack.
- **Grows:** stage 1, clear nozzles; stage 2, flush a rack's line (`wait`); stage 3, service the irrigation machine itself (its real `irrigation` kind).
- **Touches:** 24p; 17 (the `irrigation` kind and its effect on the harvest); 14 (reads the garden rota; you join the harvest); DECKS (deck architect 2: nozzle places along the racks).
- **Phone:** none new.
- **Test:** `mech_check`: cleared nozzles lift the next harvest a little; crew harvest still flows (`day_check` on a harvest day).

#### M15. Rewiring (about Day 31, Calder; Tier 2)

- **The verb:** replace a junction box's wiring by **following the colour chart on its panel**: a careful `choose` sequence (this wire, that terminal), then close it up and test. A wrong pair shows at the test (a fuse pops; open it and redo it), never a fail.
- **Taught:** Calder, on an officers' corridor junction.
- **Grows:** stage 1, a clear chart; stage 2, a faded chart you check against the room's lights; stage 3 leads straight into **P7 Faded labels** (Day 36).
- **Touches:** 24q; 17 (the `junction` and `lights` kinds); 15 (`choose`).
- **Phone:** none (a device view of the chart).
- **Test:** `mech_check`: a right sequence finishes; a wrong pair costs a redo; the same twice.

#### M16. Coolant rounds (about Day 33, Torres, with the engine crew)

- **The verb:** a weekly round on Deck 6 with the engine crew: **read the gauges** on the drive coils and the coolant loop, mark any that are off, and **top up** where it's low (carry a coolant can from stores, then `hold`). You read and top up; repairing the engines stays Tier 4.
- **Taught:** Zeke Torres, who is a Works engine officer: his home ground.
- **Grows:** stage 1, with the engine crew; stage 2, on your own; stage 3, your readings become clues for later engine cases (Tier 4, a later pillar).
- **Touches:** 24r; 17 (the `coil` kind's readings and a coolant level); DECKS[6] (deck architect 2: gauge places by the coils).
- **Phone:** none new (Deck 6 is already within its budget).
- **Test:** `mech_check`: the round's gauges match the machines; top-ups only where low; `deck_check` Deck 6.

#### M17. On the lift roof (about Day 35, a Works officer)

- **The verb:** in a quiet hour (mid-morning) the main lift is held for maintenance; crew use the other lift or the ladders for the hour. You climb onto the car's roof at the top, ride it slowly down the spine, and at each guide **stop and grease it** (`hold`): a view of the spine nobody else gets.
- **Taught:** a Works officer who looks after the lift rides down with you the first time.
- **Grows:** stage 1, with the officer; stage 2, alone; stage 3, a lift head-scratcher (a judder only at Deck 3) that you trace from the roof.
- **Touches:** 24s; 11 (the lift: a slow maintenance ride with you on the roof, through its owner); 14 (the sim engineer: crew avoid the held lift for the hour); 8b (a `grease` pose); the camera in the shaft (performance).
- **Phone:** the spine and shaft are already drawn; `deck_check`/`perf_check` measure the ride. The riskiest of the seven, so it comes last.
- **Test:** `mech_check`: the hold and release; crew still reach their places (`day_check` on a lift day); the ride ends at every deck it should.

---

## Part 3: who owns which part of the game file

*Pillar 5 is now built on its own after Pillar 4 is finished (the user, 2026-10-17), so nothing here races Pillar 4. The table stays as the map of which seat owns what; the "Pillar 4" column shows who held each part before, and the timing notes ("waits for Pillar 4's wave 3") are simply already met.*

### Which parts of the game Pillar 5 touches, and when

| Part of the file | Pillar 4 | Pillar 5 | How they stay apart |
| --- | --- | --- | --- |
| **24 WORK (new)**: 24 core + one sub-block per mechanic (24a rounds … 24j workshop, 24k-24l head-scratchers, 24m-24s the seven added mechanics) | — | the career engineer (core) and the mechanic engineers (one sub-block each) | new, lazy at load; one owner per sub-block; hooks out are one line, typeof-guarded, in the register |
| 17 machines & jobs | held by the sim engineer since the systems engineer retired; on call only (`jobReserve`, notes) | **a fresh systems engineer**: real faults, job kinds with steps, parts, tuning drift, incidents' machine side, team jobs, the pipe graph | Pillar 4 needs only `jobReserve` and `simNote('job')`, unchanged; `intro_check` on every push |
| 15 player | on call (kit bag, device lock, gift tags) | **the player engineer**: the work-step building blocks (`look`, `choose`, `turn`, `wait`), your uniform, the locker change | one owner; Pillar 4's rows first |
| 19 device | busy waves 2-3 | none: pages registered from section 24 with `deviceApp`; the device engineer only if the skin needs a new piece | no edits before Pillar 4's wave 3 |
| 13/14/10 sim | busy all of Pillar 4 | on call: the junior laundry rota, your muster station and the duty officer's walk, closed corridors and the stuck lift, crew at team jobs, `playerBed()` | small rows; the bed move waits for Pillar 4's wave 3 |
| 8b crowd and poses | on call | on call: `mop`, `tune`, `brace`, `crank`, basket carry; your uniform's tint; puddle and smoke | rows |
| DECKS[n] | deck architect: Deck 3 mostly, Bunk 1, the Works tea corner | **deck architect 2**: the laundry's places (Deck 4), storage counts and the hold (Deck 5), valves and the extinguisher, the Deck 5 machine rooms and spine (M9), 4-23 | different rooms; a `// P5 places` block per deck |
| 20 social, 22 lines | busy | reads: Work reputation, `relAdd`, `lineFor`; training and incident lines written as `content/` files if the dialogue engineer agrees | reads only; lines through the head writer |
| 18 events / traditions | busy | reads only: the voice budget and event days (so incidents avoid them) | none |

### Rules (Pillar 4's, reused)

- **One mechanic, one sub-block, one owner.** Removing a sub-block removes the mechanic and nothing else breaks; its unlock simply never comes.
- **`playerTier()`** replaces `PLAYER_TIER` once, early and inert, with `cadet_test` identical.
- **Hash keys** (checked free by the build master): 850-899 for all of Pillar 5 (24 core 850-859, then ten keys per two mechanics as the career engineer hands them out). Incidents are in section 24, not section 18, so no `k + 100` jitter range is needed. *(Pillar 6's events will take 950-999 as the build master suggested.)*
- **The save:** `save.career` (tier, the ladder, tools, skill by kind, uniform, the work log ring, certification) and one small part per mechanic inside it; read defensively; `SAVE_V` stays 2.
- **Merge order:** systems (17) → player (15) → career (24 core) → mechanics (24a… in ladder order) → head-scratchers (24k, 24l) → deck architect 2 → the writer's lines. One build master combines them (Part 5).
- **Notes on the bus:** `simNote('trained', { mech })`, `simNote('found', { machine })`, `simNote('incident', { id, step })`, `simNote('promoted')`, `simNote('uniform', { state })`, so Pillar 4's lines and reputation can react without new hooks.

---

## Part 4: the team, the order and the check-ins (Pillar 5 on its own)

**Changed 2026-10-17 (the user, question 7):** "This has changed: we will develop Pillar 5 on its own. Please restructure the labor plan accordingly." **Pillar 5 is built after Pillar 4 is finished, not alongside it.** So there's no racing Pillar 4 for the one game file, no second build master next to Pillar 4's, no cross-pillar coordinators and no "quiet start". One small team with one build master, **sized lean (at most about 6 helpers at once**; the user is watching usage), and **a check-in with the user after every step**. *(The earlier plan's Full-level crew, two build masters and coordinators were for building beside Pillar 4; they're no longer needed and are left out.)*

### The seats (at most 6 at once)

**Standing seats** (the whole pillar):

| # | Seat | New? | Branch | Builds | Owns |
| --- | --- | --- | --- | --- | --- |
| D | **Designer** (mechanics and puzzles; no code) | this role continues | `claude/p5-design` | — | a spec page per mechanic and per puzzle type (`plans/mechanics/<id>.html`), the case engine page, the fault tables in plain words, the Chief's notes; plays generated cases for fairness; keeps this plan current; answers builders' design questions |
| B | **Build master** | new (or Pillar 4's, carried over when Pillar 4 is done) | `claude/integration-test` | candidates on the lead's release line | combines the builders' branches in merge order, runs every check (1-2 short-lived check runners only for the slow ones), reviews each branch against `plans/review-checklist.md` plus a Pillar 5 section (mechanics physical, words not numbers, the ladder's rules, determinism twice, phone budget, one owner per sub-block), hands the lead each candidate; the lead releases |
| C | **Career engineer** | new | `claude/works-career` | 0.44.x | section 24 core (ladder, training, tools and their wear, skill, trust, the drill and inspection hooks, certification, promotion, device pages); `career_check.py`; the frames of `mech_check.py` and `puzzle_check.py` |

**Rotating builders** (up to 3 at once; each joins for its step and is archived, with a handover note, when its part is signed off):

| # | Seat | Branch | Builds | Owns |
| --- | --- | --- | --- | --- |
| S | Systems engineer (a fresh session) | `claude/ship-systems` | 0.33.38+ | section 17: `playerTier()`, more real faults, job kinds with steps, each mechanic's machine side, the fault tables; `machine_check.py` |
| P | Player engineer | `claude/player-needs` | 0.28.23+ | section 15: the work steps (`look`, `choose`, `turn`, `wait`), `careerSpeed`, your uniform, the Ask button, off-shift activities; `player_check.py` |
| M1 | Mechanic engineer 1 | `claude/mech-rounds` | 0.45.x | 24a rounds, 24b laundry, 24c drill and inspection, 24d hauling, 24m tool upkeep, 24n the logbook |
| M2 | Mechanic engineer 2 | `claude/mech-incidents` | 0.51.x | 24e tuning, 24f incidents, 24h team jobs, 24o leak hunting, 24p irrigation, 24r coolant rounds |
| M3 | Mechanic engineer 3 | `claude/mech-diagnose` | 0.53.x | 24g scanner, 24i tracing, 24j workshop (and tinkering), 24q rewiring, 24s the lift roof |
| H | Head-scratcher engineer | `claude/mech-cases` | 0.55.x | 24k the case engine, the solver, Fault notes, the Chief's notes, hints, P1-P4; 24l P5-P8, the logger, the test rig, grades, favour cases, the cold-case board; `puzzle_check.py` |
| A | Deck architect 2 | `claude/decks-p5` | 0.47.x | `// P5 places` blocks in `DECKS[n]`: laundry, storage and hold, valves and extinguisher, your bench, the garden racks, Deck 6 gauges, cabin 4-23, the Deck 5 machine rooms and spine, the shop's order board and test rig |
| W | Works writer | `claude/writer-p5` | — | `content/` lines: training moments, incidents, inspection remarks, the promotion, workshop orders, witness and handover-note templates, logbook summaries |

*(Build ranges: the earlier ones were confirmed free by the build master on 2026-10-17; 0.55.x is a suggestion to confirm.)* **On call** (their pillars are finished; reopened from their handover notes only when a step needs them): sim (the laundry rota, musters, the duty officer, the stuck lift, the held lift's hour, `playerBed()`), performance (poses, decals, the lift-roof camera, `perf_check`), device (three small screen pieces for Fault notes), interactions, galley (oven tuning), social (Work reputation, reactions).

### The common brief (every seat's starts with this)

"You are the <seat> for Starship Cadet's Pillar 5 (new ways to work). Pillar 5 is built on its own, after Pillar 4. Read CLAUDE.md, then DEV_NOTES.md, plans/pillar5-plan.md (Part 1, Part 3, your seat in Part 4, your mechanics in Part 2 or Part 6), plans/pillar5-notes.md (the user's answers), the approved spec page for each thing you build (plans/mechanics/<id>.html), TEAM.md, and your predecessor's handover note if your role had one. Push only to <branch>. Touch only what your seat owns; anything else goes through its owner via the lead. Each turn: small exact-string edits (never rewrite the game file), bump the build in the HUD, add a DEV_NOTES row, run the tests (one browser check at a time; always `intro_check` when you touch jobs, the player or the clock), commit, push, and report to the lead with send_message; the build master takes your branch from there. Hooks into other sections are one-line, typeof-guarded, and listed in DEV_NOTES' hook register. Hand over at about 70% memory with plans/handover-<role>.md. Commit messages end with the Co-Authored-By line; never put model names anywhere else."

### The steps (one at a time; a check-in after each)

| Step | What's built | Seats active (at most 6) | Check-in with the user |
| --- | --- | --- | --- |
| 0 | Approval: **done** (the user answered every question, 2026-10-17). Pillar 5 waits for Pillar 4 to finish. | — | — |
| 1 · Foundation | `playerTier()`, more real faults, job kinds with steps (17); the work steps (15); section 24 core: the ladder, training moments, tools, skill in words, trust, **reputation bands deciding the jobs left for you and the Record's "What's next" (Part 7)**, device pages, inert then switched on. The designer's pages for the foundation, M1-M4 and the case engine. | D, B, C, S, P | **1:** a work day with more real faults and quicker repairs; approve the pages |
| 2 · Your second week | M1 rounds, M2 laundry and uniforms, M3 the drill and inspection, M4 hauling; their places | D, B, C, M1, A (S, P on call) | **2:** play your second week |
| 3 · Puzzles start; the rest of Tier 1 | the case engine, P3, P1, P2, P4 (H); M5 tuning, M6 incidents (M2); M7 the scanner (M3); lines (W, briefly) | D, B, H, M2, M3 (+W) | **3:** the first head-scratchers, tuning, a burst pipe, the scanner |
| 4 · Promotion | certification with its puzzle step; **the full promotion sequence (Part 7): the summons, the scene and the crew, the badge, the escorted move to cabin 4-23, the officer ceremony** (sim and performance on call) | D, B, C, A, W | **4:** from a save near certification, through the summons and the move, to the ceremony |
| 5 · After promotion, part 1 | M8 team jobs, M9 tracing with P5 and the logger, M10 the workshop with P8 and the test rig, M11 tool upkeep, M12 the logbook, M13 leak hunting | D, B, M1, M3, H (+A) | **5:** weeks 4-5 |
| 6 · After promotion, part 2 | M14 irrigation, M15 rewiring, P6, P7, M16 coolant rounds, M17 the lift roof, the fault-finder grades, favour cases, the cold-case board, cabin touches, star logging; **the second promotion's machinery, inert** (Part 7.4) | D, B, M2, M3, H (+W) | **6:** Pillar 5 final; then a pull request to `main` with the user's OK |

**Merge order inside a step:** systems (17) → player (15) → career (24 core) → mechanics (24a… in ladder order) → head-scratchers (24k, 24l) → deck architect 2 → the writer's lines (generated blocks re-baked with `content_gen.py`, never merged by hand).

**Leaner still** (if usage must drop): at most 4 at once (D, B and two builders); the build master also runs the career checks; the steps take longer but nothing is cut. **Scaling up** is the reverse: reopen archived seats from their handover notes.

### Test changes

- **New `career_check.py`** (C): the ladder (never two openings on a day; waits for use), training moments, tools and their wear, skill words, trust, certification (pass, delay, pass), promotion, the cabin, the save, an old save, determinism twice.
- **New `mech_check.py`** (C's frame, one part per mechanic, M1-M17): each mechanic's steps end to end, its stages, crew doing it when you don't, the same twice.
- **New `puzzle_check.py`** (H, outline in 6.8).
- **`machine_check`** (S): jobs left for you and the fault share per shift day; job kinds with steps; parts; tuning drift; incidents' machine side; team jobs; the pipe graph; the fault tables.
- **`player_check`** (P): the work steps, quicker tasks, the uniform, tidying, the off-shift activities.
- **`day_check`**: a laundry day, a Wednesday drill, a Thursday inspection, an incident day, a team-job day, a harvest day, a lift-roof day; draw calls under 450.
- **`deck_check`**: the new places; your cabin; the M9 rooms; Deck 6's gauges.
- **`intro_check`** on every push that touches jobs, the player or the clock.

---

## Part 5: building and checking (one team)

- **One build master, one branch, one release line.** The build master combines on `claude/integration-test` and hands the lead each candidate (what's in, every check result, every difference explained, the hash); only the lead pushes `claude/ship-integration` and publishes the playable link.
- **Reviews:** the build master reviews each branch against the checklist before combining. For the two riskiest pieces (the case engine with its solver, and promotion with the bed move) the lead may start **one short-lived reviewer** to try to break it, then archive it.
- **Check runners:** only for the slow checks, one or two at a time, archived when they report.
- **Phone speed:** the performance engineer, on call, runs `perf_check` on each candidate.
- **Playtesting:** the designer plays each check-in build (and a set of generated head-scratchers) before the user does, and notes anything unfair or confusing.
- **No cross-pillar crew:** with Pillar 4 finished first, the clash checks the earlier plan needed (`clash_check.py`, the shared page, two coordinators) aren't needed. Name clashes inside Pillar 5 are still caught by the existing `name_check`, and hash keys and save fields are checked by the build master.

---

## Part 6: Added: deductive repair puzzles ("head-scratchers")

**Added 2026-10-17 by the Pillar 5 designer, from the user's ask:** "I love our plan and want to keep it all. But we also need to add about 30-50% into the progression: deductive reasoning puzzles tied to repair. This is only some repairs, not all. And these go alongside all other stuff." **Everything in Parts 1-5 stays exactly as it is.** **What "30-50% into" means (the user's correction, 2026-10-17, through the lead):** the puzzles **start** about a third to a half of the way into the job's progression; the arc is not made longer. This part adds a second track beside the ladder, inside the existing arc. Mock-up screens: `plans/pillar5-puzzles-mockup.html` and `plans/shots/p5-puzzle-*.png`.

### 6.1 The idea in one paragraph

Some faults don't tell you their cause. The crew call them **head-scratchers**. The job card names a symptom ("the oven runs cool, but only at dinner"); a short list of **suspects** (the parts or causes it could be) goes into a new device page, **Fault notes**; and you collect **clues** by walking the ship: reading a machine's log at its panel, asking the crew who were there, finding the last shift's handover note, checking a gauge on Deck 5, looking at the week's calendar. Each clue lets you cross a suspect out. When you're sure, you **call it**: the job's part is set, and the rest is the ordinary loop (fetch, fit, turn in). It is the job loop's "Diagnose" step done for real, not a game laid over the job. A wrong call costs time and a walk, never a fail, and there's always "the long way" (fit each suspect in turn) so no case can ever leave you stuck.

### 6.2 How it fits the rules (an addition to Part 1's rule 3, nothing removed)

Rule 3 says "physical, not a mini-game … no puzzles that stand in for the work". Head-scratchers keep to its spirit:
- **The clues are in the world.** Every clue comes from a place you walk to or a person you find (by Roster, as now). Nothing is solved by tapping in a menu alone; the device only holds your notes.
- **The fix stays physical.** Calling it only names the part; you still fetch it, carry it and fit it with your hands.
- **No timers, no scores, no fail.** The ship keeps running (the device never pauses), but nothing counts down on a case.
- **Words, not numbers** for you: "Right first time", "A clever fix", "Fault-finder". Machine readings on a gauge are numbers, as the scanner's already are; your own progress never is.

*The user approved this (question 8, 2026-10-17); the lead has added it to design-doc.md.*

### 6.3 Which repairs get a puzzle (only some)

Only **real faults** (Part 1's "more real faults") can be head-scratchers, and only those with one of these shapes. Servicing, restocking, chores, laundry, hauling, the drill, incidents' make-it-safe step and team jobs never are. A plain fault stays plain: inspect, fetch, fit.

| Shape | What makes it a puzzle | From |
| --- | --- | --- |
| **Comes and goes** (intermittent) | It only happens at some times, or under some load | Tier 1, Day 14 |
| **Somebody tried already** | The last shift left notes on what didn't work | Tier 1, Day 13 |
| **Seen by others** | The crew saw it; you didn't | Tier 1, Day 17 |
| **The gauge is lying** | A sensor reads wrong, so the machine "looks fine" | Tier 1 with the scanner, Day 19 |
| **Starts somewhere else** (traced) | The symptom and the cause are on different machines | Tier 2 (M9's harder stages) |
| **Two parts, one symptom** | Several identical parts, one or two bad | Tier 2 |
| **A clash** | Fine on its own; trips when two things happen together | **Tier 3, a later pillar** (the user: keep it for later tiers) |

**How often** (a share of the real faults left for you; the 3-6 jobs a day don't grow, head-scratchers come out of them):

| When | Share of your real faults | At most |
| --- | --- | --- |
| Days 1-12 (Pillar 4's week, the first ladder steps) | none | — |
| Days 13-19 (first types taught) | about 1 in 8 (one every other shift day) | 1 open at a time, 1 new a day |
| Day 19 to promotion | about 1 in 6 | 1 open, 1 new a day |
| Tier 2, weeks 4-5 | about 1 in 5 (Tier 2 machines 1 in 3) | 2 open, 1 new a day |
| Tier 2, week 6 on (the last week of the arc, and after) | about 1 in 4 (Tier 2 machines 1 in 3) | 2 open, 2 new a day |

None are posted on days off or event days (Pillar 6); crew favour cases (6.6) can come off shift. If a case isn't taken by the end of your shift, the crew solve it the slow way (the long way, over a day) so the ship never waits on you. **No setting** for more or fewer (the user, question 10): the share is the same for everyone, and the hints and the long way keep it kind.

### 6.4 The nine puzzle types (eight in Pillar 5; the clash waits for Tier 3)

Every type has the same frame: **symptom → suspects (3-6) → clues at places → cross out → call it → fetch and fit.** Each is **taught** like a ladder step (the teacher works the first case with you, thinking aloud, then watches you do one, then it's yours) and adds a page of rules of thumb to **the Chief's notes** (6.5). Each grows in three bands: **T1** (Tier 1: 2-3 suspects, 2-3 clues, one deck), **T1+** (late Tier 1: 4 suspects, one clue that doesn't help, two decks), **T2** (Tier 2: 5-6 suspects, clues across decks and needing tools, one honest mistake among the witnesses), and the fault-finder band **T2+** (two causes at once, or a cause hiding a second one: "fixed it; now the real one shows").

**P1. When does it happen?** (Day 14, Torres)
- *Example (T1):* "Brennan's oven runs cool, but only at dinner." Suspects: the element, the door seal, the thermostat (a tuning job, M5), the Deck 3 power junction. Clues: the oven's log at its panel (fine at breakfast, sags 17:00-18:30), Brennan ("it's when the big range and the extractor are both going"), the junction's panel (its load peaks at dinner). A bad element or seal would be cool all day; a drifted thermostat wouldn't follow the range. **It's the junction, sagging under load.**
- *Grows:* T1+ two machines share the time; T2 "Deck 4 showers weak after 18:00" (the recycler's pump can't keep up at the evening peak, but a clogged filter would be weak all day); T2+ with **the logger** (a tool, 6.6): clip it on, come back tomorrow (the `wait` step) for a full day's trace.
- *Screen:* a day strip (00-24) with the machine's output as a bar per hour and your clues pinned at their times.

**P2. Who saw what?** (Day 17, Calder sets it, Tomas shows you how to ask)
- *Example (T1):* "The mess door on Deck 3 sticks now and then." Ask the crew (a new **Ask about the fault** button on the chat card): Brennan ("stuck when the hand pushed the food trolley through, just before lunch"), Pell ("fine at breakfast, I walked through"), Rina ("stuck at 17:10, the trolley again"), Tomas ("it stuck on me at 13:00!"; his schedule had him at the gym then: he means the gym door, an honest mix-up, never a lie). Suspects: the motor, the track, the safety sensor, the control relay. **Only when something wide goes through: the safety sensor misreads.**
- *Grows:* T1+ a witness who only saw part of it; T2 witnesses on two decks and one on a different shift you have to find (Roster); T2+ two stories that both are true and point to two faults.
- *Screen:* a card per person (portrait initial, where and when, what they said), with a tap to mark "doesn't fit".

**P3. What's been tried?** (Day 13, Torres; the first head-scratcher, the gentlest)
- *Example (T1):* "The lamp in Bunk 2 flickers." Taped to the job: Torres's note ("Swapped the bulb. Still flickers. Z."), and Pell's ("Reset the breaker last night: fine for an hour, then back"). Suspects: bulb, switch, the junction's relay, the wiring. The bulb is out; a switch or wiring fault wouldn't care about a reset; **fine for an hour then back is a relay warming up.**
- *Grows:* T1+ a note that rules out less than it seems ("changed the filter", but the wrong size was fitted); T2 a night-shift handover log with five entries; T2+ the cold-case board (6.6).
- *Screen:* the notes as paper slips, each crossing out what it proves.

**P4. Which gauge is lying?** (Day 19, Torres, with the scanner, M7)
- *Example (T1):* "The cold store's display says 3°, but the milk's going off." Clues: the chiller's own reading (3°), the scanner on the back shelf (9°), the door log (closed most of the night), Brennan's spoiled crate in Mail. Suspects: the compressor, the door seal, the fan, the temperature sensor. A bad compressor or seal would also show warm on the display; **the sensor is lying, so the chiller never works harder.**
- *Grows:* T1+ a table of three identical machines' readings, one out of step; T2 the scrubbers: 4-2 reads "air clean" while the junior wing is stuffy and 4-1 is working twice as hard; T2+ two sensors that disagree, both a little wrong.
- *Screen:* a small table (machines down, readings across); tap a cell to flag "doesn't match what I saw".

**P5. Follow the line** (Tier 2, with M9; Calder) *M9 as written is its first stage; this is how it gets harder.*
- *Example (T2):* "Showers on Deck 4 weak all day." The water line: recycler (Deck 3) → spine junction → manifold (Deck 5) → Deck 4 branch → showers. Each gauge is on a panel you have to walk to (the pipe kit reads it). Recycler fine, showers low: read the middle first (the manifold) and halve the line each time. **The low reading starts after the manifold's Deck 4 valve: it's sticking.**
- *Grows:* T2 one line, 4-5 gauges; T2+ a branch (two lines share a pipe), ducts for air, and the lights' circuits at Tier 2's junctions. Fewer walks is "a clever fix".
- *Screen:* the line as a simple map, gauges filled in as you visit; tap a stretch to mark it "fine".

**P6. Does it add up?** (Tier 2, with the pipe kit's second stage; Calder)
- *Example (T2):* "The garden's beds are dry at the far end." Water in must equal water out at each junction: the recycler sends 15, the branches read garden 6, Deck 4 5, galley 2: **2 are going missing**. The gallery has three joints between; read one, then the next, until the sum stops matching: **a leaking joint in the pipe gallery.**
- *Grows:* T2 one junction; T2+ two junctions and a gauge that's lying (P4 inside P6).
- *Screen:* the junction diagram with in and out sums, and a "missing" box that shrinks as you narrow it.

**P7. Faded labels** (Tier 2, Calder; a logic grid)
- *Example (T2):* The officers' corridor junction (4-junction-1) has four relays, A-D, whose labels have worn off, feeding the corridor, the closet, cabins 4-20 to 4-22, and cabins 4-23 to 4-25; one relay chatters. Clues: Pell's old sketch ("A isn't the corridor"), the Wednesday **power drill** (M3: the drill switches relay D off first, and you saw cabins 4-23 to 4-25 go dark), flipping a test switch and walking to see which lights blink (each flip is a walk), and the cabin where the lights flicker. **Work out which relay feeds what, then which one chatters.** Solving it lets you **relabel the panel** (it stays labelled in the save, and the next case there is quicker).
- *Grows:* T2 4×4; T2+ 5×5 with two clues from the night shift's log. Never larger than 5×5 on a phone.
- *Screen:* a tick-and-cross grid with big cells (at least 44 px); each clue sits under the grid.

**P8. Swap testing at the bench** (Tier 2, the machine shop tech; the **test rig**)
- *Example (T2):* The recycler's membrane bank has five cartridges; one is leaking. Taking them all is wasteful (stores run low, M4). At the machine shop's **test rig** you put any group of them on the rig, it runs for 10 ship minutes, and it says how many in the group leak, not which. You have 3 test runs before the shift's end. Test {1, 2} → none; test {3} → one: **cartridge 3.**
- *Grows:* T2 five cartridges, one bad, three runs; T2+ six cartridges, two bad, four runs. Running out of runs isn't a fail: Calder says "fit new ones all round", which costs the parts.
- *Screen:* the cartridges as five big toggles, "Run test", and a list of past runs with their answers.

**P9. The clash** (**moved to Tier 3, a later pillar**, the user's answer to question 16; designed here, built with Tier 3's "planning around people", which it fits: its fix moves a crew member's routine)
- *Example (T3):* "The recycler trips on Tuesdays and Fridays at 06:40." Clues: the device's Calendar and the crew's real week (Roster), the recycler's log: Tuesday is the laundry's big wash, both days have the gym's morning class showering, Friday the galley's bread bake fills the dish pit. Only the morning class falls on both days and nothing else does; but the class alone is fine on Wednesday (the log). **Class plus a second big draw trips it: the relief valve is fine, the load is the problem.** The fix: service the recycler and **ask the laundry hand to move Tuesday's wash to 08:00** (a short talk; it goes into their schedule).
- *Grows (at Tier 3):* two things clash; then three, and the fix you pick has a cost someone feels (Brennan grumbles if bread moves). Tier 3's power shutdowns ("pick a quiet hour") give it more to work with.
- *Screen:* a week grid (days across, the morning hours down) with the trips marked; tap a calendar item to lay it over.

### 6.5 Hints, mistakes and teaching

- **Hints, gentlest first:**
  1. **The Chief's notes** (a device page and a binder on Calder's shelf): rules of thumb per type and per kind of machine, a page added with each training ("Weak only at peak: the pump. Weak all day: the filter."). More rules appear for kinds you know well (the plan's skill in words). Free, always.
  2. **Ask a Works hand on shift** (at the board or the tea corner): they tell you what kind of clue you're missing ("Have you checked when it happens?"). Free.
  3. **Talk it through** with Torres or Calder (at the board, or an appointment): they cross one suspect out with you. The case can still be "right first time", but not "a clever fix".
  4. **The long way:** fit each suspect in turn. Always works.
- **What a wrong call costs:** the walk to storage and back, and the fitting time; the part you took goes back on the shelf unused (Tier 1). At Tier 2, a used seal or cartridge is spent (stock falls, restocked as usual; the user: yes). After two wrong calls on one case, Torres or Calder comes by to talk it through (hint 3, offered). Never a fail, never a remark worse than "Tricky one, that."
- **Teaching:** each type's first case is a training moment (Part 1's `train` slot): the teacher reads the first clue with you and thinks aloud, you finish it; the second you do while they watch. Opening rules as the ladder: never two openings on one day (a puzzle type counts as an opening), and each type waits until the one before has been solved about twice.

### 6.6 Where puzzles start, and how they grow

**The first head-scratcher comes about a third of the way into Pillar 5's progression.** The whole arc runs from Day 1 (Pillar 4's first week) to about Day 42 (the end of the after-promotion mechanics, week 6). The first puzzle is at about **Day 13: 13 of 42 days, about 31% of the way in by time**. Counted by milestones instead, it came after **5 of 12 ladder steps (about 42%)** when this was agreed; with the seven added mechanics (M11-M17, all after promotion) the ladder has 19 steps, so by steps it's now after 5 of 19 (**about 26%**). **By time played, which is what you feel, it's still 31%**, inside the user's 30-50%, and the user confirmed this start (question 9). Nothing is added to the arc's length: the seven fit in the same weeks 4-6.

| Share of the arc | Day | Where you are |
| --- | --- | --- |
| 0-17% | Days 1-7 | Pillar 4's first week: fetch and replace only. **No puzzles.** |
| 19-29% | Days 8-12 | The first ladder steps: rounds, laundry, the drill and inspection, hauling. **No puzzles.** |
| **31%** | **Day 13** | **The first head-scratcher** (P3 What's been tried?), taught by Torres, Tier 1 |
| 33-48% | Days 14-20 | Three more Tier 1 types and the certification job's puzzle step |
| 50-100% | Days 21-42 | Tier 2: four more types, the grades, the extras (beside M8-M17) |

**What triggers it:** not the date. The first head-scratcher opens like any ladder step (Part 1's rules): **once hauling (M4, the fourth step after your first week) has been used about 3 times**, on a day with no other opening, while you're still Tier 1. For a steady player that's about Day 13; a slower player gets it later, but always at the same point in the arc: after hauling, before tuning. It arrives as a training moment: Torres finds you at the board with a job the last shift couldn't crack.

**How the share grows after that** (6.3 has the details): about 1 in 8 of your real faults from the first one, 1 in 6 after the scanner, 1 in 5 at Tier 2, and 1 in 4 in week 6 (1 in 3 on Tier 2 machines). Only some repairs, never all.

**The puzzle track, beside the ladder** (fitted into the free days of the same arc; never two openings a day):

| Around | Share of arc | Opens | Taught by | Next to the ladder's |
| --- | --- | --- | --- | --- |
| Day 13 | 31% | **P3 What's been tried?** and the Fault notes page, the Chief's notes | Torres | after hauling (Day 12) |
| Day 14 | 33% | **P1 When does it happen?** | Torres | before tuning (Day 15) |
| Day 17 | 40% | **P2 Who saw what?** (the Ask button) | Calder, Tomas | after incidents (Day 16) |
| Day 19 | 45% | **P4 Which gauge is lying?** | Torres | the day after the scanner (Day 18) |
| Day 20 | 48% | the certification job gains one easy head-scratcher step | Calder | certification |
| Day 26 | 62% | **P5 Follow the line** (M9's harder stages); **the logger** | Calder | two days after tracing (M9, Day 24) |
| Day 30 | 71% | **P8 Swap testing** and **the test rig** | the machine shop tech | two days after the workshop (M10, Day 28) |
| Day 32 | 76% | **P6 Does it add up?** | Calder | |
| Day 34 | 81% | **Fault-finder** (grade 1), a ticket case | Calder | |
| Day 36 | 86% | **P7 Faded labels** | Calder | after rewiring (M15, Day 31) |
| Day 38 | 90% | **Trusted fault-finder** (grade 2) | Calder | |
| Day 39 | 93% | crew **favour cases** start | the crew | |
| Day 42 | 100% | **the cold-case board** | Calder | the end of Pillar 5 |
| After Pillar 5 | — | **the ship's fault-finder** (grade 3), whenever you're ready | Calder | keeps the puzzles going |
| Tier 3 (a later pillar) | — | **P9 The clash** | Calder | with Tier 3 |

*The seven added mechanics (M11-M17) take the odd days between these (Days 23-35), so there's never more than one opening a day.*

**What's new to earn:**
- **Fault-finder grades** (words, a small pin on your uniform): Calder sets a **ticket case** for each, a harder case on a Tier 2 machine, supervised like certification and, like it, **only ever delayed**. Fault-finder (Day 34) → Trusted fault-finder (Day 38) → the ship's fault-finder (after Pillar 5's arc, its ticket case ready when you are). *(The user: yes, three grades with pins.)* They sit inside Tier 2; they're not a promotion (Pillar 7's career story can build on them).
- **Tools that open new clue types** (each with its training, on the Tools page): the scanner (exists, M7: part readings, sensor tables), **the logger** (new, week 4: a day's trace for P1 T2+), the pipe kit (exists, M9: gauges along a line; stage 2: sums at junctions for P6), **the test rig** (new, a fixed bench in the machine shop: P8).
- **A name for clever fixes:** "right first time" (no wrong call) and "a clever fix" (right first time, no talk-it-through, few walks) go in the work log, lift Work reputation a little (`simNote('cleverFix')`, which Pillar 4's lines can react to: "Heard you sorted the mess door. The sensor! Who knew?"), and count toward experience (+1, like a found-by-you job).
- **Crew asking you for help:**
  - **Favour cases** (from Day 39, after Trusted fault-finder; the user: yes): crew bring you their own little mysteries off shift, as favours (the existing favours system): "My lamp flickers only when Pell plays guitar next door" (a shared circuit). Solved in their cabin; a friendship moment.
  - **Juniors stuck on a case** ask you at the board: you tell them which clue they're missing (pick one of three). The first taste of mentoring, which design-doc's Tier 2 "a junior tech to mentor" points to.
- **The cold-case board** (Day 42, as Pillar 5 ends, so it keeps puzzles coming afterwards; the user: yes): a board in Calder's office of old faults the crew never got to the bottom of, generated from the ship's own past weeks. Optional, for keen players; one at a time; solving one is a line in the Record.

**How it sits beside every Pillar 5 mechanic** (nothing in them changes; these are extra links):

| Mechanic | The link |
| --- | --- |
| Experience, skill in words | A head-scratcher counts like a repair, +1 if right first time; "Ovens: you know these well" also adds rules to the Chief's notes for ovens |
| More real faults | Head-scratchers are a share of the real faults, not extra jobs |
| M1 Rounds | A "something's off" mark can open a head-scratcher; stage 3 rounds read your loggers |
| M2 Laundry | Washer cases ("the whites come out grey on Tuesdays"); the laundry hand is a witness |
| M11-M17 (the seven) | Tool upkeep keeps the scanner and logger quick; your logbook lines come back as P3 clues; leak hunting's drips can be a P6 case; irrigation cases from the garden; rewiring leads into P7; coolant readings are clues for later engine cases; a lift judder is a P1 case from the roof |
| M3 Drill and inspection | The Wednesday power drill is a free P7 clue (which lights go dark first); no puzzles at the inspection |
| M4 Hauling and stores | Wrong calls at Tier 2 draw on stock (a stocktake shows it); "more filters taken than the log says" is a P3 clue |
| M5 Tuning | Some cases end "it's a setting, not a part": the answer is a tuning job |
| M6 Incidents | Never a puzzle while making it safe; afterwards an optional "why did it burst?" case for a clever fix |
| M7 Scanner | Its readings are one clue type; P4 opens the day after it |
| Certification, promotion | One easy head-scratcher step in the test job; the rest unchanged; still only delayed |
| M8 Team jobs | A case's answer can be "needs a team job"; never a puzzle during one |
| M9 Tracing | M9 is P5's first stage; P5 and P6 are how it grows |
| M10 Workshop | The test rig lives in the machine shop; a test jig can be a workshop order |
| Off shift | Favour cases come to you; tinkering, cabin touches, star logging unchanged |
| Device work pages | Fault notes (open cases) and the Chief's notes join Training, Work log and Tools |

### 6.7 How it shows on a phone

- **Fault notes** is a page in the device (registered from section 24 with `deviceApp`, like the other work pages), in the device's cyan old-screen style. One case per screen, top to bottom: the symptom; the **suspects** as big chips (tap to cross out, tap again to bring back; you cross them out, the game never does it for you); the type's own view (the day strip, the line map, the grid, the rig); the **clues** list (each with a small mark: clock, person, gauge, note, calendar); and a **Call it** button that asks which suspect, then sets the job's part and points the arrow at storage.
- **Clues arrive by doing:** reading a panel, asking someone (the Ask button on the chat card), finding a note at the board, a gauge on your rounds. Each brings a quiet "+ clue: Pell" toast and a badge on Fault notes; the tracked job's arrow can point at the next unvisited clue place (a "Where next?" button: the goal pointer, one arrow as now).
- **Touch first:** cells and chips at least 44 px, everything reachable with a thumb in the two-thirds sheet, no dragging needed (tap only), grids at most 5×5, maps at most 6 gauges on screen (scrolls sideways beyond). On the TriFold unfolded, Fault notes can stay docked beside the ship while you walk.
- **Nothing new in the 3D scene:** loggers are a tiny shared prop clipped to a machine (1 draw call each, at most 3); everything else is device screens. No draw-call cost on the decks.
- Mock-ups: `plans/pillar5-puzzles-mockup.html` (P1 the day strip, P5 the line, P8 the test rig), shots in `plans/shots/p5-puzzle-*.png`.

### 6.8 Built from the real ship, the same every time

**Fault tables** (section 17, data): for each machine kind, its **causes**: which part (or setting, or load), what the symptom looks like, when it shows (always, at load peaks, after use, at a time), what each reading says, and what each kind of clue would show. Kinds are added a few at a time (Tier 1 kinds first: oven, range, extractor, chiller, washer, lights, junction, doorgear; then Tier 2: scrubber, recycler, heater, airplant, fan, manifold, pump, filter).

**Making a case** (section 24k, when a real fault of a puzzle shape is posted for you):
1. **The seed:** `hash(machine id, day, 'case', k)` with Pillar 5's keys (puzzles: 880-894). Never `R()`.
2. **The true cause:** from the kind's causes, weighted by the machine's real wear (its worn parts likelier).
3. **The suspects:** the true cause plus 2-5 decoys from the same table, by band.
4. **The clues, from the simulation:**
   - logs and day strips from the machine's real load by hour (the schedules' use counters, `machNorm`): the oven really is busiest at dinner;
   - witnesses are crew who really were (or weren't) at that place at those times (the schedules, `schedWants`); a mixed-up witness is one whose schedule had them elsewhere, so the mix-up can be checked;
   - handover notes come from the real job history on that machine (who worked on it, what they fitted);
   - lines and sums from the pipe and duct graph (M9's `MACHINE_LINKS`) and a simple flow sum;
   - clashes from the real week (the calendar, rotas, traditions).
5. **Frozen:** the case (seed, cause, suspects, clue list) goes into the save when it's posted, so it doesn't change as the ship moves on; clue texts are built from it when you collect them.

**The solvability check, every case, at posting** (a small solver in the game, a few milliseconds):
- **Exactly one answer:** apply every reachable clue's eliminations; exactly one suspect must survive.
- **Needs thinking:** no single clue solves it alone; at least 2 clues at T1, 3 at T2.
- **Reachable:** every clue's place is open to your key and tier, the person is aboard and findable during the case, the tool is one you have.
- **In its band:** suspects, clues and decks within the band's limits.
- If any check fails, try the next sub-seed (`k + 1`), up to 8 times; if none passes, **it's a plain fault** (no puzzle). So a bad case can never reach you.

**`puzzle_check.py`** (new, the head-scratcher engineer's; outline):
```
load the build headless (like machine_check); new game; skip the intro
for seed in [two fixed saves]:
  step 8 ship weeks of days on paper, the player at Tier 1 then Tier 2 from day 22
  for each case posted:
    solver: brute force every suspect against every reachable clue -> exactly 1 left
    no single clue solves it; clue count within the band
    every clue reachable: place exists on its deck, person aboard and on the Roster
      in the case's window, tool owned at that tier, key opens the room
    the long way: fit each suspect in turn -> the case always ends
    a wrong call: time and a walk (T1 no stock used; T2 one consumable), never a fail
  shares: head-scratchers per tier within 6.3's table; never on a day off or event day;
    never more open than the limit; none before Day 13
  fallbacks: count cases that fell back to plain faults (warn above 10%)
  determinism: run it twice -> identical case lists (seed, cause, suspects, clues)
  save mid-case, load -> the same case, the same clues collected
  in a browser: making a case takes under 5 ms on the phone profile
cadet_test: with head-scratchers off, ALL IDENTICAL
```

### 6.9 What it adds to the build plan (seats, order, risks)

**Seats:** folded into Part 4's one lean team: the **designer** (D) covers the puzzle pages too, and one **head-scratcher engineer** (H) builds 24k and 24l across Steps 3, 5 and 6.

**On call:** systems (fault tables, machine load by hour, the job history, the logger's reading); player (the Ask button, the `choose` step reused for Call it); the device engineer (three small screen pieces: a day strip, a line map, a grid; until then Fault notes uses plain lists, still playable); sim (who was where, read-only); the Works writer (witness lines as templates, the handover notes, the Chief's notes, about 8 training scripts); deck architect 2 (the test rig's bench and the cold-case board as places; panel places for every gauge in P5/P6).

**Order (Part 4's steps):**
- **Step 1:** the designer writes the case-engine page and the P3/P1 pages.
- **Step 3:** H builds the case engine inert, then P3, P1, P2, P4 (Days 13-19). **Check-in 3** includes the first head-scratchers.
- **Step 4:** the certification job's puzzle step.
- **Step 5:** P5 with M9 and the logger, P8 with the workshop and the test rig.
- **Step 6:** P6, P7, the grades, favour cases, the cold-case board. (P9 waits for Tier 3.)
- **Hash keys:** 880-894 from Pillar 5's 850-899. **Save:** `save.career.cases` (open cases, solved count by type, grades, relabelled panels, cold cases done), read defensively; `SAVE_V` stays 2.
- **Section:** 24k and 24l, one owner; removing them turns every head-scratcher back into a plain fault.

**Risks:**
- **Unfair or unsolvable cases.** *Answer:* the solver at posting, the fallback to a plain fault, `puzzle_check`, the long way, and the designer playing generated cases each check-in.
- **Feeling like a mini-game.** *Answer:* clues only in the world, the fix physical, no timers or scores, real ship data so the answers make sense on the deck.
- **Too much reading on a small screen.** *Answer:* short clue lines (one sentence), grids at most 5×5, one case per screen, tap only.
- **Words to write.** *Answer:* witness lines and notes as templates filled from the case (who, where, when, what); the writer writes per type and per kind, not per case.
- **Too hard for some players, too easy for others.** *Answer:* bands by tier, hints gentlest first, the long way, grades and cold cases for the keen (no setting, the user's choice).
- **The device engineer's queue.** *Answer:* three small screen pieces from the device engineer, on call; until then Fault notes uses plain lists (still playable).
- **Section 17's load.** *Answer:* fault tables are data rows per kind, added a few kinds at a time; machine logs are worked out from the schedules when you look, not stored.

---

## Part 7: Added: career progression

**Added 2026-10-17 by the Pillar 5 designer, from the user (through the lead):** career progression moves **into Pillar 5** "since it all coincides" (until now it was Pillar 7's). The user's points: promotion must be **unmistakable** (a real summons to an appointment with the Chief during the work day, not a note); a **proper promotion scene** with the crew reacting and the badge; **someone senior walks you to your new quarters**, with your things already moved; a **small formal officer ceremony with the Captain** when you become an officer; later, at a higher rank, **a visitors' cabin on Deck 2 (the Command deck) becomes your cabin**; and it must be **clear how ranking up works: reputation from jobs is how you rank up and get better, more complex tasks.** Everything in Parts 1-6 stays; this part replaces only "The moment" in Part 2's certification card with the full sequence below.

### 7.1 How ranking up works (one clear rule)

**Do good work → your Works reputation grows → you're given harder, more interesting jobs → when it's high enough and you've learned the job, the Chief sets your certification → pass it and you're promoted.**

- **One measure you can see: your Works reputation,** in words, never a number. It's Pillar 4's Work reputation (the ship's opinion of your work, which already exists), so there's one idea, not two. Part 2's "experience" and "trust" are what feed it, not separate things you track.
- **What raises it:** jobs finished (bigger faults count more), faults you found before they broke, the right part first time, a clever fix on a head-scratcher, turning up to the drill and the inspection, keeping your shift. **What lowers it:** missed shifts and abandoned jobs (the design's existing rules, with their warnings and the Chief's talk).
- **What it gives you: better, more complex tasks.** Each band changes which jobs the crew leave for you on the board (the systems engineer's "jobs left for you"):

| Band (words; Pillar 4's Work bands where they already have words) | Jobs left for you | Ladder and career |
| --- | --- | --- |
| **New** (week 1) | fetch and replace, chores | Pillar 4's first week |
| **Steady** | about half real faults; rounds, laundry, hauling | the week-2 mechanics open |
| **Reliable** | urgent jobs too; the first head-scratchers; tuning and incidents | Days 13-19's openings |
| **Trusted** | a supervised Tier 2 job now and then; the hardest Tier 1 faults | Calder says you're nearly there |
| **Relied on** | — | **Calder sets your certification** |

  After promotion the bands start again for your new rank ("New officer" → … → "Relied on"), and each lifts you to harder Tier 2 work: traced faults, team jobs, Tier 2 head-scratchers, then the fault-finder tickets.
- **The ladder still waits for use** (Part 1): a mechanic opens when the one before has been used a few times **and** your reputation has reached its band. For a steady player the band is already there, so nothing changes; a careless player waits a little longer, and is told why.
- **You always know where you stand:** your device's Record shows your rank, your reputation in words and **one "What's next" line** ("Calder wants to see you handle a scrubber before she puts you up"); Calder's progress talks (built in Pillar 3) say the same in person. Never demoted: a falling reputation only means fewer interesting jobs until you pick up again.

### 7.2 The ranks, and which promotions happen in Pillar 5

The ship's ranks (design-doc): Junior Officer → Officer → Senior Officer → Department Chief → Executive Officer → Captain. **You climb but never command**, so your career tops out at Senior Officer.

| Rank | Works title (tier) | Room | Ceremony | When |
| --- | --- | --- | --- | --- |
| Junior Officer | Junior Technician (Tier 1) | Bunk 1, junior wing (Deck 4) | — | Day 0, your arrival (Pillar 4) |
| **Officer** | **Technician (Tier 2)** | **Cabin 4-23, officers' corridor (Deck 4)** | **The officer ceremony with the Captain** | **About Day 20: built in full in Pillar 5** |
| Officer | the fault-finder grades (inside Tier 2) | 4-23 | a pin from Calder at the board | Days 34-38, and after (Part 6) |
| **Senior Officer** | **Senior Technician (Tier 3)** | **Deck 2's second visitors' cabin, converted to yours** | a smaller one: the Captain's word at the Captain's table | **When Tier 3 comes (a later pillar)**: designed now, its scenes built on Pillar 5's machinery |
| Senior Officer | Engine Specialist (Tier 4) | your Deck 2 cabin | a commendation | later still |

*This changes two lines in design-doc.md (the lead's): the player could rise "to Officer and senior technician, but not beyond", and Tiers 3-4 were "Officer" rank. The plan's default puts Tiers 3-4 at **Senior Officer**, the rank of the six senior officers who live on Deck 2 and sit at briefings (the conference table "by right from Tier 3" already fits). Still never command. (Question C3.)*

**Inside Pillar 5's arc** (Day 1 to about Day 42) that's **one promotion, Junior Officer to Officer, with the whole sequence (7.3)**, plus the fault-finder grades as smaller recognitions. The second promotion needs Tier 3's work (shutdowns, planning around the crew) to mean anything, so it goes live when Tier 3 is built (question C2). Pillar 5 builds every piece it uses (the summons, the scene, the escorted move, the ceremony, the cabin conversion as data), so the later pillar only adds Tier 3 and switches it on.

### 7.3 The first promotion, step by step (about Day 20)

1. **The certification job** (Part 2, unchanged): a real Tier 2 job held for you, with Calder following. Only ever delayed: if it goes wrong she tells you there and then what to practise and sets another in a week.
2. **The summons, the next work day:** mid-morning (about 10:30) your device sounds an **urgent toast**, not a quiet badge: *"Chief Calder: My office, 11:00. — C."* It's a real appointment (Pillar 3's appointments) in her glass office in the Works bay. The goal arrow points there, and Torres says "Go on. She doesn't bite. Usually." **It can't be missed:** if you don't come by 11:15, Calder walks over to find you wherever you are on the ship (the escort's lead-and-follow walking, from Pillar 4) and says it there.
3. **The scene in her office** (a short meeting, `MEETING_SCRIPTS`): she tells you you've passed; she hands you the **Technician's badge** and your **Officer's collar pip**; one choice of reply (proud, surprised, "about time"), which she remembers.
4. **The crew react:** you walk out into the Works bay and the Works crew on shift have gathered by the board: applause, Torres's grin, a "Told you" from Pell if he's on. That day **everyone who knows you reacts** when you meet (Pillar 4's lines via `simNote('promoted')`: friends congratulate, acquaintances nod, a rival grumbles), **Mail** from friends and the Captain, a **ship news item** in the Ship app, and **Brennan's cake** at the Works tea corner after the shift.
5. **Your new quarters, that evening (about 17:00):** **Calder walks you there** (on her day off, Commander Vance, the Executive Officer): from the Works bay, up the lift, along the officers' corridor (the escort's walking again; she talks on the way about officers' ways: your door, the "Come over" visits, quiet hours). **On the way you pass Tomas and Pell carrying your box.** At 4-23 the **door plate already has your name and rank**; your key opens it; **your things are already there**: your locker's contents, the keepsakes on your shelf, the framed menu if you have one, gifts you were given. Tomas says goodbye as a bunkmate ("Don't be a stranger, Officer"). That night you sleep in your own cabin, and Pillar 4's "Come over" visits start.
6. **The officer ceremony, the next afternoon (about 16:30, after your shift):** a summons from the Captain's office by Mail in the morning, so you can get ready (a clean uniform matters: M2). In the **observation room on Deck 1** (the conference table, the stern windows): the Captain, Commander Vance, Calder, Torres, and the friends you're closest to (up to three, invited by the game from your relationships). Short and formal: the Captain reads your commission, **pins your Officer's insignia** (your uniform now shows it: a small collar mark, a material change, no new meshes), a handshake, one line from you, a toast with the Captain's tea. A **keepsake** (the framed commission) goes on your cabin shelf. Your Record: "Commissioned Officer, Day 21."
7. **After:** your Tier 2 key opens the Deck 5 machine rooms and the pipe galleries; the board starts leaving you Tier 2 jobs; the next mechanic (team jobs) opens the day after; your reputation bands start again as "New officer".

*Pacing check:* certification about Day 20, the summons Day 21 morning, the move Day 21 evening, the ceremony Day 22 afternoon. Team jobs (M8) open on Day 22 as planned, so the ceremony and team jobs share a day: the ceremony isn't a ladder opening, so Part 1's "one opening a day" still holds.

### 7.4 The second promotion (designed now; live when Tier 3 comes)

- **Ranking up again works the same way:** Tier 2 reputation reaches "Relied on", the ladder's Tier 2 steps are used, and Calder sets a Tier 3 certification (a supervised shutdown job, once Tier 3 exists).
- **The summons comes from higher up:** Calder first ("My office"), then together to the **Captain's ready room**, where the Captain tells you yourself.
- **Your Deck 2 cabin:** the **second visitors' cabin** (inside the senior corridor's loop, no window, next to the Deputy Survey Chief) **is converted to yours.** You see it happen: in the days before, a Works job on the board refits it (you can take it yourself or leave it to the crew), and its door plate changes from "Visitors" to your name. **Commander Vance walks you up to Deck 2**, with your things moved from 4-23 (which goes back to being a spare). The visitors' suite and Envoy Saruth's cabin stay as they are; from then on, ship-wide events (Pillar 6) lodge any extra visitors in Deck 4's guest cabins. (Question C4: or the visitors' suite, with its window.)
- **The ceremony:** smaller, as senior officers have it: the Captain's word and a toast at the **Captain's table** dinner (built in Pillar 3), and your place at the conference table "by right".

### 7.5 What moves where (and how Pillar 7 shrinks)

| Was in Pillar 7 | Now |
| --- | --- |
| How ranking up works (reputation, certification, what's next) | **Pillar 5** (7.1) |
| The first promotion's scenes: summons, crew reaction, badge, escorted move, officer ceremony | **Pillar 5** (7.3) |
| The second promotion's design and machinery (the Deck 2 cabin conversion, Vance's walk, the Captain's table) | **Pillar 5** builds it; it **switches on with Tier 3** |
| Tier 3 (Senior Technician: shutdowns, planning around the crew, "the clash" puzzle) and Tier 4 (Engine Specialist: engine repairs, leading team jobs) | **Pillar 7** |
| The night shift assignment, the story and milestones around your career, mentoring a junior | **Pillar 7** |

**So Pillar 7 becomes "Tiers 3 and 4, and the story":** it adds new work and story to a career system that already exists, rather than building the system. (design-doc.md's roadmap is the lead's to update; question C10.)

### 7.6 What it adds to the build (lean, no new seats)

- **Who:** the **career engineer (C)** already owns certification and promotion; the scenes are theirs. The **designer** writes a "Promotion" spec page (the sequence, the scripts' outline, the ceremony's room and guests) and a short page for the second promotion. **On call:** sim (Calder coming to find you, the crew gathering, the ceremony's guests, `playerBed()`, Tomas and Pell carrying the box, Vance's walk later), performance (the collar mark on your uniform, a box-carry pose), deck architect 2 (4-23's door plate and keepsake shelf, ceremony places in the observation room, Deck 2's second visitors' cabin as data for later), the Works writer (the summons, the scene, the crew's reactions, the walk, the ceremony), social (reactions on `simNote('promoted')`).
- **When:** the reputation bands and "What's next" in **Step 1** (the foundation: C with S, since bands decide which jobs are left for you); the whole first promotion in **Step 4** (already the promotion step; check-in 4 now plays the summons, the scene, the move and the ceremony); the second promotion's machinery inert in **Step 6**, tested on paper. **No new seats; still at most about 6 at once.**
- **Save:** `save.career` gains rank, reputation band per rank, ceremony done, keepsakes; read defensively; `SAVE_V` stays 2.
- **Tests (`career_check`):** the bands change the jobs left for you; the summons is an urgent appointment during the shift, and Calder comes to find you if you miss it; the badge and pip; the move (bed, door plate, things, Tomas's goodbye); the ceremony's guests are there and it happens once; an old save loads as Tier 1; the second promotion's conversion on paper (door plate, bed, 4-23 back to spare) with a test-only Tier 3 switch; determinism twice. **`day_check`** on Day 21 and Day 22 (the crew still reach their places around the gathering and the ceremony). **`intro_check`** unchanged.
- **Risks:** *a promotion you miss* (answer: the urgent toast, Calder comes to you, the move waits for you); *crowding Deck 1 and the voice budget at the ceremony* (answer: at most about 8 people, after shifts, never on an event or tradition evening; it moves a day if needed); *a hollow second promotion* (answer: it waits for Tier 3's real work).

---

## Risks

- **Too much at once for a new player.** *Answer:* the ladder: one mechanic at a time, taught by a person, never two on a day, waiting for you to use the last one; everything earlier keeps working the simple way.
- **Mechanics turning into mini-games** (the design's "no mini-games standing in for the job"). *Answer:* every verb happens in the world with your hands; feedback is the machine itself; no timers or scores; tuning flagged to the user.
- **Phone draw calls (450).** Laundry baskets, crates, puddles, smoke, made things, the new rooms. *Answer:* each mechanic's props at most 2-3 draw calls (instanced, its deck only, only while in use); cabin spots at most 4; the M9 rooms measured by `deck_check`; the performance engineer on call.
- **Determinism.** Faults, drift, incidents and which part fails are chosen. *Answer:* hashed from ids and the day or hour, never `R()`; every check runs twice.
- **The one-file merge load.** *Answer:* Pillar 5 is built on its own after Pillar 4 (the user's choice), by at most about 6 helpers; one new section with a sub-block per mechanic; one build master (Part 5).
- **Breaking Pillar 4's first week.** *Answer:* reserved jobs untouched; the ladder starts on Day 8; `intro_check` on every relevant push.
- **The crew still do everything.** *Answer:* each mechanic's crew side is measured in `mech_check` (they do it when you don't, but slower) so the ship never depends on you, and there's still work for you.
- **Two ideas of reliability.** *Answer:* trust reads Pillar 4's Work reputation.
- **Beds.** *Answer:* Pillar 4 is finished first, so the cabin move clashes with nothing; 4-23 is a spare (checked against the crew designer's reserve pool).
- **Head-scratchers (Part 6):** unfair cases, mini-game feel, small screens, writing load, difficulty, the device queue, section 17's load. *Answer:* Part 6.9.
- **The seven added mechanics.** The lift roof is the riskiest (the lift and the camera in the shaft): it comes last, through the lift's owner, measured by `perf_check`. *Answer:* each of the seven is small, its own sub-block, after promotion, at most one opening a day.
- **Usage limits and memory.** *Answer:* a lean team (about 6 at most, 4 if needed), the lead's hourly check-in, the 70% handover rule; each mechanic is small enough for one session.

---

## The user's answers (2026-10-17), and new questions

1. **Tuning (M5):** turning a setting and watching the machine respond: right side of "no mini-games"? **Answered: yes, as described.**
2. **Your uniform:** grubby with work, changed at your locker, washed through the laundry. Should a grubby uniform look different on your character (a duller shade)? **Answered: yes, slightly duller.**
3. **Laundry duty:** about once a week on a junior rota, with crew covering if you skip it. **Answered: less often: about every two weeks** (crew cover if you skip it). M2 updated.
4. **The ladder's pace:** about one new mechanic every 2-3 ship days after week 1, promotion at about Day 20. **Answered: yes.**
5. **Which "more ideas"** (leak hunting, tool upkeep, the lift roof, irrigation, coolant rounds, the logbook, rewiring) should join the ladder? **Answered: all seven.** On the ladder as M11-M17 after promotion (Part 2, "The seven from more ideas").
6. **Your own cabin:** Spare 4-23 (no window)? **Answered: yes.**
7. **The coordinator in Step 1:** should X1 (the code coordinator) start in Step 1 to watch the career engineer's branch and draft the shared table early, or wait for Step 2 with the rest of the crew? **Answered: no early coordinator; and "this has changed: we will develop Pillar 5 on its own. Please restructure the labor plan accordingly."** Parts 4 and 5 rewritten: one lean team after Pillar 4, no coordinators, one build master, check-ins kept.

**Added with Part 6 (head-scratchers):**

8. **The ground rule:** may design-doc.md's "No mini-games standing in for the job" gain a line: "Deduction puzzles are the Diagnose step done for real: clues gathered in the world, the fix physical, no timers or scores"? **Answered (the user, 2026-10-17): yes.** design-doc.md updated by the lead on `claude/lead-pillar1`.
9. **The start and the share:** the first head-scratcher after hauling has been used about 3 times (about Day 13, about a third of the way into the arc), then about 1 in 8 of your real faults, rising to about 1 in 4 at Tier 2 (1 in 3 on Tier 2 machines)? **Answered: yes, as planned.**
10. **A setting** for fewer / normal / more head-scratchers? **Answered: no setting.** 6.3 updated.
11. **The nine types:** keep all nine, or drop any (P8 swap testing and P7 faded labels are the most "puzzle-like")? **Answered: keep all nine** (eight built in Pillar 5; the clash moves to Tier 3, question 16).
12. **Fault-finder grades** (three, in words, with a uniform pin, only delayed): yes? **Answered: yes.**
13. **Wrong calls at Tier 2 spend a consumable part** (a seal, a cartridge), while Tier 1 wrong calls only cost time? **Answered: yes.**
14. **Crew favour cases and the cold-case board** (optional, for keen players)? **Answered: yes, both.**
15. **The name:** "head-scratchers" (the crew's word), "Fault notes" (the device page), "the Chief's notes" (the hint binder)? **Answered: yes, keep the names.**
16. **The P9 fix moves a crew member's routine** (the laundry wash to 08:00): fine for a Tier 2 case, or keep moving routines for Tier 3 (Pillar 7)? **Answered: keep it for later tiers.** P9 The clash moves to Tier 3 (a later pillar), designed here and built with Tier 3.

**Added with Part 7 (career progression), for the user's survey:**

- C1. **The summons:** an urgent toast mid-morning the day after you pass ("My office, 11:00"), and Calder comes to find you if you don't come. Right? *Default:* yes.
- C2. **How many promotions in Pillar 5:** just the first (Officer, about Day 20), with the second (Senior Officer, the Deck 2 cabin) built now but switched on when Tier 3's work comes in a later pillar? Or build Tier 3 into Pillar 5 too, so the Deck 2 move happens in this pillar (a much bigger pillar)? *Default:* the first only; the second switches on with Tier 3.
- C3. **Your top rank:** Senior Officer at Tier 3 (the rank whose crew live on Deck 2 and sit at briefings), still never in command? The design doc today says you stop at Officer. *Default:* yes, Senior Officer.
- C4. **Which Deck 2 cabin becomes yours:** the second visitors' cabin (inside the loop, no window), or the visitors' suite (on the hull, with a window)? Envoy Saruth's stays hers either way. *Default:* the second visitors' cabin; events then lodge extra visitors on Deck 4.
- C5. **Who walks you to your new cabin:** Calder (Commander Vance on her day off), with Tomas and Pell carrying your box past you? *Default:* yes.
- C6. **The move:** the same evening as the summons? *Default:* yes, about 17:00.
- C7. **The officer ceremony:** the next afternoon after your shift, in the observation room on Deck 1, with the Captain, Commander Vance, Calder, Torres and up to three of your closest friends? *Default:* yes.
- C8. **Your insignia:** should your uniform show your rank (a small collar mark) once you're an officer? *Default:* yes.
- C9. **Reputation in words** in your Record, with one "What's next" line, and bands deciding which jobs are left for you? A falling reputation means fewer interesting jobs, never a lower rank. *Default:* yes.
- C10. **Pillar 7's new scope:** Tiers 3 and 4 (with the second promotion switched on), the night shift, the career story and milestones, mentoring a junior. *Default:* yes.
