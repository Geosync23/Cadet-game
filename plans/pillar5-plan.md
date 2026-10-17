# Pillar 5 plan: new ways to work (expanded core mechanics)

**DRAFT 2 (2026-10-17, the Pillar 5 planner, branch `claude/pillar5-plan`).** Rewritten from the user's survey answers (`plans/pillar5-notes.md`, "The user's answers"): **Pillar 5 is expanded core mechanics only.** Ship-wide events move to Pillar 6; career progression, story and the night shift to Pillar 7 (design-doc.md, "Roadmap after Pillar 4"). The user asked for a detailed plan before any work, and for new mechanic ideas from the planner. **Nothing is built until the user approves this plan, and each mechanic gets its own short spec page the user reviews before it's built.**

Read with `design-doc.md` ("The clockwork", "The player", "Works progression", "Roadmap after Pillar 4"), `plans/pillar4-plan.md` (Part 6: the rules for sharing the one game file), `TEAM.md`, `DEV_NOTES.md` ("Machines and wear", "Chores and openJobs", "Player needs and the device", "Player interactions", "Hook register") and the handover notes for systems, player, galley and device.

A plain-language version for the user is `plans/pillar5-plan.html`.

**Added 2026-10-17 (the Pillar 5 designer): Part 6, deductive repair puzzles ("head-scratchers").** The user: keep the whole plan, and add deduction puzzles to some repairs, **starting about 30-50% of the way into the progression** (the early job has none). They begin about a third of the way in (Day 13 of the Day 1 to about Day 42 arc) and grow from there. Part 6 adds a track beside the ladder, inside the same arc; nothing in Parts 1-5 is removed or shrunk.

---

## The pitch (one page)

Today the Works job is one verb: **fetch a part and replace it** (or hold to work at a spot for a chore). Pillar 4's first week teaches that loop. Pillar 5 gives the job **a ladder of new mechanics**, each a different way of working with your hands, **unlocked slowly, one at a time, each taught to you by a person**, so you start simple and the job keeps opening up as you work on more of the ship.

**The ladder** (about one new mechanic every two or three ship days after your first week; numbers are starting points):

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
| — | **Certification and your first promotion** | a supervised job using what you've learned | Calder | about Day 20 |
| 8 | **Team jobs** | one pair of hands on a big job with others | a Works officer | after promotion |
| 9 | **Tracing connected faults** (Tier 2) | follow a symptom back along pipes and ducts | Calder | after promotion |
| 10 | **The workshop** | crew order small things; you make them | the machine shop tech | after promotion |

**Added (Part 6):** beside the ladder, a **puzzle track**: some real faults become **head-scratchers** you solve by deduction from clues gathered around the ship (nine types; the first about a third of the way in, at Day 13, after hauling; then growing to the end of Pillar 5 at about Day 42, with fault-finder grades, two new tools and crew asking you for help).

Around the ladder: **more real faults reach you**; **repairs get quicker with practice** (in words); **tools arrive one at a time, each with training**; **off-shift tinkering, cabin touches and star logging**; **the device's work pages** (your training record, work log, tools). Still Works only.

