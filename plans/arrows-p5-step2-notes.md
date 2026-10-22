# Arrows for Pillar 5 Step 2: the junior days (Days 2-8)

AR2's notes for the arrow project (2026-10-22). Build played: `claude/integration` 2b4a05db (0.64.15, the published one). Analysis only: nothing in the game was changed. AR1 owns the combined page (`plans/arrows-pillar5-plan.html`); the drop-in section for it is `plans/arrows-p5-step2-section.html`.

**What this covers:** M1 Rounds (Day 2, Torres), M2 your work uniform (Day 8 in the build; Day 5 in the plan), M3 the drill and the inspection (Days 3-4), M4 hauling (Day 3, Yara Esposito), M5 tuning (Day 4, Calder with Brennan), M6 small incidents (Day 8, Calder), M7 the scanner (Day 5, Emeka Halloran, since Torres is off on Fridays), and the Day 5 head-scratcher lesson (p3) that rides on M7. Each has its training meeting.

## How I tested

I played Days 2 to 11 in Chromium (headless, a phone-sized 420 x 860 window) with a small robot player that only does what the game shows it:

- **It follows the arrow.** Wherever the goal pointer points, it goes (it jumps there instead of walking), and at the spot it taps what a player would tap: the thing the arrow names, or the floor at the marker.
- **It uses the job board** when the arrow says so: turns in a finished job, else takes the training job if one is offered, else the first job listed.
- **It answers cards** the way a careful player would (a round's marks by what the machine really looks like, a tuning dial toward steady).
- **It reads through meetings,** picking the first answer.
- **It uses the Tracked list** ten minutes before a training meeting, if the arrow isn't already pointing there (an attentive player).
- Needs are kept topped up, so need arrows don't hide what the job arrows do.

Everything else (a toast, a Mail, a tip, a speech bubble) was logged and not acted on, because that's the test: does the arrow alone carry you through? Logs: four runs (Days 2-8 plain, Days 2-10, Days 2-8 with the robot dropping a job to take a training job, Day 8 with everything before it done). The scripts are in this session's scratch folder; they aren't part of the repo.

## The goal pointer today, in short

- **One arrow at a time.** `IX_GOAL` (any section's `setGoal`) wins; with none, and while job tracking is on (`SHIP.player.track` not null), the arrow shows your job's next step (`ixJobStep`), or, with no job on a shift day, "Clock in at the time clock" then "Take a job at the job board" (`ixWorkStep`).
- **What it can point at:** a deck (via "Take the lift to Deck N: ..."), then a place, a thing on the deck (an item by name, like the job board or a shelf), a room's middle, a spot on the floor, or a crew member standing on your deck (`g.crew`).
- **What it can't point at:** anything inside the device (an app, a card, a button on a card), a row on the job board (only the board itself), a person on another deck, a side job's stops (the drill), or "nowhere, it's done". It also can't say *why* (only a short label) and it hides while a progress bar is up.
- **Who sets it, and who loses.** About thirty places in the code call `setGoal`; each simply replaces the last. There is no queue and no "most important first". A training ask only sets its arrow if no job is tracked, which mid-shift is almost never, so the career's most important moments are the ones most likely to get no arrow.

---

## BROKEN (fix first)

Each with what I did and what went wrong. Numbers are for reference in the plan page.

**B1. The drill can't be done (M3, Wednesday 15:00).**
- Steps: Day 3 (or any Wednesday as a junior) at 14:50: Calder's toast "Drill in ten minutes. Muster at the Works bay. Take the extinguisher. Stand by the hatch." and the arrow "Fire drill, 15:00" to the Works bay. Go there, tap the fire extinguisher on its bracket.
- What happens: the extinguisher shows its description ("It comes off the bracket for the fire drill"). Nothing starts. Tapping the floor at the bracket does nothing either, with or without a board job in hand. At 15:15 "All clear. Drill over." and Calder says "Four and a half minutes. We'll talk about it." whatever you did.
- Why: the drill is a "side job" (yours beside your board job). The tap code (`ixChore`, `jobHere`) and the arrow (`ixJobStep`) only ever look at your main job (`myJob()`, which leaves side jobs out). `mySideJobs()` exists but nothing uses it. mech_check passes because it marks the steps done directly, not by tapping.
- Knock-on: the drill row is never "used", so it never trains, never gives its reputation, and Calder's Friday-tea word never comes. The arrow "Fire drill, 15:00" is also still up after the all-clear (it isn't cleared at 15:15).

**B2. Yara's hauling lesson only works on a Wednesday with crates still in the hold (M4), and when it misses it blocks the whole junior week.**
- Steps: let Rounds slip one day (for example, still holding a job when Torres's talk ends on Day 2; see M1). Rounds trains on Day 3, so hauling's ask comes on Day 4 (Thursday): "Shelves done? Meet me at the hold. There's a manifest with your name on it." Go to the meeting.
- What happens: Yara's talk plays in full ("The manifest. Three crates today. Linen, medical, store stock...") and then nothing. The lesson is quietly marked "try again". It retries each workday at 06:00, before the 10:00 delivery, so even the next Wednesday it finds no crates. In my run nothing new opened from Day 4 to Day 10 (tuning, the scanner and incidents all wait for hauling to be used once). Yara's "Let's try that again. Follow me, and watch." came on Day 11 at 06:00.
- Why: `WORK_MECH.m4.reserve` needs crates on the manifest (`haulCrates()`); off a delivery day, or once the crew's run has taken them, there are none. The retry runs at the morning ask time, before the delivery.

**B3. The scanner never counts as used if you follow the arrow (M7), so Making it safe (M6) and the Tier 2 test never open.**
- Steps: be trained on the scanner (Day 5). Take any repair job with a fault. Follow the arrow.
- What happens: the arrow says "Fetch a lamp: the Lights shelf" straight away (the job already names its part), then "Repair the stage lights". You never look the machine over, so the scanner never reads. Making it safe needs the scanner used once; it never opens (Day 8 and Day 9 passed with nothing). The Tier 2 test job needs Making it safe, so promotion never comes.
- Only if you go to the machine first, against the arrow, and tap it does the scanner panel open (in my run: "lamp 13, relay 80": pick lamp). Even then the arrow had already named the part, so the scanner adds nothing.
- Why: the scanner is used only by the look-over before parts (`jobBegin`, then `scanOpen`); `worksUse('m7')` is only called when a scanned pick is fitted (`scanFitted`). The arrow and the "Job taken" toast both say "parts first".

**B4. The teacher's own job is on the board marked for you, and taking it skips the lesson (M5, M7, likely M4).**
- Steps: Day 5, after Emeka's 09:00 meeting, go to the board. It lists "Repair: Washer 4 (leaks)" marked for you (it's Emeka's demonstration job, the "watch" step).
- What happens: taking it counts as your turn. You fetch a valve and repair it the old way (no scanner yet: the scanner is only handed over at your turn), and at turn-in "Trained: the scanner, with Emeka Halloran. Torres's old scanner is yours now." You never read the scanner in the lesson. The Washer 2 head-scratcher that should follow (the scanner reading on Washer 2, then the case) then appears on the board and finishes as a plain 24-minute repair: no case is called. Its clue toasts read "+ clue: Eklund | undefined" and "+ clue: Teague | undefined". Emeka's p3 talk ("Open Fault notes. Three suspects...") plays after the job is already done.
- On Day 4 the same happened with tuning (I took Calder's Oven 1 and tuned it myself), which is harmless there.
- Why: the "watch" job is reserved for you (`heldForYou`), so it's on your board, and `trainTick` treats taking it as starting your turn.

**B5. The incident lesson points to the wrong deck and lapses (M6, Day 8).**
- Steps: Day 8 with everything before it done. Tracked lists "Training: making it safe [10:30]"; its arrow goes to the Works Chief's office, Deck 5. Be there at 10:30.
- What happens: Calder's meeting plays ("Burst pipe. Junior wing. With me... Go.") and the arrow changes to "Meet Ines", still pointing at her office on Deck 5. The burst is on Deck 4. The "watch" step only counts while you're near the pipe on Deck 4, and nothing points there. At 17:00 the lesson lapses; next workday 06:00: "Let's try that again. Follow me, and watch."
- Why: the call's arrow uses the occasion's room (Calder's office), not the burst; the teacher's walk (lead mode) can't be followed across the lift.

**B6. Wrong words in the training Mails.**
- Tuning (Day 4): "Galley, 10:15. Bring nothing. (08:40, Galley on Deck 3.)": two different times. The meeting is at 08:40, which is also before the 09:00 shift starts.
- Rounds (Day 2), when you miss the 10:45 meeting: the notes Mail says "Your first round is on the board." It isn't; the lesson is offered again the next workday.
- Hauling (Day 3/4): "Meet me at the hold", but the meeting and its arrow are in Main storage.

**B7. The inspection is never taught or announced (M3, Thursday 06:30).**
- Steps: Day 4. Wake at 06:00 as usual.
- What happens: nothing before it. No Tomas scene (the plan's "Tomas shows you how to get ready"), no Mail the evening before, no arrow to your bunk, no word about the three things checked. If you tap your bunk on Thursday morning it does offer "Make the bed" and "Tidy your locker" with "The inspection is at 06:30", but nothing sends you there. At 06:59 a Mail from Calder: "Two of the three weren't right this morning. Uniform, bed, locker: all three next week." The Calendar line says "Bunk inspection: tidy your bunk" at **06:40**; the walk is 06:30.
- I'd call this half BROKEN and half HIDDEN: it works, but the first time you meet it you're already marked down for something you were never told.

### Found on the way (outside M1-M7: for `plans/backlog.md`, not fixed here)

- **"Service: Main lift" can be taken but never worked.** The main lift (`5-mainlift-1`) has no panel spot, so the arrow "Repair the main lift" leads to the lift and no tap starts the work. You're stuck holding it until you drop it. It came up on Day 2's board in every run.
- **A fresh game with no save starts with job arrows off.** `SHIP.player.track` is read from the save as `SAVED && SAVED.player && SAVED.player.track`, which is `null` when there's no save, and null means "tracking off". So no "Clock in" or "Take a job" arrow until you take your first job at the board. The arrival day's own arrows hide it; "Skip to Monday" shows it.
- **Dropping a job leaves its part in your hands,** and the next cart job then refuses ("Your hands are full (a relay). Put them back in main storage first.") while the arrow points at the Cart bay. Nothing points to main storage.
- **A need arrow says "A shower, Deck 2" while its toast says "Junior wing, Deck 4",** and the Deck 2 spot has nothing to tap (the robot stood there an hour).
- **Tracked, when two things start at the same time,** can track the wrong one (on Day 5, "On shift 09:00" instead of "Training: the scanner 09:00"), and a training appointment's arrow label is only the room ("Works bay, Deck 5"), not who or what.

---

## The mechanics, one by one

Status words: **WORKS**, **WORKS BUT HIDDEN** (it works, but you'd only find it by luck or by reading every Mail), **BROKEN**, **NOT BUILT**.

### M1. Rounds (Day 2, Zeke Torres): WORKS BUT HIDDEN

**A. Inventory**
- **What:** walk 4-6 machines on one deck, look at each, mark Fine / Worn / Something's off. A worn one you mark becomes a cheap service job "found by you".
- **Unlocks:** Day 2, a workday, after Day 1's shadow shift. Big row. Ask between 06:00 and 10:30 (in play: 09:00).
- **Taught:** Torres, at the tea corner in the Works bay, Deck 5, at 10:35-10:55 (10:45 in play). He explains; then your first round (Deck 4, a washer first) is on the board for you; the arrow and green tips lead you through it (self-led since 0.45.9: Torres doesn't walk with you).
- **Steps:** (1) the ask: toast and Mail "Fancy a walk? I'll show you my round. Tea corner, or the bay till half eleven. (10:45, Works bay on Deck 5.)"; (2) the meeting (lines, one question, "Your first round's on the board. Take it, and your device will show you the way."); (3) take "Your first round, Deck 4" at the board; (4) for each machine: walk there, tap it, stand while you look (a few seconds), mark it on the card; (5) turn it in at the board: "Trained: rounds, with Zeke Torres. Round clipboard is yours now." After that a "Morning round" is on the board at 07:00 each workday, held for you until 11:00. Stage 2 (after 5 rounds): you pick the machines yourself (a card: "Pick a handful to look at today: four to six"): seen on Day 8.
- **How the game tells you today:** a toast (about 5 seconds) and a Mail at the ask; **no arrow** if you have a job tracked (you nearly always do at 09:00). The meeting is in Tracked ("Training: rounds 10:45"), but tracking it gives only "Works bay, Deck 5". After the talk, the best guidance in the game: the arrow and a green tip at every step ("Your first round is on the job board. Take it, and follow the arrow." / "Walk to Washer 1. Follow the arrow." / "Look at Washer 1. Listen to it. Then mark what you see." / "Mark it: fine, worn, or something's off. Trust your eyes." / "Next one." / "Round done. Turn it in at the job board."), and Torres's bubbles ("Your turn. Stand still a sec. Listen first.").
- **Does it work?** Yes, end to end, when you're at the meeting with free hands. Problems: no arrow at the ask (B-level for the arrow project); if you're still holding a job when the talk ends, the arrow says "Take your first round at the job board" but the board won't give it (it says "You have a job. Finish it or drop it to take another.", which the arrow doesn't); at 17:00 the lesson lapses and comes back the next morning at 06:00 (before your shift), which moves everything after it by a day (and see B2). Missing the meeting gives the wrong notes Mail (B6).

**B. Arrows**

| Moment | Arrow points at | Appears | Goes | Line |
| --- | --- | --- | --- | --- |
| The ask (09:00) | Torres, wherever he is; else the tea corner | at once if you're between jobs; else as soon as your job's turned in, or 10 minutes before the meeting, whichever is first (your job's arrow comes back after) | when you reach him or the meeting starts | "Torres: rounds, 10:45" |
| Meeting soon (10:35) | the tea corner, Works bay | 10 minutes before | when the talk starts | "Rounds with Zeke, 10:45" |
| After the talk, hands full | your job's next step, with "first" | at once | when the job's turned in or dropped | "Finish your job first: then your first round" |
| Take the round | the job board, and the round's row on the board | when your hands are free | when it's taken | "Take your first round" (today's, good) |
| Each machine | the machine's panel (today's) | each stop | when you mark it | "Look at Washer 1" (today's, good) |
| The mark | the card (inside the device: today's pointer can't) | when the look ends | when you mark | the tip does it today |
| Turn in | the job board (today's) | when done | when turned in | "Turn it in at the job board" |
| Next morning | the board, on the "Morning round" row | 07:00 on workdays until 11:00, once clocked in | taken, or 11:00 | "Your morning round is on the board" |

Tracked chain (today, when tracked): take, Washer 1, Light relays 1, Washer 4, Light relays 2, the board. It's the model for the others.

### M2. Your work uniform (Day 8 in the build): WORKS BUT HIDDEN

**A. Inventory**
- **What:** oily jobs (ovens, ranges, the galley plant, pumps, the lift and more) make your uniform grubby: a duller tint on your character. A shower doesn't clean it; a change at your wardrobe does. Grubby drains hygiene and the Thursday inspection notices.
- **Unlocks:** the first oily job you turn in from Day 8 (the plan said Day 5). Small row: no meeting by Mail.
- **Taught:** Torres's two lines in the meeting panel wherever you are, at the moment it opens ("You've got half a machine on you. Change before tea. Calder notices." / "Shower won't shift it. Wardrobe will."), then "Trained: your work uniform, with Zeke Torres." and a notes Mail.
- **Steps:** none to start; to clear it, go to your wardrobe in Bunk 1 (Deck 4) and change.
- **How the game tells you today:** the panel lines and the toast. No arrow to the wardrobe; nothing on screen says you're grubby except the tint (hard to see on a phone).
- **Does it work?** Yes (mech_check's part passes; in play the lines and the toast came on Day 8). Stage 2 (servicing the washers): NOT BUILT (the lead kept stages out of Steps 1-2).

**B. Arrows**

| Moment | Arrow points at | Appears | Goes | Line |
| --- | --- | --- | --- | --- |
| Torres's word | your wardrobe, Bunk 1 | after his lines, if you're off shift or between jobs (never over a job step) | when you change, or at bedtime | "Change at your wardrobe" |
| Grubby again later | your wardrobe | once a day, when you turn in an oily job and you're grubby, between jobs | when you change | "Grubby uniform: your wardrobe" |
| Wednesday evening before an inspection, grubby | your wardrobe | 20:00 Wednesday | when you change | "Clean uniform for the inspection" |

### M3a. The drill (Wednesdays 15:00, Calder): BROKEN (B1)

**A. Inventory**
- **What:** a fire drill (Day 3), then pressure, then power, by week. Fire: take the extinguisher off its bracket, stand by the hatch 10 minutes, put it back. Pressure: turn the bulkhead wheel four steps, stand by the door. Power: the breaker cabinet, then stand.
- **Unlocks:** Day 3, a Wednesday you're on shift as a junior. Small row: trained by the first drill you turn up to.
- **Taught:** Calder's toast at 14:50 ("Drill in ten minutes. Muster at the Works bay. Take the extinguisher. Stand by the hatch."), then her word on your time at 15:15.
- **Steps (as designed):** go to the Works bay; take the extinguisher (bracket by the west door); stand by the hatch to the utility closet; put it back. Over at 15:15 whatever you did.
- **How the game tells you today:** the toast and an arrow "Fire drill, 15:00" to the Works bay (the room's middle). The Calendar says "Drill at 15:00: Fire drill. Muster at the Works bay".
- **Does it work?** No: no tap starts any step (B1). The arrow never moves past the room and outlives the all-clear.

**B. Arrows**

| Moment | Arrow points at | Appears | Goes | Line |
| --- | --- | --- | --- | --- |
| 14:50 | the extinguisher bracket (`5-drill-ext`) (fire); the bulkhead wheel (`5-drill-door`) (pressure); the breaker cabinet (`5-drill-breaker`) (power). It takes over from your job's arrow; your job comes back after | 14:50 | when you take it / turn it | "Fire drill: take the extinguisher" |
| Extinguisher in hand | the hatch (`5-drill-hatch`) | after the take | when you're there | "Stand by the hatch" |
| Standing | none (a progress bar: "Standing by: 10 min") | | | |
| Put back | the bracket | after the stand | put back | "Back on its bracket" |
| 15:15 | your job's next step again | the all-clear | | Calder's time word as now |

Needs: the tap and arrow code to read side jobs (B1). A muster spot arrow (`5-muster-1..6`) is a nice extra for the officer years, not needed now.

### M3b. The inspection (Thursdays 06:30, Tomas and the duty officer): WORKS BUT HIDDEN (B7)

**A. Inventory**
- **What:** three things checked: a clean uniform (changed today and not grubby), your bed made (this morning), your locker tidy. A nod or a gentle remark; +1 reputation each time you turn up.
- **Unlocks:** Day 4 (Thursday). Small row: the first inspection is the training.
- **Taught:** designed as Tomas showing you on Day 4; in the build nobody does.
- **Steps:** before 06:30 on Thursday: change at your wardrobe; tap your bunk: "Make the bed" (a minute), "Tidy your locker" if you bought things; be in your bunk room 06:30-06:59 for the duty officer (Calder the first time). Not there: a Mail at 07:00 (it still counts if all three were right).
- **How the game tells you today:** the bunk's own card on Thursday morning ("The inspection is at 06:30."), the Calendar line at 06:40, and the result Mail. Nothing points anywhere.
- **Does it work?** The check itself works (mech_check passes; my run got the "Two of the three" Mail). The teaching doesn't exist.

**B. Arrows**

| Moment | Arrow points at | Appears | Goes | Line |
| --- | --- | --- | --- | --- |
| Wednesday evening (first time: Tomas in Bunk 1) | Tomas | 20:30 Wednesday, if you're on Deck 4 | when you talk to him | "Tomas: inspection tomorrow" (his scene: the three things) |
| Thursday 06:00, uniform not changed | your wardrobe | on waking | changed | "Inspection 06:30: change into a clean uniform" |
| Then, bed not made | your bunk | after the change | bed made | "Make your bed" |
| Then, locker untidy | your bunk (its card has "Tidy your locker") | after the bed | tidy | "Tidy your locker" |
| 06:25 | your bunk room (stand by your bunk) | | when the officer arrives | "Stand by your bunk: inspection" |
| After | nothing; the word or nod is enough | | | |

Today's pointer can reach every place here; what's missing is the trigger and the order.

### M4. Hauling (Day 3, Yara Esposito): WORKS on a Wednesday; BROKEN on any other day (B2)

**A. Inventory**
- **What:** a manifest run: take a hover cart, load each crate in the cargo hold (a tap each), take the lift, drop each crate where it goes (linen to the laundry on Deck 4, medical supplies to the infirmary and store stock to the crew store on Deck 3), the cart back to its dock.
- **Unlocks:** Day 3 (Wednesday), after Rounds has been used once. Big row.
- **Taught:** Yara, in Main storage on Deck 5, after the 10:00 delivery is unloaded (11:00-12:00). The ask at 06:00 by toast and Mail: "Shelves done? Meet me at the hold. There's a manifest with your name on it. (12:00, Main storage on Deck 5.)"
- **Steps:** (1) the ask; (2) the meeting (one question: "Why not? / In which order? / (Pick up the manifest)"); (3) watch: Yara takes the cart and loads the first crate (you're counted as watching while you're near the hold); (4) your run is on the board: "Manifest run: 3 crates" (held for you); (5) take it: cart (2 min), 3 loads, 3 drops on Decks 4 and 3, cart back; (6) turn it in: "Trained: hauling and stores, with Yara Esposito." Later Wednesdays: the run is held for you to 16:00 after the unload. Stage 2 (choose the order) from Day 10 after 2 runs; stage 3 (the stocktake) as an officer.
- **How the game tells you today:** toast and Mail at 06:00; no arrow while a job is tracked; the meeting is in Tracked ("Main storage, Deck 5"). After that, the job's own arrows, but **every arrow's label is just "Manifest run: 3 crates"**, never "Take a cart", "Load the linen", "Linen to the laundry, Deck 4" or "Cart back to its dock". The step's words only come after each stop ("Medical supplies on the cart. Done here. 5 stops to go: follow the marker.").
- **Does it work?** On Day 3 in my run with free hands: yes, end to end (11:50 to 13:09). Off a Wednesday: no (B2).

**B. Arrows**

| Moment | Arrow points at | Appears | Goes | Line |
| --- | --- | --- | --- | --- |
| The ask | Yara (or Main storage) | 06:00, or when you're between jobs | at the meeting | "Yara: hauling, 12:00" |
| Watch | Yara, following her (she's on Deck 5 the whole time) | after the talk | when your run is posted | "Watch Yara load the cart" |
| Take your run | the board's "Manifest run" row | when posted | taken | "Your manifest run is on the board" |
| The cart | the free cart dock | taken | cart in hand | "Take a hover cart" |
| Each load | the hold's crate stack | | loaded | "Load the linen (1 of 3)" |
| Each drop | the drop spot (`4-laundry-drop`, `3-infirmary-drop`, `3-store-drop`) | | dropped | "Linen to the laundry, Deck 4" |
| The cart back | the dock | | docked | "Cart back to its dock" |
| Turn in | the board | | | today's |

Today's pointer reaches every one of these; only the labels are missing (the stop's own `opts.text` is right there to use).

### M5. Tuning (Day 4, Calder with Chef Brennan): WORKS BUT HIDDEN

**A. Inventory**
- **What:** a machine that has drifted (an oven running hot, lights flickering, a cart dock charging slow). At its panel you press − or + a step at a time and watch the machine change; at steady it's done.
- **Unlocks:** Day 4 (Thursday), after hauling has been used once. Big row. Opening it drifts both galley ovens two steps hot.
- **Taught:** Calder (Torres is off on Thursdays), in the galley on Deck 3, with Brennan watching. Ask at 06:00: "Galley, 10:15. Bring nothing. (08:40, Galley on Deck 3.)" (B6). Meeting at 08:40 (before the 09:00 shift).
- **Steps:** (1) the meeting: Brennan "Forty rolls, love. Burnt edges." / Calder "Nothing's broken. It's drifted... Watch the glow, not the dial... Oven 2 is doing the same. Your turn."; (2) watch: "Follow me. Watch this one." (toast) as Calder tunes Oven 1 (you need to be near it for 10 minutes); (3) your turn: "Tune: Oven 2" held for you; (4) at the panel the card: "Oven 2 · A step at a time; watch the machine. · − / +", then "Oven 2: a little hot." ... "steady"; (5) turn in: "Trained: tuning", Brennan: "Here. Have a biscuit, you've earned it."
- **How the game tells you today:** toast and Mail (with two times); no arrow at the ask while a job is tracked; no arrow during the watch (Calder walks; you have to follow her); after that the job's arrows, labelled "Repair the oven" (not "Tune").
- **Does it work?** Yes. In my run I took Calder's Oven 1 from the board during the watch and was trained on it (B4), which is harmless here. The dial card says which way the machine is ("running hot") but not which button cools it.

**B. Arrows**

| Moment | Arrow points at | Appears | Goes | Line |
| --- | --- | --- | --- | --- |
| The ask | Calder; else the galley | when you're between jobs, or over a tracked job with "after this" | at the meeting | "Calder in the galley, 08:40: tuning" |
| Watch | Calder at Oven 1 (on your deck: `g.crew`) | after the talk | after the 10 minutes | "Watch Calder tune Oven 1" |
| Your turn | the board row "Tune: Oven 2" (or straight to the oven, held for you) | after the watch | taken | "Your turn: Oven 2" |
| At the oven | Oven 2's panel | | the card opens | "Tune Oven 2" |
| The dial | the card (inside the device: needs a highlight on − or +) | | steady | "Running hot: press − and watch the glow" |
| Turn in | the board | | | today's |

### M6. Small incidents: Making it safe (Day 8, Calder): BROKEN (B5, and gated by B3)

**A. Inventory**
- **What:** about once a week an incident on one deck: a burst pipe (shut the right valve upstream, mop two puddles, then fit a seal at the burst), a stuck lift (turn the brake release, check the car), or the galley alarm (reset the panel, open the vents and wait, look at the hood). Never at night, never on event days.
- **Unlocks:** Day 8 (Monday), after the scanner has been used once (B3: in practice, never). Big row; an urgent call, no Mail.
- **Taught:** Calder. The occasion is booked for 10:30 in her office (Deck 5); at 10:30 a burst starts on Deck 4 and she calls you.
- **Steps:** (1) the call and her lines ("Burst pipe. Junior wing. With me. / Three steps. Safe. Clean. Fix. Never in another order. / Safe means shut it off upstream. Follow the pipe back from the wet... Go."); (2) watch: her walk to the valve panel on Deck 4 (a minute there); (3) yours: at the valve panel a card "Which valve? The pipe runs from valve 1 to valve 3, then on down the corridor to the wet. Close one." (Valve 3 is right; a wrong one: "Still running. That one shuts the whole wing. Follow the pipe: the closest one upstream of the wet."); mop the two wet spots (3 minutes each); (4) the fix: a seal from stores, fitted at the burst; (5) turn it in: trained.
- **How the game tells you today:** "Training: making it safe [10:30]" in Tracked (its arrow: the Chief's office). At 10:30 the arrow "Meet Ines", which stays on her office on Deck 5. Nothing points to Deck 4.
- **Does it work?** In play: no. It never opened for the arrow-following player (B3); with the scanner use given by hand, it opened, the talk played, and the lesson lapsed at 17:00 because the watch step needs you on Deck 4 and nothing sends you there (B5). mech_check's on-paper steps pass.

**B. Arrows**

| Moment | Arrow points at | Appears | Goes | Line |
| --- | --- | --- | --- | --- |
| The call (10:30) | the valve panel on the burst's deck (`4-valve-panel`); Calder there. It takes over from everything (urgent) | 10:30 | when you arrive | "Burst pipe, Deck 4: meet Calder at the valves" |
| Watch | Calder at the panel (`g.crew`) | when you're on Deck 4 | after her minute | "Watch Calder" |
| Make it safe | the valve panel; then the card (inside the device: needs the card to show the pipe, valve 1 to 3, and the wet) | | the right valve | "Close the valve upstream of the wet" |
| Clean | wet spot 1, then 2 (`4-wet-1`, `4-wet-2`) | after the valve | mopped | "Mop up (1 of 2)" |
| Fix: parts | the Plumbing shelf | after the mop | seal in hand | "Fetch a seal: the Plumbing shelf" |
| Fix: fit | the burst (`4-wet-1`'s joint) | | fitted | "Fit the seal at the burst" |
| Turn in | the board | | | today's |

Lift and galley alarm: the same pattern (the brake wheel `5-lift-brake`, then "Check the car" at `4-lift-1`; the alarm panel, then "Open the vents" at `3-vent-1` with "Wait: air clearing, ready at 14:05", then "Look at the hood").

### M7. The scanner (Day 5, Emeka Halloran) and the first head-scratcher (p3): BROKEN (B3, B4)

**A. Inventory**
- **What:** at a faulty machine, looking it over with the scanner shows its 3-5 parts with a bar and a word each (good, worn, low, failing). You pick the part to fetch. A wrong pick costs a walk back, never a fail. p3, the same morning: your first head-scratcher (Washer 2 leaks: crew notes say what's been tried; cross off what didn't work).
- **Unlocks:** Day 5 (Friday), after tuning has been used once. Big row. p3 is the small row after it.
- **Taught:** Emeka (Torres is off on Fridays). Ask at 06:00: "Board, when you're in. Torres left you something. (09:00, Works bay on Deck 5.)" Meeting 09:00. Then Emeka's demonstration job (in play: Washer 4, leaks), then your reading on Washer 2, which is p3's case: Emeka stays with you until you call it.
- **Steps (as designed):** meeting; watch Emeka at Washer 4; take Washer 2 (the scanner handed over at the board); look it over: the scanner panel opens in the device (bars; "Fetch: seal / valve / pump"); the case (Fault notes app: suspects and the crew's notes; cross off; call it); fetch and fit; turn in.
- **How the game tells you today:** toast and Mail; Tracked; toasts "Here's a funny one. Head-scratcher: Washer 2 leaks. Open Fault notes: the first note's taped to the job." and a device notice. The scanner panel and Fault notes are in the device, where the arrow can't go. The arrow says "Fetch a valve" before any look-over.
- **Does it work?** Not as a lesson (B4), and the scanner's use doesn't count for an arrow-follower (B3). The scanner panel itself works when you go to the machine first.

**B. Arrows**

| Moment | Arrow points at | Appears | Goes | Line |
| --- | --- | --- | --- | --- |
| The ask | Emeka, or the Works bay | when you're between jobs | at the meeting | "Emeka, 09:00: the scanner" |
| Watch | Emeka at Washer 4 (`g.crew`, Deck 4) | after the talk | after the watch | "Watch Emeka read Washer 4" |
| Your turn | the board's Washer 2 row | after the watch | taken | "Your turn: Washer 2" |
| Look it over | **Washer 2's panel, before any parts** (whenever you have the scanner and the job has a fault cause) | taken | the scanner panel opens | "Look it over with the scanner" |
| Read | inside the device: highlight the bars, then the Fetch buttons | the panel | a pick | "Pick the part that reads lowest... or check the notes" |
| The case (p3) | the Fault notes app (device button glow + a pointer inside the app to the suspects) | when the case opens | called | "Cross off what's been tried" |
| Fetch | the shelf for the picked part | picked | in hand | today's "Fetch a seal: the Plumbing shelf" |
| Fit | the panel | | fitted | "Fit the seal" |
| Turn in | the board | | | today's |

The rule this needs (for every scanner job, not only the lesson): when you have the scanner and the job has a fault cause, the job's first arrow is "Look it over" at the machine, and the part isn't named until you've read it.

### Training meetings, all of them

| Mechanic | Day, time (in play) | Who | Where | Ask by | Arrow today |
| --- | --- | --- | --- | --- | --- |
| M1 Rounds | Day 2, 10:45 | Torres | tea corner, Works bay, Deck 5 | toast + Mail at 09:00 | none while a job is tracked; Tracked gives "Works bay, Deck 5" |
| M4 Hauling | Day 3, 12:00 | Yara | Main storage, Deck 5 | toast + Mail at 06:00 | same |
| M5 Tuning | Day 4, 08:40 | Calder, Brennan | galley, Deck 3 | toast + Mail at 06:00 (two times) | same |
| M7 Scanner | Day 5, 09:00 | Emeka | Works bay, Deck 5 | toast + Mail at 06:00 | same |
| p3 Head-scratcher | Day 5, after M7 | Emeka | at the job | toast + device notice | none (device) |
| M6 Incidents | Day 8, 10:30 | Calder | Chief's office, then Deck 4 | none (urgent call) | "Meet Ines" on the wrong deck |
| M2 Uniform | first oily job from Day 8 | Torres | wherever you are | the meeting panel itself | none needed; wardrobe after |
| M3 Drill | Wednesday 14:50 | Calder | Works bay | toast | room only |
| M3 Inspection | Thursday 06:30 | the duty officer (Calder first) | your bunk room | nothing | none |

A meeting is "met" by walking into its room at any time in its window (about 30 minutes from its start); walking out of the room ends the talk early. Missed, its notes come by Mail and the lesson is offered again the next workday. If you're mid-job, you leave it half done; nothing says the job will wait for you (it does).

---

## What today's pointer needs (the shared parts)

These are the changes the arrows above rely on, roughly in order of how much they unblock. They're for the arrow plan to decide; none is built.

1. **Side jobs in the job arrow and the taps** (the drill): `ixJobStep`, `ixChore` and `jobHere` should look at a side job that's due before your main job (B1).
2. **A priority order for arrows, instead of "the last one set wins":** urgent (an incident call, the drill) > a training step > your tracked job's step > a meeting soon > needs > tea and suggestions. And a "comes back after" rule: when a higher one ends, the one it covered returns (Tracked's `back` already does this for one case). This is what stops "arrows like crazy": fewer arrows shown, each one at the right time.
3. **Training asks always get their arrow, at a good time:** not mid-step, but as soon as you're between jobs or 10 minutes before the meeting, whichever is first, even when a job is tracked; and the label names the person, the thing and the time ("Rounds with Zeke, 10:45").
4. **Following a person:** the arrow can already point at someone on your deck (`g.crew`, used by tap-to-join). For the "watch" steps it should follow the teacher, including "Take the lift to Deck 4: Calder" when they're on another deck.
5. **The teacher's job off your board** while it's theirs (B4), and the watch step needs to say "Watch" with the teacher's arrow, not a job to take.
6. **Inside the device:** a pointer (or a glow) on the button to press: the right mark on a round card, − or + on a tuning card, the valve card's choices, the scanner's bars and Fetch buttons, the Fault notes app. Today's arrow is a world arrow only; the device needs its own small highlight, and the device button should glow when the next step is inside it.
7. **The job board row:** when the arrow says "Take your first round", highlight that row on the board (it's a list today).
8. **Step labels from the stop's own words:** a manifest run's stops, the drill's, an incident's, a tune ("Tune Oven 2", not "Repair the oven"). Most stops already carry the words (`opts.text`, `opts.label`).
9. **Clearing:** a timed arrow ("Fire drill, 15:00", "Meet Ines") goes when its moment is over.
10. **Retry rules that don't strand the lesson:** a training that can't make its job (hauling off a Wednesday) should wait for the day it can, and say so ("Next Wednesday's delivery, then"), instead of failing silently each morning (B2).

## Open questions for the user

1. **The order of arrows.** Is this the right priority: emergencies, then training, then your job, then meetings, then needs, then tea? (Needed for item 2.)
2. **Training over a job in hand.** When a training meeting comes up while you're mid-job, should the arrow take you to the meeting (your job waits), or wait until you've finished the job (and risk missing the meeting)?
3. **The scanner.** Should the arrow always send you to look a machine over first once you have the scanner (so the part is never named until you've read it)? That makes the scanner matter and fixes B3, but every job gets one more stop.
4. **The inspection.** Should Tomas teach it on Wednesday evening (the plan), or is a Mail the evening before and an arrow at 06:00 enough?
5. **Inside the device.** A pointer inside cards and apps (a glowing outline on the button to press), or only words ("Tap − to cool it")?
