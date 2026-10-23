# Arrows for Pillar 5: raw notes (AR1, 2026-10-22)

Build under test: claude/integration 2b4a05db (0.64.15, starship-cadet.html). Nothing in the game was changed.
The plan page is plans/arrows-pillar5-plan.html (Steps 1-2). These are the raw notes behind it: AR1's own play of the
tracked shift (Step 1), how the arrow system works today, then the four helpers' notes as written (group A: the junior
first week; group B: the burst pipe, the career screens, the road to Officer; group C: head-scratchers and tracing;
group D: side jobs). Groups C and D (Steps 3+) were cut short when the lead narrowed the scope to Steps 1-2; they are
kept for later. Play tools: plans/arrows-tools/.

Verdicts: WORKS / WORKS BUT HIDDEN / BROKEN / NOT BUILT. Line numbers are starship-cadet.html at 2b4a05db.

## Step 1: the tracked shift, played end to end (AR1)

How: shift.py (in AR1's scratchpad; copied to plans/arrows-tools/ in this commit). Dev mode sets the career, then the
game runs in real time; the "player" goes wherever the arrow points (a teleport stands in for the walk) and taps the
thing the arrow points at, presses the clock screen's and the board's own buttons, reads dialogues through. Tracking
is set back to "a job was taken yesterday" (SHIP.player.track = a stale id), as in a real game. Logs: shift2.txt
(Day 2, 07:30-18:30, "On shift" tracked), shift9.txt (Day 9 afternoon).

What the player is told, Day 2 (shift2.txt):
- 07:30 Tracked panel: Breakfast (Now), On shift 09:00, Tea and biscuits 13:00, Dinner, the evening traditions,
  tomorrow's, then Places (the job board, your bunk, the call booths). No "Clock in" row yet (it only appears once
  you are late: clockTrkItem, clockRmEasy).
- 07:30 tap "On shift": arrow "The Works bay, Deck 5" (devItemGoal, the room's middle). On Deck 5 it pins a
  workbench in the middle of the bay. Tapping there does nothing.
- 08:00 tip "Clock in by the tea corner at shift start, out at the end." The clock is open, but the arrow stays on the
  bay's middle (IX_GOAL wins over ixWorkStep's "Clock in").
- 08:40 toast "Time clock: Your shift starts at 09:00. Clock in at the time clock in the Works bay, by the tea corner."
- 09:00 the tracked shift clears itself (trkDoneCheck: started with you in the room) and the arrow becomes "Clock in
  at the time clock" (5-timeclock-1). Tap: the clock screen, "Clock in". On time, just.
- 09:01 "Take a job at the job board" -> board -> Take it -> "Job taken: Food to the cold store... Follow the marker."
  + tip "Track it on your device; the marker shows the way."
- Then every step has its arrow and a clear label: "Take a hover cart from the Cart bay" -> "Load the cart in the
  cargo hold" -> "Unload at the cold store" (Deck 3; off deck: "Take the lift to Deck 3: ...") -> "Dock the cart in
  the Cart bay" -> "Turn it in at the job board" -> next job: "Fetch a relay: the Lights shelf" -> "Repair the light
  relays" (Deck 1) -> turn in -> "Fetch a cartridge: the Filters shelf" -> "Repair the pool filter" (rec deck) -> ...
  Four jobs done 09:01-10:47 by following the arrow alone. WORKS.
- 10:00 Torres's Rounds ask (Mail + toast, 11:20 in the Works bay): no arrow (the tracked job, C1). The player, busy on
  jobs, never goes; 11:50 Mail "Torres's round (notes)", training back to "ask". BROKEN for a real player.