**How it's built:** each mechanic is **one self-contained sub-block of a new section 24 with one owner**, on top of a small shared foundation (the unlock ladder, training moments, work-step building blocks). A **mechanic designer** writes each mechanic's one-page spec for the user ahead of the builders. **Timing (the user's middle path):** after approval only clash-free work starts (the designer's spec pages and the inert foundation inside section 24); full building starts when Pillar 4 is mostly writing. Staffing is tiered and generous (the user: "don't be afraid to hire as many as needed"): up to 11 building seats, plus a **Pillar 5 build master**, **two cross-pillar coordinators** who keep Pillar 4 and Pillar 5 from colliding, adversarial reviewers and check runners, mirroring Pillar 4's Full level (Part 5), with steps to scale down. **A check-in with the user after every one or two mechanics.**

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
- **Pacing:** a ship day is 40 real minutes. Week 1 is Pillar 4's; the ladder's first nine steps fit in weeks 2-3 (about 9 real hours), so the first promotion lands at about 2 ship weeks of steady work after your first week (the user's "2 weeks"). The last three mechanics come after promotion, spread over weeks 4-6.

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

- **The verb:** you now have a **uniform** that gets grubby as you work (oily jobs faster, a shower doesn't clean it). Change at your locker (a clean one from your stack), **drop the worn one in the laundry**, and every so often **take a laundry duty**: load a washer, start it, come back when it's done (it runs about 40 ship minutes: the `wait` step), move the load to the dryer, fold, and deliver the clean linen to the bunk rooms by cart.
- **Why it matters:** a grubby uniform drains hygiene faster and gets remarks (exists); **the Thursday inspection checks it** (M3); clean linen in the bunks helps everyone's sleep a little; the washers wear with use, so you also see their faults coming. Crew do laundry duty too (a junior rota), so if you skip it someone else does.
- **Taught:** a laundry hand (a Works junior on the rota) shows you a full duty once.
- **Grows:** stage 1, your own uniform; stage 2, laundry duty on the rota (about once a week); stage 3, you can service the washers between loads (the washers become real machines with panels).
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
- **The moment:** at the board the next morning Calder hands you the Officer's badge in front of the Works crew (a short meeting); the Captain's Mail; the news spreads (`simNote('promoted')`).
- **Your own cabin:** Spare 4-23 on the officers' corridor: your bed and locker move, the door opens for you, Tomas says goodbye as a bunkmate, and Pillar 4's "Come over" visits start. *(Bigger story around promotion is Pillar 7; Pillar 5 builds the working moment.)*
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

### More ideas (not in the ladder yet; the user can pick any)

- **Leak hunting:** find a hidden drip by listening (a sound cue grows louder near it, once sound comes in) and looking for the puddle.
- **Tool upkeep:** your tools wear; recharge the scanner and clean the kit at your bench on Friday afternoons.
- **Lift maintenance from the car roof:** ride on top of the lift car between decks to service its guides (a unique view of the spine).
- **Garden irrigation work** with the garden crew: clear nozzles along the racks while they harvest.
- **Coolant top-ups on Deck 6:** a weekly round with the engine crew, reading gauges on the coils.
- **Logbook:** write a line in the Works log at the end of a shift (a choice of three summaries); Calder reads it at progress talks.
- **Rewiring:** replace a junction box's wiring by following a colour chart on the panel (a careful `choose` sequence).

---

## Part 3: not colliding with Pillar 4

### Which parts of the game Pillar 5 touches, and when

| Part of the file | Pillar 4 | Pillar 5 | How they stay apart |
| --- | --- | --- | --- |
| **24 WORK (new)**: 24 core + one sub-block per mechanic (24a rounds … 24j workshop) | — | the career engineer (core) and the mechanic engineers (one sub-block each) | new, lazy at load; one owner per sub-block; hooks out are one line, typeof-guarded, in the register |
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
- **Merge order:** Pillar 5 after Pillar 4 each round: … → systems (17) → player (15) → career (24 core) → mechanics (24a…) → deck architect 2. The **Pillar 5 build master** combines Pillar 5's branches on its own candidate branch, on top of the latest released Pillar 4 build, and the **cross-pillar coordinators** check every combine for clashes first (Part 5).
- **Notes on the bus:** `simNote('trained', { mech })`, `simNote('found', { machine })`, `simNote('incident', { id, step })`, `simNote('promoted')`, `simNote('uniform', { state })`, so Pillar 4's lines and reputation can react without new hooks.

---

## Part 4: staffing, waves and check-ins

### The building seats (tiered; up to 11; the build and coordination crew is in Part 5)

**Tier 1, the foundation** (F1 and F4 start right after approval, in Step 1; F2 and F3 start in Step 2, when Pillar 4 is mostly writing):

| # | Seat | New? | Branch | Builds | Owns |
| --- | --- | --- | --- | --- | --- |
| F1 | Mechanic designer | **new** (no code) | `claude/p5-design` | — | `plans/mechanics/<id>.html`, one page per mechanic for the user, a step ahead of the builders; keeps this plan current; answers builders' design questions |
| F2 | Systems engineer | existing role, **fresh session** (takes section 17 back from the sim engineer) | `claude/ship-systems` | 0.33.38+ | section 17; `machine_check.py` |
| F3 | Player engineer | existing | `claude/player-needs` | 0.28.23+ | section 15; `player_check.py` |
| F4 | Career engineer | **new** | `claude/works-career` | 0.44.x | section 24 core (ladder, training, tools, skill, trust, drill and inspection hooks, certification, promotion, device pages); `career_check.py`; `mech_check.py`'s frame |

**Tier 2, the mechanics** (from Step 2 on; each joins when its spec page is approved; two or three at a time):

| # | Seat | New? | Branch | Builds | Owns |
| --- | --- | --- | --- | --- | --- |
| M-A | Rounds and tuning engineer | new | `claude/mech-rounds` | 0.45.x | 24a rounds, 24e tuning |
| M-B | Laundry engineer | new | `claude/mech-laundry` | 0.49.x | 24b laundry and uniforms, 24c the drill and inspection |
| M-C | Stores and workshop engineer | new | `claude/mech-stores` | 0.51.x | 24d hauling and stores, 24j the workshop, the off-shift tinkering |
| M-D | Incidents and team-jobs engineer | new | `claude/mech-incidents` | 0.52.x | 24f incidents, 24h team jobs |
| M-E | Diagnosis and tracing engineer | new | `claude/mech-diagnose` | 0.53.x | 24g scanner and diagnosing, 24i traced faults |

**Tier 3, support:**

| # | Seat | New? | Branch | Builds | Owns |
| --- | --- | --- | --- | --- | --- |
| S1 | Deck architect 2 | new | `claude/decks-p5` | 0.47.x | `// P5 places` blocks in `DECKS[n]`, kit at the end of 4b |
| S2 | Works writer | new (or a Pillar 4 writer moved over in their wave 4) | `claude/writer-p5` | — | `content/` lines for training moments, incidents, inspection remarks, the promotion; reports to Pillar 4's head writer |

**On call:** sim (rotas, musters, the duty officer, the stuck lift, crew at team jobs, `playerBed()`), performance (poses and decals), galley (oven tuning's effect on cooking, Brennan's lines), social A (Work reputation as trust; reactions), device (only if the skin needs something), interactions (tap targets for new places), crew designer (the junior laundry rota, if it's roster data). **This planner** stays on until the mechanic designer is hired, then hands over (`plans/handover-pillar5-planner.md`).

*(Build ranges 0.44, 0.45, 0.47, 0.49 and 0.51-0.54 confirmed free by the build master, 2026-10-17.)* The build master, reviewers, check runners, watchdog and the cross-pillar coordinators are in **Part 5**.

### The briefs (ready to paste)

**Every brief starts with this paragraph:** "You are the <seat> for Starship Cadet's Pillar 5 (new ways to work). Read CLAUDE.md, then DEV_NOTES.md, plans/pillar5-plan.md (Parts 1 and 3, your seat in Part 4, and your mechanics in Part 2), plans/pillar5-notes.md (the user's answers), the approved spec page for each mechanic you build (plans/mechanics/<id>.html), plans/pillar4-plan.md Part 6 (the rules for sharing the one game file with Pillar 4, which is building at the same time), TEAM.md, and your predecessor's handover note if your role had one. Push only to <branch>. Touch only what your seat owns; anything else goes through its owner via the lead. Each turn: small exact-string edits (never rewrite the game file), bump the build in the HUD, add a DEV_NOTES row, run the tests (one browser check at a time; always `intro_check` when you touch jobs, the player or the clock), commit, push, and report to the lead (the current lead is named at the top of TEAM.md; at the time of writing session_01KPJMYjXAPkNUcrQ8VRkhLE) with send_message; the Pillar 5 build master takes your branch from there. Hooks into other sections are one-line, typeof-guarded, and listed in DEV_NOTES' hook register. Hand over at about 70% memory with plans/handover-<role>.md. Commit messages end with the Co-Authored-By line; never put model names anywhere else."

- **F1 Mechanic designer.** For each mechanic in Part 2, in ladder order, write `plans/mechanics/<id>.html` in the style of `plans/pillar5-plan.html`: what you do step by step (with a small sketch), who teaches it and the training script outline, how it unlocks and grows, what the crew do, what changes on the deck, what it asks of each section, the phone budget, and 2-3 questions for the user. Stay one or two pages ahead of the builders; the lead shows each page to the user; nothing is built from a page the user hasn't approved. Also weigh the "more ideas" list with the user's picks.
- **F2 Systems engineer.** Section 17. First: take section 17 back from the sim engineer (session_01R6RBwwBM9aorpsqDCrztDU) and read `plans/handover-systems.md`. Then: `playerTier()` (inert); real faults for you (`CREW_LEAVE_FAULT`, the `found` delay, crew busier on bigger jobs, measured in `machine_check`); **job kinds with steps** (a job carries a mechanic id and its steps, so each mechanic's jobs post, are claimed by crew, and are done by you through section 24); then each mechanic's machine side as its spec asks: rounds' found jobs, the washers as real machines, manifests and stock counts, tuning drift, parts and readings, incidents, team jobs, the pipe graph. Never change a reserved job.
- **F3 Player engineer.** Section 15. The work-step building blocks (`look`, `choose`, `turn`, `wait`, and `hold`/`carry` as now) as data a mechanic can describe; `careerSpeed(kind)` in task minutes; your uniform (worn, grubby, changed at the locker) and its hygiene effect; tidying your berth; the off-shift activities (tinkering, cabin spots, star logging). Keep `player_check` current.
- **F4 Career engineer.** (Step 1: inside section 24 only, inert, with stand-ins for sections 15 and 17; Pillar 4's build master combines you until B1 is hired.) New lazy section `// 24. WORK` (after section 21) with the core: `SHIP.career` and `save.career`, `CAREER_LADDER`, `careerHas`, training moments (a `train` slot on `jobReserve`, the teacher leading then following, meeting lines, `simNote('trained')`), tools, skill in words, trust (reads Work reputation; a stand-in until it's in), the drill and inspection hooks for M-B, certification and promotion (with the sim engineer for the bed and door), the device pages (Training, Work log, Tools via `deviceApp`). `career_check.py`, and the frame of `mech_check.py` that each mechanic adds a part to. Give out hash keys from 850-899.
- **M-A … M-E Mechanic engineers.** Build your mechanics from their approved spec pages, each in its own sub-block of section 24 (`// 24a. ROUNDS` and so on), on the foundation's building blocks; ask F2/F3/F4 directly (sideways, as TEAM.md allows) for anything the foundation lacks rather than editing their sections. Add your part to `mech_check.py`. One mechanic at a time: build it, test it, the user plays it at a check-in, then the next.
- **S1 Deck architect 2.** Read the Pillar 4 deck architect's handover and DEV_NOTES "How decks work". Places and dressing for Pillar 5's rooms in `// P5 places` blocks: the laundry (load, dryer, fold, the linen cart dock), storage count spots and the hold's crates, valves by the corridors, the extinguisher and bulkhead, your cabin 4-23 with its spots, the Deck 5 machine rooms and the spine (M9), the machine shop's order board. `deck_check` on every push; other decks pixel-identical.
- **S2 Works writer.** Follow `content/README.md`, the voice bible and the voice cards. Write the training moments, the incidents' lines, the inspection's nods and remarks, the drill, the promotion and the workshop orders; report to the head writer.

### Steps and the staffing ramp (the user's middle path, 2026-10-17)

The user chose the middle path: **(1)** nothing starts until the user approves this plan; **(2)** after approval, only clash-free work starts: the mechanic designer's spec pages and the shared foundation inside Pillar 5's own new section 24, inert; **(3)** full Pillar 5 building (the mechanic engineers, the second build master and the rest of Part 5's crew) starts when **Pillar 4 enters its mostly-writing stage**, after Pillar 4's wave 3 engineering, so Pillar 5's mechanics aren't squeezed by Pillar 4's busy sections.

**Step 0: approval (now).** The user reads this plan and approves it. Nothing is hired, nothing is built.

**Step 1: the clash-free start (after approval, alongside Pillar 4's waves 2-3).** Two seats only: **F1 the mechanic designer** and **F4 the career engineer**.
- F1 writes the spec pages: the foundation (the ladder, training moments, the work-step building blocks), then M1 rounds, M2 laundry, M3 the drill and inspection, M4 hauling, staying one or two pages ahead of the builders from then on.
- F4 builds the foundation **only inside the new section 24**, on paper and inert: `SHIP.career` and the save, `CAREER_LADDER` as data, training moments as data, tools, skill in words, trust with its stand-in, the device pages registered but hidden, `career_check.py` and `mech_check.py`'s frame. Where it needs section 15 or 17 (task minutes, job kinds with steps, `playerTier()`), it uses typeof-guarded stand-ins and writes down what it will ask F2 and F3 for. **It touches no other section.**
- **Who combines it:** Pillar 4's build master, as one small branch in its rounds (a new section only; `cadet_test` ALL IDENTICAL, every check passes), reviewed by Pillar 4's reviewers. No Pillar 5 crew is hired yet.
- **Check-in 1 (pages only):** the user approves the foundation page and the spec pages for M1-M4. Nothing to play yet.

**Step 2: full building starts (when Pillar 4's wave 3 engineering is done and Pillar 4 is mostly writing).** The lead hires the Part 5 crew first (**B1** the Pillar 5 build master, **X1 and X2** the coordinators, **R3** the reviewer, 2-3 check runners; the watchdog is shared), and X1 builds the shared table and `clash_check.py` before the first Pillar 5 combine. Then the building seats: **F2** systems (takes section 17 back from the sim engineer), **F3** player, **M-A**, **M-B**, **S1** deck architect 2, **S2** the Works writer.
- First the foundation's other half: `playerTier()`, more real faults, job kinds with steps (17), the work steps (15). Gate: inert first (`cadet_test` ALL IDENTICAL, `intro_check` passes), then switched on.
- Then M1 rounds, M2 laundry and uniforms, M3 the drill and inspection.
- **Check-in 2:** play a work day with more real faults and quicker repairs, then your second week: a round, a laundry duty, a drill and an inspection.

**Step 3: hauling and tuning.** M-C (M4), M-A (M5); **R4** joins. **Check-in 3.**

**Step 4: incidents, the scanner and promotion.** M-D (M6), M-E (M7), F4's certification and promotion (with the sim engineer's bed move; Pillar 4's crew coming and going is done by now). **Check-in 4:** a burst pipe, the scanner, and from a save near certification to your own cabin.

**Step 5: after promotion.** M-D (M8 team jobs), M-E (M9 tracing), M-C (M10 the workshop, tinkering), F3 (cabin touches, star logging). **Check-in 5:** Pillar 5 final; then a pull request to `main` with the user's OK.

**The staffing ramp** (Pillar 5 sessions active, not counting on-call helpers):

| Step | When | Pillar 5 seats active | About |
| --- | --- | --- | --- |
| 0 | now | none (this planner, answering questions) | 0 |
| 1 | after approval, during Pillar 4's waves 2-3 | F1, F4 | 2 |
| 2 | Pillar 4 mostly writing | F1, F2, F3, F4, M-A, M-B, S1, S2 + B1, X1, X2, R3, 2-3 check runners | 14-15 |
| 3 | | + M-C, R4 | 16-17 |
| 4 | | + M-D, M-E (M-A, M-B winding down) | 17-19 |
| 5 | | M-C, M-D, M-E, F3, F4, S1, S2 + the crew | 12-14 |

The lead can drop to Normal or Lean at any step (Part 5).

### Test changes

- **New `career_check.py`** (F4): the ladder (never two on a day; waits for use), training moments, tools, skill words, trust, certification (pass, delay, pass), promotion, the cabin, the save, an old save, determinism twice.
- **New `mech_check.py`** (F4's frame, one part per mechanic): each mechanic's steps end to end, its stages, crew doing it when you don't, the same twice.
- **`machine_check`** (F2): jobs left for you and the fault share per shift day; job kinds with steps; parts; tuning drift; incidents' machine side; team jobs; the pipe graph.
- **`player_check`** (F3): the work steps, quicker tasks, the uniform, tidying, the off-shift activities.
- **`day_check`**: a laundry day, a Wednesday drill, a Thursday inspection, an incident day, a team-job day; draw calls under 450.
- **`deck_check`**: the new places; your cabin; the M9 rooms.
- **`intro_check`** (Pillar 4's) on every push that touches jobs, the player or the clock.

---

## Part 5: the build and coordination crew (mirrors Pillar 4's Full level)

The user (2026-10-17): "don't be afraid to hire as many as needed. Like some workers focused on keeping the two pillar development straight. Like our reviewers but specifically for this task", and "We might want a 2nd master builder for Pillar 5. We should mirror our current structure to the appropriate scale." So Pillar 5 gets its own copy of Pillar 4's Full-level crew (TEAM.md, "Staffing levels"), smaller, plus **two cross-pillar coordinators** whose only job is keeping the two pillars from colliding.

### The seats

| # | Seat | New? | Branch | Builds | Does |
| --- | --- | --- | --- | --- | --- |
| B1 | **Pillar 5 build master** | new | `claude/integration-test-p5` | candidates numbered by the lead's release line | combines and checks Pillar 5's branches on its own candidate branch, always on top of the latest released `claude/ship-integration`; runs the Pillar 5 check runners; hands the lead each candidate: what's in, every check result, explained differences, the hash to release |
| X1 | **Cross-pillar coordinator 1: the code** | new | `claude/cross-pillar` (notes and a script only) | — | owns the shared ownership table and the shared hook register for both pillars (`plans/cross-pillar.md`); writes and runs `clash_check.py`; checks every Pillar 5 branch against Pillar 4's current branches (and the reverse) before it's combined |
| X2 | **Cross-pillar coordinator 2: the work** | new | `claude/cross-pillar-2` (notes only) | — | watches for duplicate or overlapping work across the two pillars' seats (designs, data, lines, places, Mail, device pages); keeps the clash log; settles small overlaps sideways and sends anything bigger to the lead |
| R3 | **Adversarial reviewer 3** | new | `claude/reviews-3` (notes only) | — | reviews every Pillar 5 branch before it's combined (PASS / PASS WITH FIXES / BLOCK), using `plans/review-checklist.md` plus a Pillar 5 section it adds: mechanics stay physical, words not numbers, the ladder's rules, determinism, phone budget |
| R4 | Adversarial reviewer 4 (from Step 3, when more mechanic engineers are active) | new | `claude/reviews-4` | — | splits the Pillar 5 branches with R3 (R3: foundation and M-A, M-B; R4: M-C, M-D, M-E, S1) |
| CR | **Pillar 5 check runners** (2-3, short-lived) | new each time | — | — | run one check each on B1's candidate in parallel, report to B1, archived when they report |
| W | **Phone-speed watchdog** | shared: performance engineer 2 (`claude/crowd-render`) | — | — | `perf_check` on every combined build from either pillar; a second watchdog only if it can't keep up |
| PT | Playtester (from Step 2, shared with Pillar 4's if there is one) | — | — | — | plays each Pillar 5 check-in build as a new player would, before the user does |

**Reporting** (TEAM.md's chain of command): all of these report to the lead. B1 and X1 also send every clash straight to Pillar 4's build master (session_012K7RZ3oSX2vpBb1rR66MBh), sideways, so both build masters see it at once.

### How the two build masters share one ship

- **One `claude/ship-integration`, one release line, one releaser.** Only the lead pushes `claude/ship-integration` and publishes the playable link. Releases stay in one sequence (0.60.N, …); each release note says whose round it was.
- **Separate candidate branches.** Pillar 4's build master builds candidates on `claude/integration-test`; Pillar 5's on `claude/integration-test-p5`. Neither ever pushes to the other's.
- **Pillar 4 releases first each round.** When both have a candidate ready, Pillar 4's goes first. Pillar 5's build master then **merges** the new release into its candidate (a merge, never a rebase, so helpers' checkouts stay valid), re-runs every check, and only then offers it to the lead. A Pillar 5 candidate built on an older release is never released as it is.
- **Never racing.** While a Pillar 4 candidate is with the lead, B1 finishes its checks but waits. If Pillar 4 has nothing ready, Pillar 5 can release on its own. If one pillar is blocked for long, the lead may alternate rounds instead.
- **Before every combine, either pillar's:** X1 runs `clash_check.py` on the incoming branches against the other pillar's latest candidate; X2 confirms nothing duplicates work in flight; then the build master combines.
- **Generated blocks** (ROSTER, LINES, MEETINGS, TRADITIONS) are always re-generated after a merge, never merged by hand (Pillar 4's rule).
- **Pillar 5's merge order inside a round:** systems (17) → player (15) → career (24 core) → mechanics (24a…, in ladder order) → deck architect 2 → Works writer's lines (through the head writer's generated blocks).

### What the coordinators check

`clash_check.py` (X1's, run on any two branches or a branch against a candidate):
- **Sections touched:** every changed line is mapped to its section; a branch touching a section it doesn't own (by the shared ownership table) is flagged.
- **Names:** any new top-level `const`, `let`, `function` or `class` that already exists elsewhere (the player engineer's handover lists two real collisions this caused).
- **Hash keys:** every `schedU(..., k)` / `k:` against the shared key list (Pillar 4: 434-849; Pillar 5: 850-899; Pillar 6 later: 950-999; section 18's `k + 100` rule).
- **Save fields:** new `save.*` and `SAVE_EXTRA` entries, and anything that changes `SAVE_V`.
- **Build ranges and HUD lines:** each branch's build number inside its seat's range.
- **Hooks:** every new one-line cross-section call is in the shared hook register.
- **Merge order:** the branch's base is the latest release (or it says why not).

X2's watch list: two seats designing the same thing (as when two seats both built a tasting vote); the same machine, room or place changed by both pillars' architects; the same crew member's lines or schedule changed by both; device pages that say the same thing; Mail that would arrive twice; traditions or events that would stack on the same evening. X2 reads both pillars' seat lists, their latest pushes and the spec pages each round.

**The shared page `plans/cross-pillar.md`** (X1 and X2): the ownership table for every section and sub-block across both pillars, the shared hook register (DEV_NOTES keeps its copy in step), the hash-key list, the save fields, the build ranges, and the clash log (open and settled).

### Briefs (ready to paste; each starts with Part 4's common paragraph)

- **B1 Pillar 5 build master.** Read TEAM.md ("Chain of command", "Staffing levels") and Pillar 4's build master's notes first; agree the hand-off in this part with them (session_012K7RZ3oSX2vpBb1rR66MBh) before your first combine. Combine Pillar 5 branches on `claude/integration-test-p5`, always on top of the latest `claude/ship-integration`, in the merge order above, after X1's clash check and R3/R4's verdicts. Run every check (start check runners for the slow ones, one check each); explain every difference; never release: hand the lead the candidate's hash, what's in and every result. When Pillar 4 releases while you have a candidate, merge the release in and re-run everything.
- **X1 Cross-pillar coordinator (the code).** Build `plans/cross-pillar.md` from both plans, DEV_NOTES' hook register and key list, and the current branches. Write `clash_check.py` (git diff by section, names, keys, save fields, builds, hooks, base). Run it on every Pillar 5 branch before B1 combines it and on every Pillar 4 branch that touches a section Pillar 5 uses, and on each pair of candidates before a release. Send each clash to the owners of both branches, both build masters and the lead; log it. You never edit the game file.
- **X2 Cross-pillar coordinator (the work).** Each round, read both pillars' seat lists, the latest pushes, the spec pages and the tradition and line work in flight; look for duplicated or overlapping work (X2's watch list above). Settle small overlaps directly with the two seats (who does it, who drops it); anything that changes a seat's scope or the design goes to the lead. Keep the clash log in `plans/cross-pillar.md` with X1.
- **R3 / R4 Adversarial reviewers.** Read `plans/review-checklist.md` and add a Pillar 5 section (mechanics physical, no timers or scores, words not numbers, the ladder's rules, `intro_check` run, determinism twice, phone budget, one owner per sub-block). Review each Pillar 5 branch before it's combined: try to break it, then give PASS / PASS WITH FIXES / BLOCK with a note to the lead and the branch's owner.
- **CR Check runners.** Run the one check you're given on B1's candidate, report the result and any failure's details to B1, then idle to be archived.

### Pillar 5's staffing levels (like TEAM.md's)

| Level | Who is active (Pillar 5) | Who merges and checks Pillar 5 |
| --- | --- | --- |
| **Full** | the wave's seats + B1 + X1 + X2 + R3 (+R4 from Step 3) + 2-3 check runners + the shared watchdog (+ playtester from Step 2) | B1 on `claude/integration-test-p5`; X1/X2 before each combine; R3/R4 before each branch; the lead releases |
| **Normal** | the wave's seats + B1 + one coordinator (X1 takes X2's watch list) | B1 combines; seats self-check against the review checklist; check runners only when needed |
| **Lean** | at most 2-3 seats on the current mechanic's critical path; everyone else on standby | Pillar 4's build master combines Pillar 5 branches in its own rounds (after Pillar 4's); X1 runs `clash_check.py` only |

**Scaling down from Full to Normal (the lead):**
1. R3/R4: finish the review in hand, send findings, idle; archived. Seats self-check against `plans/review-checklist.md`.
2. X2: write its open watch items into `plans/cross-pillar.md`, idle; archived. X1 takes the watch list.
3. Check runners: stop starting new ones; archive those that reported.
4. Playtester (if any): write findings, idle, archive.

**Normal to Lean:**
1. B1: finish the current combine, push its state to `claude/integration-test-p5`, write `plans/handover-build-master-p5.md` (what's merged, what's pending, check results), idle; archived. Pillar 4's build master takes Pillar 5 branches in its rounds.
2. Pause every seat not on the current mechanic's critical path ("finish your turn, push, update your handover note, idle"): the writer and the designer first (their work is text), then the mechanic engineers not on the current mechanic.
3. X1 stays (light: `clash_check.py` before each combine), or hands its table to Pillar 4's build master if usage must drop further.

**Scaling back up:** the reverse; reopen archived sessions or hire fresh ones from the handover notes. Nothing is lost: every role's work is on its branch and in its handover note.

**Head count at Full:** 4 foundation seats + up to 5 mechanic engineers + 2 support (deck architect 2, the writer) + B1 + 2 coordinators + 1-2 reviewers + 2-3 short-lived check runners: about 16-19 Pillar 5 sessions at the busiest (Steps 3-4), alongside Pillar 4's wave 4 (when Pillar 4 is mostly writers, who are light on usage). The lead can drop to Normal or Lean at any time with the steps above.

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
| **A clash** | Fine on its own; trips when two things happen together | Tier 2, late |

**How often** (a share of the real faults left for you; the 3-6 jobs a day don't grow, head-scratchers come out of them):

| When | Share of your real faults | At most |
| --- | --- | --- |
| Days 1-12 (Pillar 4's week, the first ladder steps) | none | — |
| Days 13-19 (first types taught) | about 1 in 8 (one every other shift day) | 1 open at a time, 1 new a day |
| Day 19 to promotion | about 1 in 6 | 1 open, 1 new a day |
| Tier 2, weeks 4-5 | about 1 in 5 (Tier 2 machines 1 in 3) | 2 open, 1 new a day |
| Tier 2, week 6 on (the last week of the arc, and after) | about 1 in 4 (Tier 2 machines 1 in 3) | 2 open, 2 new a day |

None are posted on days off or event days (Pillar 6); crew favour cases (6.6) can come off shift. If a case isn't taken by the end of your shift, the crew solve it the slow way (the long way, over a day) so the ship never waits on you. A Settings line, **Head-scratchers: fewer · normal · more**, scales the share (open question 10).

### 6.4 The nine puzzle types

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

**P9. The clash** (Tier 2, late; Calder; a taste of Tier 3's "planning around people")
- *Example (T2):* "The recycler trips on Tuesdays and Fridays at 06:40." Clues: the device's Calendar and the crew's real week (Roster), the recycler's log: Tuesday is the laundry's big wash, both days have the gym's morning class showering, Friday the galley's bread bake fills the dish pit. Only the morning class falls on both days and nothing else does; but the class alone is fine on Wednesday (the log). **Class plus a second big draw trips it: the relief valve is fine, the load is the problem.** The fix: service the recycler and **ask the laundry hand to move Tuesday's wash to 08:00** (a short talk; it goes into their schedule).
- *Grows:* T2 two things clash; T2+ three, and the fix you pick has a cost someone feels (Brennan grumbles if bread moves).
- *Screen:* a week grid (days across, the morning hours down) with the trips marked; tap a calendar item to lay it over.

### 6.5 Hints, mistakes and teaching

- **Hints, gentlest first:**
  1. **The Chief's notes** (a device page and a binder on Calder's shelf): rules of thumb per type and per kind of machine, a page added with each training ("Weak only at peak: the pump. Weak all day: the filter."). More rules appear for kinds you know well (the plan's skill in words). Free, always.
  2. **Ask a Works hand on shift** (at the board or the tea corner): they tell you what kind of clue you're missing ("Have you checked when it happens?"). Free.
  3. **Talk it through** with Torres or Calder (at the board, or an appointment): they cross one suspect out with you. The case can still be "right first time", but not "a clever fix".
  4. **The long way:** fit each suspect in turn. Always works.
- **What a wrong call costs:** the walk to storage and back, and the fitting time; the part you took goes back on the shelf unused (Tier 1). At Tier 2, a used seal or cartridge is spent (stock falls, restocked as usual). After two wrong calls on one case, Torres or Calder comes by to talk it through (hint 3, offered). Never a fail, never a remark worse than "Tricky one, that."
- **Teaching:** each type's first case is a training moment (Part 1's `train` slot): the teacher reads the first clue with you and thinks aloud, you finish it; the second you do while they watch. Opening rules as the ladder: never two openings on one day (a puzzle type counts as an opening), and each type waits until the one before has been solved about twice.

### 6.6 Where puzzles start, and how they grow

**The first head-scratcher comes about a third of the way into Pillar 5's progression.** The whole arc runs from Day 1 (Pillar 4's first week) to about Day 42 (the end of the after-promotion mechanics, week 6). The first puzzle is at about **Day 13: 13 of 42 days, about 31% of the way in by time**. Counted by milestones instead, it comes after **5 of the arc's 12 ladder steps** (fetch and replace, rounds, laundry, the drill and inspection, hauling; then tuning, incidents, the scanner, certification, team jobs, tracing, the workshop): **about 42% of the way in**. Either way it sits inside the user's 30-50%, and nothing is added to the arc's length.

| Share of the arc | Day | Where you are |
| --- | --- | --- |
| 0-17% | Days 1-7 | Pillar 4's first week: fetch and replace only. **No puzzles.** |
| 19-29% | Days 8-12 | The first ladder steps: rounds, laundry, the drill and inspection, hauling. **No puzzles.** |
| **31%** | **Day 13** | **The first head-scratcher** (P3 What's been tried?), taught by Torres, Tier 1 |
| 33-48% | Days 14-20 | Three more Tier 1 types and the certification job's puzzle step |
| 50-100% | Days 21-42 | Tier 2: five more types, the grades, the extras |

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
| Week 4 (Days 22-28) | 52-67% | **P5 Follow the line** (M9's harder stages); **the logger** | Calder | with M9 |
| Week 5 (Days 29-35) | 69-83% | **P8 Swap testing** and **the test rig**; **P6 Does it add up?**; **Fault-finder** (grade 1) | the machine shop tech; Calder | after the workshop (M10) |
| Week 6 (Days 36-42) | 86-100% | **P7 Faded labels**; **P9 The clash**; **Trusted fault-finder** (grade 2); favour cases | Calder, the crew | the end of Pillar 5 |
| After Pillar 5 | — | **the ship's fault-finder** (grade 3) and **the cold-case board** | Calder | they keep the puzzles going into Pillar 7 |

**What's new to earn:**
- **Fault-finder grades** (words, a small pin on your uniform): Calder sets a **ticket case** for each, a harder case on a Tier 2 machine, supervised like certification and, like it, **only ever delayed**. Fault-finder (week 5) → Trusted fault-finder (week 6) → the ship's fault-finder (after Pillar 5's arc, its ticket case ready when you are). They sit inside Tier 2; they're not a promotion (Pillar 7's career story can build on them).
- **Tools that open new clue types** (each with its training, on the Tools page): the scanner (exists, M7: part readings, sensor tables), **the logger** (new, week 4: a day's trace for P1 T2+), the pipe kit (exists, M9: gauges along a line; stage 2: sums at junctions for P6), **the test rig** (new, a fixed bench in the machine shop: P8).
- **A name for clever fixes:** "right first time" (no wrong call) and "a clever fix" (right first time, no talk-it-through, few walks) go in the work log, lift Work reputation a little (`simNote('cleverFix')`, which Pillar 4's lines can react to: "Heard you sorted the mess door. The sensor! Who knew?"), and count toward experience (+1, like a found-by-you job).
- **Crew asking you for help:**
  - **Favour cases** (week 6, after Trusted fault-finder): crew bring you their own little mysteries off shift, as favours (the existing favours system): "My lamp flickers only when Pell plays guitar next door" (a shared circuit). Solved in their cabin; a friendship moment.
  - **Juniors stuck on a case** ask you at the board: you tell them which clue they're missing (pick one of three). The first taste of mentoring, which design-doc's Tier 2 "a junior tech to mentor" points to.
- **The cold-case board** (the last day of week 6, so it opens as Pillar 5 ends; it keeps puzzles coming afterwards): a board in Calder's office of old faults the crew never got to the bottom of, generated from the ship's own past weeks. Optional, for keen players; one at a time; solving one is a line in the Record.

**How it sits beside every Pillar 5 mechanic** (nothing in them changes; these are extra links):

| Mechanic | The link |
| --- | --- |
| Experience, skill in words | A head-scratcher counts like a repair, +1 if right first time; "Ovens: you know these well" also adds rules to the Chief's notes for ovens |
| More real faults | Head-scratchers are a share of the real faults, not extra jobs |
| M1 Rounds | A "something's off" mark can open a head-scratcher; stage 3 rounds read your loggers |
| M2 Laundry | Washer cases ("the whites come out grey on Tuesdays"); the laundry hand is a witness, and the one asked to move the wash in P9 |
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

**New seats** (joining Part 4's tiers; nothing in Part 4 changes):

| # | Seat | New? | Branch | Builds | Owns |
| --- | --- | --- | --- | --- | --- |
| F1b | **Puzzle designer** (this role, no code) | new (now) | `claude/pillar5-plan`, then `claude/p5-design` with F1 | — | a spec page per puzzle type and for the case engine, the Chief's notes' rules, the fault tables' causes in plain words; plays generated cases for fairness |
| M-F | **Head-scratcher engineer 1** | new | `claude/mech-cases` | to be confirmed free by the build master (suggest 0.55.x) | 24k: the case engine, the solver, Fault notes, the Chief's notes, hints, P1-P4, `puzzle_check.py` |
| M-G | **Head-scratcher engineer 2** (from Step 5) | new | `claude/mech-cases-2` | suggest 0.56.x | 24l: P5-P9 (P5 with M-E), the logger, the test rig, grades, favour cases, the cold-case board |

**On call:** F2 systems (fault tables, machine load by hour, the job history, the logger's reading); F3 player (the Ask button, the `choose` step reused for Call it); the device engineer (three small screen pieces: a day strip, a line map, a grid; after Pillar 4's wave 3); sim (who was where, read-only; the moved laundry wash in P9); S2 the Works writer (witness lines as templates, the handover notes, the Chief's notes, ~9 training scripts); S1 deck architect 2 (the test rig's bench and the cold-case board as places; panel places for every gauge in P5/P6).

**Order (fits Part 4's steps, adds one):**
- **Step 1:** F1b writes the case-engine page and the P3/P1 pages (pages only).
- **Step 3** (hauling and tuning): M-F builds the case engine inert, then P3 and P1 (Days 13-14 sit between hauling and tuning). **Check-in 3** includes a first head-scratcher.
- **Step 4** (incidents, scanner, promotion): M-F adds P2 and P4 and the certification step. **Check-in 4** includes the mess door and the lying chiller.
- **Step 5** (after promotion): M-G joins; P5 with M-E's M9, P8 with M-C's workshop, P6.
- **New Step 6:** P7, P9, the grades, favour cases, the cold-case board. **Check-in 6:** play weeks 5-6 from a save. (This is an extra build step, not extra ship days: the puzzles fit inside the existing arc.) Then Pillar 5 final and the pull request.
- **Head count:** +1 now (the designer), +1 from Step 3, +1 from Step 5: about 18-21 Pillar 5 sessions at the busiest instead of 16-19. Lean still works: M-F alone covers P1-P4.
- **Hash keys:** 880-894 from Pillar 5's 850-899. **Save:** `save.career.cases` (open cases, solved count by type, grades, relabelled panels, cold cases done), read defensively; `SAVE_V` stays 2.
- **Section:** 24k and 24l, one owner each; removing them turns every head-scratcher back into a plain fault.

**Risks:**
- **Unfair or unsolvable cases.** *Answer:* the solver at posting, the fallback to a plain fault, `puzzle_check`, the long way, and F1b playing generated cases each check-in.
- **Feeling like a mini-game.** *Answer:* clues only in the world, the fix physical, no timers or scores, real ship data so the answers make sense on the deck.
- **Too much reading on a small screen.** *Answer:* short clue lines (one sentence), grids at most 5×5, one case per screen, tap only.
- **Words to write.** *Answer:* witness lines and notes as templates filled from the case (who, where, when, what); the writer writes per type and per kind, not per case.
- **Too hard for some players, too easy for others.** *Answer:* bands by tier, hints gentlest first, the fewer/normal/more setting, grades and cold cases for the keen.
- **The device engineer's queue.** *Answer:* three small screen pieces, asked for after Pillar 4's wave 3; until then Fault notes uses plain lists (still playable).
- **Section 17's load.** *Answer:* fault tables are data rows per kind, added a few kinds at a time; machine logs are worked out from the schedules when you look, not stored.

---

## Risks

- **Too much at once for a new player.** *Answer:* the ladder: one mechanic at a time, taught by a person, never two on a day, waiting for you to use the last one; everything earlier keeps working the simple way.
- **Mechanics turning into mini-games** (the design's "no mini-games standing in for the job"). *Answer:* every verb happens in the world with your hands; feedback is the machine itself; no timers or scores; tuning flagged to the user.
- **Phone draw calls (450).** Laundry baskets, crates, puddles, smoke, made things, the new rooms. *Answer:* each mechanic's props at most 2-3 draw calls (instanced, its deck only, only while in use); cabin spots at most 4; the M9 rooms measured by `deck_check`; the performance engineer on call.
- **Determinism.** Faults, drift, incidents and which part fails are chosen. *Answer:* hashed from ids and the day or hour, never `R()`; every check runs twice.
- **The one-file merge load.** Up to about 19 Pillar 5 sessions next to Pillar 4 at the busiest. *Answer:* one new section with a sub-block per mechanic; a Pillar 5 build master and two cross-pillar coordinators (Part 5); Pillar 4 releases first each round; mechanics two or three at a time.
- **Breaking Pillar 4's first week.** *Answer:* reserved jobs untouched; the ladder starts on Day 8; `intro_check` on every relevant push.
- **The crew still do everything.** *Answer:* each mechanic's crew side is measured in `mech_check` (they do it when you don't, but slower) so the ship never depends on you, and there's still work for you.
- **Two ideas of reliability.** *Answer:* trust reads Pillar 4's Work reputation.
- **Beds.** *Answer:* the cabin move waits for Pillar 4's wave 3; 4-23 is a spare (checked against the crew designer's reserve pool).
- **Head-scratchers (Part 6):** unfair cases, mini-game feel, small screens, writing load, difficulty, the device queue, section 17's load. *Answer:* Part 6.9.
- **Usage limits and memory.** *Answer:* tiered hiring, the lead's hourly check-in, the 70% handover rule; each mechanic is small enough for one session.

---

## Open questions for the user (with the plan's defaults)

1. **Tuning (M5):** turning a setting and watching the machine respond: right side of "no mini-games"? *Default:* yes, with no timer or score.
2. **Your uniform:** grubby with work, changed at your locker, washed through the laundry. Should a grubby uniform look different on your character (a duller shade)? *Default:* yes, slightly.
3. **Laundry duty:** about once a week on a junior rota, with crew covering if you skip it. *Default:* yes.
4. **The ladder's pace:** about one new mechanic every 2-3 ship days after week 1, promotion at about Day 20. *Default:* yes.
5. **Which "more ideas"** (leak hunting, tool upkeep, the lift roof, irrigation, coolant rounds, the logbook, rewiring) should join the ladder? *Default:* none yet; the designer brings the user's picks as spec pages after Step 2.
6. **Your own cabin:** Spare 4-23 (no window)? *Default:* yes.
7. **The coordinator in Step 1:** should X1 (the code coordinator) start in Step 1 to watch the career engineer's branch and draft the shared table early, or wait for Step 2 with the rest of the crew? *Default:* wait for Step 2; in Step 1 there's only one small new-section branch, which Pillar 4's build master and reviewers already cover.

**Added with Part 6 (head-scratchers):**

8. **The ground rule:** may design-doc.md's "No mini-games standing in for the job" gain a line: "Deduction puzzles are the Diagnose step done for real: clues gathered in the world, the fix physical, no timers or scores"? **Answered (the user, 2026-10-17): yes.** design-doc.md updated by the lead on `claude/lead-pillar1`.
9. **The start and the share:** the first head-scratcher after hauling has been used about 3 times (about Day 13, about a third of the way into the arc), then about 1 in 8 of your real faults, rising to about 1 in 4 at Tier 2 (1 in 3 on Tier 2 machines)? *Default:* yes.
10. **A setting** for fewer / normal / more head-scratchers? *Default:* yes, normal by default.
11. **The nine types:** keep all nine, or drop any (P8 swap testing and P7 faded labels are the most "puzzle-like")? *Default:* keep all nine.
12. **Fault-finder grades** (three, in words, with a uniform pin, only delayed): yes? *Default:* yes.
13. **Wrong calls at Tier 2 spend a consumable part** (a seal, a cartridge), while Tier 1 wrong calls only cost time? *Default:* yes.
14. **Crew favour cases and the cold-case board** (optional, for keen players)? *Default:* yes: favours from week 6, the board as Pillar 5 ends.
15. **The name:** "head-scratchers" (the crew's word), "Fault notes" (the device page), "the Chief's notes" (the hint binder)? *Default:* yes.
16. **The P9 fix moves a crew member's routine** (the laundry wash to 08:00): fine for a Tier 2 case, or keep moving routines for Tier 3 (Pillar 7)? *Default:* allowed, one small move per case.
