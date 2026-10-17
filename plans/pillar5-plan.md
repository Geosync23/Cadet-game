# Pillar 5 plan: new ways to work (expanded core mechanics)

**DRAFT 2 (2026-10-17, the Pillar 5 planner, branch `claude/pillar5-plan`).** Rewritten from the user's survey answers (`plans/pillar5-notes.md`, "The user's answers"): **Pillar 5 is expanded core mechanics only.** Ship-wide events move to Pillar 6; career progression, story and the night shift to Pillar 7 (design-doc.md, "Roadmap after Pillar 4"). The user asked for a detailed plan before any work, and for new mechanic ideas from the planner. **Nothing is built until the user approves this plan, and each mechanic gets its own short spec page the user reviews before it's built.**

Read with `design-doc.md` ("The clockwork", "The player", "Works progression", "Roadmap after Pillar 4"), `plans/pillar4-plan.md` (Part 6: the rules for sharing the one game file), `TEAM.md`, `DEV_NOTES.md` ("Machines and wear", "Chores and openJobs", "Player needs and the device", "Player interactions", "Hook register") and the handover notes for systems, player, galley and device.

A plain-language version for the user is `plans/pillar5-plan.html`.

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

Around the ladder: **more real faults reach you**; **repairs get quicker with practice** (in words); **tools arrive one at a time, each with training**; **off-shift tinkering, cabin touches and star logging**; **the device's work pages** (your training record, work log, tools). Still Works only.

**How it's built:** each mechanic is **one self-contained sub-block of a new section 24 with one owner**, on top of a small shared foundation (the unlock ladder, training moments, work-step building blocks). A **mechanic designer** writes each mechanic's one-page spec for the user ahead of the builders. Staffing is tiered and generous (the user: "don't be afraid to hire as many as needed"): up to about 13 Pillar 5 seats, joining in waves as Pillar 4 winds down. **A check-in with the user after every one or two mechanics.**

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
3. **Physical, not a mini-game.** Every verb happens in the world with your character's hands: walking, looking, carrying, holding, turning. Where a choice is needed (which part, which valve), it's a choice you make with what you've seen on the deck. No timing games, no puzzles that stand in for the work. *(Tuning, M5, is the closest to a panel; it's an open question for the user.)*
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
- **Merge order:** Pillar 5 after Pillar 4 each round: … → systems (17) → player (15) → career (24 core) → mechanics (24a…) → deck architect 2. A **Pillar 5 collector** merges the mechanic branches into one branch first, so the lead takes about four Pillar 5 branches a round, not ten.
- **Notes on the bus:** `simNote('trained', { mech })`, `simNote('found', { machine })`, `simNote('incident', { id, step })`, `simNote('promoted')`, `simNote('uniform', { state })`, so Pillar 4's lines and reputation can react without new hooks.

---

## Part 4: staffing, waves and check-ins

### The seats (tiered; up to 13)

**Tier 1, the foundation (start when the user approves):**

| # | Seat | New? | Branch | Builds | Owns |
| --- | --- | --- | --- | --- | --- |
| F1 | Mechanic designer | **new** (no code) | `claude/p5-design` | — | `plans/mechanics/<id>.html`, one page per mechanic for the user, a step ahead of the builders; keeps this plan current; answers builders' design questions |
| F2 | Systems engineer | existing role, **fresh session** (takes section 17 back from the sim engineer) | `claude/ship-systems` | 0.33.38+ | section 17; `machine_check.py` |
| F3 | Player engineer | existing | `claude/player-needs` | 0.28.23+ | section 15; `player_check.py` |
| F4 | Career engineer | **new** | `claude/works-career` | 0.44.x | section 24 core (ladder, training, tools, skill, trust, drill and inspection hooks, certification, promotion, device pages); `career_check.py`; `mech_check.py`'s frame |