- 10:48 "Service: Main lift": arrow "Repair the main lift" on Deck 5 with no place (the lift has no panel place:
  MACHINES row ['5-mainlift-1', 'lift', null], panelPlace null) so it points at the lift landing [18, 8]. Tapping
  the Lift panel, the Lift brake, the Spine ladder or the spot itself (a real click at the pin) starts nothing. The
  player stays stuck on it from 10:52 to the end of the shift (shift2.txt). Suspected BROKEN: needs a builder's look
  (the lift's repair may be meant to start some other way).
- 15:17 "Very hungry" -> arrow "Food, Deck 3" (needs arrow, over the job arrow; comes back after). 15:49 "Bursting" ->
  "A toilet". Both clear themselves and hand back to the job. WORKS.
- 17:00 shift end: no clock-out word or arrow while a job is still in hand (the job's arrow keeps the screen).
  18:00 toast "Shift over: the clock signed you out at 17:00." + Mail "You didn't clock out".
- Shelves: the arrow's spot for a shelf (5-parts-2 "Filters") is exactly as close to the Lights shelf as to the
  Filters shelf (1.12 m each; 5-parts-3 Plumbing likewise next to Filters). A player tapping under the pin can tap
  the wrong shelf; the game's toast then says "Cartridges are on the Filters shelf: it's lit up for you." Small fix:
  point the shelf arrow at the shelf itself (item: the shelf's title), not the place in front of the aisle.
- Board empty (Day 9 afternoon, shift9.txt): no arrow and no word at all, 14:30-18:00. A line such as "Nothing on the
  board for you just now. New jobs come on the hour." would help.

The tracked-shift chain, as it is today (what wins the one arrow):
1. Any IX_GOAL (set by anyone: a tracked appointment, a needs arrow, a tea arrow, a career arrow, the drill...).
2. Else, if tracking isn't switched off (SHIP.player.track !== null): your job's next step (ixJobStep).
3. Else, on a shift day with no job: "Clock in at the time clock" (from 08:00), then "Take a job at the job board"
   while the board has something for you (ixWorkStep). Nothing for clocking out (section 15's clock reminder sets
   its own IX_GOAL only if no other arrow is up).
So the chain itself is good, and every failure the user meets comes from step 1: an arrow that took over and never
let go, or an arrow that never came because a check looked at "is a job tracked".

## How the game guides the player today (0.64.15, integration 2b4a05db)

### The world arrow (section 15b, lines 15655-15870)
- One arrow on screen at a time: `#ixGoal` (a gold ring with a pointer when the spot is off screen, a bobbing pin when it is on screen, and a label pill). Drawn by `ixFrame` each frame.
- What it shows: `IX_GOAL` if set (any section can `setGoal({ deck, room | place | item | crew | xz | at, label })`), else your tracked job's next step (`ixJobStep`, recomputed each ship minute), else, on a shift day with no job, `ixWorkStep` (clock in, then "Take a job at the job board").
- Off your deck it says "Take the lift to Deck N: ..." and points at the lift.
- It hides while a progress bar is over you.
- No priority, no queue. Each caller decides for itself whether to overwrite: some check "never over someone else's arrow" (intro arrows, tea, needs, round guide), some overwrite at once (drill 45906, incidents 48376, team jobs 48535, promotion summons 49409, move 49468, clue arrows 47635-47641), and some skip if a job is tracked (training asks 45268, the test job 49306).
- `SHIP.player.track`: `undefined` = job arrow on (nothing chosen), a job id = that job tracked, `null` = tracking off. Taking a job at the board sets it to the job id (15631) and **nothing resets it when the job is turned in**, so it stays truthy for the rest of the game. The clue arrows, Maps, Roster, Tracked taps set it to `null` (job arrow off) and only Tracked's own `trkDone` turns it back on.
- Nobody clears an arrow they set unless they wrote code for it. 24 core's training-meeting arrow is never cleared.

### First-time arrows (section 21, 43110-43200)
- `INTRO_ARROWS` (clock, board, eat, stow, tea, call): shown the first time you are told to do something; saved done flag per id (`SHIP.intro.done['arrow:<id>']`); never over another arrow; cleared once done or past its time. This is the pattern Pillar 5 should copy.

### Tips (section 19, 11517-11532)
- `tipShow(id, text)`: a green card at the foot of the screen, once ever per id (saved in `SHIP.device.tipsSeen`), a queue of one at a time, closes on tap or after about 9 seconds; off if tips are off in Settings. Text only; it cannot point.
- The round guide (`roundGuide`, 15741-15771) is the one place that pairs a tip with the arrow, step by step: the model for teaching a mechanic.

### Toasts, Mail, bubbles
- `toast(title, text)`: the line at the foot of the screen, a few seconds, no history.
- `mailSend`: Mail on the device (badge on the Mail app). Most Pillar 5 asks arrive as Mail plus a toast.
- `bubbleSay` / `worksSay`: a speech bubble over a crew member; if they are not on your deck, a toast.
- The Tracked panel (button on the main screen, and an app): lists your job, what is on today and tomorrow morning, and three places; a tap sets the arrow.

### The device and panels
- Apps are tiles with `data-app="<id>"` (11763); a badge count from `DEV.notes`. Pillar 5 apps: `works` (Training, Work log, Tools, Fault notes tabs), `scanner`, `pipekit`, `faultnotes`.
- The job board panel: `#ixBoard`, rows in `#ixBoardL` with a Take / Turn it in button.
- No way today to point at a button inside a panel, at a device tile, or at a board row. That is new work.

---

## Group A notes: the junior first week (Days 2-5, Day 8's uniform)

Build 0.64.15 (branch claude/arrows-plan), starship-cadet.html. Analysis only. Evidence: code reading plus runs with
harnessA.py (a per-process copy of AR1's harness, after the run_min fix) and these scratchpad scripts:
botA.py (bot + heads-ups, bubbles, device choices logged), probe_drill.py, probe_m2.py, probe_d5.py.
Outputs: day2.txt (AR1's), dayB3.txt, dayB4.txt, dayB5.txt, drill.txt, m2.txt, d5.txt. No JS errors in any run
unless said below.

## Problems that hit every training (core 24, not one mechanic)

C1. BROKEN: the meeting arrow never shows for a real player. trainTell (line 45268) only calls setGoal when
`!SHIP.player.track`. Taking any job at the board sets track to that job's id (15631) and nothing resets it at
turn-in, so from the first job a player ever takes, every training ask (m1 Day 2, m4 Day 3, m5 Day 4, m7 Day 5, m6,
t2's 49306 the same) comes with a toast and a Mail but no arrow. On Day 2 even the bot (track = the first solo job,
set by 43723) got no arrow for Torres's 10:45 meeting (day2.txt 10:00). Note: Dev mode's devmodeSetCareerTo leaves
track = null (switched off), so a bot run from Dev mode DOES see the meeting arrow; a real player does not.

C2. BROKEN: when the meeting arrow is set it is never cleared. Nothing in section 24 calls clearGoal. Seen: Day 3
"hauling and stores with Yara, 12:00" still up at 12:12 during the do stage, and still up at 14:40 in drill.txt
(the meeting long missed). Day 4: set at 06:00 for an 08:40 meeting. While it is up (IX_GOAL wins over everything,
15781) it hides the "Clock in at the time clock" arrow and your job's own arrow; in dayA3 (old harness) the bot never
clocked in all morning because the arrow never said so ("Not clocked in" toasts 09:43, 10:24).
Fix shape: clear it when the meeting starts (trainTick, c.st leaves 'meet'), and let it show only from about 15
minutes before the meeting (an ask at 06:00 for 12:00 should not own the arrow for six hours).

C3. HIDDEN: the watch stage has no arrow. trainWatch (45277) sets no goal; the teacher walks to the job (worksEscort
'lead') and the player must stay within 3 tiles / the same room for the row's watch minutes (10) or the training goes
to 'again' at shift end and is offered next workday with no word why. The only signal is the teacher's bubble
"Follow me. Watch this one." (or a toast if they're on another deck). The bot itself had to be teleported to
trainSpot to make it work.

C4. Toasts replace each other (toast(), line 52957: one slot, no queue). Several asks land in the same minute as other
toasts and are wiped at once: Day 2 10:00 had four toasts in the same minute (Calder's solo job, Torres's ask,
"Yesterday's clothes", then the mail toast), so Torres's ask is on screen for a frame. The ask's Mail is sent
quiet: true (no "New mail" toast). The heads-up strip (devHeadsTick) does give "Training: X starts in 15 min [Go]",
the one reliable signal; its Go sets the arrow.

C5. Small rows' briefings come AFTER the event. worksTrained (about line 45325) plays a small row's meeting script
when the row is first used, which is after the drill / inspection / uniform moment. Calder's "Drill at three... Back
to it. Ten minutes." and Tomas's "Three things... Before half six." both play after the thing they prepare you for.
The writer's asks works.ask.m3d ("Drill at three...") and works.ask.m3i ("Inspection tomorrow | Inspection is
Thursday at 06:30...") exist (33804-33807) but small rows never go through trainOffer, so they are never sent.

(Mechanic sections follow.)

C6. BROKEN: every small row's "word" (worksTrained, about line 45325: dialogueShow(sc) with no meeting) closes within a
ship minute. dialogueShow (37837) makes a meeting with no `where`; meetingsTick's last line (37929) closes any
dialogue whose meeting you're not "in", and inMeeting (37903) is false without a where. Seen in m2.txt: Day 8 10:00
"Trained: your work uniform" toast, then at once Mail "Your uniform (notes)" (quiet, the walk-away gist), no
dialogue left on screen (dlg null). Applies to m2, m3d, m3i and p3's trained talk. The player sees it for about
1-2 real seconds, then only a quiet Mail.

---------------------------------------------------------------------------------------------------------------
## M1 Rounds (Day 2, Torres)

What: walk a route of 4-6 machines on one deck, look at each, mark fine / worn / something's off; worn ones you mark
go on the board "found by you".
Unlock: ladder row m1 (45064): Day 2+, junior, needs Day 1's shadow shift done. Ask at 06:00 for a meeting at
10:45 (WORK_MECH.m1.at 625 -> 10:45 in play), Works bay. The ask is held until Calder's solo-job talk
(introSoloHold) and told at 10:00. After the talk (M1 is "self": no watch stage) "Your first round, Deck 4" is
reserved for you on the board; from the next workday a "Morning round, Deck N" at 07:00, held to 11:00.
Start / finish: be in the Works bay at 10:45 (the meeting plays when you're in the room) -> take "Your first
round" at the board -> walk to each machine's panel, tap it, stand 4 s ("Looking"), pick a mark on the card ->
after the last, turn it in at the board. Trained on turn-in (clipboard given).
What the player is told (day2.txt):
- 10:00 Mail Zeke Torres "Fancy a walk?" + toast "Fancy a walk? I'll show you my round. Tea corner, or the bay till
  half eleven. (10:45, Works bay on Deck 5.)" - but in the same minute Calder's solo job toast, the "Yesterday's
  clothes" toast and the mail toast replace it (C4).
- NO arrow to the meeting: the solo job is tracked (43723), so trainTell skips setGoal (C1). Confirmed.
- 10:30 heads-up "Training: rounds starts in 15 min / Works bay [Go]" (from the Calendar; only if heads-ups are on).
- 10:45 the meeting (dialogue train.m1.torres-zeke) if you're in the Works bay.
- After it: arrow "Take your first round at the job board" (roundGuide, RG_GOAL, 15757) + tip rg:take "Your first
  round is on the job board. Take it, and follow the arrow."
- Then per stop: arrow "Look at Washer 2" (ixJobStep, names the machine), tips rg:go / rg:look ("Look at Washer 4.
  Listen to it. Then mark what you see.") / rg:mark / rg:next; Torres's bubble "Your turn. Stand still a sec. Listen
  first."; the marks card (deviceChoose: Fine / Worn / Something's off); toast "Round done. Anything worn is on the
  board, found by you." -> arrow "Turn it in at the job board" -> toast "Trained: rounds, with Zeke Torres. Round
  clipboard is yours now."
Verdict: WORKS once you're at the meeting (the best-guided mechanic in the group); getting TO the meeting is
HIDDEN (no arrow, toast wiped). If you miss 10:45 the row goes back to 'ask' and is offered on your next workday.
Small oddities: tip numbering rg:look:1 named Washer 4 after rg:next:1 named Light relays 1 (bot teleports; may be
bot-only). The 07:00 morning rounds from Day 3 have no ask or tip of their own: they just appear on the board.
Arrow moments:
1. 10:00-10:45, after Calder's talk: world arrow to Works bay / Torres (setGoal {deck 5, crew: 'torres-zeke'} or
   room 'w'), "Meet Zeke at the tea corner, 10:45" (needs C1 fixed: show it over the tracked job, or queue it
   after the solo job). Goes when the meeting starts.
2. After the meeting: existing RG_GOAL arrow "Take your first round at the job board" - then inside the board
   panel an arrow on the "Your first round" row's Take it button (NEW: panel arrow).
3. Each stop: existing job arrow "Look at <machine>".
4. At the marks card: point at the card itself (NEW: device-card arrow) "Pick what you saw".
5. Turn-in: existing "Turn it in at the job board" + panel arrow on Turn it in.

## M2 Your work uniform (Day 8, Torres)

What: oily jobs make your uniform grubby (a shade darker); a change at your wardrobe cleans it, a shower doesn't.
Unlock: row m2 (Day 8+, junior, needs flag works.oily). The flag is set by the first oily machine job (oven, range,
extractor, galleyplant, cartdock, lift, pump, heatpump, fan, irrigation) turned in on Day 8 or later (45780). The
row opens at the next hour tick 06:00-16:00 and trains at once (open -> worksUse).
Start / finish: nothing to do; it's a word from Torres, then just a rule (grime .35 per oily repair, grubby from .6:
two oily repairs; change at the Bunk 1 wardrobe).
What the player is told (m2.txt, a 3-oven-1 repair turned in at 09:50 Day 8):
- 10:00 toast "Trained: your work uniform, with Zeke Torres." immediately replaced by "Yesterday's clothes: You're
  in yesterday's clothes. Change at your wardrobe in Bunk 1..." (C4).
- 10:00 Torres's two lines (train.m2.torres-zeke) open and close at once (C6) -> quiet Mail "Your uniform (notes)":
  "Zeke told you oily jobs make your uniform grubby. Change at your wardrobe after them; a shower won't do it."
- After one oily repair grime is 0.35, uniformState 'clean': Torres's "half a machine on you" fires before you
  look grubby at all.
- The writer's ask works.ask.m2 ("Your uniform | Saw you after that job. Change before tea...") is never used.
Verdict: WORKS BUT HIDDEN (the talk flashes away; the tint is subtle; the only lasting trace is a quiet Mail).
Arrow moments:
1. When it opens: world arrow to Torres if on deck, else to the wardrobe in Bunk 1 (existing setGoal with place =
   the wardrobe, as CLOTHES_GOAL does at 43516) "Change at your wardrobe" - shown when uniformState() is grubby,
   gone after the change.

## M3 The drill (Wednesday 15:00, Day 3) and the inspection (Thursday 06:30, Day 4)

What: the drill: at 14:50 a drill job is yours (fire week 1: extinguisher off its bracket, stand by the hatch,
extinguisher back; pressure: four turns of the bulkhead wheel; power: the breaker cabinet), all-clear 15:15, Calder
words your time. The inspection: be in your bunk room at 06:30-07:00 Thursday with a clean uniform (changed today),
bed made (tap your bunk, "Make the bed"), locker tidy; the duty officer's line, else a Mail at 07:00.
Unlock: rows m3d (Day 3, Wednesdays, small, no needs) and m3i (Day 4, Thursdays, small, no needs). Both open at the
06:00 ladder tick the same day. A small row is trained by its first use (drill attended / inspection attended or
all three right while away). Juniors only.

### The drill
Start / finish (as built): 14:50 the job "Fire drill" is claimed for you (45882) as a SIDE job; its stops are
5-drill-ext, 5-drill-hatch, 5-drill-ext; it closes at 15:15 whatever you did.
What the player is told (drill.txt, Day 3):
- 14:50 toast Calder "Drill in ten minutes. Muster at the Works bay. Take the extinguisher. Stand by the hatch."
- 14:50 arrow "Fire drill, 15:00" to the Works bay room (45906). Never cleared by 24c (stays after 15:15).
- 15:07 (late) heads-up "Drill at 15:00: Fire drill. Muster at the Works bay is starting / the lift lobby on each
  deck" (the Calendar's DEV_WEEK line, 11283, says the lift lobby; the job says the Works bay).
- 15:15 toast "All clear. Drill over." + Calder's time word (slow if you never reached a stop).
Verdict: BROKEN. A real player cannot do any drill step. Repro: Dev mode, Set career to Day 2, skip to Day 3 14:40,
clock in, at 14:52 stand at 5-drill-ext and tap "Fire extinguisher": playerTap returns false, no activity, the job's
stops stay undone (drill.txt). Why: the drill is a side job (jobKindAdd 'drill', side: true); myJob() (19180)
excludes side jobs, and the chore tap ixChoreTap (15305) and the job arrow ixJobStep (15668) only ever look at
myJob(). Nothing reads the items' `drill: 'ext'` / `drill: 'door'` tags (4790-4791) and mySideJobs (19181) has no
caller. So the drill always ends "slow" with j.reached undefined; worksUse('m3d') never runs (45922 needs did or
mins), so m3d is never trained and Calder's briefing (train.m3d.calder) never plays. (In Dev mode's career set it is
marked trained on paper, which hides this.)
Also: no ask before the day (works.ask.m3d "Drill at three. Works bay, ten to. Fire, this week." unused, C5).
Arrow moments (once the taps work):
1. 14:50: world arrow to the muster (room 'w' or place 5-muster-k) "Drill: muster in the Works bay" (existing).
2. Then the step arrows, which need the job arrow to follow side jobs (NEW in ixJobStep: a side job's next stop
   wins over the board job while it's open): "Take the extinguisher" (place 5-drill-ext / item "Fire
   extinguisher"), "Stand by the hatch" (5-drill-hatch), "Put it back" (5-drill-ext); pressure: "Turn the bulkhead
   wheel" (item "Bulkhead wheel"); power: "The breaker cabinet" (5-drill-breaker).
3. 15:15: clear the arrow with the all-clear.

### The inspection
What the player is told (dayA4.txt, Day 4; the bot was elsewhere):
- Nothing the day before. The writer's ask works.ask.m3i ("Inspection tomorrow | Inspection is Thursday at 06:30.
  Clean uniform, bed made, locker tidy.") is never sent (C5).
- The Calendar's fixed Thursday line (DEV_WEEK, 11285): "Bunk inspection: tidy your bunk" at 06:40 (the walk is
  06:30, INSPECT_AT 390).
- 06:25 heads-up "Bunk inspection: tidy your bunk starts in 15 min / your bunk, Deck 4" (no Go button: the line has
  no deck/room).
- Tapping your bunk Thursday 05:30-08:00 gives a card "Your bunk: The inspection is at 06:30. [Make the bed | Tidy
  your locker | Lie down]" (bunkPick, 13265) - the only in-world hint, and only if you happen to tap the bunk.
- 06:59 Mail Calder "This morning's inspection: Two of the three weren't right this morning. Uniform, bed, locker:
  all three next week." (+ "New mail" toast).
- Day 4's m5 ask arrives at 06:00 with an arrow to the galley for 08:40 (when its arrow shows at all, C1/C2), which
  pulls the player out of the bunk room before 06:30.
- Tomas's briefing (train.m3i.tomas "Three things. Clean uniform. Bed made. Locker tidy. Before half six.") plays only
  after a first inspection that counts (C5), and then flashes away (C6).
Verdict: WORKS BUT HIDDEN. It runs and never fails, but a new player cannot know it is coming or what is checked
until the remark Mail. A player who leaves the bunk room before 06:30 and isn't perfect is not trained that week.
Arrow moments:
1. Wednesday evening (from ~20:00) or Thursday 06:00 wake: world arrow to your bunk (place playerBed()) "Make your
   bed: inspection 06:30" (existing setGoal); goes when bedMade === today.
2. If not changed today: arrow to the wardrobe in Bunk 1 "Fresh uniform for inspection" (existing; CLOTHES_GOAL
   pattern). If untidy: the bunk again, "Tidy your locker".
3. Inside the bunk card: point at "Make the bed" (NEW: device-card arrow).
4. 06:25-06:30: if out of the bunk room, arrow to the bunk room "Inspection at 06:30" (existing setGoal, room).
   Goes at 07:00 or when the officer has spoken.

## M5 Tuning (Day 4, Calder / Brennan)

What: a machine out of adjustment (oven running hot, relay flickering, dock charging slow): at its panel press − or +
one step at a time, watching the machine, until it settles.
Unlock: row m5 (Day 4+, junior, needs one manifest run, m4 use 1). Teacher: Calder (first on shift; Brennan speaks
in the script). Opening drifts 3-oven-1 and 3-oven-2 two steps hot (48185). Ask 06:00 for a meeting at 08:40 in
the Galley (Deck 3, room K). Afterwards tune jobs ("Tune: Oven 1 (running hot)") come from section 17's drift.
Start / finish: be in the Galley at 08:40 -> watch Calder tune Oven 1 (stay within 3 tiles / in the galley 10 ship
minutes) -> "Tune: Oven 2" is held for you on the board -> take it -> at Oven 2's panel the card "Oven 2: Watch the
machine, not the dial. It's a little hot. [− | +]" -> press until settled -> turn in. Trained on turn-in.
What the player is told (dayA4.txt, Day 4; the bot started with tracking off so it saw the arrow):
- 06:00 Mail + toast Calder "Galley, 10:15. Bring nothing. (08:40, Galley on Deck 3.)" - BROKEN text: the writer's
  ask (works.ask.m5, line 33811) hard-codes 10:15; trainOffer (45255) adds the real time 08:40 in brackets because
  the body doesn't contain it. Two times in one message.
- 06:00 arrow "tuning with Ines, 08:40" (only with tracking off; a real player gets none, C1). Set at 06:00 it
  owns the arrow for 2 h 40 and drags the player off to Deck 3 before the 06:30 inspection (M3).
- 08:25 heads-up "Training: tuning starts in 15 min / Galley, Deck 3 [Go]".
- 08:40 meeting train.m5.calder (Brennan: "Forty rolls, love..."). The meeting is before the 09:00 shift and before
  you can clock in.
- 08:43-08:53 watch: Calder's bubbles ("One down. Watch it."), no arrow (C3). 08:53 "Your turn. It's on the board
  for you; I'll be right behind you." (bubble or toast).
- Your job: the job arrow says "Repair the <oven>" (ixJobStep's machine branch, 15697: a tune job has no parts, so
  it gets the repair label), not "Tune Oven 2".
- On the card each press says "Oven 2: a little hot." etc.; settled -> Brennan's "There. That's my oven back."
Verdict: WORKS (on paper the stages run in order; the turn card is section 15's tested workStep) but HIDDEN at the
start (no arrow, a wrong time in the ask) and in the watch.
Arrow moments:
1. 08:25-08:40: world arrow to the Galley (room 'K', deck 3) "Tuning with Calder, 08:40" (existing; needs C1/C2).
2. Watch: arrow at Calder / Oven 1's panel (setGoal {crew: 'calder'} or place panelPlace('3-oven-1')) "Watch
   Calder tune Oven 1" - goes when the watch ends.
3. Do: "Take Tune: Oven 2 at the job board" (existing ixWorkStep arrow) + panel arrow on its Take it button (NEW).
4. At the panel: label should read "Tune Oven 2" (small fix in ixJobStep for kind 'tune').
5. On the turn card: point at − (NEW device-card arrow) "Watch the oven, press −"; goes when settled.

## M4 Hauling and stores (Day 3, Yara Esposito)

What: the manifest run: after the Wednesday delivery, take a hover cart, load each crate in the hold, ride the lift,
drop each at its stop, dock the cart.
Unlock: row m4 (Day 3+, junior, needs one round of yours, m1 use 1). Ask 06:00 for a meeting at 12:00 in Main
storage (WORK_MECH.m4.at 660 -> the schedU slot gave 12:00). From then on each Wednesday's run ("Manifest run: N
crates") is held for you 13:00-16:00. Stage 2 (choose the order) from Day 10 after 2 runs; stage 3 the stocktake
(Thursdays 13:30) only from Day 18 as an officer, so not in this week.
Start / finish: be in Main storage at 12:00 -> watch Yara's "Manifest run: 1 crate" (cart + first crate; stay
near 10 ship minutes) -> "Manifest run: 3 crates" held for you -> take it -> cart at the Cart bay dock, load
each crate in the hold, drop each at its stop (linen to the laundry etc.), cart back -> turn in. Trained on turn-in.
What the player is told (dayB3.txt, Day 3):
- 06:00 Mail + toast Yara "The rest of the delivery: Shelves done? Meet me at the hold. There's a manifest with your
  name on it. (12:00, Main storage on Deck 5.)" - says "at the hold" but the meeting room is Main storage (r), not
  the cargo hold (c).
- 06:00 arrow "hauling and stores with Yara, 12:00" (lower-case start; only with tracking off, C1) -> it stays from
  06:00 until after the run (C2), hiding the clock-in arrow all morning (dayA3: never clocked in).
- 10:00 the delivery itself ("Supply delivery" heads-up, "Unload the Wednesday delivery" on the board) - the ask
  ("Shelves done?") assumes you unloaded it; nothing points you to that unload.
- 11:45 heads-up "Training: hauling and stores starts in 15 min / Main storage, Deck 5 [Go]".
- 12:00 meeting train.m4.esposito-yara; 12:02 bubble "Follow me. Watch this one." (watch, no arrow, C3).
- 12:12 do: the board shows "Manifest run: 3 crates"; Yara's lines on each step ("Your go. Two more. Mind the
  corners.", "Laundry. Linen by the door, not on the floor."); the cart run's own arrows (ixJobStep restock/haul
  stops: cart, load, deliver, return) are the job arrow's.
- 12:14 toast "Trained: hauling and stores, with Yara Esposito."
Verdict: WORKS (the bot did it on paper: m4 trained 12:14) but HIDDEN at the ask and the watch (C1-C3). Honest
taps not re-run for the haul stops (they go through ixChoreTap like other chores, which works for the cart runs
already in the game).
Arrow moments:
1. 10:00 (delivery): existing heads-up Go to the cargo hold; an arrow on the board row "Unload the Wednesday
   delivery" would help (NEW panel arrow).
2. 11:45-12:00: world arrow to Main storage / Yara (setGoal {crew: 'esposito-yara'}) "Meet Yara in Main storage,
   12:00". Goes when the meeting starts.
3. Watch: arrow at Yara (crew) "Watch Yara load the cart"; goes at the do stage.
4. Do: "Take Manifest run at the job board" + panel arrow on its Take it. Then the existing job arrows; check the
   first one names the Cart bay dock ("Take a hover cart from the Cart bay").
5. Later Wednesdays: a 13:00 nudge, arrow to the board "Manifest run waiting" while it is held for you (none today).

## M7 The scanner (Day 5; Torres is off on Fridays, so Emeka Halloran or Calder teaches)

What: your first tool. At a faulty machine's panel the look-over opens the Scanner (device app 'scanner', hidden
from the grid, 46418): 3-5 parts with a bar and a word (good / worn / low / failing) and a "Fetch: <part>" button
each; you pick the part to fetch (scanPick). A wrong pick shows when you fit it ("Still leaks: it's the pump"), the
part goes back on its shelf.
Unlock: row m7 (Day 5+, junior, needs one tuning, m5 use 1). Ask 06:00 for 09:00 at the board. The teacher's job
(a faulty Tier 1 machine on Deck 3/4, d5.txt: Washer 4 (leaks)) is the watch (15 ship minutes, TRAIN_WATCH, M7 has
no watch override); your job is Day 5's P3 training case on Washer 2 (scanTrainReserve, 46430: c.m7 = true, the
teacher held with you, worksEscortHold). The scanner is handed over when your job is reserved.
Start / finish (as designed): 09:00 board meeting -> watch -> take "Repair: Washer 2 (leaks)" -> at Washer 2's panel
look it over -> the Scanner opens -> that reading is what shows P3's case (p3Tick `here` needs j.scan) -> the
case is called (Fault notes or a Fetch button) -> fetch, fit -> turn in.
What the player is told (d5.txt, Day 5):
- 06:00 Mail + toast Halloran "Board, when you're in. Torres left you something. (09:00, Works bay on Deck 5.)"
- 06:00 arrow "the scanner with Emeka, 09:00" (only with tracking off; C1), up for 3 hours (C2).
- 09:00 meeting train.m7.halloran-emeka; 09:03-09:18 watch (Washer 4), no arrow (C3); his bubbles ("Watch. Panel,
  scanner, and a moment's patience.").
- 09:18 toast "New job: Washer 2 (leaks), Deck 4 · laundry"; Take it -> toast "Job taken: Washer 2 (leaks)... Follow
  the marker: parts first, from main storage on Deck 5." + tip "Track it on your device; the marker shows the way."
- 09:19 arrow "Fetch a pump: the Plumbing shelf" (5-parts-3). BROKEN: p3Stage (47729, line 47739) puts j.parts = ['pump'] on
  the training job, so ixJobStep's "parts first" branch names the answer and sends you to storage before any
  scan. The board card and Take-it toast say "parts first" too.
- Following that arrow honestly (d5b.txt): tap "Plumbing" in Main storage 09:20 -> "Main storage: You take a pump.
  Now to the washer on Deck 4." -> arrow "Repair the washer" (generic, lower case) -> tap "Washer 2" 09:26 ->
  "Washer 2: You fit a pump. You set to work on the washer: about 28 minutes." No look-over, no Scanner, j.scan
  false, P3's case still waiting (wait true, no clues, no calls). Repro: Dev mode, Set career to Day 4, skip to Day 5
  05:50, attend the 09:00 board meeting and the watch, Take "Repair: Washer 2 (leaks)", follow the arrow.
- Consequences (code): caseFitted (47527) returns false for a case still waiting, so the repair finishes as a plain
  job; caseTick (47486) closes the waiting case when its job is done; the turn-in trains m7 (worksDone, the hold
  ends as the case is closed) without one scan (worksUse('m7') is only in scanFitted, 46399); P3's one training case
  (C.first) is spent, so P3 waits for a random case (CASE_RATE junior .1 a fault, at most 1).
- The Scanner panel itself (scanView, read from the game at 09:26): "Scanner · Washer 2 (Laundry) / The job: leaks /
  Pump · worn 55, Seal · worn 44, Valve · worn 49, Bearing · good 71, Relay · good 94 / Fetch: pump | Fetch: seal |
  Fetch: valve | Fetch: bearing | Fetch: relay". On the training case every suspect reads "worn" and the answer
  reads highest (by design), so the scanner alone can't solve it: the player needs Fault notes.
Verdict: BROKEN as a lesson: the arrow skips the scanner entirely on Day 5 (above). The scanner app itself works when you tap a faulty machine's panel
without the part in hand.
Arrow moments:
1. 08:45-09:00: world arrow to the job board (item /job board/) "Halloran at the board, 09:00".
2. Watch: arrow at Halloran (crew) "Watch Emeka scan Washer 4".
3. Do: Take it (panel arrow), then the job arrow must go to Washer 2's PANEL first, "Look Washer 2 over" (fix:
   no parts on the training job until the case is called).
4. Scanner open: arrow inside the device at the bars "Read the bars", then (training) at the Works app's Fault
   notes tab, "Open Fault notes" (NEW: device arrows).

## P3 What's been tried? (Day 5, first head-scratcher)

What: a fault the crew already had a go at; their notes ("New door seal in. Still leaks. — Kovac") rule out what
they tried. You cross out suspects in Fault notes (a tab of the Works app, 47651) and Call it.
Unlock: row p3 (small, Day 5+, needs trained m7). Day 5's case is staged at 18:00 Day 4 on Washer 2 (or 3), cause
the pump, tries on the seal and the valve overnight (p3Stage, 47729). It shows (caseShow: the job retitled
"Head-scratcher: Washer 2 leaks", deviceNotify on the Works app, the teacher's bubble "Here's a funny one... Open
Fault notes: the first note's taped to the job.") when the row is open, or during M7 once you've scanned it.
Clues: the first note is collected when you hold the job (at 'board'), the others by standing at the machine's
panel ("+ clue: Kovac" toast + device notice). Fault notes: suspects as chips (tap to cross out), the clues list,
"Where next?" (sets an arrow to the next clue), "Call it: <part>" -> "Yes / Not yet" -> toast "Called it: A pump
from main storage, Deck 5. Follow the marker." The Scanner's Fetch buttons also call the case (scanPick -> caseCall).
Hints: The Chief's notes; "Talk it through" after two wrong calls; "Fit them one by one".
Trained when the case's job is turned in (caseDone -> worksUse('p3')), then its talk flashes (C6).
What happens in play: on the honest Day 5 path the case never shows (see M7: the arrow fetches the pump, the pump is
fitted, the case closes unseen). Fault notes then reads "No head-scratchers open. When the board has one, its notes
are here." The case UI (caseView/caseAct) was read in code, not driven live this session.
Verdict: BROKEN on Day 5 (unreachable by following the game's own arrow). When a case does show, Fault notes is a
tab inside the Works app with a badge; the only pointers are a device notice, the teacher's bubble and "+ clue"
toasts: WORKS BUT HIDDEN at best.
Arrow moments:
1. When the case shows: device arrow on the Works app icon, then on the "Fault notes" tab (NEW).
2. In Fault notes: arrow on "Where next?" (NEW panel arrow) -> then the existing world arrow it sets (place of the
   next clue, "Laundry").
3. After the clues: arrow on a suspect chip "Cross out what was tried", then on "Call it: pump" (NEW).
4. After the call: the existing job arrow "Fetch a pump: the Plumbing shelf", then "Repair the Washer 2", turn in.

---------------------------------------------------------------------------------------------------------------
## Summary (BROKEN first)

BROKEN
- Drill (M3, Wednesday): no drill step can be done; the side job is invisible to the tap and arrow code (myJob
  excludes side jobs). Never trained; Calder always says "slow"; arrow stays up after 15:15.
- Day 5 scanner + P3: the training job carries j.parts = ['pump'] (47739), so the arrow says "Fetch a pump", you fit
  it, no scan, the head-scratcher never shows and is spent; m7 still "trained".
- C1: no meeting arrow for any training once you've taken one job (track never reset; 45268).
- C2: when the meeting arrow does show it is never cleared and hides the clock-in / job arrows for hours.
- C6: small rows' talks (m2, m3d, m3i, p3) close within a ship minute; only a quiet "(notes)" Mail is left.
- M5 ask text names two times: "Galley, 10:15. Bring nothing. (08:40, Galley on Deck 3.)".
WORKS BUT HIDDEN
- M1 rounds (well guided after the meeting; the ask is wiped by other toasts), M4 hauling, M5 tuning (watch stage
  unpointed, C3), the inspection (no warning before the first; Calendar says 06:40; heads-up has no Go), M2 uniform.
NOT BUILT (in this group): the stocktake is built but only from Day 18 for officers; M2's stage 2 (a washer held
for you) is "not yet" (45772).
JS errors: none in any run (drill.txt, m2.txt, dayB3.txt, d5.txt, d5b.txt).

New arrow kinds needed (beyond setGoal): an arrow inside the job board panel (a row's Take it / Turn in), inside a
device card (marks card, turn card, bunk card) and on the device (Works app icon, Fault notes tab, Where next?,
Call it). The world arrow also needs: a "crew" goal to follow a teacher during a watch (ixGoalWorld already supports
g.crew, 15715), a rule that a training meeting's arrow shows only in the last ~15 minutes and clears at the meeting,
and side jobs (the drill) in ixJobStep.

---

## Group B notes: M6 incidents, the career's own screens, then the road to Officer (Days 8-11)

Build 0.64.15 (branch claude/arrows-plan), read-only. Line numbers are starship-cadet.html.
How tested: my own copies of AR1's harness (B_harness.py / B2_harness.py, with the fixed run_min), no JS errors in any run.
- B_run2.txt: Set career to Day 7, then Days 8, 9, 10, 11 played in a row by the follow-the-arrow bot (track reset to on, clocks in at 08:20, takes every job it can). The bot cheats (teleports, takes jobs with claimJob instead of the board, does steps on paper), so I used it for the order of events and checked the honest path separately.
- B_run3.txt: Set career to Day 9 (test passed), Days 10 and 11.
- B_m6.py: an honest Day 8 morning in the Works bay, then the walk to the office and the pipe. B_team2/3.py: the Day 11 team job at the player's spot.
- Screenshots: B_worksapp.png, B_record.png, B_m6_call.png, B_m6_after.png, B_m6_pipe.png, B_team2.png, r2_d8..d11.png, r3_d10/11.png.

## Problems that cut across everything (they hit most of my mechanics)

X1. Stale arrows. Every career arrow is set with setGoal and nothing in section 24 ever clears it:
"Meet Ines" (incidents, 48366), "Your test job" (49306), "The Chief's office, 11:00" (49409), "Your cabin, 4-23"
(49465), "Your commission, the observation room" (49570), the team job's "brace the housing" (48536), trainTell's
meeting arrow (45268). Seen in play: "Meet Ines" stayed up from 10:30 to the end of Day 8; "The Chief's office, 11:00"
from 10:30 to 17:00 on Day 10; "Your cabin, 4-23" from 17:00 Day 10 through all of Day 11 (it was still up when the
team-job meeting at 09:20 needed an arrow). While IX_GOAL is set, goalNow() hides the job arrow, the clock-in arrow and
"Take a job at the job board" (15663). Only taking a job at the real board clears it (15631).
Fix idea: a career goal carries its own done-test (`until`), cleared when the meeting is met/missed, the job is taken, etc.

X2. Tracking off after Dev "Set career". After devmodeSetCareerTo(7) SHIP.player.track is null (the Settling-in list's
"go" sets track = null, 11911), so goalNow() shows no job arrow and no clock-in arrow at all until the player takes a
job at the board. Any device "go" button (heads-up 11456, Maps 12070, roster 12148, cases 47635) does the same. In
honest play the user who tests with Dev mode sees no arrows on Day 8 morning. AR1's finding the other way round also
holds: once any job has been taken, track is a job id and trainTell (45268) and promoTestTell (49306) skip their arrow.

X3. The Works reputation the career uses (SHIP.works.xp, "Relied on" gates the test job) is never shown changing.
There is no toast when the band moves up or down, and a missed shift quietly takes 3 (onSim shiftMissed, 45453).
The turn-in card's gold chip "Works reputation up" (turnInGains 15915, from careerJobIn 40276) is the other,
Pillar 4 department reputation (SHIP.rep), not this one. Two different things share one name.

---------------------------------------------------------------------------------------------------------
## Step 1 parts (the career's own screens)

### S1. Reputation in words (worksBand / worksBandWord, 45428-45432)
- What: your standing as a junior, five words New / Steady / Reliable / Trusted / Relied on (Tier 2 restarts at "New officer").
- Unlock: SHIP.works exists from Day 1 17:00. Points: service +1, repair +2, overhaul +3, +1 found by you, +1 right
  first time (from Day 5), +1 clever; side jobs (vents, calibrate, carry runs) flat and capped at +2 a day (worksSideXp);
  missed shift -3, abandoned -2 (WORK_XP 45099). Bands at 0/8/18/30/40 (WORK_BANDS 45096).
- In play: Set career Day 7 gives 30 (Trusted). The bot took about 20 jobs on Day 8 and ended at 37 (most were capped
  side jobs), so not "Relied on" on Day 8; 56 by the end of Day 9. A player who misses a shift loses 3 each day
  (run811: 30 -> 27 -> 24 -> 21 over Days 8-10 with no message about the drop).
- How told: only by reading it. Works app Training tab first line "Junior Officer. Works reputation: Trusted." and the
  Record's first line. No toast when it changes. The board's order changes with the band (18433), silently.
- Verdict: WORKS BUT HIDDEN. Also a words problem: the rank shows as "Junior Officer" (writer's works.rank.junior) and
  the Record reads "Junior Technician · Junior Officer." while the promotion is to "Works Officer": a junior reads as
  already an officer.
- Arrow moments: none in the world. Needed: a small toast/chip when the band changes ("Works reputation: Reliable"),
  pointing at the Works app icon (device arrow, new).

### S2. The turn-in card's gains and the chip (turnInShow 15935, turnInGains, careerJobIn 40276)
- What: after "Job complete", a row of chips: gold "Works reputation up" (or the department's), then "+4 Power" etc.
- Unlock: any job turned in at the board, from Day 1. careerJobIn fills j.gains.rep; the meters come from j.meters.
- How told: the chips on the turn-in toast. Not seen in my runs because the bot turns in with turnInJob directly
  (no board UI); code path is straightforward.
- Verdict: WORKS (not re-tested by a real board tap here), but see X3: the gold chip is the department reputation,
  and it shows "up" even when the career band does not move (a capped side job). Never a down chip.
- Arrow moments: none needed. Better: when the career band crosses a line, the chip says the new word.

### S3. The Works app (device app 'works', order 31, worksView 45534; tabs Training 45510, Work log 45521, Tools 45527, + Fault notes from 24k)
- What: Training (rank, reputation, What's next, what you're trained in, "What you know" per machine kind after 5
  jobs), Work log (last 30 jobs with found by you / right first time / clever / who noticed), Tools (what's in your locker, wear).
- Unlock: hidden until SHIP.works exists (Day 1 17:00).
- In play (Set career Day 7, B_worksapp.png): tabs "Training / Work log / Tools / Fault notes". Training: "Junior
  Officer. Works reputation: Trusted." / "What's next Calder's waiting to teach you about incidents." / Trained list
  (job loop Day 1 ... scanner Day 5). Work log after Set career: "No jobs yet. The board's waiting." (Dev leaves it
  empty; real play fills it). Tools: "Round clipboard [In your locker · like new · since Day 2] / Torres's old scanner
  [In your locker · Charged · since Day 5]".
- How told: nothing points at it. The "Trained: ..." toast (worksTrained 45341) does not mention the app; the app
  has no badge for a new training or tool (only Fault notes has a badge).
- Verdict: WORKS BUT HIDDEN.
- Arrow moments (all device-side, new: the world arrow can't do it):
  - First "Trained" toast (Day 2 rounds): point at the Works icon on the device home, "Your training is in Works" (< 40 chars). Gone when the app is opened once.
  - First tool given: point at the Tools tab, "Your tools live here". Gone on first open of the tab.
  - First job turned in after Day 2: point at Work log once, "Every job you turn in".

### S4. The Record's first line / What's next (worksRecordHead 45483, worksNext 45462)
- What: rank, title, band and one sentence of what comes next.
- In play: "Junior Technician · Junior Officer. Works reputation: Trusted. What's next: Calder's waiting to teach you about incidents."
- BROKEN (misleading words): worksNext (45477) picks the next unopened big ladder row without checking its needs, so
  from the moment m6 is trained it says "Calder has a test job for you: Tier 2." (writer's next.t2). In play that
  line showed all of Day 8 evening and all of Day 9 while no test existed and the player was short of "Relied on"
  (B_run2 end of Day 8: xp 37, test null, next "Calder has a test job for you: Tier 2."). The player is never told the
  real condition (reach "Relied on"). Repro: Set career 7, play Day 8; read worksNext() after m6 is trained.
- Also: on the test day after passing, "Calder wants you in her office. Don't keep her waiting." shows from Day 9
  evening, a day before the summons exists (fine, but no time is given).
- Arrow moments: none in the world; the line itself is the teacher. It should name the gate ("Reach Relied on: Calder
  will set your test") and the time when there is one.

### S5. The locker text (worksLockerText 45414, PLAYER_TAPS hook 45420)
- What: tap the Kit lockers in the Works bay: "Your locker. Clean clothes, and your tools: Round clipboard, Torres's old scanner."
- Unlock: once you have a tool (Day 2 clipboard).
- How told: nothing; the Tools tab says "In your locker". Verdict: WORKS BUT HIDDEN (flavour only, nothing to do there).
- Arrow moment: optional, once with the first tool: Kit lockers item, "Your locker: your tools", until tapped.

---------------------------------------------------------------------------------------------------------
## M6 Making it safe / incidents (24f, 48194-48427)

- What: a burst pipe (or stuck lift, galley alarm): close the right valve, mop the wet, then fit a new joint.
- Unlock (code): ladder row m6, Day 8, big, needs one scanner use (m7 uses >= 1), teacher Calder on shift (45071).
  The ask is not a Mail: incOffer (48326) books a 15-minute meeting in Calder's office (Deck 5 'o') at 10:30, no
  Mail, no toast, no told flag. At 10:30 (WORK_TICKS 48352) the incident starts, Calder says "Burst pipe, junior wing.
  With me." (bubble if she's on your deck, else a toast) and setGoal "Meet Ines" to her office.
  After that (Week 3 on) one incident a week on the board, held for you 30 min (incPlan, incPost).
- In play (B_run2 Day 8 and B_m6.py): row opened at 06:00 (training m6:meet, occasion works.m6@10:30). Nothing told
  the player before 10:30. Standing in the Works bay: at 10:30 the arrow "Meet Ines @D5 o" appeared; her line was a
  bubble (no toast because she was on the same deck). Walking into the office at 10:33 played train.m6.calder.
- To start: be in Calder's office between 10:30 and 10:45. To finish: follow Calder to Deck 4's valve panel (watch 1
  minute within 3 tiles), then go back to the job board on Deck 5 and take "! Burst pipe, Deck 4", close the right
  valve (the last one on the line), mop the wet spots, then the fix job "Replace a burst joint: junior corridor"
  (a seal from the Plumbing shelf). Trained when the joint job is turned in.
- How told, with times (B_m6): 10:30 arrow "Meet Ines"; 10:33 meeting; 10:35 board shows "! Burst pipe, Deck 4:
  with Ines" (her walk, not yours); 10:47 (after I teleported to the pipe) board "! Burst pipe, Deck 4"; Calder's
  bubble "Your turn. It's on the board for you; I'll be right behind you."; then the step lines (train.m6.follow.*:
  "Which valve? Follow the pipe.", "Water's off. Mop. Plenty of it.", "One seal. Stores. Then the joint.") and
  toast "Trained: making it safe, with Chief Ines Calder."
- Verdict: BROKEN for an honest player (works only if you already know the way):
  1. After the meeting the arrow still says "Meet Ines" and points at the office you are standing in. Calder walks off
     to Deck 4 (worksEscort 'lead'), nothing points there; the board entry "...: with Ines" is not takeable. If you
     don't follow her, c.w never counts (trainNear) and the training sits in 'watch' until the shift ends, then is
     offered again next workday (B_m6: stayed 10 minutes in the office, still 'watch', arrow still "Meet Ines").
     Code: trainWatch 45277 sets no arrow (AR1's finding bites here), incidents' call arrow 48366 never cleared.
  2. Once you reach the pipe and it's your turn, your job is on the board on Deck 5, not at the pipe: back up the
     lift, take it, back down. Nothing says so except her bubble; the arrow still says "Meet Ines" (X1), which hides
     the job arrow "Take a job at the job board".
  3. No warning before 10:30. A player mid-job on another deck has 15 minutes to reach Deck 5's office; late means
     missed, c.st 'ask', and the incident goes to the crew. Next workday at 06:00 (run811 Day 9 and 10) Calder's
     toast "Let's try that again. Follow me, and watch." arrives while you're in bed, with no place or time, and the
     reserved walk job sits on the board; Days 9 and 10 repeated the same with no arrow. While m6 is pending, W.cur
     blocks every other big row, and the test job needs m6 trained, so the whole promotion waits on this.
  4. The burst incident from a failed Day 8 stayed open over the next days (run811: same incident id, the puddle stays).
  Repro: Set career 7; skip to Day 8 10:00; stand in the Works bay; at 10:30 walk to the office; after the talk do
  nothing: training stays 'watch', arrow stays "Meet Ines".
- Arrow moments:
  a. 10:15 (new: a heads-up 15 min before): toast "Calder wants you at 10:30, her office". World arrow: Calder's office (Deck 5 'o'), "Calder's office, 10:30". setGoal can do it.
  b. 10:30 call: keep "Meet Calder: burst pipe" to the office (exists). Clear it when the meeting is met or missed.
  c. Watch: arrow on Calder herself (setGoal { crew: 'calder' }, already supported by ixGoalWorld) "Follow Calder", then the valve panel place 4-valve-panel "The burst pipe, Deck 4". Gone when c.st becomes 'do'.
  d. Do: "Take the burst pipe job" at the job board item (/job board/i, Deck 5). Better: let the player take it at the pipe (no new arrow then). Gone when taken; the job's own steps take over.
  e. Valve step: the 'choose' card (Which valve?) needs a hint inside the panel: "The one nearest the wet" (in-panel pointer, new).
  f. Wet spots: job arrow already walks them (4-wet-1, 4-wet-2).
  g. Fix: job arrow already covers "Fetch a seal: the Plumbing shelf" then the joint.

---------------------------------------------------------------------------------------------------------
## The road to Officer (only partly re-tested; lower priority per the lead)

### T2. The Tier 2 test job (24p, 49261-49330)
- What: one real Tier 2 repair (an air scrubber on Deck 4: filter, then settle the fan) with Calder watching.
- Unlock: workday from Day 8, 09:10, needs "Relied on" and m6 trained (promoAnnounce 49276). Said in person if you're
  in the Works bay, else Mail at 10:00. Test on the next workday: board slot held 09:00-15:00. Not taken by 14:00 /
  dropped: set again two workdays later, Mail "Not today, then..." (promoDelay).
- In play (B_run2): not announced on Day 8 (xp 37 < 40 after ~20 jobs). Day 9 10:00 Mail "Your test job :: Tomorrow,
  your test job. A real Tier 2 job. I'll be watching. Sleep." Day 10 06:00 toast "There it is. Yours. I'm watching,
  not helping." and arrow "Your test job @D4 s" while the player is in bed and the job isn't on the board till 09:00.
  09:00 job up, passed 09:01 (bot); "Your test job" arrow stayed up the rest of the day (X1).
- Verdict: WORKS BUT HIDDEN, and a day late against the design for a busy player (announce Day 9, test Day 10,
  promotion Day 11, ceremony Day 12). The gate ("Relied on") is never said (S4). If the player has ever taken a job,
  the start arrow is skipped (49306, track check). The 06:00 start line is wasted in bed.
- Arrow moments: test day 09:00 (not 06:00): job board item "Your test job: on the board" until taken; then the job's
  own arrow. Announce: a toast as well as the Mail.

### P1. The first promotion (summons, scene, cake, move, ceremony; 24p 49331-49577)
- In play (B_run3, Set career 9, Day 10): 10:30 toasts "Calendar :: Chief Calder: My office, 11:00. — C." and the
  same from Chief Calder, arrow "The Chief's office, 11:00". 11:01 the scene (promo.officer) played; Mail from the
  Captain, Tomas and Pell queued. Arrow then stayed up till 17:00 (X1). 16:30 toast "Brennan's made a cake. Works tea
  corner, before five." (no arrow; nothing waits on it). 17:00 arrow "Your cabin, 4-23 @D4 W" plus the clock's
  "shift's done, clock out" pulling the other way; the bot did not get there and at 17:30 Mail "Your cabin :: You
  weren't about, so we moved you anyway..." The cabin arrow then stayed up into Day 11.
  Day 11: Mail 08:00 "Your commission, 17:15"; no arrow at 17:15 (only at 17:30 when Calder comes: toast "The
  Captain's waiting..." and arrow "Your commission, the observation room @D1 O").
- BROKEN (words): a missed ceremony's Mail at 19:00 reads like an invitation, sent after the event: "Your commission,
  17:15 :: The officer ceremony is today at 17:15, observation room, Deck 1. Clean uniform...". promoCommission
  (49537) looks up 'mail.promo.ceremony' first, and the writer's baked line under that key (31371) is the invite; the
  real "we missed you" line is under 'promo.ceremony.mail' (31985). Also 17:40 a "Your commission (notes)" Mail says
  you were commissioned before it happened. Repro: B_run3 (Set career 9, play Days 10-11, don't reach Deck 1).
- Verdict otherwise: WORKS in real play (the chain ran from the real test on Day 10 to officer on Day 11 in B_run2),
  BUT HIDDEN at the cake, the move and the ceremony's start.
- Arrow moments: 10:30 office (exists; clear at the scene). 16:30 cake: Brennan / place 5-tea-3, "Your cake: tea corner", until 17:00 or you're near. 17:00: Calder herself ({ crew }), "Follow Calder to your cabin", then 4-23. Day 11 17:00: the observation room, "Your commission, 17:15", gone when the scene starts.

### M8. Team jobs (24h, 48428-48641)
- What: a big job with three or four crew; you do the "your turn" steps at your spot when the lead calls.
- Unlock: m8 row, Day 11, officer, trained t2; Mail 16:00 the day before and 08:05; meeting at the recycler (Deck 3 R) 09:20.
- In play (B_run3 Day 11 and B_team2/3): Mail Day 10 16:00 "Recycler membrane change tomorrow at 09:30, Deck 3...
  be at your spot", Day 11 08:05 "Recycler's membrane bank, 09:30, Deck 3. Need four." (subject "team jobs" in
  lower case). No arrow to the 09:20 meeting (teamOffer 48619 never tells; the stale cabin arrow was up instead).
  09:36 toast "Your turn: brace the housing", arrow "brace the housing @D3 R".
- BROKEN: your turn can't be done. The team kind is a side kind with a machine (19109), so myJob(), ixChore() and
  jobHere() all return null (19180, 15292, 14213); tapping the floor at your spot (3-recycler-team-4, type 'event',
  no item) or the Water recycler does nothing ("Water recycler: in good order. It's your job."). Because you're at your
  spot, j.youIn is true, so teamLate never fires (48573): the job waits on you all day, the arrow stays, m8 is never
  trained, and next day it's 'again'. Repro: Set career 10; skip to Day 11 09:05; go to Deck 3 room R; after the talk,
  stand at the spot: at 10:09 still j.cur 1, "brace the housing". mySideJobs (19181) exists but nothing uses it.
- Arrow moments (after the fix): 09:10 the recycler room, "Team job at 09:30: recycler"; each turn, the spot place
  (not the room middle) "Your turn: brace the housing"; gone when the step is done.

### B. The bridge by invitation (bridgeBarred 40164, bridgeInviteReady 40163)
- Not reached in my runs (needs the first ship-wide event over: the ion storm is Day 12). Doors say "The bridge. The
  duty crew only: you need the Captain's permission to go in." on tap or walking up. Invitation is a chance meeting
  with Vance at breakfast, no notice (38054). Verdict: not tested; by design hidden.
- Arrow moment: none needed before the invite; after it, "The bridge, Deck 1" on the bridge-hour day.

---

# Later steps (3+), kept for when they come up

## Group C: the officer's puzzles (Days 11-15 on), build 0.64.15

Analyst C for AR1. Analysis only, nothing in the repo changed. Cut short at the lead's call: P2 and a full honest
P1 first case were not played to the end (noted below).

How it was played: cplay.py (a follow-the-arrow player that taps the nearest thing where the arrow points, clocks
in at the time clock, takes jobs at the board the way the board's Take button does: track = job, clearGoal). Cases
are never auto-called: the player opens Works > Fault notes, presses the panel's own DOM buttons (Where next?,
suspect chips, Call it, Yes), and goes where the arrow points. Runs: s12 (Day 12, m9 training, career set to the
end of Day 11), s14 (s12 then a skip to Day 15), s15 (Day 15 with career set to the end of Day 14), s13 and sfav
(Day 13, favour cases, ticket Mail). Logs: s12b.txt, s13.txt, s14.txt, s15.txt, sfav.txt in the scratchpad.
No JS errors in any run (page errors and console errors both empty).

Screenshots (390x844) in the scratchpad: case-p1.png (Fault notes, a ticket case before any clue),
case-p1-clues.png (after three clues: the day strip), case-d15.png / case-d15-clues.png (the same on another
run), case-p1-before.png (Fault notes with no case), trace-pipekit.png (the Pipe kit page after a reading),
favour-jobs.png (the Jobs app with a favour case accepted: it is not listed).

---------------------------------------------------------------------------------------------------------------
## BROKEN (first)

### B1. After you call a case, the job's arrow never comes back (all cases: P1, P3, P2, tickets)
- "Where next?" (caseAct 'next', 47632-47641) does `SHIP.player.track = null` and `setGoal(...)` with no `trk`, so
  trkDoneCheck (15951) never clears it. Nothing else clears it. After the call the job needs a part fetched, but
  goalNow() stays on the last clue place, and with track = null the job's own arrow (ixJobStep) is hidden.
- Seen (s14 and s15, Day 15 08:39): after Yes the toast says "Called it: A seal from main storage, Deck 5. Follow the
  marker." and the arrow still reads "manifold room" (the last clue, Deck 5). track: null.
- Repro: take any case, press Where next?, collect, call it: the arrow stays on the clue.
- The only way back is Jobs app > Track (verb 'track', 12018), which nothing tells the player.
- Fix idea: give the clue goal `trk` + `back: true` (so trkDone puts track back on arrival), and clearGoal in
  caseAct 'yes'.

### B2. A ticket (and the P1 first case) points the job arrow straight at the answer
- A P1 case's job is the faulty machine itself. ixJobStep (15687-15712) uses `machineById(j.machine)` directly; it
  never asks 24k's caseAt (only jobStopsBase does, 19202). Before any call the arrow reads "Repair the water filter
  bank" (Day 15 08:00, s15/s14), and the filter bank's seal is the answer. 24k's comment (47757) says the card and
  the stop must not name the machine.
- The ticket's card also names it: ffPost (48802) sets `j.title = 'Ticket case: {machine} {shows}'` after caseShow,
  so the board, the Jobs app and "Job taken" say "Ticket case: Water filter bank low flow", while the suspects list
  shows "Water filter bank: seal". The puzzle is solved by reading the title.
- Repro: Dev mode, career to end of Day 14, skip to Day 15 05:50, clock in, take "Showers on Deck 4 run weak, but
  only after it's been used" at 08:00: the arrow and title name the cause.

### B3. Favour cases can't be done at all
- Accepted (chat Help? > yes, or favourAccept), 24l makes the 'fcase' side job (48765) with three clue stops at the
  friend's bunk and a choose. But: no arrow (ixJobStep and ixChore only read myJob(), which excludes side jobs,
  19180); the Jobs app doesn't list it (favour-jobs.png); tapping the bunk does nothing (playerTap -> false; the stop
  taps in 15b, ixChoreLast/jobHere, only serve myJob(); 24l has no tap of its own, unlike shop/drill/team).
- Seen (sfav, Day 13): 19:30 Mail from Tomas Lind "My door :: My door squeaks, but only at night. In the day it's
  silent. Am I imagining it?" Accepted 19:38; side job "A door that only squeaks at night", stops 4-B1-1 x4; goal
  null; six taps on the Bunk, nothing; state stays 'taken'.
- Also the Mail doesn't say how to accept (talk to Tomas, Help?). The favour's own fix stop has placeId null until
  solved, so it can't be handed back either.
- Repro: Dev mode, career to end of Day 12, skip to Day 13 19:20, wait for the Mail, accept, try anything.

### B4. M9 training: the traced job is on the board from 06:00, before the pipe kit
- WORK_MECH.m9.open (46616) posts 5-valve-2's traced job at 06:00 ("Showers weak on Deck 4", held for you). The pipe
  kit is only given at the meeting (09:20; reserve -> toolGive, 46618). A player who clocks in and takes it first gets
  an arrow "Read the water line: try Circulation pumps" and every tap says "You need the pipe kit to read the flow."
  (s12, 08:00 and 09:00). Taking the job also clears the meeting arrow (board Take: clearGoal, 15631), so the
  09:20 meeting has no arrow at all after that.
- Repro: Day 12, clock in at 08:00, take the showers job, follow the arrow.

### B5. M9: the arrow ignores what the readings say (the "halve it" lesson is contradicted)
- traceGoal (46539) orders the unread machines by distance from the middle only. Seen (s12, 09:33-10:12): reading
  Circulation pumps: "Full after it: the trouble is further down the line." Next arrow: "try UV steriliser"
  (upstream), then Circulation pumps 1, 2, then Water filter bank (upstream again), then Pipe valves 2. Six readings
  where two or three should do, and the arrow sends you up the line right after the toast says down.
- Fix idea: after a reading, keep only the side the reading points to (after full: downstream; before low: upstream).

### B6. P1 doesn't open on Day 12, and its first case waits days
- Only one small ladder row opens per workday (ladderTick 45188). On Day 12 m10 (small) opens at 06:00 because p1
  needs m9 trained (not yet at 06:00). Day 13-14 are off. So p1 opens on Day 15 at the earliest, then p2 on the next
  workday, and m11, m12, m13 queue behind them. The plan says P1 Day 12, P2 Day 15.
- Seen (s14): m9 trained Day 12 11:11; the first P1 case (3-pump-1, reserve21) staged at once but still waiting at
  Day 15 08:30 (op has nothing after Day 12 at 05:50). Meanwhile Day 15's ticket at 08:00 is a P1 case, so the
  player meets P1 first as a ticket, with no word from Calder and no Chief's notes page shown.
- (With Dev mode "set career", p1 is marked trained and C.p1 = 'none': the first P1 case is never staged.)

### B7. The arrow and meeting rules from AR1 bite M9
- trainTell (45268) skipped its arrow when track is set: with a job taken earlier, the m9 meeting has no arrow.
  In s12 the meeting arrow ("tracing with Ines, 09:20") was set at 06:00, then cleared by taking the job at 08:00.
- trainWatch: no arrow to the demo (Calder reading 5-pump-1 on Deck 5) during 09:23-09:33; the arrow kept pointing
  at the job's line. A player who doesn't stand near 5-pump-1 never gets to 'do' (c.w counts only when trainNear).
- With no job taken (s12 first run) the meeting arrow stayed up after the meeting and hid "Clock in".

---------------------------------------------------------------------------------------------------------------
## The mechanics

### 1. The case engine and the head-scratcher card (24k, 47233-47400)
- What: some repairs become puzzles: suspects, clues at places or people, cross out, call it, then fetch and fit.
- Unlock: a kind's ladder row open (caseKindsOpen). Roll cases: a repair or overhaul at your tier posted 06-15h on
  your shift day, chance .2 an Officer (CASE_RATE 47257), at most 1 open. None rolled in the runs played.
- Start: take the "Head-scratcher: ..." job at the board (held for you till the shift ends). Finish: call, fetch,
  fit; a wrong call says so at the machine ("New X in. Still Y.").
- Told: board card title "Head-scratcher: <machine> <shows>" (P1: the line's symptom; state "head-scratcher, asked
  for you"); device note with the title (caseTick, 47457). "Job taken" toast: "..., Follow the marker." Nothing says
  "open Fault notes". The writer's line case.new "A new head-scratcher is on the board." exists but no code uses it.
  The job arrow before a call: "Repair the <machine>" at the machine (a P3 or P2 case's job is that machine, fine;
  P1 see B2). Fitting with no call: toast "You look it over: it still <shows>. Fault notes has the suspects."
- Verdict: WORKS BUT HIDDEN (the panel is two taps deep, Works > Fault notes, never named on taking), plus B1, B2.
- Arrows: at take, a pointer to the device button, then to the Works app's "Fault notes" tab ("Open Fault notes");
  gone once the tab is open. New: device/panel arrows (the world arrow can't point into the device).

### 2. Fault notes panel (Works app tab 'faults', 47604-47652)
- What: the case's notepad: suspects (tap to cross out), clues got, Where next?, Call it, hints.
- Told: a badge "(1)" on the tab while a case has no clue yet (CASE_BADGE), "+ clue: <name>" toasts.
- Seen (case-p1.png, Day 15): "Showers on Deck 4 run weak, but only after it's been used / Suspects (tap to cross
  out) / Water filter bank: seal | Pipe valves 2: valve | Circulation pumps 2: pump | UV steriliser: seal / Clues /
  More to find. / WHERE NEXT? / CALL IT: ... x4 / THE CHIEF'S NOTES / FIT THEM ONE BY ONE".
- Where next? works: arrows "water recycler, Deck 3" (UV steriliser panel), "starboard pipe gallery, Deck 5",
  "manifold room" (labels are the room, not the machine; fine). Each clue was got on arrival, toast "+ clue: log".
- Crossing out: chips toggle; crossed ones drop out of the Call it list (good). Call asks "Call it: the Water filter
  bank: seal?" Yes / Not yet; then "Called it: A seal from main storage, Deck 5. Follow the marker." (but B1).
- The call is allowed at any time, even with no clues (all four Call it buttons show at once).
- Verdict: WORKS (panel), BROKEN after the call (B1).
- Arrows (inside the panel, new): "Where next?" button on first open ("Find the clues"); a suspect chip after a clue
  that rules it out ("This log rules it out: tap"); the last Call it button once one suspect is left ("Call it");
  Yes. World arrow: each clue place (exists, B1 fix needed so it hands back to the job).

### 3. Hints, wrong calls, talk it through, the long way (47570-47600)
- What: Chief's notes (rules of thumb per kind), Where next? falls back to a hint toast, after 2 wrong fitted calls a
  "Talk it through" button crosses one decoy out; "Fit them one by one" fits each suspect in turn.
- Told: after the 2nd wrong fit: toast "Fault notes :: <Torres/Calder> can talk it through with you: it's on Fault
  notes." (caseFitted 47566). The talk is instant (no meeting, unlike the spec's appointment).
- Not reached in play (the wrong-call run was cut). From code: a ticket's wrong fit ends the ticket ("Not yet. Next
  week."), so talk-it-through only happens on non-ticket cases.
- Odd: a ticket's hint says "no hints till you've looked at three things yourself" (ticket.nohint), but a T2 P1 has
  exactly three clues, so by then the hint is only "You've got every clue there is." Seen in s15.
- "Fit them one by one" sits next to the Chief's notes from the first second, with no word of what it costs
  (no clever fix, no right first time). Easy to tap by mistake.
- Verdict: WORKS BUT HIDDEN (untested end to end).
- Arrows: after the toast, a device arrow to Works > Fault notes > "Talk it through".

### 4. P3 What's been tried? (as an Officer roll case) (47660-47746)
- What: the crew already tried some parts and left notes; a note's part is ruled out.
- Unlock: p3 row (Day 5, Junior, after m7). As an Officer it rolls on repairs (machine with 3+ part causes on one card).
- Start/finish: the case waits (hidden from the board) 2-12 h while the crew's tries happen, then shows during your
  shift; first note taped to the job (got when you take it), others at the machine panel.
- Told: device note with the title only. Not seen in play (no roll in the days played).
- Verdict: WORKS BUT HIDDEN (Day 5 training covered by group A/B; the Officer roll not reached).
- Arrows: same as 2; clue "at the machine's panel" is the job's own machine (the job arrow already goes there).

### 5. P1 When does it happen? (47747-47912)
- What: a fault on a water/heat/air line that shows only at some hours; each other machine's log at its panel shows a
  full day = not it.
- Unlock: p1 row (Day 12 in the table; needs m9 trained; see B6). First case staged after the tracing lesson
  (3-pump-1), shown with Calder's word: "Here's one the pipe kit won't settle. ... When does it happen? That's the
  question. The logs are at the panels." (bubble; train.p1.word has no written line).
- Seen as a ticket on Day 15: card "Showers on Deck 4 run weak, but only after it's been used", "Deck 4 · the water
  line", "head-scratcher, asked for you" (good) but title overridden (B2). Clues: three logs, each "full output
  every hour, evenings too", the day strip shows (case-p1-clues.png). Solved by elimination in 7 game minutes.
- Note: all three logs read the same; the "when" (only after use) plays no part: it is pure elimination.
- Verdict: BROKEN as a puzzle while B2 stands; panel WORKS.
- Arrows: Where next? to each panel (exists); a panel arrow at the strip ("All day fine: cross it out").

### 6. P2 Who saw what? (47913-48125)
- What: ask crew who were near the machine when it acted up; one may be mixed up (the Roster says where they were).
- Unlock: p2 row (Day 15, Officer) AND Tomas's (or Torres's) word at a meal you share: p2Word (48097) only fires
  when you stand in the room where Tomas is eating breakfast/lunch/dinner. First case 4-scrubber-2 staged 16:00
  Day 14 (seen: creserve22, wait, held off the board).
- Start: after the word, the case shows; clues by "Ask about the fault" on each witness's chat card.
- Told: Tomas's bubble "You're asking around about the scrubber? Ask who sleeps near it. And check they were in."
  Nothing says to eat with Tomas; next.wait.p2-style lines are the only hint (What's next on Training).
- Not reached in play (row not open by 08:30 Day 15; run cut). Where next? for a person points at where they are
  now (whereIs), good; the chat card's "Ask about the fault" button needs the player to open the chat.
- Verdict: WORKS BUT HIDDEN (gate is invisible; untested in play).
- Arrows: at a meal time, "Eat with Tomas" to his seat; after: the witness (crew arrow, `crew:` goal exists, 15702);
  inside the chat card, the "Ask about the fault" button (new).

### 7. M9 Tracing with the pipe kit (24i, 46449-46629)
- What: a traced fault's card names the symptom; tap machines on the line with the pipe kit to read flow before/after;
  "fine before, low after" is the machine.
- Unlock: Day 12, Officer, ladder row m9 (big), teacher Calder (or Emeka Halloran). In play: Day 12 06:00.
- Told: 06:00 Mail and toast Calder "The pipe kit :: Board, first thing. Showers on Four are weak. You'll find out
  why. (09:20, Works bay on Deck 5.)"; 06:00 toast "New job: Showers weak on Deck 4, Deck 4 · the water line";
  arrow "tracing with Ines, 09:20" (Works bay). 09:20 meeting dialogue train.m9.calder. 09:23 watch (no arrow). 09:33
  'do'. Each reading: toast "Pipe kit :: You clip the pipe kit on and read the flow.", then e.g. "Circulation pumps
  :: Before: full · After: full. Full after it: the trouble is further down the line."; the Pipe kit page opens by
  itself (trace-pipekit.png: bars and the line upstream first). Found at 10:12: "Pipe valves 2 :: Before: full ·
  After: low. Full before, low after. It's Pipe valves 2." Then a normal repair: "Fetch 2 × valve: the Plumbing shelf",
  "Repair the pipe valves", trained 10:52: "Trained: tracing, with Chief Ines Calder. Pipe kit is yours now."
- Verdict: WORKS, with B4, B5, B7. Maps marks the line (traceMarks), not checked on screen.
- Arrows: meeting (exists, B7); watch: "Watch Calder read the pumps" to 5-pump-1 (world arrow can do it); reading:
  traceGoal (exists, B5); after the first reading the Pipe kit page "The line, upstream first" list (device, new).

### 8. Fault-finder tickets (24l, 48780-48857)
- What: from Day 13, a harder T2 case on the board at 08:00 each workday, held till 17:00; solved right first time
  makes you Fault-finder grade 1 (a pin on your uniform); a wrong fitted call: "Not yet. Next week."
- Unlock: Officer, Day 13 Mail; first ticket on the next workday (Day 15 in play; Day 13-14 are off).
- Told: Day 13 08:10 (09:11 in s14) Mail Calder "A ticket case :: A ticket case, when you're ready. It's on the Works
  board. Harder than the others. Take your time." Day 15 08:00 toast "New job: Showers on Deck 4 run weak, but only
  after it's been used, Deck 4 · the water line." Board title "Ticket case: Water filter bank low flow".
- Seen: taken, three clues, called right. The fetch/fit/turn-in and the pin were not reached (run cut; B1 would stall
  an arrow-follower at the last clue).
- Verdict: BROKEN as a puzzle (B2), engine WORKS; the pin/grade untested.
- Arrows: board entry "Ticket case" on Day 15 08:00 ("Your ticket: take it"); then as 2.

### 9. Favour cases (24l, 48642-48778)
- What: off shift, about once a week a crew friend Mails a small mystery; three looks in their cabin, then "What's
  causing it?" (a pick), then fix and hand back.
- Unlock: Officer, Day 13+, an evening 18:00-21:00, a friend at relTier 3 (Day 13: only tomas and torres-zeke were).
- Told: Mail only (see B3). Verdict: BROKEN (B3).
- Arrows: Mail -> "Tomas asks a favour: find him" (crew arrow); chat "Help?" button (new, chat card); each clue stop
  (world arrow, once a side job can drive it); the choose card (device).

### 10. The cold-case board
- NOT BUILT (no code; only in plan Part 6, seat H's list).

### 11. The plan's nine kinds (plan Part 4)
- BUILT: P1 When does it happen?, P2 Who saw what?, P3 What's been tried? (CASE_KINDS, 47715, 47893, 48058).
- NOT BUILT: P4 Which gauge is lying? (Day 17), P5 Follow the line (Day 18; M9 is its first stage), P6 Does it add
  up? (Day 22), P7 Faded labels (Day 23), P8 Swap testing (Day 25), P9 The clash (Day 19). Also not built: the
  logger and the test rig as clue tools (WORK_TOOLS has 'logger' with mech 'p5', unused), grades 2 and 3.
- Plan vs code: P3 is Day 5 (Junior) in the code, Day 11 in the plan's table.

---------------------------------------------------------------------------------------------------------------
## Arrow moments, short list (for the arrow plan)
| when | where | line | can the world arrow do it? |
|---|---|---|---|
| a case job taken | device button, then Works > Fault notes tab | Open Fault notes | no: device arrow |
| Fault notes first open | Where next? button | Find the clues | no: panel arrow |
| clue place | the clue's place (panel, board, person) | Read the log here | yes (exists), needs trk/back (B1) |
| a clue got that rules one out | that suspect chip | Cross it out | no: panel arrow |
| one suspect left | its Call it button, then Yes | Call it | no: panel arrow |
| after Yes | the part's shelf (job arrow) | Fetch a seal: Plumbing shelf | yes, once B1 is fixed |
| wrong fit x2 | Fault notes > Talk it through | Talk it through | no: panel arrow |
| m9 watch | 5-pump-1 panel, Deck 5 | Watch Calder read it | yes |
| m9 reading | next machine on the halved line | Read the flow here | yes (B5 fix) |
| P2 gate | Tomas at his meal | Eat with Tomas | yes (crew goal) |
| P2 witness | the person; chat card "Ask about the fault" | Ask them | world yes; chat button new |
| ticket day | board entry at 08:00 | Your ticket is up | yes (board item) |
| favour Mail | the friend; chat "Help?" | Tomas needs a hand | crew yes; chat button new |

Not checked (cut): P2 in play, a P3 roll as Officer, talk it through end to end, the ticket's pin, the first P1
case's showing with Calder's word, Maps line marks.

---

## Group D: side jobs and off-shift things (Day 12 on, as an officer)

AR1's analyst D. Build 0.64.15 (starship-cadet.html on claude/arrows-plan). Analysis only; nothing in the repo changed.
Scripts and raw output are in this scratchpad: ladderD.py / ladderD.txt (when each row opens; meetings missed),
ladderD2.py / ladderD2.txt (the same with each training finished as a steady player would), tapD.py, tapD2.py,
tapD3.py (+ .txt): real taps through playerTap on ITEMS at the times a player would come by. No JS errors in any run.

## BROKEN first (full summary at the end)
- M15 and M17 meetings: no meeting arrow while a job is tracked (45268); stale meeting and team-job arrows stay up;
  m15 meets 08:40 before clock-in; nothing leads from the m17 meeting to the lift (about 20-minute window).
- M10: "follow the marker" toast, but side jobs get no arrow (myJob 19180 leaves them out).
- Everything else in this group works but is hidden (see each section).

## Overview

### How the side rows really open (ladderTick, 45177-45193)
- At most **one small row a workday** and one big row; nothing opens on a day off (`playerShiftOn`), small rows only
  06:00-16:00. The small rows go in table order (CAREER_LADDER 45064-45099), so the "Day 12" side jobs come **one a day**.
- Steady player (ladderD2: m9 done on Day 12): m10 Day 12 (Fri), p1 Day 15, p2 Day 16, **m11 Day 17**, **m12 Day 18**,
  **m13 Day 19**, **m14 Day 22**. Big rows: **m15 Day 17** (Wed), **m17 Day 18** (Thu).
- If m9 is never finished (ladderD): m10 12, p2 15, m11 16, m12 17, m13 18, m14 19. m15 and m17 never open, because
  W.cur (m9 'ask') blocks every big row (45185, `size === 'big' && (W.cur || ...)`).
- The design's check-in ("Day 12: an order on the shop board, your bench, the log at 16:30", step4-summary) is not
  what happens: on Day 12 only the workshop opens. Not a bug in the code, but the user should know the real order.
- **A small row opening says nothing at all.** ladderOpen (45194-45204) only pushes the id and calls the sub-block's
  `open`; m10's open is empty (46826), m11/m12 are `{ noJob: true }` (46207, 46322), m13/m14 `{}` (48986, 49250). No
  toast, Mail, tip, arrow or bubble on the day any of them opens (checked in ladderD/ladderD2 logs, Days 12-32).
- **The Works app never lists side jobs.** "What's next" (worksNext 45461-45481) looks only at big rows; the Training
  tab lists rows once trained. A small row is invisible until you have already done it once.
- The writer's lesson for each small row (MEETING_SCRIPTS train.m11/m12/m13/m14, 34643-34648) plays at the **first
  use** (worksTrained 45330), so it comes after the player has found the thing alone. m12's ends "Go on. Today's."
  although the entry has just been written.

### Shared arrow problems that hit this group
- trainTell (45268) sets the meeting arrow only when no job is tracked (`!SHIP.player.track`); track is set when you
  take any job (15631) and never cleared, so m15's and m17's meeting arrows are usually skipped (AR1's finding 1).
- The meeting arrow is never cleared (AR1's finding 2). Seen here: tapD/tapD3 still showed **"tracing with Ines,
  09:20"** (Day 12's m9 meeting) on Day 18 at 16:02, over the order board, the bench, the log, the telescope and the roof.
- A team job's arrow ("brace the housing @D3 R", Day 18 09:37, m8) stayed up from Day 18 to Day 25 in ladderD2 and
  replaced the m17 meeting arrow the same morning. (m8 is another group's; noted because it hides m17.)
- **Side jobs have no arrow at all.** ixJobStep (15667) follows `myJob()`, and myJob (19180) leaves out side kinds
  (`!jobSide(j)`), so the workshop order is never pointed at. The device's Jobs app (12021) also shows only myJob.
- **"New job" toasts skip jobs with no machine** (jobNotice 14029: `j.machine`): leak jobs and the nozzle job are
  never announced. Rewiring jobs (they have a machine) are.

## M10 The workshop (order board, lathe/fabricator, hand over) and tinkering (24j, 46630-46826)
- What: crew pin little orders in the machine shop; you make the thing at the lathe or fabricator and hand it over.
  Tinkering: with no order, tap the lathe/fabricator and make a gift or cabin thing from offcuts.
- Unlock: orders from Day 12 as an officer (shopOn 46686), posted Day 12 08:00 then Mondays 08:00 (46813). Row m10
  (small) opened Day 12 in both runs. Trained at the first hand-over (worksUse in shopGiveSay 46805; tr.m10 = 12).
  Tinkering from Day 6 (TINKER_FROM), no row.
- Start: tap "Order board" (Deck 5, machine shop f, place 5-shop-board) -> device card "Order board: Take an order:
  make it here, then hand it over in person." -> pick one. Finish: tap the "Lathe" / "Parts fabricator" (set it going,
  a 10-minute wait), tap again after 10 min (collect), tap again (finish by hand, 2 min) -> thing in your hands ->
  find the person -> chat card button "Give the lamp arm".
- Told today (tapD2, Day 12): 08:15 toast "Order board: You take Yara's order: the lamp arm. At the lathe." 08:15
  bubble/toast Halloran "Set the lathe going. Come back in ten. Lovely." toast "You set the lathe going on the lamp arm.
  Ready at 08:25; come back then." 08:33 toast "Make the lamp arm for Yara: Done here. 1 stop to go: **follow the
  marker**." 08:36 "Machine shop: The lamp arm is done, and in your hands. Hand it to Yara in person." Hand-over:
  "The lamp arm works. I can see my page. Thank you." Nothing announces the order going up; the only Mail is the lapse
  a week later ("Yara Esposito: The lamp arm: I made do, don't worry. Thanks anyway.", Day 19 00:05).
- Verdict: **WORKS BUT HIDDEN**, with one **BROKEN** line: "follow the marker" (the generic step toast) promises a
  marker that never comes, because side jobs get no arrow (19180). Repro: Day 12 08:10, take an order, tap the lathe,
  wait 10 min, tap again: toast says follow the marker; the arrow still shows the old meeting (or nothing).
  Also: the collect tap and the finish tap are two separate taps on the same machine (3 taps in all), with no tip.
  Yara was on Deck 3 at work at the time; nothing says where she is.
- Arrow moments:
  1. Order up (Day 12 08:00, Mondays 08:00), while no order is taken: item "Order board" (5-shop-board), Deck 5.
     "A crew order: the order board". Goes when you take one or it lapses. Existing world arrow can do it
     (`{deck:5, place:'5-shop-board'}` or `item:/^order board$/i`); needs a rule for side jobs (a goal source after the
     board job, or when no board job).
  2. Order taken: place 5-shop-lathe / 5-shop-fab, "Set the lathe going". Goes when the wait starts.
  3. Wait done (at the ready time): same place, "The lamp arm is ready: finish it". Goes when the thing is in hand.
  4. Thing in hand: the person (goal `crew: id`, ixGoalWorld supports it, or deck/room from whereIs), "Give Yara the
     lamp arm". Goes on hand-over. Needs: ixJobStep (or a sibling) to read mySideJobs() / shopData(); new code.
  5. Tinkering (Day 6+, once): a one-time tip at the lathe, not an arrow.

## Off shift: cabin touches (24t, 46830-46944)
- What: put things you made or bought on four spots in your officer's cabin 4-23 (floor, desk, shelf, ledge).
- Unlock: once 4-23 is yours (worksHome, after the promotion move, about Day 10-11). No row.
- Start/finish: hold a fitting thing (tinkered, or from the crew store) and tap "The desk" / "The floor" / "The
  shelf" / "The ledge" in 4-23. Two or more: a small mood bonus at 06:00; visitors remark.
- Told today: nothing until you tap a spot. An empty-handed tap says "Nothing in your hands fits here. Something like
  a little lamp: make one in the machine shop or buy one at the crew store." (46905). Placing: "You put the little lamp
  there. It looks like yours now." (tapD2: placed, cabinData {desk: little lamp}).
- Verdict: **WORKS BUT HIDDEN** (self-explaining once tapped; the spots are invisible hit boxes until something is on
  them, so a player has no reason to tap an empty desk corner).
- Arrow moments: only one, first time you hold a cabin thing (tinkered or bought) and are on Deck 4 with 4-23 yours:
  item "The desk" (or the spot that fits), "A spot for it: your desk". Goes when placed or dropped. Existing arrow can
  point (`item:'The desk'`, deck 4); a one-time tip is probably enough instead.

## Off shift: star logging (24t, 46946-46991)
- What: 20:00-23:30 from Day 6, at the observatory telescope (Deck 2, room J), pick the new star of three; one a night.
- Unlock: Day 6, no row, no rank. starTap 46987-46992.
- Start/finish: tap "Telescope" in the observatory in the window -> card "Star log" -> pick -> "Logged: Wren 1. Survey
  will see it in the morning." (tapD3, Day 12 20:32). Every third: a Survey bubble; ten: a Record line.
- Told today: nothing. Crew invitations ("Observatory night? Stars, tea, and Rossi's tiny telescope", Zeke, Day 18
  15:40) bring you there but never mention logging. Outside the hours the telescope does its old thing, silently.
- Verdict: **WORKS BUT HIDDEN**.
- Arrow moments: an evening from Day 6 (20:00, only if not logged that night, first few times): Deck 2, item
  "Telescope" in room J, "Log a star at the telescope". Goes at the log or 23:30. Existing arrow can (deck 2 item);
  needs an off-shift goal source and a "not tonight" rule so it doesn't nag every evening (say the first 3 nights).

## M11 Tool upkeep (24m, 46144-46216)
- What: at "Your bench" in the Works bay, recharge the scanner (5-min wait), clean the pipe kit, check logger/tester.
- Unlock: row m11, small, day 12 (CAREER_LADDER 45082); opens **Day 17** for a steady player (Day 16 without m9).
  The bench tap only answers once m11 is open (46211); tool wear only counts from then (toolUpkeepOn 45383).
- Start/finish: tap "Your bench" (5-bench-you) -> card listing each tool and its state -> pick one -> hold (or the
  scanner's wait). First use: lesson dialogue train.m11.<officer> + toast "Trained: tool upkeep, with Emeka Halloran."
  + notes Mail "Torres's Friday routine (notes)" (tapD, forced open Day 12 08:43).
- Told today: nothing when the row opens. Before it opens, tapping "Your bench" gives no response (tapD: returned
  false, no toast). The only pointer: once a tool is "Due" (charge under 30, about 18 scans) a toast once a day
  "Your scanner's charge is low. Bench, when you can." (toolSlow 45394). Tools page in the Works app shows
  "Charged / Getting low / Due".
- Verdict: **WORKS BUT HIDDEN** (and the lesson waits until the player has already found the bench).
- Arrow moments:
  1. The row opens (Day 17 06:00) or the first "Due"/"Getting low": item "Your bench" (place 5-bench-you, Deck 5 w),
     "Look after your tools: your bench". Goes after the first upkeep. Existing arrow can (`place:'5-bench-you'`).
  2. Scanner on charge: none needed (toast says no need to wait).
  3. Stage 3 (after 4 upkeeps, once a week): item "Tool wall" (5-tool-rack), "The team's rack needs you". Optional.

## M12 The logbook (24n, 46218-46324)
- What: one line in the Works log, 16:30-17:30 on a workday, at the Works bay terminal by the notice board.
- Unlock: row m12, small; opens **Day 18** steady (Day 17 without m9). Tap only answers when the row is open, on a
  workday, 16:30-17:30, within 3.5 m of 5-works-terminal, not yet written today (46316-46321).
- Start/finish: tap "Notice board" (the terminal is not an item; the board is 1.25 m from it) -> card "Write the log:
  Which one's your log for today?" with three summaries -> pick -> toast "Works log: Logged. Calder will read it."
  First time: lesson train.m12.calder + toast "Trained: the logbook, with Chief Ines Calder." + notes Mail (tapD3).
- Told today: nothing. No word that the notice board is where the log is written; outside 16:30-17:30 the notice
  board does its ordinary thing. On Fridays the shift ends 15:30, so the player is usually gone by 16:30.
- Verdict: **WORKS BUT HIDDEN** (very hard to find by chance: a narrow window, a misleading item name).
  Note for testers: Dev mode's clock skip marks skipped workdays as excused (devmodeExcused, careerOff 40103), so
  playerShiftOn is false and the tap silently does nothing after a skip; that is a test trap, not a player bug.
- Arrow moments: workdays from the row's opening, 16:30 (or at clock-out if later, while not written): item "Notice
  board" (place 5-works-terminal), Deck 5 w, "Write today's log: the notice board". Goes when written or at 17:30.
  Existing arrow can (`place:'5-works-terminal'`); needs a time-window goal source. Better still: rename the item's
  title in that window or add a tip at the board.

## M13 Leak hunting (24o, 48858-49041)
- What: once a week a joint drips; follow the puddle and the damp to the joint and tighten it (or fetch a new joint).
- Unlock: row m13 small; opens **Day 19** steady (Day 18 without m9). The first leak posts that same day at 08:00
  (ladderD: Day 18 08:00 Deck 3; ladderD2: Day 19 08:00 Deck 3 joint 3-leak-4), then one a week on a workday.
- Start/finish: board job "A pipe drips somewhere on Deck 3" (a normal board job; takes your one board slot). Stops:
  look at the puddle, look at the damp, tighten (a turn to 3) -> "Dry. Found it yourself." First puddle look = the
  training (worksTrained in leakStepDone 48943). Not taken: crew do it the long way (an hour) at shift end + 1 h.
- Told today: only the board line. **No "New job" toast** (jobNotice 14029 needs j.machine). After you take it the
  arrow (ixJobStep chore path) points straight at the puddle place with the label "A pipe drips somewhere on Deck 3".
  In both runs the crew fixed it unseen (found: 'quist-ilse', 'eklund-leila'); the "crew found it the long way" toast
  only shows once you are trained (48960), so a player who never saw it hears nothing.
- Verdict: **WORKS BUT HIDDEN** (on the board, but unannounced and easy to miss among service jobs).
- Arrow moments:
  1. Leak posted (08:00 that day) while you hold no job: Deck 5 item "Job board", "A leak on Deck 3: job board".
     ixWorkStep (15712) already points at the board when openJobs is non-empty, but its label is generic; a leak-
     specific label or a one-time tip is needed. Fix jobNotice to include kind 'leak' (14029).
  2. Taken: existing job arrow works (puddle, then damp, then joint). Its label stays the board title at every stop;
     better per-stop labels: "Look at the puddle", "Follow the damp up the wall", "Tighten the joint" (ixJobStep's
     chore branch already reads the next stop; add a label from the stop's tag).

## M14 Garden irrigation (24r, 49168-49260)
- What: on a harvest Saturday morning, clear the clogged nozzles on the garden's three grow racks (Deck 3).
- Unlock: row m14 small, day 13; opens only on a workday and one small row a day, so **Day 22** steady (Day 19
  without m9). The job then goes up only on a harvest day (gardenHarvestDay 16497); harvests in this save fall on
  Days 6, 20, 34 (every two weeks). So the first nozzle job is **Day 34** for a steady player (Day 20 in ladderD,
  posted then: "Clear the nozzles", 4 clogged).
- Start/finish: board job "Clear the nozzles" (Deck 3, leave 1440), from the harvesters' first pick to midnight.
  Holds at 3-rack-1..3; first rack = the training (gardener's lesson). Salad toast that evening 18:00-21:00.
- Told today: only the board line on a Saturday (no "New job" toast: no machine, 14029; ixWorkStep's board arrow is
  shift-only, 15710). The player has no reason to visit the Works bay on a Saturday. A board job still needs your one
  board slot. Ship traditions Mail the evening before says "Harvest morning 09:30" but nothing about nozzles.
- Verdict: **WORKS BUT HIDDEN**, and very late (Day 34 for a steady player, against the design's "first harvest from
  Day 13", step4-summary). The cause is the one-small-row-a-workday rule plus "workdays only" (45177, 45186) for a
  weekend job. Repro: ladderD2.py (m14 opens Day 22; harvest Day 20 passes with the row closed).
- Arrow moments:
  1. Evening before the harvest (with the traditions Mail, 18:00), once the row is open: no arrow; a Mail/tip line
     "Harvest tomorrow: the racks' nozzles need clearing".
  2. Harvest morning from the job's posting: Deck 3, place of the first rack with clogged nozzles (nozStops' first
     placeId, e.g. 3-rack-1), "Clear the nozzles: grow rack 1". The job must be taken first; better to let the arrow
     lead to the board, or let a tap on the rack take it. Needs an off-shift goal source (ixWorkStep is shift-only).
  3. Each rack done: next rack's place, "Next rack". Goes when all clear. Existing job arrow can do 2-3 once taken.

## M15 Rewiring with the conduit tester (24q, 49042-49167; big row Day 17)
- What: rewire a junction box by its colour chart (open, pair each wire to its terminal, test).
- Unlock: row m15 big, day 17, Calder on shift, W.cur empty (45185). Steady run: asked Day 17 06:05, meeting 08:40 at
  Deck 4 room '-' (officers' corridor utility closet), Calder rewires 4-junction-2 while you watch (10 min), then
  4-junction-1 held for you; trained when you turn it in; the tester is given. Afterwards one rewiring a week at
  08:00 on a workday (49158). If m9's training is still open (cur 'ask'), m15 never opens (ladderD, Days 17-26).
- Told today (ladderD2): Day 17 06:05 Mail + toast from Calder (the ask, with time and place), arrow "rewiring with
  Ines, 08:40" @D4 '-' (only because no job was tracked: trainTell 45268). Meeting dialogue train.m15.calder. Then
  bubble "Follow me. Watch this one." (trainWatch). Weekly jobs: "New job: Rewire junction 4-J2 ..." toast (has a
  machine), board line "Rewire junction 4-J2".
- Verdict: **BROKEN for most players** (as AR1 found): a player who took any job before (every steady player) gets no
  meeting arrow (45268), and the old m9 meeting arrow (or a team job's) is still up, pointing elsewhere. The meeting
  is at 08:40, before the 09:00 clock-in, while the clock-in arrow and toasts pull the player to Deck 5. Repro: play
  Day 12 normally (take a job), set career to Day 16, skip to Day 17 06:00: Mail and toast arrive, the arrow stays on
  "tracing with Ines, 09:20". trainWatch sets no arrow to Calder's job (45289; only the escort walk).
  Mechanics past the meeting: WORKS (ladderD2 trained via the hand-simulated meeting; mech_check covers the steps).
- Arrow moments:
  1. Ask told (06:00-08:40): Deck 4 room '-', "Rewiring with Calder, 08:40". Over a tracked job's arrow (the meeting
     is time-bound). Goes when the meeting starts. Existing arrow can, if trainTell drops the track check / clears it.
  2. Watching: Calder (goal `crew:'calder'`) or 4-junction-2's panel, "Watch Calder rewire the box". Goes at your turn.
  3. Your turn: the reserved job 4-junction-1 is on the board: Deck 5 "Job board", "Your rewiring job: job board",
     then the job's own arrow (panel of 4-junction-1). Existing job arrow, labels per stop would help ("Open the box",
     "Match the wires", "Test it").
  4. Weekly job: covered by the board and the New job toast.

## M17 The lift roof (24s, 46985-47232; big row Day 18)
- What: Thursdays 15:30-16:30, climb on the main lift's roof on Deck 1 and grease each deck's guide on the way down.
- Unlock: row m17 big, day 18; offer only on a Thursday at or before 15:00 with Halloran on shift (47212) and only if
  no other training is under way (45185) and m15 has opened first (table order). Steady run: asked Day 18 06:05,
  meeting 15:30 Deck 1 room '+', trained at the meeting (noJob). Then roofOpen 15:30 to about 16:10 (roofLen 20 min).
- Start/finish: after the meeting, tap the lift (doors or "Lift panel") on Deck 1 -> card "The lift roof: ... Climb
  onto the roof / Ride inside" -> ride (about 20 ship min) -> out on Deck 6. tapD3: rides 1, Halloran's toasts
  "Up you get. Harness clipped? Lovely." ... "Smoother already. Can you feel it? Lovely work.", end on Deck 6.
- Told today (ladderD2): 06:05 Mail + toast from Halloran ("Meet me at the lift on Deck 1 at 15:30: we're riding the
  roof."), arrow "the lift roof with Emeka, 15:30" @D1 '+' — replaced at 09:37 by a team job's arrow and never
  restored. After the meeting: toast "Trained: the lift roof, with Emeka Halloran." Nothing points at the lift, and the
  meeting script's last line is the only hint ("Up you get"). Lift held 15:30-16:30 toasts "Held for maintenance".
- Verdict: **BROKEN for most players** (same arrow causes as M15: no meeting arrow while a job is tracked, 45268;
  other arrows override it; nothing leads from the meeting to the lift; a 40-minute window). Also slips a week if
  m15's training is not finished by Thursday morning (cur blocks big rows, 45185), and never opens if any earlier
  training is stuck. Ride itself: WORKS (tapD3, no errors).
- Arrow moments:
  1. Ask told (06:00-15:30, Thursday): Deck 1 room '+', "The lift roof with Emeka, 15:30". Over a tracked job only from
     about 15:15 (the time-bound part). Goes at the meeting.
  2. Trained (meeting over) until 16:10 or the climb: Deck 1 item "Lift panel" (or LIFT_AT), "Climb onto the lift roof".
     New: a goal set at worksTrained('m17') when roofOpen(); cleared by roofClimb or when roofOpen() goes false.
  3. Later Thursdays 15:30-16:10 (stage 0-1, optional): a tip, not an arrow ("Thursday: the lift's maintenance hour").

## Other things seen (outside the brief, for the backlog)
- tapD/ladderD Mail log shows Tomas Lind's "Tonight?" body as JS source ("(c, p) => tradText(t, 'ask', c, p)",
  Days 15, 16, 19; 36030 and 38564 make body a function). Probably our logger's String(m.body) and not on screen;
  worth one look at the Mail app.
- "Yesterday's clothes" toast every day after a Dev skip (expected after skips).

## Summary of verdicts
- BROKEN: M15 meeting (no arrow when a job is tracked; stale arrows; 08:40 before clock-in), M17 meeting and the step
  from meeting to lift; M10's "follow the marker" toast with no marker for side jobs.
- WORKS BUT HIDDEN: M10 order board and tinkering, cabin touches, star logging, M11 bench, M12 logbook (worst: odd
  item, narrow window), M13 leaks (no New job toast), M14 irrigation (no announcement, weekend, first job Day 34).
- Structural: small rows open silently one a workday (m11 Day 17, m12 18, m13 19, m14 22 for a steady player);
  What's next never mentions side jobs; side jobs have no arrow (myJob 19180); jobNotice ignores jobs with no machine
  (14029).
- New arrow plumbing needed: a goal source for side jobs (mySideJobs / shopData), time-window goals (log 16:30, stars
  20:00, roof after the meeting), off-shift goals (harvest Saturday), a `crew:` goal for hand-overs, and per-stop
  labels for chore-path jobs (leak, nozzles, rewire).