**Tier 2, the mechanics (each joins when its spec page is approved; two or three at a time):**

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
| S3 | Pillar 5 collector | new | `claude/p5-mechanics` | 0.54.x | merges M-A…M-E (and S2's baked lines via the head writer) into one branch, runs every check, hands the lead one branch a round |
| S4 | Check runner | as Pillar 4 | `claude/integration-test` | — | runs the checks in parallel |

**On call:** sim (rotas, musters, the duty officer, the stuck lift, crew at team jobs, `playerBed()`), performance (poses and decals), galley (oven tuning's effect on cooking, Brennan's lines), social A (Work reputation as trust; reactions), device (only if the skin needs something), interactions (tap targets for new places), crew designer (the junior laundry rota, if it's roster data). **This planner** stays on until the mechanic designer is hired, then hands over (`plans/handover-pillar5-planner.md`).

*(Build ranges 0.51-0.54 look free in DEV_NOTES and git history; the build master confirms before the first push. The user's staffing answer was cut off ("some workers focused on keeping the…"); the collector and the check runner are the planner's guess at it, to be adjusted.)*

### The briefs (ready to paste)

**Every brief starts with this paragraph:** "You are the <seat> for Starship Cadet's Pillar 5 (new ways to work). Read CLAUDE.md, then DEV_NOTES.md, plans/pillar5-plan.md (Parts 1 and 3, your seat in Part 4, and your mechanics in Part 2), plans/pillar5-notes.md (the user's answers), the approved spec page for each mechanic you build (plans/mechanics/<id>.html), plans/pillar4-plan.md Part 6 (the rules for sharing the one game file with Pillar 4, which is building at the same time), TEAM.md, and your predecessor's handover note if your role had one. Push only to <branch>. Touch only what your seat owns; anything else goes through its owner via the lead (mechanic engineers: via the collector). Each turn: small exact-string edits (never rewrite the game file), bump the build in the HUD, add a DEV_NOTES row, run the tests (one browser check at a time; always `intro_check` when you touch jobs, the player or the clock), commit, push, and report to the lead (session_01PJtmxWgAPLebXSZKP6ZRpG) with send_message (mechanic engineers report to the collector). Hooks into other sections are one-line, typeof-guarded, and listed in DEV_NOTES' hook register. Hand over at about 70% memory with plans/handover-<role>.md. Commit messages end with the Co-Authored-By line; never put model names anywhere else."

- **F1 Mechanic designer.** For each mechanic in Part 2, in ladder order, write `plans/mechanics/<id>.html` in the style of `plans/pillar5-plan.html`: what you do step by step (with a small sketch), who teaches it and the training script outline, how it unlocks and grows, what the crew do, what changes on the deck, what it asks of each section, the phone budget, and 2-3 questions for the user. Stay one or two pages ahead of the builders; the lead shows each page to the user; nothing is built from a page the user hasn't approved. Also weigh the "more ideas" list with the user's picks.
- **F2 Systems engineer.** Section 17. First: take section 17 back from the sim engineer (session_01R6RBwwBM9aorpsqDCrztDU) and read `plans/handover-systems.md`. Then: `playerTier()` (inert); real faults for you (`CREW_LEAVE_FAULT`, the `found` delay, crew busier on bigger jobs, measured in `machine_check`); **job kinds with steps** (a job carries a mechanic id and its steps, so each mechanic's jobs post, are claimed by crew, and are done by you through section 24); then each mechanic's machine side as its spec asks: rounds' found jobs, the washers as real machines, manifests and stock counts, tuning drift, parts and readings, incidents, team jobs, the pipe graph. Never change a reserved job.
- **F3 Player engineer.** Section 15. The work-step building blocks (`look`, `choose`, `turn`, `wait`, and `hold`/`carry` as now) as data a mechanic can describe; `careerSpeed(kind)` in task minutes; your uniform (worn, grubby, changed at the locker) and its hygiene effect; tidying your berth; the off-shift activities (tinkering, cabin spots, star logging). Keep `player_check` current.
- **F4 Career engineer.** New lazy section `// 24. WORK` (after section 21) with the core: `SHIP.career` and `save.career`, `CAREER_LADDER`, `careerHas`, training moments (a `train` slot on `jobReserve`, the teacher leading then following, meeting lines, `simNote('trained')`), tools, skill in words, trust (reads Work reputation; a stand-in until it's in), the drill and inspection hooks for M-B, certification and promotion (with the sim engineer for the bed and door), the device pages (Training, Work log, Tools via `deviceApp`). `career_check.py`, and the frame of `mech_check.py` that each mechanic adds a part to. Give out hash keys from 850-899.
- **M-A … M-E Mechanic engineers.** Build your mechanics from their approved spec pages, each in its own sub-block of section 24 (`// 24a. ROUNDS` and so on), on the foundation's building blocks; ask F2/F3/F4 (via the collector) for anything the foundation lacks rather than editing their sections. Add your part to `mech_check.py`. One mechanic at a time: build it, test it, the user plays it at a check-in, then the next.
- **S1 Deck architect 2.** Read the Pillar 4 deck architect's handover and DEV_NOTES "How decks work". Places and dressing for Pillar 5's rooms in `// P5 places` blocks: the laundry (load, dryer, fold, the linen cart dock), storage count spots and the hold's crates, valves by the corridors, the extinguisher and bulkhead, your cabin 4-23 with its spots, the Deck 5 machine rooms and the spine (M9), the machine shop's order board. `deck_check` on every push; other decks pixel-identical.
- **S2 Works writer.** Follow `content/README.md`, the voice bible and the voice cards. Write the training moments, the incidents' lines, the inspection's nods and remarks, the drill, the promotion and the workshop orders; report to the head writer.
- **S3 Pillar 5 collector.** Merge the mechanic engineers' branches into `claude/p5-mechanics` in a fixed order, run every check, fix merge seams with their owners, and hand the lead one branch a round.

### Waves (tied to Pillar 4's progress)

**Wave 0: approval (now).** The user approves this plan. F1 (the designer) is hired first and writes the spec pages for M1-M3.

**Wave 1: the foundation (alongside Pillar 4's waves 2-3).** F2, F3, F4 (+F1). The ladder, training moments, work steps, `playerTier()`, real faults, skill in words, the device pages, `career_check`, `mech_check`'s frame. **Gate:** everything inert in a combined build (`cadet_test` ALL IDENTICAL, every check passes, `intro_check` included), then the real faults switched on.
- **Check-in 1:** play a work day with more real faults and quicker repairs; approve the spec pages for M1-M3.

**Wave 2: rounds, laundry, the drill and the inspection.** M-A (M1), M-B (M2, M3), S1, S2, S3. **Check-in 2:** play week 2: your first round, a laundry duty, a drill and an inspection.

**Wave 3: hauling and tuning** (after Pillar 4's wave 3). M-C (M4), M-A (M5). **Check-in 3.**

**Wave 4: incidents, the scanner, and promotion.** M-D (M6), M-E (M7), F4's certification and promotion (with the sim engineer's bed move). **Check-in 4:** a burst pipe, the scanner, and from a save near certification to your own cabin.

**Wave 5: after promotion.** M-D (M8 team jobs), M-E (M9 tracing), M-C (M10 workshop, tinkering), F3 (cabin touches, star logging). **Check-in 5:** Pillar 5 final; then a pull request to `main` with the user's OK.

At most about 9 Pillar 5 sessions at once (wave 2-3), while Pillar 4 thins out into writing.

### Test changes

- **New `career_check.py`** (F4): the ladder (never two on a day; waits for use), training moments, tools, skill words, trust, certification (pass, delay, pass), promotion, the cabin, the save, an old save, determinism twice.
- **New `mech_check.py`** (F4's frame, one part per mechanic): each mechanic's steps end to end, its stages, crew doing it when you don't, the same twice.
- **`machine_check`** (F2): jobs left for you and the fault share per shift day; job kinds with steps; parts; tuning drift; incidents' machine side; team jobs; the pipe graph.
- **`player_check`** (F3): the work steps, quicker tasks, the uniform, tidying, the off-shift activities.
- **`day_check`**: a laundry day, a Wednesday drill, a Thursday inspection, an incident day, a team-job day; draw calls under 450.
- **`deck_check`**: the new places; your cabin; the M9 rooms.
- **`intro_check`** (Pillar 4's) on every push that touches jobs, the player or the clock.

---

## Risks

- **Too much at once for a new player.** *Answer:* the ladder: one mechanic at a time, taught by a person, never two on a day, waiting for you to use the last one; everything earlier keeps working the simple way.
- **Mechanics turning into mini-games** (the design's "no mini-games standing in for the job"). *Answer:* every verb happens in the world with your hands; feedback is the machine itself; no timers or scores; tuning flagged to the user.
- **Phone draw calls (450).** Laundry baskets, crates, puddles, smoke, made things, the new rooms. *Answer:* each mechanic's props at most 2-3 draw calls (instanced, its deck only, only while in use); cabin spots at most 4; the M9 rooms measured by `deck_check`; the performance engineer on call.
- **Determinism.** Faults, drift, incidents and which part fails are chosen. *Answer:* hashed from ids and the day or hour, never `R()`; every check runs twice.
- **The one-file merge load.** Up to 13 new seats next to Pillar 4. *Answer:* one new section with a sub-block per mechanic; the collector merges mechanics first; Pillar 5 after Pillar 4 each round; mechanics two or three at a time.
- **Breaking Pillar 4's first week.** *Answer:* reserved jobs untouched; the ladder starts on Day 8; `intro_check` on every relevant push.
- **The crew still do everything.** *Answer:* each mechanic's crew side is measured in `mech_check` (they do it when you don't, but slower) so the ship never depends on you, and there's still work for you.
- **Two ideas of reliability.** *Answer:* trust reads Pillar 4's Work reputation.
- **Beds.** *Answer:* the cabin move waits for Pillar 4's wave 3; 4-23 is a spare (checked against the crew designer's reserve pool).
- **Usage limits and memory.** *Answer:* tiered hiring, the lead's hourly check-in, the 70% handover rule; each mechanic is small enough for one session.

---

## Open questions for the user (with the plan's defaults)

1. **Tuning (M5):** turning a setting and watching the machine respond: right side of "no mini-games"? *Default:* yes, with no timer or score.
2. **Your uniform:** grubby with work, changed at your locker, washed through the laundry. Should a grubby uniform look different on your character (a duller shade)? *Default:* yes, slightly.
3. **Laundry duty:** about once a week on a junior rota, with crew covering if you skip it. *Default:* yes.
4. **The ladder's pace:** about one new mechanic every 2-3 ship days after week 1, promotion at about Day 20. *Default:* yes.
5. **Which "more ideas"** (leak hunting, tool upkeep, the lift roof, irrigation, coolant rounds, the logbook, rewiring) should join the ladder? *Default:* none yet; the designer brings the user's picks as spec pages after wave 2.
6. **Your own cabin:** Spare 4-23 (no window)? *Default:* yes.
7. **Staffing:** the rest of the user's sentence ("some workers focused on keeping the…"): the collector and the check runner are the planner's guess.
